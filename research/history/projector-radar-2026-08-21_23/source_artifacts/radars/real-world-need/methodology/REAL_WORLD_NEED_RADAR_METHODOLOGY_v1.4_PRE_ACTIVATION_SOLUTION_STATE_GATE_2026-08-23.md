# REAL-WORLD NEED RADAR — METHODOLOGY v1.4
## Pre-Activation Currentness / Solution-State Gate
Date: 2026-08-23

## Trigger

A read-only preflight was authorized for:

`BIR-01 — FreeCAD Assembly Slider Collapse`

The candidate had been ranked as the strongest Projector live-test candidate because discovery evidence showed:
- real production-derived artifact;
- deterministic reproducer;
- strong attempt history;
- unknown root cause;
- accessible source;
- objective feedback.

Effect-time preflight changed the state materially.

## Evidence found at preflight

Issue:
`FreeCAD/FreeCAD #31855`

The issue is still OPEN.

However, a later issue comment states that the author:
- instrumented FreeCAD/Assembly/OndselSolver;
- found the root cause in `JointObject.py -> Joint.matchJCS()`;
- ruled out the originally suspected mbD solver;
- identified the precise pre-solve mechanism;
- implemented a local fix;
- verified that the 7 panel positions remain distinct after recompute.

The current FreeCAD main branch still contains the old full-JCS `matchJCS()` transform, so the local patch does not appear to have been merged upstream at preflight time.

Therefore:

```text
ISSUE STATE = OPEN
PROBLEM ROOT CAUSE = FOUND
LOCAL FIX = VERIFIED
UPSTREAM FIX = NOT MERGED
UNKNOWN HOW = NO LONGER TRUE
```

## Candidate verdict

```text
BIR-01
= REJECTED AS PROJECTOR UNKNOWN-HOW TEST

WHY:
the real Human project has already crossed the discovery / explanation / local-fix boundary.

OPEN ISSUE
!=
UNSOLVED PROJECT
```

Implementing or independently rediscovering the already-published fix would no longer be a clean test of:

`HUMAN INTENT → UNKNOWN HOW → DISCOVERY → DECISION → ACTION → FEEDBACK`

It would instead be closer to:
- replay;
- implementation verification;
- upstreaming;
- regression-hardening.

Those may be useful tasks, but they are a different test.

## Fallback check #1

`BIR-02 — FreeCAD CAM #31849`

Preflight showed:
- issue remains open;
- later comments corrected the original problem statement;
- the real trigger is multiple Tool Controllers, not headless execution generally;
- a public PR already exists: `FreeCAD/FreeCAD #31863`;
- the issue author confirmed that the PR addresses the main bug;
- a working ordering workaround is documented.

Therefore:

```text
BIR-02 MAIN BLOCKER
= SUBSTANTIALLY RESOLVED / PR EXISTS

UNKNOWN HOW
= TOO LOW FOR CLEAN PROJECTOR TEST
```

A secondary Proxy-less-object hang remains a separate possible problem, but selecting it would create a new local goal rather than continue the originally ranked case.

## Fallback check #2

`BI-01 — GS-DIFF / PGSR reproduction gap`

Issue:
`Chumsy0725/GS-DIFF #2`

Preflight showed:
- issue is open;
- a second independent user reports the same reproduction gap;
- no public solution is present in comments;
- HOWEVER the public repository at current main contains only `README.md` and `LICENSE`;
- the implementation / scenes / experiment artifacts required to reproduce the reported 0.2–0.3 vs 0.6+ gap are not present in the public repo.

Therefore:

```text
PROBLEM = LIVE
UNKNOWN HOW = LIVE
PUBLIC EXECUTION ARTIFACTS = INSUFFICIENT

PROJECTOR TEST SUITABILITY
= FAIL / CURRENTLY NOT ACTIONABLE WITHOUT ORIGINAL HUMAN ARTIFACTS
```

## New methodology rule

The Radar previously checked:
- issue freshness;
- open/closed status;
- artifact availability at discovery time.

That is not enough.

Add a mandatory **PRE-ACTIVATION SOLUTION-STATE GATE**.

Immediately before selecting a case for execution, re-read:

```text
ISSUE BODY
LATEST COMMENTS
RELATED PRs
RELATED COMMITS
CURRENT REPO HEAD
ATTACHMENT AVAILABILITY
KNOWN WORKAROUNDS
LOCAL FIX CLAIMS
```

Then re-evaluate:

```text
GOAL STILL ACTIVE?
BLOCKER STILL ACTIVE?
UNKNOWN HOW STILL UNKNOWN?
ARTIFACTS STILL ACCESSIBLE?
NO FIX ALREADY EXISTS?
CAN WE ACT NOW?
```

## Hard invariant

```text
OPEN ISSUE != UNSOLVED PROJECT
```

and:

```text
DISCOVERY CURRENTNESS
!=
SOLUTION-STATE CURRENTNESS
```

and:

```text
UNKNOWN HOW
MUST BE REVALIDATED
AT ACTIVATION TIME
```

## Why this matters

For fast-moving GitHub projects, the strongest candidates can become stale within hours or days:
- a maintainer comments with the root cause;
- another contributor opens a PR;
- the author finds a workaround;
- a patch exists locally but issue state remains open;
- attachments disappear;
- current main changes behavior.

Therefore the final Projector test candidate cannot be chosen from a cached Radar card alone.

## Revised selection sequence

```text
BLOCKED INTENT RADAR
→ PROJECTOR TEST SUITABILITY
→ PRE-ACTIVATION SOLUTION-STATE GATE
→ FREEZE BASELINE
→ START REAL WORK
```

No solution design may begin before the solution-state gate passes.

## Current operational state

```text
BIR-01 FREECAD SLIDER
= REJECTED BY PREFLIGHT

BIR-02 FREECAD CAM
= REJECTED AS MAIN UNKNOWN-HOW CASE

BI-01 GS-DIFF
= LIVE BUT ARTIFACT-INCOMPLETE

PRIMARY LIVE TEST
= NOT YET ACTIVATED
```

This is a successful preflight outcome: it prevented Projector from testing itself against a problem whose solution state had already changed.
