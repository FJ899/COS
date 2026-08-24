# REAL-WORLD NEED RADAR — METHODOLOGY v1.6
## Candidate Attrition / Activation Readiness
Date: 2026-08-23

## Trigger

The FINAL PROJECTOR-CANDIDATE SCAN applied the v1.4 solution-state gate and v1.5 execution-self-sufficiency gate to fresh open issues.

A high percentage of apparently excellent candidates failed immediately before activation.

## New observation

```text
DISCOVERY QUALITY
!=
ACTIVATION READINESS
```

A candidate can be excellent at discovery time and become unsuitable hours or days later because:

- root cause is published in a comment;
- a fix PR appears;
- the author discovers a workaround;
- the issue remains open even though UNKNOWN HOW is closed;
- public artifacts disappear or were never actually sufficient;
- current main no longer reproduces;
- the only meaningful experiment needs private data or special hardware.

This creates:

`CANDIDATE ATTRITION`

## Candidate half-life

Fast-moving technical candidates have a short methodological half-life.

Do not treat a Radar card as reserving an unsolved problem.

```text
RADAR CARD
= LEAD

NOT
= FROZEN UNSOLVED PROJECT
```

The stronger and more active the issue, the greater the probability that its state changes between discovery and activation.

Add:

`CANDIDATE_HALF_LIFE_RISK`

Values:

- HIGH — active issue/PR, many contributors, fast-moving repo, obvious fix attempts;
- MEDIUM — active discussion but no implementation movement;
- LOW — stable blocker, little current solution activity.

High half-life risk does not reduce discovery quality. It increases required revalidation frequency.

## Mandatory currentness metadata

Every shortlisted execution candidate must store:

```text
DISCOVERED_AT
LAST_SOLUTION_STATE_CHECK
LAST_ARTIFACT_CHECK
ISSUE_STATE
RELATED_PR_STATE
RELATED_FIX_COMMIT
KNOWN_WORKAROUND_STATE
UNKNOWN_HOW_STATUS
EXECUTION_SELF_SUFFICIENCY_STATUS
CANDIDATE_HALF_LIFE_RISK
```

## Activation readiness

Introduce a separate field:

`ACTIVATION_READINESS`

Do not derive it from the original Blocked Intent score.

Suggested values:

```text
READY
READY_WITH_BASELINE_CHECK
CONDITIONAL
STALE
REJECTED
```

### READY

All E1–E9 are verified at effect time and baseline has already been independently reproduced.

### READY_WITH_BASELINE_CHECK

All external/state gates pass and a public reproducer exists, but this test environment has not yet executed the frozen baseline.

### CONDITIONAL

One non-fatal execution dependency remains to be established.

### STALE

The candidate may once have been valid, but current solution/artifact state has changed.

### REJECTED

A critical Projector-test gate fails.

## Pre-activation order matters

Do not diagnose before freezing the baseline.

Correct order:

```text
CURRENTNESS CHECK
→ ARTIFACT CHECK
→ RELATED FIX / PR CHECK
→ FREEZE SOURCE SHAs
→ RUN ORIGINAL BASELINE
→ RUN PUBLISHED CONTROLS
→ PRESERVE RAW EVIDENCE
→ DEFINE DONE
→ ONLY THEN GENERATE HYPOTHESES
```

Why:

If Intelligence reads current code and begins solving before baseline freeze, the test becomes contaminated. It may:
- import a known solution;
- silently adapt the reproducer;
- change the failure condition;
- confuse a non-reproduction with a fix;
- lose the original external ground truth.

## Non-reproduction is evidence

A frozen public reproducer may fail to reproduce in a new environment.

That is not automatically a bad candidate and must not trigger ad-hoc repair.

```text
BASELINE NON-REPRODUCTION
= OBSERVATION
```

First classify:
- dependency drift;
- JDK/runtime drift;
- OS/kernel difference;
- upstream main drift;
- timing/concurrency nondeterminism;
- missing environmental assumption.

Only after classification may the Human decide whether the candidate remains worth continuing.

## New distinction: source-level versus execution-level PASS

For E4:

```text
E4-SOURCE
= public reproducer + credible independent evidence

E4-EXECUTION
= reproduced by the actual Projector test environment
```

A candidate may be selected as:

`READY_WITH_BASELINE_CHECK`

when E4-SOURCE passes but E4-EXECUTION has not yet been established.

Do not call it fully activated before E4-EXECUTION passes.

## Final scan lesson

The final scan selected `eclipse-jdtls/eclipse.jdt.ls #3866` because it currently offers:

```text
REAL HUMAN GOAL
+ LIVE BLOCKER
+ UNKNOWN HOW
+ PUBLIC REPRODUCER
+ FAIL/PASS CONTROL VARIANTS
+ ORDINARY HARDWARE
+ NO PRIVATE DATA
+ INDEPENDENT EXECUTION
+ OBJECTIVE FAILURE
+ MULTI-LAYER DEPTH
```

At selection time its activation status is:

`READY_WITH_BASELINE_CHECK`

not `ACTIVE`.

This distinction is intentional.

## Canonical sequence v1.6

```text
BLOCKED INTENT DISCOVERY
→ STRUCTURED-EVIDENCE CHECK
→ PROJECTOR TEST SUITABILITY
→ EXECUTION SELF-SUFFICIENCY
→ EFFECT-TIME SOLUTION-STATE CHECK
→ ACTIVATION READINESS
→ FREEZE SHAs
→ E4-EXECUTION BASELINE
→ DEFINE DONE
→ START REAL WORK
```

## Hard rules added

```text
OPEN ISSUE != UNSOLVED PROJECT

DISCOVERY CURRENTNESS != SOLUTION-STATE CURRENTNESS

ACTIONABLE IN PRINCIPLE != EXECUTABLE BY PROJECTOR

DISCOVERY QUALITY != ACTIVATION READINESS

E4-SOURCE != E4-EXECUTION

RADAR CARD != RESERVED UNSOLVED PROJECT
```
