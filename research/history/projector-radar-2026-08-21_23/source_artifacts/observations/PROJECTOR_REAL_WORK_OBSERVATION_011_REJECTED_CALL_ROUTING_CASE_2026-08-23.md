# PROJECTOR REAL-WORK OBSERVATION 011 — REJECTED TEST CANDIDATE: CALL ROUTING — 2026-08-23

## Candidate

Recruitment-company call-routing / branch-selection problem.

## Human clarification

Two decisive facts make this a poor current Projektor test:

1. Changes to the telephone/central-routing mechanism cannot currently be implemented.
2. Existing contact analysis already established the dominant causal mechanism: callers choose the first offices available on the list.

## Classification

```text
REAL PROBLEM = YES
UNKNOWN HOW = LOW / PARTLY RESOLVED
IMPLEMENTATION PATH = BLOCKED
FAST CLOSED LOOP = NO
SUITABLE CURRENT TEST = NO
```

## Why this matters

A useful real-work test should not merely be a real problem. It should provide a trajectory in which Projektor can:

- discover or refine HOW;
- execute or cause bounded real changes under Human authority;
- receive external feedback;
- update state;
- reroute if needed;
- reach an externally verifiable outcome.

This candidate fails because the key mechanism is already known and the available intervention path is blocked.

## Learned selection rule

```text
REAL PROBLEM
!=
GOOD PROJECTOR TEST
```

Prefer tasks with all four:

```text
UNKNOWN / NONTRIVIAL HOW
+ ACTIONABLE PATH
+ FAST EXTERNAL FEEDBACK
+ OBJECTIVE / OBSERVABLE DONE
```

Avoid selecting tasks where:
- the main cause is already established;
- implementation is impossible;
- outcome depends mainly on an unavailable owner/system;
- the work would collapse into analysis with no effect loop.

## Status

`CALL-ROUTING CASE = REJECTED AS CURRENT TEST CANDIDATE`

No product or architecture change follows from this finding.
