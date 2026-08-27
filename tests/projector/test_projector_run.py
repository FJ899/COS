from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "projector_run.py"
IMPLEMENTATION_SHA = "1111111111111111111111111111111111111111"


def provenance() -> dict:
    return {
        "task_contract": {
            "version": "v1.0",
            "commit": "ef128a0885310524475fba1cd291d1f34400b0cc",
            "path": "governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md",
        },
        "architecture_contract": {
            "version": "v2.0",
            "commit": "6916fa5ddb78604ccbf039576a0f1165d5a8a6a1",
            "path": "governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.0.md",
        },
        "implementation": {
            "repository": "FJ899/COS",
            "branch": "impl/projector-real-project-v2",
            "sha": IMPLEMENTATION_SHA,
        },
    }


def init_payload() -> dict:
    return {
        "raw_human_intent": "Find a bounded way to improve this real outcome without making me choose tooling.",
        "bounded_target": "Produce one observable outcome while preserving the Human goal.",
        "goal": "Improve the target outcome",
        "done": "The predefined external check reports the target effect",
        "verification_method": "Read the independently observable result artifact",
        "current_critical_unknown": "Which evidence-seeking route can produce the target effect?",
        "assumptions": ["Available tools can inspect the target state"],
        "known_human_authority_gates": ["Public or irreversible effect requires Human decision"],
        "provenance": provenance(),
        "initial_route": {
            "route_id": "route-inspect",
            "next_move_kind": "EVIDENCE_SEEKING",
            "description": "Inspect current target state",
            "justification": "Current state is unknown and inspection is reversible",
            "evidence_basis": [],
        },
    }


def evidence(evidence_id: str, scope: str, supports: list[str]) -> dict:
    return {
        "evidence_id": evidence_id,
        "kind": "OBSERVATION",
        "scope": scope,
        "locator": f"fixture://{evidence_id}",
        "immutable_identity": f"sha256:{evidence_id:0<64}"[:71],
        "observed_at": "2026-08-26T00:00:00+00:00",
        "producer": "TEST_FIXTURE",
        "supports": supports,
    }


def transition_payload(*, goal: str = "Improve the target outcome", done: str | None = None) -> dict:
    observed = evidence("ev-observed-1", "TEST", ["R-004"])
    return {
        "current_goal": goal,
        "current_done": done or "The predefined external check reports the target effect",
        "observed_facts": ["Current target state was inspected"],
        "assumptions": ["A reversible next move remains available"],
        "claims": ["The next move is likely to reduce uncertainty"],
        "unknowns": ["Whether the next move will produce the effect"],
        "critical_unknown_or_blocker": "Whether the next move will produce the effect",
        "material_evidence_refs": [observed],
        "route": {
            "route_id": "route-inspect",
            "next_move_kind": "EVIDENCE_SEEKING",
            "description": "Collect one more bounded observation",
            "justification": "The first observation did not yet establish effect",
            "evidence_basis": ["ev-observed-1"],
        },
        "status": "ACTIVE",
        "transition_reason": "Recorded new observed state",
        "material_evidence_change": {
            "evidence_refs": ["ev-observed-1"],
            "invalidates_current_route": False,
        },
        "evidence_basis": ["ev-observed-1"],
        "human_intervention": None,
        "route_change": None,
        "goal_change": None,
    }


class ProjectorRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run_dir = self.root / "run-core"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_input(self, name: str, payload: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def run_cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(expect, result.returncode, msg=result.stderr or result.stdout)
        return result

    def initialize(self) -> None:
        path = self.write_input("init.json", init_payload())
        self.run_cli("init", "--run-dir", str(self.run_dir), "--input", str(path))

    def test_init_records_rough_intent_binding_and_distinct_state_categories(self) -> None:
        self.initialize()
        run = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        state = json.loads((self.run_dir / "states" / "0000.json").read_text(encoding="utf-8"))
        self.assertEqual(init_payload()["raw_human_intent"], run["raw_human_intent"])
        self.assertEqual(init_payload()["bounded_target"], run["initial_binding"]["bounded_target"])
        self.assertEqual([], state["observed_facts"])
        self.assertEqual(init_payload()["assumptions"], state["assumptions"])
        self.assertEqual([], state["claims"])
        self.assertEqual([init_payload()["current_critical_unknown"]], state["unknowns"])
        self.assertEqual("ACTIVE", state["status"])

    def test_init_missing_required_field_creates_no_partial_bundle(self) -> None:
        payload = init_payload()
        del payload["done"]
        path = self.write_input("bad-init.json", payload)
        self.run_cli("init", "--run-dir", str(self.run_dir), "--input", str(path), expect=1)
        self.assertFalse(self.run_dir.exists())

    def test_unauthorized_goal_change_is_rejected_without_new_snapshot(self) -> None:
        self.initialize()
        payload = transition_payload(goal="Convenient replacement goal")
        path = self.write_input("bad-goal.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path), expect=1)
        self.assertFalse((self.run_dir / "states" / "0001.json").exists())

    def test_explicit_human_goal_change_requires_durable_human_decision_evidence(self) -> None:
        self.initialize()
        payload = transition_payload(goal="Human-approved revised outcome")
        decision = evidence("ev-human-goal", "HUMAN_DECISION", ["R-003", "R-013"])
        payload["material_evidence_refs"].append(decision)
        payload["evidence_basis"].append("ev-human-goal")
        payload["goal_change"] = {
            "type": "HUMAN_GOAL_CHANGE",
            "human_decision_evidence_ref": "ev-human-goal",
            "new_goal": "Human-approved revised outcome",
            "new_done": payload["current_done"],
        }
        payload["human_intervention"] = {
            "classification": "GENUINE_HUMAN_OWNED_GATE",
            "reason": "Human explicitly changed the goal",
            "authority_basis": "GOAL_OR_NORMATIVE_MEANING",
            "human_decision_evidence_ref": "ev-human-goal",
        }
        path = self.write_input("goal-change.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path))
        latest = json.loads((self.run_dir / "states" / "0001.json").read_text(encoding="utf-8"))
        self.assertEqual("Human-approved revised outcome", latest["current_goal"])
        self.assertEqual("HUMAN_GOAL_CHANGE", latest["goal_change"]["type"])

    def test_material_human_intervention_must_be_classified(self) -> None:
        self.initialize()
        payload = transition_payload()
        decision = evidence("ev-human-gate", "HUMAN_DECISION", ["R-006"])
        payload["material_evidence_refs"].append(decision)
        payload["human_intervention"] = {
            "classification": "UNCLASSIFIED",
            "reason": "Human answered a material question",
            "authority_basis": "GOAL_OR_NORMATIVE_MEANING",
            "human_decision_evidence_ref": "ev-human-gate",
        }
        path = self.write_input("bad-human.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path), expect=1)

    def test_genuine_human_gate_accepts_frozen_authority_basis_and_decision_evidence(self) -> None:
        self.initialize()
        payload = transition_payload()
        decision = evidence("ev-human-gate", "HUMAN_DECISION", ["R-006"])
        payload["material_evidence_refs"].append(decision)
        payload["human_intervention"] = {
            "classification": "GENUINE_HUMAN_OWNED_GATE",
            "reason": "A materially risky action needs Human authority",
            "authority_basis": "COSTLY_PUBLIC_DESTRUCTIVE_IRREVERSIBLE_OR_MATERIALLY_RISKY_EFFECT",
            "human_decision_evidence_ref": "ev-human-gate",
        }
        path = self.write_input("human-gate.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path))
        latest = json.loads((self.run_dir / "states" / "0001.json").read_text(encoding="utf-8"))
        self.assertEqual("GENUINE_HUMAN_OWNED_GATE", latest["human_intervention"]["classification"])

    def test_done_rejects_projector_internal_or_test_only_evidence(self) -> None:
        self.initialize()
        payload = transition_payload()
        payload["status"] = "DONE"
        payload["critical_unknown_or_blocker"] = None
        payload["unknowns"] = []
        path = self.write_input("fake-done.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path), expect=1)

    def test_done_accepts_workload_external_effect_reference(self) -> None:
        self.initialize()
        payload = transition_payload()
        external = evidence("ev-effect", "WORKLOAD_EXTERNAL", ["R-007", "AC-006"])
        payload["material_evidence_refs"].append(external)
        payload["evidence_basis"].append("ev-effect")
        payload["route"]["evidence_basis"].append("ev-effect")
        payload["status"] = "DONE"
        payload["critical_unknown_or_blocker"] = None
        payload["unknowns"] = []
        payload["transition_reason"] = "Predefined external verification observed the effect"
        payload["material_evidence_change"]["evidence_refs"].append("ev-effect")
        path = self.write_input("done.json", payload)
        self.run_cli("transition", "--run-dir", str(self.run_dir), "--input", str(path))
        latest = json.loads((self.run_dir / "states" / "0001.json").read_text(encoding="utf-8"))
        self.assertEqual("DONE", latest["status"])


if __name__ == "__main__":
    unittest.main()
