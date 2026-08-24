# PROJECTOR REAL-WORK OBSERVATION 006 — KYC / SENSITIVE IDENTITY AUTHORITY GATE — 2026-08-23

## Source

Human-supplied live Freelancer.com KYC screen during the first-real-revenue trajectory.

## Context

The current activity is still a real-work test / first-revenue attempt. Reaching the Freelancer bid path exposed a new external requirement before continuation.

The KYC screen requests:
- government-issued identity document;
- photo/selfie with a unique code and identity document;
- proof of residential address.

## Human observation

The Human explicitly identified this as a materially larger step than ordinary profile setup:

> submitting an identity document to "some website" is a very large step, especially while this remains part of a test.

## Classification

```text
OBS-006:
SENSITIVE IDENTITY DISCLOSURE GATE

TYPE:
HUMAN PRIVACY / IDENTITY / AUTHORITY GATE

SEVERITY:
HIGH

REVERSIBILITY:
LOWER THAN ORDINARY PROFILE EDITING

CURRENT AUTHORITY:
NOT GRANTED

KYC SUBMISSION:
DO NOT PROCEED

NEW COMPONENT REQUIRED:
NO

NEW SESSION REQUIRED:
NO

REROUTE REQUIRED:
YES
```

## Important distinction

```text
REAL HUMAN GATE
!=
AUTOMATIC PERMISSION TO CROSS IT
```

The fact that a platform requires identity verification does not mean the Human has authorized disclosure of sensitive identity documents merely because the current goal is first revenue.

The correct behavior is:

```text
GOAL
→ PATH
→ SENSITIVE-DATA GATE APPEARS
→ STOP
→ HUMAN DECIDES WHETHER THE PRIVACY/IDENTITY COST IS ACCEPTABLE
```

If Human does not explicitly authorize the disclosure:

```text
DO NOT PUSH THROUGH
→ PRESERVE GOAL
→ CHANGE HOW
```

## New operating rule

### SENSITIVE IDENTITY DISCLOSURE RULE

Before any action involving:
- government ID;
- passport;
- driver's license;
- selfie/biometric-style verification;
- proof of residential address;
- tax identity;
- banking identity;
- other high-sensitivity personal documentation;

Projektor must treat the step as a distinct Human authority gate.

It must not:
- normalize the disclosure as "just another signup step";
- imply that completing the goal requires accepting it;
- pressure the Human to proceed;
- silently broaden authorization from "create/use an account" to "submit sensitive identity documents".

## Recommended continuation

Preserve the same goal:

`FIRST REAL EXTERNAL REVENUE`

But add a temporary constraint:

`NO NEW HIGH-SENSITIVITY IDENTITY DISCLOSURE FOR THIS TEST`

Then reroute toward channels where the Human can legitimately act without submitting new government-ID/address documentation solely for this experiment.

Possible route classes to evaluate:
- existing accounts/platforms already verified by Human;
- direct outreach using existing legitimate communication channels;
- opportunities where payment can be received without new high-sensitivity KYC at the discovery/bid stage;
- local/direct business opportunities;
- other marketplaces only after their verification requirements are checked before profile-building work.

## Lesson for future sessions

Verify **platform entry costs and authority requirements early enough** to avoid investing profile-building effort before discovering a high-cost gate.

New sequencing:

```text
TARGET CHANNEL
→ CHECK ENTRY / KYC / PAYMENT / IDENTITY REQUIREMENTS
→ HUMAN ACCEPTS COST?
   NO → REJECT CHANNEL EARLY
   YES → continue setup
```

This does not invalidate the Freelancer work already done; it exposes a previously unknown real-world constraint.

## Status

```text
GOAL:
UNCHANGED

FREELANCER PATH:
BLOCKED BY UNAUTHORIZED SENSITIVE-ID KYC

NEXT:
REROUTE, DO NOT RESET

DEVELOPMENT:
NO
```
