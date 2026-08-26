#!/usr/bin/env python3
"""Fail closed when capability status outruns executable evidence."""

from __future__ import annotations

import ast
import fnmatch
import json
import re
import shlex
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
_EXEC_DIRECT = "direct"
_EXEC_UNITTEST_DISCOVERY = "unittest-discovery"


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


def _literal_value(node: ast.AST, constants: dict[str, object] | None = None) -> tuple[bool, object]:
    if constants is not None and isinstance(node, ast.Name) and node.id in constants:
        return True, constants[node.id]
    try:
        return True, ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False, None


def _static_truthiness(node: ast.AST, constants: dict[str, object] | None = None) -> int:
    known, value = _literal_value(node, constants)
    if known:
        return _TRUTH_TRUE if bool(value) else _TRUTH_FALSE

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        truth = _static_truthiness(node.operand, constants)
        if truth == _TRUTH_TRUE:
            return _TRUTH_FALSE
        if truth == _TRUTH_FALSE:
            return _TRUTH_TRUE
        return _TRUTH_UNKNOWN

    if isinstance(node, ast.BoolOp):
        truths = [_static_truthiness(item, constants) for item in node.values]
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
        known, left = _literal_value(node.left, constants)
        if not known:
            return _TRUTH_UNKNOWN
        for operator, comparator in zip(node.ops, node.comparators):
            known, right = _literal_value(comparator, constants)
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
        condition = _static_truthiness(node.test, constants)
        if condition == _TRUTH_TRUE:
            return _static_truthiness(node.body, constants)
        if condition == _TRUTH_FALSE:
            return _static_truthiness(node.orelse, constants)
        body = _static_truthiness(node.body, constants)
        orelse = _static_truthiness(node.orelse, constants)
        if body == orelse and body != _TRUTH_UNKNOWN:
            return body

    return _TRUTH_UNKNOWN


def _expr_has_runtime_dependency(node: ast.AST, constants: dict[str, object] | None = None) -> bool:
    if isinstance(node, (ast.Constant, ast.Name, ast.Lambda)):
        return False
    if isinstance(node, ast.Call):
        return True
    if isinstance(node, (ast.Await, ast.Yield, ast.YieldFrom, ast.Attribute, ast.Subscript)):
        return True
    if isinstance(node, ast.BoolOp):
        for item in node.values:
            if _expr_has_runtime_dependency(item, constants):
                return True
            truth = _static_truthiness(item, constants)
            if isinstance(node.op, ast.Or) and truth == _TRUTH_TRUE:
                break
            if isinstance(node.op, ast.And) and truth == _TRUTH_FALSE:
                break
        return False
    if isinstance(node, ast.IfExp):
        if _expr_has_runtime_dependency(node.test, constants):
            return True
        condition = _static_truthiness(node.test, constants)
        if condition == _TRUTH_TRUE:
            return _expr_has_runtime_dependency(node.body, constants)
        if condition == _TRUTH_FALSE:
            return _expr_has_runtime_dependency(node.orelse, constants)
        return _expr_has_runtime_dependency(node.body, constants) or _expr_has_runtime_dependency(
            node.orelse, constants
        )
    if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        return True
    return any(_expr_has_runtime_dependency(child, constants) for child in ast.iter_child_nodes(node))


def _static_assignment_value(
    node: ast.AST, constants: dict[str, object]
) -> tuple[bool, object]:
    known, value = _literal_value(node, constants)
    if known:
        return True, value
    truth = _static_truthiness(node, constants)
    if truth == _TRUTH_TRUE:
        return True, True
    if truth == _TRUTH_FALSE:
        return True, False
    return False, None


def _assigned_names(target: ast.AST) -> set[str]:
    return {node.id for node in ast.walk(target) if isinstance(node, ast.Name)}


def _record_static_assignment(
    target: ast.AST,
    known: bool,
    value: object,
    constants: dict[str, object],
) -> None:
    if isinstance(target, ast.Name):
        if known:
            constants[target.id] = value
        else:
            constants.pop(target.id, None)
        return

    if isinstance(target, (ast.Tuple, ast.List)):
        if known and isinstance(value, (tuple, list)) and len(target.elts) == len(value):
            for element, item in zip(target.elts, value):
                _record_static_assignment(element, True, item, constants)
            return
        for name in _assigned_names(target):
            constants.pop(name, None)


def _merge_static_constants(
    destination: dict[str, object],
    left: dict[str, object],
    right: dict[str, object],
) -> None:
    destination.clear()
    for name in left.keys() & right.keys():
        left_value = left[name]
        right_value = right[name]
        try:
            same = type(left_value) is type(right_value) and left_value == right_value
        except (TypeError, ValueError):
            same = False
        if same:
            destination[name] = left_value


def _unittest_assertion_is_constant_success(
    call: ast.Call, constants: dict[str, object]
) -> bool:
    if not isinstance(call.func, ast.Attribute) or not call.func.attr.startswith("assert"):
        return False
    name = call.func.attr
    if name.startswith("assertRaises") or name.startswith("assertWarns"):
        return False
    if any(_expr_has_runtime_dependency(arg, constants) for arg in call.args):
        return False
    if any(_expr_has_runtime_dependency(keyword.value, constants) for keyword in call.keywords):
        return False
    if not call.args:
        return False

    if name == "assertTrue":
        return _static_truthiness(call.args[0], constants) == _TRUTH_TRUE
    if name == "assertFalse":
        return _static_truthiness(call.args[0], constants) == _TRUTH_FALSE
    if name in {"assertIsNone", "assertIsNotNone"}:
        known, value = _literal_value(call.args[0], constants)
        if not known:
            return False
        return (value is None) if name == "assertIsNone" else (value is not None)

    if name not in {"assertEqual", "assertNotEqual", "assertIs", "assertIsNot"} or len(call.args) < 2:
        return False
    left_known, left = _literal_value(call.args[0], constants)
    right_known, right = _literal_value(call.args[1], constants)
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


def _python_command_parts(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return []


def _is_python_executable(value: str) -> bool:
    return re.fullmatch(r"python(?:3(?:\.\d+)?)?", value) is not None


def _command_executes_python_path_directly(command: str, evidence_path: str) -> bool:
    parts = _python_command_parts(command)
    return len(parts) >= 2 and _is_python_executable(parts[0]) and parts[1] == evidence_path


def _unittest_discovery_covers_path(command: str, evidence_path: str) -> bool:
    parts = _python_command_parts(command)
    if len(parts) < 4 or not _is_python_executable(parts[0]):
        return False
    if parts[1:4] != ["-m", "unittest", "discover"]:
        return False

    start_directory = "."
    pattern = "test*.py"
    index = 4
    while index < len(parts):
        token = parts[index]
        if token in {"-s", "--start-directory"} and index + 1 < len(parts):
            start_directory = parts[index + 1]
            index += 2
            continue
        if token in {"-p", "--pattern"} and index + 1 < len(parts):
            pattern = parts[index + 1]
            index += 2
            continue
        index += 1

    normalized_path = evidence_path.replace("\\", "/").lstrip("./")
    normalized_start = start_directory.replace("\\", "/").strip("/")
    if normalized_start not in {"", "."}:
        prefix = normalized_start + "/"
        if not normalized_path.startswith(prefix):
            return False
    return fnmatch.fnmatch(Path(normalized_path).name, pattern)


def _python_evidence_execution_modes(evidence_path: str, ci_commands: Iterable[str]) -> set[str]:
    modes: set[str] = set()
    for command in ci_commands:
        if _command_executes_python_path_directly(command, evidence_path):
            modes.add(_EXEC_DIRECT)
        if _unittest_discovery_covers_path(command, evidence_path):
            modes.add(_EXEC_UNITTEST_DISCOVERY)
    return modes


def _block_is_provably_vacuous(
    statements: Iterable[ast.stmt],
    *,
    main_guard_truth: int,
    constants: dict[str, object],
) -> bool:
    for node in statements:
        if isinstance(node, ast.Pass):
            continue
        if isinstance(node, ast.Import):
            for alias in node.names:
                constants.pop(alias.asname or alias.name.split(".", 1)[0], None)
            continue
        if isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                constants.clear()
            else:
                for alias in node.names:
                    constants.pop(alias.asname or alias.name, None)
            continue
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            constants.pop(node.name, None)
            continue
        if isinstance(node, ast.Assert):
            if _expr_has_runtime_dependency(node.test, constants):
                return False
            if _static_truthiness(node.test, constants) == _TRUTH_TRUE:
                continue
            return False
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr.startswith("assert"):
                    if _unittest_assertion_is_constant_success(node.value, constants):
                        continue
                    return False
            if _expr_has_runtime_dependency(node.value, constants):
                return False
            continue
        if isinstance(node, ast.Assign):
            if _expr_has_runtime_dependency(node.value, constants):
                return False
            if any(isinstance(target, (ast.Attribute, ast.Subscript)) for target in node.targets):
                return False
            known, value = _static_assignment_value(node.value, constants)
            for target in node.targets:
                _record_static_assignment(target, known, value, constants)
            continue
        if isinstance(node, ast.AnnAssign):
            if node.value is not None and _expr_has_runtime_dependency(node.value, constants):
                return False
            if isinstance(node.target, (ast.Attribute, ast.Subscript)):
                return False
            if node.value is None:
                _record_static_assignment(node.target, False, None, constants)
            else:
                known, value = _static_assignment_value(node.value, constants)
                _record_static_assignment(node.target, known, value, constants)
            continue
        if isinstance(node, ast.If):
            if _is_main_guard(node):
                condition = main_guard_truth
            else:
                if _expr_has_runtime_dependency(node.test, constants):
                    return False
                condition = _static_truthiness(node.test, constants)

            if condition == _TRUTH_TRUE:
                if not _block_is_provably_vacuous(
                    node.body, main_guard_truth=main_guard_truth, constants=constants
                ):
                    return False
                continue
            if condition == _TRUTH_FALSE:
                if not _block_is_provably_vacuous(
                    node.orelse, main_guard_truth=main_guard_truth, constants=constants
                ):
                    return False
                continue

            body_constants = dict(constants)
            orelse_constants = dict(constants)
            if not _block_is_provably_vacuous(
                node.body, main_guard_truth=main_guard_truth, constants=body_constants
            ):
                return False
            if not _block_is_provably_vacuous(
                node.orelse, main_guard_truth=main_guard_truth, constants=orelse_constants
            ):
                return False
            _merge_static_constants(constants, body_constants, orelse_constants)
            continue
        if isinstance(node, (ast.With, ast.AsyncWith)):
            if any(_expr_has_runtime_dependency(item.context_expr, constants) for item in node.items):
                return False
            if not _block_is_provably_vacuous(
                node.body, main_guard_truth=main_guard_truth, constants=constants
            ):
                return False
            continue
        if isinstance(node, ast.Try):
            blocks = [node.body, node.orelse, node.finalbody, *(handler.body for handler in node.handlers)]
            if any(
                not _block_is_provably_vacuous(
                    block, main_guard_truth=main_guard_truth, constants=dict(constants)
                )
                for block in blocks
            ):
                return False
            constants.clear()
            continue
        if isinstance(node, ast.While):
            if _expr_has_runtime_dependency(node.test, constants):
                return False
            if _static_truthiness(node.test, constants) == _TRUTH_FALSE:
                if not _block_is_provably_vacuous(
                    node.orelse, main_guard_truth=main_guard_truth, constants=constants
                ):
                    return False
                continue
            return False
        if isinstance(node, (ast.For, ast.AsyncFor)):
            if _expr_has_runtime_dependency(node.iter, constants):
                return False
            known, value = _literal_value(node.iter, constants)
            if known and hasattr(value, "__len__") and len(value) == 0:
                if not _block_is_provably_vacuous(
                    node.orelse, main_guard_truth=main_guard_truth, constants=constants
                ):
                    return False
                continue
            return False
        if isinstance(node, ast.Return):
            if node.value is not None and _expr_has_runtime_dependency(node.value, constants):
                return False
            continue
        return False
    return True


def _unittest_import_context(tree: ast.Module) -> dict[str, set[str]]:
    context = {
        "modules": set(),
        "TestCase": set(),
        "skip": set(),
        "skipIf": set(),
        "skipUnless": set(),
    }
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "unittest":
                    context["modules"].add(alias.asname or "unittest")
        elif isinstance(node, ast.ImportFrom) and node.module == "unittest":
            for alias in node.names:
                if alias.name in {"TestCase", "skip", "skipIf", "skipUnless"}:
                    context[alias.name].add(alias.asname or alias.name)
    return context


def _matches_unittest_symbol(
    expression: ast.AST,
    context: dict[str, set[str]],
    symbol: str,
) -> bool:
    if isinstance(expression, ast.Name):
        return expression.id in context[symbol]
    return (
        isinstance(expression, ast.Attribute)
        and isinstance(expression.value, ast.Name)
        and expression.value.id in context["modules"]
        and expression.attr == symbol
    )


def _unittest_decorator_definitely_skips(
    decorator: ast.AST,
    context: dict[str, set[str]],
    constants: dict[str, object],
) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    if _matches_unittest_symbol(decorator.func, context, "skip"):
        return True
    if _matches_unittest_symbol(decorator.func, context, "skipIf"):
        return bool(decorator.args) and _static_truthiness(decorator.args[0], constants) == _TRUTH_TRUE
    if _matches_unittest_symbol(decorator.func, context, "skipUnless"):
        return bool(decorator.args) and _static_truthiness(decorator.args[0], constants) == _TRUTH_FALSE
    return False


def _unittest_class_is_testcase(
    node: ast.ClassDef,
    context: dict[str, set[str]],
    known_testcase_names: set[str],
) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and (
            base.id in context["TestCase"] or base.id in known_testcase_names
        ):
            return True
        if _matches_unittest_symbol(base, context, "TestCase"):
            return True
    return False


def _unittest_testcase_classes(
    tree: ast.Module, context: dict[str, set[str]]
) -> list[ast.ClassDef]:
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    known_names: set[str] = set()
    discovered: list[ast.ClassDef] = []
    changed = True
    while changed:
        changed = False
        for node in classes:
            if node.name in known_names:
                continue
            if _unittest_class_is_testcase(node, context, known_names):
                known_names.add(node.name)
                discovered.append(node)
                changed = True
    return discovered


def _class_method_map(node: ast.ClassDef) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        child.name: child
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _function_body_is_provably_vacuous(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    module_constants: dict[str, object],
) -> bool:
    return _block_is_provably_vacuous(
        node.body,
        main_guard_truth=_TRUTH_FALSE,
        constants=dict(module_constants),
    )


def _unittest_discovery_is_provably_vacuous(
    tree: ast.Module,
    module_constants: dict[str, object],
) -> bool:
    context = _unittest_import_context(tree)
    testcase_classes = _unittest_testcase_classes(tree, context)

    top_level_functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if "load_tests" in top_level_functions:
        return False

    tests_by_class: list[
        tuple[
            ast.ClassDef,
            dict[str, ast.FunctionDef | ast.AsyncFunctionDef],
            list[ast.FunctionDef | ast.AsyncFunctionDef],
        ]
    ] = []
    for testcase_class in testcase_classes:
        methods = _class_method_map(testcase_class)
        test_methods = [method for name, method in methods.items() if name.startswith("test")]
        if test_methods:
            tests_by_class.append((testcase_class, methods, test_methods))

    if not tests_by_class:
        return True

    for fixture_name in ("setUpModule", "tearDownModule"):
        fixture = top_level_functions.get(fixture_name)
        if fixture is not None and not _function_body_is_provably_vacuous(fixture, module_constants):
            return False

    for testcase_class, methods, test_methods in tests_by_class:
        class_skipped = any(
            _unittest_decorator_definitely_skips(decorator, context, module_constants)
            for decorator in testcase_class.decorator_list
        )
        if class_skipped:
            continue

        for fixture_name in ("setUpClass", "tearDownClass"):
            fixture = methods.get(fixture_name)
            if fixture is not None and not _function_body_is_provably_vacuous(fixture, module_constants):
                return False

        setup = methods.get("setUp")
        teardown = methods.get("tearDown")
        for test_method in test_methods:
            if any(
                _unittest_decorator_definitely_skips(decorator, context, module_constants)
                for decorator in test_method.decorator_list
            ):
                continue
            for reachable_method in (setup, test_method, teardown):
                if reachable_method is not None and not _function_body_is_provably_vacuous(
                    reachable_method, module_constants
                ):
                    return False

    return True


def _python_evidence_is_vacuous(path: Path, execution_mode: str) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (UnicodeDecodeError, SyntaxError):
        return False

    module_constants: dict[str, object] = {}
    main_guard_truth = _TRUTH_TRUE if execution_mode == _EXEC_DIRECT else _TRUTH_FALSE
    if not _block_is_provably_vacuous(
        tree.body,
        main_guard_truth=main_guard_truth,
        constants=module_constants,
    ):
        return False

    if execution_mode == _EXEC_UNITTEST_DISCOVERY:
        return _unittest_discovery_is_provably_vacuous(tree, module_constants)

    return True


def _evidence_vacuity_errors(
    root: Path,
    cap_id: str,
    field: str,
    values: Iterable[str],
    ci_commands: Iterable[str],
) -> list[str]:
    issues: list[str] = []
    for value in values:
        path = root / value
        if not path.is_file() or path.suffix != ".py":
            continue
        modes = _python_evidence_execution_modes(value, ci_commands)
        if not modes:
            continue
        if all(_python_evidence_is_vacuous(path, mode) for mode in modes):
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
                _evidence_vacuity_errors(
                    root,
                    cap_id,
                    "executable_evidence",
                    values["executable_evidence"],
                    values["ci_commands"],
                )
            )
            errors.extend(
                _evidence_vacuity_errors(
                    root,
                    cap_id,
                    "failure_evidence",
                    values["failure_evidence"],
                    values["ci_commands"],
                )
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
