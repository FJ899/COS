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
        (self.root / "tests" / "capability").mkdir(parents=True)
        (self.root / "governance" / "BEHAVIOR_FIRST_CAPABILITY_POLICY.md").write_text("policy\n", encoding="utf-8")
        (self.root / "governance" / "P1_INTENT_TO_OUTCOME_RUN_CONTRACT.md").write_text("contract\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

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

    def write_registry(self, capabilities: list[dict]) -> None:
        payload = {"schema_version": 1, "allowed_statuses": GATE.STATUSES, "capabilities": capabilities}
        (self.root / "governance" / "CAPABILITY_REGISTRY.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    def write_workflow(self, commands: list[str]) -> None:
        (self.root / ".github" / "workflows" / "verify.yml").write_text("\n".join(commands) + "\n", encoding="utf-8")

    def write_direct_fixture(self, positive: str, failure: str | None = None) -> dict:
        if failure is None:
            failure = positive
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text(
            "def run(value=1):\n"
            "    if value < 0:\n"
            "        raise ValueError('negative input')\n"
            "    return value * 2\n",
            encoding="utf-8",
        )
        (self.root / "tests" / "positive.py").write_text(positive, encoding="utf-8")
        (self.root / "tests" / "failure.py").write_text(failure, encoding="utf-8")
        commands = ["python tests/positive.py", "python tests/failure.py"]
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/positive.py"]
        entry["failure_evidence"] = ["tests/failure.py"]
        entry["ci_commands"] = commands
        self.write_workflow(commands)
        self.write_registry([entry])
        return entry

    def write_unittest_fixture(self, positive: str, failure: str | None = None) -> dict:
        if failure is None:
            failure = positive
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text(
            "def run(value=1):\n"
            "    if value < 0:\n"
            "        raise ValueError('negative input')\n"
            "    return value * 2\n",
            encoding="utf-8",
        )
        (self.root / "tests" / "capability" / "test_positive.py").write_text(positive, encoding="utf-8")
        (self.root / "tests" / "capability" / "test_failure.py").write_text(failure, encoding="utf-8")
        command = "python -m unittest discover -s tests/capability -p 'test_*.py'"
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/capability/test_positive.py"]
        entry["failure_evidence"] = ["tests/capability/test_failure.py"]
        entry["ci_commands"] = [command]
        self.write_workflow([command])
        self.write_registry([entry])
        return entry

    @staticmethod
    def direct_loader() -> str:
        return (
            "import importlib.util\n"
            "from pathlib import Path\n"
            "impl_path = Path(__file__).resolve().parents[1] / 'scripts' / 'impl.py'\n"
            "spec = importlib.util.spec_from_file_location('fixture_impl', impl_path)\n"
            "module = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(module)\n"
        )

    def test_proposed_requires_no_fake_implementation(self) -> None:
        self.write_registry([self.base_entry("PROPOSED")])
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_tested_requires_evidence_and_ci(self) -> None:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        self.write_registry([entry])
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("TESTED+ requires executable_evidence", joined)
        self.assertIn("TESTED+ requires failure_evidence", joined)
        self.assertIn("TESTED+ requires ci_commands", joined)

    def test_registered_python_pass_stub_fails(self) -> None:
        entry = self.base_entry("IMPLEMENTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    pass\n", encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        self.write_registry([entry])
        self.assertTrue(any("obvious stub `pass`" in error for error in GATE.validate_repository(self.root)))


    def test_unregistered_formal_markdown_claim_fails(self) -> None:
        self.write_registry([self.base_entry("PROPOSED")])
        (self.root / "README.md").write_text("CAPABILITY CLAIM: CAP-NOT-REGISTERED\n", encoding="utf-8")
        self.assertTrue(any("unregistered formal claim CAP-NOT-REGISTERED" in error for error in GATE.validate_repository(self.root)))

    def test_reliable_requirements_remain_fail_closed(self) -> None:
        entry = self.base_entry("RELIABLE")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        positive = self.direct_loader() + "assert module.run(2) == 4\n"
        failure = self.direct_loader() + "try:\n    module.run(-1)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('expected ValueError')\n"
        (self.root / "tests" / "positive.py").write_text(positive, encoding="utf-8")
        (self.root / "tests" / "failure.py").write_text(failure, encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/positive.py"]
        entry["failure_evidence"] = ["tests/failure.py"]
        entry["ci_commands"] = ["python tests/positive.py", "python tests/failure.py"]
        entry["real_work_evidence"] = ["evidence/run1.md"]
        (self.root / "evidence").mkdir()
        (self.root / "evidence" / "run1.md").write_text("run\n", encoding="utf-8")
        self.write_workflow(entry["ci_commands"])
        self.write_registry([entry])
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("RELIABLE requires at least two independent real_work_evidence paths", joined)
        self.assertIn("RELIABLE requires reliability_evidence", joined)

    def test_role_separation_rejects_same_single_witness(self) -> None:
        proof = self.direct_loader() + "assert module.run(2) == 4\n"
        entry = self.write_direct_fixture(proof, proof)
        (self.root / "tests" / "failure.py").unlink()
        entry["failure_evidence"] = ["tests/positive.py"]
        entry["ci_commands"] = ["python tests/positive.py"]
        self.write_workflow(entry["ci_commands"])
        self.write_registry([entry])
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("role-distinct executable_evidence witness", joined)
        self.assertIn("role-distinct failure_evidence witness", joined)

    def test_assert_true_is_rejected(self) -> None:
        self.write_direct_fixture("assert True\n", "assert True\n")
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("behavior-insensitive / unconditional-success", joined)

    def test_import_only_is_not_behavioral_credit(self) -> None:
        proof = self.direct_loader() + "assert True\n"
        self.write_direct_fixture(proof, proof)
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("behavior-insensitive / unconditional-success", joined)

    def test_direct_definition_time_implementation_call_is_sensitive(self) -> None:
        positive = self.direct_loader() + "observed = module.run(2)\nassert observed == 4\n"
        failure = (
            self.direct_loader()
            + "try:\n"
            + "    module.run(-1)\n"
            + "except ValueError as exc:\n"
            + "    assert 'negative input' in str(exc)\n"
            + "else:\n"
            + "    raise AssertionError('expected ValueError')\n"
        )
        self.write_direct_fixture(positive, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_prior_constant_and_unreachable_direct_family_is_rejected(self) -> None:
        proofs = [
            "assert 1\n",
            "assert 1 == 1\n",
            "assert not False\n",
            "assert (1, 2)\n",
            "assert True or runtime_call()\n",
            "flag = False\nif flag:\n    runtime_call()\nassert True\n",
            "if False:\n    runtime_call()\nassert True\n",
            "def test_claim():\n    runtime_call()\nassert True\n",
        ]
        for proof in proofs:
            with self.subTest(proof=proof):
                self.write_direct_fixture(proof, proof)
                self.assertNotEqual([], GATE.validate_repository(self.root))

    def test_unittest_module_level_function_not_credited(self) -> None:
        proof = "def test_claim():\n    runtime_call()\n"
        self.write_unittest_fixture(proof, proof)
        self.assertNotEqual([], GATE.validate_repository(self.root))

    def test_unittest_non_testcase_method_not_credited(self) -> None:
        proof = "class Something:\n    def test_claim(self):\n        runtime_call()\n"
        self.write_unittest_fixture(proof, proof)
        self.assertNotEqual([], GATE.validate_repository(self.root))

    def test_unittest_skipped_method_not_credited(self) -> None:
        proof = (
            "import unittest\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    @unittest.skip('skip')\n"
            "    def test_claim(self):\n"
            "        runtime_call()\n"
        )
        self.write_unittest_fixture(proof, proof)
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("behavior-insensitive / unconditional-success", joined)

    def test_unittest_inherited_class_skip_not_credited(self) -> None:
        proof = (
            "import unittest\n"
            "@unittest.skip('skip base')\n"
            "class Base(unittest.TestCase):\n"
            "    pass\n"
            "class EvidenceTest(Base):\n"
            "    def test_claim(self):\n"
            "        runtime_call()\n"
        )
        self.write_unittest_fixture(proof, proof)
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("behavior-insensitive / unconditional-success", joined)

    def test_adversarial_unittest_load_tests_empty_suite_not_credited(self) -> None:
        proof = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        run(2)\n"
            "def load_tests(loader, tests, pattern):\n"
            "    return unittest.TestSuite()\n"
        )
        self.write_unittest_fixture(proof, proof)
        self.assertNotEqual([], GATE.validate_repository(self.root))

    def test_adversarial_unittest_setupclass_runtime_dependency_is_sensitive(self) -> None:
        positive = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    @classmethod\n"
            "    def setUpClass(cls):\n"
            "        cls.value = run(2)\n"
            "    def test_claim(self):\n"
            "        self.assertEqual(4, self.value)\n"
        )
        failure = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class FailureEvidence(unittest.TestCase):\n"
            "    def test_failure(self):\n"
            "        with self.assertRaises(ValueError):\n"
            "            run(-1)\n"
        )
        self.write_unittest_fixture(positive, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_unittest_inherited_setup_call_is_sensitive(self) -> None:
        proof = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class Base(unittest.TestCase):\n"
            "    def setUp(self):\n"
            "        run(2)\n"
            "class EvidenceTest(Base):\n"
            "    def test_claim(self):\n"
            "        self.assertTrue(True)\n"
        )
        failure = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class FailureEvidence(unittest.TestCase):\n"
            "    def test_failure(self):\n"
            "        with self.assertRaises(ValueError):\n"
            "            run(-1)\n"
        )
        self.write_unittest_fixture(proof, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_unittest_definition_time_call_is_sensitive(self) -> None:
        positive = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "TOKEN = run(2)\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        self.assertEqual(4, TOKEN)\n"
        )
        failure = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "try:\n"
            "    run(-1)\n"
            "except ValueError:\n"
            "    FAILURE_SEEN = True\n"
            "else:\n"
            "    FAILURE_SEEN = False\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        self.assertTrue(FAILURE_SEEN)\n"
        )
        self.write_unittest_fixture(positive, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_unittest_setup_runtime_dependency_is_sensitive(self) -> None:
        positive = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def setUp(self):\n"
            "        self.value = run(2)\n"
            "    def test_claim(self):\n"
            "        self.assertEqual(4, self.value)\n"
        )
        failure = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        with self.assertRaises(ValueError):\n"
            "            run(-1)\n"
        )
        self.write_unittest_fixture(positive, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_unittest_teardown_runtime_dependency_is_sensitive(self) -> None:
        positive = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        self.assertTrue(True)\n"
            "    def tearDown(self):\n"
            "        run(2)\n"
        )
        failure = (
            "import unittest\n"
            "from scripts.impl import run\n"
            "class EvidenceTest(unittest.TestCase):\n"
            "    def test_claim(self):\n"
            "        with self.assertRaises(ValueError):\n"
            "            run(-1)\n"
        )
        self.write_unittest_fixture(positive, failure)
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_allowlist_does_not_execute_arbitrary_registered_command(self) -> None:
        proof = self.direct_loader() + "assert module.run(2) == 4\n"
        entry = self.write_direct_fixture(proof, proof.replace("run(2)", "run(-1)").replace("assert module.run(-1) == 4", ""))
        entry["ci_commands"] = ["bash tests/positive.py", "bash tests/failure.py"]
        self.write_workflow(entry["ci_commands"])
        self.write_registry([entry])
        joined = "\n".join(GATE.validate_repository(self.root))
        self.assertIn("no allowlisted registered execution mode", joined)

    def test_cli_contract_distinguishes_valid_and_vacuous(self) -> None:
        original_root = GATE.ROOT
        try:
            self.write_direct_fixture("assert True\n", "assert True\n")
            GATE.ROOT = self.root
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(1, GATE.main())
            self.assertIn("behavior-insensitive / unconditional-success", stderr.getvalue())

            positive = self.direct_loader() + "assert module.run(2) == 4\n"
            failure = (
                self.direct_loader()
                + "try:\n"
                + "    module.run(-1)\n"
                + "except ValueError:\n"
                + "    pass\n"
                + "else:\n"
                + "    raise AssertionError('expected ValueError')\n"
            )
            self.write_direct_fixture(positive, failure)
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(0, GATE.main())
            self.assertIn("[PASS] capability evidence gate", stdout.getvalue())
        finally:
            GATE.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
