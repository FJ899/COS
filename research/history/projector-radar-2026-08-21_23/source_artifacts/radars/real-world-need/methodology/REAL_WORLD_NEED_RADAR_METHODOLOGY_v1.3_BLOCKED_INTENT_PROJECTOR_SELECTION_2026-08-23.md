# REAL-WORLD NEED RADAR — METHODOLOGY v1.3
## Blocked Intent / Projector Test Candidate Selection
Date: 2026-08-23

## 1. Why this revision exists

Five independent BLOCKED INTENT RADAR runs were compared:

- Test 2 A
- Test 2 B
- Test 2 Gemini
- Test 2 Genspark
- Test 2 Grok

The scan target was shifted from:

`I have a problem and do not know how to solve it`

to:

`I know what I want, I already tried, I have a concrete blocker, and I am missing capability / knowledge / HOW.`

The shift worked. All five systems found cases with:
- explicit Human goal;
- non-zero current state;
- real prior effort;
- concrete blocker;
- observable outcome.

## 2. Main finding

The BLOCKED INTENT formulation is better suited to finding a real Projector test case than a pure pain/opportunity scan.

Why:

```text
PAIN RADAR
→ proves that a problem exists

BLOCKED INTENT RADAR
→ gives us an active trajectory
```

A strong blocked-intent case already contains:

```text
HUMAN INTENT
+ CURRENT STATE
+ ATTEMPT HISTORY
+ UNKNOWN HOW
+ ACTIONABLE NEXT EXPERIMENT
+ EXTERNAL FEEDBACK
```

This is much closer to the operating loop Projector is intended to support.

## 3. New bias discovered

The Blocked Intent contract strongly favors GitHub-style cases.

Reason:

GitHub issues naturally expose:
- reproducible current state;
- exact environment;
- attempted fixes;
- logs / traces;
- source code;
- deterministic failure;
- objective verification.

Reddit contains more pain, ideas, advice requests and one-answer troubleshooting, so many Reddit cases are filtered out.

Therefore:

```text
BLOCKED INTENT QUALITY SCORE
is partly a score of
HOW WELL THE HUMAN DOCUMENTED THE BLOCKER
```

not only how valuable or deep the underlying project is.

New bias label:

`STRUCTURED-EVIDENCE BIAS`

This must not be confused with actual project suitability.

## 4. Five-run best single cases

### Test 2 A
FreeCAD Assembly Slider collapse.

Strengths:
- production-derived model;
- deterministic reproducer;
- no special hardware;
- can act without original author for diagnosis;
- multiple competing hypotheses;
- binary regression result.

### Test 2 B
GS-DIFF / PGSR reproduction gap.

Strengths:
- numeric external metric;
- working pipeline;
- multiple prior approaches;
- real research uncertainty.

Risks:
- missing unpublished settings;
- compute/environment burden may be material.

### Gemini
Watermark-resistant PDF OCR for RAG.

Strengths:
- concrete pipeline;
- observable text-quality result.

Risks:
- primary cited case appears older than preferred window;
- freshness/current activity is weaker;
- grounding/source presentation is less clean than the strongest GitHub cases.

### Genspark
Paper reproduction gap, ~73% vs ~77%.

Strengths:
- scientific method required;
- failure can still produce useful evidence;
- no platform owner on critical path.

Risks:
- older case admitted exceptionally;
- identity/paper/dataset details are incomplete;
- compute cost may create an execution barrier.

### Grok
Custom microWakeWord on Home Assistant Voice PE.

Strengths:
- purchased hardware;
- two prior model attempts;
- clear last-mile blocker;
- immediate binary physical feedback.

Risks:
- final verification requires the owner's physical device;
- signed firmware/platform constraints could turn it into a platform-owner gate.

## 5. New distinction: good Blocked Intent vs good Projector test

A case can score highly as BLOCKED INTENT and still be a poor Projector test.

Add a second qualification layer:

`PROJECTOR_TEST_SUITABILITY`

Required dimensions:

```text
P1 PUBLIC / ACCESSIBLE ARTIFACTS
P2 CAN ACT WITHOUT ORIGINAL HUMAN ON EVERY STEP
P3 MULTI-STEP UNKNOWN HOW
P4 FAST OBJECTIVE FEEDBACK
P5 FAILURE DOES NOT END THE PROJECT
P6 NO RARE / UNAVAILABLE HARDWARE
P7 NO INCUMBENT-ONLY CRITICAL ACTION
P8 EXTERNAL VERIFICATION IS POSSIBLE
P9 ENOUGH DEPTH FOR MULTI-SESSION CONTINUITY
P10 SAFE / REVERSIBLE FIRST EXPERIMENT
```

This is different from market attractiveness and from technical difficulty.

## 6. Current cross-run meta-ranking for Projector test suitability

### #1 — FreeCAD Assembly Slider collapse

Current strongest candidate.

Why:
- public issue + reproducer;
- no rare hardware;
- deterministic baseline;
- real production-derived artifact;
- author already exhausted obvious paths;
- original vs relinked/healed vs synthetic cases create a strong hypothesis space;
- experiments can proceed without waiting for platform owner;
- success can become a regression test;
- failure of one hypothesis produces information rather than blocking the path.

Most important shape:

```text
OBSERVATION IS STRONG
EXPLANATION IS MISSING
ACTION IS AVAILABLE
REALITY CAN ANSWER
```

This is an unusually clean Projector test.

### #2 — GS-DIFF / PGSR reproduction gap

Excellent scientific-loop candidate, but compute/config dependency is higher.

### #3 — Paper reproduction 73% vs 77%

Strong research methodology test, but weaker freshness and potentially heavier compute burden.

### #4 — Custom microWakeWord

Excellent physical-world feedback loop, but owner/device is on the critical path.

### #5 — FreeCAD headless CAM

Very strong execution case; may be shallower if the defect collapses quickly to a local lifecycle bug or is already fixed in a recent weekly build.

## 7. Important lesson from lack of exact cross-system recurrence

The five scans did not converge on one identical project.

That is not a failure.

The purpose of this stage is not consensus voting.

Different search systems exposed different portions of the live project space.

Therefore:

```text
CROSS-AI AGREEMENT
is useful for recurrence,
but is NOT required
for selecting a Projector test case.
```

For a test candidate we should choose based on evidence accessibility and trajectory quality, not popularity among scanners.

## 8. Candidate selection rule

For the next real Projector case, prefer:

```text
REAL HUMAN GOAL
+ PUBLIC CURRENT STATE
+ REAL PRIOR ATTEMPTS
+ UNKNOWN NONTRIVIAL HOW
+ ARTIFACTS WE CAN ACCESS
+ FIRST EXPERIMENT WE CAN RUN OURSELVES
+ OBJECTIVE FEEDBACK
+ MULTIPLE POSSIBLE REROUTES
+ EXTERNAL FINAL VERIFICATION
```

Avoid:

```text
needs proprietary hardware we do not have
needs hidden company data
needs the original Human for every experiment
depends on platform-owner permission
can be solved by one documentation lookup
is only a feature request
has no stable baseline
```

## 9. Current recommendation

`FREECAD ASSEMBLY SLIDER COLLAPSE`

is the strongest current candidate for the next Projector real-work validation.

Before activation, do one narrow preflight only:

```text
1. confirm issue is still open/current;
2. confirm reproducer/artifacts are actually retrievable;
3. confirm current FreeCAD revision still reproduces;
4. freeze original issue state and expected failure;
5. define DONE without designing the solution.
```

If any of 1–3 fails, do not repair the candidate selection. Move to the next candidate.

## 10. Canonical rule

```text
BLOCKED INTENT RADAR
FINDS PROJECTS

PROJECTOR_TEST_SUITABILITY
SELECTS THE TEST
```

Do not use the Blocked Intent score alone as the final selection criterion.
