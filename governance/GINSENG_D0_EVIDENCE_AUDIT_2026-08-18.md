---
document: GINSENG_D0_EVIDENCE_AUDIT
version: 1
status: READ_ONLY_AUDIT_RECORDED
owner: HUMAN_AUTHORIZED_AUDIT
candidate: GINSENG_CANDIDATE_R0
done_scope: GINSENG_DONE_D0
audited_at: 2026-08-18
runtime_claim: NONE
project_completion_claim: NONE
---

# Ginseng D0 — Evidence Audit

## 1. Human authority

The Human explicitly authorized:

`AKCEPTUJĘ GINSENG D0 EVIDENCE AUDIT`

and subsequently authorized recording the result together with the bounded D-01 current-state reconciliation:

`AKCEPTUJĘ GINSENG D0 AUDIT RECORD + D-01 STATUS RECONCILIATION PR`

This record captures the completed READ_ONLY audit against the Human-frozen `GINSENG_DONE_D0` criteria.

It does not authorize a new behavioral test, implementation, runtime, UI, graph platform, external imports, release, deployment, tag, secrets, credentials, spending, merge of COS PR #18, or a Ginseng D0 completion claim.

## 2. Exact repository context

Audit repository:

`JTJ07/COS`

Exact `main` at audit / branch creation:

`ddaf354b87460ff7261838b64526ca5f092e94a5`

Relevant authoritative current records:

- `governance/GINSENG_CANDIDATE_R0_FREEZE_2026-08-18.md`;
- `governance/GINSENG_DONE_D0_FREEZE_2026-08-18.md`;
- `tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md`;
- `tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md`.

Recovered exact source identities retained by the frozen candidate:

```text
GINSENG_TEST_2_BLIND_INPUT(1).zip
SHA-256:
b0cccb8fc9be9049faaaca90f50e3983fce2540a7d449dbb2c6e99c4814ee7cf

GINSENG_TEST_2_S001_RESULT_v1_1.zip
SHA-256:
4abaf4696d4c7f832c99ccd3e7586e8618c45e893f5d0e2e3ce66c97206a36be
```

Test-003 evidence package identity:

```text
GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.zip
SHA-256:
d9077d08012667a8a2a91e93912ee752bf991b50b5b01e4d2f80914cde315fdf
entry_count: 39
```

## 3. Audit rule

For each D0 gate the audit first reused already available evidence.

No duplicate proof was created merely because the proof originated in an earlier test.

Classification:

```text
SATISFIED
NOT SATISFIED
HUMAN DECISION REQUIRED
FINAL RECHECK REQUIRED
```

A missing proof is not converted into a new capability requirement automatically.

## 4. Gate results

### D-01 — AUTHORITY / CURRENT STATE COHERENCE

Audit verdict before this PR:

`NOT SATISFIED`

Observed contradiction:

- the authoritative Test-003 contract on current `main` states `EXECUTED / INDEPENDENTLY_VERIFIED_PASS`;
- the later result record states `GINSENG_TEST-003: PASS`;
- `CREATIVE_OS.md`, which is used as the cross-project state owner by `START_HERE.md`, still states `QUEUED / NOT EXECUTED` in the current test queue and current handoff.

This is a state-coherence defect, not a failure of Ginseng behavior.

Bounded reconciliation in this PR updates only current-state references in `CREATIVE_OS.md` to the already accepted Test-003 result and current D0 audit state.

Historical append-only records are not rewritten as though the past never happened.

If this PR is merged without conflicting state changes:

`D-01: SATISFIED`

### D-02 — DECISION-SPACE ANALYSIS

Verdict:

`SATISFIED`

Existing Test-2 / Test-003 evidence demonstrates bounded scenario analysis with traceable distinctions between:

- direct impacts;
- indirect impacts;
- `NO_IMPACT` controls;
- blocking decisions/gates;
- source-backed reasoning.

No new test is required for D-02.

### D-03 — CHANGE PROPAGATION / LOCAL RECALCULATION

Verdict:

`SATISFIED`

`GINSENG_TEST-003: PASS` independently established that one authorized test decision:

- closed exactly one intended blocking gate;
- reduced blocking gates from `7` to `6`;
- changed only causally dependent impacts;
- preserved the other six blocking gates;
- preserved all five `NO_IMPACT` controls;
- preserved the baseline;
- kept `implementation_readiness = BLOCKED`.

No new test is required for D-03.

### D-04 — TRUTH TYPES / RELATION AUTHORITY

Verdict:

`SATISFIED`

The current evidence set preserves the relevant authority boundary:

- `FACT`, `DECISION` and `HYPOTHESIS` remain distinct semantic classes;
- the Test-003 injected choice remains separately typed as `TEST_ONLY_DECISION`;
- it is not promoted to an external FACT or production DECISION;
- AI-generated relations/hypotheses are not accepted as authoritative truth without an allowed authority source or Human act.

No new D-04 test is justified by the observed evidence.

### D-05 — DECISION LINEAGE

Verdict:

`NOT SATISFIED`

This is the smallest currently measured functional proof gap.

Existing evidence proves decision identity, bounded authority, source references and causal propagation, but the audit did not find one complete lifecycle proof covering the full D0 lineage semantics together:

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

Equivalent field names remain acceptable if they preserve the same semantics.

This verdict does not yet prescribe HOW to close D-05 and does not authorize a new test.

### D-06 — ELEMENT -> FUNCTION / CAPABILITY -> EFFECT

Verdict:

`SATISFIED`

Existing Test-2/Test-003 evidence already contains causal paths and semantic relations that explain material effects through functions/capabilities rather than only through generic object-to-object dependency labels.

Examples in the accepted evidence include roles/units performing or owning processes and paths using semantic relations such as `PERFORMS`, `OWNS`, `USES`, `MEASURED_BY` and `SUPPORTS`.

The Test-003 recalculation preserved this explanatory structure while changing only the authorized causal scope.

No separate D-06 behavioral test is required.

### D-07 — UNCERTAINTY / HUMAN DECISION NEED

Verdict:

`SATISFIED`

Existing evidence shows that unresolved Human-owned decisions remain unresolved rather than being silently converted into certainty:

- Test-2 surfaced seven blocking Human decision gates;
- Test-003 supplied exactly one bounded test decision;
- exactly one gate closed;
- the other six remained blocking;
- readiness remained `BLOCKED`;
- no remaining gate was normatively resolved by the model.

No separate D-07 behavioral test is required.

### D-08 — DURABLE EVIDENCE / REPLAY

Technical replay verdict:

`SATISFIED`

Evidence custody verdict:

`HUMAN DECISION REQUIRED`

The Test-003 evidence was independently replayable without original process memory and the replayed verifier report was byte-identical to the original verifier report.

The exact external evidence package identity is durably recorded in COS.

However, the full evidence bytes are not embedded in COS itself.

Therefore D0 still requires the Human-owned custody choice already frozen in `GINSENG_DONE_D0`:

```text
A — accept exact external package + recorded digest/retrievability as sufficient D0 custody

or

B — require exact evidence bytes to be copied into a durable retrievable store under separate authority
```

The audit does not choose A or B.

### D-09 — FALSE SUCCESS

Current evidence verdict:

`SATISFIED`

Test-003 independently reported:

`FALSE SUCCESS PATHS: 0`

The prepared adversarial checks covered fake gate counts, closing the wrong/additional gate, baseline drift, `NO_IMPACT` drift, semantic weakening of remaining gates, provenance loss, readiness false-positive, truth-type escalation, undeclared semantic delta and candidate authority over the detached artifact manifest.

Final requirement:

`FINAL RECHECK REQUIRED AT D0 CLOSURE`

D-09 cannot be used to bypass an unresolved D0 gate.

## 5. Audit summary

```text
D-01 AUTHORITY / CURRENT STATE:            NOT SATISFIED -> FIXED BY THIS PR IF MERGED
D-02 DECISION-SPACE ANALYSIS:              SATISFIED
D-03 CHANGE PROPAGATION:                   SATISFIED
D-04 TRUTH TYPES / RELATION AUTHORITY:     SATISFIED
D-05 DECISION LINEAGE:                     NOT SATISFIED
D-06 FUNCTION / CAPABILITY / EFFECT:       SATISFIED
D-07 UNCERTAINTY / HUMAN DECISION NEED:    SATISFIED
D-08 TECHNICAL REPLAY:                     SATISFIED
D-08 DURABLE CUSTODY:                      HUMAN DECISION REQUIRED
D-09 FALSE SUCCESS:                        SATISFIED / FINAL RECHECK REQUIRED
```

Current completion status:

```text
GINSENG D0 COMPLETION: BLOCKED

MEASURED FUNCTIONAL PROOF GAP:
D-05 DECISION LINEAGE

OPEN HUMAN-OWNED NON-FUNCTIONAL GATE:
D-08 EVIDENCE CUSTODY

RUNTIME REQUIRED TO RESOLVE CURRENT AUDIT:
NO

NEW D-06 TEST REQUIRED:
NO

NEW D-07 TEST REQUIRED:
NO
```

## 6. D-01 reconciliation boundary

The companion edit to `CREATIVE_OS.md` is current-state reconciliation only.

It may:

- replace the current Test-003 queue status with the accepted PASS state;
- replace the current handoff's stale `QUEUED / NOT EXECUTED` state;
- point the current next Ginseng step to the D0 closure gaps established by this audit.

It may not:

- rewrite historical append-only entries as if Test-003 had already passed when those entries were created;
- claim D0 completion;
- choose the D-08 custody decision;
- create or authorize D-05 proof work;
- activate Ginseng as a formal project.

## 7. Next boundary

After this record and D-01 reconciliation are separately reviewed and merged, the remaining D0 closure work is bounded to:

1. Human decision on D-08 evidence custody;
2. selection of the smallest proof path for D-05 Decision Lineage;
3. final D-09 false-success recheck after those gaps are closed.

No runtime, UI or graph-platform work is implied by this audit.