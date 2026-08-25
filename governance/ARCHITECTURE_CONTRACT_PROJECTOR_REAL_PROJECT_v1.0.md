# ARCHITECTURE CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT

VERSION: v1.0
STATUS: READY FOR P3 IMPLEMENTATION
BASED ON TASK CONTRACT: `governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md` @ `ef128a0885310524475fba1cd291d1f34400b0cc`
SOURCE / REPO IDENTITY:

```text
REPOSITORY: FJ899/COS
P1 SPECIFICATION BRANCH: spec/projector-real-project-v1
P1 FROZEN HEAD: ef128a0885310524475fba1cd291d1f34400b0cc
SOURCE TECHNICAL BASELINE: main@bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19
P2 ARCHITECTURE BRANCH: arch/projector-real-project-v1
P2 BASE SHA: ef128a0885310524475fba1cd291d1f34400b0cc
IMPLEMENTATION REPOSITORY: FJ899/COS
P3 IMPLEMENTATION BASE: arch/projector-real-project-v1 @ exact SHA containing this contract
P3 IMPLEMENTATION BRANCH: impl/projector-real-project-v1
```

## PROVENANCE GATE

```text
REQUIREMENT OWNER: P1 SPECIFICATION under Human-owned intent
TASK CONTRACT VERSION: v1.0
TASK CONTRACT IDENTITY: governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md @ ef128a0885310524475fba1cd291d1f34400b0cc
ARCHITECTURE DECISION OWNER: P2 ARCHITECTURE
ARCHITECTURE CONTRACT VERSION: v1.0
IMPLEMENTATION OWNER: P3 IMPLEMENTATION
IMPLEMENTATION IDENTITY: NOT YET IMPLEMENTED
EVIDENCE PACKAGE: NOT YET CREATED
INDEPENDENT VERIFIER: P4 INDEPENDENT AUDIT
P4 AUDIT: NOT YET AUDITED
HUMAN FINAL ACCEPTANCE: NOT YET CREATED
```

No completed stage may advance with ambiguous identity. Missing provenance for a stage that should already be complete is a STOP condition.

---

# CURRENT STATE

Reconnaissance against `main@bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19` establishes:

- `CAP-ITO-001` is `PROPOSED` with no registered implementation or evidence.
- no Projector runtime or end-to-end product implementation exists.
- COS already contains durable governance artifacts and a tested capability-evidence promotion guard `CAP-GATE-001`.
- CI uses Python 3.11, `unittest`, and `.github/workflows/verify-creative-os.yml`.
- existing continuity and lineage artifacts demonstrate the repository pattern of durable state, exact source binding, cold-start recovery, and fail-closed verification.
- the standalone HOT runtime is parked and is not implementation authority.

Existing useful components are therefore governance/evidence infrastructure only. They do not satisfy the Projector product behavior themselves.

## KNOWN FAILURE MODES IN CURRENT STATE

- architecture or documentation being mistaken for capability;
- hidden Human operational routing being mistaken for autonomous progress;
- loss of durable state across chat/session boundaries;
- unsupported capability promotion;
- continuing an obsolete route after contradictory evidence;
- fabricated or hardcoded success;
- provenance loss between P1/P2/P3/P4.

---

# ARCHITECTURE GOAL

Implement the smallest working vertical slice that can take one rough Human intent into a durable, bounded run; maintain evidence-separated state; select and record the next justified move or Human gate; re-route truthfully when evidence invalidates the current route; recover from durable artifacts; and produce an auditable evidence package for a real effect-based workload.

The architecture deliberately does not create a new autonomous platform, scheduler, master router, multi-agent runtime, HOT runtime, persistence service, database, or framework.

The core design is:

```text
Human rough intent
    ↓
Projector Run Kernel
    ↓
Durable Run State + Evidence Ledger
    ↓
Intelligence-selected next move
    ↓
Tool / local execution / research / Human gate
    ↓
Observation / evidence
    ↓
Projector Run Kernel validates transition
    ↓
Updated durable state or truthful BLOCKED state
```

The intelligence that proposes the next move may be the current capable AI actor. Projector's product mechanism is the deterministic state/control contract around that intelligence: preserving intent, evidence classification, authority boundaries, transition validation, provenance, and recoverability.

---

# REQUIREMENT → DECISION MAP

| Requirement | Architecture decisions |
|---|---|
| R-001 | AD-001, AD-002, AD-008 |
| R-002 | AD-002, AD-003 |
| R-003 | AD-003, AD-004 |
| R-004 | AD-003, AD-004 |
| R-005 | AD-004, AD-005 |
| R-006 | AD-005, AD-006 |
| R-007 | AD-008, AD-010 |
| R-008 | AD-004, AD-009 |
| R-009 | AD-011 |
| R-010 | AD-003, AD-007 |
| R-011 | AD-007, AD-010 |
| R-012 | AD-010 |
| R-013 | AD-006, AD-010 |

---

# AD-001 — SAME-REPOSITORY VERTICAL SLICE

Requirement: R-001, C-005, C-006

Decision:
Implement Projector inside `FJ899/COS` as a small first-use product slice rather than creating a new repository or service.

Mechanism:
Add one local product package plus tests/evidence under the existing repository and reuse existing CI/governance only where requirements require it.

Recommended topology:

```text
projector/
  __init__.py
  model.py
  kernel.py
  storage.py
  authority.py
  provenance.py
  cli.py

tests/projector/
  test_run_kernel.py
  test_recovery.py
  test_reroute.py
  test_authority.py
  test_failure_paths.py

projector_runs/
  <run-id>/
    run.json
    events.jsonl
    evidence/
    artifacts.json
```

Why:
The baseline already provides a Python test/CI environment and durable governance repository. A separate service/repository would add deployment, synchronization, identity, and evidence complexity without a requirement-driven need.

Alternatives:
- separate Projector repository;
- service/database architecture;
- multi-agent runtime.

Rejected:
All add capabilities and operational surfaces not required for the first bounded proof.

Trade-offs:
Tighter coupling to COS repository conventions; acceptable for the first vertical slice.

Risks:
Repository may later become too broad for repeated product use. That is future evidence, not current justification for abstraction.

Evidence expected:
Executable end-to-end test uses the actual package and durable run artifacts, not documentation-only proof.

---

# AD-002 — ONE EXPLICIT RUN ENTRYPOINT

Requirement: R-001, R-002

Decision:
Provide one product entrypoint that accepts rough Human intent without requiring architecture/tool selection.

Mechanism:
A CLI or equivalent callable entrypoint accepts raw text plus only genuinely Human-owned fields when necessary. It creates a run and returns/binds a durable bounded target state.

Interface shape:

```text
projector start --intent <raw text>
```

or an equivalent Python function:

```text
start_run(raw_intent: str, human_inputs: dict | None = None) -> RunState
```

The entrypoint must not ask the Human to select implementation language, repository topology, router, workflow engine, or ecosystem component.

Why:
Directly satisfies rough-intent operation while preventing implementation choices from leaking into Human input.

Alternatives:
Form-driven architecture configuration; multi-step setup wizard.

Rejected:
They externalize operational decomposition to the Human.

Trade-offs:
The first implementation may support only a bounded local execution environment; this is acceptable if the tested workload fits it.

Risks:
A weak intent binder could merely restate the prompt. Tests must verify a concrete bounded target and DONE binding.

Evidence expected:
Raw Human intent and resulting durable bounded target/state in the accepted run.

---

# AD-003 — DURABLE RUN STATE AS CANONICAL PRODUCT STATE

Requirement: R-003, R-004, R-010

Decision:
Each run has a versioned durable canonical state document separate from chat history.

Mechanism:
`run.json` is the current state projection. `events.jsonl` is append-only transition history. The canonical state schema must contain at minimum:

```text
run_id
schema_version
raw_human_intent
human_goal
run_done_definition
verification_method
observed_state
critical_unknown_or_blocker
current_evidence_refs
next_move_or_gate
route
status
artifact_identity
human_authority_gates
assumptions
updated_at
last_event_id
```

Facts, assumptions, claims, and unknowns must be distinguishable by typed records, not prose convention only.

Why:
This makes the current run recoverable without relying on one chat session and supports exact traceability of goal and state.

Alternatives:
Chat transcript as state; Markdown-only freeform journal; external database.

Rejected:
Chat-only state violates R-010. Freeform-only state weakens deterministic checks. Database is unnecessary for one repository-backed vertical slice.

Trade-offs:
JSON schema is less human-friendly than pure Markdown; optional rendered summaries may be added without becoming authoritative state.

Risks:
State schema may be overdesigned. Keep only fields needed by acceptance criteria.

Evidence expected:
Cold-start recovery test reconstructs AC-003 fields from durable run artifacts only.

---

# AD-004 — FAIL-CLOSED TRANSITION KERNEL

Requirement: R-003, R-004, R-005, R-008

Decision:
All material run state transitions pass through a deterministic transition kernel that rejects invalid or unjustified transitions.

Mechanism:
A transition proposal contains:

```text
prior_state_identity
proposed_observation_or_evidence
classification: OBSERVED | ASSUMPTION | CLAIM | UNKNOWN
proposed_next_route_or_gate
rationale
source/evidence refs
actor
```

The kernel must enforce:

- Human goal/DONE cannot change without explicit Human-owned goal-change event;
- observations cannot be recorded without evidence/source metadata where evidence is applicable;
- an invalidated route cannot remain current unless explicitly justified by new evidence;
- unresolved critical unknown remains visible until resolved or superseded by evidence;
- success/DONE requires verification evidence, not a success claim;
- missing required provenance produces BLOCKED/UNKNOWN, never PASS.

Why:
The intelligence selecting a move may be probabilistic; the invariants protecting intent and evidence must be deterministic and auditable.

Alternatives:
Prompt-only instructions; fixed workflow graph.

Rejected:
Prompt-only enforcement is not independently verifiable. Fixed pipeline violates R-005/C-006.

Trade-offs:
The kernel validates transitions but does not itself solve arbitrary tasks. Intelligence remains responsible for choosing useful moves.

Risks:
Overly strict validation could block legitimate work. Rules must be limited to frozen invariants, not arbitrary workflow preferences.

Evidence expected:
Tests for silent goal substitution, evidence classification, route invalidation, truthful blocking, and fabricated DONE rejection.

---

# AD-005 — ADAPTIVE ROUTE AS STATE, NOT FIXED PIPELINE

Requirement: R-005, R-006

Decision:
Represent the current route as data in run state rather than as a predetermined component pipeline.

Mechanism:
The acting Intelligence proposes the next evidence-seeking or productive move based on current durable state. A move may invoke only what the current task needs: repository inspection, code execution, web research, artifact creation, or a Human gate.

When new material evidence contradicts a route premise, the next transition must either:

```text
REROUTE -> new justified move
or
BLOCK -> truthful blocker
```

It may not silently continue the invalidated route.

Why:
This preserves behavior-first execution and avoids creating a master router merely to satisfy the concept of orchestration.

Alternatives:
DAG/workflow engine; router agent; planner/executor/evaluator pipeline.

Rejected:
No current case demonstrates a need for those mechanisms.

Trade-offs:
General-purpose intelligence remains an execution dependency. The first contract requires product behavior, not a bespoke model runtime.

Risks:
Human may still rescue routing. Every Human intervention must therefore be classified by AD-006.

Evidence expected:
Controlled reroute case records old route/premise, contradictory evidence, updated state, and new route/blocker.

---

# AD-006 — EXPLICIT HUMAN AUTHORITY GATES AND RESCUE CLASSIFICATION

Requirement: R-006, R-013, C-008

Decision:
Human involvement is typed as either authority or operational rescue; the system cannot blur the distinction.

Mechanism:
Every Human intervention event contains:

```text
classification:
  GENUINE_HUMAN_OWNED_GATE
  HUMAN_OPERATIONAL_RESCUE

authority_reason
requested_decision
response
material_effect
```

The kernel may request a genuine gate only for:

- goal/normative meaning;
- final acceptance;
- costly/public/destructive/irreversible/materially risky effects;
- genuine preference choices unresolved by evidence.

Routine routing/decomposition/recovery instructions from the Human are recorded as `HUMAN_OPERATIONAL_RESCUE` and remain visible in evidence.

Why:
This makes hidden Human runtime measurable without creating dedicated HOT machinery.

Alternatives:
Standalone HOT runtime/instrumentation; untyped Human messages.

Rejected:
HOT runtime is explicitly not pre-authorized; untyped intervention cannot satisfy AC-005.

Trade-offs:
Classification still requires semantic review by P4 for borderline cases.

Risks:
P3 could misclassify rescue as authority. P4 must independently inspect raw event evidence.

Evidence expected:
Accepted run contains an intervention ledger sufficient to classify every material Human intervention.

---

# AD-007 — APPEND-ONLY PROVENANCE AND EXACT ARTIFACT IDENTITY

Requirement: R-010, R-011, C-002, C-004

Decision:
Every material transition and evidence item is bound to exact identities in an append-only event/evidence ledger.

Mechanism:
Each event must record, as applicable:

```text
event_id
run_id
actor/project
prior_state_digest
result_state_digest
task_contract_version
architecture_contract_version
implementation_identity
artifact/source paths
content digest or git blob/SHA
external source/date/identifier
parent event/evidence refs
```

Mutable working files may exist, but evidence references must bind exact bytes/version at the time of claim.

Why:
Directly implements the system-wide provenance invariant and supports fresh-actor recovery.

Alternatives:
Latest-filename references; chat links; prose lineage only.

Rejected:
They cannot establish exact identity after mutation.

Trade-offs:
More metadata per event.

Risks:
External artifacts may not expose Git-style SHA. In that case store a cryptographic digest plus source/date/identifier.

Evidence expected:
Provenance matrix can reconstruct Requirement -> AD -> implementation identity -> evidence -> P4 finding without guessing.

---

# AD-008 — EFFECT-BASED WORKLOAD ADAPTER IS RUN-SPECIFIC, NOT A FRAMEWORK

Requirement: R-001, R-007

Decision:
The first real workload plugs into Projector through a minimal run-specific effect/verification adapter selected only after the Human names OQ-001.

Mechanism:
Core Projector remains domain-neutral at the state/invariant layer. The selected workload defines:

```text
input boundary
allowed reversible operations
effect-based DONE
verification function / observable check
material risk gates
```

P3 may implement only the smallest workload-specific adapter needed for the selected first proof. It must not generalize into a reusable plugin system from one use.

Why:
OQ-001 does not block architecture, but the effect proof cannot be fabricated in advance. This design leaves the semantic workload choice Human-owned while freezing the integration boundary.

Alternatives:
Choose workload in P2; build generic plugin framework now.

Rejected:
P2 cannot take the Human's workload-selection right. A plugin framework violates the two-real-use abstraction rule.

Trade-offs:
A small P3 follow-up commit may be required after the Human selects the workload, but no new architectural decision should be needed.

Risks:
If the selected workload requires capabilities outside the bounded adapter contract (e.g. consequential credentials/deployment), implementation may become BLOCKED pending Human authority or Architecture Contract v1.1.

Evidence expected:
At least one real bounded run reaches independently observable DONE outside Projector build artifacts.

---

# AD-009 — FAILURE / INTERRUPTION PROOF AS FIRST-CLASS TEST CASE

Requirement: R-008

Decision:
The test architecture must deliberately invalidate a material assumption/dependency/route and verify truthful behavior.

Mechanism:
At least one deterministic test fixture starts from a valid run state, introduces a dependency failure or contradictory evidence, and proves that the kernel records the failure and either reroutes or blocks.

No hardcoded success or mock-only happy path is sufficient.

Why:
Failure behavior is explicitly required and must be proven before capability promotion.

Alternatives:
Rely only on naturally occurring failure in real workload.

Rejected:
Could leave R-008 untested and non-reproducible.

Trade-offs:
Controlled test complements rather than replaces real-work evidence.

Evidence expected:
Executable failure-path test plus event/evidence record.

---

# AD-010 — EVIDENCE PACKAGE AND P4 AUDIT BOUNDARY

Requirement: R-007, R-011, R-012, R-013

Decision:
P3 must produce a frozen implementation/evidence package that P4 can inspect without relying on P3's self-assessment.

Mechanism:
The package must include:

```text
IMPLEMENTATION_PACKAGE manifest
exact repository / branch / commit SHA
environment identity
TASK CONTRACT identity
ARCHITECTURE CONTRACT identity
run IDs and exact run artifact identities
requirement-to-evidence provenance matrix
unit/integration/failure test commands and outputs
cold-start recovery evidence
reroute evidence
Human intervention classification evidence
real-work effect evidence
capability registry state after implementation
explicit fields:
  P4 AUDIT = NOT YET AUDITED
  HUMAN ACCEPTANCE = NOT YET CREATED
```

P4 owns final requirement findings. Technical evidence must remain inspectable independently of any P3 claim.

Why:
Separates BUILD from VERIFY and satisfies the provenance invariant.

Alternatives:
Single P3 completion report; screenshots only.

Rejected:
Would make P3's claims part of the proof rather than evidence subject to audit.

Trade-offs:
Requires structured evidence packaging discipline.

Risks:
Evidence package can still omit semantic context; P4 may return UNKNOWN/BLOCKED.

Evidence expected:
P4 can reproduce tests and trace every requirement without requesting hidden chat state.

---

# AD-011 — CAPABILITY REGISTRY IS POST-EVIDENCE GOVERNANCE, NOT RUNTIME

Requirement: R-009

Decision:
Reuse the existing `CAP-GATE-001` verifier only to constrain formal `CAP-ITO-001` status after implementation/evidence exists.

Mechanism:
P3 must not promote `CAP-ITO-001` beyond the level justified by exact registered paths and evidence. The existing registry/verifier remains outside the Projector execution path.

Expected status progression is evidence-dependent, not architecturally predetermined.

Why:
The gate already solves unsupported claim promotion and should not be duplicated. It does not provide Projector behavior.

Alternatives:
New Projector-specific claim registry; integrate capability gate into runtime.

Rejected:
Duplicate governance is unnecessary; runtime integration creates coupling with no behavioral need.

Trade-offs:
Semantic sufficiency still requires P4, as the existing gate itself documents.

Risks:
Mechanical prerequisites may pass while semantic Projector behavior is weak; P4 remains mandatory.

Evidence expected:
Registry and CI are mechanically consistent with the exact evidence package; no unsupported promotion.

---

# COMPONENT MODEL

## 1. Projector Run Kernel

Owns transition validation and invariant enforcement.

Does not own Human intent semantics, domain execution expertise, or final verification verdict.

## 2. Run State Model

Typed representation of Human intent, goal, DONE, observed state, critical unknown, evidence references, route, Human gates, assumptions, and status.

## 3. Durable Run Store

Filesystem-backed run directory in the repository/workspace.

Responsibilities:
- atomic state write;
- append-only events;
- evidence/artifact identity binding;
- reload/recovery.

No database in v1.0.

## 4. Authority Boundary

Classifies requested Human interactions and records authority/rescue events.

## 5. Provenance Binder

Computes/records exact digests/SHAs and parent references for evidence and state transitions.

## 6. Product Entrypoint

Thin CLI/callable for start, inspect/resume, apply evidence/transition, and verify/recover operations.

It must not contain separate planning intelligence.

## 7. Existing COS Capability Gate

External governance component reused after evidence creation. Not part of Projector runtime.

---

# DATA / CONTROL FLOW

## START

```text
raw Human intent
-> start entrypoint
-> bind raw intent + Human-owned goal/DONE fields
-> create run_id
-> persist initial run.json + event 0001
-> identify current critical unknown
-> expose current state to acting Intelligence
```

## NORMAL PROGRESS

```text
current durable state
-> Intelligence proposes next move
-> execute/research/create or request genuine gate
-> collect observation/evidence
-> transition proposal
-> kernel validates invariants
-> append event + bind evidence
-> atomically update run.json
-> repeat
```

## EVIDENCE INVALIDATES ROUTE

```text
current route premise
-> contradictory evidence
-> kernel records premise invalidation
-> obsolete route cannot remain silently active
-> Intelligence proposes reroute or blocker
-> validated transition
```

## RECOVERY

```text
fresh actor
-> open exact implementation identity + run directory
-> load run.json
-> verify events/digests/provenance
-> reconstruct goal/state/blocker/evidence/next move or gate
-> continue without original chat transcript
```

## DONE

```text
candidate DONE claim
-> run-specific verification executes/observes effect
-> evidence bound to exact run
-> kernel records VERIFIED_EFFECT if evidence is sufficient
-> P3 freezes implementation/evidence package
-> P4 independently audits
-> Human records ACCEPTED / REJECTED / DEFERRED
```

---

# INTERFACES

## RunState

Stable fields required by AD-003. P3 may add local fields but may not remove or weaken required semantic distinctions.

## TransitionProposal

Must contain prior identity, actor, evidence/observation classification, next route/gate, rationale, and sources.

## EvidenceRef

Must distinguish:

```text
kind
source
path/identifier
digest/version
observed_at
producer
claim_scope
```

## HumanGate

Must include reason, authority class, requested decision, and whether work is blocked pending response.

## Workload Verification Boundary

Callable or command that returns observable verification data, not a prose assertion. Exact implementation depends on OQ-001 but must produce storable evidence.

---

# INVARIANTS

1. `raw_human_intent` is immutable after run creation.
2. Human-owned goal/DONE can change only through an explicit Human-owned goal-change event.
3. Every material state update has a parent state/event identity.
4. `OBSERVED`, `ASSUMPTION`, `CLAIM`, and `UNKNOWN` remain distinguishable.
5. A claim cannot be upgraded to observed fact without evidence reference.
6. A materially invalidated current route cannot continue silently.
7. Human operational rescue is never recorded as autonomous success.
8. Genuine Human authority is never bypassed by automation.
9. DONE is effect-based and requires run-specific verification evidence.
10. Architecture/docs/code existence never satisfy DONE by themselves.
11. Missing required evidence/provenance yields truthful BLOCKED/UNKNOWN, not PASS.
12. Exact implementation identity is frozen before consequential P3 evidence is claimed.
13. P3 never writes a P4 verdict.
14. Technical PASS never writes Human acceptance.
15. `CAP-ITO-001` status never exceeds registered evidence.

---

# FAILURE MODES

## FM-001 — Weak intent binding
Bound target is merely a paraphrase and not executable/verifiable.

Mitigation: AC-001 test requires raw input and concrete target/DONE state.

## FM-002 — Silent goal drift
Local optimization replaces Human goal.

Mitigation: immutable intent plus explicit Human goal-change event and transition validation.

## FM-003 — Stale route continuation
Contradictory evidence appears but old plan continues.

Mitigation: route premise invalidation event and fail-closed reroute/block rule.

## FM-004 — Hidden Human runtime
Human gives next operational steps.

Mitigation: mandatory intervention classification; rescue remains visible to P4.

## FM-005 — State corruption / partial write
Current state and event history diverge.

Mitigation: atomic state replacement and append event with state digests; recovery verifier fails closed.

## FM-006 — Evidence identity drift
File changes after evidence was cited.

Mitigation: digest/blob/SHA binding at capture time.

## FM-007 — Fake success
Implementation hardcodes DONE/result.

Mitigation: external/run-specific verification and explicit failure-path tests.

## FM-008 — Unsupported capability promotion
Registry claims more than evidence.

Mitigation: existing `CAP-GATE-001` plus P4 semantic audit.

## FM-009 — Workload requires unplanned consequential access
First real workload needs credentials/public/destructive operations.

Mitigation: Human authority gate; if architecture boundary is insufficient, BLOCK and issue Architecture Contract v1.1 rather than silently expand.

---

# SECURITY / SAFETY CONSIDERATIONS

- Default first implementation must support reversible/local effects where possible.
- Public, destructive, irreversible, costly, credential-sensitive, or materially risky effects require Human authority before execution.
- Evidence capture must avoid storing secrets in run artifacts; store references/redacted metadata where needed.
- Run artifact paths must be constrained to the designated run directory when written by Projector storage code.
- External command execution, if needed by a workload adapter, must be explicitly bounded by the adapter and Human authority policy rather than exposed as unrestricted shell capability in the kernel.

---

# MIGRATION / COMPATIBILITY

No Projector implementation exists, so there is no product migration.

Compatibility rules:

- do not change historical governance artifacts to manufacture continuity;
- preserve current `CAP-ITO-001 = PROPOSED` until P3 evidence justifies a status change;
- extend existing CI rather than replace it;
- do not alter existing Ginseng/continuity behavior except where a shared verifier must be minimally updated for new registered Projector evidence;
- P1 PR #45 remains specification provenance and does not become implementation history.

---

# OBSERVABILITY

P3/P4 must be able to observe behavior from durable artifacts without hidden chat state.

Required observable records:

```text
initial raw intent
initial bound goal/DONE
state checkpoints
critical unknown changes
evidence references
route changes
Human gate/rescue events
failure/interruption event
cold-start recovery output
final effect verification
exact implementation identity
capability registry status
```

The primary observability surface is the run state/event/evidence artifacts, not a dedicated telemetry service.

---

# EVIDENCE / TEST ARCHITECTURE

P3 MUST implement executable proofs for at least:

1. Rough intent -> durable bounded target.
2. Goal preservation across multiple material transitions.
3. Fact/assumption/claim/unknown distinction.
4. Route invalidation -> reroute or truthful BLOCKED.
5. Human gate vs Human operational rescue recording.
6. Failure/interruption case.
7. Cold-start recovery from durable artifacts only.
8. DONE rejection without effect evidence.
9. Exact provenance binding and tamper/change detection for evidence/state where implemented.
10. Existing capability gate compatibility.

The first real workload evidence is not replaced by unit/integration tests.

CI should extend the existing workflow with Projector test command(s), preferably standard-library `unittest` to minimize dependency change.

---

# IMPLEMENTATION BOUNDARIES

## MUST

- implement in `FJ899/COS` from the exact frozen P2 base;
- create branch `impl/projector-real-project-v1` from the exact Architecture Contract commit SHA;
- build the minimal Projector vertical slice defined here;
- use durable repository/workspace artifacts for canonical run state;
- maintain append-only material transition history;
- preserve typed evidence/assumption/claim/unknown distinctions;
- enforce Human goal/DONE and authority invariants deterministically;
- record Human operational rescue explicitly;
- support reroute/block after material route invalidation;
- provide cold-start recovery from durable artifacts;
- provide executable happy, reroute, recovery, and failure-path tests;
- produce a frozen implementation/evidence package with exact identities;
- keep `P4 AUDIT = NOT YET AUDITED` until P4 acts;
- keep `HUMAN ACCEPTANCE = NOT YET CREATED` until Human acts;
- use existing capability registry/gate for any capability-status change.

## MAY

- refactor local helpers if behavior remains unchanged and tests cover the refactor;
- add a human-readable rendered summary of `run.json` if canonical state remains machine-readable;
- add schema validation code using the Python standard library;
- add the minimal run-specific workload adapter after Human selects OQ-001;
- update existing workflow with Projector test commands;
- add a deterministic evidence-package verifier if needed to make P4 reproduction easier.

## MUST NOT

- create a new repository without Architecture Contract v1.1;
- introduce a database/persistence service;
- introduce a master router, scheduler, workflow engine, planner/executor/evaluator framework, multi-agent runtime, or generic plugin architecture;
- introduce standalone HOT runtime/instrumentation;
- make capability registry part of Projector's runtime control flow;
- require Human routine routing/decomposition/recovery as normal operation;
- silently classify Human rescue as a genuine authority gate;
- silently mutate Human goal/DONE;
- mark DONE from architecture/code/docs existence;
- fabricate effect evidence;
- promote `CAP-ITO-001` beyond exact evidence;
- write P4 findings or Human acceptance on behalf of those owners;
- generalize a reusable adapter abstraction from the single first workload.

---

# DO NOT CHANGE

The following remain frozen from Task Contract v1.0:

```text
GOAL
R-001 through R-013
C-001 through C-009
NON-GOALS
AC-001 through AC-011
Human authority boundaries
OQ-001 ownership by HUMAN
```

If P3 discovers that these cannot be satisfied under this HOW, implementation stops and returns to P2 with concrete evidence. If satisfying the contract requires changing WHAT, return to P1.

---

# ASSUMPTIONS

## ASSUMPTION A-01

The first vertical slice may depend on the currently available capable AI actor as the intelligence that proposes next moves, provided Projector itself makes the durable state, authority, evidence, transition, and provenance mechanism independently inspectable.

Reason: the Task Contract requires the behavior, not a new model runtime, and explicitly forbids architecture-by-default.

Falsifier: if executable evidence shows that the current Intelligence cannot perform AC-001/AC-004 without a new planning mechanism, P3 must stop and return evidence to P2 rather than adding a router/framework ad hoc.

## ASSUMPTION A-02

Filesystem-backed durable state in the exact repository/workspace is sufficient for the first bounded run.

Falsifier: a selected real workload demonstrates a concrete concurrency/durability requirement that cannot be met safely by atomic local files.

## ASSUMPTION A-03

The first real workload can expose its effect-based DONE through a deterministic or independently observable verification boundary.

This does not select the workload or its semantic DONE; Human still owns OQ-001.

---

# KNOWN RISKS

## KR-001 — Intelligence/kernel boundary may be misunderstood
Projector is not merely JSON persistence, but neither is it a new bespoke AI runtime. P4 must test end-to-end behavior, not file existence.

## KR-002 — One-run adapter could leak domain logic into core
P3 must keep domain-specific verification outside the state kernel and resist premature plugin abstraction.

## KR-003 — Human rescue classification can be gamed semantically
Raw Human interaction evidence must remain available to P4.

## KR-004 — Filesystem artifacts can be manually edited
Digest/event consistency checks and exact Git/evidence identities mitigate but do not make the filesystem tamper-proof. P4 should verify exact committed/frozen package.

## KR-005 — OQ-001 may expose new architectural pressure
This is permitted. If the workload cannot fit the frozen adapter boundary without a material architecture decision, issue v1.1 rather than improvising in P3.

---

# OPEN BLOCKERS

## OQ-001 — FIRST REAL VALIDATION WORKLOAD

```text
OWNER: HUMAN
BLOCKS P2 ARCHITECTURE: NO
BLOCKS P3 CORE IMPLEMENTATION: NO
BLOCKS FINAL REAL-WORK PROOF: YES
```

The workload must be selected before AC-006 real-work execution. Selection must include an effect-based DONE and observable verification independent of Projector build artifacts.

No other architecture blocker is currently known.

---

# P3 HANDOFF GATE

P3 may begin only after the exact commit containing this Architecture Contract is identified and used as the base of `impl/projector-real-project-v1`.

```text
HANDOFF -> P3 IMPLEMENTATION

INPUT:
TASK CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0
ARCHITECTURE CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0

EXACT WORKING SCOPE:
REPOSITORY: FJ899/COS
BASE BRANCH: arch/projector-real-project-v1
BASE SHA: <EXACT SHA CONTAINING ARCHITECTURE CONTRACT v1.0>
IMPLEMENTATION BRANCH: impl/projector-real-project-v1

PURPOSE:
Implement the frozen architecture without redefining WHAT or introducing new architectural mechanisms.

IMPLEMENTATION STATUS AT P2 HANDOFF:
NOT YET IMPLEMENTED

P4 STATUS:
NOT YET AUDITED
```
