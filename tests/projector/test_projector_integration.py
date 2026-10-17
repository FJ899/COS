from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "projector_run.py"
IMPLEMENTATION_SHA = "3333333333333333333333333333333333333333"


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
        "raw_human_intent": "Get this bounded outcome despite uncertainty, but stop where I own the decision.",
        "bounded_target": "Reach one observable external effect through an evidence-driven route.",
        "goal": "Reach the bounded external effect",
        "done": "External verification reports the predefined effect",
        "verification_method": "Inspect the frozen workload-external result",
        "current_critical_unknown": "Will route A remain viable after inspection?",
        "assumptions": ["Route A is initially available"],
        "known_human_authority_gates": ["Materially risky external effect requires Human authority"],
        "provenance": provenance(),
        "initial_route": {
            "route_id": "route-A",
            "next_move_kind": "EVIDENCE_SEEKING",
            "description": "Inspect dependency A",
            "justification": "Dependency A appears to be the shortest reversible evidence path",
            "evidence_basis": [],
        },
    }


def ref(evidence_id: str, *, scope: str = "TEST", supports: list[str] | None = None) -> dict:
    return {
        "evidence_id": evidence_id,
        "kind": "OBSERVATION",
        "scope": scope,
        "locator": f"fixture://{evidence_id}",
        "immutable_identity": "sha256:" + (evidence_id.encode().hex() + "0" * 64)[:64],
        "observed_at": "2026-08-26T00:02:00+00:00",
        "producer": "TEST_FIXTURE",
        "supports": supports or ["R-005"],
    }


def base_transition(route_id: str, evidence_refs: list[dict], critical: str, *, status: str = "ACTIVE") -> dict:
    evidence_ids = [item["evidence_id"] for item in evidence_refs]
    return {
        "current_goal": "Reach the bounded external effect",
        "current_done": "External verification reports the predefined effect",
        "observed_facts": ["A material dependency result was observed"],
        "assumptions": [],
        "claims": [],
        "unknowns": [] if status == "DONE" else [critical],
        "critical_unknown_or_blocker": None if status == "DONE" else critical,
        "material_evidence_refs": evidence_refs,
        "route": {
            "route_id": route_id,
            "next_move_kind": "EVIDENCE_SEEKING" if status == "ACTIVE" else ("STOP" if status == "BLOCKED" else "DONE"),
            "description": "Continue from the latest evidence",
            "justification": "The latest evidence determines whether work reroutes, blocks, or completes",
            "evidence_basis": evidence_ids,
        },
        "status": status,
        "transition_reason": "Apply the material evidence result",
        "material_evidence_change": {
            "evidence_refs": evidence_ids,
            "invalidates_current_route": False,
        },
        "evidence_basis": evidence_ids,
        "human_intervention": None,
        "route_change": None,
        "goal_change": None,
    }


class ProjectorIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run_dir = self.root / "run-integration"
        self.init_file = self.write("init.json", init_payload())
        self.cli("init", "--run-dir", str(self.run_dir), "--input", str(self.init_file))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, payload: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
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

    def test_declared_route_invalidation_rejects_silent_old_route_and_accepts_explicit_reroute(self) -> None:
        failure = ref("ev-route-a-failed", supports=["R-005", "R-008", "AC-004"])
        stale = base_transition("route-A", [failure], "Which alternate route is viable?")
        stale["material_evidence_change"]["invalidates_current_route"] = True
        stale_file = self.write("stale.json", stale)
        self.cli("transition", "--run-dir", str(self.run_dir), "--input", str(stale_file), expect=1)
        self.assertFalse((self.run_dir / "states" / "0001.json").exists())

        reroute = base_transition("route-B", [failure], "Will route B produce the external effect?")
        reroute["material_evidence_change"]["invalidates_current_route"] = True
        reroute["route_change"] = {
            "from_route_id": "route-A",
            "to_route_id": "route-B",
            "reason": "Exact evidence shows dependency A is unavailable",
        }
        reroute["route"]["description"] = "Inspect dependency B"
        reroute_file = self.write("reroute.json", reroute)
        self.cli("transition", "--run-dir", str(self.run_dir), "--input", str(reroute_file))

        recovered = json.loads(self.cli("recover", "--run-dir", str(self.run_dir)).stdout)
        self.assertEqual("route-B", recovered["route"]["route_id"])
        self.assertEqual("Reach the bounded external effect", recovered["goal"])
        self.assertEqual(1, recovered["latest_state_sequence"])

    def test_declared_route_invalidation_may_truthfully_block_without_fabricating_success(self) -> None:
        failure = ref("ev-no-route", supports=["R-008", "AC-007"])
        blocked = base_transition("route-A", [failure], "No authorized route is currently available", status="BLOCKED")
        blocked["material_evidence_change"]["invalidates_current_route"] = True
        blocked["route"]["description"] = "Stop until a new authorized route exists"
        blocked_file = self.write("blocked.json", blocked)
        self.cli("transition", "--run-dir", str(self.run_dir), "--input", str(blocked_file))
        recovered = json.loads(self.cli("recover", "--run-dir", str(self.run_dir)).stdout)
        self.assertEqual("BLOCKED", recovered["status"])
        self.assertEqual("No authorized route is currently available", recovered["critical_unknown_or_blocker"])

    def test_human_operational_rescue_remains_visible_in_durable_state(self) -> None:
        observation = ref("ev-observed")
        rescue = ref("ev-human-rescue", scope="HUMAN_DECISION", supports=["R-006", "AC-005"])
        payload = base_transition("route-A", [observation, rescue], "Can the system proceed without more Human routing?")
        payload["human_intervention"] = {
            "classification": "HUMAN_OPERATIONAL_RESCUE",
            "reason": "Human supplied the routine next operational step",
            "authority_basis": "NONE_OPERATIONAL_RESCUE",
            "human_decision_evidence_ref": "ev-human-rescue",
        }
        path = self.write("rescue.json", payload)
        self.cli("transition", "--run-dir", str(self.run_dir), "--input", str(path))
        recovered = json.loads(self.cli("recover", "--run-dir", str(self.run_dir)).stdout)
        self.assertEqual("HUMAN_OPERATIONAL_RESCUE", recovered["human_intervention"]["classification"])

    def test_completed_implementation_stage_provenance_is_exact_and_recoverable(self) -> None:
        recovered = json.loads(self.cli("recover", "--run-dir", str(self.run_dir)).stdout)
        p = recovered["provenance"]
        self.assertEqual("v1.0", p["task_contract"]["version"])
        self.assertEqual("ef128a0885310524475fba1cd291d1f34400b0cc", p["task_contract"]["commit"])
        self.assertEqual("v2.0", p["architecture_contract"]["version"])
        self.assertEqual("6916fa5ddb78604ccbf039576a0f1165d5a8a6a1", p["architecture_contract"]["commit"])
        self.assertEqual("FJ899/COS", p["implementation"]["repository"])
        self.assertEqual("impl/projector-real-project-v2", p["implementation"]["branch"])
        self.assertEqual(IMPLEMENTATION_SHA, p["implementation"]["sha"])

    def test_wrong_frozen_architecture_identity_is_rejected_before_run_creation(self) -> None:
        other_dir = self.root / "run-wrong-provenance"
        payload = init_payload()
        payload["provenance"]["architecture_contract"]["commit"] = "0" * 40
        path = self.write("wrong-provenance.json", payload)
        self.cli("init", "--run-dir", str(other_dir), "--input", str(path), expect=1)
        self.assertFalse(other_dir.exists())


if __name__ == "__main__":
    unittest.main()
