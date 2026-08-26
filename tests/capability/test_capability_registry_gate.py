from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "verify_capability_evidence.py"
SPEC = importlib.util.spec_from_file_location("capability_gate", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load capability gate")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class CapabilityEvidenceGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "governance").mkdir(parents=True)
        (self.root / ".github" / "workflows").mkdir(parents=True)
        (self.root / "scripts").mkdir(parents=True)
        (self.root / "tests").mkdir(parents=True)
        (self.root / "governance" / "BEHAVIOR_FIRST_CAPABILITY_POLICY.md").write_text("policy\n", encoding="utf-8")
        (self.root / "governance" / "P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md").write_text("contract\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_registry(self, capabilities: list[dict]) -> None:
        payload = {
            "schema_version": 1,
            "allowed_statuses": GATE.STATUSES,
            "capabilities": capabilities,
        }
        (self.root / "governance" / "CAPABILITY_REGISTRY.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    @staticmethod
    def base_entry(status: str = "PROPOSED") -> dict:
        return {
            "id": "CAP-TEST-001",
            "name": "test capability",
            "claim": "given input, produce verified output",
            "status": status,
            "implementation": [],
            "executable_evidence": [],
            "failure_evidence": [],
            "integration_evidence": [],
            "real_work_evidence": [],
            "reliability_evidence": [],
            "ci_commands": [],
            "integration_ci_commands": [],
            "notes": "fixture",
        }

    def write_tested_fixture(self, proof: str) -> dict:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        (self.root / "tests" / "proof.py").write_text(proof, encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/proof.py"]
        entry["failure_evidence"] = ["tests/proof.py"]
        entry["ci_commands"] = ["python tests/proof.py"]
        (self.root / ".github" / "workflows" / "verify.yml").write_text("python tests/proof.py\n", encoding="utf-8")
        self.write_registry([entry])
        return entry

    def test_proposed_requires_no_fake_implementation(self) -> None:
        self.write_registry([self.base_entry("PROPOSED")])
        errors = GATE.validate_repository(self.root)
        self.assertEqual([], errors)

    def test_tested_without_executable_and_failure_proof_fails(self) -> None:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        self.write_registry([entry])
        errors = GATE.validate_repository(self.root)
        joined = "\n".join(errors)
        self.assertIn("TESTED+ requires executable_evidence", joined)
        self.assertIn("TESTED+ requires failure_evidence", joined)
        self.assertIn("TESTED+ requires ci_commands", joined)

    def test_registered_python_pass_stub_fails(self) -> None:
        entry = self.base_entry("IMPLEMENTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    pass\n", encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        self.write_registry([entry])
        errors = GATE.validate_repository(self.root)
        self.assertTrue(any("obvious stub `pass`" in error for error in errors))

    def test_unregistered_formal_markdown_claim_fails(self) -> None:
        self.write_registry([self.base_entry("PROPOSED")])
        (self.root / "README.md").write_text("CAPABILITY CLAIM: CAP-NOT-REGISTERED\n", encoding="utf-8")
        errors = GATE.validate_repository(self.root)
        self.assertTrue(any("unregistered formal claim CAP-NOT-REGISTERED" in error for error in errors))

    def test_reliable_requires_two_real_work_records_and_reliability_evidence(self) -> None:
        entry = self.base_entry("RELIABLE")
        files = {
            "scripts/impl.py": "def run():\n    return 1\n",
            "tests/proof.py": "assert observed == expected\n",
            "tests/integration.py": "assert True\n",
            "evidence/run1.md": "run 1\n",
        }
        for relative, content in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/proof.py"]
        entry["failure_evidence"] = ["tests/proof.py"]
        entry["integration_evidence"] = ["tests/integration.py"]
        entry["real_work_evidence"] = ["evidence/run1.md"]
        entry["ci_commands"] = ["python tests/proof.py"]
        entry["integration_ci_commands"] = ["python tests/integration.py"]
        (self.root / ".github" / "workflows" / "verify.yml").write_text(
            "python tests/proof.py\npython tests/integration.py\n", encoding="utf-8"
        )
        self.write_registry([entry])
        errors = GATE.validate_repository(self.root)
        joined = "\n".join(errors)
        self.assertIn("RELIABLE requires at least two independent real_work_evidence paths", joined)
        self.assertIn("RELIABLE requires reliability_evidence", joined)

    def test_vacuous_tested_capability_fails(self) -> None:
        self.write_tested_fixture("assert True\n")
        errors = GATE.validate_repository(self.root)
        joined = "\n".join(errors)
        self.assertIn("executable_evidence evidence is behaviorally vacuous / unconditional-success", joined)
        self.assertIn("failure_evidence evidence is behaviorally vacuous / unconditional-success", joined)

    def test_bounded_unconditional_success_forms_fail(self) -> None:
        proofs = [
            "assert 1\n",
            "assert 1 == 1\n",
            "assert not False\n",
            "assert (1, 2)\n",
            "assert True or runtime_call()\n",
            "runtime_value = False\nassert runtime_value or True\n",
            "pass\n",
            "answer = 42\n",
        ]
        for proof in proofs:
            with self.subTest(proof=proof):
                exec(compile(proof, str(self.root / "tests" / "proof.py"), "exec"), {})
                self.write_tested_fixture(proof)
                errors = GATE.validate_repository(self.root)
                self.assertTrue(any("behaviorally vacuous / unconditional-success" in error for error in errors))

    def test_behavior_dependent_operation_before_constant_assert_is_not_vacuous(self) -> None:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text(
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
        positive = loader + "module.run(2)\nassert True\n"
        failure = (
            loader
            + "try:\n"
            "    module.run(-1)\n"
            "except ValueError as exc:\n"
            "    assert 'negative input' in str(exc)\n"
            "else:\n"
            "    raise AssertionError('expected ValueError')\n"
        )
        (self.root / "tests" / "positive.py").write_text(positive, encoding="utf-8")
        (self.root / "tests" / "failure.py").write_text(failure, encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/positive.py"]
        entry["failure_evidence"] = ["tests/failure.py"]
        entry["ci_commands"] = ["python tests/positive.py", "python tests/failure.py"]
        (self.root / ".github" / "workflows" / "verify.yml").write_text(
            "python tests/positive.py\npython tests/failure.py\n", encoding="utf-8"
        )
        self.write_registry([entry])

        exec(compile(positive, str(self.root / "tests" / "positive.py"), "exec"), {"__file__": str(self.root / "tests" / "positive.py")})
        exec(compile(failure, str(self.root / "tests" / "failure.py"), "exec"), {"__file__": str(self.root / "tests" / "failure.py")})
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_valid_tested_capability_uses_behavior_dependent_positive_and_failure_evidence(self) -> None:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text(
            "def run(value):\n"
            "    if value < 0:\n"
            "        raise ValueError('negative input')\n"
            "    return value * 2\n",
            encoding="utf-8",
        )
        proof = (
            "import importlib.util\n"
            "from pathlib import Path\n"
            "impl_path = Path(__file__).resolve().parents[1] / 'scripts' / 'impl.py'\n"
            "spec = importlib.util.spec_from_file_location('fixture_impl', impl_path)\n"
            "module = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(module)\n"
            "assert module.run(2) == 4\n"
            "try:\n"
            "    module.run(-1)\n"
            "except ValueError as exc:\n"
            "    assert 'negative input' in str(exc)\n"
            "else:\n"
            "    raise AssertionError('expected ValueError')\n"
        )
        (self.root / "tests" / "proof.py").write_text(proof, encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/proof.py"]
        entry["failure_evidence"] = ["tests/proof.py"]
        entry["ci_commands"] = ["python tests/proof.py"]
        (self.root / ".github" / "workflows" / "verify.yml").write_text("python tests/proof.py\n", encoding="utf-8")
        self.write_registry([entry])

        namespace = {"__file__": str(self.root / "tests" / "proof.py")}
        exec(compile(proof, str(self.root / "tests" / "proof.py"), "exec"), namespace)
        errors = GATE.validate_repository(self.root)
        self.assertEqual([], errors)

    def test_cli_contract_distinguishes_valid_and_vacuous_repositories(self) -> None:
        original_root = GATE.ROOT
        try:
            for proof in ["assert True\n", "pass\n"]:
                with self.subTest(proof=proof):
                    self.write_tested_fixture(proof)
                    GATE.ROOT = self.root
                    with contextlib.redirect_stderr(io.StringIO()) as stderr:
                        self.assertEqual(1, GATE.main())
                    self.assertIn("behaviorally vacuous / unconditional-success", stderr.getvalue())

            entry = self.base_entry("TESTED")
            (self.root / "scripts" / "impl.py").write_text(
                "def run(value):\n"
                "    if value < 0:\n"
                "        raise ValueError('negative input')\n"
                "    return value * 2\n",
                encoding="utf-8",
            )
            proof = (
                "import importlib.util\n"
                "from pathlib import Path\n"
                "impl_path = Path(__file__).resolve().parents[1] / 'scripts' / 'impl.py'\n"
                "spec = importlib.util.spec_from_file_location('fixture_impl', impl_path)\n"
                "module = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(module)\n"
                "assert module.run(2) == 4\n"
                "try:\n"
                "    module.run(-1)\n"
                "except ValueError as exc:\n"
                "    assert 'negative input' in str(exc)\n"
                "else:\n"
                "    raise AssertionError('expected ValueError')\n"
            )
            (self.root / "tests" / "proof.py").write_text(proof, encoding="utf-8")
            entry["implementation"] = ["scripts/impl.py"]
            entry["executable_evidence"] = ["tests/proof.py"]
            entry["failure_evidence"] = ["tests/proof.py"]
            entry["ci_commands"] = ["python tests/proof.py"]
            self.write_registry([entry])
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(0, GATE.main())
            self.assertIn("[PASS] capability evidence gate", stdout.getvalue())
        finally:
            GATE.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
