---
document: PROJECTOR_PRIVATE_ANALYSIS_OPERATIONAL_PROFILE
version: 1.0
status: HUMAN_AUTHORIZED_FOR_PRIVATE_USE_AND_REPOSITORY_INTEGRATION
owner: USER
authorized_at: 2026-10-17
repository: FJ899/COS
profile: PRIVATE_SINGLE_USER_ANALYSIS_ONLY
public_effects_enabled: false
capability_registry_changed: false
release_authorized: false
deploy_authorized: false
tag_authorized: false
---

# Projector — private analysis operational profile

## Human purpose

Projector is used privately by one Human to preserve and analyze conversations
with AI, retain goals and decisions, expose unresolved questions, and prevent a
task from being marked `DONE` without explicit evidence criteria.

The Human authorized closing and integrating the project at this real usage
level. This decision supersedes the earlier merge prohibition only for the
bounded integration sequence needed to place the private-analysis
implementation on canonical `main`.

## Accepted operational scope

- durable append-only run and state recording;
- strict parsing and hash-chain verification;
- recovery of historical runs, including schema 2.0;
- schema 2.1 `done_criteria` and exact evidence-to-criterion binding;
- visible assumptions, claims, unknowns, route changes and Human decisions;
- local, private, single-user analysis.

## Explicitly excluded scope

- autonomous GitHub writes or any other public effect;
- production use of caller-provided write sinks;
- multi-user or cross-machine authority replay protection;
- release, deploy, tag or automatic merge;
- a claim that arbitrary chat import is already implemented;
- promotion of `CAP-ITO-001` beyond evidence recorded in the capability
  registry.

The pinned authority policy enforces this boundary with
`public_effects_enabled: false`. Public-effect preparation and execution must
fail closed before a target write.

## Integration authority

The authorized repository operation is limited to:

1. integrate the reviewed hardening branch represented by PR #52 into the
   Projector implementation branch;
2. integrate the resulting Projector implementation represented by PR #47
   into canonical `main`;
3. preserve both PR histories and their CI evidence.

No release, deployment, tag or autonomous effect is authorized by this record.

## Verification floor

Integration is allowed only when:

- Projector tests pass, including the disabled-public-effect failure path;
- capability tests pass;
- the bundled schema 2.0 history remains valid;
- repository validators pass;
- the final candidate merges cleanly with current `main`;
- GitHub CI succeeds on the exact candidate head.

## Reopen conditions

This profile must be reopened and independently re-audited before any of the
following becomes required:

- public or autonomous writes;
- use by more than one authority or from multiple machines;
- a production GitHub sink;
- independent remote readback after writes;
- reliability or general-purpose capability promotion.

ScanChat import and knowledge extraction are a separate next project. Their
data completeness, fidelity, idempotency and confidentiality must be proven
before they are treated as reliable Projector input.
