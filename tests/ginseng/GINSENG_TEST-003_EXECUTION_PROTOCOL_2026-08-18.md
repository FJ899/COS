---
document: GINSENG_TEST-003_EXECUTION_PROTOCOL
version: 1.1
status: PREPARATION_ONLY / NOT_EXECUTED
owner: USER
prepared_at: 2026-08-18
amended_at: 2026-08-18
candidate: GINSENG_CANDIDATE_R0
candidate_freeze_source: governance/GINSENG_CANDIDATE_R0_FREEZE_2026-08-18.md
runtime_authorized: false
test_execution_authorized: false
evidence_integrity_revision: DETACHED_AFTER_ARTIFACT_MANIFEST
---

# GINSENG TEST-003 — bounded execution protocol

## 1. Purpose

This document prepares the minimum safe and replayable execution path for the frozen `GINSENG_CANDIDATE_R0`.

It does **not** execute Test 003, implement a Ginseng runtime, activate Ginseng as a formal project, modify the frozen candidate, or claim functional completion.

The authoritative functional question remains `tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md`.

## 2. Exact authority-bound object under test

```text
candidate: GINSENG_CANDIDATE_R0
freeze status: HUMAN_ACCEPTED_CANDIDATE_FREEZE
implementation claim: NONE
runtime claim: NONE
formal project activation: NO
```

The execution must preserve the R0 ownership boundary:

- Human owns goal / DONE / normative decisions;
- Ginseng analyzes decision space, lineage, consequences, dependencies, uncertainty and Human-decision needs;
- External/Base Intelligence may perform the reasoning work used by this behavioral test;
- Saddle validates HOW against intent when a consequential path is proposed; it does not originate HOW;
- COS preserves durable high-level/cross-project state and provenance without taking local semantic ownership;
- Executor is required only if a later step performs consequential external/repository effects beyond preparation/evidence capture;
- Verifier establishes facts independently of the candidate-producing worker.

## 3. What Test 003 is proving

The test is behavioral, not a runtime-product claim.

Starting from the exact Test-2 v1.1 baseline and one test-only formal decision for `R003 / P002 / DEC002`, the candidate behavior must demonstrate that it can:

1. resolve exactly the complaints-ownership gate;
2. reduce the active blocking-gate count from `7` to `6`;
3. update only causally dependent impacts and paths;
4. preserve the other six gates semantically;
5. preserve all five Test-2 `NO_IMPACT` controls unless an explicit new causal path is proved;
6. keep `implementation_readiness = BLOCKED`;
7. keep the source baseline unchanged;
8. preserve complete provenance and replayable before/after evidence.

A hand-edited output that merely matches the expected counts is not proof.

## 4. First-run test decision

The authoritative Test-003 contract defines `VARIANT_A_KEEP_DEC002` as the default first run because it does not supersede the approved baseline decision.

The prepared fixture is:

```text
decision_id: GINSENG_TEST003_DECISION_A
scope: TEST_ONLY
variant: VARIANT_A_KEEP_DEC002
subject: R003 / P002 / DEC002
meaning:
  Preserve DEC002.
  Preserve the complaints-process owner in a distinct Customer Service function
  inside the proposed Customer Operations structure.
production_authority: NONE
```

This is a test fixture. It is not a production organizational decision and cannot modify `BASELINE_2026_07`.

## 5. Execution roles and trust separation

### A. Trusted Controller

The controller must:

- pin the exact R0 freeze record;
- verify the exact input package SHA-256 values before any reasoning call;
- verify every file in the blind-input manifest;
- unpack all inputs into a fresh temporary workspace;
- mark Test-2 v1.1 artifacts as immutable `BEFORE` evidence;
- materialize exactly one test decision fixture;
- create a new empty candidate output directory;
- create a separate controller-owned evidence directory that the candidate worker cannot write;
- record environment, timestamps, model/tool identity and all input hashes;
- prevent writes to the original input directories;
- pass only the allowed candidate inputs to the candidate worker;
- after candidate generation is complete, compute SHA-256 over the raw bytes of all six required AFTER artifacts and write `after_artifact_manifest.json` in the controller-owned evidence directory.

`after_artifact_manifest.json` is a detached integrity record. It hashes the six candidate AFTER artifacts and does **not** hash itself. Its own integrity is established by independent replay/recomputation from the saved raw bundle, not by an impossible self-referential hash.

The controller must never manufacture PASS.

### B. Candidate Worker / Base Intelligence

The worker performs a fresh full impact recalculation.

Allowed semantic inputs:

- exact blind graph input from Test 2;
- frozen R0 semantic rules required for this gate;
- the one test-only decision `GINSENG_TEST003_DECISION_A`.

The worker must not be instructed to delete one gate mechanically or to copy an expected output. It must reason from the graph and decision.

The worker may receive the Test-2 v1.1 package only as immutable `BEFORE` material required by the authoritative contract. The execution wrapper must distinguish that material from writable output and the verifier must not treat similarity to BEFORE as proof.

Required candidate outputs:

- `S001_gate_closure_report.md`;
- `S001_gate_closure_result.json`;
- `S001_gate_closure_overlay.json`;
- `S001_gate_closure_evidence.json`;
- `S001_gate_closure_source_index.json`;
- `S001_gate_closure_delta.json`.

`S001_gate_closure_evidence.json` may record SHA-256 values for the other five peer candidate artifacts, but it must not be required to contain a SHA-256 of its own final bytes. Integrity of all six candidate outputs, including the evidence file itself, is bound by the detached controller-owned `after_artifact_manifest.json`.

The worker may not create, edit or overwrite the controller-owned `after_artifact_manifest.json`.

The worker may not edit the Test-2 source package or the blind-input package.

### C. Independent Verifier

The verifier must execute in a fresh context that did not generate the candidate output.

It must calculate the verdict itself from raw artifacts and exact inputs. It must ignore any candidate-provided `PASS`, `success`, `gate_count`, `baseline_mutated`, or equivalent summary field until recomputed independently.

The verifier contract is recorded separately in `GINSENG_TEST-003_VERIFIER_CONTRACT_2026-08-18.md`.

## 6. Gate identity mapping

Test-2 v1.1 uses two naming layers. The verifier must bind them explicitly rather than compare only counts.

```text
complaints_ownership        <-> PROCESS_OWNER_GATE
reporting_model             <-> REPORTING_LINE_GATE
sod_and_privacy             <-> SOD_RODO_GATE
service_quality_capacity    <-> SERVICE_QUALITY_GATE
customer_data_ownership     <-> DATA_OWNERSHIP_GATE
crm_knowledge_continuity    <-> CRM_KNOWLEDGE_GATE
shared_kpi_catalog          <-> KPI_BASELINE_GATE
```

Expected active-gate set change for Variant A:

```text
BEFORE:
  reporting_model
  complaints_ownership
  sod_and_privacy
  service_quality_capacity
  customer_data_ownership
  crm_knowledge_continuity
  shared_kpi_catalog

AFTER:
  reporting_model
  sod_and_privacy
  service_quality_capacity
  customer_data_ownership
  crm_knowledge_continuity
  shared_kpi_catalog
```

Any second gate removal is FAIL.

## 7. Five immutable NO_IMPACT controls

The Test-2 v1.1 controls are:

```text
P003
I002
C001
A003
G003
```

Their `NO_IMPACT` meaning must remain semantically unchanged unless the candidate output proves a new path created by `GINSENG_TEST003_DECISION_A`.

For this first-run Variant A, any changed `NO_IMPACT` classification is presumptively FAIL and requires an explicit causal proof before a verifier may accept it.

## 8. Allowed and forbidden delta

### Allowed

A changed impact, path, source reference, gate record or explanation is allowed only when the candidate can provide a causal chain from the test decision through one or more of:

```text
DEC002
R003
P002
```

Downstream nodes may change only when their changed semantics are causally derived from that chain.

### Forbidden without new authority/evidence

- changing baseline nodes/relations/source facts;
- changing any unrelated gate meaning;
- changing scenario scope;
- resolving another decision;
- promoting an AI hypothesis or relation to `FACT`, `DECISION` or `CONFIRMED` without authority;
- turning six remaining blockers into `READY`;
- changing R0 ownership;
- adding runtime/UI/schema/platform claims.

## 9. Source and decision provenance

All 17 Test-2 source records must remain available and attributable.

The test-only decision must have its own provenance record and must not masquerade as an external source fact.

Minimum decision provenance:

```text
decision_id: GINSENG_TEST003_DECISION_A
decision_type: TEST_ONLY_DECISION
owner: HUMAN_TEST_CONTRACT
source_contract: tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md
variant: VARIANT_A_KEEP_DEC002
production_effect: NONE
```

The source index may therefore contain the original 17 source records plus a separately typed test-decision provenance record. A raw source-count comparison alone is not a PASS criterion.

## 10. Required raw evidence bundle

Execution evidence must contain at least:

```text
run_metadata.json
candidate_identity.json
input_manifest.json
input_hashes.json
execution_environment.json
model_or_worker_identity.json
test_decision.json
before/
  exact Test-2 v1.1 artifacts
after/
  six required candidate artifacts
controller/
  after_artifact_manifest.json
verifier/
  recomputed_metrics.json
  semantic_diff.json
  false_success_checks.json
  verifier_report.json
replay/
  replay_report.json
```

The detached `controller/after_artifact_manifest.json` must list filename and SHA-256 for exactly the six required candidate AFTER artifacts. It must be created only after candidate generation has ended and must be outside the candidate-writable output directory.

No file produced by the candidate worker may be treated as authoritative verifier evidence merely because of its filename. A candidate-supplied copy of `after_artifact_manifest.json` has no authority and must be ignored.

## 11. Replay requirement

Preparation defines two distinct notions:

1. **Evidence replay** — a fresh verifier can reconstruct the verdict from the saved inputs and outputs without process memory. This is mandatory for Test-003 PASS.
2. **Second candidate-generation run** — useful for repeatability analysis, but not automatically required by the original Test-003 contract.

A second generation run becomes mandatory before closure if the first run reveals output instability, ambiguous semantic deltas, or a false-success path that cannot be ruled out from one run plus independent replay.

This preserves the frozen Test-003 contract instead of silently adding a new product requirement.

## 12. False-success attack set

The verifier must actively attack at least these paths:

- candidate deletes `complaints_ownership` but does not resolve `DEC002/R003/P002` semantics;
- candidate reports gate count `6` while raw gate set differs;
- candidate closes two or more gates;
- candidate changes baseline and falsely reports `baseline_mutated = false`;
- candidate changes a NO_IMPACT control without a causal path;
- candidate weakens one of the remaining six gate meanings while keeping its name;
- candidate drops sources or rewrites provenance;
- candidate copies/edit-patches Test-2 output instead of recomputing a causally supported result;
- candidate creates `READY` while six blockers remain;
- candidate promotes its own relation/hypothesis to authoritative truth;
- candidate-provided PASS is trusted without independent recomputation;
- candidate attempts to supply or overwrite the detached controller-owned AFTER-artifact manifest;
- verifier relies on hidden session memory instead of the evidence bundle.

Any confirmed path is Test-003 FAIL or BLOCKED, depending on whether the failure is candidate behavior or missing evidence.

## 13. Execution outcome vocabulary

Only these terminal execution-test states are allowed:

```text
PASS
PASS_WITH_FIXES
FAIL
BLOCKED
```

`PASS_WITH_FIXES` is limited by the authoritative Test-003 contract to formatting, naming or report-completeness defects when gate logic is otherwise correct and the baseline remains intact.

`BLOCKED` is used when the required exact source, independent verifier evidence, or replayable artifact set is missing; it must never be converted to PASS by inference.

## 14. What execution preparation does not authorize

This preparation does not authorize:

- running Test 003;
- model/API spending;
- creating or using credentials/secrets;
- building a Ginseng runtime;
- building a graph platform or UI;
- merging COS PR #18;
- modifying Saddle or Executor;
- changing R0 semantics or Test-003 criteria;
- writing results to `main`;
- merging any preparation or later result PR without separate Human authority.

## 15. Prepared next boundary

After this preparation is reviewed and merged, the next separately authorized action may be:

```text
GINSENG TEST-003 EXECUTION
```

That action must use the exact input manifest, Variant A test decision and independent verifier contract prepared here. Any need for new implementation discovered during execution must stop at `BLOCKED` and be returned as a measured implementation gap rather than silently broadening the candidate.
