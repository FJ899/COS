from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("compare_ideas", Path(__file__).resolve().parents[2] / "scripts/compare_ideas.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IdeaComparisonTests(unittest.TestCase):
    def idea(self, identity, cost, benefit):
        return {"id": identity, "feasible": True, "feasibility_evidence": "supplied feasibility check",
                "metrics": {"cost": {"value": cost, "evidence": "quote"},
                            "benefit": {"value": benefit, "evidence": "trial"}}}

    def payload(self):
        return {"goal": "Choose a prototype", "criteria": {"cost": "minimize", "benefit": "maximize"},
                "ideas": [self.idea("A", 10, 5), self.idea("B", 20, 4)]}

    def test_dominated_alternative_is_explained(self):
        report = MODULE.compare(self.payload())
        self.assertEqual(["A"], report["frontier_among_evidenced"])
        self.assertEqual(["A"], report["results"][1]["dominated_by"])

    def test_tradeoff_and_tie_do_not_invent_winner(self):
        for cost, benefit in ((20, 8), (10, 5)):
            payload = self.payload()
            payload["ideas"][1] = self.idea("B", cost, benefit)
            self.assertEqual(["A", "B"], MODULE.compare(payload)["frontier_among_evidenced"])

    def test_missing_evidence_is_not_zero_score_or_rejection(self):
        payload = self.payload()
        payload["ideas"][1]["metrics"]["benefit"].pop("evidence")
        report = MODULE.compare(payload)
        self.assertEqual(["B"], report["unresolved"])
        self.assertEqual("NEEDS_EVIDENCE", report["results"][1]["status"])
        self.assertEqual([], report["results"][1]["dominated_by"])

    def test_feasibility_requires_evidence(self):
        for feasible, evidence, expected in ((False, "test", "INFEASIBLE"), (False, "", "NEEDS_EVIDENCE"),
                                              (None, "test", "NEEDS_EVIDENCE")):
            payload = self.payload()
            payload["ideas"][0].update(feasible=feasible, feasibility_evidence=evidence)
            self.assertEqual(expected, MODULE.compare(payload)["results"][0]["status"])

    def test_bad_input_is_rejected(self):
        for bad in (None, [], {}, {"goal": "x", "criteria": {}, "ideas": []}):
            with self.assertRaises(MODULE.ComparisonError):
                MODULE.compare(bad)
        for bad in (True, "5", float("nan"), float("inf")):
            payload = self.payload()
            payload["ideas"][0]["metrics"]["cost"]["value"] = bad
            with self.assertRaises(MODULE.ComparisonError):
                MODULE.compare(payload)

    def test_duplicate_ids_are_rejected(self):
        payload = self.payload()
        payload["ideas"][1]["id"] = "A"
        with self.assertRaises(MODULE.ComparisonError):
            MODULE.compare(payload)

    def test_input_order_does_not_change_shortlist(self):
        payload = self.payload()
        first = MODULE.compare(payload)
        payload["ideas"].reverse()
        self.assertEqual(first["frontier_among_evidenced"], MODULE.compare(payload)["frontier_among_evidenced"])


if __name__ == "__main__":
    unittest.main()
