from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "verify_capability_evidence.py"
SPEC = importlib.util.spec_from_file_location("capability_gate_positive_evidence", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load capability gate")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class CapabilityRegistryPositiveEvidence(unittest.TestCase):
    def test_behavior_sensitive_tested_fixture_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "governance").mkdir(parents=True)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "scripts").mkdir(parents=True)
            (root / "tests").mkdir(parents=True)
            (root / "governance" / "BEHAVIOR_FIRST_CAPABILITY_POLICY.md").write_text("policy\n", encoding="utf-8")
            (root / "governance" / "P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md").write_text("contract\n", encoding="utf-8")
            (root / "scripts" / "impl.py").write_text(
                "def run(value):\n"
                "    if value < 0:\n"
                "        raise ValueError('negative input')\n"
                "    return value * 2\n",
                encoding="utf-8",
            )
            loader = (
                "import importlib.util\n"
                "from pathlib import Path\n"
                "impl_path = Path(__file__).resolve().parents[1] / 'scripts' / 'impl.py'\n"
                "spec = importlib.util.spec_from_file_location('fixture_impl', impl_path)\n"
                "module = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(module)\n"
            )
            positive = loader + "assert module.run(2) == 4\n"
            failure = (
                loader
                + "try:\n"
                + "    module.run(-1)\n"
                + "except ValueError as exc:\n"
                + "    assert 'negative input' in str(exc)\n"
                + "else:\n"
                + "    raise AssertionError('expected ValueError')\n"
            )
            (root / "tests" / "positive.py").write_text(positive, encoding="utf-8")
            (root / "tests" / "failure.py").write_text(failure, encoding="utf-8")
            commands = ["python tests/positive.py", "python tests/failure.py"]
            (root / ".github" / "workflows" / "verify.yml").write_text("\n".join(commands) + "\n", encoding="utf-8")
            registry = {
                "schema_version": 1,
                "allowed_statuses": GATE.STATUSES,
                "capabilities": [
                    {
                        "id": "CAP-POSITIVE-001",
                        "name": "positive fixture",
                        "claim": "positive and controlled failure behavior are observed",
                        "status": "TESTED",
                        "implementation": ["scripts/impl.py"],
                        "executable_evidence": ["tests/positive.py"],
                        "failure_evidence": ["tests/failure.py"],
                        "integration_evidence": [],
                        "real_work_evidence": [],
                        "reliability_evidence": [],
                        "ci_commands": commands,
                        "integration_ci_commands": [],
                        "notes": "role-specific positive evidence fixture",
                    }
                ],
            }
            (root / "governance" / "CAPABILITY_REGISTRY.json").write_text(
                json.dumps(registry, indent=2), encoding="utf-8"
            )
            self.assertEqual([], GATE.validate_repository(root))


if __name__ == "__main__":
    unittest.main()
