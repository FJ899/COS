#!/usr/bin/env python3
"""Projector v2.1 deterministic public-effect manifest builder.

This module is intentionally NOT effect-capable.  It can normalize exact Git
facts into D/E manifests and construct/validate the exact Human authority tuple,
but caller-supplied facts can never reach an external write from this module.
The sole effect-capable consumer lives in projector_public_effect_trusted_runtime.py.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

ARCHITECTURE_AMENDMENT = {
    "version": "v2.1",
    "commit": "6e07fa2cce685521e216c1c2e5c1ccf3cf7e779e",
    "path": "governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.1.md",
    "blob_sha": "caf6f6f08219cdd961af712febc37c92fe9cc768",
}
ARCHITECTURE_PARENT = {
    "version": "v2.0",
    "commit": "6916fa5ddb78604ccbf039576a0f1165d5a8a6a1",
    "path": "governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.0.md",
    "blob_sha": "e2e2158440939ba96cddffe9c0ac158ad07510f4",
}
EFFECT_KINDS = {"PUSH_CANDIDATE_REF", "CREATE_OR_UPDATE_PR"}
BASE_EQUALS = "CURRENT_BASE_EQUALS_FROZEN_SOURCE"
BASE_ADVANCED = "CURRENT_BASE_ADVANCED_FROM_FROZEN_SOURCE"
PROVEN_ANCESTOR = "PROVEN_ANCESTOR"
EQUAL = "EQUAL"
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
GIT_MODE_RE = re.compile(r"^[0-7]{6}$")
OBJECT_TYPES = {"blob", "tree", "commit"}
CHANGE_KINDS = {"ADDED", "MODIFIED", "DELETED", "RENAMED", "COPIED", "TYPE_CHANGED"}


class PublicEffectGateError(RuntimeError):
    """Fail-closed validation error."""


class _Blocked(PublicEffectGateError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class PublicEffectWriteSink(Protocol):
    def write(self, effect_descriptor: dict[str, Any]) -> dict[str, Any]:
        """Protocol retained only for backward-compatible type annotations."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _Blocked(f"{name} must be an object")
    return value


def _list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise _Blocked(f"{name} must be a list")
    return value


def _string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _Blocked(f"{name} must be a non-empty string")
    return value


def _sha40(value: Any, name: str) -> str:
    text = _string(value, name)
    if SHA40_RE.fullmatch(text) is None:
        raise _Blocked(f"{name} must be an exact 40-character lowercase Git SHA")
    return text


def _timestamp(value: Any, name: str) -> str:
    text = _string(value, name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise _Blocked(f"{name} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise _Blocked(f"{name} must include timezone information")
    return text


def _require_keys(value: dict[str, Any], required: set[str], name: str) -> None:
    missing = sorted(required - value.keys())
    if missing:
        raise _Blocked(f"{name} missing required fields: {', '.join(missing)}")


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "schema_version": "projector-public-effect-gate-result/1.1",
        "status": "BLOCKED",
        "effect_evidence_status": "UNKNOWN",
        "target_write_performed": False,
        "target_write_result": "NOT_CREATED",
        "reason": reason,
        "next_route": "RE_OBSERVE_RECOMPUTE_REAUTHORIZE_OR_TRUTHFUL_BLOCKER",
        "architecture_parent": ARCHITECTURE_PARENT,
        "architecture_amendment": ARCHITECTURE_AMENDMENT,
        "merge_authorized": False,
        "release_authorized": False,
        "deploy_authorized": False,
        "capability_promotion_authorized": False,
        "human_final_acceptance_created": False,
    }


def _expected_pre_purpose(effect_kind: str) -> str:
    if effect_kind == "PUSH_CANDIDATE_REF":
        return "B_PRE_PUSH"
    if effect_kind == "CREATE_OR_UPDATE_PR":
        return "B_PRE_PR"
    raise _Blocked(f"unsupported PUBLIC_EFFECT kind: {effect_kind}")


def _normalize_git_object(value: Any, name: str) -> dict[str, Any]:
    obj = _object(value, name)
    _require_keys(obj, {"object_id", "object_type", "git_mode"}, name)
    values = (obj.get("object_id"), obj.get("object_type"), obj.get("git_mode"))
    if all(item is None for item in values):
        return {"object_id": None, "object_type": None, "git_mode": None}
    if any(item is None for item in values):
        raise _Blocked(f"{name} must have all object fields or all null fields")
    object_id = _sha40(obj.get("object_id"), f"{name}.object_id")
    object_type = _string(obj.get("object_type"), f"{name}.object_type")
    if object_type not in OBJECT_TYPES:
        raise _Blocked(f"{name}.object_type must be one of {sorted(OBJECT_TYPES)}")
    git_mode = _string(obj.get("git_mode"), f"{name}.git_mode")
    if GIT_MODE_RE.fullmatch(git_mode) is None:
        raise _Blocked(f"{name}.git_mode must be a six-digit Git mode")
    return {"object_id": object_id, "object_type": object_type, "git_mode": git_mode}


def _normalize_changed_entries(value: Any) -> list[dict[str, Any]]:
    entries = _list(value, "changed_entries")
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str]] = set()
    for index, raw in enumerate(entries):
        item = _object(raw, f"changed_entries[{index}]")
        _require_keys(item, {"path", "previous_path", "change_kind", "base_object", "candidate_object"}, f"changed_entries[{index}]")
        path = _string(item.get("path"), f"changed_entries[{index}].path")
        previous_path = item.get("previous_path")
        if previous_path is not None:
            previous_path = _string(previous_path, f"changed_entries[{index}].previous_path")
        change_kind = _string(item.get("change_kind"), f"changed_entries[{index}].change_kind")
        if change_kind not in CHANGE_KINDS:
            raise _Blocked(f"changed_entries[{index}].change_kind is unsupported")
        base_object = _normalize_git_object(item.get("base_object"), f"changed_entries[{index}].base_object")
        candidate_object = _normalize_git_object(item.get("candidate_object"), f"changed_entries[{index}].candidate_object")
        if change_kind == "ADDED" and (base_object["object_id"] is not None or candidate_object["object_id"] is None):
            raise _Blocked("ADDED entry must have null base and exact candidate object")
        if change_kind == "DELETED" and (candidate_object["object_id"] is not None or base_object["object_id"] is None):
            raise _Blocked("DELETED entry must have exact base and null candidate object")
        if change_kind not in {"ADDED", "DELETED"} and (base_object["object_id"] is None or candidate_object["object_id"] is None):
            raise _Blocked(f"{change_kind} entry requires exact base and candidate objects")
        if change_kind in {"RENAMED", "COPIED"} and previous_path is None:
            raise _Blocked(f"{change_kind} entry requires previous_path")
        key = (previous_path, path)
        if key in seen:
            raise _Blocked("changed_entries contains a duplicate path identity")
        seen.add(key)
        normalized.append({
            "path": path,
            "previous_path": previous_path,
            "change_kind": change_kind,
            "base_object": base_object,
            "candidate_object": candidate_object,
        })
    return sorted(normalized, key=lambda item: (item["path"], item["previous_path"] or "", item["change_kind"]))


def _normalize_topology(value: Any, *, candidate_sha: str, candidate_tree_sha: str) -> dict[str, Any]:
    topology = _object(value, "candidate_commit_topology")
    _require_keys(topology, {"candidate_head_sha", "candidate_head_tree_sha", "candidate_commits"}, "candidate_commit_topology")
    if _sha40(topology.get("candidate_head_sha"), "candidate_commit_topology.candidate_head_sha") != candidate_sha:
        raise _Blocked("candidate topology head differs from exact candidate SHA")
    if _sha40(topology.get("candidate_head_tree_sha"), "candidate_commit_topology.candidate_head_tree_sha") != candidate_tree_sha:
        raise _Blocked("candidate topology tree differs from exact candidate tree")
    commits = _list(topology.get("candidate_commits"), "candidate_commit_topology.candidate_commits")
    if not commits:
        raise _Blocked("candidate topology must contain at least the candidate head commit")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(commits):
        commit = _object(raw, f"candidate_commit_topology.candidate_commits[{index}]")
        _require_keys(commit, {"commit_sha", "tree_sha", "ordered_parent_shas"}, f"candidate_commit_topology.candidate_commits[{index}]")
        commit_sha = _sha40(commit.get("commit_sha"), f"candidate_commit_topology.candidate_commits[{index}].commit_sha")
        tree_sha = _sha40(commit.get("tree_sha"), f"candidate_commit_topology.candidate_commits[{index}].tree_sha")
        parents = [_sha40(parent, f"candidate_commit_topology.candidate_commits[{index}].ordered_parent_shas") for parent in _list(commit.get("ordered_parent_shas"), f"candidate_commit_topology.candidate_commits[{index}].ordered_parent_shas")]
        if commit_sha in seen:
            raise _Blocked("candidate topology contains duplicate commit SHA")
        seen.add(commit_sha)
        normalized.append({"commit_sha": commit_sha, "tree_sha": tree_sha, "ordered_parent_shas": parents})
    if normalized[-1]["commit_sha"] != candidate_sha or normalized[-1]["tree_sha"] != candidate_tree_sha:
        raise _Blocked("candidate topology must end at exact candidate head/tree")
    return {"candidate_head_sha": candidate_sha, "candidate_head_tree_sha": candidate_tree_sha, "candidate_commits": normalized}


def _prepare(data: dict[str, Any], *, trust_level: str) -> dict[str, Any]:
    effect_kind = _string(data.get("effect_kind"), "effect_kind")
    if effect_kind not in EFFECT_KINDS:
        raise _Blocked(f"effect_kind must be one of {sorted(EFFECT_KINDS)}")
    repository = _string(data.get("repository"), "repository")
    if repository.count("/") != 1:
        raise _Blocked("repository must use owner/name form")
    base_ref = _string(data.get("base_ref"), "base_ref")
    candidate_ref = _string(data.get("candidate_ref_or_pr_head"), "candidate_ref_or_pr_head")
    frozen_source_sha = _sha40(data.get("frozen_source_sha"), "frozen_source_sha")
    expected_public_result = _object(data.get("expected_public_result"), "expected_public_result")

    base = _object(data.get("base_observation"), "base_observation")
    _require_keys(base, {"purpose", "repository", "base_ref", "sha", "observed_at", "evidence_ref"}, "base_observation")
    if base.get("purpose") != _expected_pre_purpose(effect_kind):
        raise _Blocked(f"{effect_kind} requires a separately fresh {_expected_pre_purpose(effect_kind)} observation")
    if base.get("repository") != repository or base.get("base_ref") != base_ref:
        raise _Blocked("base observation is bound to different repository/base ref")
    base_sha = _sha40(base.get("sha"), "base_observation.sha")
    _timestamp(base.get("observed_at"), "base_observation.observed_at")
    _string(base.get("evidence_ref"), "base_observation.evidence_ref")

    candidate = _object(data.get("candidate_observation"), "candidate_observation")
    _require_keys(candidate, {"repository", "candidate_ref_or_pr_head", "sha", "tree_sha", "observed_at", "evidence_ref"}, "candidate_observation")
    if candidate.get("repository") != repository or candidate.get("candidate_ref_or_pr_head") != candidate_ref:
        raise _Blocked("candidate observation is bound to different repository/ref")
    candidate_sha = _sha40(candidate.get("sha"), "candidate_observation.sha")
    candidate_tree_sha = _sha40(candidate.get("tree_sha"), "candidate_observation.tree_sha")
    _timestamp(candidate.get("observed_at"), "candidate_observation.observed_at")
    _string(candidate.get("evidence_ref"), "candidate_observation.evidence_ref")

    ancestry = _object(data.get("ancestry"), "ancestry")
    _require_keys(ancestry, {"frozen_to_base", "base_to_candidate", "merge_base_sha"}, "ancestry")
    frozen_to_base = _object(ancestry.get("frozen_to_base"), "ancestry.frozen_to_base")
    base_to_candidate = _object(ancestry.get("base_to_candidate"), "ancestry.base_to_candidate")
    _require_keys(frozen_to_base, {"status", "evidence_ref"}, "ancestry.frozen_to_base")
    _require_keys(base_to_candidate, {"status", "evidence_ref"}, "ancestry.base_to_candidate")
    _string(frozen_to_base.get("evidence_ref"), "ancestry.frozen_to_base.evidence_ref")
    _string(base_to_candidate.get("evidence_ref"), "ancestry.base_to_candidate.evidence_ref")
    if frozen_source_sha == base_sha:
        if frozen_to_base.get("status") not in {EQUAL, PROVEN_ANCESTOR}:
            raise _Blocked("frozen-source/current-base equality is not positively proven")
        relation = BASE_EQUALS
    else:
        if frozen_to_base.get("status") != PROVEN_ANCESTOR:
            raise _Blocked("FROZEN_SOURCE_NOT_PROVEN_ANCESTOR_OF_CURRENT_BASE")
        relation = BASE_ADVANCED
    if base_to_candidate.get("status") != PROVEN_ANCESTOR:
        raise _Blocked("CURRENT_BASE_NOT_PROVEN_ANCESTOR_OF_CANDIDATE")
    merge_base_sha = _sha40(ancestry.get("merge_base_sha"), "ancestry.merge_base_sha")
    if merge_base_sha != base_sha:
        raise _Blocked("merge base does not equal exact proven current base")

    topology = _normalize_topology(data.get("candidate_commit_topology"), candidate_sha=candidate_sha, candidate_tree_sha=candidate_tree_sha)
    changed_entries = _normalize_changed_entries(data.get("changed_entries"))
    diff_manifest = {
        "schema_version": "projector-authorized-diff-manifest/1.0",
        "repository": repository,
        "S_FROZEN": frozen_source_sha,
        "B_PRE_X": base_sha,
        "C_PRE_X": candidate_sha,
        "base_relation": relation,
        "merge_base_sha": merge_base_sha,
        "ancestry_proof_ref_or_identity": {
            "frozen_to_base": frozen_to_base["evidence_ref"],
            "base_to_candidate": base_to_candidate["evidence_ref"],
        },
        "candidate_commit_topology": topology,
        "changed_entries": changed_entries,
    }
    diff_hash = sha256_json(diff_manifest)
    effect_descriptor = {
        "schema_version": "projector-public-effect-descriptor/1.0",
        "effect_kind": effect_kind,
        "repository": repository,
        "base_ref": base_ref,
        "candidate_ref_or_pr_head": candidate_ref,
        "S_FROZEN": frozen_source_sha,
        "B_PRE_X": base_sha,
        "C_PRE_X": candidate_sha,
        "D_HASH_X": diff_hash,
        "expected_public_result": expected_public_result,
    }
    effect_hash = sha256_json(effect_descriptor)
    return {
        "schema_version": "projector-public-effect-gate-preparation/1.1",
        "status": "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY",
        "trust_level": trust_level,
        "effect_evidence_status": "NOT_YET_CREATED",
        "target_write_performed": False,
        "architecture_parent": ARCHITECTURE_PARENT,
        "architecture_amendment": ARCHITECTURE_AMENDMENT,
        "source_invocation_id": data.get("source_invocation_id"),
        "public_effect_gate": {
            "effect_kind": effect_kind,
            "repository": repository,
            "base_ref": base_ref,
            "candidate_ref_or_pr_head": candidate_ref,
            "frozen_source_sha": frozen_source_sha,
            "fresh_base_sha": base_sha,
            "base_relation": relation,
            "candidate_sha": candidate_sha,
            "candidate_tree_sha": candidate_tree_sha,
            "base_observation_ref": base["evidence_ref"],
            "candidate_observation_ref": candidate["evidence_ref"],
            "ancestry_evidence_refs": [frozen_to_base["evidence_ref"], base_to_candidate["evidence_ref"]],
            "diff_manifest": diff_manifest,
            "diff_manifest_sha256": diff_hash,
            "effect_descriptor": effect_descriptor,
            "effect_sha256": effect_hash,
        },
        "merge_authorized": False,
        "release_authorized": False,
        "deploy_authorized": False,
        "capability_promotion_authorized": False,
        "human_final_acceptance_created": False,
    }


def prepare_public_effect_gate(data: dict[str, Any]) -> dict[str, Any]:
    """Pure deterministic builder; caller-declared evidence is not effect-capable."""
    try:
        return _prepare(_object(data, "public effect input"), trust_level="CALLER_DECLARED_NOT_EFFECT_CAPABLE")
    except _Blocked as exc:
        return _blocked(exc.reason)


def authority_request(prepared: dict[str, Any]) -> dict[str, Any]:
    if prepared.get("status") != "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY":
        raise PublicEffectGateError("authority request requires successfully prepared gate")
    gate = prepared["public_effect_gate"]
    return {
        "schema_version": "projector-public-effect-authority-request/1.0",
        "classification": "GENUINE_HUMAN_OWNED_GATE",
        "authority_basis": "PUBLIC_EFFECT",
        "effect_kind": gate["effect_kind"],
        "repository": gate["repository"],
        "base_ref": gate["base_ref"],
        "candidate_ref_or_pr_head": gate["candidate_ref_or_pr_head"],
        "S_FROZEN": gate["frozen_source_sha"],
        "B_PRE_X": gate["fresh_base_sha"],
        "base_relation": gate["base_relation"],
        "C_PRE_X": gate["candidate_sha"],
        "D_HASH_X": gate["diff_manifest_sha256"],
        "E_HASH_X": gate["effect_sha256"],
        "architecture_amendment_commit": ARCHITECTURE_AMENDMENT["commit"],
    }


def _validate_human_authority(prepared: dict[str, Any], authority: Any) -> dict[str, Any]:
    record = _object(authority, "human_authority")
    request = authority_request(prepared)
    _require_keys(record, set(request) | {"decision", "human_decision_evidence_ref"}, "human_authority")
    if record.get("decision") != "AUTHORIZE":
        raise _Blocked("Human PUBLIC_EFFECT decision is not AUTHORIZE")
    _string(record.get("human_decision_evidence_ref"), "human_authority.human_decision_evidence_ref")
    for key, expected in request.items():
        if record.get(key) != expected:
            raise _Blocked(f"Human PUBLIC_EFFECT authority does not bind exact {key}")
    return record


def _validated_write_result(write_result: Any) -> dict[str, Any]:
    result = _object(write_result, "write_result")
    _require_keys(result, {"result_ref", "result_identity", "observed_at"}, "write_result")
    _string(result.get("result_ref"), "write_result.result_ref")
    _string(result.get("result_identity"), "write_result.result_identity")
    _timestamp(result.get("observed_at"), "write_result.observed_at")
    return result


def execute_authorized_public_effect(
    prepared: dict[str, Any],
    human_authority: dict[str, Any],
    write_time_revalidation: dict[str, Any],
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """Legacy caller-supplied path is physically disarmed after P4 FAIL."""
    _ = prepared, human_authority, write_time_revalidation, sink
    return _blocked("UNTRUSTED_CALLER_EVIDENCE_NOT_EFFECT_CAPABLE")


def write_record_exclusive_atomic(path: str | Path, value: dict[str, Any]) -> None:
    """Persist exact gate/result evidence without overwriting prior evidence."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise PublicEffectGateError(f"refusing to overwrite public-effect evidence: {destination}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=str(destination.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(canonical_json_bytes(value))
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError as exc:
            raise PublicEffectGateError(f"refusing to overwrite public-effect evidence: {destination}") from exc
    finally:
        temporary.unlink(missing_ok=True)
