#!/usr/bin/env python3
"""Fail closed when capability status outruns executable evidence."""

from __future__ import annotations

import ast
import json
import re
import shlex

import sys
from pathlib import Path
from typing import Iterable

import yaml

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
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{cap_id}: {field} must be a list of non-empty strings")
        return []
    return value


def _repository_file(root: Path, value: str) -> Path | None:
    """Require canonical, repository-local files, including symlink targets."""
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts or "\\" in value:
        return None
    try:
        resolved = (root / relative).resolve(strict=True)
        resolved.relative_to(root.resolve())
        return resolved if resolved.is_file() else None
    except (OSError, RuntimeError, ValueError):
        return None


def _existing_paths(root: Path, cap_id: str, field: str, values: Iterable[str], errors: list[str]) -> None:
    for value in values:
        if _repository_file(root, value) is None:
            errors.append(f"{cap_id}: {field} path does not exist or escapes repository: {value}")


def _python_stub_errors(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
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
        path = _repository_file(root, value)
        if path is None:
            continue
        if path.suffix == ".py":
            for issue in _python_stub_errors(path):
                issues.append(f"{cap_id}: {issue}")
    return issues


def _tokens(command: str) -> tuple[str, ...]:
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = tuple(lexer)
        if any(token in {";", "&&", "||", "|", "&", ">", ">>", "<", "<<", "(", ")"} or "$" in token or "`" in token for token in tokens):
            return ()
        return tokens
    except ValueError:
        return ()


def _workflow_commands(root: Path, errors: list[str]) -> set[tuple[str, ...]]:
    """Read actual unconditional root-level run steps; never execute registry input.

    This checks declarations, not GitHub run results. Complex shell wrappers,
    reusable workflows and conditional jobs need explicit review.
    """
    commands: set[tuple[str, ...]] = set()
    workflow_root = root / ".github" / "workflows"
    paths = sorted(set(workflow_root.glob("*.yml")) | set(workflow_root.glob("*.yaml")))
    for path in paths:
        try:
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"cannot inspect workflow {path.name}: {exc}")
            continue
        if not isinstance(workflow, dict):
            errors.append(f"workflow {path.name} must be a mapping")
            continue
        # PyYAML's YAML 1.1 loader reads the unquoted Actions key 'on' as True.
        events = workflow.get("on", workflow.get(True))
        if isinstance(events, str):
            events = [events]
        if not isinstance(events, (list, dict)) or "pull_request" not in events:
            continue
        jobs = workflow.get("jobs", {})
        if not isinstance(jobs, dict):
            errors.append(f"workflow {path.name} jobs must be a mapping")
            continue
        for job in jobs.values():
            if not isinstance(job, dict) or "uses" in job:
                continue
            if job.get("if", True) is not True or job.get("continue-on-error", False) is not False:
                continue
            steps = job.get("steps", [])
            if not isinstance(steps, list):
                errors.append(f"workflow {path.name} steps must be a list")
                continue
            for step in steps:
                if not isinstance(step, dict) or not isinstance(step.get("run"), str):
                    continue
                if step.get("if", True) is not True or step.get("continue-on-error", False) is not False:
                    continue
                defaults = workflow.get("defaults", {})
                job_defaults = job.get("defaults", {})
                if not isinstance(defaults, dict) or not isinstance(job_defaults, dict):
                    continue
                global_run = defaults.get("run", {})
                job_run = job_defaults.get("run", {})
                if not isinstance(global_run, dict) or not isinstance(job_run, dict):
                    continue
                run_defaults = {**global_run, **job_run}
                directory = step.get("working-directory", run_defaults.get("working-directory", "."))
                if directory not in (".", "./"):
                    continue
                shell = step.get("shell", run_defaults.get("shell", "bash"))
                if shell != "bash":
                    continue
                lines = [line.strip() for line in step["run"].splitlines()
                         if line.strip() and not line.lstrip().startswith("#")]
                parsed = [_tokens(line) for line in lines]
                # Reject the whole block if shell flow can skip/mask a command.
                if parsed and all(tokens and tokens[0] in {"python", "python3"} for tokens in parsed):
                    commands.update(parsed)
    return commands


def _formal_claim_errors(root: Path, registered_ids: set[str]) -> list[str]:
    errors: list[str] = []
    ignored_parts = {".git"}
    for path in root.rglob("*.md"):
        if ignored_parts.intersection(path.parts):
            continue
        if _repository_file(root, str(path.relative_to(root))) is None:
            errors.append(f"formal claim document escapes repository or is unavailable: {path.relative_to(root)}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"cannot inspect formal claim document {path.relative_to(root)}: {exc}")
            continue
        for cap_id in CLAIM_RE.findall(content):
            if cap_id not in registered_ids:
                errors.append(f"unregistered formal claim {cap_id} in {path.relative_to(root)}")
    return errors


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    registry_file = root / REGISTRY_PATH

    for required in [root / POLICY_PATH, root / RUN_CONTRACT_PATH, registry_file]:
        if not required.is_file():
            errors.append(f"required governance file missing: {required.relative_to(root)}")

    if not registry_file.is_file():
        return errors

    try:
        registry = json.loads(registry_file.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        errors.append(f"invalid capability registry: {exc}")
        return errors

    if not isinstance(registry, dict):
        return errors + ["capability registry must be an object"]

    if type(registry.get("schema_version")) is not int or registry.get("schema_version") != 1:
        errors.append("registry schema_version must be 1")
    if registry.get("allowed_statuses") != STATUSES:
        errors.append("registry allowed_statuses must exactly match the frozen status ladder")

    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list):
        errors.append("registry capabilities must be a list")
        return errors

    workflow_commands = _workflow_commands(root, errors)
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
        if not isinstance(status, str) or status not in RANK:
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
                if not _tokens(command) or _tokens(command) not in workflow_commands:
                    errors.append(f"{cap_id}: CI does not execute declared command: {command}")

        if RANK[status] >= RANK["INTEGRATION_TESTED"]:
            if not values["integration_evidence"]:
                errors.append(f"{cap_id}: INTEGRATION_TESTED+ requires integration_evidence")
            if not values["integration_ci_commands"]:
                errors.append(f"{cap_id}: INTEGRATION_TESTED+ requires integration_ci_commands")
            _existing_paths(root, cap_id, "integration_evidence", values["integration_evidence"], errors)
            for command in values["integration_ci_commands"]:
                if not _tokens(command) or _tokens(command) not in workflow_commands:
                    errors.append(f"{cap_id}: CI does not execute integration command: {command}")

        if RANK[status] >= RANK["OBSERVED_IN_REAL_WORK"]:
            if not values["real_work_evidence"]:
                errors.append(f"{cap_id}: OBSERVED_IN_REAL_WORK+ requires real_work_evidence")
            _existing_paths(root, cap_id, "real_work_evidence", values["real_work_evidence"], errors)

        if status == "RELIABLE":
            if len({_repository_file(root, value) for value in values["real_work_evidence"]} - {None}) < 2:
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
