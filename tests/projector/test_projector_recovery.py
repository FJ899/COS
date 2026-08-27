from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "projector_run.py"
IMPLEMENTATION_SHA = "2222222222222222222222222222222222222222"


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
        "raw_human_intent": "Recover this work later without relying on this conversation.",
        "bounded_target": "Maintain a durable recoverable state for the bounded work.",
        "goal": "Preserve enough durable state to continue correctly",
        "done": "A fresh process reconstructs the exact current state",
        "verification_method": "Run the recover command in a fresh process",
        "current_critical_unknown": "Will the first evidence update remain recoverable?",
        "assumptions": ["Filesystem persistence is available"],
        "known_human_authority_gates": [],
        "provenance": provenance(),
        "initial_route": {
            "route_id": "route-record",
            "next_move_kind": "EVIDENCE_SEEKING",
            "description": "Record one exact observation",
            "justification": "Recovery needs a material transition to reconstruct",
            "evidence_basis": [],
        },
    }


def evidence() -> dict:
    return {
        "evidence_id": "ev-recovery-1",
        "kind": "OBSERVATION",
        "scope": "TEST",
        "locator": "fixture://recovery-observation",
        "immutable_identity": "sha256:" + "a" * 64,
        "observed_at": "2026-08-26T00:01:00+00:00",
        "producer": "TEST_FIXTURE",
        "supports": ["R-010", "AC-003"],
    }


def transition_payload() -> dict:
    ref = evidence()
    return {
        "current_goal": "Preserve enough durable state to continue correctly",
        "current_done": "A fresh process reconstructs the exact current state",
        "observed_facts": ["One durable state transition was recorded"],
        "assumptions": ["Filesystem persistence remains available"],
        "claims": [],
        "unknowns": ["Whether a later actor can reconstruct without chat memory"],
        "critical_unknown_or_blocker": "Whether a later actor can reconstruct without chat memory",
        "material_evidence_refs": [ref],
        "route": {
            "route_id": "route-record",
            "next_move_kind": "VERIFY_RECOVERY",
            "description": "Recover the bundle in a fresh process",
            "justification": "The durable transition now exists and can be replayed",
            "evidence_basis": ["ev-recovery-1"],
        },
        "status": "ACTIVE",
        "transition_reason": "Persist the recovery checkpoint",
        "material_evidence_change": {
            "evidence_refs": ["ev-recovery-1"],
            "invalidates_current_route": False,
        },
        "evidence_basis": ["ev-recovery-1"],
        "human_intervention": None,
        "route_change": None,
        "goal_change": None,
    }


class ProjectorRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run_dir = self.root / "run-recovery"
        self._write_and_run("init.json", init_payload(), "init")
        self._write_and_run("transition.json", transition_payload(), "transition")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _run(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
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

    def _write_and_run(self, filename: str, payload: dict, command: str) -> None:
        path = self.root / filename
        path.write_text(json.dumps(payload), encoding="utf-8")
        self._run(command, "--run-dir", str(self.run_dir), "--input", str(path))

    def test_fresh_process_recovery_reconstructs_required_current_state_and_provenance(self) -> None:
        result = self._run("recover", "--run-dir", str(self.run_dir))
        recovered = json.loads(result.stdout)
        self.assertEqual("Preserve enough durable state to continue correctly", recovered["goal"])
        self.assertEqual("A fresh process reconstructs the exact current state", recovered["done"])
        self.assertEqual(["One durable state transition was recorded"], recovered["observed_facts"])
        self.assertEqual("Whether a later actor can reconstruct without chat memory", recovered["critical_unknown_or_blocker"])
        self.assertEqual("VERIFY_RECOVERY", recovered["route"]["next_move_kind"])
        self.assertEqual(1, recovered["latest_state_sequence"])
        self.assertEqual(IMPLEMENTATION_SHA, recovered["provenance"]["implementation"]["sha"])

    def test_verify_reports_exact_latest_state_identity(self) -> None:
        result = self._run("verify", "--run-dir", str(self.run_dir))
        verified = json.loads(result.stdout)
        state = json.loads((self.run_dir / "states" / "0001.json").read_text(encoding="utf-8"))
        self.assertEqual("VALID", verified["verification"])
        self.assertEqual(state["state_sha256"], verified["latest_state_sha256"])
        self.assertEqual(IMPLEMENTATION_SHA, verified["implementation_sha"])

    def test_corrupt_snapshot_fails_closed_in_recover_and_verify(self) -> None:
        path = self.run_dir / "states" / "0001.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["observed_facts"] = ["tampered after the fact"]
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        self._run("recover", "--run-dir", str(self.run_dir), expect=1)
        self._run("verify", "--run-dir", str(self.run_dir), expect=1)

    def test_missing_snapshot_in_chain_fails_closed(self) -> None:
        source = self.run_dir / "states" / "0001.json"
        target = self.run_dir / "states" / "0002.json"
        source.rename(target)
        self._run("verify", "--run-dir", str(self.run_dir), expect=1)

    def test_mutated_immutable_run_manifest_is_detected(self) -> None:
        path = self.run_dir / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["raw_human_intent"] = "silently rewritten intent"
        path.write_text(json.dumps(run, indent=2), encoding="utf-8")
        self._run("recover", "--run-dir", str(self.run_dir), expect=1)


if __name__ == "__main__":
    unittest.main()
