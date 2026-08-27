#!/usr/bin/env python3
"""Canonical effect-capable Projector v2.1 trusted runtime.

Exactly one function in the P3 implementation may invoke ``sink.write``:
``execute_trusted_public_effect`` below.  It owns both trusted read boundaries:
concrete Git observations/proofs and immutable GitHub Human decision evidence.
No caller dictionary can substitute for those reads.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import secrets
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from projector_public_effect_gate import (
    EFFECT_KINDS,
    EQUAL,
    OBJECT_TYPES,
    PROVEN_ANCESTOR,
    PublicEffectWriteSink,
    _Blocked,
    _blocked,
    _expected_pre_purpose,
    _object,
    _prepare,
    _sha40,
    _string,
    _validate_human_authority,
    _validated_write_result,
    authority_request,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _repo_name(value: str) -> str:
    if value.count("/") != 1:
        raise _Blocked("repository must use owner/name form")
    return value


def _branch_name(ref: str, name: str) -> str:
    value = _string(ref, name)
    return value[len("refs/heads/"):] if value.startswith("refs/heads/") else value


class InMemoryNonPublicTestSink:
    """Only sink permitted with explicit test-only trusted sources."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def write(self, effect_descriptor: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(json.loads(json.dumps(effect_descriptor)))
        return {
            "result_ref": "test-harness://public-effect/result-1",
            "result_identity": "NON_PUBLIC_TEST_EFFECT",
            "observed_at": _utc_now(),
        }


class GitRepositoryEvidenceSource:
    """Concrete read-side Git adapter. Production instances target github.com exactly."""

    def __init__(self, worktree: str | Path, repository: str) -> None:
        self.worktree = Path(worktree).resolve()
        self.repository = _repo_name(repository)
        self.remote_url = f"https://github.com/{self.repository}.git"
        self.test_only = False
        if not (self.worktree / ".git").exists():
            raise _Blocked("trusted Git worktree must contain .git")

    @classmethod
    def for_non_public_test(cls, worktree: str | Path, repository: str, remote_url: str) -> "GitRepositoryEvidenceSource":
        obj = cls.__new__(cls)
        obj.worktree = Path(worktree).resolve()
        obj.repository = _repo_name(repository)
        obj.remote_url = _string(remote_url, "test remote_url")
        obj.test_only = True
        if not (obj.worktree / ".git").exists():
            raise _Blocked("test Git worktree must contain .git")
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
        output = self._run(
            ["diff", "--raw", "-z", "--no-abbrev", "--find-renames", "--find-copies", base_sha, candidate_sha, "--"],
            text=False,
        )
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
                return {
                    "object_id": exact_oid,
                    "object_type": self._object_type(exact_oid),
                    "git_mode": mode,
                }

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
        observation_prefix = f"git-live:{repository}:{invocation}"
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
                "evidence_ref": f"{observation_prefix}:base:{base_sha}",
            },
            "candidate_observation": {
                "repository": repository,
                "candidate_ref_or_pr_head": candidate_ref,
                "sha": candidate_sha,
                "tree_sha": topology["candidate_head_tree_sha"],
                "observed_at": observed_at,
                "evidence_ref": f"{observation_prefix}:candidate:{candidate_sha}",
            },
            "ancestry": {
                "frozen_to_base": {
                    "status": frozen_status,
                    "evidence_ref": f"{observation_prefix}:ancestry:{frozen}:{base_sha}",
                },
                "base_to_candidate": {
                    "status": PROVEN_ANCESTOR,
                    "evidence_ref": f"{observation_prefix}:ancestry:{base_sha}:{candidate_sha}",
                },
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
            raise _Blocked("issue/comment/actor IDs must be positive")
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
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        token = os.environ.get(self.token_env)
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if getattr(response, "status", 200) != 200:
                    raise _Blocked("trusted Human authority source returned non-200")
                payload = json.loads(response.read().decode("utf-8"))
        except _Blocked:
            raise
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
        if comment.get("performed_via_github_app") is not None:
            raise _Blocked("GitHub Human authority comment was performed via GitHub App")
        created_at = _string(comment.get("created_at"), "comment.created_at")
        updated_at = _string(comment.get("updated_at"), "comment.updated_at")
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
        evidence_ref = (
            f"github-issue-comment:{self.repository}:{self.issue_number}:{self.comment_id}:"
            f"{node_id}:{hashlib.sha256(body_text.encode('utf-8')).hexdigest()}"
        )
        return {
            **expected_request,
            "decision": "AUTHORIZE",
            "human_decision_evidence_ref": evidence_ref,
        }


def _canonicalize_trusted_git_proof(observed: dict[str, Any]) -> dict[str, Any]:
    """Make D_HASH fact-stable while freshness remains source-invocation-bound."""
    value = copy.deepcopy(observed)
    repo = value["repository"]
    frozen = value["frozen_source_sha"]
    base = value["base_observation"]["sha"]
    candidate = value["candidate_observation"]["sha"]
    frozen_status = value["ancestry"]["frozen_to_base"]["status"]
    candidate_status = value["ancestry"]["base_to_candidate"]["status"]
    value["ancestry"]["frozen_to_base"]["evidence_ref"] = (
        f"git-proof:{repo}:frozen-to-base:{frozen_status}:{frozen}:{base}"
    )
    value["ancestry"]["base_to_candidate"]["evidence_ref"] = (
        f"git-proof:{repo}:base-to-candidate:{candidate_status}:{base}:{candidate}"
    )
    return value


def _fresh_prepare(spec: dict[str, Any], git_source: GitRepositoryEvidenceSource, trust_level: str) -> dict[str, Any]:
    observed = git_source.observe(_object(spec, "effect spec"))
    canonical = _canonicalize_trusted_git_proof(observed)
    return _prepare(canonical, trust_level=trust_level)


def prepare_trusted_public_effect_authority_request(
    spec: dict[str, Any],
    git_source: GitRepositoryEvidenceSource,
) -> dict[str, Any]:
    """Fresh trusted B_PRE_X/Git proof for the Human gate; no write capability."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    try:
        prepared = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_PRE_HUMAN_GATE")
        return {
            "status": "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY",
            "prepared": prepared,
            "authority_request": authority_request(prepared),
            "source_invocation_id": prepared["source_invocation_id"],
            "target_write_performed": False,
        }
    except _Blocked as exc:
        return _blocked(exc.reason)


def execute_trusted_public_effect(
    spec: dict[str, Any],
    human_authority_source: GitHubIssueCommentAuthoritySource,
    git_source: GitRepositoryEvidenceSource,
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """SOLE effect-capable path: live Git -> immutable Human -> live Git -> sink."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    if type(human_authority_source) is not GitHubIssueCommentAuthoritySource:
        return _blocked("UNTRUSTED_HUMAN_AUTHORITY_SOURCE_TYPE")
    if (git_source.test_only or human_authority_source.test_only) and type(sink) is not InMemoryNonPublicTestSink:
        return _blocked("TEST_ONLY_TRUSTED_SOURCE_CANNOT_REACH_EXTERNAL_SINK")

    try:
        pre_authority = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_AUTHORITY_VERIFICATION")
        request = authority_request(pre_authority)
        authority = human_authority_source.load_authority(request)
        _validate_human_authority(pre_authority, authority)

        write_time = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_WRITE_TIME_REVALIDATION")
        if pre_authority["source_invocation_id"] == write_time["source_invocation_id"]:
            raise _Blocked("write-time Git observation was not a distinct trusted invocation")
        if authority_request(write_time) != request:
            raise _Blocked("write-time live Git state differs from Human-authorized tuple")
        _validate_human_authority(write_time, authority)
    except _Blocked as exc:
        return _blocked(exc.reason)
    except Exception as exc:
        return _blocked(f"TRUSTED_SOURCE_FAILURE:{type(exc).__name__}")

    write_result = sink.write(write_time["public_effect_gate"]["effect_descriptor"])
    try:
        result = _validated_write_result(write_result)
    except _Blocked as exc:
        raise RuntimeError(
            "external write occurred but exact result identity is unavailable; reconciliation required: " + exc.reason
        ) from exc

    gate = write_time["public_effect_gate"]
    return {
        "schema_version": "projector-public-effect-gate-result/1.1",
        "status": "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED",
        "effect_evidence_status": "OBSERVED",
        "target_write_performed": True,
        "target_write_result": result,
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
            "write_time_revalidation_evidence_ref": gate["base_observation_ref"],
            "write_time_source_invocation_id": write_time["source_invocation_id"],
            "write_performed": True,
            "write_result_ref": result["result_ref"],
        },
        "merge_authorized": False,
        "release_authorized": False,
        "deploy_authorized": False,
        "capability_promotion_authorized": False,
        "human_final_acceptance_created": False,
    }
