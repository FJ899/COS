import contextlib
import importlib.util
import io
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("cos_continuity", Path(__file__).resolve().parents[2] / "scripts/verify_creative_os.py")
COS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COS)


class ProjectTableTests(unittest.TestCase):
    def test_duplicate_projects_cannot_silently_replace_previous_state(self):
        table = "| Projekt | Status | A | B | C | D |\n|---|---|---|---|---|---|\n| X | ACTIVE | a | b | c | d |\n| X | CLOSED | a | b | c | d |\n"
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            COS.parse_rows(table)

    def test_valid_table_preserves_state(self):
        table = "| Projekt | Status | A | B | C | D |\n|---|---|---|---|---|---|\n| X | ACTIVE | a | b | c | d |\n"
        self.assertEqual("ACTIVE", COS.parse_rows(table)["X"][1])
