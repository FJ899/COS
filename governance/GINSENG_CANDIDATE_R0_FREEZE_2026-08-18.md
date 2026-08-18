---
document: GINSENG_CANDIDATE_R0_FREEZE
version: 1
status: HUMAN_ACCEPTED_CANDIDATE_FREEZE
owner: USER
accepted_at: 2026-08-18
implementation_status: NONE
runtime_status: NOT_AUTHORIZED
formal_project_activation: NO
---

# Ginseng Candidate R0 — Human Freeze Record

## 1. Human decision

The Human explicitly accepted:

`AKCEPTUJĘ GINSENG_CANDIDATE_R0 FREEZE + GOVERNANCE-ONLY RECORD PR`

This decision freezes **what is to be tested next**. It does not claim that Ginseng is implemented, functional, complete, activated as a formal project, or ready for runtime use.

## 2. Frozen candidate identity

```text
CANDIDATE: GINSENG_CANDIDATE_R0
STATUS: HUMAN_ACCEPTED_CANDIDATE_FREEZE
IMPLEMENTATION CLAIM: NONE
RUNTIME CLAIM: NONE
FORMAL PROJECT ACTIVATION: NO
```

`GINSENG_CANDIDATE_R0` is a logical, authority-bound candidate assembled from explicit source references. It is not the whole of COS PR #18, not a new runtime branch, and not a synthetic replacement for missing evidence.

## 3. Source authority map

### A. Current COS test authority

Repository: `JTJ07/COS`

Current main at freeze:

`3220310267c3d0ba2184daaf3f2adad259a9cb20`

Authoritative next functional gate:

`tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md`

Blob SHA:

`bddbfadbab36e45b73b2be3dd507e3134bb7e20e`

Status at freeze:

`QUEUED / NOT EXECUTED`

This test establishes the next missing functional question. It is not evidence that the capability already exists.

### B. Recovered exact Test-2 functional baseline

Exact recovered package:

`GINSENG_TEST_2_S001_RESULT_v1_1.zip`

SHA-256:

`4abaf4696d4c7f832c99ccd3e7586e8618c45e893f5d0e2e3ce66c97206a36be`

Exact upstream blind input:

`GINSENG_TEST_2_BLIND_INPUT(1).zip`

SHA-256:

`b0cccb8fc9be9049faaaca90f50e3983fce2540a7d449dbb2c6e99c4814ee7cf`

Recovered v1.1 package contents include:

- `S001_impact_report_test2.md`;
- `S001_scenario_branch_test2.json`;
- `S001_test2_evidence.json`;
- `S001_test2_result.json`;
- `S001_test2_source_index.json`.

The recovered baseline establishes the input state for Test 003. It does not establish Test-003 PASS.

Frozen observed baseline characteristics:

```text
impact_count: 36
blocking_gate_count: 7
no_impact_control_count: 5
baseline_mutated: false
analysis_verdict: CONDITIONAL_GO
implementation_readiness: BLOCKED
```

### C. Reusable Ginseng semantic contract

Source: COS PR #18

PR state at freeze:

`OPEN / DRAFT / UNMERGED`

Exact PR head:

`22060901523431aa86536372440e6ca0a82a8518`

Relevant contract:

`governance/GINSENG_DECISION_INTELLIGENCE_CONTRACT.md`

Blob SHA:

`a46a84820497b31d81a9f7dbcd399126510a6791`

Reusable semantic core frozen into R0:

- `GINSENG = DECISION INTELLIGENCE LAYER`;
- `FACT / DECISION / HYPOTHESIS` remain separate truth types;
- important decisions preserve Decision Lineage;
- AI cannot confirm its own proposed relation;
- relation authority preserves source / proposer / confidence / status;
- significant impact analysis can explain `ELEMENT -> FUNCTION / CAPABILITY -> EFFECT`;
- Ginseng may surface a Human Decision Gate but cannot replace the Human decision.

PR #18 itself is **not** promoted to active canon by this freeze.

### D. Later ownership correction

Source: `JTJ07/Saddle`

Observed main used for reconstruction:

`2a9aacdc0eca45f2906134a43d2eba3e8a0a7c01`

Relevant ecosystem map blob:

`e7398677ceb39b47f4e560e8f4929a0d7db67d3a`

The later ownership reconciliation classifies COS PR #18 as:

`REUSABLE GINSENG SEMANTICS + STALE/SUPERSEDED GLOBAL STATUS/PLACEMENT`

R0 therefore preserves the reusable Ginseng semantics while rejecting stale global placement and routing assumptions.

## 4. Frozen ownership boundary

`GINSENG_CANDIDATE_R0` must be interpreted under the following ownership boundary:

```text
HUMAN
  owns goal / DONE / normative decisions

GINSENG
  owns decision-space analysis, decision lineage,
  dependencies, consequences, uncertainty and Human-decision needs

EXTERNAL / BASE INTELLIGENCE
  proposes or selects HOW

SADDLE
  validates proposed HOW against intent / boundaries / invariants
  and does not originate, rank, select or route direction

COS
  preserves durable high-level / cross-project state,
  continuity, provenance and accepted cross-project state
  without becoming the owner of every component's local truth

EXECUTOR
  governs authorized consequential effects

VERIFIER
  independently establishes facts
```

Ginseng does **not** own operational HOW and does not become a command router for the ecosystem.

## 5. Explicit exclusions from R0

The following are **not** inherited into `GINSENG_CANDIDATE_R0`:

- COS PR #18 as a whole or as automatically merge-authorized canon;
- stale `ACTIVE_PRIORITY: EXECUTOR P1 / PR #32` status;
- stale Executor-specific gate ordering;
- `User -> Ginseng -> Creative OS -> ... -> Executor` as a command-control architecture;
- `Creative OS owns canon` if interpreted as global ownership over other repositories or semantic owners;
- any Ginseng capability to originate, rank, select, route or optimize operational HOW;
- a Ginseng runtime claim;
- UI, interactive graph, graph-platform or visualization implementation;
- external/CMDB import capability;
- a fixed database, JSON, SQL, API, indexing or internal module architecture;
- automatic promotion of AI hypotheses or relations to `FACT`, `DECISION` or `CONFIRMED`;
- Test 1 as independent proof of graph reasoning;
- Test 003 as executed or passed;
- any new product capability not required by a measured blocker.

## 6. Frozen next functional gate

The next functional gate for R0 is exactly:

`GINSENG_TEST-003 — SINGLE_GATE_CLOSURE / REGRESSION`

The test must start from the exact recovered Test-2 v1.1 baseline and test whether one formal decision concerning `R003 / P002 / DEC002` can:

1. resolve exactly the intended blocking gate;
2. reduce the blocking-gate count from `7` to `6`;
3. update only causally dependent impacts and paths;
4. preserve the other six gates semantically;
5. preserve all five `NO_IMPACT` controls unless an explicit new causal path exists;
6. keep `implementation_readiness = BLOCKED`;
7. keep `baseline_mutated = false`;
8. preserve complete source traceability and replayable before/after evidence.

A manually edited output that merely looks correct is not proof of this capability.

## 7. What this Human freeze authorizes

This Human decision authorizes only:

- treating `GINSENG_CANDIDATE_R0` as the single explicit object for the next Ginseng functional work;
- recording this candidate identity and authority map in a governance-only PR;
- using the exact recovered Test-2 v1.1 package as the functional baseline for the next gate;
- using the reusable semantic subset of PR #18 subject to the later Saddle ownership correction.

## 8. What this Human freeze does not authorize

It does **not** authorize:

- merging this governance PR;
- merging COS PR #18;
- activating Ginseng runtime;
- declaring Ginseng functional or complete;
- building UI or broad graph-platform capability;
- changing COS/Saddle/Executor semantic ownership;
- changing the Test-003 success criteria;
- silently replacing the recovered v1.1 source package;
- release, deployment, tag, secrets, credentials, paid services or broader external effects.

Those remain separate Human-owned decisions where applicable.

## 9. Current state after freeze

```text
GINSENG SOURCE RECOVERY: PASS
GINSENG CANDIDATE RECONSTRUCTION: PASS
GINSENG_CANDIDATE_R0: HUMAN FROZEN

SEMANTIC CORE: FROZEN FOR THIS CANDIDATE
FUNCTIONAL BASELINE: EXACT TEST-2 v1.1
NEXT FUNCTIONAL GATE: TEST-003
TEST-003 STATUS: QUEUED / NOT EXECUTED

IMPLEMENTATION: NOT CLAIMED
RUNTIME: NOT AUTHORIZED
FUNCTIONAL COMPLETION: NO
PROJECT COMPLETION: NO
```

## 10. Next decision boundary

The next phase may prepare the minimum execution path required to run Test 003 against this frozen candidate. Any implementation or runtime mutation requires its own authorized scope and may not silently broaden R0.
