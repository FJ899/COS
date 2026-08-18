---
document: GINSENG_D0_TECHNICAL_CLOSURE_CANDIDATE
version: 1
status: TECHNICAL_CLOSURE_CANDIDATE / HUMAN_ACCEPTANCE_PENDING
owner: HUMAN_OWNS_FINAL_ACCEPTANCE
candidate: GINSENG_CANDIDATE_R0
done_scope: GINSENG_DONE_D0
prepared_at: 2026-08-19
runtime_claim: NONE
formal_project_activation: NO
project_completion_claim: NONE
---

# Ginseng D0 — Technical Closure Candidate

## 1. Boundary

This record prepares the final technical closure of the Human-frozen `GINSENG_DONE_D0` for `GINSENG_CANDIDATE_R0`.

It does not itself constitute Human acceptance, project activation, runtime authorization, release, deploy, tag, secrets, credentials, spending, or a new Ginseng capability.

Final Human acceptance remains pending even if every technical gate below is independently verified.

## 2. Exact accepted base

Repository:

`JTJ07/COS`

Accepted base before D-05 closure candidate:

`main@078b88be83ac38060dd649c51d2aafc8baaee1ea`

That accepted base already contains the Human-selected D-08 Option B durable custody for the exact Test-003 evidence bytes.

## 3. Frozen completion contract

The governing DONE definition remains:

`governance/GINSENG_DONE_D0_FREEZE_2026-08-18.md`

No D0 criterion is added, removed, weakened, or reinterpreted by this closure record.

## 4. Gate closure map

```text
D-01 AUTHORITY / CURRENT STATE COHERENCE:  SATISFIED IF THIS VERIFIED CANDIDATE ENTERS ACCEPTED HISTORY
D-02 DECISION-SPACE ANALYSIS:             SATISFIED
D-03 CHANGE PROPAGATION:                  SATISFIED
D-04 TRUTH TYPES / RELATION AUTHORITY:    SATISFIED
D-05 DECISION LINEAGE:                    SATISFIED IF VERIFIED D-05 PROOF ENTERS ACCEPTED HISTORY
D-06 FUNCTION / CAPABILITY / EFFECT:      SATISFIED
D-07 UNCERTAINTY / HUMAN DECISION NEED:   SATISFIED
D-08 DURABLE EVIDENCE / REPLAY:           SATISFIED
D-09 FALSE SUCCESS FINAL RECHECK:         PASS ONLY IF INDEPENDENT CLOSURE VERIFIER PASSES EXACT PR HEAD
```

Technical D0 closure is therefore allowed only when the exact PR head passes both:

```text
python scripts/verify_ginseng_d05_lineage.py
python scripts/verify_ginseng_d09_d0_closure.py
```

A candidate-authored PASS string is not evidence.

## 5. D-01 current-state reconciliation

Current `CREATIVE_OS.md` still contains an older handoff line stating:

`Ginseng D0: BLOCKED — D-05 DECISION LINEAGE PROOF GAP + D-08 EVIDENCE CUSTODY HUMAN DECISION`

and an older next-step sentence that still refers to resolving D-08 and selecting the D-05 proof path.

If this exact verified closure candidate enters accepted COS history, those two operational current-state statements are explicitly superseded by this later closure record because:

- D-08 Option B is already accepted on `main` with exact bytes under durable repository custody;
- D-05 has a source-bound complete Decision Lineage closure candidate verified by the dedicated fail-closed verifier;
- the next remaining boundary becomes final Human D0 acceptance, not another D-05/D-08 proof action.

Historical append-only statements remain historical and are not rewritten.

This explicit supersession is limited to Ginseng D0 current-state metadata. It does not change COS portfolio priority, project activation, or local ownership.

## 6. D-05 closure evidence

Proof object:

`governance/GINSENG_D05_DECISION_LINEAGE_PROOF_2026-08-19.json`

The proof preserves the frozen 15-field Decision Lineage minimum for `GINSENG_TEST003_DECISION_A` using only already accepted source bytes.

It does not add normative meaning, create a production decision, mutate the baseline, or require runtime capability.

D-05 is not accepted merely because this record references the proof. The dedicated D-05 verifier must pass on the exact candidate head and the proof must enter accepted history.

## 7. D-08 closure evidence

Durable evidence artifact:

`tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.zip`

Required identity:

```text
SHA-256: d9077d08012667a8a2a91e93912ee752bf991b50b5b01e4d2f80914cde315fdf
byte size: 95846
ZIP entries: 39
```

Manifest:

`tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.manifest.json`

The final D-09 verifier must recompute the archive SHA-256, byte size and ZIP entry count from repository bytes rather than trusting the manifest declaration.

## 8. Final D-09 attack set

The final closure verifier must fail closed if any of these paths exists:

1. a frozen D0 gate remains unresolved while technical closure is claimed;
2. D-05 is accepted from a candidate-authored lineage record without the dedicated verifier passing;
3. D-05 source bindings no longer match the frozen accepted evidence bytes;
4. D-08 is accepted from a digest declaration while the exact ZIP bytes are missing or differ;
5. the Test-003 result no longer reports `FALSE SUCCESS PATHS: 0`;
6. stale D-05/D-08 current-state metadata is treated as current without explicit supersession;
7. technical closure is silently promoted to Human acceptance;
8. Ginseng runtime, formal project activation or project completion is inferred from D0 technical closure;
9. the D0 contract is weakened or expanded during closure;
10. a new normative decision or production effect is introduced by the closure proof.

Any confirmed path means:

`GINSENG_D09_FINAL_RECHECK: FAIL`

and D0 remains unclosed.

## 9. Technical terminal state if exact-head verification passes

Only after exact-head CI passes may the following technical state be asserted:

```text
D-01: SATISFIED
D-02: SATISFIED
D-03: SATISFIED
D-04: SATISFIED
D-05: VERIFIED CLOSURE CANDIDATE / SATISFIED IF MERGED
D-06: SATISFIED
D-07: SATISFIED
D-08: SATISFIED
D-09: FINAL RECHECK PASS

GINSENG D0 TECHNICAL CLOSURE: PASS IF MERGED
HUMAN D0 ACCEPTANCE: PENDING
RUNTIME: NOT AUTHORIZED
FORMAL PROJECT ACTIVATION: NO
PROJECT COMPLETION CLAIM: NONE
```

## 10. Next authority boundary

If the exact PR head passes final verification, the next action is a Human-owned decision on whether to accept the verified D0 closure candidate and authorize merge.

No further functional test or runtime implementation is implied by a technical PASS.
