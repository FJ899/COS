import json
import tempfile
import unittest
from pathlib import Path

from projector.authority import classify_human_intervention
from projector.kernel import ProjectorKernel, TransitionRejected
from projector.model import Classification, HumanInterventionClass, RunStatus, TransitionProposal, TypedRecord
from projector.provenance import ProvenanceContext, digest_json
from projector.storage import IntegrityError, RunStore


class ProjectorContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.prov = ProvenanceContext(implementation_identity="test-implementation@abc123")
        self.store = RunStore(self.root)
        self.kernel = ProjectorKernel(self.store, self.prov)

    def start(self):
        return self.kernel.start_run(
            "Make a bounded local result from this rough intent",
            {
                "human_goal": "Produce the requested bounded local result",
                "run_done_definition": "A named output exists and its required property is observed",
                "verification_method": "Read the output and check the required property",
            },
        )

    def evidence(self, state, *, content="observed", kind="OBSERVATION", scope="current_state"):
        return self.store.capture_evidence(
            state.run_id,
            kind=kind,
            source="test_fixture",
            identifier="fixture",
            producer="UNIT_TEST",
            claim_scope=scope,
            content=content,
        )

    def transition(self, state, **kwargs):
        defaults = dict(
            prior_state_identity=digest_json(state.to_dict()),
            classification=Classification.ASSUMPTION,
            text="bounded assumption",
            proposed_next_route_or_gate={"type": "route", "route": {"name": "inspect", "premises": []}},
            rationale="test transition",
            actor="TEST_ACTOR",
        )
        defaults.update(kwargs)
        return self.kernel.apply_transition(state, TransitionProposal(**defaults))

    def test_rough_intent_creates_durable_bounded_state(self):
        state = self.start()
        recovered = ProjectorKernel(RunStore(self.root), self.prov).recover(state.run_id)
        self.assertEqual(recovered.raw_human_intent, "Make a bounded local result from this rough intent")
        self.assertEqual(recovered.human_goal, "Produce the requested bounded local result")
        self.assertEqual(recovered.status, RunStatus.ACTIVE)
        self.assertEqual(recovered.artifact_identity, "test-implementation@abc123")

    def test_missing_human_owned_semantics_blocks_instead_of_guessing(self):
        state = self.kernel.start_run("Do something useful with this rough intent")
        self.assertEqual(state.status, RunStatus.BLOCKED)
        self.assertEqual(state.critical_unknown_or_blocker.classification, Classification.UNKNOWN)
        self.assertEqual(state.next_move_or_gate["classification"], "GENUINE_HUMAN_OWNED_GATE")

    def test_goal_preserved_and_silent_substitution_rejected(self):
        state = self.start()
        next_state = self.transition(state)
        self.assertEqual(next_state.human_goal, state.human_goal)
        with self.assertRaises(TransitionRejected):
            self.transition(next_state, proposed_human_goal="Easier replacement goal")

    def test_records_keep_fact_assumption_claim_unknown_distinct(self):
        state = self.start()
        state = self.transition(state, classification=Classification.ASSUMPTION, text="A")
        state = self.transition(state, classification=Classification.CLAIM, text="C")
        state = self.transition(state, classification=Classification.UNKNOWN, text="U")
        self.assertEqual([x.text for x in state.assumptions], ["A"])
        self.assertEqual([x.text for x in state.claims], ["C"])
        self.assertEqual([x.text for x in state.unknowns], ["U"])
        self.assertEqual(state.observed_state, [])

    def test_observation_requires_evidence_and_evidence_tamper_fails_closed(self):
        state = self.start()
        with self.assertRaises(TransitionRejected):
            self.transition(state, classification=Classification.OBSERVED, text="unsupported")
        ref = self.evidence(state, content="checkpoint evidence")
        state = self.transition(state, classification=Classification.OBSERVED, text="observed", evidence_refs=(ref,))
        path = self.root / state.run_id / ref.path_or_identifier
        record = json.loads(path.read_text(encoding="utf-8"))
        record["content"] = "changed after capture"
        path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaises(IntegrityError):
            RunStore(self.root).load_run(state.run_id, verify=True)

    def test_route_invalidation_requires_reroute_or_truthful_block(self):
        state = self.start()
        state = self.transition(
            state,
            proposed_next_route_or_gate={"type": "route", "route": {"name": "route_a", "premises": ["A available"]}},
        )
        ref = self.evidence(state, content="A unavailable")
        with self.assertRaises(TransitionRejected):
            self.transition(
                state,
                classification=Classification.OBSERVED,
                text="A unavailable",
                evidence_refs=(ref,),
                route_invalidated=True,
                proposed_next_route_or_gate={"type": "route", "route": {"name": "route_a", "premises": []}},
            )
        rerouted = self.transition(
            state,
            classification=Classification.OBSERVED,
            text="A unavailable",
            evidence_refs=(ref,),
            route_invalidated=True,
            proposed_next_route_or_gate={"type": "route", "route": {"name": "fallback", "premises": []}},
        )
        self.assertEqual(rerouted.route["name"], "fallback")

    def test_failure_path_can_block_with_visible_unknown(self):
        state = self.start()
        ref = self.evidence(state, content="dependency unavailable")
        blocked = self.transition(
            state,
            classification=Classification.OBSERVED,
            text="dependency unavailable",
            evidence_refs=(ref,),
            route_invalidated=True,
            proposed_next_route_or_gate=None,
            critical_unknown_or_blocker=TypedRecord(Classification.UNKNOWN, "No evidenced fallback"),
            target_status=RunStatus.BLOCKED,
        )
        self.assertEqual(blocked.status, RunStatus.BLOCKED)
        self.assertEqual(blocked.critical_unknown_or_blocker.text, "No evidenced fallback")

    def test_human_gate_and_operational_rescue_are_distinct(self):
        gate = classify_human_intervention(
            authority_reason="consequential_effect",
            requested_decision="Approve consequential effect",
            response=None,
            material_effect="Work blocked pending authority",
        )
        rescue = classify_human_intervention(
            authority_reason="routine_recovery_instruction",
            requested_decision="Tell system next step",
            response="Use route B",
            material_effect="Changes routing",
        )
        self.assertEqual(gate.classification, HumanInterventionClass.GENUINE_HUMAN_OWNED_GATE)
        self.assertEqual(rescue.classification, HumanInterventionClass.HUMAN_OPERATIONAL_RESCUE)
        state = self.start()
        with self.assertRaises(TransitionRejected):
            self.transition(state, human_intervention=rescue, proposed_human_goal="Replacement goal")

    def test_cold_start_recovers_material_state_and_provenance_chain(self):
        state = self.start()
        ref = self.evidence(state, content="checkpoint")
        state = self.transition(
            state,
            classification=Classification.OBSERVED,
            text="checkpoint observed",
            evidence_refs=(ref,),
            critical_unknown_or_blocker=TypedRecord(Classification.UNKNOWN, "Need one more observation"),
            proposed_next_route_or_gate={"type": "route", "route": {"name": "next_check", "premises": []}},
        )
        recovered = ProjectorKernel(RunStore(self.root), self.prov).recover(state.run_id)
        self.assertEqual(recovered.route["name"], "next_check")
        self.assertEqual(recovered.critical_unknown_or_blocker.text, "Need one more observation")
        events = [json.loads(x) for x in (self.root / state.run_id / "events.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(events[-1]["task_contract_version"], "v1.0")
        self.assertEqual(events[-1]["architecture_contract_version"], "v1.0")
        self.assertEqual(events[-1]["implementation_identity"], "test-implementation@abc123")
        self.assertEqual(events[-1]["prior_state_digest"], events[-2]["result_state_digest"])

    def test_done_rejected_without_effect_evidence_and_allowed_with_verification(self):
        state = self.start()
        with self.assertRaises(TransitionRejected):
            self.transition(state, classification=Classification.CLAIM, text="done claim", target_status=RunStatus.DONE, proposed_next_route_or_gate=None)
        ref = self.evidence(state, content="effect observed", kind="VERIFICATION", scope="run_done_definition")
        done = self.transition(
            state,
            classification=Classification.OBSERVED,
            text="bound DONE observed",
            evidence_refs=(ref,),
            target_status=RunStatus.DONE,
            proposed_next_route_or_gate=None,
        )
        self.assertEqual(done.status, RunStatus.DONE)

    def test_stale_transition_and_unfrozen_implementation_identity_fail_closed(self):
        state = self.start()
        with self.assertRaises(TransitionRejected):
            self.kernel.apply_transition(
                state,
                TransitionProposal(
                    prior_state_identity="sha256:stale",
                    classification=Classification.ASSUMPTION,
                    text="stale",
                    proposed_next_route_or_gate=None,
                    rationale="stale proposal",
                    actor="TEST_ACTOR",
                ),
            )
        with self.assertRaises(ValueError):
            ProjectorKernel(RunStore(self.root / "other"), ProvenanceContext(implementation_identity="NOT YET FROZEN"))


if __name__ == "__main__":
    unittest.main()
