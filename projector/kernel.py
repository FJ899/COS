from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

from projector.authority import require_genuine_gate
from projector.model import (
    Classification,
    HumanInterventionClass,
    RunState,
    RunStatus,
    TransitionProposal,
    TypedRecord,
)
from projector.provenance import ProvenanceContext, digest_json
from projector.storage import RunStore


class TransitionRejected(ValueError):
    pass


class ProjectorKernel:
    def __init__(self, store: RunStore, provenance: ProvenanceContext):
        provenance.validate()
        self.store = store
        self.provenance = provenance

    def start_run(
        self,
        raw_intent: str,
        human_inputs: dict[str, str] | None = None,
        *,
        actor: str = "PROJECTOR_ENTRYPOINT",
    ) -> RunState:
        raw_intent = raw_intent.strip()
        if not raw_intent:
            raise ValueError("raw Human intent must not be empty")
        inputs = human_inputs or {}
        allowed = {"human_goal", "run_done_definition", "verification_method"}
        unexpected = sorted(set(inputs) - allowed)
        if unexpected:
            raise ValueError("start_run accepts only Human-owned semantic fields: " + ", ".join(unexpected))

        goal = inputs.get("human_goal")
        done = inputs.get("run_done_definition")
        verification = inputs.get("verification_method")
        missing: list[str] = []
        if not goal:
            missing.append("Human-owned goal")
        if not done:
            missing.append("effect-based DONE definition")
        if not verification:
            missing.append("observable verification method")

        critical = None
        next_move: dict[str, Any] | None
        status = RunStatus.ACTIVE
        unknowns: list[TypedRecord] = []
        if missing:
            text = "Missing Human-owned semantic input: " + ", ".join(missing)
            critical = TypedRecord(Classification.UNKNOWN, text)
            unknowns = [critical]
            next_move = {
                "type": "human_gate",
                "classification": HumanInterventionClass.GENUINE_HUMAN_OWNED_GATE.value,
                "authority_reason": "goal_or_normative_meaning",
                "requested_decision": text,
            }
            status = RunStatus.BLOCKED
        else:
            next_move = {
                "type": "route",
                "route": {"name": "evidence_seeking", "premises": []},
                "reason": "bounded target is available; select the next justified move from current evidence",
            }

        state = RunState(
            run_id="run-" + uuid4().hex[:12],
            raw_human_intent=raw_intent,
            human_goal=goal,
            run_done_definition=done,
            verification_method=verification,
            critical_unknown_or_blocker=critical,
            next_move_or_gate=next_move,
            route={"name": "intent_binding", "premises": []},
            status=status,
            artifact_identity=self.provenance.implementation_identity,
            unknowns=unknowns,
        )
        return self.store.create_run(state, self.provenance, actor=actor)

    def recover(self, run_id: str) -> RunState:
        return self.store.load_run(run_id, verify=True)

    def apply_transition(self, prior: RunState, proposal: TransitionProposal) -> RunState:
        current_identity = digest_json(prior.to_dict())
        if proposal.prior_state_identity != current_identity:
            raise TransitionRejected("proposal does not target the exact current state")
        if proposal.classification is Classification.OBSERVED and not proposal.evidence_refs:
            raise TransitionRejected("OBSERVED records require evidence references")
        for ref in proposal.evidence_refs:
            try:
                self.store.verify_evidence_ref(prior.run_id, ref)
            except Exception as exc:
                raise TransitionRejected(str(exc)) from exc

        result = deepcopy(prior)
        if proposal.proposed_human_goal is not None and proposal.proposed_human_goal != prior.human_goal:
            if proposal.human_intervention is None:
                raise TransitionRejected("Human goal cannot change without an explicit Human-owned event")
            try:
                require_genuine_gate(proposal.human_intervention, "goal_or_normative_meaning")
            except ValueError as exc:
                raise TransitionRejected(str(exc)) from exc
            result.human_goal = proposal.proposed_human_goal
        if (
            proposal.proposed_done_definition is not None
            and proposal.proposed_done_definition != prior.run_done_definition
        ):
            if proposal.human_intervention is None:
                raise TransitionRejected("DONE cannot change without an explicit Human-owned event")
            try:
                require_genuine_gate(proposal.human_intervention, "goal_or_normative_meaning")
            except ValueError as exc:
                raise TransitionRejected(str(exc)) from exc
            result.run_done_definition = proposal.proposed_done_definition

        if proposal.human_intervention is not None:
            result.human_authority_gates.append(proposal.human_intervention)

        evidence_ids = tuple(ref.path_or_identifier for ref in proposal.evidence_refs)
        record = TypedRecord(proposal.classification, proposal.text, evidence_ids)
        if proposal.classification is Classification.OBSERVED:
            result.observed_state.append(record)
        elif proposal.classification is Classification.ASSUMPTION:
            result.assumptions.append(record)
        elif proposal.classification is Classification.CLAIM:
            result.claims.append(record)
        else:
            result.unknowns.append(record)

        known_refs = {ref.path_or_identifier for ref in result.current_evidence_refs}
        for ref in proposal.evidence_refs:
            if ref.path_or_identifier not in known_refs:
                result.current_evidence_refs.append(ref)
                known_refs.add(ref.path_or_identifier)

        if proposal.resolve_critical_unknown:
            if not proposal.evidence_refs:
                raise TransitionRejected("critical unknown cannot be resolved without evidence")
            result.critical_unknown_or_blocker = None
        if proposal.critical_unknown_or_blocker is not None:
            result.critical_unknown_or_blocker = proposal.critical_unknown_or_blocker

        next_item = proposal.proposed_next_route_or_gate
        if proposal.route_invalidated:
            if next_item and next_item.get("type") == "route":
                new_route = next_item.get("route") or {}
                if new_route.get("name") == (prior.route or {}).get("name"):
                    raise TransitionRejected("invalidated route cannot silently remain current")
                result.route = deepcopy(new_route)
            else:
                if proposal.target_status is not RunStatus.BLOCKED:
                    raise TransitionRejected("invalidated route requires REROUTE or truthful BLOCKED")
                if result.critical_unknown_or_blocker is None:
                    raise TransitionRejected("BLOCKED reroute outcome requires a visible blocker")
        elif next_item and next_item.get("type") == "route":
            result.route = deepcopy(next_item.get("route") or {})

        result.next_move_or_gate = deepcopy(next_item)
        if proposal.target_status is not None:
            result.status = proposal.target_status

        if result.status is RunStatus.DONE:
            if result.critical_unknown_or_blocker is not None:
                raise TransitionRejected("DONE is forbidden while a critical unknown/blocker remains")
            verification_refs = [
                ref
                for ref in proposal.evidence_refs
                if ref.kind == "VERIFICATION" and ref.claim_scope == "run_done_definition"
            ]
            if not verification_refs:
                raise TransitionRejected("DONE requires run-specific verification evidence")
            if not result.run_done_definition or not result.verification_method:
                raise TransitionRejected("DONE requires a bound DONE definition and verification method")

        payload = {
            "classification": proposal.classification.value,
            "text": proposal.text,
            "proposed_next_route_or_gate": proposal.proposed_next_route_or_gate,
            "rationale": proposal.rationale,
            "evidence_refs": [ref.to_dict() for ref in proposal.evidence_refs],
            "critical_unknown_or_blocker": (
                proposal.critical_unknown_or_blocker.to_dict()
                if proposal.critical_unknown_or_blocker
                else None
            ),
            "route_invalidated": proposal.route_invalidated,
            "target_status": proposal.target_status.value if proposal.target_status else None,
            "human_intervention": (
                proposal.human_intervention.to_dict() if proposal.human_intervention else None
            ),
            "goal_changed": result.human_goal != prior.human_goal,
            "done_definition_changed": result.run_done_definition != prior.run_done_definition,
            "resolve_critical_unknown": proposal.resolve_critical_unknown,
        }
        return self.store.commit_transition(
            prior,
            result,
            self.provenance,
            actor=proposal.actor,
            event_payload=payload,
        )
