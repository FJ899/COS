#!/usr/bin/env python3
"""Canonical effect-capable Projector v2.1 trusted runtime.

The external-write API deliberately does *not* accept Git/Human evidence-source
objects from its caller.  It snapshots caller locators, constructs immutable
production sources internally, performs two distinct live Git observations and
fetches one immutable GitHub Issue Comment between them.  Test adapters are not
part of this module's effect-capable API.
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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from projector_public_effect_gate import (
    EFFECT_KINDS,
    EQUAL,
    OBJECT_TYPES,
    PROVEN_ANCESTOR,
    PublicEffectGateError,
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
    write_record_exclusive_atomic,
)

AUTHORITY_POLICY_PATH = (
    Path(__file__).resolve().parents[1] / "governance" / "PROJECTOR_AUTHORITY_POLICY.json"
)
AUTHORITY_POLICY_SHA256 = "117d487c55f0cd7b0e9ba6acf5fe28a928a6b2a30a318f6e76979029172bde8d"
GIT_COMMAND_TIMEOUT_SECONDS = 30


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _repo_name(value: str) -> str:
    if value.count("/") != 1 or any(
        character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_./"
        for character in value
    ):
        raise _Blocked("repository must use owner/name form")
    return value


def _branch_name(ref: str, name: str) -> str:
    value = _string(ref, name)
    value = value[len("refs/heads/") :] if value.startswith("refs/heads/") else value
    if (
        value.startswith("-")
        or value.endswith((".", "/"))
        or ".." in value
        or "@{" in value
        or any(character in value for character in " ~^:?*[\\\n\r\t")
    ):
        raise _Blocked(f"{name} is not a safe branch name")
    return value


def _load_authority_policy(repository: str) -> set[tuple[str, int]]:
    try:
        raw_bytes = AUTHORITY_POLICY_PATH.read_bytes()
        if hashlib.sha256(raw_bytes).hexdigest() != AUTHORITY_POLICY_SHA256:
            raise _Blocked("trusted Human authority policy identity mismatch")
        policy = json.loads(raw_bytes.decode("utf-8"))
    except _Blocked:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _Blocked(f"trusted Human authority policy unavailable: {exc}") from exc
    policy = _object(policy, "Human authority policy")
    if set(policy) != {
        "schema_version",
        "operational_profile",
        "public_effects_enabled",
        "repository_owners",
        "authorized_humans",
    }:
        raise _Blocked("Human authority policy must contain exact fields")
    if policy.get("schema_version") != "projector-authority-policy/1.1":
        raise _Blocked("Human authority policy schema mismatch")
    if policy.get("operational_profile") != "PRIVATE_SINGLE_USER_ANALYSIS_ONLY":
        raise _Blocked("unsupported Projector operational profile")
    if policy.get("public_effects_enabled") is not False:
        raise _Blocked("public effects cannot be enabled in the private analysis profile")
    raise _Blocked("PUBLIC_EFFECTS_DISABLED_BY_OPERATIONAL_PROFILE")


def _authorized_humans_from_enabled_policy(policy: dict[str, Any], repository: str) -> set[tuple[str, int]]:
    """Validate actors for a future profile that explicitly enables effects.

    The current pinned profile always blocks before reaching this helper.  It
    remains separate so the existing verification suite can exercise the
    dormant effect boundary without weakening the production default.
    """
    owners = policy.get("repository_owners")
    humans = policy.get("authorized_humans")
    if not isinstance(owners, list) or repository.split("/", 1)[0] not in owners:
        raise _Blocked("repository owner is not authorized by trusted Human authority policy")
    if not isinstance(humans, list):
        raise _Blocked("Human authority policy authorized_humans must be a list")
    authorized: set[tuple[str, int]] = set()
    for index, human in enumerate(humans):
        human = _object(human, f"Human authority policy authorized_humans[{index}]")
        if set(human) != {"github_login", "github_user_id", "authority_scopes"}:
            raise _Blocked("Human authority policy actor must contain exact fields")
        scopes = human.get("authority_scopes")
        if not isinstance(scopes, list) or "PUBLIC_EFFECT" not in scopes:
            continue
        authorized.add(
            (
                _string(human.get("github_login"), "policy github_login"),
                _positive_int(human.get("github_user_id"), "policy github_user_id"),
            )
        )
    if not authorized:
        raise _Blocked("Human authority policy contains no PUBLIC_EFFECT authority")
    return authorized


def _positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise _Blocked(f"{name} must be a positive integer")
    return value


def _json_snapshot(value: Any, name: str) -> dict[str, Any]:
    """Detach runtime decisions from subsequent caller mutation."""
    try:
        cloned = json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))
    except (TypeError, ValueError) as exc:
        raise _Blocked(f"{name} must be exact JSON data") from exc
    return _object(cloned, name)


@dataclass(frozen=True, slots=True, init=False)
class _GitHubGitEvidenceSource:
    """Immutable production Git reader bound to github.com/<repository>.git.

    There is no test factory, mutable ``test_only`` marker, or stored mutable
    remote URL.  The canonical remote is derived from the frozen repository
    identity every time it is used.
    """

    worktree: Path
    repository: str

    def __init__(self, worktree: str | Path, repository: str) -> None:
        resolved = Path(worktree).resolve()
        repo = _repo_name(repository)
        if not (resolved / ".git").exists():
            raise _Blocked("trusted Git worktree must contain .git")
        object.__setattr__(self, "worktree", resolved)
        object.__setattr__(self, "repository", repo)

    @property
    def remote_url(self) -> str:
        return f"https://github.com/{self.repository}.git"

    def _git_env(self) -> dict[str, str]:
        """Prevent replace refs and caller-provided process-level Git overrides."""
        env = dict(os.environ)
        for key in list(env):
            if key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
                env.pop(key, None)
        env.pop("GIT_CONFIG_COUNT", None)
        env.pop("GIT_ALTERNATE_OBJECT_DIRECTORIES", None)
        env.pop("GIT_OBJECT_DIRECTORY", None)
        env.pop("GIT_REPLACE_REF_BASE", None)
        env["GIT_NO_REPLACE_OBJECTS"] = "1"
        return env

    def _run(self, args: list[str], *, text: bool = True, check: bool = True) -> str | bytes:
        try:
            proc = subprocess.run(
                ["git", "-C", str(self.worktree), *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=text,
                check=False,
                env=self._git_env(),
                timeout=GIT_COMMAND_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
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
            env=self._git_env(),
            timeout=GIT_COMMAND_TIMEOUT_SECONDS,
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
            [
                "diff",
                "--raw",
                "-z",
                "--no-abbrev",
                "--find-renames",
                "--find-copies",
                base_sha,
                candidate_sha,
                "--",
            ],
            text=False,
        )
        assert isinstance(output, bytes)
        parts = output.split(b"\0")
        entries: list[dict[str, Any]] = []
        index = 0
        kind_map = {
            "A": "ADDED",
            "M": "MODIFIED",
            "D": "DELETED",
            "R": "RENAMED",
            "C": "COPIED",
            "T": "TYPE_CHANGED",
        }
        while index < len(parts) and parts[index]:
            token = parts[index].decode("utf-8", "surrogateescape")
            index += 1
            if "\t" in token:
                header, first_path = token.split("\t", 1)
            else:
                header = token
                if index >= len(parts):
                    raise _Blocked("malformed trusted raw diff")
                first_path = parts[index].decode("utf-8", "surrogateescape")
                index += 1
            fields = header[1:].split()
            if not header.startswith(":") or len(fields) < 5:
                raise _Blocked("malformed trusted raw diff header")
            old_mode, new_mode, old_oid, new_oid, status = fields[:5]
            code = status[0]
            if code not in kind_map:
                raise _Blocked(f"unsupported trusted Git diff status: {status}")
            if code in {"R", "C"}:
                if index >= len(parts):
                    raise _Blocked("malformed trusted rename/copy diff")
                second_path = parts[index].decode("utf-8", "surrogateescape")
                index += 1
                previous_path, path = first_path, second_path
            else:
                previous_path, path = None, first_path

            def git_object(mode: str, oid: str) -> dict[str, Any]:
                if mode == "000000" or set(oid) == {"0"}:
                    return {"object_id": None, "object_type": None, "git_mode": None}
                exact_oid = _sha40(oid, "trusted diff object id")
                return {
                    "object_id": exact_oid,
                    "object_type": self._object_type(exact_oid),
                    "git_mode": mode,
                }

            entries.append(
                {
                    "path": path,
                    "previous_path": previous_path,
                    "change_kind": kind_map[code],
                    "base_object": git_object(old_mode, old_oid),
                    "candidate_object": git_object(new_mode, new_oid),
                }
            )
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
            items.append(
                {
                    "commit_sha": _sha40(sha, "topology commit"),
                    "tree_sha": _sha40(tree_sha, "topology tree"),
                    "ordered_parent_shas": [_sha40(parent, "topology parent") for parent in parents.split() if parent],
                }
            )
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
        candidate_ref = _branch_name(
            _string(spec.get("candidate_ref_or_pr_head"), "candidate_ref_or_pr_head"),
            "candidate_ref_or_pr_head",
        )
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

    def effect_journal_dir(self) -> Path:
        git_dir_raw = self._run(["rev-parse", "--git-dir"])
        assert isinstance(git_dir_raw, str)
        git_dir = Path(git_dir_raw.strip())
        if not git_dir.is_absolute():
            git_dir = self.worktree / git_dir
        return git_dir.resolve() / "projector-public-effects"


@dataclass(frozen=True, slots=True, init=False)
class _GitHubIssueCommentAuthoritySource:
    """Immutable production Human source that always performs a GitHub GET."""

    repository: str
    issue_number: int
    comment_id: int
    actor_login: str
    actor_id: int

    def __init__(
        self,
        repository: str,
        issue_number: int,
        comment_id: int,
        actor_login: str,
        actor_id: int,
    ) -> None:
        object.__setattr__(self, "repository", _repo_name(repository))
        object.__setattr__(self, "issue_number", _positive_int(issue_number, "issue_number"))
        object.__setattr__(self, "comment_id", _positive_int(comment_id, "comment_id"))
        object.__setattr__(self, "actor_login", _string(actor_login, "actor_login"))
        object.__setattr__(self, "actor_id", _positive_int(actor_id, "actor_id"))

    def _fetch_comment(self) -> dict[str, Any]:
        url = f"https://api.github.com/repos/{self.repository}/issues/comments/{self.comment_id}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        token = os.environ.get("GITHUB_TOKEN")
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


def _authority_locator(value: Any, repository: str) -> tuple[int, int, str, int]:
    locator = _json_snapshot(value, "human authority locator")
    required = {"repository", "issue_number", "comment_id", "actor_login", "actor_id"}
    if set(locator) != required:
        raise _Blocked("human authority locator must contain exact locator fields")
    locator_repo = _repo_name(_string(locator.get("repository"), "human authority locator.repository"))
    if locator_repo != repository:
        raise _Blocked("Human authority locator is bound to a different repository")
    resolved = (
        _positive_int(locator.get("issue_number"), "human authority locator.issue_number"),
        _positive_int(locator.get("comment_id"), "human authority locator.comment_id"),
        _string(locator.get("actor_login"), "human authority locator.actor_login"),
        _positive_int(locator.get("actor_id"), "human authority locator.actor_id"),
    )
    if (resolved[2], resolved[3]) not in _load_authority_policy(repository):
        raise _Blocked("Human authority actor is not authorized by trusted policy")
    return resolved


def _canonicalize_trusted_git_proof(observed: dict[str, Any]) -> dict[str, Any]:
    """Make D_HASH fact-stable while freshness stays invocation-bound."""
    value = copy.deepcopy(observed)
    repository = value["repository"]
    frozen = value["frozen_source_sha"]
    base = value["base_observation"]["sha"]
    candidate = value["candidate_observation"]["sha"]
    frozen_status = value["ancestry"]["frozen_to_base"]["status"]
    candidate_status = value["ancestry"]["base_to_candidate"]["status"]
    value["ancestry"]["frozen_to_base"]["evidence_ref"] = (
        f"git-proof:{repository}:frozen-to-base:{frozen_status}:{frozen}:{base}"
    )
    value["ancestry"]["base_to_candidate"]["evidence_ref"] = (
        f"git-proof:{repository}:base-to-candidate:{candidate_status}:{base}:{candidate}"
    )
    return value


def _fresh_prepare(
    spec: dict[str, Any],
    git_source: _GitHubGitEvidenceSource,
    trust_level: str,
) -> dict[str, Any]:
    observed = git_source.observe(spec)
    canonical = _canonicalize_trusted_git_proof(observed)
    return _prepare(canonical, trust_level=trust_level)


def prepare_trusted_public_effect_authority_request(
    spec: dict[str, Any],
    git_worktree: str | Path,
) -> dict[str, Any]:
    """Fresh production Git observation for the Human gate; never writes target."""
    try:
        spec_snapshot = _json_snapshot(spec, "effect spec")
        repository = _repo_name(_string(spec_snapshot.get("repository"), "repository"))
        _load_authority_policy(repository)
        git_source = _GitHubGitEvidenceSource(git_worktree, repository)
        prepared = _fresh_prepare(spec_snapshot, git_source, "TRUSTED_LIVE_GIT_PRE_HUMAN_GATE")
        return {
            "status": "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY",
            "prepared": prepared,
            "authority_request": authority_request(prepared),
            "source_invocation_id": prepared["source_invocation_id"],
            "trusted_source_origin": "INTERNAL_PRODUCTION_GITHUB_GIT_SOURCE",
            "target_write_performed": False,
        }
    except _Blocked as exc:
        return _blocked(exc.reason)
    except Exception as exc:
        return _blocked(f"TRUSTED_SOURCE_FAILURE:{type(exc).__name__}")


def execute_trusted_public_effect(
    spec: dict[str, Any],
    human_authority_locator: dict[str, Any],
    git_worktree: str | Path,
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """SOLE external-effect API: internally created live Git/Human sources -> write.

    No Git or Human evidence-source object is accepted from the caller.  The
    production Git remote is derived internally from the exact repository.  The
    Human source always performs a GitHub GET; there is no synthetic comment
    field or test-only switch on either production source.
    """

    try:
        spec_snapshot = _json_snapshot(spec, "effect spec")
        repository = _repo_name(_string(spec_snapshot.get("repository"), "repository"))
        issue_number, comment_id, actor_login, actor_id = _authority_locator(
            human_authority_locator,
            repository,
        )

        git_source = _GitHubGitEvidenceSource(git_worktree, repository)
        human_source = _GitHubIssueCommentAuthoritySource(
            repository,
            issue_number,
            comment_id,
            actor_login,
            actor_id,
        )

        pre_authority = _fresh_prepare(
            spec_snapshot,
            git_source,
            "TRUSTED_LIVE_GIT_AUTHORITY_VERIFICATION",
        )
        request = authority_request(pre_authority)
        authority = human_source.load_authority(request)
        _validate_human_authority(pre_authority, authority)

        write_time = _fresh_prepare(
            spec_snapshot,
            git_source,
            "TRUSTED_LIVE_GIT_WRITE_TIME_REVALIDATION",
        )
        if pre_authority["source_invocation_id"] == write_time["source_invocation_id"]:
            raise _Blocked("write-time Git observation was not a distinct trusted invocation")
        if authority_request(write_time) != request:
            raise _Blocked("write-time live Git state differs from Human-authorized tuple")
        _validate_human_authority(write_time, authority)

        gate = write_time["public_effect_gate"]
        authority_identity = hashlib.sha256(
            authority["human_decision_evidence_ref"].encode("utf-8")
        ).hexdigest()
        journal_root = git_source.effect_journal_dir()
        attempt_dir = journal_root / f"{gate['effect_sha256']}-{authority_identity}"
        reservation_path = attempt_dir / "0001-WRITE_RESERVED.json"
        write_record_exclusive_atomic(
            reservation_path,
            {
                "schema_version": "projector-public-effect-journal/1.0",
                "status": "WRITE_RESERVED",
                "reserved_at": _utc_now(),
                "authority_request": request,
                "human_authority": authority,
                "public_effect_gate": gate,
            },
        )
    except _Blocked as exc:
        return _blocked(exc.reason)
    except PublicEffectGateError as exc:
        if "refusing to overwrite public-effect evidence" in str(exc):
            return _blocked("PUBLIC_EFFECT_AUTHORITY_REPLAY_BLOCKED")
        return _blocked(f"PUBLIC_EFFECT_JOURNAL_FAILURE:{type(exc).__name__}")
    except Exception as exc:
        return _blocked(f"TRUSTED_SOURCE_FAILURE:{type(exc).__name__}")

    try:
        write_result = sink.write(gate["effect_descriptor"])
        result = _validated_write_result(
            write_result,
            gate["effect_descriptor"]["expected_public_result"],
        )
    except Exception as exc:
        failure = {
            "schema_version": "projector-public-effect-journal/1.0",
            "status": "RECONCILIATION_REQUIRED",
            "recorded_at": _utc_now(),
            "reason": f"{type(exc).__name__}:{exc}",
            "target_write_performed": "UNKNOWN",
            "public_effect_gate": gate,
        }
        try:
            write_record_exclusive_atomic(attempt_dir / "0002-RECONCILIATION_REQUIRED.json", failure)
        except Exception:
            pass
        return {
            **failure,
            "effect_evidence_status": "UNKNOWN",
            "target_write_result": "UNKNOWN_REQUIRES_RECONCILIATION",
            "next_route": "RECONCILE_REMOTE_STATE_BEFORE_ANY_RETRY",
            "merge_authorized": False,
            "release_authorized": False,
            "deploy_authorized": False,
            "capability_promotion_authorized": False,
            "human_final_acceptance_created": False,
        }

    completed = {
        "schema_version": "projector-public-effect-gate-result/1.2",
        "status": "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED",
        "effect_evidence_status": "OBSERVED",
        "target_write_performed": True,
        "target_write_result": result,
        "trusted_source_boundary": {
            "git": "INTERNAL_PRODUCTION_GITHUB_GIT_SOURCE",
            "human": "INTERNAL_PRODUCTION_GITHUB_ISSUE_COMMENT_SOURCE",
            "caller_source_objects_accepted": False,
            "test_adapter_path_present": False,
        },
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
    try:
        write_record_exclusive_atomic(attempt_dir / "0002-WRITE_OBSERVED.json", completed)
    except Exception as exc:
        return {
            "schema_version": "projector-public-effect-journal/1.0",
            "status": "RECONCILIATION_REQUIRED",
            "effect_evidence_status": "OBSERVED_BUT_DURABLE_RECORD_FAILED",
            "target_write_performed": True,
            "target_write_result": result,
            "reason": f"DURABLE_RESULT_RECORD_FAILED:{type(exc).__name__}",
            "next_route": "PRESERVE_RESULT_AND_RECONCILE_BEFORE_ANY_RETRY",
            "merge_authorized": False,
            "release_authorized": False,
            "deploy_authorized": False,
            "capability_promotion_authorized": False,
            "human_final_acceptance_created": False,
        }
    return completed
