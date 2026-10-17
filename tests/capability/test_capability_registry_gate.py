from __future__ import annotations

import importlib.util
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

    def write_workflow(self, run: str, **step_fields: object) -> None:
        import yaml
        workflow = {"on": ["pull_request"], "jobs": {"test": {
            "runs-on": "ubuntu-latest", "steps": [{"run": run, **step_fields}]
        }}}
        (self.root / ".github/workflows/verify.yml").write_text(
            yaml.safe_dump(workflow), encoding="utf-8"
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
            "tests/proof.py": "assert True\n",
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
        self.write_workflow("python tests/proof.py\npython tests/integration.py")
        self.write_registry([entry])
        errors = GATE.validate_repository(self.root)
        joined = "\n".join(errors)
        self.assertIn("RELIABLE requires at least two independent real_work_evidence paths", joined)
        self.assertIn("RELIABLE requires reliability_evidence", joined)

    def test_valid_tested_capability_passes(self) -> None:
        entry = self.base_entry("TESTED")
        (self.root / "scripts" / "impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        (self.root / "tests" / "proof.py").write_text("assert True\n", encoding="utf-8")
        entry["implementation"] = ["scripts/impl.py"]
        entry["executable_evidence"] = ["tests/proof.py"]
        entry["failure_evidence"] = ["tests/proof.py"]
        entry["ci_commands"] = ["python tests/proof.py"]
        self.write_workflow("python tests/proof.py")
        self.write_registry([entry])
        errors = GATE.validate_repository(self.root)
        self.assertEqual([], errors)


    def make_tested_fixture(self) -> dict:
        entry = self.base_entry("TESTED")
        (self.root / "scripts/impl.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        (self.root / "tests/proof.py").write_text("assert True\n", encoding="utf-8")
        entry.update(implementation=["scripts/impl.py"], executable_evidence=["tests/proof.py"],
                     failure_evidence=["tests/proof.py"], ci_commands=["python tests/proof.py"])
        return entry

    def test_malformed_registry_shapes_report_errors(self) -> None:
        path = self.root / "governance/CAPABILITY_REGISTRY.json"
        for value in ([], None, 7, "registry"):
            with self.subTest(value=value):
                path.write_text(json.dumps(value), encoding="utf-8")
                self.assertIn("capability registry must be an object", GATE.validate_repository(self.root))
        for value in ([], {}, None, True):
            with self.subTest(status=value):
                entry = self.base_entry()
                entry["status"] = value
                self.write_registry([entry])
                self.assertTrue(any("invalid status" in error for error in GATE.validate_repository(self.root)))

    def test_whitespace_list_value_is_invalid(self) -> None:
        entry = self.base_entry()
        entry["implementation"] = [" "]
        self.write_registry([entry])
        self.assertTrue(any("non-empty strings" in error for error in GATE.validate_repository(self.root)))

    def test_outside_paths_and_symlinks_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "impl.py"
            external.write_text("def run():\n    return 1\n", encoding="utf-8")
            (self.root / "scripts/link.py").symlink_to(external)
            for value in (str(external), "../impl.py", "scripts/link.py"):
                with self.subTest(path=value):
                    entry = self.base_entry("IMPLEMENTED")
                    entry["implementation"] = [value]
                    self.write_registry([entry])
                    self.assertTrue(any("escapes repository" in error for error in GATE.validate_repository(self.root)))

    def test_ci_mentions_and_skipped_steps_do_not_prove_execution(self) -> None:
        entry = self.make_tested_fixture()
        self.write_registry([entry])
        cases = [
            ("# python tests/proof.py", {}),
            ("echo 'python tests/proof.py'", {}),
            ("python tests/proof.py", {"if": False}),
            ("python tests/proof.py", {"continue-on-error": True}),
            ("python tests/proof.py", {"working-directory": "elsewhere"}),
            ("python tests/proof.py", {"shell": "python"}),
            ("if false; then\npython tests/proof.py\nfi", {}),
            ("exit 0\npython tests/proof.py", {}),
            ("python tests/proof.py || true", {}),
            ("python tests/proof.py-extra", {}),
        ]
        for run, fields in cases:
            with self.subTest(run=run, fields=fields):
                self.write_workflow(run, **fields)
                self.assertTrue(any("CI does not execute" in error for error in GATE.validate_repository(self.root)))

    def test_ci_quoted_equivalent_command_passes(self) -> None:
        self.write_registry([self.make_tested_fixture()])
        self.write_workflow('python "tests/proof.py" # proof')
        self.assertEqual([], GATE.validate_repository(self.root))

    def test_invalid_yaml_reports_error(self) -> None:
        self.write_registry([self.base_entry()])
        (self.root / ".github/workflows/verify.yml").write_text("jobs: [", encoding="utf-8")
        self.assertTrue(any("cannot inspect workflow" in error for error in GATE.validate_repository(self.root)))

    def test_reliability_paths_are_canonicalized(self) -> None:
        entry = self.make_tested_fixture()
        entry.update(status="RELIABLE", integration_evidence=["tests/proof.py"],
                     integration_ci_commands=["python tests/proof.py"],
                     real_work_evidence=["tests/proof.py", "tests/./proof.py"],
                     reliability_evidence=["tests/proof.py"])
        self.write_registry([entry])
        self.write_workflow("python tests/proof.py")
        self.assertTrue(any("two independent" in error for error in GATE.validate_repository(self.root)))

    def test_duplicate_json_keys_are_rejected(self) -> None:
        (self.root / "governance/CAPABILITY_REGISTRY.json").write_text(
            '{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
        self.assertTrue(any("duplicate JSON key" in error for error in GATE.validate_repository(self.root)))

    def test_job_controls_and_inherited_directory_do_not_count_as_root_execution(self) -> None:
        import yaml
        self.write_registry([self.make_tested_fixture()])
        for kind in ("if", "continue-on-error", "defaults", "trigger"):
            self.write_workflow("python tests/proof.py")
            path = self.root / ".github/workflows/verify.yml"
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            job = workflow["jobs"]["test"]
            if kind == "if":
                job["if"] = False
            elif kind == "continue-on-error":
                job["continue-on-error"] = True
            elif kind == "defaults":
                workflow["defaults"] = {"run": {"working-directory": "other"}}
                job["defaults"] = {"run": {"shell": "bash"}}
            else:
                workflow["on"] = ["workflow_dispatch"]
            path.write_text(yaml.safe_dump(workflow), encoding="utf-8")
            with self.subTest(kind=kind):
                self.assertTrue(any("CI does not execute" in error for error in GATE.validate_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
