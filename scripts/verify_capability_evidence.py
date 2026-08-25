#!/usr/bin/env python3
"""Fail closed when capability status outruns executable evidence."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("governance/CAPABILITY_REGISTRY.json")
POLICY_PATH = Path("governance/BEHAVIOR_FIRST_CAPABILITY_POLICY.md")
RUN_CONTRACT_PATH = Path("governance/P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md")

STATUSES = [
    "PROPOSED",
    "IMPLEMENTED",
    "TESTED",
    "INTEGRATION_TESTED",
    "OBSERVED_IN_REAL_WORK",
    "RELIABLE",
]
RANK = {status: index for index, status in enumerate(STATUSES)}
CLAIM_RE = re.compile(r"CAPABILITY CLAIM:\s*(CAP-[A-Z0-9-]+)\b")
ID_RE = re.compile(r"^CAP-[A-Z0-9-]+$")

LIST_FIELDS = [
    "implementation",
    "executable_evidence",
    "failure_evidence",
    "integration_evidence",
    "real_work_evidence",
    "reliability_evidence",
    "ci_commands",
    "integration_ci_commands",
]


def _list(entry: dict, field: str, errors: list[str], cap_id: str) -> list[str]:
    value = entry.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{cap_id}: {field} must be a list of non-empty strings")
        return []
    return value


def _existing_paths(root: Path, cap_id: str, field: str, values: Iterable[str], errors: list[str]) -> None:
    for value in values:
        path = root / value
        if not path.is_file():
            errors.append(f"{cap_id}: {field} path does not exist: {value}")


def _python_stub_errors(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (UnicodeDecodeError, SyntaxError) as exc:
        return [f"cannot inspect registered Python implementation {path}: {exc}"]

    issues: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Pass):
            issues.append(f"obvious stub `pass` at {path}:{node.lineno}")
        if isinstance(node, ast.Raise):
            exc = node.exc
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "NotImplementedError":
                issues.append(f"NotImplementedError stub at {path}:{node.lineno}")
            if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
                issues.append(f"NotImplementedError stub at {path}:{node.lineno}")
    return issues


def _implementation_stub_errors(root: Path, cap_id: str, implementations: Iterable[str]) -> list[str]:
    issues: list[str] = []
    for value in implementations:
        path = root / value
        if not path.is_file():
            continue
        if path.suffix == ".py":
            for issue in _python_stub_errors(path):
                issues.append(f"{cap_id}: {issue}")
    return issues


def _workflow_text(root: Path) -> str:
    workflow_root = root / ".github" / "workflows"
    if not workflow_root.is_dir():
        return ""
    chunks: list[str] = []
    for path in sorted(workflow_root.glob("*.y*ml")):
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def _formal_claim_errors(root: Path, registered_ids: set[str]) -> list[str]:
    errors: list[str] = []
    ignored_parts = {".git"}
    for path in root.rglob("*.md"):
        if ignored_parts.intersection(path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for cap_id in CLAIM_RE.findall(content):
            if cap_id not in registered_ids:
                errors.append(f"unregistered formal claim {cap_id} in {path.relative_to(root)}")
    return errors


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    registry_file = root / REGISTRY_PATH

    for required in [root / POLICY_PATH, root / RUN_CONTRACT_PATH, registry_file]:
        if not required.is_file():
            errors.append(f"required governance file missing: {required.relative_to(root)}")

    if not registry_file.is_file():
        return errors

    try:
        registry = json.loads(registry_file.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid capability registry: {exc}")
        return errors

    if registry.get("schema_version") != 1:
        errors.append("registry schema_version must be 1")
    if registry.get("allowed_statuses") != STATUSES:
        errors.append("registry allowed_statuses must exactly match the frozen status ladder")

    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list):
        errors.append("registry capabilities must be a list")
        return errors

    workflow_text = _workflow_text(root)
    seen: set[str] = set()

    for entry in capabilities:
        if not isinstance(entry, dict):
            errors.append("each capability must be an object")
            continue

        cap_id = entry.get("id")
        name = entry.get("name")
        claim = entry.get("claim")
        status = entry.get("status")

        if not isinstance(cap_id, str) or not ID_RE.fullmatch(cap_id):
            errors.append(f"invalid capability id: {cap_id!r}")
            continue
        if cap_id in seen:
            errors.append(f"duplicate capability id: {cap_id}")
        seen.add(cap_id)

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{cap_id}: name must be non-empty")
        if not isinstance(claim, str) or not claim.strip():
            errors.append(f"{cap_id}: claim must be non-empty")
        if status not in RANK:
            errors.append(f"{cap_id}: invalid status {status!r}")
            continue

        values = {field: _list(entry, field, errors, cap_id) for field in LIST_FIELDS}

        if RANK[status] >= RANK["IMPLEMENTED"]:
            if not values["implementation"]:
                errors.append(f"{cap_id}: IMPLEMENTED+ requires implementation")
            _existing_paths(root, cap_id, "implementation", values["implementation"], errors)
            errors.extend(_implementation_stub_errors(root, cap_id, values["implementation"]))

        if RANK[status] >= RANK["TESTED"]:
            if not values["executable_evidence"]:
                errors.append(f"{cap_id}: TESTED+ requires executable_evidence")
            if not values["failure_evidence"]:
                errors.append(f"{cap_id}: TESTED+ requires failure_evidence")
            if not values["ci_commands"]:
                errors.append(f"{cap_id}: TESTED+ requires ci_commands")
            _existing_paths(root, cap_id, "executable_evidence", values["executable_evidence"], errors)
            _existing_paths(root, cap_id, "failure_evidence", values["failure_evidence"], errors)
            for command in values["ci_commands"]:
                if command not in workflow_text:
                    errors.append(f"{cap_id}: CI does not execute declared command: {command}")

        if RANK[status] >= RANK["INTEGRATION_TESTED"]:
            if not values["integration_evidence"]:
                errors.append(f"{cap_id}: INTEGRATION_TESTED+ requires integration_evidence")
            if not values["integration_ci_commands"]:
                errors.append(f"{cap_id}: INTEGRATION_TESTED+ requires integration_ci_commands")
            _existing_paths(root, cap_id, "integration_evidence", values["integration_evidence"], errors)
            for command in values["integration_ci_commands"]:
                if command not in workflow_text:
                    errors.append(f"{cap_id}: CI does not execute integration command: {command}")

        if RANK[status] >= RANK["OBSERVED_IN_REAL_WORK"]:
            if not values["real_work_evidence"]:
                errors.append(f"{cap_id}: OBSERVED_IN_REAL_WORK+ requires real_work_evidence")
            _existing_paths(root, cap_id, "real_work_evidence", values["real_work_evidence"], errors)

        if status == "RELIABLE":
            if len(set(values["real_work_evidence"])) < 2:
                errors.append(f"{cap_id}: RELIABLE requires at least two independent real_work_evidence paths")
            if not values["reliability_evidence"]:
                errors.append(f"{cap_id}: RELIABLE requires reliability_evidence")
            _existing_paths(root, cap_id, "reliability_evidence", values["reliability_evidence"], errors)

    errors.extend(_formal_claim_errors(root, seen))
    return errors


def main() -> int:
    errors = validate_repository(ROOT)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    registry = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
    print(f"[PASS] capability evidence gate: {len(registry['capabilities'])} registered capabilities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
