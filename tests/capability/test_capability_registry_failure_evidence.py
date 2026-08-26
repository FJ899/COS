from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "verify_capability_evidence.py"
SPEC = importlib.util.spec_from_file_location("capability_gate_failure_evidence", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load capability gate")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class CapabilityRegistryFailureEvidence(unittest.TestCase):
    def test_behavior_insensitive_tested_fixture_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "governance").mkdir(parents=True)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "scripts").mkdir(parents=True)
            (root / "tests").mkdir(parents=True)
            (root / "governance" / "BEHAVIOR_FIRST_CAPABILITY_POLICY.md").write_text("policy\n", encoding="utf-8")
            (root / "governance" / "P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md").write_text("contract\n", encoding="utf-8")
            (root / "scripts" / "impl.py").write_text("def run(value=1):\n    return value * 2\n", encoding="utf-8")
            (root / "tests" / "positive.py").write_text("assert True\n", encoding="utf-8")
            (root / "tests" / "failure.py").write_text("assert True\n", encoding="utf-8")
            commands = ["python tests/positive.py", "python tests/failure.py"]
            (root / ".github" / "workflows" / "verify.yml").write_text("\n".join(commands) + "\n", encoding="utf-8")
            registry = {
                "schema_version": 1,
                "allowed_statuses": GATE.STATUSES,
                "capabilities": [
                    {
                        "id": "CAP-NEGATIVE-001",
                        "name": "negative fixture",
                        "claim": "behavior-insensitive evidence is rejected",
                        "status": "TESTED",
                        "implementation": ["scripts/impl.py"],
                        "executable_evidence": ["tests/positive.py"],
                        "failure_evidence": ["tests/failure.py"],
                        "integration_evidence": [],
                        "real_work_evidence": [],
                        "reliability_evidence": [],
                        "ci_commands": commands,
                        "integration_ci_commands": [],
                        "notes": "role-specific controlled failure evidence fixture",
                    }
                ],
            }
            (root / "governance" / "CAPABILITY_REGISTRY.json").write_text(
                json.dumps(registry, indent=2), encoding="utf-8"
            )
            errors = GATE.validate_repository(root)
            joined = "\n".join(errors)
            self.assertIn("behavior-insensitive / unconditional-success", joined)


if __name__ == "__main__":
    unittest.main()
