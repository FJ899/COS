from __future__ import annotations

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
    GitHubIssueCommentAuthoritySource,
    GitRepositoryEvidenceSource,
    InMemoryNonPublicTestSink,
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


def human_comment(request: dict, *, actor_login: str = ACTOR_LOGIN, actor_id: int = ACTOR_ID, app: object | None = None) -> dict:
    body = {
        "schema_version": "projector-public-effect-human-decision/1.0",
        "request": request,
        "decision": "AUTHORIZE",
        "nonce": "human-test-authority-001",
    }
    return {
        "id": COMMENT_ID,
        "node_id": "IC_test_projector_authority_001",
        "issue_url": f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}",
        "user": {"login": actor_login, "id": actor_id, "type": "User"},
        "performed_via_github_app": app,
        "created_at": "2026-08-27T09:00:00Z",
        "updated_at": "2026-08-27T09:00:00Z",
        "body": json.dumps(body, sort_keys=True, separators=(",", ":")),
    }


class ExternalLikeFakeSink:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def write(self, descriptor: dict) -> dict:
        self.calls.append(descriptor)
        return {"result_ref": "should-not-run", "result_identity": "should-not-run", "observed_at": "2026-08-27T09:00:00Z"}


class TrustedRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.remote = root / "remote.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.work = root / "work"
        subprocess.run(["git", "clone", str(self.remote), str(self.work)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        self.source = GitRepositoryEvidenceSource.for_non_public_test(self.work, REPOSITORY, str(self.remote))
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

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _authority_source(self, request: dict, **comment_kwargs: object) -> GitHubIssueCommentAuthoritySource:
        comment = human_comment(request, **comment_kwargs)
        return GitHubIssueCommentAuthoritySource.for_non_public_test(
            REPOSITORY,
            ISSUE_NUMBER,
            COMMENT_ID,
            ACTOR_LOGIN,
            ACTOR_ID,
            comment,
        )

    def _advance_base(self) -> str:
        updater = Path(self.temp.name) / f"updater-{len(list(Path(self.temp.name).glob('updater-*')))}"
        subprocess.run(["git", "clone", str(self.remote), str(updater)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    def test_trusted_git_adapter_performs_real_positive_proof_and_object_reads(self) -> None:
        result = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        self.assertEqual(result["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        prepared = result["prepared"]
        self.assertEqual(prepared["trust_level"], "TRUSTED_LIVE_GIT_PRE_HUMAN_GATE")
        gate = prepared["public_effect_gate"]
        self.assertEqual(gate["fresh_base_sha"], self.base_sha)
        self.assertEqual(gate["candidate_sha"], self.candidate_sha)
        self.assertEqual(gate["base_relation"], "CURRENT_BASE_EQUALS_FROZEN_SOURCE")
        entry = gate["diff_manifest"]["changed_entries"][0]
        self.assertEqual(entry["base_object"]["object_type"], "blob")
        self.assertEqual(entry["candidate_object"]["object_type"], "blob")
        self.assertEqual(entry["base_object"]["git_mode"], "100644")
        self.assertEqual(entry["candidate_object"]["git_mode"], "100644")
        self.assertEqual(entry["base_object"]["object_id"], run_git(self.work, "rev-parse", f"{self.base_sha}:project_registry/registry.py"))
        self.assertEqual(entry["candidate_object"]["object_id"], run_git(self.work, "rev-parse", f"{self.candidate_sha}:project_registry/registry.py"))

    def test_fresh_observation_is_new_invocation_and_push_pr_are_separate(self) -> None:
        push1 = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        push2 = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        self.assertNotEqual(push1["source_invocation_id"], push2["source_invocation_id"])
        self.assertEqual(push1["authority_request"], push2["authority_request"])

        run_git(self.work, "push", "origin", "candidate")
        pr_spec = dict(self.spec)
        pr_spec["effect_kind"] = "CREATE_OR_UPDATE_PR"
        pr = prepare_trusted_public_effect_authority_request(pr_spec, self.source)
        self.assertEqual(pr["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertNotEqual(push2["source_invocation_id"], pr["source_invocation_id"])
        self.assertEqual(pr["authority_request"]["effect_kind"], "CREATE_OR_UPDATE_PR")
        self.assertNotEqual(push2["authority_request"]["E_HASH_X"], pr["authority_request"]["E_HASH_X"])

    def test_genuine_human_comment_and_two_live_reads_allow_only_non_public_test_sink(self) -> None:
        prepared = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        authority_source = self._authority_source(prepared["authority_request"])
        sink = InMemoryNonPublicTestSink()
        result = execute_trusted_public_effect(self.spec, authority_source, self.source, sink)
        self.assertEqual(result["status"], "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED")
        self.assertTrue(result["target_write_performed"])
        self.assertEqual(len(sink.calls), 1)
        gate = result["public_effect_gate"]
        self.assertEqual(gate["authority_basis"], "PUBLIC_EFFECT")
        self.assertTrue(gate["human_authority_evidence_ref"].startswith("github-issue-comment:"))
        self.assertEqual(gate["write_time_revalidation"], "PASS")
        self.assertFalse(result["merge_authorized"])
        self.assertFalse(result["release_authorized"])
        self.assertFalse(result["deploy_authorized"])
        self.assertFalse(result["capability_promotion_authorized"])
        self.assertFalse(result["human_final_acceptance_created"])

    def test_test_only_sources_cannot_reach_external_sink(self) -> None:
        prepared = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        authority_source = self._authority_source(prepared["authority_request"])
        sink = ExternalLikeFakeSink()
        result = execute_trusted_public_effect(self.spec, authority_source, self.source, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason"], "TEST_ONLY_TRUSTED_SOURCE_CANNOT_REACH_EXTERNAL_SINK")
        self.assertEqual(sink.calls, [])

    def test_caller_fabricated_source_types_are_rejected_before_write(self) -> None:
        class FakeGit:
            pass

        class FakeHuman:
            pass

        sink = ExternalLikeFakeSink()
        result = execute_trusted_public_effect(self.spec, FakeHuman(), self.source, sink)  # type: ignore[arg-type]
        self.assertEqual(result["reason"], "UNTRUSTED_HUMAN_AUTHORITY_SOURCE_TYPE")
        self.assertEqual(sink.calls, [])
        result = execute_trusted_public_effect(self.spec, self._authority_source({}), FakeGit(), sink)  # type: ignore[arg-type]
        self.assertEqual(result["reason"], "UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
        self.assertEqual(sink.calls, [])

    def test_wrong_actor_or_app_mediated_human_comment_is_rejected(self) -> None:
        prepared = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        request = prepared["authority_request"]
        wrong_actor = self._authority_source(request, actor_login="attacker", actor_id=1)
        sink = InMemoryNonPublicTestSink()
        result = execute_trusted_public_effect(self.spec, wrong_actor, self.source, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("actor identity", result["reason"])
        self.assertEqual(sink.calls, [])

        app_comment = self._authority_source(request, app={"slug": "automation"})
        result = execute_trusted_public_effect(self.spec, app_comment, self.source, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("GitHub App", result["reason"])
        self.assertEqual(sink.calls, [])

    def test_base_advance_after_human_request_invalidates_old_authority(self) -> None:
        prepared = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        authority_source = self._authority_source(prepared["authority_request"])
        self._advance_base()
        sink = InMemoryNonPublicTestSink()
        result = execute_trusted_public_effect(self.spec, authority_source, self.source, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertEqual(sink.calls, [])

    def test_write_time_race_after_authority_verification_blocks_zero_writes(self) -> None:
        prepared = prepare_trusted_public_effect_authority_request(self.spec, self.source)
        authority_source = self._authority_source(prepared["authority_request"])
        sink = InMemoryNonPublicTestSink()
        original = self.source.observe
        calls = 0

        def racing_observe(spec: dict) -> dict:
            nonlocal calls
            calls += 1
            value = original(spec)
            if calls == 1:
                self._advance_base()
            return value

        with mock.patch.object(self.source, "observe", side_effect=racing_observe):
            result = execute_trusted_public_effect(self.spec, authority_source, self.source, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertEqual(sink.calls, [])
        self.assertGreaterEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
