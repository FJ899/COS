# ARCHITECTURE CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT — v2.1 AMENDMENT

VERSION: v2.1
STATUS: READY FOR P3 IMPLEMENTATION WHEN FROZEN BY EXACT COMMIT
ARCHITECTURE OWNER: `P2 ARCHITECTURE`
AMENDS BY ADDITION: `ARCHITECTURE CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v2.0`
EXACT FROZEN PARENT COMMIT: `6916fa5ddb78604ccbf039576a0f1165d5a8a6a1`
EXACT FROZEN PARENT FILE: `governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.0.md`
EXACT FROZEN PARENT FILE BLOB SHA: `e2e2158440939ba96cddffe9c0ac158ad07510f4`
TASK CONTRACT: `TASK CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0 @ ef128a0885310524475fba1cd291d1f34400b0cc`

> v2.1 is an additive architecture amendment. It does not overwrite, replace or silently reinterpret frozen v2.0. It narrows and makes executable the already-frozen Human-authority boundary for public/consequential Git effects. No capability promotion, merge, release, deployment or target write is authorized by this document.

---

# AMENDMENT SCOPE

Frozen v2.0 already requires exact provenance, fail-closed behavior, evidence-driven rerouting and a genuine Human authority gate for costly, public, destructive, irreversible or materially risky effects.

This amendment closes one specific execution ambiguity before any future Git `PUBLIC_EFFECT`:

```text
PUBLIC EFFECT MAY OCCUR ONLY AFTER:
1. fresh current-base identity for that exact effect;
2. positive ancestry proof;
3. exact candidate identity;
4. exact authorized diff envelope, including object metadata and candidate topology;
5. exact public-effect descriptor identity;
6. durable Human PUBLIC_EFFECT authority bound to those exact identities;
7. write-time revalidation that the bound identities are still current.

IF ANY REQUIRED IDENTITY / RELATION CANNOT BE PROVEN:
RUN STATUS: BLOCKED
EVIDENCE / VERDICT FOR THE EFFECT: UNKNOWN
TARGET WRITE: FORBIDDEN
```

This is HOW-level clarification only. It does not change `R-001` through `R-013`, `C-001` through `C-009`, `AC-001` through `AC-011`, the Human-owned goal/DONE, or the starting status `CAP-ITO-001 = PROPOSED`.

## PROSPECTIVE EFFECT

This amendment is prospective for effects claiming v2.1 compliance.

Earlier implementation/evidence created against frozen v2.0 remains historical evidence against its frozen input. Architecture prose must not retroactively manufacture either compliance or non-compliance for prior actions; P4 evaluates exact historical evidence against the exact frozen inputs applicable to that evidence.

Any new target public effect after the v2.1 freeze must satisfy this amendment.

---

# TERMINOLOGY AND IDENTITIES

For one attempted public effect `X`:

```text
S_FROZEN
  exact workload/source commit frozen before material execution

B_PRE_X
  freshly observed exact head SHA of the intended current base branch
  for this exact public-effect attempt

C_PRE_X
  exact candidate commit SHA intended to be made public by this effect

D_PRE_X
  exact canonical authorized diff manifest for B_PRE_X -> C_PRE_X

D_HASH_X
  SHA-256 of canonical D_PRE_X bytes

E_PRE_X
  exact canonical public-effect descriptor for this effect

E_HASH_X
  SHA-256 of canonical E_PRE_X bytes

H_AUTH_X
  durable Human decision evidence authorizing this exact PUBLIC_EFFECT tuple
```

A branch name, PR number, prose description, cached earlier SHA, visually similar patch or matching final file text is not a substitute for an exact identity.

## PUBLIC_EFFECT IN THIS AMENDMENT

At minimum the following GitHub writes are `PUBLIC_EFFECT`:

```text
PUSH_CANDIDATE_REF
  creation or update of a remote candidate branch/ref

CREATE_OR_UPDATE_PR
  creation of a pull request or a material update that publishes/changes
  its exact head/base relation or candidate scope
```

Merge, release, deployment, force-push, destructive rewrite and other consequential effects remain separately governed by the frozen Human authority boundary. This amendment does not authorize them.

---

# AD-V2.1-001 — FRESH EXACT PUBLIC-EFFECT AUTHORITY GATE

**Requirement:** R-005, R-006, R-008, R-010, R-011, R-013; C-002, C-004, C-008.

**Decision:** Before each Git `PUBLIC_EFFECT`, Projector/P3 must establish a fresh exact current-base identity, positively prove the required ancestry and exact candidate/diff identity, construct an exact effect descriptor, and stop at a genuine Human-owned `PUBLIC_EFFECT` gate whose durable decision record binds the exact base/candidate/diff-manifest/effect hashes. The target write may occur only while those exact identities remain current.

No ambient, earlier or prose-only approval may authorize a changed base, candidate, diff envelope, effect descriptor or later public effect.

## 1. BASE-RELATION CASES

The relation classified here is specifically `S_FROZEN -> B_PRE_X`. It is not inferred from branch names and it is not a colloquial description of the candidate branch graph.

### CASE 1 — CURRENT_BASE_EQUALS_FROZEN_SOURCE

```text
B_PRE_X == S_FROZEN
```

The current base has not advanced from the exact frozen source for this effect attempt.

This case does not remove any other gate. Candidate ancestry, diff envelope, Human authority and write-time revalidation are still required.

### CASE 2 — CURRENT_BASE_ADVANCED_FROM_FROZEN_SOURCE

```text
B_PRE_X != S_FROZEN
AND
ANCESTRY(S_FROZEN, B_PRE_X) == PROVEN_ANCESTOR
```

The required classification name is:

```text
CURRENT_BASE_ADVANCED_FROM_FROZEN_SOURCE
```

Do **not** label this case Git `diverged`.

The proven fact is that the current base advanced from the frozen source. Whether the candidate is or is not topologically compatible with that newer base is a separate proof obligation.

For Case 2, a candidate created only from the older frozen source is not eligible for target write merely because its file-level patch still looks correct. Before any public effect, P3 must positively prove:

```text
ANCESTRY(B_PRE_X, C_PRE_X) == PROVEN_ANCESTOR
```

and must compute/verify the authorized diff envelope from the fresh `B_PRE_X` to the exact `C_PRE_X`.

If that relation cannot be proven, the public-effect attempt is `BLOCKED + UNKNOWN`; no target write occurs. Any later candidate preparation is a new implementation/evidence step and must return through the full fresh public-effect gate.

## 2. FRESH CURRENT-BASE IDENTITY PER PUBLIC EFFECT

Fresh current-base identity is required separately for every public effect.

### B_PRE_PUSH

Immediately before the Human gate for `PUSH_CANDIDATE_REF`, P3 must freshly observe and freeze:

```text
B_PRE_PUSH = exact current head SHA of the intended PR/base branch
```

`S_FROZEN`, an earlier reconnaissance SHA, or an earlier pre-run freeze is not a substitute for `B_PRE_PUSH`.

### B_PRE_PR

Immediately before the Human gate for `CREATE_OR_UPDATE_PR`, P3 must freshly observe and freeze:

```text
B_PRE_PR = exact current head SHA of the intended PR/base branch
```

`B_PRE_PUSH` is not a substitute for `B_PRE_PR`.

The base may advance after the candidate push and before PR creation/update. Therefore:

```text
B_PRE_PR MAY == B_PRE_PUSH
B_PRE_PR MAY != B_PRE_PUSH
```

If it differs, P3 must reclassify the base relation, re-prove ancestry, recompute the diff manifest and effect descriptor, and obtain Human authority bound to the new exact tuple before the PR effect.

## 3. HUMAN PUBLIC_EFFECT AUTHORITY BINDS EXACT IDENTITIES

A valid Human authority record for a public effect must be classified under the existing v2.0 Human-owned gate model as:

```text
human_intervention.classification = GENUINE_HUMAN_OWNED_GATE
human_intervention.authority_basis = PUBLIC_EFFECT
```

and must durably bind at minimum:

```text
effect_kind
repository
base_ref
S_FROZEN
B_PRE_X
base_relation
C_PRE_X
D_HASH_X
E_HASH_X
human_decision_evidence_ref
```

The approval is valid only for the exact tuple it binds.

```text
CHANGE IN B_PRE_X -> OLD AUTHORITY INVALID
CHANGE IN C_PRE_X -> OLD AUTHORITY INVALID
CHANGE IN D_HASH_X -> OLD AUTHORITY INVALID
CHANGE IN E_HASH_X -> OLD AUTHORITY INVALID
CHANGE IN EFFECT KIND / TARGET REF -> OLD AUTHORITY INVALID
```

A Human decision artifact may authorize more than one public effect only if it explicitly enumerates each distinct effect tuple/hash. A generic statement such as `publish this`, `push it`, `open the PR`, or approval of a previous effect does not authorize a later changed tuple.

This exact binding preserves genuine Human authority without turning the Human into the routine router/decomposer. P3 owns the evidence gathering, ancestry proof, manifest construction and blocker handling before presenting the bounded authority gate.

## 4. AUTHORIZED DIFF ENVELOPE

Authorization is not based on patch text or changed path names alone.

`D_PRE_X` must be a deterministic manifest that covers both content identity and Git object/topology identity.

At minimum:

```text
schema_version
repository
S_FROZEN
B_PRE_X
C_PRE_X
base_relation
merge_base_sha
ancestry_proof_ref_or_identity
candidate_commit_topology
changed_entries[]
```

### Per-entry identity

Each changed entry must include enough information to detect content, executable-bit, symlink, submodule/object-type, deletion/addition and rename differences:

```text
path
previous_path or null
change_kind

base_object:
  object_id or null
  object_type or null
  git_mode or null

candidate_object:
  object_id or null
  object_type or null
  git_mode or null
```

For ordinary files, `object_id` is the exact Git blob identity. For Git object classes where the entry is not an ordinary file blob, the manifest must preserve the actual object type and object identity.

A change in Git mode or object type is a change in the authorized envelope even when file bytes are identical.

### Candidate commit topology

The diff envelope must also bind the exact candidate commit topology, not only the final tree.

At minimum:

```text
candidate_head_sha
candidate_head_tree_sha
candidate_commits[]:
  commit_sha
  tree_sha
  ordered_parent_shas[]
```

`candidate_commits[]` covers the commits on the candidate path that are part of the proposed `B_PRE_X -> C_PRE_X` effect envelope. A different commit graph, different parentage, added merge commit, substituted commit or same-tree/different-history candidate creates a different envelope and requires a new `D_HASH_X` and Human authority.

### Canonical manifest identity

`D_HASH_X` must be computed as SHA-256 over deterministic canonical UTF-8 JSON bytes with:

```text
object keys sorted lexicographically
array order preserved by the schema-defined deterministic ordering
no insignificant whitespace
UTF-8 encoding
```

P3 must preserve the canonical manifest artifact itself in addition to its hash.

## 5. PUBLIC-EFFECT DESCRIPTOR IDENTITY

`E_PRE_X` describes the exact write that the Human is authorizing.

At minimum:

```text
schema_version
effect_kind
repository
base_ref
candidate_ref_or_pr_head
S_FROZEN
B_PRE_X
C_PRE_X
D_HASH_X
expected_public_result
```

Effect-specific fields may include the expected remote candidate ref before/after the push or the intended PR head/base identities. The descriptor must be precise enough that a materially different public write produces a different `E_HASH_X`.

`E_HASH_X` uses the same deterministic canonical UTF-8 JSON + SHA-256 rule as `D_HASH_X`.

The Human authority record binds `E_HASH_X`, not merely a human-readable effect description.

## 6. WRITE-TIME REVALIDATION / TOCTOU RULE

Human authority is necessary but not sufficient if the target state changed after the authority evidence was created.

Immediately before invoking the external target-write operation, P3 must re-observe the relevant target identities and prove that the write still matches the Human-bound tuple.

At minimum:

```text
current base SHA == authorized B_PRE_X
candidate SHA == authorized C_PRE_X
diff manifest hash == authorized D_HASH_X
effect descriptor hash == authorized E_HASH_X
```

If any equality cannot be positively proven, the authority is stale for that attempt.

Required behavior:

```text
status = BLOCKED
effect_evidence_status = UNKNOWN
target_write_performed = false
next route = re-observe -> recompute -> re-authorize, or truthful blocker
```

The system must not write first and reconcile provenance afterward.

## 7. FAIL-CLOSED UNKNOWN RULE

The following are examples of insufficient proof and therefore force `BLOCKED + UNKNOWN` before target write:

- current base SHA cannot be freshly retrieved;
- `S_FROZEN -> B_PRE_X` ancestry cannot be positively proven;
- `B_PRE_X -> C_PRE_X` ancestry required for the effect cannot be positively proven;
- merge base cannot be established where required by the manifest;
- any changed entry lacks exact base/candidate object identity, Git mode or object type;
- candidate commit topology is incomplete or ambiguous;
- the canonical diff manifest cannot be reproduced exactly;
- candidate head changed after manifest construction;
- current base changed after manifest construction or Human authority;
- Human authority does not bind the exact required hashes;
- effect descriptor cannot be reproduced exactly at write time.

No fallback to branch-name similarity, patch-text similarity, prose confidence, cached screenshots or best-effort Git inference is allowed.

`UNKNOWN` is not upgraded to `PASS` because the intended change is small, tests pass, or a previous candidate looked equivalent.

---

# PUBLIC-EFFECT STATE / EVIDENCE RECORD

P3 must preserve a durable record for each attempted public effect. An additive structure is sufficient; no new service/database is authorized.

Minimum logical fields:

```text
public_effect_gate:
  effect_kind
  repository
  base_ref
  frozen_source_sha
  fresh_base_sha
  base_relation
  candidate_sha
  ancestry_evidence_refs[]
  diff_manifest_ref
  diff_manifest_sha256
  effect_descriptor_ref
  effect_sha256
  human_authority_evidence_ref
  authority_classification: GENUINE_HUMAN_OWNED_GATE
  authority_basis: PUBLIC_EFFECT
  write_time_revalidation: PASS | UNKNOWN
  write_performed: true | false
  write_result_ref: <exact durable evidence> | null
```

When blocked before write:

```text
run status: BLOCKED
public effect evidence state: UNKNOWN
target write result: NOT CREATED
```

When a write is actually executed after the complete gate, the resulting remote identity must be preserved exactly and must match the authorized effect expectation or become new material evidence requiring state update/reroute/block.

---

# REQUIRED P3 VERIFICATION

P3 must add executable verification demonstrating at least:

1. `CASE 1 — CURRENT_BASE_EQUALS_FROZEN_SOURCE` is accepted only when all remaining exact gates pass.
2. `CASE 2 — CURRENT_BASE_ADVANCED_FROM_FROZEN_SOURCE` is classified with that exact semantic meaning and is not labeled Git `diverged`.
3. `B_PRE_PUSH` and `B_PRE_PR` are independently fresh; a base advance between push and PR invalidates reuse of the push tuple.
4. Human `PUBLIC_EFFECT` authority rejects any changed base SHA, candidate SHA, `D_HASH`, `E_HASH`, target ref or effect kind.
5. A mode-only change creates a different diff envelope.
6. An object-type change creates a different diff envelope.
7. A candidate-topology change creates a different diff envelope even when the final tree/file bytes are identical.
8. Unknown/unavailable base identity, ancestry or diff identity produces `BLOCKED + UNKNOWN` and invokes zero target writes.
9. A write-time base/candidate/manifest/effect mismatch after Human authorization produces `BLOCKED + UNKNOWN` and invokes zero target writes.
10. A successful allowed write path preserves the exact authority/effect/result evidence without granting merge, release, deployment or capability-promotion authority.

Tests must use a fake/mocked write sink or another bounded non-public harness for failure-path proof. P3 must not create real target writes merely to prove that blocked paths do not write.

---

# INVARIANTS ADDED BY v2.1

1. Every public effect has its own fresh current-base identity.
2. `B_PRE_PUSH` never silently substitutes for `B_PRE_PR`.
3. Case 2 means `CURRENT_BASE_ADVANCED_FROM_FROZEN_SOURCE`; it does not assert Git `diverged`.
4. Public-effect authority is exact-hash authority, not ambient conversational permission.
5. Diff authorization covers content blobs, Git modes/object types and candidate commit topology.
6. Same bytes with different Git mode/object type are not the same authorized diff envelope.
7. Same final tree with different candidate commit topology is not the same authorized diff envelope.
8. Human authority becomes stale when any bound identity changes.
9. Unproven base/ancestry/diff identity is `BLOCKED + UNKNOWN` before any target write.
10. Target write is never used as an evidence-seeking probe for an unknown authorization state.
11. A successful push does not authorize PR creation/update; the PR effect gets its own fresh base and exact gate.
12. A successful PR effect does not authorize merge/release/deployment.
13. v2.1 does not promote `CAP-ITO-001` and does not create Human final acceptance.

---

# IMPLEMENTATION BOUNDARIES

## MUST

- preserve frozen v2.0 unchanged;
- treat this amendment as an additive frozen P2 input;
- implement `AD-V2.1-001` without creating a new planner/runtime/platform;
- obtain fresh `B_PRE_PUSH` for a push effect and fresh `B_PRE_PR` for a PR effect;
- positively prove required ancestry before target write;
- bind exact candidate commit and candidate topology;
- construct and preserve deterministic diff/effect manifests and hashes;
- stop at exact Human `PUBLIC_EFFECT` authority before the write;
- revalidate the bound identities immediately before target write;
- produce `BLOCKED + UNKNOWN` with zero target writes when required identity is unproven;
- preserve exact evidence of any successful authorized effect;
- keep `CAP-ITO-001` no higher than exact evidence supports.

## MUST NOT

- overwrite or edit `governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v2.0.md`;
- call Case 2 Git `diverged` merely because the current base is newer than the frozen source;
- reuse `B_PRE_PUSH` as `B_PRE_PR` without a fresh observation;
- treat changed path names or patch text alone as the authorized diff envelope;
- omit Git mode/object type or candidate topology from the authorization identity;
- use generic Human approval for a changed exact effect tuple;
- perform a target write when base, ancestry, candidate, diff or effect identity is `UNKNOWN`;
- auto-rebase, merge, force-push, republish or otherwise mutate a target as a substitute for exact proof;
- merge, release, deploy, promote capability or manufacture Human final acceptance under authority of this amendment.

---

# RELATION TO EXISTING P3 HISTORY

Existing P3 implementation history created from frozen v2.0 is not rewritten by this amendment.

v2.1 does not require P2 to merge/rebase existing P3 commits in order to freeze architecture. P3 may continue implementation history only by new commits and exact provenance references; no history rewrite is implied.

Before any future target public effect claims v2.1 compliance, P3 must demonstrate the required executable checks and freeze the exact implementation/evidence identity that implements this amendment.

Existing v2.0 evidence remains separately identifiable. It must not be silently relabeled as v2.1 evidence merely because v2.1 exists.

---

# CAPABILITY / ACCEPTANCE STATE

```text
CAP-ITO-001: PROPOSED
CAPABILITY PROMOTION BY v2.1: NONE
P4 AUDIT OF v2.1 IMPLEMENTATION: NOT YET AUDITED
HUMAN FINAL ACCEPTANCE: NOT YET CREATED
MERGE AUTHORITY: NOT GRANTED
RELEASE / DEPLOY AUTHORITY: NOT GRANTED
TARGET PUBLIC-EFFECT AUTHORITY: PER-EFFECT HUMAN GATE ONLY
```

---

# FREEZE / HANDOFF CONDITION

This amendment may be handed to P3 only after this exact file is frozen by a Git commit whose parent is exactly:

```text
6916fa5ddb78604ccbf039576a0f1165d5a8a6a1
```

The v2.1 commit identity is recorded externally in the P2 -> P3 handoff because a Git commit cannot self-embed its own SHA.

The freeze itself performs no target write and grants no target-write authority.

```text
HANDOFF -> P3 IMPLEMENTATION

INPUTS:
TASK CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0
  @ ef128a0885310524475fba1cd291d1f34400b0cc

ARCHITECTURE CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v2.0
  @ 6916fa5ddb78604ccbf039576a0f1165d5a8a6a1

ARCHITECTURE CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v2.1 AMENDMENT
  @ supplied in external freeze/handoff record

IMPLEMENTATION REPOSITORY:
  FJ899/COS

IMPLEMENTATION CONTINUATION:
  preserve existing P3 history; new commits only; no history rewrite implied

PURPOSE:
  Implement and prove AD-V2.1-001 before any future target PUBLIC_EFFECT.
  Preserve WHAT, preserve Human authority, fail closed on UNKNOWN identity,
  and do not promote CAP-ITO-001 by architecture or code existence.
```
