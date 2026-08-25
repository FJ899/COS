from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


SCHEMA_VERSION = "1.0"


class Classification(str, Enum):
    OBSERVED = "OBSERVED"
    ASSUMPTION = "ASSUMPTION"
    CLAIM = "CLAIM"
    UNKNOWN = "UNKNOWN"


class RunStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DONE = "DONE"


class HumanInterventionClass(str, Enum):
    GENUINE_HUMAN_OWNED_GATE = "GENUINE_HUMAN_OWNED_GATE"
    HUMAN_OPERATIONAL_RESCUE = "HUMAN_OPERATIONAL_RESCUE"


@dataclass(frozen=True)
class EvidenceRef:
    kind: str
    source: str
    path_or_identifier: str
    digest_or_version: str
    observed_at: str
    producer: str
    claim_scope: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EvidenceRef":
        return cls(**value)


@dataclass(frozen=True)
class TypedRecord:
    classification: Classification
    text: str
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification.value,
            "text": self.text,
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TypedRecord":
        return cls(
            classification=Classification(value["classification"]),
            text=value["text"],
            evidence_refs=tuple(value.get("evidence_refs", ())),
        )


@dataclass(frozen=True)
class HumanIntervention:
    classification: HumanInterventionClass
    authority_reason: str
    requested_decision: str
    response: str | None
    material_effect: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["classification"] = self.classification.value
        return data

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "HumanIntervention":
        return cls(
            classification=HumanInterventionClass(value["classification"]),
            authority_reason=value["authority_reason"],
            requested_decision=value["requested_decision"],
            response=value.get("response"),
            material_effect=value["material_effect"],
        )


@dataclass
class RunState:
    run_id: str
    raw_human_intent: str
    human_goal: str | None
    run_done_definition: str | None
    verification_method: str | None
    observed_state: list[TypedRecord] = field(default_factory=list)
    critical_unknown_or_blocker: TypedRecord | None = None
    current_evidence_refs: list[EvidenceRef] = field(default_factory=list)
    next_move_or_gate: dict[str, Any] | None = None
    route: dict[str, Any] | None = None
    status: RunStatus = RunStatus.ACTIVE
    artifact_identity: str = "NOT YET FROZEN"
    human_authority_gates: list[HumanIntervention] = field(default_factory=list)
    assumptions: list[TypedRecord] = field(default_factory=list)
    claims: list[TypedRecord] = field(default_factory=list)
    unknowns: list[TypedRecord] = field(default_factory=list)
    schema_version: str = SCHEMA_VERSION
    updated_at: str = ""
    last_event_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "schema_version": self.schema_version,
            "raw_human_intent": self.raw_human_intent,
            "human_goal": self.human_goal,
            "run_done_definition": self.run_done_definition,
            "verification_method": self.verification_method,
            "observed_state": [item.to_dict() for item in self.observed_state],
            "critical_unknown_or_blocker": (
                self.critical_unknown_or_blocker.to_dict()
                if self.critical_unknown_or_blocker
                else None
            ),
            "current_evidence_refs": [item.to_dict() for item in self.current_evidence_refs],
            "next_move_or_gate": self.next_move_or_gate,
            "route": self.route,
            "status": self.status.value,
            "artifact_identity": self.artifact_identity,
            "human_authority_gates": [item.to_dict() for item in self.human_authority_gates],
            "assumptions": [item.to_dict() for item in self.assumptions],
            "claims": [item.to_dict() for item in self.claims],
            "unknowns": [item.to_dict() for item in self.unknowns],
            "updated_at": self.updated_at,
            "last_event_id": self.last_event_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RunState":
        return cls(
            run_id=value["run_id"],
            schema_version=value.get("schema_version", SCHEMA_VERSION),
            raw_human_intent=value["raw_human_intent"],
            human_goal=value.get("human_goal"),
            run_done_definition=value.get("run_done_definition"),
            verification_method=value.get("verification_method"),
            observed_state=[TypedRecord.from_dict(item) for item in value.get("observed_state", [])],
            critical_unknown_or_blocker=(
                TypedRecord.from_dict(value["critical_unknown_or_blocker"])
                if value.get("critical_unknown_or_blocker")
                else None
            ),
            current_evidence_refs=[
                EvidenceRef.from_dict(item) for item in value.get("current_evidence_refs", [])
            ],
            next_move_or_gate=value.get("next_move_or_gate"),
            route=value.get("route"),
            status=RunStatus(value.get("status", RunStatus.ACTIVE.value)),
            artifact_identity=value.get("artifact_identity", "NOT YET FROZEN"),
            human_authority_gates=[
                HumanIntervention.from_dict(item)
                for item in value.get("human_authority_gates", [])
            ],
            assumptions=[TypedRecord.from_dict(item) for item in value.get("assumptions", [])],
            claims=[TypedRecord.from_dict(item) for item in value.get("claims", [])],
            unknowns=[TypedRecord.from_dict(item) for item in value.get("unknowns", [])],
            updated_at=value.get("updated_at", ""),
            last_event_id=value.get("last_event_id", ""),
        )


@dataclass(frozen=True)
class TransitionProposal:
    prior_state_identity: str
    classification: Classification
    text: str
    proposed_next_route_or_gate: dict[str, Any] | None
    rationale: str
    actor: str
    evidence_refs: tuple[EvidenceRef, ...] = ()
    critical_unknown_or_blocker: TypedRecord | None = None
    route_invalidated: bool = False
    target_status: RunStatus | None = None
    human_intervention: HumanIntervention | None = None
    proposed_human_goal: str | None = None
    proposed_done_definition: str | None = None
    resolve_critical_unknown: bool = False
