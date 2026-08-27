#!/usr/bin/env python3
"""Projector v2.1 public-effect authority gate.

The pure ``prepare_public_effect_gate`` helper remains useful for deterministic
manifest construction and non-public tests, but caller-supplied observations are
explicitly NOT effect-capable.  The only API in this module that may call an
external write sink is ``execute_authorized_public_effect_from_trusted_sources``.
That function obtains Git facts itself from a concrete live Git adapter, obtains
Human authority itself from an immutable GitHub Issue Comment, then performs a
second live Git observation immediately before the write.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import subprocess
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
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
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_MODE_RE = re.compile(r"^[0-7]{6}$")
OBJECT_TYPES = {"blob", "tree", "commit"}
CHANGE_KINDS = {"ADDED", "MODIFIED", "DELETED", "RENAMED", "COPIED", "TYPE_CHANGED"}


class PublicEffectGateError(RuntimeError):
    """Fail-closed gate or trusted-source error."""


class _Blocked(PublicEffectGateError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class PublicEffectWriteSink(Protocol):
    def write(self, effect_descriptor: dict[str, Any]) -> dict[str, Any]:
        """Perform exactly one already-authorized public effect."""


class InMemoryNonPublicTestSink:
    """Bounded sink allowed only with explicit test-only trusted sources."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def write(self, effect_descriptor: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(json.loads(json.dumps(effect_descriptor)))
        return {
            "result_ref": "test-harness://public-effect/result-1",
            "result_identity": "NON_PUBLIC_TEST_EFFECT",
            "observed_at": _utc_now(),
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    """Pure manifest builder. Caller-declared evidence is NEVER effect-capable."""
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


def execute_authorized_public_effect(
    prepared: dict[str, Any],
    human_authority: dict[str, Any],
    write_time_revalidation: dict[str, Any],
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """Legacy caller-supplied path is intentionally disarmed after P4 FAIL."""
    _ = prepared, human_authority, write_time_revalidation, sink
    return _blocked("UNTRUSTED_CALLER_EVIDENCE_NOT_EFFECT_CAPABLE")


def _branch_name(ref: str, name: str) -> str:
    value = _string(ref, name)
    return value[len("refs/heads/"):] if value.startswith("refs/heads/") else value


def _repo_name(value: str) -> str:
    if value.count("/") != 1:
        raise _Blocked("repository must use owner/name form")
    return value


class GitRepositoryEvidenceSource:
    """Concrete read-side Git adapter. Production instances target github.com exactly."""

    def __init__(self, worktree: str | Path, repository: str) -> None:
        self.worktree = Path(worktree).resolve()
        self.repository = _repo_name(repository)
        self.remote_url = f"https://github.com/{self.repository}.git"
        self.test_only = False
        if not (self.worktree / ".git").exists():
            raise PublicEffectGateError("trusted Git worktree must contain .git")

    @classmethod
    def for_non_public_test(cls, worktree: str | Path, repository: str, remote_url: str) -> "GitRepositoryEvidenceSource":
        obj = cls.__new__(cls)
        obj.worktree = Path(worktree).resolve()
        obj.repository = _repo_name(repository)
        obj.remote_url = _string(remote_url, "test remote_url")
        obj.test_only = True
        if not (obj.worktree / ".git").exists():
            raise PublicEffectGateError("test Git worktree must contain .git")
        return obj

    def _run(self, args: list[str], *, text: bool = True, check: bool = True) -> str | bytes:
        try:
            proc = subprocess.run(
                ["git", "-C", str(self.worktree), *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=text,
                check=False,
            )
        except OSError as exc:
            raise _Blocked(f"trusted Git invocation failed: {exc}") from exc
        if check and proc.returncode != 0:
            stderr = proc.stderr if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
            raise _Blocked(f"trusted Git proof failed: {' '.join(args[:3])}: {stderr.strip()}")
        return proc.stdout

    def _remote_head(self, branch: str) -> str:
        output = self._run(["ls-remote", self.remote_url, f"refs/heads/{branch}"])
        assert isinstance(output, str)
        rows = [line for line in output.splitlines() if line.strip()]
        if len(rows) != 1:
            raise _Blocked(f"fresh remote head unavailable or ambiguous for {branch}")
        sha, ref = rows[0].split("\t", 1)
        if ref != f"refs/heads/{branch}":
            raise _Blocked("fresh remote head returned unexpected ref")
        return _sha40(sha, "fresh remote head")

    def _fetch_branch(self, branch: str, expected_sha: str) -> None:
        self._run(["fetch", "--quiet", "--no-tags", self.remote_url, f"refs/heads/{branch}"])
        fetched = self._run(["rev-parse", "FETCH_HEAD"])
        assert isinstance(fetched, str)
        if fetched.strip() != expected_sha:
            raise _Blocked("remote branch changed during trusted observation")

    def _is_ancestor(self, older: str, newer: str) -> bool:
        proc = subprocess.run(
            ["git", "-C", str(self.worktree), "merge-base", "--is-ancestor", older, newer],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return True
        if proc.returncode == 1:
            return False
        raise _Blocked(f"trusted ancestry proof unavailable: {proc.stderr.strip()}")

    def _object_type(self, oid: str) -> str:
        output = self._run(["cat-file", "-t", oid])
        assert isinstance(output, str)
        object_type = output.strip()
        if object_type not in OBJECT_TYPES:
            raise _Blocked(f"unsupported Git object type: {object_type}")
        return object_type

    def _raw_diff_entries(self, base_sha: str, candidate_sha: str) -> list[dict[str, Any]]:
        output = self._run(["diff", "--raw", "-z", "--no-abbrev", "--find-renames", "--find-copies", base_sha, candidate_sha, "--"], text=False)
        assert isinstance(output, bytes)
        parts = output.split(b"\0")
        entries: list[dict[str, Any]] = []
        i = 0
        kind_map = {"A": "ADDED", "M": "MODIFIED", "D": "DELETED", "R": "RENAMED", "C": "COPIED", "T": "TYPE_CHANGED"}
        while i < len(parts) and parts[i]:
            token = parts[i].decode("utf-8", "surrogateescape")
            i += 1
            if "\t" in token:
                header, first_path = token.split("\t", 1)
            else:
                header = token
                if i >= len(parts):
                    raise _Blocked("malformed trusted raw diff")
                first_path = parts[i].decode("utf-8", "surrogateescape")
                i += 1
            fields = header[1:].split()
            if not header.startswith(":") or len(fields) < 5:
                raise _Blocked("malformed trusted raw diff header")
            old_mode, new_mode, old_oid, new_oid, status = fields[:5]
            code = status[0]
            if code not in kind_map:
                raise _Blocked(f"unsupported trusted Git diff status: {status}")
            if code in {"R", "C"}:
                if i >= len(parts):
                    raise _Blocked("malformed trusted rename/copy diff")
                second_path = parts[i].decode("utf-8", "surrogateescape")
                i += 1
                previous_path, path = first_path, second_path
            else:
                previous_path, path = None, first_path

            def obj(mode: str, oid: str) -> dict[str, Any]:
                if mode == "000000" or set(oid) == {"0"}:
                    return {"object_id": None, "object_type": None, "git_mode": None}
                exact_oid = _sha40(oid, "trusted diff object id")
                return {"object_id": exact_oid, "object_type": self._object_type(exact_oid), "git_mode": mode}

            entries.append({
                "path": path,
                "previous_path": previous_path,
                "change_kind": kind_map[code],
                "base_object": obj(old_mode, old_oid),
                "candidate_object": obj(new_mode, new_oid),
            })
        return entries

    def _topology(self, base_sha: str, candidate_sha: str) -> dict[str, Any]:
        tree = self._run(["show", "-s", "--format=%T", candidate_sha])
        assert isinstance(tree, str)
        candidate_tree_sha = _sha40(tree.strip(), "candidate tree")
        revs = self._run(["rev-list", "--reverse", "--topo-order", f"{base_sha}..{candidate_sha}"])
        assert isinstance(revs, str)
        commits = [line.strip() for line in revs.splitlines() if line.strip()]
        if not commits or commits[-1] != candidate_sha:
            raise _Blocked("trusted candidate topology does not terminate at candidate head")
        items: list[dict[str, Any]] = []
        for commit_sha in commits:
            line = self._run(["show", "-s", "--format=%H%x00%T%x00%P", commit_sha])
            assert isinstance(line, str)
            fields = line.rstrip("\n").split("\x00")
            if len(fields) != 3:
                raise _Blocked("trusted candidate topology record malformed")
            sha, tree_sha, parents = fields
            items.append({
                "commit_sha": _sha40(sha, "topology commit"),
                "tree_sha": _sha40(tree_sha, "topology tree"),
                "ordered_parent_shas": [_sha40(p, "topology parent") for p in parents.split() if p],
            })
        return {
            "candidate_head_sha": candidate_sha,
            "candidate_head_tree_sha": candidate_tree_sha,
            "candidate_commits": items,
        }

    def observe(self, spec: dict[str, Any]) -> dict[str, Any]:
        effect_kind = _string(spec.get("effect_kind"), "effect_kind")
        if effect_kind not in EFFECT_KINDS:
            raise _Blocked("unsupported effect kind")
        repository = _repo_name(_string(spec.get("repository"), "repository"))
        if repository != self.repository:
            raise _Blocked("trusted Git source is bound to a different repository")
        base_ref = _branch_name(_string(spec.get("base_ref"), "base_ref"), "base_ref")
        candidate_ref = _branch_name(_string(spec.get("candidate_ref_or_pr_head"), "candidate_ref_or_pr_head"), "candidate_ref_or_pr_head")
        frozen = _sha40(spec.get("frozen_source_sha"), "frozen_source_sha")
        expected_public_result = _object(spec.get("expected_public_result"), "expected_public_result")
        invocation = secrets.token_hex(16)
        observed_at = _utc_now()

        base_sha = self._remote_head(base_ref)
        self._fetch_branch(base_ref, base_sha)
        if effect_kind == "CREATE_OR_UPDATE_PR":
            candidate_sha = self._remote_head(candidate_ref)
            self._fetch_branch(candidate_ref, candidate_sha)
        else:
            local = self._run(["rev-parse", f"{candidate_ref}^{{commit}}"])
            assert isinstance(local, str)
            candidate_sha = _sha40(local.strip(), "local candidate head")

        if frozen == base_sha:
            frozen_status = EQUAL
        elif self._is_ancestor(frozen, base_sha):
            frozen_status = PROVEN_ANCESTOR
        else:
            raise _Blocked("FROZEN_SOURCE_NOT_PROVEN_ANCESTOR_OF_CURRENT_BASE")
        if not self._is_ancestor(base_sha, candidate_sha):
            raise _Blocked("CURRENT_BASE_NOT_PROVEN_ANCESTOR_OF_CANDIDATE")
        merge_base = self._run(["merge-base", base_sha, candidate_sha])
        assert isinstance(merge_base, str)
        merge_base_sha = _sha40(merge_base.strip(), "trusted merge base")
        if merge_base_sha != base_sha:
            raise _Blocked("trusted merge base does not equal current base")

        topology = self._topology(base_sha, candidate_sha)
        changed_entries = self._raw_diff_entries(base_sha, candidate_sha)
        evidence_prefix = f"git-live:{repository}:{invocation}"
        return {
            "source_invocation_id": invocation,
            "effect_kind": effect_kind,
            "repository": repository,
            "base_ref": base_ref,
            "candidate_ref_or_pr_head": candidate_ref,
            "frozen_source_sha": frozen,
            "base_observation": {
                "purpose": _expected_pre_purpose(effect_kind),
                "repository": repository,
                "base_ref": base_ref,
                "sha": base_sha,
                "observed_at": observed_at,
                "evidence_ref": f"{evidence_prefix}:base:{base_sha}",
            },
            "candidate_observation": {
                "repository": repository,
                "candidate_ref_or_pr_head": candidate_ref,
                "sha": candidate_sha,
                "tree_sha": topology["candidate_head_tree_sha"],
                "observed_at": observed_at,
                "evidence_ref": f"{evidence_prefix}:candidate:{candidate_sha}",
            },
            "ancestry": {
                "frozen_to_base": {"status": frozen_status, "evidence_ref": f"{evidence_prefix}:ancestry:{frozen}:{base_sha}"},
                "base_to_candidate": {"status": PROVEN_ANCESTOR, "evidence_ref": f"{evidence_prefix}:ancestry:{base_sha}:{candidate_sha}"},
                "merge_base_sha": merge_base_sha,
            },
            "candidate_commit_topology": topology,
            "changed_entries": changed_entries,
            "expected_public_result": expected_public_result,
        }


class GitHubIssueCommentAuthoritySource:
    """Concrete durable Human authority source: one immutable GitHub Issue Comment."""

    def __init__(
        self,
        repository: str,
        issue_number: int,
        comment_id: int,
        actor_login: str,
        actor_id: int,
        *,
        token_env: str = "GITHUB_TOKEN",
    ) -> None:
        self.repository = _repo_name(repository)
        if issue_number <= 0 or comment_id <= 0 or actor_id <= 0:
            raise PublicEffectGateError("issue/comment/actor IDs must be positive")
        self.issue_number = issue_number
        self.comment_id = comment_id
        self.actor_login = _string(actor_login, "actor_login")
        self.actor_id = actor_id
        self.token_env = token_env
        self.test_only = False
        self._test_comment: dict[str, Any] | None = None

    @classmethod
    def for_non_public_test(
        cls,
        repository: str,
        issue_number: int,
        comment_id: int,
        actor_login: str,
        actor_id: int,
        comment: dict[str, Any],
    ) -> "GitHubIssueCommentAuthoritySource":
        obj = cls(repository, issue_number, comment_id, actor_login, actor_id)
        obj.test_only = True
        obj._test_comment = json.loads(json.dumps(comment))
        return obj

    def _fetch_comment(self) -> dict[str, Any]:
        if self._test_comment is not None:
            return json.loads(json.dumps(self._test_comment))
        url = f"https://api.github.com/repos/{self.repository}/issues/comments/{self.comment_id}"
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        token = os.environ.get(self.token_env)
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if getattr(response, "status", 200) != 200:
                    raise _Blocked("trusted Human authority source returned non-200")
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise _Blocked(f"trusted Human authority retrieval failed: {exc}") from exc
        return _object(payload, "GitHub Human authority comment")

    def load_authority(self, expected_request: dict[str, Any]) -> dict[str, Any]:
        comment = self._fetch_comment()
        if comment.get("id") != self.comment_id:
            raise _Blocked("GitHub Human authority comment ID mismatch")
        issue_url = _string(comment.get("issue_url"), "comment.issue_url")
        if issue_url != f"https://api.github.com/repos/{self.repository}/issues/{self.issue_number}":
            raise _Blocked("GitHub Human authority comment is bound to different Issue")
        user = _object(comment.get("user"), "comment.user")
        if user.get("login") != self.actor_login or user.get("id") != self.actor_id or user.get("type") != "User":
            raise _Blocked("GitHub Human authority actor identity mismatch")
        if comment.get("performed_via_github_app") not in {None}:
            raise _Blocked("GitHub Human authority comment was performed via GitHub App")
        created_at = _timestamp(comment.get("created_at"), "comment.created_at")
        updated_at = _timestamp(comment.get("updated_at"), "comment.updated_at")
        if created_at != updated_at:
            raise _Blocked("GitHub Human authority comment was edited")
        body_text = _string(comment.get("body"), "comment.body")
        try:
            body = json.loads(body_text)
        except json.JSONDecodeError as exc:
            raise _Blocked("GitHub Human authority body is not exact JSON") from exc
        body = _object(body, "GitHub Human authority body")
        if set(body) != {"schema_version", "request", "decision", "nonce"}:
            raise _Blocked("GitHub Human authority body must contain exact decision fields")
        if body.get("schema_version") != "projector-public-effect-human-decision/1.0":
            raise _Blocked("GitHub Human authority schema mismatch")
        if body.get("decision") != "AUTHORIZE":
            raise _Blocked("GitHub Human authority decision is not AUTHORIZE")
        _string(body.get("nonce"), "Human authority nonce")
        if body.get("request") != expected_request:
            raise _Blocked("GitHub Human authority request does not equal exact live tuple")
        node_id = _string(comment.get("node_id"), "comment.node_id")
        evidence_ref = f"github-issue-comment:{self.repository}:{self.issue_number}:{self.comment_id}:{node_id}:{hashlib.sha256(body_text.encode('utf-8')).hexdigest()}"
        return {**expected_request, "decision": "AUTHORIZE", "human_decision_evidence_ref": evidence_ref}


def prepare_public_effect_gate_from_trusted_git(spec: dict[str, Any], git_source: GitRepositoryEvidenceSource) -> dict[str, Any]:
    """Obtain a fresh B_PRE_X and exact Git proof from the concrete read adapter."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    try:
        observed = git_source.observe(_object(spec, "effect spec"))
        return _prepare(observed, trust_level="TRUSTED_LIVE_GIT")
    except _Blocked as exc:
        return _blocked(exc.reason)


def _validated_write_result(write_result: Any) -> dict[str, Any]:
    result = _object(write_result, "write_result")
    _require_keys(result, {"result_ref", "result_identity", "observed_at"}, "write_result")
    _string(result.get("result_ref"), "write_result.result_ref")
    _string(result.get("result_identity"), "write_result.result_identity")
    _timestamp(result.get("observed_at"), "write_result.observed_at")
    return result


def execute_authorized_public_effect_from_trusted_sources(
    spec: dict[str, Any],
    human_authority_source: GitHubIssueCommentAuthoritySource,
    git_source: GitRepositoryEvidenceSource,
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """The sole effect-capable path: live Git -> Human source -> live Git -> write."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    if type(human_authority_source) is not GitHubIssueCommentAuthoritySource:
        return _blocked("UNTRUSTED_HUMAN_AUTHORITY_SOURCE_TYPE")
    if (git_source.test_only or human_authority_source.test_only) and type(sink) is not InMemoryNonPublicTestSink:
        return _blocked("TEST_ONLY_TRUSTED_SOURCE_CANNOT_REACH_EXTERNAL_SINK")
    try:
        first_observed = git_source.observe(_object(spec, "effect spec"))
        first = _prepare(first_observed, trust_level="TRUSTED_LIVE_GIT")
        request = authority_request(first)
        authority = human_authority_source.load_authority(request)
        _validate_human_authority(first, authority)

        second_observed = git_source.observe(_object(spec, "effect spec"))
        second = _prepare(second_observed, trust_level="TRUSTED_LIVE_GIT_WRITE_TIME_REVALIDATION")
        if first.get("source_invocation_id") == second.get("source_invocation_id"):
            raise _Blocked("write-time Git observation was not a distinct trusted invocation")
        if authority_request(second) != request:
            raise _Blocked("write-time live Git state differs from Human-authorized tuple")
        _validate_human_authority(second, authority)
    except _Blocked as exc:
        return _blocked(exc.reason)

    write_result = sink.write(second["public_effect_gate"]["effect_descriptor"])
    try:
        result = _validated_write_result(write_result)
    except _Blocked as exc:
        raise PublicEffectGateError(
            "write sink returned without exact durable result identity; external effect requires reconciliation: " + exc.reason
        ) from exc

    gate = second["public_effect_gate"]
    return {
        "schema_version": "projector-public-effect-gate-result/1.1",
        "status": "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED",
        "effect_evidence_status": "OBSERVED",
        "target_write_performed": True,
        "target_write_result": result,
        "architecture_parent": ARCHITECTURE_PARENT,
        "architecture_amendment": ARCHITECTURE_AMENDMENT,
        "public_effect_gate": {
            "effect_kind": gate["effect_kind"],
            "repository": gate["repository"],
            "base_ref": gate["base_ref"],
            "frozen_source_sha": gate["frozen_source_sha"],
            "fresh_base_sha": gate["fresh_base_sha"],
            "base_relation": gate["base_relation"],
            "candidate_sha": gate["candidate_sha"],
            "ancestry_evidence_refs": gate["ancestry_evidence_refs"],
            "diff_manifest_ref": f"sha256:{gate['diff_manifest_sha256']}",
            "diff_manifest_sha256": gate["diff_manifest_sha256"],
            "effect_descriptor_ref": f"sha256:{gate['effect_sha256']}",
            "effect_sha256": gate["effect_sha256"],
            "human_authority_evidence_ref": authority["human_decision_evidence_ref"],
            "authority_classification": "GENUINE_HUMAN_OWNED_GATE",
            "authority_basis": "PUBLIC_EFFECT",
            "write_time_revalidation": "PASS",
            "write_time_revalidation_evidence_ref": second["public_effect_gate"]["base_observation_ref"],
            "write_time_source_invocation_id": second["source_invocation_id"],
            "write_performed": True,
            "write_result_ref": result["result_ref"],
        },
        "merge_authorized": False,
        "release_authorized": False,
        "deploy_authorized": False,
        "capability_promotion_authorized": False,
        "human_final_acceptance_created": False,
    }


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
