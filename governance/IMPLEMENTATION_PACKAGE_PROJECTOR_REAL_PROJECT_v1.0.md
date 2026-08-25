# IMPLEMENTATION PACKAGE — PROJECTOR / INTENT-TO-OUTCOME REAL PROJECT

VERSION: v1.0
STATUS: CORE IMPLEMENTED; FINAL REAL-WORK EVIDENCE INCOMPLETE

TASK CONTRACT: `governance/TASK_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md` @ `ef128a0885310524475fba1cd291d1f34400b0cc`
ARCHITECTURE CONTRACT: `governance/ARCHITECTURE_CONTRACT_PROJECTOR_REAL_PROJECT_v1.0.md` @ `4e05e026b3c9a4eafe5040537be45386b36ba426`

## WORKING IDENTITY

```text
repo: FJ899/COS
base branch: arch/projector-real-project-v1
base SHA: 4e05e026b3c9a4eafe5040537be45386b36ba426
implementation branch: impl/projector-real-project-v1
implementation code/test identity: dadc96c97626a0b7896e8e8718a979d79c49db20
implementation package manifest: governance/IMPLEMENTATION_PACKAGE_PROJECTOR_REAL_PROJECT_v1.0.md
package commit identity: enclosing handoff commit; do not infer before freeze
```

Local execution environment used by P3:

```text
Python: 3.13.5
Project CI configured Python: 3.11
Local filesystem-backed temporary run store
```

## CHANGES MADE

- Added a standard-library `projector` package implementing typed run state, provenance, authority classification, durable filesystem storage, fail-closed transitions, recovery, and a thin CLI.
- Added append-only event records with exact Task Contract, Architecture Contract, implementation identity, state digests, parent references, and evidence paths.
- Added evidence capture with SHA-256 content identity and immutable metadata-bound evidence files.
- Added deterministic enforcement for Human goal/DONE changes, evidence-backed observations, route invalidation, truthful blocking, and DONE verification.
- Added executable Projector contract/failure/recovery tests.
- Extended the existing GitHub Actions workflow with the Projector unittest command only.
- Did not modify `CAP-ITO-001`; it remains `PROPOSED` pending evidence sufficient for any promotion.
- Did not create the AD-008 workload-specific adapter because Human-owned OQ-001 is not yet resolved.

## CHANGE → ARCHITECTURE DECISION MAP

| Change | Architecture decision(s) |
|---|---|
| `projector/model.py` typed state/evidence/intervention models | AD-003, AD-004, AD-006 |
| `projector/storage.py` atomic run state, append-only events, evidence digests, recovery/integrity | AD-003, AD-007 |
| `projector/kernel.py` fail-closed transitions, route invalidation, DONE rules | AD-004, AD-005 |
| `projector/authority.py` Human gate vs operational rescue | AD-006 |
| `projector/provenance.py` frozen upstream identities and digest binding | AD-007 |
| `projector/cli.py` explicit product entrypoint / inspect / record / verify | AD-002 |
| Projector tests and CI command | AD-009, AD-010 |
| Capability registry left at `PROPOSED` | AD-011 |
| Workload adapter | AD-008 — NOT YET IMPLEMENTED; blocked by Human-owned OQ-001 |

## FILES CHANGED

```text
projector/__init__.py
projector/model.py
projector/provenance.py
projector/authority.py
projector/storage.py
projector/kernel.py
projector/cli.py
tests/projector/test_projector.py
.github/workflows/verify-creative-os.yml
governance/IMPLEMENTATION_PACKAGE_PROJECTOR_REAL_PROJECT_v1.0.md
```

No unrelated repository cleanup was performed.

## TESTS ADDED / MODIFIED

`tests/projector/test_projector.py` covers:

1. rough intent -> durable bounded run state;
2. truthful BLOCKED state when Human-owned semantics are missing;
3. Human goal preservation and silent-substitution rejection;
4. OBSERVED / ASSUMPTION / CLAIM / UNKNOWN separation;
5. evidence requirement and evidence tamper detection;
6. invalidated route -> reroute or rejection;
7. dependency/route failure -> visible truthful blocker;
8. genuine Human gate vs Human operational rescue;
9. cold-start recovery plus provenance/state-digest chain;
10. DONE rejection without run-specific verification evidence and acceptance only with such evidence;
11. stale state proposal and unfrozen implementation provenance rejection.

CI extension:

```text
python -m unittest discover -s tests/projector -p 'test_*.py'
```

## TEST RESULTS

Local P3 execution:

```text
...........
----------------------------------------------------------------------
Ran 11 tests

OK
```

Static Python bytecode compilation:

```text
python3 -m compileall -q projector tests/projector
RESULT: PASS LOCALLY
```

CLI smoke path executed before package freeze:

```text
start -> inspect -> verify
integrity: OK
```

GitHub Actions / Python 3.11 result at package-authoring time:

```text
NOT YET AVAILABLE
```

This package does not convert local P3 results into a P4 verdict.

## RUNTIME / OTHER EVIDENCE

Mechanically demonstrated locally:

- durable `run.json` creation;
- append-only `events.jsonl` creation;
- exact event provenance fields;
- evidence file creation and digest checking;
- cold-start load from filesystem artifacts;
- tamper detection;
- route invalidation behavior;
- DONE fail-closed behavior;
- CLI integrity verification.

The smoke run used an ephemeral local temporary store and is not claimed as the required real-work evidence for AC-006.

## REQUIREMENT → IMPLEMENTATION / TEST EVIDENCE MAP

| Requirement | Architecture | Implementation / evidence at P3 | Current P3 evidence state |
|---|---|---|---|
| R-001 | AD-001, AD-002, AD-008 | `projector/`, entrypoint tests | PARTIAL — core executable; real workload evidence not yet created |
| R-002 | AD-002, AD-003 | `ProjectorKernel.start_run`, CLI, rough-intent test | LOCALLY TESTED |
| R-003 | AD-003, AD-004 | immutable intent semantics / explicit goal-change gate tests | LOCALLY TESTED |
| R-004 | AD-003, AD-004 | typed state records, blocker/evidence/next-route fields | LOCALLY TESTED |
| R-005 | AD-004, AD-005 | transition kernel and reroute tests | LOCALLY TESTED |
| R-006 | AD-005, AD-006 | authority classifier and rescue tests | LOCALLY TESTED; accepted real run not yet created |
| R-007 | AD-008, AD-010 | workload adapter / real effect evidence | NOT YET CREATED — OQ-001 owner HUMAN |
| R-008 | AD-004, AD-009 | deterministic failure/block/reroute tests | LOCALLY TESTED |
| R-009 | AD-011 | `CAP-ITO-001` remains `PROPOSED`; no promotion | OBSERVED IN REPOSITORY STATE; P4 semantic finding NOT YET AUDITED |
| R-010 | AD-003, AD-007 | cold-start recovery and integrity tests | LOCALLY TESTED |
| R-011 | AD-007, AD-010 | upstream identities in events + this provenance matrix | IMPLEMENTED; P4 link NOT YET AUDITED |
| R-012 | AD-010 | P4 audit | NOT YET AUDITED |
| R-013 | AD-006, AD-010 | Human acceptance | NOT YET CREATED |

## DEVIATIONS

NONE from the frozen architecture for the implemented core.

AD-008 is intentionally not implemented yet because the Architecture Contract explicitly leaves OQ-001 to the Human and states that it blocks the final real-work proof but not P3 core implementation.

## KNOWN LIMITATIONS

- No Human-selected first real validation workload exists yet.
- Therefore no workload-specific adapter, accepted real run, or effect-based real-work evidence exists yet.
- Local P3 tests ran under Python 3.13.5; repository CI is configured for Python 3.11 and its run result is separate evidence.
- The filesystem store is integrity-checked, not tamper-proof; committed/frozen identities remain necessary for P4.
- The general-purpose Intelligence that chooses useful next moves is outside the deterministic kernel, as specified by Architecture Contract v1.0.

## UNRESOLVED ITEMS

```text
OQ-001 FIRST REAL VALIDATION WORKLOAD
OWNER: HUMAN
STATE: NOT YET CREATED / NOT YET SELECTED
BLOCKS: R-007 / AC-006 final real-work evidence

REAL-WORK EVIDENCE PACKAGE: NOT YET CREATED
P4 AUDIT: NOT YET AUDITED
HUMAN FINAL ACCEPTANCE: NOT YET CREATED
```

## CLAIMS REQUIRING INDEPENDENT VERIFICATION

All requirement-level compliance findings remain owned by P4. In particular P4 must independently inspect/reproduce:

- intent preservation across exact run artifacts;
- evidence/claim distinction and tamper behavior;
- route invalidation behavior;
- Human intervention classification;
- cold-start recovery;
- capability-registry consistency;
- final real-work effect evidence after OQ-001 is resolved.

P3 does not assign PASS/FAIL to the project.

## HANDOFF STATE

```text
CORE IMPLEMENTATION: COMPLETE
LOCAL CORE TESTS: PASS
FINAL REAL-WORK PROOF: NOT YET CREATED — OQ-001 OWNER HUMAN
P4 AUDIT: NOT YET AUDITED
HUMAN FINAL ACCEPTANCE: NOT YET CREATED
```
