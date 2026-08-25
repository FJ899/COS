from __future__ import annotations

import argparse
import json
from pathlib import Path

from projector.kernel import ProjectorKernel
from projector.model import Classification, RunStatus, TransitionProposal, TypedRecord
from projector.provenance import ProvenanceContext, digest_json
from projector.storage import RunStore


def _kernel(args: argparse.Namespace) -> ProjectorKernel:
    return ProjectorKernel(
        RunStore(args.root),
        ProvenanceContext(implementation_identity=args.implementation_identity),
    )


def command_start(args: argparse.Namespace) -> int:
    human_inputs = {
        key: value
        for key, value in {
            "human_goal": args.goal,
            "run_done_definition": args.done,
            "verification_method": args.verification,
        }.items()
        if value is not None
    }
    state = _kernel(args).start_run(args.intent, human_inputs)
    print(json.dumps(state.to_dict(), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    state = _kernel(args).recover(args.run_id)
    print(json.dumps(state.to_dict(), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_record(args: argparse.Namespace) -> int:
    kernel = _kernel(args)
    state = kernel.recover(args.run_id)
    refs = []
    if args.evidence_file:
        content = Path(args.evidence_file).read_text(encoding="utf-8")
        refs.append(
            kernel.store.capture_evidence(
                args.run_id,
                kind=args.evidence_kind,
                source=args.evidence_source,
                identifier=args.evidence_file,
                producer=args.actor,
                claim_scope=args.claim_scope,
                content=content,
            )
        )
    next_item = None
    if args.next_route:
        next_item = {"type": "route", "route": {"name": args.next_route, "premises": []}}
    blocker = None
    if args.blocker:
        blocker = TypedRecord(Classification.UNKNOWN, args.blocker)
    proposal = TransitionProposal(
        prior_state_identity=digest_json(state.to_dict()),
        classification=Classification(args.classification),
        text=args.text,
        proposed_next_route_or_gate=next_item,
        rationale=args.rationale,
        actor=args.actor,
        evidence_refs=tuple(refs),
        critical_unknown_or_blocker=blocker,
        route_invalidated=args.invalidate_route,
        target_status=RunStatus(args.status) if args.status else None,
        resolve_critical_unknown=args.resolve_blocker,
    )
    result = kernel.apply_transition(state, proposal)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    kernel = _kernel(args)
    state = kernel.recover(args.run_id)
    print(json.dumps({"run_id": state.run_id, "integrity": "OK", "last_event_id": state.last_event_id}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="projector")
    parser.add_argument("--root", default="projector_runs")
    parser.add_argument("--implementation-identity", required=True)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("--intent", required=True)
    start.add_argument("--goal")
    start.add_argument("--done")
    start.add_argument("--verification")
    start.set_defaults(func=command_start)

    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("--run-id", required=True)
    inspect_cmd.set_defaults(func=command_inspect)

    record = sub.add_parser("record")
    record.add_argument("--run-id", required=True)
    record.add_argument("--classification", choices=[item.value for item in Classification], required=True)
    record.add_argument("--text", required=True)
    record.add_argument("--rationale", required=True)
    record.add_argument("--actor", default="PROJECTOR_ACTOR")
    record.add_argument("--evidence-file")
    record.add_argument("--evidence-kind", default="OBSERVATION")
    record.add_argument("--evidence-source", default="local_file")
    record.add_argument("--claim-scope", default="current_state")
    record.add_argument("--next-route")
    record.add_argument("--invalidate-route", action="store_true")
    record.add_argument("--blocker")
    record.add_argument("--resolve-blocker", action="store_true")
    record.add_argument("--status", choices=[item.value for item in RunStatus])
    record.set_defaults(func=command_record)

    verify = sub.add_parser("verify")
    verify.add_argument("--run-id", required=True)
    verify.set_defaults(func=command_verify)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
