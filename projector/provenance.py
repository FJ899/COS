from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


TASK_CONTRACT_VERSION = "v1.0"
TASK_CONTRACT_IDENTITY = (
    "governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md"
    "@ef128a0885310524475fba1cd291d1f34400b0cc"
)
ARCHITECTURE_CONTRACT_VERSION = "v1.0"
ARCHITECTURE_CONTRACT_IDENTITY = (
    "governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md"
    "@4e05e026b3c9a4eafe5040537be45386b36ba426"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_json(value: Any) -> str:
    data = canonical_json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class ProvenanceContext:
    implementation_identity: str
    task_contract_version: str = TASK_CONTRACT_VERSION
    task_contract_identity: str = TASK_CONTRACT_IDENTITY
    architecture_contract_version: str = ARCHITECTURE_CONTRACT_VERSION
    architecture_contract_identity: str = ARCHITECTURE_CONTRACT_IDENTITY

    def validate(self) -> None:
        required = {
            "implementation_identity": self.implementation_identity,
            "task_contract_version": self.task_contract_version,
            "task_contract_identity": self.task_contract_identity,
            "architecture_contract_version": self.architecture_contract_version,
            "architecture_contract_identity": self.architecture_contract_identity,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError("missing provenance: " + ", ".join(missing))
        if self.implementation_identity in {"NOT YET IMPLEMENTED", "NOT YET FROZEN"}:
            raise ValueError("implementation identity must be exact before evidence-bearing work")

    def to_event_fields(self) -> dict[str, str]:
        self.validate()
        return {
            "task_contract_version": self.task_contract_version,
            "task_contract_identity": self.task_contract_identity,
            "architecture_contract_version": self.architecture_contract_version,
            "architecture_contract_identity": self.architecture_contract_identity,
            "implementation_identity": self.implementation_identity,
        }
