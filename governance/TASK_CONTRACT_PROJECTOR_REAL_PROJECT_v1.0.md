# TASK CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT

VERSION: v1.0
STATUS: READY FOR P2 ARCHITECTURE
SOURCE BASELINE: `governance/CURRENT_STATE_BASELINE_PROJECTOR_REAL_PROJECT_v1.0.md`
SOURCE TECHNICAL BASELINE: `FJ899/COS main@bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19`
SOURCE HUMAN INTENT: explicit project activation in current Human conversation on 2026-08-25

## PROBLEM

Projector / Intent-to-Outcome currently exists as an accepted product direction and a formal capability claim (`CAP-ITO-001`), but not as an evidenced real product capability.

Current registered status is `PROPOSED`, with no registered implementation, executable evidence, integration evidence, real-work evidence or reliability evidence.

The problem is not lack of architecture documentation. The problem is the absence of a real, independently verifiable capability that can take Human intent through uncertain work to an observable outcome while preserving Human authority and without depending on hidden Human operational orchestration.

## GOAL

Turn Projector / Intent-to-Outcome from a conceptual/capability target into a real, versioned project whose first bounded product result can be independently shown to do the following:

```text
ROUGH HUMAN INTENT
-> bounded target
-> evidence-driven progress
-> durable state
-> re-routing when evidence changes the path
-> genuine Human authority gates only
-> observable effect-based DONE
```

The project is complete for this contract when the exact implementation has produced the required end-to-end evidence, P4 has independently audited it against this Task Contract, and the Human can make a final acceptance decision from that evidence.

This contract does not require `RELIABLE` multi-project maturity. Reliability beyond the first independently audited real-work proof is a possible later phase.

---

# REQUIREMENTS

## R-001 — REAL PRODUCT, NOT ARCHITECTURE PROXY

The result must be an observable working capability, not merely an architecture, repository scaffold, interfaces, schemas, prompts, documentation, component names or implementation claims.

## R-002 — ROUGH HUMAN INTENT INPUT

The Human must be able to begin with an unstructured or partially structured intent without being required to choose implementation tooling, architecture, repository structure, workflow engine or ecosystem component.

The product may request Human input only when information genuinely owned by the Human is missing.

## R-003 — INTENT PRESERVATION

The system must preserve the Human-owned goal and run-specific definition of DONE throughout execution.

A downstream optimization, local task or implementation convenience must not silently replace the Human goal.

## R-004 — CURRENT STATE AND CRITICAL UNKNOWN

During active work the system must maintain enough durable state to identify at minimum:

```text
CURRENT GOAL
CURRENT OBSERVED STATE
CURRENT CRITICAL UNKNOWN / BLOCKER
CURRENT EVIDENCE
NEXT JUSTIFIED MOVE OR GATE
```

The state must distinguish observed facts from assumptions, claims and unknowns.

## R-005 — EVIDENCE-DRIVEN PROGRESS AND RE-ROUTING

The system must choose productive or evidence-seeking next moves from the current state rather than follow a fixed component pipeline.

When material evidence invalidates the current path, the system must update state and re-route rather than silently preserve the obsolete plan.

## R-006 — HUMAN AUTHORITY WITHOUT HUMAN RUNTIME

The Human retains authority over:

- goal and normative meaning;
- final acceptance;
- costly, public, destructive, irreversible or materially risky effects;
- genuine preference choices that cannot be resolved by evidence.

The product must not depend on the Human to provide routine operational routing, decomposition, recovery or next-step orchestration that the claimed capability is supposed to provide.

Any Human operational rescue must be explicitly recorded as evidence and must not be silently treated as autonomous system success.

## R-007 — EFFECT-BASED REAL-WORK PROOF

At least one real, bounded workload must reach a run-specific effect-based DONE with observable evidence.

The validation workload's DONE must not be defined solely as:

- architecture completed;
- code written;
- repository created;
- interfaces defined;
- documentation produced;
- Projector declared finished.

The evidence must establish an outcome outside the mere existence of the Projector build artifacts, preventing circular self-proof.

## R-008 — FAILURE / INTERRUPTION BEHAVIOR

The project must have evidence for relevant failure or interruption paths, including at minimum one case in which an assumption, dependency, input or current route becomes invalid or unavailable.

The system must fail, block, recover or re-route truthfully according to the case; it must not manufacture success.

## R-009 — CAPABILITY CLAIM DISCIPLINE

Formal capability status must never exceed available evidence.

`CAP-ITO-001` or any successor capability claim may be promoted only to a status justified by the exact implementation and evidence package.

Documentation, architecture and code existence alone cannot justify a working-capability claim.

## R-010 — DURABLE RECOVERABILITY

Material project state needed to continue work must be recoverable from durable artifacts without depending on one chat session or hidden model memory.

A fresh actor with the required artifact access must be able to recover the Human goal, exact current artifact identity, current state and unresolved blocker/next evidence point.

## R-011 — END-TO-END PROVENANCE

For every completed stage it must be possible to identify unambiguously:

```text
requirement owner
TASK CONTRACT version
architecture decision owner
ARCHITECTURE CONTRACT version
implementation owner
exact implementation identity
evidence supporting each material requirement
independent verifier / P4
exact artifact versions used at each completed stage
```

For stages not yet reached, the state must remain explicitly `NOT YET CREATED`, `NOT YET IMPLEMENTED` or `NOT YET AUDITED`.

## R-012 — INDEPENDENT FINAL AUDIT

P4 must independently verify the exact implementation/evidence package against the frozen Task Contract and return requirement-level findings using only:

```text
PASS
FAIL
UNKNOWN
BLOCKED
NOT APPLICABLE
```

P3's implementation claims are not sufficient evidence of compliance.

## R-013 — HUMAN FINAL ACCEPTANCE

Final project acceptance belongs to the Human and occurs only after the independent audit result and underlying evidence are available.

A technical PASS must not be silently converted into Human acceptance, release or deployment authority.

---

# CONSTRAINTS

## C-001 — FOUR-PROJECT DELIVERY PIPELINE

The project must use the frozen responsibility split:

```text
P1 SPECIFICATION -> WHAT
P2 ARCHITECTURE -> HOW
P3 IMPLEMENTATION -> BUILD
P4 INDEPENDENT AUDIT -> VERIFY
HUMAN -> FINAL INTENT / ACCEPTANCE
```

A project must not self-approve its own downstream artifact.

## C-002 — FROZEN INPUTS AND VERSIONING

Every handoff artifact is frozen by exact version. Changes require a new version and must not overwrite decision history.

## C-003 — NO SILENT REINTERPRETATION

Downstream projects must not silently change this Task Contract. If it is contradictory, incomplete or impossible, work stops and returns to P1 with the specific issue.

## C-004 — EXACT IDENTITY BEFORE TECHNICAL WORK

Before consequential implementation or audit, exact relevant identity must be established, including repository, branch, SHA/version, files and environment where applicable.

P1 does not select those implementation identities unless they are part of Human-owned intent.

## C-005 — BEHAVIOR-FIRST

No new component, module, router, scheduler, agent, cache, runtime, adapter or abstraction may be justified merely because it appears useful in a future architecture.

A new mechanism must trace to a requirement and an observed/credible case it is needed to satisfy.

## C-006 — NO FORCED ECOSYSTEM PIPELINE

The product must not require every existing ecosystem component to participate in every run.

Use of existing components must be justified by the real task and architecture, not by a component quota.

## C-007 — HOT IS NOT A PRE-AUTHORIZED IMPLEMENTATION

Human Orchestration Tax / Rescue Dependency concepts may be used as evidence or measurement constructs where useful.

The archived standalone HOT runtime/instrumentation path is not implementation authority. Dedicated HOT machinery requires evidence-based justification through the normal architecture process.

## C-008 — HUMAN AUTHORITY MUST BE PRESERVED

Reducing Human operational rescue must not remove or bypass genuine Human authority, consent, preference or final-acceptance gates.

## C-009 — NO FALSE MATURITY PROMOTION

A first successful real-work result may support the corresponding evidence status, but must not automatically produce a `RELIABLE` or broader generality claim.

---

# NON-GOALS

This Task Contract does not require:

- a specific framework, language, architecture pattern or repository topology;
- a master router, scheduler, multi-agent runtime or new autonomous platform;
- integration of every existing COS ecosystem project;
- a standalone HOT implementation;
- replacement of Human semantic authority with autonomous decision-making;
- proving broad multi-project reliability in this first project phase;
- release, public deployment, paid services, new credentials or other consequential external effects unless separately authorized.

---

# ACCEPTANCE CRITERIA

## AC-001 -> R-001, R-002

Given an initial rough Human intent, the exact tested product path must produce or bind a bounded working target without requiring the Human to choose the implementation architecture/toolchain as part of normal product operation.

Evidence must include the raw input and resulting bound target/state.

## AC-002 -> R-003

Across the accepted run, every material state transition must remain traceable to the same Human-owned goal/DONE or to an explicit Human-approved goal change.

P4 must find zero silent goal substitutions.

## AC-003 -> R-004, R-010

At a selected checkpoint during an unfinished run, a fresh recovery using durable artifacts must correctly reconstruct:

```text
goal
current observed state
critical unknown/blocker
material evidence
exact artifact identity
next justified move or Human gate
```

without relying on the original chat transcript as the sole state source.

## AC-004 -> R-005

When a controlled or naturally occurring material evidence change invalidates the current route, the evidence package must show:

```text
old route / assumption
new evidence
state update
new justified route or truthful blocker
```

The obsolete route must not continue silently.

## AC-005 -> R-006

For the accepted end-to-end run, every material Human intervention must be classifiable from evidence as either:

```text
GENUINE HUMAN-OWNED GATE
or
HUMAN OPERATIONAL RESCUE
```

A PASS on the no-hidden-Human-runtime claim requires that no unacknowledged Human operational rescue was necessary for the claimed successful behavior.

If rescue occurred, it must remain visible and the affected requirement must receive the evidence-supported verdict rather than being silently passed.

## AC-006 -> R-007

At least one real bounded workload reaches its predefined effect-based DONE, and that DONE is verified by an observable artifact, external state, measurement or independently reproducible result beyond the existence of Projector source code/documentation itself.

## AC-007 -> R-008

At least one executable or reproducible failure/interruption case demonstrates truthful behavior when a material assumption, input, dependency or route fails.

A hardcoded or fabricated success result fails this criterion.

## AC-008 -> R-009

The formal capability registry/status after implementation must be mechanically and semantically consistent with the evidence package.

P4 must find zero capability promotions unsupported by the exact evidence referenced.

## AC-009 -> R-011

A provenance matrix must trace every requirement in this contract through:

```text
Requirement
-> Architecture Decision
-> Implementation identity
-> Test / Evidence
-> P4 finding
```

Any required missing link for a completed stage produces `UNKNOWN` or `FAIL`, not `PASS`.

## AC-010 -> R-012

P4 produces an independent requirement-level audit for the exact frozen artifacts and reports a final project verdict without relying on P3's self-assessment.

## AC-011 -> R-013

After P4, a distinct Human acceptance state is recorded as one of:

```text
ACCEPTED
REJECTED
DEFERRED / MORE EVIDENCE REQUIRED
```

No technical artifact may fabricate this state.

---

# ASSUMPTIONS

## ASSUMPTION A-01

The phrase "replace the idea with a real project" refers to the immediately preceding active Projector / Intent-to-Outcome direction (`CAP-ITO-001`), not to the separately parked HOT implementation track.

Basis: immediate conversation sequence and explicit prior decision to park HOT as a separate program.

If the Human later names a different semantic target, P1 must issue Task Contract v1.1+ rather than silently rebind this contract.

---

# OPEN QUESTIONS

## OQ-001 — FIRST REAL VALIDATION WORKLOAD

The exact real workload used for AC-006 is not yet selected.

```text
OWNER: HUMAN
BLOCKS P2 ARCHITECTURE: NO
BLOCKS FINAL REAL-WORK VERIFICATION: YES
```

It must be selected before the real-work proof is executed and must have an effect-based DONE independent of merely building Projector.

No other open question currently requires P2 to guess fundamental Human intent.

---

# SOURCE OF TRUTH

Conflict precedence for this project:

1. latest explicit Human intent / acceptance decision;
2. this exact `TASK CONTRACT v1.0` for WHAT;
3. `CURRENT_STATE_BASELINE_PROJECTOR_REAL_PROJECT v1.0` for starting-state facts;
4. canonical COS evidence/governance artifacts at the pinned source identity;
5. P2 Architecture Contract for HOW only;
6. P3 Implementation Package for BUILD facts only;
7. P4 Audit for independent verification findings.

The archived HOT alternative is historical/parking material and is not current implementation authority.

---

# KNOWN RISKS

## KR-001 — SELF-HOSTING CIRCULARITY

Building Projector with project chats can create an appearance of proof even when Human orchestration supplied the missing capability. AC-005 and AC-006 explicitly guard against this.

## KR-002 — ARCHITECTURE THEATER

A sophisticated architecture may look like progress without delivering the required behavior.

## KR-003 — HIDDEN HUMAN ORCHESTRATION

The Human may unconsciously become the router/planner/recovery mechanism and make the run appear more autonomous than it is.

## KR-004 — SINGLE-RUN OVERGENERALIZATION

One successful run can establish bounded evidence but not general reliability.

## KR-005 — PROVENANCE LOSS BETWEEN PROJECT CHATS

P1–P4 are separate projects. Missing exact artifact versions at handoff can destroy traceability even if each local result appears reasonable.

## KR-006 — TOOL / COMPONENT GRAVITY

Existing COS components may be used because they exist rather than because requirements need them.

---

# OUT OF SCOPE

Anything not required to satisfy R-001 through R-013, including speculative ecosystem expansion, unrelated parked ideas and unrequested release/deployment work.

---

# HANDOFF

```text
HANDOFF -> P2 ARCHITECTURE

INPUT:
TASK CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0

SOURCE BASELINE:
CURRENT STATE BASELINE PROJECTOR REAL PROJECT v1.0

PURPOSE:
Design a solution satisfying the frozen WHAT without reinterpreting it.

P2 MUST RESOLVE BEFORE P3:
- implementation repository / repository topology
- branch / base SHA
- architecture decisions
- component boundaries
- interfaces
- test/evidence strategy sufficient for this contract
- exact Architecture Contract version

P2 MUST NOT:
- treat CAP-ITO-001 as already implemented
- promote HOT archive into a requirement without evidence
- equate architecture completion with project completion
- silently change Human authority boundaries
```
