# FINAL PROJECTOR-CANDIDATE SCAN — 2026-08-23

## Authorization

Human authorization received:

`AKCEPTUJ FINAL PROJECTOR-CANDIDATE SCAN`

## Scan target

Find a live BLOCKED INTENT case that an independent third party can immediately inspect, reproduce, experiment on, and verify without:

- private data;
- repeated intervention from the original Human;
- rare/specific hardware;
- platform-owner action on the critical path.

Required activation gates:

```text
E1 CURRENT BLOCKER STILL ACTIVE
E2 UNKNOWN HOW STILL UNKNOWN
E3 PUBLIC / RETRIEVABLE INPUT ARTIFACTS
E4 REPRODUCIBLE BASELINE
E5 NO RARE HARDWARE ON CRITICAL PATH
E6 NO PRIVATE DATA ON CRITICAL PATH
E7 NO ORIGINAL-HUMAN ACTION REQUIRED FOR EACH ITERATION
E8 OBJECTIVE FEEDBACK PRODUCIBLE INDEPENDENTLY
E9 SAFE / REVERSIBLE FIRST EXPERIMENT
E10 MULTI-STEP DEPTH
```

## Candidate attrition

The scan rechecked issue bodies, current comments, related PR/fix state, artifact availability and execution dependencies close to activation.

Representative rejected cases included:

- FreeCAD #31855 — open issue, but root cause and verified local fix already published.
- FreeCAD #31849 — trigger corrected, workaround documented, fix PR already exists.
- GS-DIFF #2 — live reproduction gap, but public repository lacks implementation/scenes needed to run the experiment.
- Quarkus #56030 — root cause and fix/PR already established.
- Spring Framework #37155 — root cause and fix PR already established.
- LLVM #214665 — project owner effectively withdrew the request / preferred no-fix closure.
- openEMS #222 — shallow failure with known environment/workaround direction.
- loft-lang/loft #1078 — resolution already found / pending merge.
- FreeCAD #31832 — viable workarounds and OCCT parameterization mechanism already identified.
- rust-lang/rust #161441 — evidence suggests the regression has already moved/fixed through dependency/toolchain changes.
- GS-DIFF and several hardware/ML candidates — execution depended on missing code, private state, H100/Apple Silicon/phone/embedded/GPU hardware.
- Zcash lightwalletd #593 — technically reproducible, but repeated verification depends on stressing a public third-party service.
- Nim #26136 — extremely fresh and self-contained, but likely too shallow for a multi-session Projector test.

This attrition is itself important evidence:

```text
OPEN ISSUE
!=
UNSOLVED PROJECT

HIGH BLOCKED-INTENT SCORE
!=
ACTIVATION-READY PROJECT
```

## FINAL PRIMARY CANDIDATE

### JDTLS #3866 — StackOverflowError in HierarchyResolver

Source:
`eclipse-jdtls/eclipse.jdt.ls #3866`

Created:
2026-08-13

Current state:
OPEN

Human goal:
Use JDTLS directly and reliably query call hierarchy / outgoing calls for a real Java workspace without triggering a StackOverflowError.

### Current evidence

The reporter published a dedicated reproducer repository:

`usrlocl/jdtls-stackoverflow-reproduce`

Frozen reproducer branch at preflight:

`master @ 57fa37e03621026b3b165075934a34677a6c92d9`

The repository contains:

- `jdtls-calls.mjs` — automated JDTLS driver;
- `fail/` — failing Java workspace;
- `pass-no-module/`;
- `pass-no-self-reference-import/`;
- `pass-separate-test-pkg/`.

The reproducer directly exercises:

```text
spawn JDTLS
→ initialize workspace
→ didOpen source files
→ prepareCallHierarchy
→ outgoingCalls
→ StackOverflowError / success
```

The reporter already established several controlled deltas that suppress the failure:

1. remove `module-info.java`;
2. remove a self-reference import;
3. separate main/test package paths;
4. avoid opening all files before the call-hierarchy request.

A second participant independently reported reproducing the stack overflow and suggested it may involve the incremental builder / an upstream JDT issue, but did not establish the actual root cause or fix.

No related fix PR was found for #3866 at activation preflight.

A similar older JDT Core StackOverflow class exists, including `eclipse-jdt/eclipse.jdt.core #1490`; it remained reproducible after a previously suggested related fix. This increases evidence that the failure family is real, but does not close the exact current HOW.

Current JDTLS `main` observed during scan:

`75e47d0441c34d571b4d598c8c140d533190af61`

## Execution-self-sufficiency gate

```text
E1 CURRENT BLOCKER ACTIVE
PASS
Issue remains open; latest discussion does not contain a solution.

E2 UNKNOWN HOW STILL UNKNOWN
PASS
Several causal variables are known, but the actual recursion mechanism and correct fix are not established.

E3 PUBLIC / RETRIEVABLE ARTIFACTS
PASS
Dedicated public reproducer with fail/pass controls and driver script.

E4 REPRODUCIBLE BASELINE
PASS — EVIDENCE LEVEL
Reporter and another participant report reproduction.
Local execution still must be frozen at activation before any solution work.

E5 NO RARE HARDWARE
PASS
Ordinary Java/JDTLS/Node environment.

E6 NO PRIVATE DATA
PASS
All test inputs are public synthetic/minimal workspaces.

E7 NO ORIGINAL HUMAN EACH ITERATION
PASS
The reproducer is designed for independent execution.

E8 OBJECTIVE FEEDBACK
PASS
StackOverflowError vs successful completion / valid outgoingCalls response.

E9 SAFE / REVERSIBLE FIRST EXPERIMENT
PASS
Run in an isolated workspace/process with bounded memory/time; no external mutation is required.

E10 MULTI-STEP DEPTH
PASS
Likely spans JDTLS lifecycle, JDT Core resolution/hierarchy behavior, modules/imports, workspace state and request sequencing.
```

## Why this beats the Vite fallback

### Vite #23227

The Vite watcher case is also strong:
- live;
- inline deterministic shell reproducer;
- ordinary Linux/Node environment;
- no private data;
- objective stale-build result;
- no known fix in the issue.

But:
- another participant could not reproduce it under nearby Linux environments;
- the issue is explicitly labeled `bug: upstream`;
- kernel/watcher behavior may be a material environment variable;
- depth may collapse quickly into a narrower upstream native-watcher defect.

Therefore Vite remains the strongest fallback, but JDTLS has a better combination of independent reproduction evidence, public controlled variants and multi-layer UNKNOWN HOW.

## Reserve candidate

`rust-lang/rust #160957`

Very deep and self-contained, but optimization-triggered OOM/pathological compile-time behavior makes safe experimentation more resource-sensitive. Keep as reserve, not primary.

## Final verdict

```text
FINAL PROJECTOR-CANDIDATE SCAN
= PASS

PRIMARY:
JDTLS #3866 — StackOverflowError in HierarchyResolver

FALLBACK:
Vite #23227 — atomic replacement breaks subdirectory watch

RESERVE:
rust-lang/rust #160957

LIVE PROJECT ACTIVATION
= NOT YET STARTED
```

## Activation rule

Before any diagnosis or solution design:

```text
1. freeze issue/comments/related-state snapshot;
2. freeze JDTLS main SHA;
3. freeze reproducer SHA;
4. execute the original failing baseline unchanged;
5. execute all published passing controls unchanged;
6. preserve raw logs;
7. define LOCAL DONE;
8. only then begin hypothesis generation.
```

If the original baseline does not reproduce in the activation environment:

```text
DO NOT REPAIR THE TEST UNTIL IT PASSES.

CLASSIFY:
BASELINE NON-REPRODUCTION

THEN:
determine whether environment drift itself is the first real finding.
```
