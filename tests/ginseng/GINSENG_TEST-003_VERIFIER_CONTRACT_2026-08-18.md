---
document: GINSENG_TEST-003_VERIFIER_CONTRACT
version: 1
status: PREPARATION_ONLY / NOT_EXECUTED
prepared_at: 2026-08-18
candidate: GINSENG_CANDIDATE_R0
verifier_independence_required: true
---

# GINSENG TEST-003 — independent verifier contract

## 1. Mission

The verifier answers only one question:

> Did the frozen R0 candidate, after exactly one test-only decision, produce a causally justified single-gate closure without unauthorized semantic drift or false success?

The verifier does not generate the candidate answer, does not repair candidate artifacts, and does not decide product direction.

## 2. Mandatory independence

A valid verifier run must start in a fresh context and be given:

- exact input hashes and raw input artifacts;
- immutable Test-2 v1.1 BEFORE artifacts;
- exact Test-003 decision fixture;
- raw candidate AFTER artifacts;
- this verifier contract;
- the authoritative Test-003 contract and R0 freeze record.

It must not rely on hidden memory of how the candidate output was produced.

## 3. Source identity gate

Before semantic verification, recompute all hashes in `GINSENG_TEST-003_INPUT_MANIFEST_2026-08-18.json`.

Any mismatch in either source ZIP, internal blind-input file, Test-2 v1.1 BEFORE file, R0 freeze record or Test-003 contract is:

```text
VERDICT: BLOCKED
REASON: INPUT_IDENTITY_MISMATCH
```

No semantic analysis may convert this to PASS.

## 4. Recompute, do not trust summary fields

The verifier independently derives at least:

- active gate set BEFORE and AFTER;
- blocking-gate count BEFORE and AFTER;
- resolved gate identity;
- scenario readiness;
- baseline identity;
- NO_IMPACT node set and semantics;
- impact records changed / added / removed;
- source/provenance coverage;
- changed paths and their causal relation to the test decision.

Candidate summary fields are observations only.

## 5. Exact gate-set rule

The active gate set must satisfy:

```text
AFTER = BEFORE - {complaints_ownership}
```

Equivalent overlay rule:

```text
PROCESS_OWNER_GATE = RESOLVED / non-blocking
REPORTING_LINE_GATE = semantically preserved blocking
SOD_RODO_GATE = semantically preserved blocking
SERVICE_QUALITY_GATE = semantically preserved blocking
DATA_OWNERSHIP_GATE = semantically preserved blocking
CRM_KNOWLEDGE_GATE = semantically preserved blocking
KPI_BASELINE_GATE = semantically preserved blocking
```

A correct count with a wrong set is FAIL.

## 6. Single-decision causal rule

Every semantic change in an impact or dependency path must be traceable to:

```text
GINSENG_TEST003_DECISION_A
  -> DEC002 / R003 / P002
  -> optional downstream dependency chain
```

A changed item with no such causal chain is unauthorized semantic drift and therefore FAIL.

The verifier must not assume in advance which downstream nodes must change. It must inspect the candidate's declared causal path against the blind graph.

## 7. Remaining-gate semantic preservation

The verifier must compare meaning, not just gate IDs.

For each of the six remaining gates, compare at minimum:

- subject / affected node(s);
- blocking reason;
- required decision/action;
- governing source references;
- status;
- severity/criticality when represented.

Stylistic wording differences are allowed only when these semantics remain equivalent.

If a remaining gate becomes materially weaker, broader, narrower or easier to satisfy without new authority, FAIL.

## 8. NO_IMPACT regression gate

The five Test-2 controls are:

```text
P003
I002
C001
A003
G003
```

For each control, compare classification, reason and causal/path justification.

If any changes, the verifier must require a new causal path originating from the test decision and validate that path against the blind graph.

Absent that proof, FAIL.

## 9. Baseline immutability gate

Recompute hashes for all original blind-input files and validate that the candidate AFTER bundle does not replace or mutate them.

`baseline_mutated = false` is valid only when independently proven.

Any baseline mutation is FAIL.

## 10. Readiness gate

With six blocking gates remaining:

```text
implementation_readiness MUST remain BLOCKED
```

Any `READY`, `GO_FOR_IMPLEMENTATION`, equivalent positive implementation state, or hidden removal of blocking semantics is FAIL.

The analysis verdict may be expressed differently only if it remains logically consistent with six active blockers and does not imply readiness.

## 11. Provenance and truth-type gate

The verifier must confirm:

- all original 17 Test-2 source records remain attributable;
- the test decision has a distinct ID and provenance;
- the test decision is not represented as an external FACT;
- AI-generated relations/hypotheses are not self-promoted to authoritative `CONFIRMED`, `FACT` or production `DECISION` without an allowed authority source;
- every changed impact retains source or reasoning traceability.

A loss of provenance or truth-type escalation is FAIL.

## 12. Manual-patch / fake-recalculation attack

The verifier must attempt to distinguish causally supported recalculation from a superficial patch.

At minimum, test these adversarial cases against the raw AFTER artifacts:

1. remove only the gate name while leaving `R003/P002/DEC002` conflict text unresolved;
2. set `blocking_gate_count = 6` while retaining seven blocking records;
3. mark `PROCESS_OWNER_GATE` resolved while retaining contradictory ownership relations;
4. delete one blocking decision but leave all related impact semantics untouched when the decision requires a semantic change;
5. rewrite unrelated impacts to make the output look newly generated;
6. modify source index or evidence to hide provenance loss;
7. report `baseline_mutated = false` while input bytes differ.

If the candidate artifacts can pass solely through such a superficial edit, FAIL.

## 13. Delta completeness gate

`S001_gate_closure_delta.json` must enumerate every semantic change relative to Test-2 v1.1.

The verifier independently computes a normalized semantic diff and compares it to the declared delta.

Rules:

```text
undeclared semantic change -> FAIL
falsely declared change -> CONCERN, and FAIL if it obscures causality or gate semantics
format-only undeclared change -> allowed only when proven non-semantic
```

## 14. Artifact integrity gate

The six required AFTER artifacts must all exist and parse where applicable.

The evidence record must include SHA-256 values for all AFTER artifacts and those values must match raw bytes.

Missing or mismatched evidence is BLOCKED unless the mismatch proves candidate tampering, in which case FAIL.

## 15. Evidence replay

A fresh verifier must be able to reproduce the final verdict from the saved bundle alone.

Replay must not require:

- the original chat session;
- process memory;
- manually remembered reasoning;
- unpublished corrections.

If replay cannot determine the same verdict, Test-003 cannot PASS.

## 16. PASS_WITH_FIXES boundary

`PASS_WITH_FIXES` is permitted only when all of the following are already true:

- exact gate logic PASS;
- exact single-gate closure PASS;
- baseline immutability PASS;
- remaining six gates semantic preservation PASS;
- NO_IMPACT regression PASS;
- readiness remains BLOCKED;
- provenance/truth-type integrity PASS;
- no false-success path exists;

and the remaining defect is only naming, formatting or report completeness as permitted by the authoritative Test-003 contract.

## 17. Required verifier output

Return at least:

```text
INPUT IDENTITY: PASS / BLOCKED
SINGLE GATE CLOSURE: PASS / FAIL
CAUSAL DELTA: PASS / FAIL
REMAINING SIX GATES: PASS / FAIL
NO_IMPACT CONTROLS: PASS / FAIL
BASELINE IMMUTABILITY: PASS / FAIL
READINESS: PASS / FAIL
PROVENANCE / TRUTH TYPES: PASS / FAIL
ARTIFACT INTEGRITY: PASS / BLOCKED / FAIL
EVIDENCE REPLAY: PASS / BLOCKED / FAIL
FALSE SUCCESS PATHS: <integer>
```

Final verdict exactly one of:

```text
GINSENG_TEST-003: PASS
GINSENG_TEST-003: PASS_WITH_FIXES
GINSENG_TEST-003: FAIL
GINSENG_TEST-003: BLOCKED
```

If not PASS, include the smallest causal blocker.

## 18. Non-authority

A verifier PASS establishes facts about this test only.

It does not by itself:

- activate Ginseng runtime;
- establish whole-project completion;
- authorize new capability work;
- merge a result PR;
- modify COS, Saddle or Executor ownership;
- authorize release/deploy/tag or external effects.
