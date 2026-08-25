from __future__ import annotations

from projector.model import HumanIntervention, HumanInterventionClass


GENUINE_AUTHORITY_REASONS = {
    "goal_or_normative_meaning",
    "final_acceptance",
    "consequential_effect",
    "unresolved_human_preference",
}


def classify_human_intervention(
    *,
    authority_reason: str,
    requested_decision: str,
    response: str | None,
    material_effect: str,
) -> HumanIntervention:
    classification = (
        HumanInterventionClass.GENUINE_HUMAN_OWNED_GATE
        if authority_reason in GENUINE_AUTHORITY_REASONS
        else HumanInterventionClass.HUMAN_OPERATIONAL_RESCUE
    )
    return HumanIntervention(
        classification=classification,
        authority_reason=authority_reason,
        requested_decision=requested_decision,
        response=response,
        material_effect=material_effect,
    )


def require_genuine_gate(intervention: HumanIntervention, reason: str) -> None:
    if intervention.classification is not HumanInterventionClass.GENUINE_HUMAN_OWNED_GATE:
        raise ValueError("human operational rescue cannot authorize a Human-owned change")
    if intervention.authority_reason != reason:
        raise ValueError(f"Human-owned change requires authority reason {reason}")
    if not intervention.response:
        raise ValueError("Human-owned change requires an explicit Human response")
