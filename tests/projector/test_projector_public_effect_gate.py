from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from projector_public_effect_gate import (  # noqa: E402
    BASE_ADVANCED,
    BASE_EQUALS,
    PublicEffectGateError,
    authority_request,
    execute_authorized_public_effect,
    prepare_public_effect_gate,
    write_record_exclusive_atomic,
)

S = "1" * 40
B2 = "2" * 40
C = "3" * 40
TREE = "4" * 40
MID = "5" * 40
MID_TREE = "6" * 40
BASE_BLOB = "a" * 40
CANDIDATE_BLOB = "b" * 40
OTHER_OBJECT = "c" * 40


class FakeSink:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def write(self, effect_descriptor: dict) -> dict:
        self.calls.append(copy.deepcopy(effect_descriptor))
        return {
            "result_ref": "fixture://public-effect/result-1",
            "result_identity": "remote-object:exact-1",
            "observed_at": "2026-08-27T00:00:03+00:00",
        }


def changed_entry(*, candidate_mode: str = "100644", candidate_type: str = "blob", candidate_object: str = CANDIDATE_BLOB) -> dict:
    return {
        "path": "project_registry/registry.py",
        "previous_path": None,
        "change_kind": "MODIFIED" if candidate_type == "blob" else "TYPE_CHANGED",
        "base_object": {
            "object_id": BASE_BLOB,
            "object_type": "blob",
            "git_mode": "100644",
        },
        "candidate_object": {
            "object_id": candidate_object,
            "object_type": candidate_type,
            "git_mode": candidate_mode,
        },
    }


def effect_input(
    *,
    effect_kind: str = "PUSH_CANDIDATE_REF",
    base_sha: str = S,
    purpose: str | None = None,
) -> dict:
    if purpose is None:
        purpose = "B_PRE_PUSH" if effect_kind == "PUSH_CANDIDATE_REF" else "B_PRE_PR"
    frozen_status = "EQUAL" if base_sha == S else "PROVEN_ANCESTOR"
    return {
        "effect_kind": effect_kind,
        "repository": "FJ899/executor-pilot-target",
        "base_ref": "case-003-broken",
        "candidate_ref_or_pr_head": "projector/v2-1-candidate",
        "frozen_source_sha": S,
        "base_observation": {
            "purpose": purpose,
            "repository": "FJ899/executor-pilot-target",
            "base_ref": "case-003-broken",
            "sha": base_sha,
            "observed_at": "2026-08-27T00:00:00+00:00",
            "evidence_ref": f"fixture://base/{purpose}/{base_sha}",
        },
        "candidate_observation": {
            "repository": "FJ899/executor-pilot-target",
            "candidate_ref_or_pr_head": "projector/v2-1-candidate",
            "sha": C,
            "tree_sha": TREE,
            "observed_at": "2026-08-27T00:00:01+00:00",
            "evidence_ref": "fixture://candidate/exact",
        },
        "ancestry": {
            "frozen_to_base": {
                "status": frozen_status,
                "evidence_ref": f"fixture://ancestry/frozen-base/{base_sha}",
            },
            "base_to_candidate": {
                "status": "PROVEN_ANCESTOR",
                "evidence_ref": f"fixture://ancestry/base-candidate/{base_sha}",
            },
            "merge_base_sha": base_sha,
        },
        "candidate_commit_topology": {
            "candidate_head_sha": C,
            "candidate_head_tree_sha": TREE,
            "candidate_commits": [
                {
                    "commit_sha": C,
                    "tree_sha": TREE,
                    "ordered_parent_shas": [base_sha],
                }
            ],
        },
        "changed_entries": [changed_entry()],
        "expected_public_result": {
            "draft_only": True,
            "merge_authorized": False,
            "candidate_sha": C,
        },
    }


def human_authority(prepared: dict) -> dict:
    return {
        **authority_request(prepared),
        "decision": "AUTHORIZE",
        "human_decision_evidence_ref": "fixture://human/public-effect-authority-1",
    }


def revalidation(prepared: dict) -> dict:
    gate = prepared["public_effect_gate"]
    return {
        "schema_version": "projector-public-effect-write-time-revalidation/1.0",
        "effect_kind": gate["effect_kind"],
        "repository": gate["repository"],
        "base_ref": gate["base_ref"],
        "candidate_ref_or_pr_head": gate["candidate_ref_or_pr_head"],
        "observed_base_sha": gate["fresh_base_sha"],
        "observed_candidate_sha": gate["candidate_sha"],
        "diff_manifest": copy.deepcopy(gate["diff_manifest"]),
        "effect_descriptor": copy.deepcopy(gate["effect_descriptor"]),
        "observed_at": "2026-08-27T00:00:02+00:00",
        "evidence_ref": "fixture://write-time/revalidation-1",
    }


class PublicEffectGateV21Tests(unittest.TestCase):
    def test_case1_equals_source_requires_remaining_exact_gates(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        self.assertEqual(prepared["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertEqual(prepared["public_effect_gate"]["base_relation"], BASE_EQUALS)

        broken = effect_input()
        broken["ancestry"]["base_to_candidate"]["status"] = "UNKNOWN"
        blocked = prepare_public_effect_gate(broken)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual(blocked["effect_evidence_status"], "UNKNOWN")
        self.assertFalse(blocked["target_write_performed"])

    def test_case2_is_advanced_from_frozen_source_not_diverged(self) -> None:
        prepared = prepare_public_effect_gate(effect_input(base_sha=B2))
        self.assertEqual(prepared["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        relation = prepared["public_effect_gate"]["base_relation"]
        self.assertEqual(relation, BASE_ADVANCED)
        self.assertNotIn("diverged", relation.lower())

    def test_push_and_pr_require_separate_fresh_base_observations(self) -> None:
        push = prepare_public_effect_gate(effect_input(effect_kind="PUSH_CANDIDATE_REF", base_sha=S))
        self.assertEqual(push["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")

        reused = effect_input(
            effect_kind="CREATE_OR_UPDATE_PR",
            base_sha=S,
            purpose="B_PRE_PUSH",
        )
        blocked = prepare_public_effect_gate(reused)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertIn("B_PRE_PR", blocked["reason"])

        pr = prepare_public_effect_gate(effect_input(effect_kind="CREATE_OR_UPDATE_PR", base_sha=B2))
        self.assertEqual(pr["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertEqual(pr["public_effect_gate"]["fresh_base_sha"], B2)
        self.assertNotEqual(push["public_effect_gate"]["diff_manifest_sha256"], pr["public_effect_gate"]["diff_manifest_sha256"])

        sink = FakeSink()
        result = execute_authorized_public_effect(pr, human_authority(push), revalidation(pr), sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(len(sink.calls), 0)

    def test_human_authority_is_exact_hash_and_target_authority(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        valid = human_authority(prepared)
        mutations = {
            "effect_kind": "CREATE_OR_UPDATE_PR",
            "B_PRE_X": B2,
            "C_PRE_X": "7" * 40,
            "D_HASH_X": "d" * 64,
            "E_HASH_X": "e" * 64,
            "candidate_ref_or_pr_head": "projector/other-candidate",
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                authority = copy.deepcopy(valid)
                authority[key] = value
                sink = FakeSink()
                result = execute_authorized_public_effect(prepared, authority, revalidation(prepared), sink)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
                self.assertEqual(len(sink.calls), 0)

    def test_mode_only_change_changes_authorized_diff_envelope(self) -> None:
        normal = effect_input()
        executable = effect_input()
        executable["changed_entries"] = [changed_entry(candidate_mode="100755")]
        first = prepare_public_effect_gate(normal)
        second = prepare_public_effect_gate(executable)
        self.assertNotEqual(
            first["public_effect_gate"]["diff_manifest_sha256"],
            second["public_effect_gate"]["diff_manifest_sha256"],
        )

    def test_object_type_change_changes_authorized_diff_envelope(self) -> None:
        normal = prepare_public_effect_gate(effect_input())
        changed = effect_input()
        changed["changed_entries"] = [
            changed_entry(candidate_mode="160000", candidate_type="commit", candidate_object=OTHER_OBJECT)
        ]
        typed = prepare_public_effect_gate(changed)
        self.assertEqual(typed["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertNotEqual(
            normal["public_effect_gate"]["diff_manifest_sha256"],
            typed["public_effect_gate"]["diff_manifest_sha256"],
        )

    def test_candidate_topology_changes_hash_even_with_same_final_tree(self) -> None:
        direct = prepare_public_effect_gate(effect_input())
        two_commit = effect_input()
        two_commit["candidate_commit_topology"]["candidate_commits"] = [
            {"commit_sha": MID, "tree_sha": MID_TREE, "ordered_parent_shas": [S]},
            {"commit_sha": C, "tree_sha": TREE, "ordered_parent_shas": [MID]},
        ]
        alternate = prepare_public_effect_gate(two_commit)
        self.assertEqual(alternate["status"], "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY")
        self.assertEqual(
            direct["public_effect_gate"]["candidate_tree_sha"],
            alternate["public_effect_gate"]["candidate_tree_sha"],
        )
        self.assertNotEqual(
            direct["public_effect_gate"]["diff_manifest_sha256"],
            alternate["public_effect_gate"]["diff_manifest_sha256"],
        )

    def test_unknown_identity_or_diff_is_blocked_and_never_calls_sink(self) -> None:
        cases: list[dict] = []

        missing_base = effect_input()
        missing_base["base_observation"]["sha"] = None
        cases.append(missing_base)

        unknown_ancestry = effect_input(base_sha=B2)
        unknown_ancestry["ancestry"]["frozen_to_base"]["status"] = "UNKNOWN"
        cases.append(unknown_ancestry)

        incomplete_diff = effect_input()
        incomplete_diff["changed_entries"][0]["candidate_object"]["git_mode"] = None
        cases.append(incomplete_diff)

        for payload in cases:
            blocked = prepare_public_effect_gate(payload)
            self.assertEqual(blocked["status"], "BLOCKED")
            self.assertEqual(blocked["effect_evidence_status"], "UNKNOWN")
            sink = FakeSink()
            result = execute_authorized_public_effect(blocked, {}, {}, sink)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(len(sink.calls), 0)

    def test_write_time_mismatch_after_human_authority_blocks_without_write(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        authority = human_authority(prepared)
        current = revalidation(prepared)
        current["observed_base_sha"] = B2
        sink = FakeSink()
        result = execute_authorized_public_effect(prepared, authority, current, sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["effect_evidence_status"], "UNKNOWN")
        self.assertFalse(result["target_write_performed"])
        self.assertEqual(len(sink.calls), 0)

    def test_success_preserves_exact_evidence_without_downstream_authority(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        authority = human_authority(prepared)
        current = revalidation(prepared)
        sink = FakeSink()
        result = execute_authorized_public_effect(prepared, authority, current, sink)

        self.assertEqual(result["status"], "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED")
        self.assertEqual(result["effect_evidence_status"], "OBSERVED")
        self.assertTrue(result["target_write_performed"])
        self.assertEqual(len(sink.calls), 1)
        self.assertEqual(sink.calls[0], prepared["public_effect_gate"]["effect_descriptor"])
        gate = result["public_effect_gate"]
        self.assertEqual(gate["authority_basis"], "PUBLIC_EFFECT")
        self.assertEqual(gate["human_authority_evidence_ref"], authority["human_decision_evidence_ref"])
        self.assertEqual(gate["write_time_revalidation"], "PASS")
        self.assertEqual(gate["diff_manifest_sha256"], prepared["public_effect_gate"]["diff_manifest_sha256"])
        self.assertEqual(gate["effect_sha256"], prepared["public_effect_gate"]["effect_sha256"])
        self.assertFalse(result["merge_authorized"])
        self.assertFalse(result["release_authorized"])
        self.assertFalse(result["deploy_authorized"])
        self.assertFalse(result["capability_promotion_authorized"])
        self.assertFalse(result["human_final_acceptance_created"])

        with tempfile.TemporaryDirectory() as temp_name:
            path = Path(temp_name) / "public-effect-result.json"
            write_record_exclusive_atomic(path, result)
            restored = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(restored, result)
            with self.assertRaises(PublicEffectGateError):
                write_record_exclusive_atomic(path, result)


if __name__ == "__main__":
    unittest.main()
