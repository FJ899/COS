---
document: GINSENG_DONE_D0_FREEZE
version: 1
status: HUMAN_ACCEPTED_DONE_SCOPE_FREEZE
owner: USER
accepted_at: 2026-08-18
candidate: GINSENG_CANDIDATE_R0
runtime_required_for_d0: false
formal_project_activation_required_for_d0: false
project_completion_claim: NONE
---

# Ginseng DONE D0 — Human Freeze Record

## 1. Human decision

The Human explicitly accepted:

`AKCEPTUJĘ GINSENG_DONE_D0 FREEZE + STATUS RECONCILIATION PR`

This decision freezes the minimum completion criteria against which `GINSENG_CANDIDATE_R0` is to be assessed.

It does **not** declare Ginseng complete, activate a runtime, authorize a new capability, merge COS PR #18, or authorize merge of this PR.

## 2. Why this freeze exists

After `GINSENG_TEST-003: PASS`, the remaining blocker was no longer an observed failure of the tested capability. The unresolved authority gap was the absence of one explicit Human-owned definition of what `GINSENG DONE` means for the frozen R0 candidate.

This record closes that authority gap by freezing `GINSENG_DONE_D0` before any new functional work is selected.

The governing rule remains:

> First establish what exists and what has authority. Only then determine what is still missing to DONE.

## 3. Scope of GINSENG_DONE_D0

`GINSENG_DONE_D0` is the minimum closure contract for `GINSENG_CANDIDATE_R0`.

It is deliberately smaller than a runtime/product-platform definition.

The following are **not required** for D0 unless a later Human decision changes scope:

- Ginseng runtime;
- UI;
- interactive graph;
- graph platform;
- CMDB/external imports;
- fixed database technology;
- fixed JSON/SQL/API/indexing/module architecture;
- release/deploy/tag.

## 4. D0 completion gates

### D-01 — AUTHORITY / CURRENT STATE COHERENCE

DONE requires one current, non-contradictory authority view for the frozen candidate, its governing semantics, test status and completion state.

Requirements:

- later authoritative records must override stale status metadata explicitly rather than by hidden session knowledge;
- historical/open-PR semantics must not be mistaken for current global state;
- local semantic ownership must remain with the correct owner;
- no stale document may claim a test is unexecuted when the accepted current record says it passed.

Current assessment at freeze:

`PARTIALLY SATISFIED — Test-003 status reconciliation included in this PR.`

### D-02 — DECISION-SPACE ANALYSIS

Ginseng must be able to analyze a bounded scenario and preserve traceable distinctions between:

- direct impact;
- indirect impact;
- NO_IMPACT;
- blocking decisions/gates;
- source-backed reasoning.

Current assessment at freeze:

`PROVEN BY EXISTING TEST-2 / TEST-003 EVIDENCE.`

### D-03 — CHANGE PROPAGATION / LOCAL RECALCULATION

After exactly one authorized decision, Ginseng must update only the causally dependent portion of the scenario while preserving unrelated gates, NO_IMPACT controls and baseline state.

Current assessment at freeze:

`PROVEN BY GINSENG_TEST-003 PASS.`

### D-04 — TRUTH TYPES / RELATION AUTHORITY

Ginseng must preserve the semantic separation of:

- `FACT`;
- `DECISION`;
- `HYPOTHESIS`.

It must not allow AI to promote its own hypothesis/relation to authoritative truth without an allowed authority source or Human act.

Current assessment at freeze:

`STRONG EXISTING PROOF — final closure must confirm coverage is sufficient across the D0 evidence set.`

### D-05 — DECISION LINEAGE

Important decisions must preserve enough lineage to answer why they exist and what changes when their premises change.

Minimum closure coverage:

```text
DECISION_ID
PROBLEM
PREMISES
CONSIDERED_OPTIONS
SELECTED_OPTION
SELECTION_REASON
REJECTED_OPTIONS
REJECTION_REASONS
EXPECTED_CONSEQUENCES
DECISION_OWNER
DECIDED_AT
SOURCE_REFERENCES
SUPERSEDES
SUPERSEDED_BY
STATUS
```

Equivalent structure is allowed if it preserves the same semantics.

Current assessment at freeze:

`NOT YET FULLY PROVEN.`

The Test-003 decision fixture proves bounded decision authority and causal propagation, but it was not designed as a complete Decision Lineage lifecycle proof.

### D-06 — ELEMENT → FUNCTION / CAPABILITY → EFFECT

Material impact must be explainable through the function/capability that produces the effect, rather than only through object-to-object dependency labels.

Current assessment at freeze:

`EVIDENCE AUDIT REQUIRED BEFORE ANY NEW TEST OR IMPLEMENTATION.`

Existing Test-2/Test-003 evidence must be checked first. A new capability/test is justified only if the existing evidence cannot establish this gate.

### D-07 — UNCERTAINTY / HUMAN DECISION NEED

Uncertainty must remain visible and must not silently become false certainty.

Unresolved Human-owned decisions must remain unresolved until an authorized decision exists. Ginseng may identify a Human Decision Gate but may not substitute its own normative choice.

Current assessment at freeze:

`EVIDENCE AUDIT REQUIRED BEFORE ANY NEW TEST OR IMPLEMENTATION.`

### D-08 — DURABLE EVIDENCE / REPLAY

DONE requires independently verifiable evidence sufficient to reconstruct the accepted factual result without relying on hidden process memory.

Current assessment at freeze:

```text
independent replay at Test-003 execution time: PROVEN
exact evidence-package identity in COS: RECORDED
full evidence bytes embedded in COS: NO
repo-alone future replay without obtaining exact external package: NOT CLAIMED
```

D0 closure must make an explicit custody decision: either the existing external-package identity is accepted as sufficient for D0, or the exact evidence bytes must be moved into a durable retrievable store under separate authority.

### D-09 — FALSE SUCCESS

No terminal DONE/PASS may be reached through a known false-success path.

Current assessment at freeze:

`PROVEN FOR GINSENG_TEST-003: FALSE SUCCESS PATHS = 0.`

Final D0 closure must confirm that no newly discovered unresolved D0 gate is being bypassed by the completion claim.

## 5. Existing evidence already accepted for reassessment

The following current records are part of the D0 evidence base:

- `governance/GINSENG_CANDIDATE_R0_FREEZE_2026-08-18.md`;
- `tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md`;
- exact recovered Test-2 v1.1 baseline identity;
- reusable Ginseng semantic subset from COS PR #18, subject to the later ownership correction frozen in R0;
- Test-003 independent verifier and replay evidence identity recorded on `main`.

Evidence already proving a gate must be reused. D0 does not authorize creating duplicate proof merely because the proof originated in an earlier test.

## 6. Next-work selection rule

After this freeze, the next task is **not automatically another behavioral test**.

The correct sequence is:

```text
D0 GATE
  -> inspect existing evidence
  -> SATISFIED / NOT SATISFIED / AMBIGUOUS
  -> identify smallest measured gap
  -> only then authorize new work if necessary
```

In particular:

- D-06 and D-07 require evidence audit first;
- D-05 currently has the clearest known proof gap;
- a second gate type such as SoD/RODO remains a recommendation, not an automatic D0 requirement;
- one future test may cover multiple remaining proof gaps only when doing so is the smallest measured path.

## 7. Ownership boundary preserved by D0

```text
HUMAN
  owns goal / DONE / normative decisions

GINSENG
  analyzes decision space, lineage, dependencies,
  consequences, uncertainty and Human-decision needs

EXTERNAL / BASE INTELLIGENCE
  proposes/selects HOW

SADDLE
  validates proposed HOW against intent/boundaries/invariants
  and does not originate or route direction

COS
  preserves durable high-level/cross-project state,
  continuity, provenance and accepted cross-project state
  without taking every component's local semantic ownership

EXECUTOR
  governs authorized consequential effects

VERIFIER
  independently establishes facts
```

D0 does not transfer semantic ownership between layers.

## 8. What this freeze authorizes

This decision authorizes only:

- using `GINSENG_DONE_D0` as the Human-owned closure definition for R0;
- recording this definition in a governance-only PR;
- reconciling stale Test-003 status metadata with the already accepted result record;
- performing a later READ_ONLY evidence audit against D-01 through D-09 after this PR is merged under separate Human authority.

## 9. What this freeze does not authorize

It does **not** authorize:

- merge of this PR;
- runtime activation;
- Ginseng implementation work;
- UI / graph-platform work;
- new tests;
- choosing SoD/RODO or Variant B as a mandatory next test;
- merging COS PR #18;
- changing Saddle or Executor;
- formal project activation;
- project completion claim;
- release/deploy/tag;
- secrets, credentials, paid-service spending or broader external effects.

## 10. State after this freeze if merged

```text
GINSENG_CANDIDATE_R0: HUMAN FROZEN
GINSENG_DONE_D0: HUMAN FROZEN
GINSENG_TEST-003: PASS
TEST-003 STATUS METADATA: RECONCILED

D-02: PROVEN
D-03: PROVEN
D-04: STRONG EXISTING PROOF / CLOSURE AUDIT REQUIRED
D-05: NOT YET FULLY PROVEN
D-06: EVIDENCE AUDIT REQUIRED
D-07: EVIDENCE AUDIT REQUIRED
D-08: REPLAY PROVEN / CUSTODY DECISION OPEN
D-09: PROVEN FOR TEST-003

GINSENG D0 COMPLETION: NOT YET CLAIMED
RUNTIME: NOT REQUIRED FOR D0
FORMAL PROJECT ACTIVATION: NOT REQUIRED FOR D0
```

## 11. Next decision boundary

After merge, the next correct phase is:

`GINSENG D0 EVIDENCE AUDIT`

The audit must attempt to close D-01 through D-09 from evidence already available before proposing any new capability or test.
