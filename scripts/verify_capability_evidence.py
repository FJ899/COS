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

_TRUTH_FALSE = 0
_TRUTH_TRUE = 1
_TRUTH_UNKNOWN = 2


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


def _literal_value(node: ast.AST) -> tuple[bool, object]:
    try:
        return True, ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False, None


def _static_truthiness(node: ast.AST) -> int:
    known, value = _literal_value(node)
    if known:
        return _TRUTH_TRUE if bool(value) else _TRUTH_FALSE

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        truth = _static_truthiness(node.operand)
        if truth == _TRUTH_TRUE:
            return _TRUTH_FALSE
        if truth == _TRUTH_FALSE:
            return _TRUTH_TRUE
        return _TRUTH_UNKNOWN

    if isinstance(node, ast.BoolOp):
        truths = [_static_truthiness(item) for item in node.values]
        if isinstance(node.op, ast.Or):
            if any(truth == _TRUTH_TRUE for truth in truths):
                return _TRUTH_TRUE
            if all(truth == _TRUTH_FALSE for truth in truths):
                return _TRUTH_FALSE
        elif isinstance(node.op, ast.And):
            if any(truth == _TRUTH_FALSE for truth in truths):
                return _TRUTH_FALSE
            if all(truth == _TRUTH_TRUE for truth in truths):
                return _TRUTH_TRUE
        return _TRUTH_UNKNOWN

    if isinstance(node, ast.Compare):
        known, left = _literal_value(node.left)
        if not known:
            return _TRUTH_UNKNOWN
        for operator, comparator in zip(node.ops, node.comparators):
            known, right = _literal_value(comparator)
            if not known:
                return _TRUTH_UNKNOWN
            try:
                if isinstance(operator, ast.Eq):
                    matches = left == right
                elif isinstance(operator, ast.NotEq):
                    matches = left != right
                elif isinstance(operator, ast.Lt):
                    matches = left < right
                elif isinstance(operator, ast.LtE):
                    matches = left <= right
                elif isinstance(operator, ast.Gt):
                    matches = left > right
                elif isinstance(operator, ast.GtE):
                    matches = left >= right
                elif isinstance(operator, ast.Is):
                    matches = left is right
                elif isinstance(operator, ast.IsNot):
                    matches = left is not right
                elif isinstance(operator, ast.In):
                    matches = left in right
                elif isinstance(operator, ast.NotIn):
                    matches = left not in right
                else:
                    return _TRUTH_UNKNOWN
            except (TypeError, ValueError):
                return _TRUTH_UNKNOWN
            if not matches:
                return _TRUTH_FALSE
            left = right
        return _TRUTH_TRUE

    if isinstance(node, ast.IfExp):
        condition = _static_truthiness(node.test)
        if condition == _TRUTH_TRUE:
            return _static_truthiness(node.body)
        if condition == _TRUTH_FALSE:
            return _static_truthiness(node.orelse)
        body = _static_truthiness(node.body)
        orelse = _static_truthiness(node.orelse)
        if body == orelse and body != _TRUTH_UNKNOWN:
            return body

    return _TRUTH_UNKNOWN


def _expr_has_runtime_dependency(node: ast.AST) -> bool:
    if isinstance(node, (ast.Constant, ast.Name, ast.Lambda)):
        return False
    if isinstance(node, ast.Call):
        return True
    if isinstance(node, (ast.Await, ast.Yield, ast.YieldFrom, ast.Attribute, ast.Subscript)):
        return True
    if isinstance(node, ast.BoolOp):
        for item in node.values:
            if _expr_has_runtime_dependency(item):
                return True
            truth = _static_truthiness(item)
            if isinstance(node.op, ast.Or) and truth == _TRUTH_TRUE:
                break
            if isinstance(node.op, ast.And) and truth == _TRUTH_FALSE:
                break
        return False
    if isinstance(node, ast.IfExp):
        if _expr_has_runtime_dependency(node.test):
            return True
        condition = _static_truthiness(node.test)
        if condition == _TRUTH_TRUE:
            return _expr_has_runtime_dependency(node.body)
        if condition == _TRUTH_FALSE:
            return _expr_has_runtime_dependency(node.orelse)
        return _expr_has_runtime_dependency(node.body) or _expr_has_runtime_dependency(node.orelse)
    if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        return True
    return any(_expr_has_runtime_dependency(child) for child in ast.iter_child_nodes(node))


def _unittest_assertion_is_constant_success(call: ast.Call) -> bool:
    if not isinstance(call.func, ast.Attribute) or not call.func.attr.startswith("assert"):
        return False
    name = call.func.attr
    if name.startswith("assertRaises") or name.startswith("assertWarns"):
        return False
    if any(_expr_has_runtime_dependency(arg) for arg in call.args):
        return False
    if any(_expr_has_runtime_dependency(keyword.value) for keyword in call.keywords):
        return False
    if not call.args:
        return False

    if name == "assertTrue":
        return _static_truthiness(call.args[0]) == _TRUTH_TRUE
    if name == "assertFalse":
        return _static_truthiness(call.args[0]) == _TRUTH_FALSE
    if name in {"assertIsNone", "assertIsNotNone"}:
        known, value = _literal_value(call.args[0])
        if not known:
            return False
        return (value is None) if name == "assertIsNone" else (value is not None)

    if name not in {"assertEqual", "assertNotEqual", "assertIs", "assertIsNot"} or len(call.args) < 2:
        return False
    left_known, left = _literal_value(call.args[0])
    right_known, right = _literal_value(call.args[1])
    if not left_known or not right_known:
        return False
    if name == "assertEqual":
        return left == right
    if name == "assertNotEqual":
        return left != right
    if name == "assertIs":
        return left is right
    return left is not right


def _is_main_guard(node: ast.If) -> bool:
    test = node.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False
    left = test.left
    right = test.comparators[0]
    return (
        isinstance(left, ast.Name)
        and left.id == "__name__"
        and isinstance(right, ast.Constant)
        and right.value == "__main__"
    ) or (
        isinstance(right, ast.Name)
        and right.id == "__name__"
        and isinstance(left, ast.Constant)
        and left.value == "__main__"
    )


def _block_is_provably_vacuous(statements: Iterable[ast.stmt]) -> bool:
    for node in statements:
        if isinstance(node, (ast.Pass, ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal)):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.Assert):
            if _expr_has_runtime_dependency(node.test):
                return False
            if _static_truthiness(node.test) == _TRUTH_TRUE:
                continue
            return False
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr.startswith("assert"):
                    if _unittest_assertion_is_constant_success(node.value):
                        continue
                    return False
            if _expr_has_runtime_dependency(node.value):
                return False
            continue
        if isinstance(node, ast.Assign):
            if _expr_has_runtime_dependency(node.value):
                return False
            if any(isinstance(target, (ast.Attribute, ast.Subscript)) for target in node.targets):
                return False
            continue
        if isinstance(node, ast.AnnAssign):
            if node.value is not None and _expr_has_runtime_dependency(node.value):
                return False
            if isinstance(node.target, (ast.Attribute, ast.Subscript)):
                return False
            continue
        if isinstance(node, ast.If):
            if _is_main_guard(node):
                continue
            if _expr_has_runtime_dependency(node.test):
                return False
            if not _block_is_provably_vacuous(node.body) or not _block_is_provably_vacuous(node.orelse):
                return False
            continue
        if isinstance(node, (ast.With, ast.AsyncWith)):
            if any(_expr_has_runtime_dependency(item.context_expr) for item in node.items):
                return False
            if not _block_is_provably_vacuous(node.body):
                return False
            continue
        if isinstance(node, ast.Try):
            blocks = [node.body, node.orelse, node.finalbody, *(handler.body for handler in node.handlers)]
            if any(not _block_is_provably_vacuous(block) for block in blocks):
                return False
            continue
        if isinstance(node, ast.While):
            if _expr_has_runtime_dependency(node.test):
                return False
            if _static_truthiness(node.test) == _TRUTH_FALSE:
                if not _block_is_provably_vacuous(node.orelse):
                    return False
                continue
            return False
        if isinstance(node, (ast.For, ast.AsyncFor)):
            if _expr_has_runtime_dependency(node.iter):
                return False
            known, value = _literal_value(node.iter)
            if known and hasattr(value, "__len__") and len(value) == 0:
                if not _block_is_provably_vacuous(node.orelse):
                    return False
                continue
            return False
        if isinstance(node, ast.Return):
            if node.value is not None and _expr_has_runtime_dependency(node.value):
                return False
            continue
        return False
    return True


def _python_evidence_is_vacuous(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (UnicodeDecodeError, SyntaxError):
        return False

    if not _block_is_provably_vacuous(tree.body):
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            if not _block_is_provably_vacuous(node.body):
                return False

    return True


def _evidence_vacuity_errors(
    root: Path, cap_id: str, field: str, values: Iterable[str]
) -> list[str]:
    issues: list[str] = []
    for value in values:
        path = root / value
        if not path.is_file() or path.suffix != ".py":
            continue
        if _python_evidence_is_vacuous(path):
            issues.append(
                f"{cap_id}: {field} evidence is behaviorally vacuous / unconditional-success: {value}"
            )
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
            errors.extend(
                _evidence_vacuity_errors(root, cap_id, "executable_evidence", values["executable_evidence"])
            )
            errors.extend(
                _evidence_vacuity_errors(root, cap_id, "failure_evidence", values["failure_evidence"])
            )
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
