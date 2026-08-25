# HOT — standalone Human Orchestration Tax experiment track

Status: `PARKED ALTERNATIVE / NOT ACTIVE TASK / NOT IMPLEMENTATION AUTHORITY`
Recorded: `2026-08-25`
Decision baseline: `FJ899/COS main@bfc1b5a1120e8d7d9c44228f8ddb7b264d0c4a19`
Related accepted change: PR `#44`, merged from authorized head `445dfbdf0b42d91d5fc384621155c636ef302dd4`

## Why this record exists

A separate HOT program was considered as a way to measure how much operational intelligence the Human must supply for the system to keep work moving.

The useful research question remains:

```text
How much operational intelligence does the Human have to supply
for the system to preserve intent and reach a real outcome?
```

The rejected step is **not the HOT hypothesis itself**. The rejected step is activating HOT now as a separate implementation/program track with its own instrumentation before the current real P1 target has been bound and observed.

## Rejected path for now

```text
HOT-001 design
-> build / add passive logging or HOT-specific instrumentation
-> run HOT baseline
-> HOT-002 minimal intervention
-> A/B
-> transfer study
```

when performed **before** a real P1 target and its local current state create evidence that such machinery is necessary.

## Current canonical context

At the decision baseline, canonical P1 is already:

```text
P1 — Intent-to-Outcome primary run on one real Human project
STATUS: CURRENT PRIORITY
```

Its accepted run contract already requires the system to:

- bind the real target;
- identify the current critical unknown;
- use only what naturally helps;
- preserve material evidence and state changes;
- re-route when evidence changes the path;
- record continuity breaks;
- record Human rescue events when the Human had to provide an operational next step rather than a genuine Human-owned decision;
- avoid treating architecture production as task progress.

Therefore a separate HOT runtime or logging implementation is not currently required to begin measuring the phenomenon of interest.

## Why this path is parked

### 1. Experiment design is not a target implementation assumption

```text
EXPERIMENT DESIGN
!=
TARGET IMPLEMENTATION ASSUMPTION
```

Knowing what should be observed does not establish where a logger belongs, whether new code is needed, or which local project owns the evidence surface.

### 2. Portfolio hypothesis is not local project truth

```text
PORTFOLIO HYPOTHESIS
!=
LOCAL PROJECT TRUTH
```

Before a real target is bound and reconciled, adding instrumentation would require guessing local architecture and ownership.

### 3. The current P1 contract already captures the key observation

`Human rescue events` are already a required observation surface in the accepted P1 run contract. The first real run should establish whether that observation mechanism is sufficient before a dedicated experimental subsystem is introduced.

### 4. Avoid test-created need

A separate HOT implementation created only to run HOT can create this loop:

```text
TEST CREATES NEED
-> NEED CREATES IMPLEMENTATION
-> IMPLEMENTATION CREATES NEW TEST
```

That conflicts with the current behavior-first rule that new mechanisms enter only under observed pressure from real work.

### 5. Preserve baseline purity

For the first P1 run, an observer/evidence record outside the studied runtime may be enough. Adding instrumentation before the baseline could change the very orchestration burden being measured.

### 6. Do not fork the current global priority

HOT is a useful measurement lens on P1. Turning it into a parallel active program now risks replacing the real Human project with ecosystem-development work.

## Valuable material preserved for possible future use

The following ideas remain potentially useful and are deliberately preserved:

```text
HUMAN ORCHESTRATION TAX

LEGITIMATE HUMAN INPUT
vs
HUMAN OPERATIONAL RESCUE

R0–R4 rescue severity / dependency scale

RESCUE DEPENDENCY

A/B comparison after a measured intervention

TRANSFER evaluation on an independent real task
```

These concepts are **candidate measurement constructs**, not current canonical product requirements and not evidence by themselves.

## Evidence discipline if HOT returns

Future HOT work should preserve these distinctions:

```text
Human Rescue transcript
!=
classified Rescue

classified Rescue
!=
proof of counterfactual impact

AI says DONE
!=
External / observable DONE

CHAT CLAIM
!=
CURRENT REPOSITORY FACT
```

A rescue classification should identify observable evidence and distinguish genuine Human-owned authority/normative decisions from operational steering the system should reasonably have supplied itself.

## Return conditions

Re-open formal HOT work only if at least one of the following becomes true:

1. a real P1 run produces repeated, material Human operational rescue that is not explained by genuine Human-owned authority gates;
2. the existing P1 observation record cannot reliably distinguish legitimate Human input from operational rescue;
3. a measured intervention is proposed and an A/B-style comparison is needed to determine whether it reduces Human orchestration burden without weakening Human semantic authority;
4. the Human explicitly activates HOT as a formal research/product experiment.

If none of these conditions occurs, keep HOT as an analytical lens and do not create dedicated architecture for it.

## What to avoid

Do not:

- add a HOT logger, router, scheduler, agent or runtime before a real observed need;
- choose a target repository merely because it appears convenient for instrumentation;
- treat a transcript as already-classified evidence;
- treat a rescue count alone as proof that the system caused the rescue;
- treat HOT as a replacement for the current P1 product direction;
- promote measurement constructs into product requirements without evidence.

## Preferred near-term path instead

```text
CANONICAL P1
-> real Human project
-> bind exact target
-> local read-only current-state reconciliation
-> freeze RAW INTENT / GOAL / effect-based DONE / VERIFICATION
-> run ecosystem AS-IS
-> preserve Human rescue and continuity evidence
-> inspect measured friction
-> only then decide whether formal HOT instrumentation or experiment is needed
```

This archive is intentionally non-canonical for current work. It preserves an alternative research path and a set of failure modes to avoid.
