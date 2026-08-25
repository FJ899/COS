#!/usr/bin/env python3
"""Projector v2.0 durable run recorder and transition verifier.

This executable is deliberately not a planner or workflow engine. It validates
machine-readable run bindings/transitions produced by the existing Intelligence
surface and appends immutable, hash-chained state snapshots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "2.0"
TASK_CONTRACT = {
    "version": "v1.0",
    "commit": "ef128a0885310524475fba1cd291d1f34400b0cc",
    "path": "governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md",
}
ARCHITECTURE_CONTRACT = {
    "version": "v2.0",
    "commit": "6916fa5ddb78604ccbf039576a0f1165d5a8a6a1",
    "path": "governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.0.md",
}
IMPLEMENTATION_REPOSITORY = "FJ899/COS"
IMPLEMENTATION_BRANCH = "impl/projector-real-project-v2"
STATUSES = {"ACTIVE", "BLOCKED", "DONE"}
EVIDENCE_SCOPES = {"PROJECTOR_INTERNAL", "WORKLOAD_EXTERNAL", "HUMAN_DECISION", "TEST"}
HUMAN_INTERVENTION_CLASSES = {"GENUINE_HUMAN_OWNED_GATE", "HUMAN_OPERATIONAL_RESCUE"}
HUMAN_AUTHORITY_BASES = {
    "GOAL_OR_NORMATIVE_MEANING",
    "FINAL_ACCEPTANCE",
    "COSTLY_PUBLIC_DESTRUCTIVE_IRREVERSIBLE_OR_MATERIALLY_RISKY_EFFECT",
    "GENUINE_PREFERENCE_NOT_RESOLVABLE_BY_EVIDENCE",
}
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


class ProjectorError(RuntimeError):
    """Fail-closed validation or integrity error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def state_hash(state: dict[str, Any]) -> str:
    payload = dict(state)
    payload.pop("state_sha256", None)
    return sha256_json(payload)


def read_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProjectorError(f"cannot read {path}: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProjectorError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProjectorError(f"JSON root must be an object: {path}")
    return value


def write_json_exclusive_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ProjectorError(f"refusing to overwrite append-only artifact: {path}")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError as exc:
            raise ProjectorError(f"refusing to overwrite append-only artifact: {path}") from exc
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            _missing_temp_file = True


def require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProjectorError(f"{name} must be an object")
    return value


def require_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ProjectorError(f"{name} must be a list")
    return value


def require_string(value: Any, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ProjectorError(f"{name} must be a string")
    if not allow_empty and not value.strip():
        raise ProjectorError(f"{name} must be non-empty")
    return value


def require_nullable_string(value: Any, name: str) -> str | None:
    if value is None:
        return None
    return require_string(value, name)


def require_exact_keys(value: dict[str, Any], required: set[str], name: str) -> None:
    missing = sorted(required - value.keys())
    if missing:
        raise ProjectorError(f"{name} missing required fields: {', '.join(missing)}")


def validate_timestamp(value: Any, name: str) -> str:
    text = require_string(value, name)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProjectorError(f"{name} must be an ISO-8601 timestamp") from exc
    return text


def validate_provenance(value: Any) -> dict[str, Any]:
    provenance = require_object(value, "provenance")
    require_exact_keys(provenance, {"task_contract", "architecture_contract", "implementation"}, "provenance")

    task = require_object(provenance["task_contract"], "provenance.task_contract")
    architecture = require_object(provenance["architecture_contract"], "provenance.architecture_contract")
    implementation = require_object(provenance["implementation"], "provenance.implementation")

    for name, actual, expected in (
        ("task_contract", task, TASK_CONTRACT),
        ("architecture_contract", architecture, ARCHITECTURE_CONTRACT),
    ):
        for key, expected_value in expected.items():
            if actual.get(key) != expected_value:
                raise ProjectorError(
                    f"provenance.{name}.{key} must equal frozen identity {expected_value!r}"
                )

    if implementation.get("repository") != IMPLEMENTATION_REPOSITORY:
        raise ProjectorError("provenance.implementation.repository does not match frozen repository")
    if implementation.get("branch") != IMPLEMENTATION_BRANCH:
        raise ProjectorError("provenance.implementation.branch does not match frozen branch")
    sha = require_string(implementation.get("sha"), "provenance.implementation.sha")
    if not SHA40_RE.fullmatch(sha):
        raise ProjectorError("provenance.implementation.sha must be an exact 40-character lowercase git SHA")
    return provenance


def validate_evidence_ref(value: Any, name: str) -> dict[str, Any]:
    ref = require_object(value, name)
    required = {
        "evidence_id",
        "kind",
        "scope",
        "locator",
        "immutable_identity",
        "observed_at",
        "producer",
        "supports",
    }
    require_exact_keys(ref, required, name)
    for key in ("evidence_id", "kind", "locator", "immutable_identity", "producer"):
        require_string(ref[key], f"{name}.{key}")
    if ref["scope"] not in EVIDENCE_SCOPES:
        raise ProjectorError(f"{name}.scope must be one of {sorted(EVIDENCE_SCOPES)}")
    validate_timestamp(ref["observed_at"], f"{name}.observed_at")
    supports = require_list(ref["supports"], f"{name}.supports")
    if not supports:
        raise ProjectorError(f"{name}.supports must contain at least one traceability target")
    for index, item in enumerate(supports):
        require_string(item, f"{name}.supports[{index}]")
    return ref


def validate_evidence_refs(value: Any, name: str) -> list[dict[str, Any]]:
    refs = require_list(value, name)
    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, item in enumerate(refs):
        ref = validate_evidence_ref(item, f"{name}[{index}]")
        evidence_id = ref["evidence_id"]
        if evidence_id in seen:
            raise ProjectorError(f"duplicate evidence_id in {name}: {evidence_id}")
        seen.add(evidence_id)
        validated.append(ref)
    return validated


def validate_route(value: Any, name: str = "route") -> dict[str, Any]:
    route = require_object(value, name)
    required = {"route_id", "next_move_kind", "description", "justification", "evidence_basis"}
    require_exact_keys(route, required, name)
    for key in ("route_id", "next_move_kind", "description", "justification"):
        require_string(route[key], f"{name}.{key}")
    evidence_basis = require_list(route["evidence_basis"], f"{name}.evidence_basis")
    for index, evidence_id in enumerate(evidence_basis):
        require_string(evidence_id, f"{name}.evidence_basis[{index}]")
    return route


def validate_human_intervention(value: Any, evidence_index: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if value is None:
        return None
    intervention = require_object(value, "human_intervention")
    required = {"classification", "reason", "authority_basis", "human_decision_evidence_ref"}
    require_exact_keys(intervention, required, "human_intervention")
    classification = intervention.get("classification")
    if classification not in HUMAN_INTERVENTION_CLASSES:
        raise ProjectorError(
            "human_intervention.classification must be GENUINE_HUMAN_OWNED_GATE or HUMAN_OPERATIONAL_RESCUE"
        )
    require_string(intervention.get("reason"), "human_intervention.reason")
    authority_basis = require_string(intervention.get("authority_basis"), "human_intervention.authority_basis")
    evidence_id = require_string(
        intervention.get("human_decision_evidence_ref"),
        "human_intervention.human_decision_evidence_ref",
    )
    ref = evidence_index.get(evidence_id)
    if ref is None:
        raise ProjectorError("human intervention must reference preserved Human-decision evidence")
    if ref.get("scope") != "HUMAN_DECISION":
        raise ProjectorError("human intervention evidence must have scope HUMAN_DECISION")
    if classification == "GENUINE_HUMAN_OWNED_GATE" and authority_basis not in HUMAN_AUTHORITY_BASES:
        raise ProjectorError("genuine Human-owned gate has an invalid frozen authority basis")
    return intervention


def validate_goal_change(
    value: Any,
    *,
    previous_goal: str,
    previous_done: str,
    proposed_goal: str,
    proposed_done: str,
    evidence_index: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    changed = proposed_goal != previous_goal or proposed_done != previous_done
    if value is None:
        if changed:
            raise ProjectorError("goal/DONE changed without explicit Human-owned goal_change evidence")
        return None

    goal_change = require_object(value, "goal_change")
    required = {"type", "human_decision_evidence_ref", "new_goal", "new_done"}
    require_exact_keys(goal_change, required, "goal_change")
    if goal_change.get("type") != "HUMAN_GOAL_CHANGE":
        raise ProjectorError("goal_change.type must be HUMAN_GOAL_CHANGE")
    if not changed:
        raise ProjectorError("goal_change supplied but goal/DONE did not change")
    if goal_change.get("new_goal") != proposed_goal or goal_change.get("new_done") != proposed_done:
        raise ProjectorError("goal_change new_goal/new_done must exactly match proposed current_goal/current_done")
    evidence_id = require_string(
        goal_change.get("human_decision_evidence_ref"), "goal_change.human_decision_evidence_ref"
    )
    ref = evidence_index.get(evidence_id)
    if ref is None or ref.get("scope") != "HUMAN_DECISION":
        raise ProjectorError("goal_change requires preserved evidence with scope HUMAN_DECISION")
    return goal_change


def validate_material_evidence_change(
    value: Any,
    evidence_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    change = require_object(value, "material_evidence_change")
    required = {"evidence_refs", "invalidates_current_route"}
    require_exact_keys(change, required, "material_evidence_change")
    refs = require_list(change["evidence_refs"], "material_evidence_change.evidence_refs")
    for index, evidence_id in enumerate(refs):
        require_string(evidence_id, f"material_evidence_change.evidence_refs[{index}]")
        if evidence_id not in evidence_index:
            raise ProjectorError(f"material_evidence_change references unknown evidence_id: {evidence_id}")
    if not isinstance(change["invalidates_current_route"], bool):
        raise ProjectorError("material_evidence_change.invalidates_current_route must be boolean")
    if change["invalidates_current_route"] and not refs:
        raise ProjectorError("route invalidation requires at least one exact evidence reference")
    return change


def validate_route_change(value: Any, previous_route_id: str, current_route_id: str) -> dict[str, Any] | None:
    changed = previous_route_id != current_route_id
    if value is None:
        if changed:
            raise ProjectorError("route_id changed without route_change record")
        return None
    route_change = require_object(value, "route_change")
    required = {"from_route_id", "to_route_id", "reason"}
    require_exact_keys(route_change, required, "route_change")
    if not changed:
        raise ProjectorError("route_change supplied but route_id did not change")
    if route_change.get("from_route_id") != previous_route_id:
        raise ProjectorError("route_change.from_route_id does not match previous route")
    if route_change.get("to_route_id") != current_route_id:
        raise ProjectorError("route_change.to_route_id does not match proposed route")
    require_string(route_change.get("reason"), "route_change.reason")
    return route_change


def validate_state_common(state: dict[str, Any], run: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "run_id",
        "sequence",
        "previous_state_sha256",
        "run_manifest_sha256",
        "current_goal",
        "current_done",
        "observed_facts",
        "assumptions",
        "claims",
        "unknowns",
        "critical_unknown_or_blocker",
        "material_evidence_refs",
        "route",
        "human_intervention",
        "route_change",
        "transition_reason",
        "material_evidence_change",
        "evidence_basis",
        "goal_change",
        "status",
        "state_sha256",
    }
    require_exact_keys(state, required, "state")
    if state["schema_version"] != SCHEMA_VERSION:
        raise ProjectorError("state schema_version mismatch")
    if state["run_id"] != run["run_id"]:
        raise ProjectorError("state run_id does not match run manifest")
    if not isinstance(state["sequence"], int) or state["sequence"] < 0:
        raise ProjectorError("state.sequence must be a non-negative integer")
    if state["previous_state_sha256"] is not None:
        prior_hash = require_string(state["previous_state_sha256"], "state.previous_state_sha256")
        if not HEX64_RE.fullmatch(prior_hash):
            raise ProjectorError("state.previous_state_sha256 must be a sha256 hex digest")
    manifest_hash = require_string(state["run_manifest_sha256"], "state.run_manifest_sha256")
    if not HEX64_RE.fullmatch(manifest_hash):
        raise ProjectorError("state.run_manifest_sha256 must be a sha256 hex digest")
    require_string(state["current_goal"], "state.current_goal")
    require_string(state["current_done"], "state.current_done")
    for category in ("observed_facts", "assumptions", "claims", "unknowns"):
        values = require_list(state[category], f"state.{category}")
        for index, item in enumerate(values):
            if not isinstance(item, (str, dict)):
                raise ProjectorError(f"state.{category}[{index}] must be a string or object")
    critical = state["critical_unknown_or_blocker"]
    if state["status"] in {"ACTIVE", "BLOCKED"}:
        if critical is None or (isinstance(critical, str) and not critical.strip()):
            raise ProjectorError("ACTIVE/BLOCKED state requires one visible critical unknown/blocker")
    elif critical is not None and not isinstance(critical, (str, dict)):
        raise ProjectorError("critical_unknown_or_blocker must be null, string, or object")
    validate_evidence_refs(state["material_evidence_refs"], "state.material_evidence_refs")
    validate_route(state["route"])
    require_string(state["transition_reason"], "state.transition_reason")
    evidence_basis = require_list(state["evidence_basis"], "state.evidence_basis")
    for index, evidence_id in enumerate(evidence_basis):
        require_string(evidence_id, f"state.evidence_basis[{index}]")
    if state["status"] not in STATUSES:
        raise ProjectorError(f"state.status must be one of {sorted(STATUSES)}")
    digest = require_string(state["state_sha256"], "state.state_sha256")
    if not HEX64_RE.fullmatch(digest):
        raise ProjectorError("state.state_sha256 must be a sha256 hex digest")
    if state_hash(state) != digest:
        raise ProjectorError("state snapshot hash mismatch")


def validate_run_manifest(run: dict[str, Any], expected_run_id: str | None = None) -> None:
    required = {
        "schema_version",
        "run_id",
        "created_at",
        "raw_human_intent",
        "initial_binding",
        "provenance",
    }
    require_exact_keys(run, required, "run.json")
    if run["schema_version"] != SCHEMA_VERSION:
        raise ProjectorError("run schema_version mismatch")
    run_id = require_string(run["run_id"], "run_id")
    if not RUN_ID_RE.fullmatch(run_id):
        raise ProjectorError("run_id contains unsupported characters")
    if expected_run_id is not None and run_id != expected_run_id:
        raise ProjectorError("run_id does not match run directory name")
    validate_timestamp(run["created_at"], "created_at")
    require_string(run["raw_human_intent"], "raw_human_intent")
    binding = require_object(run["initial_binding"], "initial_binding")
    required_binding = {
        "bounded_target",
        "goal",
        "done",
        "verification_method",
        "current_critical_unknown",
        "assumptions",
        "known_human_authority_gates",
    }
    require_exact_keys(binding, required_binding, "initial_binding")
    for key in ("bounded_target", "goal", "done", "verification_method", "current_critical_unknown"):
        require_string(binding[key], f"initial_binding.{key}")
    require_list(binding["assumptions"], "initial_binding.assumptions")
    require_list(binding["known_human_authority_gates"], "initial_binding.known_human_authority_gates")
    validate_provenance(run["provenance"])


def run_id_from_dir(run_dir: Path) -> str:
    run_id = run_dir.name
    if not RUN_ID_RE.fullmatch(run_id):
        raise ProjectorError("run directory basename must be a safe run_id")
    return run_id


def initial_route(input_data: dict[str, Any], current_critical_unknown: str) -> dict[str, Any]:
    if "initial_route" in input_data:
        return validate_route(input_data["initial_route"], "initial_route")
    return {
        "route_id": "INITIAL_BINDING",
        "next_move_kind": "INTELLIGENCE_DECISION_REQUIRED",
        "description": "Existing Intelligence must propose the first justified move before material work.",
        "justification": f"Initial binding froze the current critical unknown: {current_critical_unknown}",
        "evidence_basis": [],
    }


def validate_init_input(value: dict[str, Any], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    required = {
        "raw_human_intent",
        "bounded_target",
        "goal",
        "done",
        "verification_method",
        "current_critical_unknown",
        "assumptions",
        "known_human_authority_gates",
        "provenance",
    }
    require_exact_keys(value, required, "init input")
    for key in (
        "raw_human_intent",
        "bounded_target",
        "goal",
        "done",
        "verification_method",
        "current_critical_unknown",
    ):
        require_string(value[key], key)
    assumptions = require_list(value["assumptions"], "assumptions")
    authority_gates = require_list(value["known_human_authority_gates"], "known_human_authority_gates")
    provenance = validate_provenance(value["provenance"])

    run = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": utc_now(),
        "raw_human_intent": value["raw_human_intent"],
        "initial_binding": {
            "bounded_target": value["bounded_target"],
            "goal": value["goal"],
            "done": value["done"],
            "verification_method": value["verification_method"],
            "current_critical_unknown": value["current_critical_unknown"],
            "assumptions": assumptions,
            "known_human_authority_gates": authority_gates,
        },
        "provenance": provenance,
    }
    validate_run_manifest(run, run_id)
    manifest_hash = sha256_json(run)
    route = initial_route(value, value["current_critical_unknown"])
    if route["evidence_basis"]:
        raise ProjectorError("initial_route.evidence_basis must be empty because init carries no evidence references")
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "sequence": 0,
        "previous_state_sha256": None,
        "run_manifest_sha256": manifest_hash,
        "current_goal": value["goal"],
        "current_done": value["done"],
        "observed_facts": [],
        "assumptions": assumptions,
        "claims": [],
        "unknowns": [value["current_critical_unknown"]],
        "critical_unknown_or_blocker": value["current_critical_unknown"],
        "material_evidence_refs": [],
        "route": route,
        "human_intervention": None,
        "route_change": None,
        "transition_reason": "INITIAL_BINDING",
        "material_evidence_change": {"evidence_refs": [], "invalidates_current_route": False},
        "evidence_basis": [],
        "goal_change": None,
        "status": "ACTIVE",
    }
    state["state_sha256"] = state_hash(state)
    validate_state_common(state, run)
    return run, state


def state_paths(run_dir: Path) -> list[Path]:
    states_dir = run_dir / "states"
    if not states_dir.is_dir():
        raise ProjectorError("missing states directory")
    paths = sorted(path for path in states_dir.iterdir() if path.is_file())
    if not paths:
        raise ProjectorError("run has no state snapshots")
    expected_names = [f"{index:04d}.json" for index in range(len(paths))]
    actual_names = [path.name for path in paths]
    if actual_names != expected_names:
        raise ProjectorError("state snapshots must be contiguous append-only NNNN.json files")
    return paths


def build_evidence_index(states: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for state in states:
        for ref in state["material_evidence_refs"]:
            evidence_id = ref["evidence_id"]
            existing = index.get(evidence_id)
            if existing is not None and existing != ref:
                raise ProjectorError(f"evidence identity drift detected for {evidence_id}")
            index[evidence_id] = ref
    return index


def verify_bundle(run_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    run_id = run_id_from_dir(run_dir)
    run_path = run_dir / "run.json"
    if not run_path.is_file():
        raise ProjectorError("missing immutable run.json")
    run = read_json(run_path)
    validate_run_manifest(run, run_id)
    manifest_hash = sha256_json(run)
    states: list[dict[str, Any]] = []
    previous_hash: str | None = None
    previous_goal = run["initial_binding"]["goal"]
    previous_done = run["initial_binding"]["done"]
    previous_route_id: str | None = None
    evidence_index: dict[str, dict[str, Any]] = {}

    for expected_sequence, path in enumerate(state_paths(run_dir)):
        state = read_json(path)
        validate_state_common(state, run)
        if state["sequence"] != expected_sequence:
            raise ProjectorError("state sequence does not match snapshot filename/order")
        if state["run_manifest_sha256"] != manifest_hash:
            raise ProjectorError("run.json was changed after state snapshots were written")
        if state["previous_state_sha256"] != previous_hash:
            raise ProjectorError("state hash chain is broken")

        current_refs = validate_evidence_refs(state["material_evidence_refs"], "state.material_evidence_refs")
        for ref in current_refs:
            evidence_id = ref["evidence_id"]
            old = evidence_index.get(evidence_id)
            if old is not None and old != ref:
                raise ProjectorError(f"evidence identity drift detected for {evidence_id}")
            evidence_index[evidence_id] = ref

        for evidence_id in state["evidence_basis"]:
            if evidence_id not in evidence_index:
                raise ProjectorError(f"state evidence_basis references unknown evidence_id: {evidence_id}")
        for evidence_id in state["route"]["evidence_basis"]:
            if evidence_id not in evidence_index:
                raise ProjectorError(f"route evidence_basis references unknown evidence_id: {evidence_id}")

        if expected_sequence == 0:
            if state["current_goal"] != previous_goal or state["current_done"] != previous_done:
                raise ProjectorError("initial state must preserve initial goal/DONE")
            if state["goal_change"] is not None or state["human_intervention"] is not None:
                raise ProjectorError("initial state cannot contain a transition-only Human event")
            if state["route_change"] is not None:
                raise ProjectorError("initial state cannot contain route_change")
        else:
            validate_goal_change(
                state["goal_change"],
                previous_goal=previous_goal,
                previous_done=previous_done,
                proposed_goal=state["current_goal"],
                proposed_done=state["current_done"],
                evidence_index=evidence_index,
            )
            validate_human_intervention(state["human_intervention"], evidence_index)
            assert previous_route_id is not None
            validate_route_change(state["route_change"], previous_route_id, state["route"]["route_id"])
            material_change = validate_material_evidence_change(state["material_evidence_change"], evidence_index)
            if material_change["invalidates_current_route"]:
                rerouted = state["route"]["route_id"] != previous_route_id
                if not rerouted and state["status"] != "BLOCKED":
                    raise ProjectorError("declared route invalidation must reroute or truthfully BLOCK")

        if state["status"] == "DONE":
            external = [ref for ref in state["material_evidence_refs"] if ref["scope"] == "WORKLOAD_EXTERNAL"]
            if not external:
                raise ProjectorError("DONE requires workload-external effect evidence")
            if state["critical_unknown_or_blocker"] is not None:
                raise ProjectorError("DONE cannot retain a critical unknown/blocker")
            require_string(run["initial_binding"]["verification_method"], "initial_binding.verification_method")

        previous_hash = state["state_sha256"]
        previous_goal = state["current_goal"]
        previous_done = state["current_done"]
        previous_route_id = state["route"]["route_id"]
        states.append(state)

    return run, states


def validate_transition_input(
    proposed: dict[str, Any],
    *,
    run: dict[str, Any],
    states: list[dict[str, Any]],
) -> dict[str, Any]:
    required = {
        "current_goal",
        "current_done",
        "observed_facts",
        "assumptions",
        "claims",
        "unknowns",
        "critical_unknown_or_blocker",
        "material_evidence_refs",
        "route",
        "status",
        "transition_reason",
        "material_evidence_change",
        "evidence_basis",
        "human_intervention",
        "route_change",
        "goal_change",
    }
    require_exact_keys(proposed, required, "transition input")
    previous = states[-1]
    current_refs = validate_evidence_refs(proposed["material_evidence_refs"], "material_evidence_refs")
    evidence_index = build_evidence_index(states)
    for ref in current_refs:
        evidence_id = ref["evidence_id"]
        old = evidence_index.get(evidence_id)
        if old is not None and old != ref:
            raise ProjectorError(f"evidence identity drift detected for {evidence_id}")
        evidence_index[evidence_id] = ref

    route = validate_route(proposed["route"])
    evidence_basis = require_list(proposed["evidence_basis"], "evidence_basis")
    for index, evidence_id in enumerate(evidence_basis):
        require_string(evidence_id, f"evidence_basis[{index}]")
        if evidence_id not in evidence_index:
            raise ProjectorError(f"transition evidence_basis references unknown evidence_id: {evidence_id}")
    current_evidence_ids = {ref["evidence_id"] for ref in current_refs}
    if not evidence_basis:
        raise ProjectorError("every material transition requires a non-empty evidence_basis")
    if not route["evidence_basis"]:
        raise ProjectorError("every proposed next move/gate requires a non-empty route.evidence_basis")
    for evidence_id in evidence_basis:
        if evidence_id not in current_evidence_ids:
            raise ProjectorError(f"transition evidence_basis must be present in current material_evidence_refs: {evidence_id}")
    for evidence_id in route["evidence_basis"]:
        if evidence_id not in evidence_index:
            raise ProjectorError(f"route evidence_basis references unknown evidence_id: {evidence_id}")
        if evidence_id not in current_evidence_ids:
            raise ProjectorError(f"route evidence_basis must be present in current material_evidence_refs: {evidence_id}")

    proposed_goal = require_string(proposed["current_goal"], "current_goal")
    proposed_done = require_string(proposed["current_done"], "current_done")
    goal_change = validate_goal_change(
        proposed["goal_change"],
        previous_goal=previous["current_goal"],
        previous_done=previous["current_done"],
        proposed_goal=proposed_goal,
        proposed_done=proposed_done,
        evidence_index=evidence_index,
    )
    human_intervention = validate_human_intervention(proposed["human_intervention"], evidence_index)
    if goal_change is not None:
        if human_intervention is None:
            raise ProjectorError("Human goal/DONE change must also be recorded as a material Human intervention")
        if human_intervention["classification"] != "GENUINE_HUMAN_OWNED_GATE":
            raise ProjectorError("Human goal/DONE change must be classified as GENUINE_HUMAN_OWNED_GATE")
        if human_intervention["authority_basis"] != "GOAL_OR_NORMATIVE_MEANING":
            raise ProjectorError("Human goal/DONE change requires GOAL_OR_NORMATIVE_MEANING authority basis")
        if human_intervention["human_decision_evidence_ref"] != goal_change["human_decision_evidence_ref"]:
            raise ProjectorError("goal_change and Human intervention must reference the same Human decision evidence")
    route_change = validate_route_change(
        proposed["route_change"], previous["route"]["route_id"], route["route_id"]
    )
    material_change = validate_material_evidence_change(proposed["material_evidence_change"], evidence_index)
    for evidence_id in material_change["evidence_refs"]:
        if evidence_id not in current_evidence_ids:
            raise ProjectorError(
                f"material_evidence_change evidence must be present in current material_evidence_refs: {evidence_id}"
            )
    if human_intervention is not None and human_intervention["human_decision_evidence_ref"] not in current_evidence_ids:
        raise ProjectorError("Human intervention evidence must be present in current material_evidence_refs")
    if goal_change is not None and goal_change["human_decision_evidence_ref"] not in current_evidence_ids:
        raise ProjectorError("goal-change evidence must be present in current material_evidence_refs")

    status = proposed["status"]
    if status not in STATUSES:
        raise ProjectorError(f"status must be one of {sorted(STATUSES)}")
    critical = proposed["critical_unknown_or_blocker"]
    if status in {"ACTIVE", "BLOCKED"}:
        if critical is None or (isinstance(critical, str) and not critical.strip()):
            raise ProjectorError("ACTIVE/BLOCKED transition requires a visible critical unknown/blocker")
    elif critical is not None and not isinstance(critical, (str, dict)):
        raise ProjectorError("critical_unknown_or_blocker must be null, string, or object")

    for category in ("observed_facts", "assumptions", "claims", "unknowns"):
        values = require_list(proposed[category], category)
        for index, item in enumerate(values):
            if not isinstance(item, (str, dict)):
                raise ProjectorError(f"{category}[{index}] must be a string or object")

    if material_change["invalidates_current_route"]:
        rerouted = route["route_id"] != previous["route"]["route_id"]
        if not rerouted and status != "BLOCKED":
            raise ProjectorError("declared route invalidation must reroute or truthfully BLOCK")

    if status == "DONE":
        external = [ref for ref in current_refs if ref["scope"] == "WORKLOAD_EXTERNAL"]
        if not external:
            raise ProjectorError("DONE requires at least one workload-external effect evidence reference")
        if critical is not None:
            raise ProjectorError("DONE cannot retain a critical unknown/blocker")
        require_string(run["initial_binding"]["verification_method"], "initial_binding.verification_method")

    require_string(proposed["transition_reason"], "transition_reason")
    sequence = previous["sequence"] + 1
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run["run_id"],
        "sequence": sequence,
        "previous_state_sha256": previous["state_sha256"],
        "run_manifest_sha256": sha256_json(run),
        "current_goal": proposed_goal,
        "current_done": proposed_done,
        "observed_facts": proposed["observed_facts"],
        "assumptions": proposed["assumptions"],
        "claims": proposed["claims"],
        "unknowns": proposed["unknowns"],
        "critical_unknown_or_blocker": critical,
        "material_evidence_refs": current_refs,
        "route": route,
        "human_intervention": human_intervention,
        "route_change": route_change,
        "transition_reason": proposed["transition_reason"],
        "material_evidence_change": material_change,
        "evidence_basis": evidence_basis,
        "goal_change": goal_change,
        "status": status,
    }
    state["state_sha256"] = state_hash(state)
    validate_state_common(state, run)
    return state


def command_init(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    run_id = run_id_from_dir(run_dir)
    if run_dir.exists():
        raise ProjectorError("run directory already exists; init is immutable")
    input_data = read_json(Path(args.input))
    run, state = validate_init_input(input_data, run_id)

    parent = run_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f".{run_id}.", dir=str(parent)))
    try:
        write_json_exclusive_atomic(temp_dir / "run.json", run)
        write_json_exclusive_atomic(temp_dir / "states" / "0000.json", state)
        try:
            os.replace(temp_dir, run_dir)
        except OSError as exc:
            raise ProjectorError(f"cannot atomically publish run bundle: {exc}") from exc
    finally:
        if temp_dir.exists():
            for path in sorted(temp_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
            temp_dir.rmdir()
    print(json.dumps({"run_id": run_id, "status": "INITIALIZED", "state_sha256": state["state_sha256"]}))
    return 0


def command_transition(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    run, states = verify_bundle(run_dir)
    proposed = read_json(Path(args.input))
    state = validate_transition_input(proposed, run=run, states=states)
    path = run_dir / "states" / f"{state['sequence']:04d}.json"
    write_json_exclusive_atomic(path, state)
    verify_bundle(run_dir)
    print(
        json.dumps(
            {
                "run_id": run["run_id"],
                "status": state["status"],
                "sequence": state["sequence"],
                "state_sha256": state["state_sha256"],
            }
        )
    )
    return 0


def recovery_payload(run: dict[str, Any], latest: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run["run_id"],
        "raw_human_intent": run["raw_human_intent"],
        "goal": latest["current_goal"],
        "done": latest["current_done"],
        "observed_facts": latest["observed_facts"],
        "assumptions": latest["assumptions"],
        "claims": latest["claims"],
        "unknowns": latest["unknowns"],
        "critical_unknown_or_blocker": latest["critical_unknown_or_blocker"],
        "material_evidence_refs": latest["material_evidence_refs"],
        "route": latest["route"],
        "human_intervention": latest["human_intervention"],
        "provenance": run["provenance"],
        "latest_state_sequence": latest["sequence"],
        "latest_state_sha256": latest["state_sha256"],
        "status": latest["status"],
    }


def command_recover(args: argparse.Namespace) -> int:
    run, states = verify_bundle(Path(args.run_dir))
    print(json.dumps(recovery_payload(run, states[-1]), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    run, states = verify_bundle(Path(args.run_dir))
    latest = states[-1]
    print(
        json.dumps(
            {
                "run_id": run["run_id"],
                "verification": "VALID",
                "state_count": len(states),
                "latest_state_sequence": latest["sequence"],
                "latest_state_sha256": latest["state_sha256"],
                "implementation_sha": run["provenance"]["implementation"]["sha"],
            },
            sort_keys=True,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Projector v2.0 run recorder / transition verifier")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "transition"):
        item = sub.add_parser(command)
        item.add_argument("--run-dir", required=True)
        item.add_argument("--input", required=True)
    for command in ("recover", "verify"):
        item = sub.add_parser(command)
        item.add_argument("--run-dir", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            return command_init(args)
        if args.command == "transition":
            return command_transition(args)
        if args.command == "recover":
            return command_recover(args)
        if args.command == "verify":
            return command_verify(args)
        raise ProjectorError(f"unsupported command: {args.command}")
    except ProjectorError as exc:
        print(f"[PROJECTOR BLOCKED] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
