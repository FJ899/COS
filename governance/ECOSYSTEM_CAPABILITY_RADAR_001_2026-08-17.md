# ECOSYSTEM CAPABILITY RADAR — 001

Date: 2026-08-17
Status: EVIDENCE SNAPSHOT / READ_ONLY FINDINGS / NO ADOPTION CLAIMED
Scope: COS / Ginseng / Executor

## Purpose

Preserve the strongest findings from an external capability scan so that the conversation is not the only place where the reasoning survives.

The radar does not authorize implementation. A candidate remains external evidence until it passes impact analysis, architecture comparison, an appropriate gate, and a user decision.

## Search orientation

Priority areas:

- decision lineage and provenance;
- independent verification;
- evidence / attestation;
- change propagation and invalidation;
- temporal / versioned knowledge;
- controlled execution and sandboxing;
- context routing / progressive disclosure;
- canonical-state reconciliation;
- workflow reconstruction / replay;
- human decision gates;
- mature mechanisms that can replace something we might otherwise build ourselves;
- anti-patterns showing what not to build.

## Strongest candidates from Radar 001

### RADAR-001-A — in-toto / Sigstore / Rekor

Problem area: authorized execution, signed evidence, artifact provenance, independent verification.

Why relevant:

- resembles the Executor → Evidence → Verifier trust problem;
- may provide mature semantics for binding an authorized step to its inputs, outputs and attestations;
- may reduce the amount of custom Evidence / Ledger design we need to invent.

Current recommendation: INVESTIGATE_FURTHER — HIGHEST PRIORITY.

Deep-dive questions:

1. Which semantics can be reused without importing a full software-supply-chain stack?
2. Can an in-toto-style statement replace part of a custom evidence schema?
3. Which trust assumptions do Sigstore/Rekor add, and which remain external?
4. How do they prevent or detect evidence produced by the same party that is being verified?
5. Which failure modes map directly to Executor P1/P2?

No implementation is authorized by this record.

### RADAR-001-B — Bazel dependency / invalidation model

Problem area: determine what actually needs recalculation or retesting after a change.

Why relevant:

- strong conceptual match for future Ginseng impact propagation;
- suggests explicit dependency edges + transitive impact instead of broad AI guessing;
- may support targeted regression rather than full-system retesting.

Current recommendation: DEFER_UNTIL_GATE / HIGH-VALUE FUTURE TEST.

Important caution: a decision graph is not a build graph. Business and semantic dependencies can be uncertain, conditional and temporal.

### RADAR-001-C — Temporal event history / replay

Problem area: reconstruct workflow state after process loss and continue from durable history.

Why relevant:

- potential model for replayable evidence and state reconstruction;
- useful distinction between append-only history and derived current state.

Current recommendation: ADAPT_EXISTING AS A MODEL ONLY.

Do not infer a need for Temporal runtime.

### RADAR-001-D — Argo CD desired / observed / diff

Problem area: distinguish what should be true from what is actually true.

Why relevant:

- maps cleanly to canonical state vs observed implementation state;
- strengthens the existing rule that canonical acceptance is not the same as implementation status.

Current recommendation: ADAPT_EXISTING SEMANTICS.

Do not copy automatic reconciliation. A semantic diff may require Human Decision Gate rather than automatic apply.

### RADAR-001-E — gVisor / Firecracker isolation

Problem area: stronger execution boundary for untrusted candidate code.

Why relevant:

- benchmark for the quality of an Executor sandbox;
- reinforces the anti-pattern: containerized does not automatically mean safely sandboxed.

Current recommendation: DEFER_UNTIL_GATE.

Use only if P1/P2 demonstrates a concrete insufficiency in the current isolation boundary.

### RADAR-001-F — Open Policy Agent

Problem area: separate policy decision from policy enforcement.

Why relevant:

- possible future pattern for known authorization rules;
- could reduce scattered runtime permission checks.

Current recommendation: DEFER_UNTIL_GATE.

Important boundary: a policy engine may evaluate an existing policy; it must not replace the human for a new goal, new risk decision or undefined policy.

### RADAR-001-G — OpenLineage small core + extensible facets

Problem area: evolve structured evidence without turning one schema into a giant object.

Why relevant:

- suggests a small stable envelope with optional typed extensions;
- may fit Evidence Package evolution better than one monolithic schema.

Current recommendation: INVESTIGATE_FURTHER.

This is a candidate pattern, not an adopted Evidence Package design.

## Cross-cutting anti-patterns

### AP-RADAR-001 — APPEND-ONLY DOES NOT MEAN SELF-TRUSTING

A ledger or transparency log being append-only does not by itself make the resulting truth independently trustworthy.

Implication for COS / Executor:

- do not let a future ledger prove itself;
- keep independent verification / monitoring as a separate trust concern;
- preserve FALSE SUCCESS = 0.

### AP-RADAR-002 — CONTAINERIZED IS NOT EQUIVALENT TO TRUSTED SANDBOX

Isolation claims must be tested against the actual trust boundary, not inferred from the use of containers.

### AP-RADAR-003 — DO NOT IMPORT THE WHOLE FRAMEWORK TO GET ONE GOOD SEMANTIC PATTERN

Preferred order:

1. identify the useful invariant or mechanism;
2. compare with what COS already has;
3. reuse existing architecture when possible;
4. import runtime only after a measured blocker proves it necessary.

## Future ideas promoted from this radar

The following should exist in the canonical Idea Inbox as PARKING / FUTURE IDEAS rather than active architecture:

1. Radar Deep Dive Escalation — automatically or manually promote only the strongest radar findings to source-level deep dives before any adoption decision.
2. Component Impact & Integration Testing — impact-before-adoption with dependency/blast-radius analysis and targeted regression.
3. Same Capability, Smaller Footprint — actively search for functionally equivalent mechanisms with lower complexity, runtime, dependency, state, context or attack-surface cost; improvement does not have to mean newer.
4. Evidence Package: Small Stable Core + Extensible Facets — investigate whether evidence can evolve through typed extensions rather than one monolithic schema.

## Radar principle

The best external discovery may be a reason to delete something from our future architecture, not a reason to add another component.

Desired question:

> Can this mature external mechanism let us remove, simplify or avoid building part of COS / Ginseng / Executor while preserving the required capability and invariants?

## Implementation status

ARCHITECTURE CHANGE: NO
NEW COMPONENT: NO
RUNTIME CHANGE: NO
EXECUTOR CONTRACT CHANGE: NO
GINSENG SEMANTICS CHANGE: NO
ADOPTION DECISION: NO

This file preserves evidence and candidate reasoning only.
