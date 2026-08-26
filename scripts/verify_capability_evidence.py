#!/usr/bin/env python3
"""Fail closed when capability status outruns executable evidence."""
from __future__ import annotations

import ast
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("governance/CAPABILITY_REGISTRY.json")
POLICY_PATH = Path("governance/BEHAVIOR_FIRST_CAPABILITY_POLICY.md")
RUN_CONTRACT_PATH = Path("governance/P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md")
STATUSES = ["PROPOSED", "IMPLEMENTED", "TESTED", "INTEGRATION_TESTED", "OBSERVED_IN_REAL_WORK", "RELIABLE"]
RANK = {status: index for index, status in enumerate(STATUSES)}
CLAIM_RE = re.compile(r"CAPABILITY CLAIM:\s*(CAP-[A-Z0-9-]+)\b")
ID_RE = re.compile(r"^CAP-[A-Z0-9-]+$")
LIST_FIELDS = [
    "implementation", "executable_evidence", "failure_evidence", "integration_evidence",
    "real_work_evidence", "reliability_evidence", "ci_commands", "integration_ci_commands",
]
_EXEC_DIRECT = "direct"
_EXEC_UNITTEST = "unittest-discovery"
_PROBE_MARKER = "COS_CAPABILITY_EVIDENCE_PROBE_SENTINEL"
_PROBE_TIMEOUT = 30


def _list(entry: dict, field: str, errors: list[str], cap_id: str) -> list[str]:
    value = entry.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{cap_id}: {field} must be a list of non-empty strings")
        return []
    return value


def _existing_paths(root: Path, cap_id: str, field: str, values: Iterable[str], errors: list[str]) -> None:
    for value in values:
        if not (root / value).is_file():
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
        if path.is_file() and path.suffix == ".py":
            issues.extend(f"{cap_id}: {issue}" for issue in _python_stub_errors(path))
    return issues


def _workflow_text(root: Path) -> str:
    chunks: list[str] = []
    for path in sorted((root / ".github" / "workflows").glob("*.y*ml")):
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def _formal_claim_errors(root: Path, registered_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        errors.extend(
            f"unregistered formal claim {cap_id} in {path.relative_to(root)}"
            for cap_id in CLAIM_RE.findall(content) if cap_id not in registered_ids
        )
    return errors


def _parts(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return []


def _is_python(value: str) -> bool:
    return re.fullmatch(r"python(?:3(?:\.\d+)?)?", value) is not None


def _norm(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def _unittest_spec(command: str) -> tuple[str, str] | None:
    parts = _parts(command)
    if len(parts) < 4 or not _is_python(parts[0]) or parts[1:4] != ["-m", "unittest", "discover"]:
        return None
    start, pattern, index = ".", "test*.py", 4
    while index < len(parts):
        token = parts[index]
        if token in {"-s", "--start-directory", "-p", "--pattern", "-t", "--top-level-directory"} and index + 1 < len(parts):
            value = parts[index + 1]
            if token in {"-s", "--start-directory"}:
                start = value
            elif token in {"-p", "--pattern"}:
                pattern = value
            index += 2
            continue
        return None
    return start, pattern


def _modes(evidence: str, commands: Iterable[str]) -> list[tuple[str, str | None]]:
    found: list[tuple[str, str | None]] = []
    normalized = _norm(evidence)
    for command in commands:
        parts = _parts(command)
        if len(parts) == 2 and _is_python(parts[0]) and _norm(parts[1]) == normalized:
            mode = (_EXEC_DIRECT, None)
            if mode not in found:
                found.append(mode)
        spec = _unittest_spec(command)
        if spec is None:
            continue
        start, pattern = spec
        start_norm = _norm(start).strip("/")
        if start_norm not in {"", "."} and not normalized.startswith(start_norm + "/"):
            continue
        if fnmatch.fnmatch(Path(normalized).name, pattern):
            mode = (_EXEC_UNITTEST, start)
            if mode not in found:
                found.append(mode)
    return found


def _command(evidence: str, mode: tuple[str, str | None]) -> list[str]:
    if mode[0] == _EXEC_DIRECT:
        return [sys.executable, evidence]
    parent = str(Path(_norm(evidence)).parent)
    if parent == ".":
        parent = mode[1] or "."
    return [sys.executable, "-m", "unittest", "discover", "-s", parent, "-p", Path(evidence).name]


def _bootstrap() -> str:
    return f'''import json, os, runpy, sys, threading\nfrom pathlib import Path\nMARKER={_PROBE_MARKER!r}\nPATHS={{os.path.realpath(p) for p in json.loads(sys.argv[1])}}\nMODE,EVIDENCE=sys.argv[2],sys.argv[3]\nclass COSCapabilityEvidenceProbeSentinel(BaseException): pass\ndef profile(frame,event,arg):\n    if event=="call" and frame.f_code.co_name!="<module>":\n        name=frame.f_code.co_filename\n        name=os.path.normcase(name if os.path.isabs(name) else os.path.abspath(name))\n        if name in PATHS: raise COSCapabilityEvidenceProbeSentinel(MARKER+":"+frame.f_code.co_name)\nsys.setprofile(profile); threading.setprofile(profile)\nif MODE=="direct":\n    sys.argv=[EVIDENCE]; sys.path[0]=str(Path(EVIDENCE).resolve().parent); runpy.run_path(EVIDENCE,run_name="__main__")\nelif MODE=="unittest-discovery":\n    sys.argv=["unittest","discover","-s",sys.argv[4],"-p",sys.argv[5]]; runpy.run_module("unittest",run_name="__main__")\nelse: raise SystemExit("unsupported probe mode")\n'''


def _run(root: Path, evidence: str, mode: tuple[str, str | None], implementations: Iterable[str], control: bool) -> tuple[int, str, str]:
    command = _command(evidence, mode)
    if control:
        paths = json.dumps([str((root / value).resolve()) for value in implementations if (root / value).is_file()])
        command = [sys.executable, "-c", _bootstrap(), paths, mode[0], evidence]
        if mode[0] == _EXEC_UNITTEST:
            parent = str(Path(_norm(evidence)).parent)
            if parent == ".":
                parent = mode[1] or "."
            command += [parent, Path(evidence).name]
    try:
        completed = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=_PROBE_TIMEOUT, check=False)
        return completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout if isinstance(exc.stdout, str) else "", (exc.stderr if isinstance(exc.stderr, str) else "") + "\nprobe timed out"


def _probe(root: Path, evidence: str, mode: tuple[str, str | None], implementations: Iterable[str]) -> tuple[bool, str, tuple[int, str, str], tuple[int, str, str] | None]:
    baseline = _run(root, evidence, mode, implementations, False)
    if baseline[0] != 0:
        return False, "baseline execution failed", baseline, None
    control = _run(root, evidence, mode, implementations, True)
    combined = control[1] + "\n" + control[2]
    if control[0] != 0 and _PROBE_MARKER in combined:
        return True, "control failed on implementation-call sentinel", baseline, control
    if control[0] == 0:
        return False, "control also succeeded without entering registered implementation callable", baseline, control
    return False, "control failed without implementation-call sentinel", baseline, control


def _probe_role(root: Path, cap_id: str, field: str, values: Iterable[str], commands: Iterable[str], implementations: Iterable[str]) -> tuple[list[str], set[str]]:
    issues: list[str] = []
    sensitive: set[str] = set()
    for value in values:
        path = root / value
        if not path.is_file() or path.suffix != ".py":
            continue
        modes = _modes(value, commands)
        if not modes:
            issues.append(f"{cap_id}: {field} Python evidence has no allowlisted registered execution mode: {value}")
            continue
        results = [_probe(root, value, mode, implementations) for mode in modes]
        if any(result[0] for result in results):
            sensitive.add(value)
        elif all(result[2][0] == 0 and result[3] is not None and result[3][0] == 0 for result in results):
            issues.append(f"{cap_id}: {field} evidence is behavior-insensitive / unconditional-success: {value}")
        else:
            issues.append(f"{cap_id}: {field} evidence runtime probe failed: {value}: " + "; ".join(result[1] for result in results))
    return issues, sensitive


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
        cap_id, name, claim, status = entry.get("id"), entry.get("name"), entry.get("claim"), entry.get("status")
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
            for field in ["executable_evidence", "failure_evidence", "ci_commands"]:
                if not values[field]:
                    errors.append(f"{cap_id}: TESTED+ requires {field}")
            _existing_paths(root, cap_id, "executable_evidence", values["executable_evidence"], errors)
            _existing_paths(root, cap_id, "failure_evidence", values["failure_evidence"], errors)
            executable_set, failure_set = set(values["executable_evidence"]), set(values["failure_evidence"])
            if not executable_set - failure_set:
                errors.append(f"{cap_id}: TESTED+ requires a role-distinct executable_evidence witness")
            if not failure_set - executable_set:
                errors.append(f"{cap_id}: TESTED+ requires a role-distinct failure_evidence witness")
            exec_errors, exec_sensitive = _probe_role(root, cap_id, "executable_evidence", values["executable_evidence"], values["ci_commands"], values["implementation"])
            fail_errors, fail_sensitive = _probe_role(root, cap_id, "failure_evidence", values["failure_evidence"], values["ci_commands"], values["implementation"])
            errors.extend(exec_errors + fail_errors)
            if not exec_sensitive - failure_set:
                errors.append(f"{cap_id}: TESTED+ has no successful role-distinct implementation-sensitive executable_evidence witness")
            if not fail_sensitive - executable_set:
                errors.append(f"{cap_id}: TESTED+ has no successful role-distinct implementation-sensitive failure_evidence witness")
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
