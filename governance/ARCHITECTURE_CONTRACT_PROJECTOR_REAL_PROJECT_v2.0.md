# ARCHITECTURE CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT

VERSION: v2.0
STATUS: READY FOR P3 IMPLEMENTATION
BASED ON TASK CONTRACT: `TASK CONTRACT — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0`
ARCHITECTURE OWNER: `P2 ARCHITECTURE`

> Version v2.0 is a fresh architecture derivation from the revalidated frozen P1 state. A repository branch named `arch/projector-real-project-v1` exists, but the current Human revalidation explicitly states that no prior Architecture Contract is current. That branch and its decisions are therefore not an input to this contract. v2.0 avoids overwriting repository history and does not inherit prior AD or OQ numbering.

---

# SOURCE / REPO IDENTITY

```text
REPOSITORY: FJ899/COS

CURRENT STATE BASELINE:
  VERSION: v1.0
  FILE: governance/CURRENT_STATE_BASELINE_PROJECTOR_REAL_PROJECT_v1.0.md
  P1 FROZEN COMMIT: ef128a0885310524475fba1cd291d1f34400b0cc
  FILE BLOB SHA: 29de6c30c97dd13ca57069b765195290a175297f

TASK CONTRACT:
  VERSION: v1.0
  FILE: governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md
  BRANCH: spec/projector-real-project-v1
  FROZEN COMMIT: ef128a0885310524475fba1cd291d1f34400b0cc
  FILE BLOB SHA: b75045bb1b83fffdee87a4cb697c289f82f29655

SOURCE TECHNICAL BASELINE:
  BRANCH: main
  SHA: bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19

P2 ARCHITECTURE BRANCH:
  arch/projector-real-project-v2

P2 ARCHITECTURE BASE:
  ef128a0885310524475fba1cd291d1f34400b0cc

P3 IMPLEMENTATION REPOSITORY:
  FJ899/COS

P3 IMPLEMENTATION BASE:
  exact commit containing this frozen Architecture Contract v2.0
  (recorded externally in the P2 -> P3 handoff because a Git commit cannot self-embed its own identity)

P3 IMPLEMENTATION BRANCH:
  impl/projector-real-project-v2
```

## PROVENANCE STATE AT ARCHITECTURE FREEZE

```text
REQUIREMENT OWNER: P1 SPECIFICATION under Human-owned intent
TASK CONTRACT: v1.0 @ ef128a0885310524475fba1cd291d1f34400b0cc
ARCHITECTURE DECISION OWNER: P2 ARCHITECTURE
ARCHITECTURE CONTRACT: v2.0
IMPLEMENTATION OWNER: P3 IMPLEMENTATION
IMPLEMENTATION IDENTITY: NOT YET IMPLEMENTED
EVIDENCE PACKAGE: NOT YET CREATED
INDEPENDENT VERIFIER: P4 INDEPENDENT AUDIT
P4 AUDIT: NOT YET AUDITED
HUMAN FINAL ACCEPTANCE: NOT YET CREATED
```

---

# CURRENT STATE

Reconnaissance was performed against the exact frozen P1 input and `main@bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19`.

Established facts:

1. `CAP-ITO-001` is `PROPOSED`.
2. Its registry entry has no registered implementation, executable evidence, failure evidence, integration evidence, real-work evidence or reliability evidence.
3. No Projector implementation/runtime is present on the technical baseline.
4. Existing relevant COS mechanisms are governance/evidence mechanisms, not Projector product behavior:
   - `governance/CAPABILITY_REGISTRY.json`;
   - `scripts/verify_capability_evidence.py`;
   - `tests/capability/test_capability_registry_gate.py`;
   - `.github/workflows/verify-creative-os.yml` using Python 3.11 and `unittest`;
   - durable continuity/provenance artifacts and cold-start tests.
5. Historical Projector research exists under `research/history/projector-radar-2026-08-21_23/`. It is evidence about observed pressure/failure modes only. It is not current implementation authority and does not prove `CAP-ITO-001`.
6. Historical observations establish useful pressure for this design:
   - a high-sensitivity KYC step correctly became a Human authority gate instead of being silently crossed;
   - new evidence caused a channel reroute while preserving the same goal;
   - current-state/recovery drift is a confirmed recurring failure class;
   - a real problem can still be a bad validation workload if HOW is already known, implementation is blocked, feedback is slow, or DONE is not externally observable.
7. The current technical baseline already has a small Python/CI verification path. No database, workflow engine, server, scheduler or agent framework is established as necessary.

## EXISTING TEST COVERAGE

```text
CAP-GATE-001: TESTED
CAP-ITO-001: PROPOSED
PROJECTOR UNIT TESTS: NOT YET CREATED
PROJECTOR FAILURE TESTS: NOT YET CREATED
PROJECTOR RECOVERY TEST: NOT YET CREATED
PROJECTOR INTEGRATION REPLAY: NOT YET CREATED
PROJECTOR REAL-WORK PROOF: NOT YET CREATED
PROJECTOR P4 AUDIT: NOT YET AUDITED
```

## KNOWN FAILURE MODES

- architecture/documentation mistaken for capability;
- rough intent silently narrowed into a convenient local task;
- goal/DONE silently replaced downstream;
- facts, assumptions, claims and unknowns collapsed into one narrative;
- stale route continued after invalidating evidence;
- Human operational routing hidden as autonomous success;
- genuine Human authority bypassed in the name of autonomy;
- current-state drift across sessions;
- mutable state losing transition history;
- missing or ambiguous exact artifact identity;
- fabricated/hardcoded DONE;
- capability registry promoted beyond evidence;
- a self-hosted Projector-building exercise used as circular real-work proof.

---

# ARCHITECTURE GOAL

Create the smallest executable Projector vertical slice that makes the existing Intelligence-to-work path durable, inspectable and fail-closed without creating a new autonomous platform.

The target runtime shape is:

```text
ROUGH HUMAN INTENT
        |
        v
EXISTING INTELLIGENCE
bind target / preserve Human meaning / choose evidence-seeking move
        |
        v
PROJECTOR RUN RECORDER + TRANSITION VERIFIER
(single stdlib Python executable)
        |
        v
DURABLE RUN BUNDLE
immutable intent/provenance + chained state snapshots + evidence references
        |
        +--------------------+
        |                    |
        v                    v
ROUTINE REVERSIBLE WORK   HUMAN AUTHORITY GATE
using whatever tool/path   only where Human owns decision
is naturally useful
        |                    |
        +---------+----------+
                  v
              EVIDENCE
                  |
                  v
        STATE UPDATE / REROUTE / BLOCK
                  |
                  v
        EFFECT-BASED DONE VERIFICATION
                  |
                  v
            P4 INDEPENDENT AUDIT
                  |
                  v
          HUMAN FINAL ACCEPTANCE
```

The Projector executable is not the intelligence/planner. It is the durable state, transition-integrity and provenance boundary around work performed by the existing Intelligence and available tools.

---

# REQUIREMENT -> MECHANISM MAP

| Requirement | Required mechanism |
|---|---|
| R-001 | An executable run recorder/verifier plus an actual bounded end-to-end real-work run. Architecture files and schemas alone never count. |
| R-002 | Human-facing entry remains rough natural-language intent through existing Intelligence. The system-generated binding is durably recorded; the Human is not asked to choose toolchain/repository/runtime. |
| R-003 | Immutable raw-intent anchor plus goal/DONE lineage. Goal or DONE may change only through an explicit Human-owned goal-change transition with durable Human-decision evidence. |
| R-004 | Every durable state snapshot contains observed facts, assumptions, claims, unknowns, one current critical unknown/blocker, evidence references and the next justified move or gate. |
| R-005 | Every next move records its evidence basis and route identity. Material evidence that invalidates a route mechanically requires a new route or truthful `BLOCKED`; a fixed component pipeline is forbidden. |
| R-006 | Every material Human intervention is recorded as `GENUINE_HUMAN_OWNED_GATE` or `HUMAN_OPERATIONAL_RESCUE`. Risk/authority gates cannot be crossed without Human decision evidence. |
| R-007 | A Human-selected bounded validation workload is mandatory before real-work proof. `DONE` requires workload-external effect evidence and a predefined verification method, not Projector build artifacts. |
| R-008 | Executable failure/interruption tests must demonstrate truthful reject/block/recover/reroute behavior for invalid route evidence, missing/corrupt durable state or a failed dependency/input case. |
| R-009 | Reuse the existing capability registry and evidence gate. `CAP-ITO-001` status may move only when the exact evidence package supports it; architecture/code existence alone causes no promotion. |
| R-010 | Store the run as durable repository/filesystem artifacts that a fresh process/actor can validate and recover without chat memory. State history is append-only/chained rather than overwritten. |
| R-011 | Bind Task Contract, Architecture Contract, implementation SHA, state/evidence identities and later P4 finding IDs in a provenance manifest/matrix. Not-yet-completed stages remain explicit. |
| R-012 | P3 produces evidence, not a final compliance verdict. P4 receives frozen inputs and fills requirement-level findings independently. |
| R-013 | Human acceptance is a separate post-P4 artifact/state. No Projector/P3 command may manufacture `ACCEPTED`, release or deployment authority. |

---

# BOUNDED VALIDATION WORKLOAD DETERMINATION

A bounded validation workload **is required** because R-007 and its acceptance criterion require a real effect-based outcome outside Projector build artifacts.

The exact workload is not selected by P2 because it is Human-owned intent. P2 defines only admissibility constraints:

```text
VALID WORKLOAD MUST HAVE:
- a genuine Human-owned goal;
- a predefined effect-based DONE outside Projector source/docs;
- a verification method known before the run;
- an actionable path under available authority/resources;
- enough uncertainty/nontrivial HOW that Projector behavior is meaningfully exercised;
- observable external feedback or independently reproducible effect;
- bounded scope suitable for one first real-work proof.

REJECT AS FIRST VALIDATION WORKLOAD IF:
- DONE is merely architecture/code/repository/document completion;
- the key HOW is already resolved and no meaningful uncertain path remains;
- implementation/effect is unavailable to the current actors;
- success depends primarily on an unavailable external owner;
- there is no realistic observable effect loop;
- the workload would make the Human the routine router/decomposer/recovery mechanism.
```

This selection blocks the **real-work validation execution**, not the P2 architecture freeze or P3 core implementation.

---

# ARCHITECTURE DECISIONS

## AD-V2-001 — SAME-REPOSITORY, NO-NEW-PLATFORM IMPLEMENTATION

**Requirement:** R-001, R-009, R-011; C-004, C-005, C-006.

**Decision:** Implement the first Projector vertical slice in `FJ899/COS`, based on the exact frozen P2 commit, using Python 3.11 standard library and the existing GitHub Actions verification workflow. Do not create another repository, service, database, workflow engine, scheduler, agent platform or external runtime dependency.

**Mechanism:**

```text
IMPLEMENTATION: scripts/projector_run.py
TESTS: tests/projector/
RUN ARTIFACTS: projector/runs/<run-id>/
CI: extend .github/workflows/verify-creative-os.yml
```

**Why:** The repository already owns the capability registry, provenance/governance state and CI verification path. No observed requirement needs another deployment boundary.

**Alternatives:** separate Projector repository; hosted service; database-backed application; new agent runtime.

**Rejected:** All add an unproven operational/deployment boundary and make provenance harder without satisfying a requirement unavailable in the current repo.

**Trade-offs:** Tighter coupling to COS repository conventions, but lower implementation surface and stronger exact provenance.

**Risks:** A monolithic script can become overgrown if future use expands; that is intentionally deferred until repeated real use justifies abstraction.

**Evidence expected:** exact implementation SHA; file identities; Python 3.11 CI pass; no undeclared external dependency.

---

## AD-V2-002 — EXISTING INTELLIGENCE IS THE REASONING SURFACE; PROJECTOR IS THE EXECUTABLE STATE/INTEGRITY BOUNDARY

**Requirement:** R-002, R-005, R-006; C-005, C-006, C-007.

**Decision:** Do not implement a new planner/router/agent. Existing Intelligence receives rough Human intent, derives a bounded target, chooses evidence-seeking/productive moves and uses whatever existing tool is naturally useful. Projector executable code records and validates those decisions and their durable consequences.

**Mechanism:** Human-facing interaction remains natural language. The executable receives machine-readable init/transition inputs produced by the Intelligence/tool layer and writes only validated durable state.

**Why:** The frozen P1 run contract explicitly places evidence-seeking progress on existing Intelligence and states that a central Projector runtime is not pre-authorized. Historical research also found central runtime need `NOT ESTABLISHED`.

**Alternatives:** deterministic fixed workflow; master router; multi-agent supervisor; fully narrative/manual record.

**Rejected:** Fixed workflow violates R-005; central autonomous layers lack observed necessity; manual narrative alone cannot provide executable fail-closed evidence.

**Trade-offs:** Reasoning quality remains dependent on the existing Intelligence and cannot be proven by deterministic unit tests alone. That is why controlled integration replay plus real-work evidence and P4 audit are required.

**Risks:** Intelligence may emit a plausible but unjustified next move. The recorder cannot prove semantic optimality; it can only require explicit evidence basis and preserve the decision for P4.

**Evidence expected:** raw Human input, resulting system-bound target, next-move records with evidence basis, and real-run behavior without hidden Human routing.

---

## AD-V2-003 — APPEND-ONLY RUN BUNDLE WITH CHAINED STATE SNAPSHOTS

**Requirement:** R-003, R-004, R-010, R-011.

**Decision:** Represent each run as an immutable run manifest plus append-only numbered state snapshots. Do not use a mutable single current-state file as the sole source of truth.

**Mechanism:**

```text
projector/runs/<run-id>/
  run.json
  states/
    0000.json
    0001.json
    0002.json
    ...
```

`run.json` is created once and contains at minimum:

```text
schema_version
run_id
created_at
raw_human_intent
initial_binding:
  bounded_target
  goal
  done
  verification_method
  current_critical_unknown
  assumptions
  known_human_authority_gates
provenance:
  task_contract identity/version
  architecture_contract identity/version
  implementation repository/branch/SHA
```

Each state snapshot contains at minimum:

```text
schema_version
run_id
sequence
previous_state_sha256
current_goal
current_done
observed_facts[]
assumptions[]
claims[]
unknowns[]
critical_unknown_or_blocker
material_evidence_refs[]
route:
  route_id
  next_move_kind
  description
  justification
  evidence_basis[]
human_intervention
route_change
transition_reason
status: ACTIVE | BLOCKED | DONE
```

The executable writes a new state atomically only after validating the complete chain and proposed transition.

**Why:** Current-state drift and provenance loss are observed failure classes; a chained append-only history makes silent mutation detectable and cold-start recovery deterministic.

**Alternatives:** one mutable JSON file; database/event service; prose-only handoff files.

**Rejected:** Mutable single state loses lineage; database is unnecessary; prose-only state cannot be mechanically validated.

**Trade-offs:** More files per run and some duplicated current-state fields, in exchange for simple reviewable history and no persistence service.

**Risks:** Manual edits can still corrupt the chain; verifier must fail closed and require repair/new evidence, never silently recompute history.

**Evidence expected:** recovery test in a fresh process/temp directory; tamper/broken-chain failure test; exact snapshot hashes.

---

## AD-V2-004 — INTENT ANCHOR AND HUMAN-ONLY GOAL/DONE CHANGE

**Requirement:** R-003, R-013.

**Decision:** Raw Human intent and initial binding are immutable. `current_goal` and `current_done` must remain lineage-equivalent unless a transition explicitly carries a Human-owned goal/DONE change with durable Human-decision evidence.

**Mechanism:** `scripts/projector_run.py transition` rejects a changed goal/DONE unless the proposed transition contains:

```text
goal_change.type = HUMAN_GOAL_CHANGE
goal_change.human_decision_evidence_ref = <durable evidence id>
goal_change.new_goal / new_done
```

A routine system optimization, implementation convenience or Human operational suggestion cannot satisfy this gate.

**Why:** Silent goal substitution is a direct Task Contract failure and cannot be repaired by later prose.

**Alternatives:** free mutation of state; goal hash only without lineage event; requiring Human confirmation on every step.

**Rejected:** Free mutation enables drift; hash-only detects but does not explain authorized changes; repeated confirmation would turn Human into runtime orchestration.

**Trade-offs:** Explicit goal changes create more durable records but preserve Human semantic authority.

**Risks:** Semantic drift can occur without textually changing the goal. P4 must therefore inspect material transitions; the executable only enforces the mechanical boundary.

**Evidence expected:** test that silent goal/DONE change fails; test that explicit Human-owned goal change preserves complete lineage; P4 zero silent substitutions.

---

## AD-V2-005 — EVIDENCE-BASED ROUTE TRANSITIONS, NOT A FIXED COMPONENT PIPELINE

**Requirement:** R-004, R-005, R-008.

**Decision:** A next move is a state property justified by current evidence, not a stage in a predetermined pipeline. Every material evidence change explicitly declares whether it invalidates the current route.

**Mechanism:** Each transition contains:

```text
material_evidence_change:
  evidence_refs[]
  invalidates_current_route: true | false
```

If `invalidates_current_route = true`, the next accepted snapshot must either:

```text
- use a new route_id with a new evidence-based next move; or
- set status = BLOCKED with the truthful blocker.
```

Continuing the old route silently is rejected by the executable verifier.

**Why:** Historical evidence includes an actual KYC authority gate followed by a channel reroute while preserving the goal. R-005 directly requires this behavior.

**Alternatives:** fixed planner stages; advisory reroute prose with no enforceable record.

**Rejected:** Fixed stages violate the contract; advisory prose does not prevent obsolete route continuation.

**Trade-offs:** The system must explicitly say when evidence is material; semantic correctness remains reviewable rather than fully automatic.

**Risks:** Intelligence may misclassify materiality. P4 and real-work evidence remain the semantic verification boundary.

**Evidence expected:** controlled reroute test showing old route + new evidence + changed state + new route/blocker; failure test that unchanged route is rejected after declared invalidation.

---

## AD-V2-006 — HUMAN AUTHORITY AND OPERATIONAL RESCUE ARE DISTINCT RECORDED EVENTS

**Requirement:** R-006, R-013; C-008.

**Decision:** Every material Human intervention must be explicitly classified. Genuine authority gates are allowed and required where applicable; routine Human routing/decomposition/recovery is recorded as operational rescue and cannot be silently counted as autonomous Projector success.

**Mechanism:** A state transition with Human intervention carries:

```text
human_intervention:
  classification:
    GENUINE_HUMAN_OWNED_GATE
    | HUMAN_OPERATIONAL_RESCUE
  reason
  authority_basis
  human_decision_evidence_ref
```

A `GENUINE_HUMAN_OWNED_GATE` must cite one of the frozen Human authority categories: goal/normative meaning, final acceptance, costly/public/destructive/irreversible/materially risky effect, or genuine preference not resolvable by evidence.

The system may record rescue and continue when appropriate, but the evidence package must surface it; P4 decides the affected requirement verdict.

**Why:** Historical KYC evidence demonstrates a real authority gate; the Task Contract identifies hidden Human orchestration as a major confounder.

**Alternatives:** count all Human inputs as equivalent; prohibit all Human intervention; dedicated HOT runtime.

**Rejected:** Equivalence hides rescue; prohibition violates Human authority; dedicated HOT machinery is not justified or authorized.

**Trade-offs:** Some classification is semantic and therefore auditable rather than perfectly machine-detectable.

**Risks:** Mislabeling rescue as a gate. P4 must inspect the underlying intervention evidence.

**Evidence expected:** tests that intervention records require classification; accepted run intervention ledger; P4 classification review.

---

## AD-V2-007 — EXACT EVIDENCE REFERENCES AND PROVENANCE MATRIX

**Requirement:** R-004, R-007, R-009, R-011, R-012.

**Decision:** Evidence is referenced by exact identity, not prose claims. The P3 Implementation Package must include a provenance matrix whose completed-stage links are unambiguous.

**Mechanism:** Every evidence reference contains at minimum:

```text
evidence_id
kind
scope: PROJECTOR_INTERNAL | WORKLOAD_EXTERNAL | HUMAN_DECISION | TEST
locator
immutable_identity
observed_at
producer
supports[]
```

Identity rules:

```text
repository artifact -> repository + commit + path (+ blob SHA when available)
external web/state   -> preserved snapshot/artifact + retrieval time + digest where possible
command/test result  -> command + environment + exit/result + preserved output identity
Human decision       -> durable copied decision record/event + timestamp/source reference
```

P3 provenance matrix columns:

```text
Requirement
Task Contract identity
Architecture Decision ID + Architecture Contract identity
Implementation path + implementation SHA
Test/evidence IDs
P4 finding: NOT YET AUDITED until P4
Human acceptance: NOT YET CREATED until post-P4 Human action
```

**Why:** Claim != evidence and the system-wide provenance invariant require exact identity at every completed stage.

**Alternatives:** narrative evidence summary; chat-history-only provenance; mutable latest links.

**Rejected:** All permit ambiguity or future drift.

**Trade-offs:** More explicit metadata and hashing work in exchange for auditability.

**Risks:** Some external systems cannot be perfectly replayed. In that case evidence must remain bounded and P4 may return `UNKNOWN`; no prose may upgrade it to PASS.

**Evidence expected:** machine-readable provenance matrix/package; verifier failure when required completed-stage identity is missing.

---

## AD-V2-008 — THREE-LAYER VERIFICATION: EXECUTABLE TESTS, REAL-WORK EFFECT, INDEPENDENT P4

**Requirement:** R-001, R-007, R-008, R-010, R-012.

**Decision:** Do not use one test class as a proxy for the full capability. Verification is deliberately split:

```text
LAYER 1 — deterministic executable verification
  run format, chain integrity, intent-change gate, route invalidation,
  Human intervention record, DONE evidence requirements, failure paths

LAYER 2 — bounded real-work validation
  exact frozen Projector implementation + Human-selected workload
  -> observable workload-external effect

LAYER 3 — independent P4 audit
  requirement-by-requirement semantic verification against frozen artifacts
```

**Mechanism / required P3 tests:**

```text
tests/projector/test_projector_run.py
  init/binding record
  state classification completeness
  intent preservation / unauthorized goal-change rejection
  Human intervention classification
  DONE evidence gating

tests/projector/test_projector_recovery.py
  fresh recovery from durable bundle
  corrupt/missing snapshot chain failure
tests/projector/test_projector_integration.py
  controlled multi-step route invalidation and reroute/block replay
  provenance completeness for completed implementation stage
```

Required CI commands are added to the existing workflow; no new test framework is introduced.

**Why:** Deterministic tests can prove integrity mechanisms but cannot independently prove long-horizon intelligent behavior. Real-work effect and P4 are required to close that gap.

**Alternatives:** unit tests only; manual demo only; P3 self-assessment.

**Rejected:** Each violates one or more explicit requirements.

**Trade-offs:** Full closure requires more than CI, but evidence categories remain honest.

**Risks:** A replay fixture could look like intelligence proof. It must be labeled `TEST`, never `WORKLOAD_EXTERNAL` real-work evidence.

**Evidence expected:** exact CI results; controlled failure/reroute evidence; cold-start recovery; final real-work bundle; P4 findings.

---

## AD-V2-009 — CAPABILITY STATUS AND HUMAN ACCEPTANCE REMAIN OUTSIDE PROJECTOR SELF-APPROVAL

**Requirement:** R-009, R-012, R-013.

**Decision:** Reuse `CAP-GATE-001` for mechanical status discipline, but do not let Projector or P3 self-promote based on code/tests alone. Human final acceptance is a distinct post-P4 state.

**Mechanism:** P3 may update the `CAP-ITO-001` registry entry only to the highest status justified by the exact registered evidence prerequisites and semantic package. Architecture completion causes no registry change. A first real-work success must not become `RELIABLE`. P4 findings remain independent. Human acceptance is recorded separately after P4 as `ACCEPTED`, `REJECTED`, or `DEFERRED / MORE EVIDENCE REQUIRED`.

**Why:** Existing registry gate already enforces bounded mechanical prerequisites, while the Task Contract explicitly reserves semantic verification to P4 and final acceptance to Human.

**Alternatives:** new Projector-specific maturity system; automatic status promotion; automatic acceptance on CI/P4 PASS.

**Rejected:** Duplicates governance or violates authority boundaries.

**Trade-offs:** Existing registry schema remains simple; semantic sufficiency is still a P4 responsibility.

**Risks:** Mechanical registry prerequisites can pass while semantic evidence is weak. P4 must return the evidence-supported verdict rather than trusting CI.

**Evidence expected:** registry diff tied to exact evidence paths; existing capability verifier pass; distinct P4 report and later Human acceptance record.

---

# COMPONENT MODEL

## C1 — EXISTING INTELLIGENCE

Existing reasoning surface. Owns no Human intent. It binds rough intent into a bounded working target, selects justified moves, observes results and proposes reroutes/gates.

Not a new P3 component.

## C2 — PROJECTOR RUN RECORDER / TRANSITION VERIFIER

Physical implementation: `scripts/projector_run.py`.

Responsibilities:

```text
init run bundle
validate proposed state transition
append immutable snapshot
validate chain/provenance
recover current state
fail closed on invalid transition/corrupt state
```

It does not decide the substantive next move and does not execute a master workflow.

Required command interface:

```text
python scripts/projector_run.py init --run-dir <path> --input <json-file>
python scripts/projector_run.py transition --run-dir <path> --input <json-file>
python scripts/projector_run.py recover --run-dir <path>
python scripts/projector_run.py verify --run-dir <path>
```

Exact CLI spelling above is frozen for P3 v2.0 implementation.

## C3 — DURABLE RUN BUNDLE

Physical runtime artifacts under `projector/runs/<run-id>/` as defined in AD-V2-003.

## C4 — WORKLOAD TOOL / EFFECT PATH

Whatever existing tool, repository, browser, API or local action naturally serves the selected real workload. This is workload-dependent and is **not** a mandatory Projector component.

## C5 — EXISTING CAPABILITY EVIDENCE GATE

`governance/CAPABILITY_REGISTRY.json` + `scripts/verify_capability_evidence.py` + existing CI.

Used for claim discipline only; not Projector reasoning/runtime.

## C6 — P4 INDEPENDENT AUDIT

External verification stage. Not implemented by P3.

---

# DATA / CONTROL FLOW

```text
1. Human supplies rough intent.
2. Intelligence creates a bounded target without asking Human to choose architecture/tooling.
3. Before material real-work execution, `init` freezes raw intent, goal, DONE,
   verification method, current critical unknown, known authority gates and exact provenance.
4. Intelligence chooses one current justified move from current state/evidence.
5. If the move is routine/reversible and authorized, normal tools execute it.
6. If the move requires Human authority, execution stops at a recorded Human gate.
7. Resulting evidence is preserved by exact reference.
8. Intelligence proposes the next complete state snapshot.
9. `transition` validates intent lineage, state categories, evidence refs, route semantics,
   Human intervention classification and provenance, then appends the snapshot.
10. If evidence invalidates the route, the accepted next state must reroute or block.
11. `recover` allows a fresh actor/process to reconstruct the canonical current state.
12. `DONE` is accepted into the run record only with predefined verification and
    at least one workload-external/independently reproducible effect evidence reference.
13. P3 freezes implementation/evidence identities and hands them to P4.
14. P4 audits independently.
15. Human makes a separate final acceptance decision.
```

No step requires every COS component, and no fixed component pipeline is implied.

---

# INTERFACES

## I-V2-001 — INIT INPUT

Required fields:

```text
raw_human_intent
bounded_target
goal
done
verification_method
current_critical_unknown
assumptions[]
known_human_authority_gates[]
provenance.task_contract
provenance.architecture_contract
provenance.implementation
```

The Human provides `raw_human_intent`; system-owned binding fields are created by Intelligence and preserved as system output, not silently attributed to Human.

## I-V2-002 — TRANSITION INPUT

Required fields correspond to the full state schema in AD-V2-003 plus:

```text
transition_reason
material_evidence_change
evidence_basis
human_intervention or null
route_change or null
goal_change or null
```

## I-V2-003 — EVIDENCE REFERENCE

Exact contract defined in AD-V2-007.

## I-V2-004 — RECOVERY OUTPUT

`recover` returns the validated latest state plus the run identity/provenance needed to continue:

```text
goal
DONE
observed facts
assumptions
claims
unknowns
critical unknown/blocker
material evidence refs
current route / next justified move or Human gate
Task Contract identity
Architecture Contract identity
implementation identity
latest state sequence/hash
```

## I-V2-005 — P3 -> P4 EVIDENCE PACKAGE

Must include:

```text
frozen Task Contract identity
frozen Architecture Contract identity
exact implementation repository/branch/SHA
implementation file list/blob identities
CI/test evidence identities
failure/interruption evidence
recovery evidence
controlled reroute evidence
Human intervention ledger
real-work run bundle/effect evidence if available
capability registry state/diff
requirement provenance matrix
```

P4 finding fields remain `NOT YET AUDITED` when P3 creates the package.

---

# INVARIANTS

1. Raw Human intent is never overwritten.
2. Goal/DONE cannot change without durable Human-owned goal-change evidence.
3. Facts, assumptions, claims and unknowns remain distinct categories.
4. Exactly one current critical unknown/blocker is recoverable from each active state.
5. Every current next move/gate has an explicit justification and evidence basis.
6. Declared route invalidation cannot silently continue the same route.
7. A Human intervention is never left unclassified when material to the run.
8. Human authority gates are not reclassified as routine execution to increase autonomy.
9. Human operational rescue is never hidden or counted as autonomous success.
10. State snapshots are append-only and hash-chained; corruption fails closed.
11. No `DONE` based only on Projector code/docs/tests is valid real-work DONE.
12. Exact Task/Architecture/implementation identities are present for every completed stage.
13. `UNKNOWN` evidence state never becomes `PASS` by omission.
14. `CAP-ITO-001` status never exceeds exact registered evidence.
15. Projector/P3 never fabricates P4 findings or Human final acceptance.
16. Historical Projector research is not retroactively reclassified as evidence produced by the new implementation.

---

# FAILURE MODES AND REQUIRED BEHAVIOR

| Failure | Required behavior |
|---|---|
| Missing required init field | reject init; no partial run bundle |
| Proposed goal/DONE silently changes | reject transition |
| Snapshot chain missing/corrupt | `verify`/`recover` fail closed; no guessed current state |
| Evidence invalidates route but same route continues | reject transition |
| Dependency/input becomes unavailable | record evidence; reroute or `BLOCKED`, never fabricated success |
| Human operational rescue occurs | record as rescue; continue only truthfully; surface to P4 |
| Consequential Human-owned action lacks authority evidence | stop at Human gate |
| DONE has only Projector-internal artifacts | reject real-work DONE classification |
| Evidence identity is missing for a completed stage | provenance status `UNKNOWN`/failure; no automatic handoff |
| Capability promotion outruns evidence | existing registry verifier must fail or P4 must reject semantic overclaim |
| Real workload cannot produce external effect | reject workload/stop validation; Human selects another workload |

---

# SECURITY / SAFETY CONSIDERATIONS

- Do not store credentials, tokens, private keys, identity documents, biometric images or unnecessary sensitive personal data in Projector run bundles or repository evidence.
- For sensitive/costly/public/destructive/irreversible/materially risky actions, store the decision/gate evidence, not the secret material itself.
- External evidence should be minimized to what is needed for verification and preferably preserved as redacted/sanitized artifacts with exact identity.
- The executable has no authority to bypass platform/user consent or Human authority boundaries.
- A public repository must be assumed observable; secrets and high-sensitivity personal evidence must remain outside it with a safe immutable reference where verification permits.

---

# MIGRATION / COMPATIBILITY

This architecture is additive.

```text
NO EXISTING DATA MIGRATION REQUIRED
NO REGISTRY SCHEMA CHANGE REQUIRED
NO DATABASE REQUIRED
NO NEW CI FRAMEWORK REQUIRED
NO CHANGE TO EXISTING GINSENG/COS CONTINUITY ARTIFACTS
NO CHANGE TO HISTORICAL PROJECTOR RESEARCH
```

The existing `CAP-GATE-001` mechanism remains unchanged unless P3 discovers a concrete incompatibility. Any such incompatibility is a new architecture issue; P3 must not silently redesign the gate.

The non-current `arch/projector-real-project-v1` branch is preserved as repository history and is not merged, rewritten or used as implementation authority by this contract.

---

# OBSERVABILITY

P3 and P4 must be able to inspect at least:

```text
run id
raw Human intent
current Human-owned goal / DONE
current observed facts
assumptions / claims / unknowns
critical unknown/blocker
current route + next move/gate
all material evidence identities
route revisions and their evidence triggers
all material Human interventions + classification
implementation SHA
state sequence/hash chain
DONE verification evidence
capability registry status/evidence references
P4 finding state
Human acceptance state
```

Observability is artifact-based. Dedicated HOT runtime/instrumentation is not introduced.

---

# IMPLEMENTATION BOUNDARIES

## MUST

- implement against the exact frozen Architecture Contract v2.0 commit;
- use `FJ899/COS` and `impl/projector-real-project-v2`;
- implement `scripts/projector_run.py` with the four frozen commands;
- use Python 3.11 standard library only unless P3 finds a hard blocker and returns to P2;
- implement the run bundle and state/evidence interfaces defined here;
- implement fail-closed validation before writing a state transition;
- create the three Projector test files defined in AD-V2-008;
- extend existing GitHub Actions to run Projector tests;
- preserve exact P1/P2/P3 provenance;
- freeze an exact implementation SHA before any real-work validation run;
- after Human selects the real workload, create its pre-run freeze before material execution;
- preserve Human rescue/gate evidence exactly enough for P4 classification;
- keep capability status no higher than exact evidence supports;
- hand P4 a package with P4 fields still `NOT YET AUDITED`.

## MAY

- use local helper functions/classes inside `scripts/projector_run.py` where they reduce duplication;
- add test fixtures under `tests/projector/fixtures/` if a controlled replay materially benefits test readability;
- preserve external evidence outside `projector/runs/` and reference it by exact immutable identity;
- add concise operator documentation only after executable behavior exists.

## MUST NOT

- implement a new planner, master router, scheduler, persistent autonomous agent, multi-agent supervisor, database, service or dashboard;
- implement standalone HOT runtime/instrumentation;
- force all COS components into each run;
- ask the Human to choose architecture/toolchain as normal product input;
- silently change any Task Contract requirement/constraint/acceptance criterion;
- silently mutate or rewrite earlier state snapshots;
- treat historical Projector observations as evidence generated by this implementation;
- use architecture/code/test existence as effect-based real-work DONE;
- cross a genuine Human authority gate autonomously;
- hide Human operational rescue;
- auto-promote to `RELIABLE` after one run;
- create P4 PASS findings or Human `ACCEPTED` state.

---

# DO NOT CHANGE

```text
GOAL from Task Contract v1.0
R-001 through R-013
C-001 through C-009
AC-001 through AC-011
CAP-ITO-001 starting status = PROPOSED
Human authority boundaries
UNKNOWN != PASS
CLAIM != EVIDENCE
ARCHITECTURE != PRODUCT PROGRESS
HOT runtime is not pre-authorized
first real-work proof does not imply RELIABLE maturity
```

---

# ASSUMPTIONS

## ASSUMPTION A-V2-001

The P3/validation environment can execute Python 3.11 and read/write a local checkout of the implementation repository. Basis: the pinned repository already verifies through Python 3.11 GitHub Actions.

If false, P3 must return `ARCHITECTURE BLOCKED -> P2` with the exact execution constraint; it must not substitute a new platform.

## ASSUMPTION A-V2-002

The normal Human-facing rough-intent surface is the existing Human <-> Intelligence interaction, while the CLI is an internal durable-state interface used by the system/tool layer. This is consistent with the frozen P1 run contract and does not require Human tooling choices.

If a standalone end-user interface is later required, that is a new architecture/version decision.

## ASSUMPTION A-V2-003

For external effects that cannot be replayed byte-for-byte, a preserved snapshot/result plus exact retrieval/source identity may constitute evidence, but P4 retains authority to judge sufficiency and may return `UNKNOWN`.

---

# OPEN QUESTIONS

## P2-OQ-V2-001 — FIRST BOUNDED REAL-WORK VALIDATION WORKLOAD

```text
QUESTION:
Which genuine bounded Human workload will be used for the first real-work proof?

OWNER: HUMAN

REQUIRED BEFORE:
real-work validation execution for R-007 / AC-006

BLOCKS P2 ARCHITECTURE FREEZE: NO
BLOCKS P3 CORE IMPLEMENTATION: NO
BLOCKS FINAL END-TO-END REAL-WORK EVIDENCE: YES
BLOCKS FINAL P4 PASS ON R-007: YES
```

The selected workload must satisfy the admissibility constraints in `BOUNDED VALIDATION WORKLOAD DETERMINATION` and must be frozen with raw intent, goal, effect-based DONE, verification method, current critical unknown and known Human authority gates before material execution.

This is a new P2 open-question identity. It does not inherit the numbering of any prior downstream narrative.

---

# KNOWN RISKS

## KR-V2-001 — SEMANTIC QUALITY OUTRUNS MECHANICAL VALIDATION

The executable can enforce evidence references and transition rules but cannot prove that an Intelligence-selected move is actually the best justified move. P4 and real-work evidence remain necessary.

## KR-V2-002 — SELF-HOSTING CIRCULARITY

Building Projector cannot itself satisfy the real-work proof. The selected workload must have an effect external to Projector build artifacts.

## KR-V2-003 — HUMAN RESCUE MISCLASSIFICATION

A rescue may be mislabeled as a genuine gate. Preserve the underlying intervention evidence for P4.

## KR-V2-004 — EXTERNAL EVIDENCE EPHEMERALITY

External states may disappear or change. Preserve snapshots/digests/identities as early as practical.

## KR-V2-005 — SINGLE-RUN OVERGENERALIZATION

One bounded success is not broad reliability and must not produce a `RELIABLE` claim.

## KR-V2-006 — MONOLITHIC FIRST SLICE PRESSURE

A single script may become awkward. Do not extract a new architecture from that discomfort until a second independent real use demonstrates the common boundary or a safety/integrity need requires it.

---

# OPEN BLOCKERS

```text
ARCHITECTURE BLOCKERS: NONE
P3 CORE IMPLEMENTATION BLOCKERS: NONE
REAL-WORK VALIDATION BLOCKER: P2-OQ-V2-001 / OWNER HUMAN
P4 FINAL REAL-WORK VERIFICATION: BLOCKED UNTIL THAT WORKLOAD IS EXECUTED AND EVIDENCE IS FROZEN
```

---

# HANDOFF CONDITION

P2 may hand off to P3 only after this exact Architecture Contract is frozen by Git commit and the implementation branch is created from that exact commit.

P3 may implement the core vertical slice immediately, but must stop before the first real-work validation run until `P2-OQ-V2-001` has a Human answer and the workload pre-run freeze is durable.

```text
HANDOFF -> P3 IMPLEMENTATION

INPUT:
TASK CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v1.0
ARCHITECTURE CONTRACT PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT v2.0
EXACT IMPLEMENTATION BASE SHA: supplied in the external freeze/handoff record
IMPLEMENTATION BRANCH: impl/projector-real-project-v2

PURPOSE:
Build the frozen minimal vertical slice without redefining WHAT or introducing new architecture.
```
