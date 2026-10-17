from __future__ import annotations

import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from projector_public_effect_trusted_runtime import (  # noqa: E402
    _GitHubGitEvidenceSource,
    _GitHubIssueCommentAuthoritySource,
    execute_trusted_public_effect,
    prepare_trusted_public_effect_authority_request,
)

REPOSITORY = "FJ899/executor-pilot-target"
ACTOR_LOGIN = "FJ899"
ACTOR_ID = 275481581
ISSUE_NUMBER = 99
COMMENT_ID = 123456


def run_git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


def human_comment(
    request: dict,
    *,
    actor_login: str = ACTOR_LOGIN,
    actor_id: int = ACTOR_ID,
    app: object | None = None,
) -> dict:
    body = {
        "schema_version": "projector-public-effect-human-decision/1.0",
        "request": request,
        "decision": "AUTHORIZE",
        "nonce": "human-test-authority-002",
    }
    return {
        "id": COMMENT_ID,
        "node_id": "IC_test_projector_authority_002",
        "issue_url": f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}",
        "user": {"login": actor_login, "id": actor_id, "type": "User"},
        "performed_via_github_app": app,
        "created_at": "2026-08-27T10:00:00Z",
        "updated_at": "2026-08-27T10:00:00Z",
        "body": json.dumps(body, sort_keys=True, separators=(",", ":")),
    }


class ExternalLikeFakeSink:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def write(self, descriptor: dict) -> dict:
        self.calls.append(json.loads(json.dumps(descriptor)))
        return {
            "result_ref": "fixture://external-like/result-1",
            "result_identity": "EXACT_NON_PUBLIC_TEST_RESULT",
            "observed_at": "2026-08-27T10:00:03Z",
        }


class TrustedRuntimeOriginIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.remote = root / "remote.git"
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.work = root / "work"
        subprocess.run(
            ["git", "clone", str(self.remote), str(self.work)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        run_git(self.work, "config", "user.name", "Projector Test")
        run_git(self.work, "config", "user.email", "projector-test@example.invalid")
        run_git(self.work, "checkout", "-b", "base")
        target = self.work / "project_registry" / "registry.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("VALUE = 1\n", encoding="utf-8")
        run_git(self.work, "add", "project_registry/registry.py")
        run_git(self.work, "commit", "-m", "base")
        self.base_sha = run_git(self.work, "rev-parse", "HEAD")
        run_git(self.work, "push", "origin", "base")

        run_git(self.work, "checkout", "-b", "candidate")
        target.write_text("VALUE = 2\n", encoding="utf-8")
        run_git(self.work, "add", "project_registry/registry.py")
        run_git(self.work, "commit", "-m", "candidate")
        self.candidate_sha = run_git(self.work, "rev-parse", "HEAD")

        self.spec = {
            "effect_kind": "PUSH_CANDIDATE_REF",
            "repository": REPOSITORY,
            "base_ref": "base",
            "candidate_ref_or_pr_head": "candidate",
            "frozen_source_sha": self.base_sha,
            "expected_public_result": {
                "draft_only": True,
                "merge_authorized": False,
                "candidate_sha": self.candidate_sha,
            },
        }
        self.locator = {
            "repository": REPOSITORY,
            "issue_number": ISSUE_NUMBER,
            "comment_id": COMMENT_ID,
            "actor_login": ACTOR_LOGIN,
            "actor_id": ACTOR_ID,
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _remote_redirect(self):
        return mock.patch.object(
            _GitHubGitEvidenceSource,
            "remote_url",
            new_callable=mock.PropertyMock,
            return_value=str(self.remote),
        )

    def _prepare(self) -> dict:
        with self._remote_redirect():
            return prepare_trusted_public_effect_authority_request(self.spec, self.work)

    def _execute(self, comment: dict, sink: ExternalLikeFakeSink) -> dict:
        with self._remote_redirect(), mock.patch.object(
            _GitHubIssueCommentAuthoritySource,
            "_fetch_comment",
            return_value=comment,
        ):
            return execute_trusted_public_effect(self.spec, self.locator, self.work, sink)

    def _advance_base(self) -> str:
        updater = Path(self.temp.name) / f"updater-{len(list(Path(self.temp.name).glob('updater-*')))}"
        subprocess.run(
            ["git", "clone", str(self.remote), str(updater)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        run_git(updater, "config", "user.name", "Projector Test")
        run_git(updater, "config", "user.email", "projector-test@example.invalid")
        run_git(updater, "checkout", "base")
        path = updater / "base-advance.txt"
        path.write_text("advanced\n", encoding="utf-8")
        run_git(updater, "add", "base-advance.txt")
        run_git(updater, "commit", "-m", "advance base")
        sha = run_git(updater, "rev-parse", "HEAD")
        run_git(updater, "push", "origin", "base")
        return sha

    def test_external_effect_api_accepts_no_evidence_source_objects(self) -> None:
        parameters = list(inspect.signature(execute_trusted_public_effect).parameters)
        self.assertEqual(parameters, ["spec", "human_authority_locator", "git_worktree", "sink"])
        self.assertNotIn("git_source", parameters)
        self.assertNotIn("human_authority_source", parameters)

    def test_production_sources_remove_test_factory_and_are_not_mutable_by_normal_setattr(self) -> None:
        git_source = _GitHubGitEvidenceSource(self.work, REPOSITORY)
        human_source = _GitHubIssueCommentAuthoritySource(
            REPOSITORY,
            ISSUE_NUMBER,
            COMMENT_ID,
            ACTOR_LOGIN,
            ACTOR_ID,
        )
        self.assertFalse(hasattr(type(git_source), "for_non_public_test"))
        self.assertFalse(hasattr(type(human_source), "for_non_public_test"))
        self.assertFalse(hasattr(git_source, "test_only"))
        self.assertFalse(hasattr(human_source, "test_only"))
        self.assertFalse(hasattr(human_source, "_test_comment"))
        self.assertEqual(git_source.remote_url, f"https://github.com/{REPOSITORY}.git")

        mutations = [
            (git_source, "test_only", False),
            (git_source, "remote_url", str(self.remote)),
            (human_source, "test_only", False),
            (human_source, "_test_comment", human_comment({})),
        ]
        for source, field, value in mutations:
            with self.subTest(field=field):
                before = repr(source)
                with self.assertRaises((AttributeError, TypeError)):
                    setattr(source, field, value)
                self.assertEqual(repr(source), before)

    def test_new_p4_mutable_adapter_counterexample_is_structurally_blocked(self) -> None:
        prepared = self._prepare()
        fake_comment = human_comment(prepared["authority_request"])
        git_source = _GitHubGitEvidenceSource(self.work, REPOSITORY)
        human_source = _GitHubIssueCommentAuthoritySource(
            REPOSITORY,
            ISSUE_NUMBER,
            COMMENT_ID,
            ACTOR_LOGIN,
            ACTOR_ID,
        )
        sink = ExternalLikeFakeSink()

        for source, field, value in [
            (git_source, "test_only", False),
            (git_source, "remote_url", str(self.remote)),
            (human_source, "test_only", False),
            (human_source, "_test_comment", fake_comment),
        ]:
            with self.subTest(field=field), self.assertRaises((AttributeError, TypeError)):
                setattr(source, field, value)

        result = execute_trusted_public_effect(
            self.spec,
            human_source,  # type: ignore[arg-type]
            git_source,  # type: ignore[arg-type]
            sink,
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertFalse(result["target_write_performed"])
        self.assertEqual(sink.calls, [])

    def test_internal_production_git_source_performs_positive_git_object_proof(self) -> None:
        result = self._prepare()
        self.assertEqual(result["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertEqual(result["trusted_source_origin"], "INTERNAL_PRODUCTION_GITHUB_GIT_SOURCE")
        prepared = result["prepared"]
        gate = prepared["public_effect_gate"]
        self.assertEqual(gate["fresh_base_sha"], self.base_sha)
        self.assertEqual(gate["candidate_sha"], self.candidate_sha)
        self.assertEqual(gate["base_relation"], "CURRENT_BASE_EQUALS_FROZEN_SOURCE")
        entry = gate["diff_manifest"]["changed_entries"][0]
        self.assertEqual(entry["base_object"]["object_type"], "blob")
        self.assertEqual(entry["candidate_object"]["object_type"], "blob")
        self.assertEqual(entry["base_object"]["git_mode"], "100644")
        self.assertEqual(entry["candidate_object"]["git_mode"], "100644")
        self.assertEqual(
            entry["base_object"]["object_id"],
            run_git(self.work, "rev-parse", f"{self.base_sha}:project_registry/registry.py"),
        )
        self.assertEqual(
            entry["candidate_object"]["object_id"],
            run_git(self.work, "rev-parse", f"{self.candidate_sha}:project_registry/registry.py"),
        )

    def test_internal_human_fetch_and_second_live_read_allow_exactly_one_sink_call(self) -> None:
        prepared = self._prepare()
        comment = human_comment(prepared["authority_request"])
        sink = ExternalLikeFakeSink()
        result = self._execute(comment, sink)
        self.assertEqual(result["status"], "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED")
        self.assertTrue(result["target_write_performed"])
        self.assertEqual(len(sink.calls), 1)
        self.assertEqual(result["trusted_source_boundary"]["caller_source_objects_accepted"], False)
        self.assertEqual(result["trusted_source_boundary"]["test_adapter_path_present"], False)
        self.assertTrue(result["public_effect_gate"]["human_authority_evidence_ref"].startswith("github-issue-comment:"))
        self.assertEqual(result["public_effect_gate"]["write_time_revalidation"], "PASS")
        self.assertFalse(result["merge_authorized"])
        self.assertFalse(result["release_authorized"])
        self.assertFalse(result["deploy_authorized"])
        self.assertFalse(result["capability_promotion_authorized"])
        self.assertFalse(result["human_final_acceptance_created"])

    def test_wrong_actor_or_app_mediated_comment_is_blocked_before_write(self) -> None:
        prepared = self._prepare()
        request = prepared["authority_request"]
        sink = ExternalLikeFakeSink()

        result = self._execute(human_comment(request, actor_login="attacker", actor_id=1), sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("actor identity", result["reason"])
        self.assertEqual(sink.calls, [])

        result = self._execute(human_comment(request, app={"slug": "automation"}), sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("GitHub App", result["reason"])
        self.assertEqual(sink.calls, [])

    def test_base_advance_after_human_request_blocks_zero_writes(self) -> None:
        prepared = self._prepare()
        comment = human_comment(prepared["authority_request"])
        self._advance_base()
        sink = ExternalLikeFakeSink()
        result = self._execute(comment, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertEqual(sink.calls, [])

    def test_race_between_first_and_second_internal_git_reads_blocks_zero_writes(self) -> None:
        prepared = self._prepare()
        comment = human_comment(prepared["authority_request"])
        sink = ExternalLikeFakeSink()
        original = _GitHubGitEvidenceSource.observe
        calls = 0

        def racing_observe(source: _GitHubGitEvidenceSource, spec: dict) -> dict:
            nonlocal calls
            calls += 1
            value = original(source, spec)
            if calls == 1:
                self._advance_base()
            return value

        with self._remote_redirect(), mock.patch.object(
            _GitHubIssueCommentAuthoritySource,
            "_fetch_comment",
            return_value=comment,
        ), mock.patch.object(
            _GitHubGitEvidenceSource,
            "observe",
            new=racing_observe,
        ):
            result = execute_trusted_public_effect(self.spec, self.locator, self.work, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertEqual(sink.calls, [])
        self.assertGreaterEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
