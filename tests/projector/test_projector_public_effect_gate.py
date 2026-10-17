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
        return {"result_ref": "fixture://result", "result_identity": "fake", "observed_at": "2026-08-27T00:00:03+00:00"}


def changed_entry(*, candidate_mode: str = "100644", candidate_type: str = "blob", candidate_object: str = CANDIDATE_BLOB) -> dict:
    return {
        "path": "project_registry/registry.py",
        "previous_path": None,
        "change_kind": "MODIFIED" if candidate_type == "blob" else "TYPE_CHANGED",
        "base_object": {"object_id": BASE_BLOB, "object_type": "blob", "git_mode": "100644"},
        "candidate_object": {"object_id": candidate_object, "object_type": candidate_type, "git_mode": candidate_mode},
    }


def effect_input(*, effect_kind: str = "PUSH_CANDIDATE_REF", base_sha: str = S, purpose: str | None = None) -> dict:
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
            "frozen_to_base": {"status": frozen_status, "evidence_ref": f"fixture://ancestry/frozen-base/{base_sha}"},
            "base_to_candidate": {"status": "PROVEN_ANCESTOR", "evidence_ref": f"fixture://ancestry/base-candidate/{base_sha}"},
            "merge_base_sha": base_sha,
        },
        "candidate_commit_topology": {
            "candidate_head_sha": C,
            "candidate_head_tree_sha": TREE,
            "candidate_commits": [{"commit_sha": C, "tree_sha": TREE, "ordered_parent_shas": [base_sha]}],
        },
        "changed_entries": [changed_entry()],
        "expected_public_result": {"draft_only": True, "merge_authorized": False, "candidate_sha": C},
    }


def caller_authority(prepared: dict) -> dict:
    return {**authority_request(prepared), "decision": "AUTHORIZE", "human_decision_evidence_ref": "fake://not-human"}


def caller_revalidation(prepared: dict) -> dict:
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
        "evidence_ref": "fake://not-live",
    }


class PublicEffectPureBuilderTests(unittest.TestCase):
    def test_case1_equals_source_requires_remaining_exact_gates(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        self.assertEqual(prepared["public_effect_gate"]["base_relation"], BASE_EQUALS)
        broken = effect_input()
        broken["ancestry"]["base_to_candidate"]["status"] = "UNKNOWN"
        self.assertEqual(prepare_public_effect_gate(broken)["status"], "BLOCKED")

    def test_case2_exact_semantics_not_diverged(self) -> None:
        prepared = prepare_public_effect_gate(effect_input(base_sha=B2))
        relation = prepared["public_effect_gate"]["base_relation"]
        self.assertEqual(relation, BASE_ADVANCED)
        self.assertNotIn("diverged", relation.lower())

    def test_push_and_pr_purpose_are_separate(self) -> None:
        reused = effect_input(effect_kind="CREATE_OR_UPDATE_PR", purpose="B_PRE_PUSH")
        blocked = prepare_public_effect_gate(reused)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertIn("B_PRE_PR", blocked["reason"])

    def test_mode_only_change_changes_diff_hash(self) -> None:
        a = prepare_public_effect_gate(effect_input())
        b = effect_input()
        b["changed_entries"] = [changed_entry(candidate_mode="100755")]
        b = prepare_public_effect_gate(b)
        self.assertNotEqual(a["public_effect_gate"]["diff_manifest_sha256"], b["public_effect_gate"]["diff_manifest_sha256"])

    def test_object_type_change_changes_diff_hash(self) -> None:
        a = prepare_public_effect_gate(effect_input())
        b = effect_input()
        b["changed_entries"] = [changed_entry(candidate_mode="160000", candidate_type="commit", candidate_object=OTHER_OBJECT)]
        b = prepare_public_effect_gate(b)
        self.assertNotEqual(a["public_effect_gate"]["diff_manifest_sha256"], b["public_effect_gate"]["diff_manifest_sha256"])

    def test_topology_change_changes_diff_hash_same_final_tree(self) -> None:
        direct = prepare_public_effect_gate(effect_input())
        data = effect_input()
        data["candidate_commit_topology"]["candidate_commits"] = [
            {"commit_sha": MID, "tree_sha": MID_TREE, "ordered_parent_shas": [S]},
            {"commit_sha": C, "tree_sha": TREE, "ordered_parent_shas": [MID]},
        ]
        alternate = prepare_public_effect_gate(data)
        self.assertEqual(direct["public_effect_gate"]["candidate_tree_sha"], alternate["public_effect_gate"]["candidate_tree_sha"])
        self.assertNotEqual(direct["public_effect_gate"]["diff_manifest_sha256"], alternate["public_effect_gate"]["diff_manifest_sha256"])

    def test_unknown_identity_is_blocked(self) -> None:
        data = effect_input()
        data["base_observation"]["sha"] = None
        blocked = prepare_public_effect_gate(data)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual(blocked["effect_evidence_status"], "UNKNOWN")

    def test_p4_counterexample_is_physically_disarmed(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        sink = FakeSink()
        result = execute_authorized_public_effect(prepared, caller_authority(prepared), caller_revalidation(prepared), sink)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason"], "UNTRUSTED_CALLER_EVIDENCE_NOT_EFFECT_CAPABLE")
        self.assertFalse(result["target_write_performed"])
        self.assertEqual(sink.calls, [])

    def test_pure_builder_explicitly_marks_untrusted(self) -> None:
        prepared = prepare_public_effect_gate(effect_input())
        self.assertEqual(prepared["trust_level"], "CALLER_DECLARED_NOT_EFFECT_CAPABLE")

    def test_append_only_record_still_preserves_exact_bytes(self) -> None:
        value = prepare_public_effect_gate(effect_input())
        with tempfile.TemporaryDirectory() as temp_name:
            path = Path(temp_name) / "record.json"
            write_record_exclusive_atomic(path, value)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), value)
            with self.assertRaises(PublicEffectGateError):
                write_record_exclusive_atomic(path, value)


if __name__ == "__main__":
    unittest.main()
