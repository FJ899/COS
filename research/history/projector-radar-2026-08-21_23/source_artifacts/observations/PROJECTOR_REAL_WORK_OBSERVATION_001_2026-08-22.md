# PROJECTOR REAL-WORK OBSERVATION 001 — TOOL-FIRST DRIFT

Date: 2026-08-22
Status: OBSERVED / CORRECTABLE / NOT A PRODUCT BLOCKER
Source: first real-work session after post-test reconciliation

## Context
Human goal: reach the first real external payment using current Human + AI capabilities, without assuming a product, market, or method in advance.

The session began correctly by trying to establish actual available assets/capabilities and current market demand. It explicitly treated unconfirmed items as UNKNOWN and avoided inventing access to unavailable repositories.

## Observation
Before establishing a concrete evidence need that required email access, the session attempted to invoke/connect Gmail while still performing broad current-state / asset discovery.

This created a permission prompt even though no specific hypothesis had yet been established for which Gmail was the necessary or best evidence source.

## Classification
LOCAL CORRECTABLE ERROR

Not:
- architecture failure;
- capability failure;
- reason to restart the project;
- reason to add a new component;
- reason to grant broader permissions.

## Failure pattern

AVAILABLE TOOL
→ MAY BE USEFUL
→ REQUEST ACCESS

This is the wrong order.

## Preferred rule

GOAL
→ CURRENT STATE
→ CRITICAL UNKNOWN
→ REQUIRED EVIDENCE
→ BEST SOURCE
→ MINIMUM TOOL / PERMISSION

Therefore:

AVAILABLE TOOL != REQUIRED TOOL

A connector or permission should be requested only when a specific decision-relevant unknown has been identified and that connector is the minimum reasonable source needed to resolve it.

## Correct behavior in this case
Do not connect Gmail yet.
Continue the task using currently available evidence and tools.
If the work later establishes a concrete hypothesis such as "existing warm contacts may be the fastest path to first payment" and email is the best available source for validating that hypothesis, then request Gmail access with an explicit reason and expected evidence.

## Continuity implication
Do NOT restart the session because of this error.
A useful Projektor should be able to accept the correction, update HOW, preserve GOAL, and continue from the existing state.

Restarting immediately would erase evidence about whether the system can self-correct and reroute after Human feedback.

## Escalation condition
Treat this as a measured blocker only if the same TOOL-FIRST pattern repeats materially after this correction, especially if it repeatedly asks for broad permissions before establishing a concrete evidence need.

If repeated:
- record repeated failure;
- classify as collaboration / evidence-selection friction;
- then consider the smallest semantic guard.

Until then:
FINDING != TASK.

## Next-session recovery note
When resuming real work, preserve this rule:

TOOL REQUEST MUST BE JUSTIFIED BY A SPECIFIC CURRENT UNKNOWN.

Do not enumerate or connect available tools simply because they exist.
