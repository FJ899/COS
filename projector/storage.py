from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from projector.model import EvidenceRef, RunState
from projector.provenance import ProvenanceContext, digest_bytes, digest_json


class IntegrityError(RuntimeError):
    pass


_RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _run_dir(self, run_id: str) -> Path:
        if not _RUN_ID_RE.fullmatch(run_id):
            raise ValueError("invalid run_id")
        path = (self.root / run_id).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError("run path escapes configured root")
        return path

    def _atomic_json_write(self, path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def _append_event(self, run_dir: Path, event: dict[str, Any]) -> None:
        events_path = run_dir / "events.jsonl"
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def create_run(
        self,
        state: RunState,
        provenance: ProvenanceContext,
        *,
        actor: str,
    ) -> RunState:
        provenance.validate()
        run_dir = self._run_dir(state.run_id)
        if run_dir.exists():
            raise FileExistsError(f"run already exists: {state.run_id}")
        (run_dir / "evidence").mkdir(parents=True)
        event_id = "evt-000001"
        persisted = replace(state, updated_at=utc_now(), last_event_id=event_id)
        result_digest = digest_json(persisted.to_dict())
        event = {
            "event_id": event_id,
            "run_id": state.run_id,
            "event_type": "RUN_STARTED",
            "actor": actor,
            "prior_state_digest": None,
            "result_state_digest": result_digest,
            "artifact_source_paths": [],
            "parent_event_evidence_refs": [],
            "recorded_at": persisted.updated_at,
            **provenance.to_event_fields(),
        }
        self._append_event(run_dir, event)
        self._atomic_json_write(run_dir / "run.json", persisted.to_dict())
        self._atomic_json_write(run_dir / "artifacts.json", {"run_id": state.run_id, "artifacts": []})
        return persisted

    def capture_evidence(
        self,
        run_id: str,
        *,
        kind: str,
        source: str,
        identifier: str,
        producer: str,
        claim_scope: str,
        content: str,
        observed_at: str | None = None,
    ) -> EvidenceRef:
        run_dir = self._run_dir(run_id)
        if not run_dir.exists():
            raise FileNotFoundError(f"unknown run: {run_id}")
        observed_at = observed_at or utc_now()
        raw = content.encode("utf-8")
        digest = digest_bytes(raw)
        record = {
            "kind": kind,
            "source": source,
            "identifier": identifier,
            "digest": digest,
            "observed_at": observed_at,
            "producer": producer,
            "claim_scope": claim_scope,
            "content": content,
        }
        evidence_id = digest_json(record).split(":", 1)[1][:16]
        relative = f"evidence/{evidence_id}.json"
        evidence_path = run_dir / relative
        if evidence_path.exists():
            existing = json.loads(evidence_path.read_text(encoding="utf-8"))
            if existing != record:
                raise IntegrityError("digest collision or evidence identity mismatch")
        else:
            self._atomic_json_write(evidence_path, record)
        return EvidenceRef(
            kind=kind,
            source=source,
            path_or_identifier=relative,
            digest_or_version=digest,
            observed_at=observed_at,
            producer=producer,
            claim_scope=claim_scope,
        )

    def verify_evidence_ref(self, run_id: str, ref: EvidenceRef) -> None:
        run_dir = self._run_dir(run_id)
        path = (run_dir / ref.path_or_identifier).resolve()
        if run_dir.resolve() not in path.parents:
            raise IntegrityError("evidence path escapes run directory")
        if not path.is_file():
            raise IntegrityError(f"missing evidence: {ref.path_or_identifier}")
        record = json.loads(path.read_text(encoding="utf-8"))
        actual_digest = digest_bytes(str(record.get("content", "")).encode("utf-8"))
        if actual_digest != ref.digest_or_version or record.get("digest") != ref.digest_or_version:
            raise IntegrityError(f"evidence digest mismatch: {ref.path_or_identifier}")
        if record.get("kind") != ref.kind or record.get("source") != ref.source:
            raise IntegrityError("evidence metadata mismatch")
        if record.get("observed_at") != ref.observed_at:
            raise IntegrityError("evidence timestamp mismatch")
        if record.get("producer") != ref.producer or record.get("claim_scope") != ref.claim_scope:
            raise IntegrityError("evidence provenance mismatch")

    def commit_transition(
        self,
        prior: RunState,
        result: RunState,
        provenance: ProvenanceContext,
        *,
        actor: str,
        event_payload: dict[str, Any],
    ) -> RunState:
        provenance.validate()
        current = self.load_run(prior.run_id, verify=True)
        current_digest = digest_json(current.to_dict())
        expected_prior = digest_json(prior.to_dict())
        if current_digest != expected_prior:
            raise IntegrityError("stored state changed since transition was proposed")
        run_dir = self._run_dir(prior.run_id)
        events = self._read_events(run_dir)
        event_id = f"evt-{len(events) + 1:06d}"
        persisted = replace(result, updated_at=utc_now(), last_event_id=event_id)
        result_digest = digest_json(persisted.to_dict())
        refs = [item.get("path_or_identifier") for item in event_payload.get("evidence_refs", [])]
        event = {
            "event_id": event_id,
            "run_id": prior.run_id,
            "event_type": "STATE_TRANSITION",
            "actor": actor,
            "prior_state_digest": current_digest,
            "result_state_digest": result_digest,
            "artifact_source_paths": [ref for ref in refs if ref],
            "parent_event_evidence_refs": [prior.last_event_id, *[ref for ref in refs if ref]],
            "recorded_at": persisted.updated_at,
            "transition": event_payload,
            **provenance.to_event_fields(),
        }
        self._append_event(run_dir, event)
        self._atomic_json_write(run_dir / "run.json", persisted.to_dict())
        return persisted

    def _read_events(self, run_dir: Path) -> list[dict[str, Any]]:
        path = run_dir / "events.jsonl"
        if not path.is_file():
            raise IntegrityError("missing events.jsonl")
        events: list[dict[str, Any]] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise IntegrityError(f"invalid event JSON at line {line_number}") from exc
        if not events:
            raise IntegrityError("event log is empty")
        return events

    def verify_integrity(self, run_id: str) -> None:
        run_dir = self._run_dir(run_id)
        if not run_dir.is_dir():
            raise FileNotFoundError(f"unknown run: {run_id}")
        state = RunState.from_dict(json.loads((run_dir / "run.json").read_text(encoding="utf-8")))
        events = self._read_events(run_dir)
        previous_result: str | None = None
        expected_index = 1
        for event in events:
            expected_id = f"evt-{expected_index:06d}"
            if event.get("event_id") != expected_id:
                raise IntegrityError("event sequence is not contiguous")
            if event.get("run_id") != run_id:
                raise IntegrityError("event run_id mismatch")
            if expected_index == 1:
                if event.get("prior_state_digest") is not None:
                    raise IntegrityError("initial event has unexpected parent state")
            elif event.get("prior_state_digest") != previous_result:
                raise IntegrityError("event state-digest chain is broken")
            previous_result = event.get("result_state_digest")
            expected_index += 1
        if state.last_event_id != events[-1].get("event_id"):
            raise IntegrityError("run state does not point to the final event")
        if digest_json(state.to_dict()) != events[-1].get("result_state_digest"):
            raise IntegrityError("run state digest does not match the final event")
        for ref in state.current_evidence_refs:
            self.verify_evidence_ref(run_id, ref)

    def load_run(self, run_id: str, *, verify: bool = True) -> RunState:
        run_dir = self._run_dir(run_id)
        path = run_dir / "run.json"
        if not path.is_file():
            raise FileNotFoundError(f"unknown run: {run_id}")
        state = RunState.from_dict(json.loads(path.read_text(encoding="utf-8")))
        if verify:
            self.verify_integrity(run_id)
        return state
