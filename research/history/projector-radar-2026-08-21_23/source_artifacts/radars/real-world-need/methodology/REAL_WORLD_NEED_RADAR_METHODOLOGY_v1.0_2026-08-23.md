# REAL-WORLD NEED RADAR — METHODOLOGY v1.0
## Operational methodology extracted from Discovery Runs 001–002
Date: 2026-08-23

## 1. PURPOSE

The Radar exists to detect current, real, repeatable human problems from external evidence and convert them into decision-quality opportunity candidates.

It is NOT an idea generator.

Primary objective:

```text
WORLD
→ HUMAN-REPORTED PAIN
→ INDEPENDENT VALIDATION
→ WORKAROUND
→ WTP
→ EXISTING SOLUTIONS
→ WHY THEY FAIL
→ RESIDUAL GAP
→ DECISION-QUALITY OPPORTUNITY
```

The system should be better at rejecting attractive but weak ideas than at producing large numbers of ideas.

---

## 2. CORE PRINCIPLES

### 2.1 HUMAN PAIN FIRST

A problem qualifies only when a real person describes their own pain, failure, workaround, need, or constraint.

Examples of valid pain signals:
- "I have to do this manually."
- "This stopped working."
- "I'm looking for an alternative."
- "This costs me hours every week."
- "I built my own workaround because..."
- "I pay for X but still have to..."

AI inference alone is not evidence of demand.

```text
AI-INFERRED PROBLEM != HUMAN PAIN SIGNAL
```

### 2.2 BUILDER POST != HUMAN PAIN SIGNAL

A product author / builder describing the problem their own product solves may be useful as DISCOVERY, but cannot independently validate the need.

```text
BUILDER POST
= DISCOVERY ALLOWED

BUILDER POST
!= VALIDATION

VALIDATION
= INDEPENDENT USER DESCRIBING OWN EXPERIENCE
```

This rule prevents the Radar from treating marketing copy, launch posts, founder research, or self-serving problem statements as market evidence.

### 2.3 DISCOVERY SOURCE != VALIDATION SOURCE

The source that reveals a problem should not automatically count as independent validation.

Preferred pattern:

```text
DISCOVERY:
Reddit thread A

VALIDATION:
Reddit thread B
or GitHub issue
or independent user comments
or another community/repository
```

Strong candidates should have at least 2 independent Human pain signals.

If this condition is not met:

```text
CONFIDENCE = LOW
```

### 2.4 FINDING != TASK

A discovered problem does not automatically become work.

```text
FINDING
→ QUALIFICATION
→ VALIDATION
→ DECISION

NOT:

FINDING
→ BUILD
```

This protects the project from turning every interesting signal into a new product or component.

---

## 3. SOURCE STRATEGY

Primary sources currently tested:

```text
Reddit
GitHub
```

They are complementary.

### Reddit tends to provide:
- natural language pain;
- workarounds;
- emotional intensity;
- willingness to switch;
- user comparisons;
- explicit search for alternatives;
- community confirmation.

### GitHub tends to provide:
- reproducible technical failures;
- feature requests;
- issue persistence;
- cross-product recurrence;
- workaround repositories;
- forks;
- implementation constraints;
- evidence that an issue survives contact with real systems.

Neither source alone should dominate every run.

---

## 4. RAW EVIDENCE PACKAGE

Every Opportunity Card should preserve the raw evidence necessary for replay and audit.

Required fields:

```text
URL
DATE
RAW PAIN QUOTE
ENGAGEMENT
INDEPENDENT PEOPLE COUNT
DISCOVERY SOURCE
VALIDATION SOURCE
WORKAROUND
WTP SIGNAL
EXISTING SOLUTIONS
WHY THEY FAIL
CLUSTER ID
CONFIDENCE
```

Recommended additions where available:

```text
SOURCE COMMUNITY / REPOSITORY
POST / ISSUE TITLE
AUTHOR TYPE
BUILDER / USER / MAINTAINER / CUSTOMER
REACTIONS / UPVOTES / COMMENTS
FORK / STAR / ISSUE ACTIVITY
PAID PRODUCT MENTION
CUSTOM WORKAROUND
MIGRATION / SWITCHING SIGNAL
ESTIMATED COST OF PAIN
EVIDENCE FRESHNESS
```

Raw evidence should be preserved before synthesis so future sessions can re-check the conclusion without reconstructing the search.

---

## 5. ENGAGEMENT IS SUPPORTING EVIDENCE, NOT THE OPPORTUNITY

Likes, upvotes, comments, reactions, stars, forks, citations or shares may strengthen a signal, but do not create a market by themselves.

```text
HIGH ENGAGEMENT
!=
HIGH-VALUE PROBLEM
```

Opportunity quality should instead be judged from a combination of:

```text
EXPLICIT PAIN
× RECURRENCE
× INDEPENDENT PEOPLE
× RECENCY
× WORKAROUND COST
× WTP
× EXISTING SOLUTION FAILURE
× REACHABLE BUYER
```

A low-engagement post can still be highly valuable if it contains a strong paid workaround or a severe operational failure.

---

## 6. CLUSTERING AND DEDUPLICATION

Do not count semantically equivalent posts as separate opportunities.

Example:

```text
"X is too expensive"
"what do you use instead of X?"
"I built my own replacement for X"
"X stopped syncing"
```

may belong to one underlying cluster.

Every cluster receives a stable `CLUSTER ID`.

The Radar should count:
- independent people;
- independent sources;
- independent communities/repositories;

rather than merely total posts.

```text
20 POSTS
!=
20 INDEPENDENT PROBLEMS
```

---

## 7. ANTI-BIAS MODE

Discovery Run 001 was strongly AI/devtools-heavy. This exposed a risk that the Radar could mirror the current ecosystem's vocabulary or interests.

Therefore a periodic anti-bias run should:

```text
NOT SEARCH FOR:
project-native phrases
known product names
known ecosystem concepts
previous winning opportunity labels
```

For Projektor specifically, anti-bias runs should avoid phrases such as:

```text
decision provenance
proof of run
execution truth
false success
intent review
```

and similar internal vocabulary.

A diversity gate may be used when testing general-market coverage.

Validated RUN 002 structure:

```text
MAX:
3 AI/devtools cards

MIN:
2 SMB / operations
2 consumer / prosumer
1 creator/content workflow
1 physical-world / admin / field-work niche
```

The remaining slots may be filled by the strongest evidence regardless of category.

Diversity is a diagnostic tool, not a permanent market-allocation quota.

---

## 8. OPPORTUNITY CARD QUALIFICATION

Each card should answer:

```text
WHAT EXACTLY HURTS?
WHO EXPERIENCES IT?
HOW OFTEN?
HOW MANY INDEPENDENT PEOPLE CONFIRM IT?
WHAT DO THEY DO TODAY?
WHAT DOES THE WORKAROUND COST?
DO THEY ALREADY PAY FOR THE CATEGORY?
WHAT PRODUCTS ALREADY EXIST?
WHY DO THOSE PRODUCTS FAIL?
WHAT NARROW GAP REMAINS?
HOW CONFIDENT ARE WE?
```

A card should not jump directly from pain to a proposed startup.

Preferred sequence:

```text
PAIN
→ CURRENT BEHAVIOR
→ MARKET
→ FAILURE OF CURRENT SOLUTIONS
→ RESIDUAL GAP
```

---

## 9. WTP — WILLINGNESS TO PAY

Strong WTP evidence includes:

```text
existing paid subscription
switching between paid vendors
paying a human to do the workaround
paying for plugins/tools
custom integration built internally
budget explicitly stated
business loss caused by the failure
```

Especially strong:

```text
USER BUILDS CUSTOM WORKAROUND
+
SECOND USER ASKS TO USE IT
```

This is stronger than hypothetical survey interest.

Indirect WTP should be labeled as indirect.

No WTP evidence should be reported as `UNKNOWN` rather than guessed.

---

## 10. EXISTING SOLUTIONS ARE NOT AUTOMATIC DISQUALIFICATION

A market with many existing products can be positive evidence that people already pay.

The key question is not:

```text
DOES A SOLUTION EXIST?
```

but:

```text
WHAT STILL FAILS DESPITE PEOPLE PAYING?
```

Examples from RUN 002:

- inventory management exists → residual gap may be continuity / migration / health monitoring;
- bank sync exists → residual gap may be safe ingestion / conflict preview;
- video editors exist → residual gap may be personal footage retrieval / assembly prep.

Avoid building broad categories that already exist.

```text
GENERAL PRODUCT
→ OFTEN NO-GO

NARROW FAILURE GAP
→ POSSIBLE OPPORTUNITY
```

---

## 11. DEEP VALIDATION

The TOP candidates should enter a second pass.

Required sequence:

```text
PAIN CLUSTER
→ INDEPENDENT SOURCE EXPANSION
→ BUYER
→ CURRENT SPEND / WORKAROUND
→ COMPETITORS
→ EXACT FAILURE GAP
→ TECHNICAL FEASIBILITY
→ REACHABILITY OF FIRST USERS
→ MINIMAL WEDGE
→ KILL CRITERIA
```

The purpose is NOT to justify building.

The purpose is to try to destroy the opportunity with better evidence.

```text
DEEP VALIDATION
= ATTEMPT TO KILL

SURVIVES
→ GO DEEPER

FAILS
→ PARK / REJECT
```

---

## 12. KILL CRITERIA

Kill criteria should be defined before substantial product work.

Generic examples:

```text
PAIN IS TEMPORARY / ONE-OFF
INCUMBENTS ALREADY SOLVE THE GAP
NO SEPARATE WTP
TECHNICAL ACCESS MAKES THE WEDGE TOO HEAVY
BUYERS ARE NOT REACHABLE
CUSTOMER ACQUISITION REQUIRES HEAD-ON COMPETITION WITH SUITES
EVIDENCE IS CONCENTRATED IN ONE VENDOR / COMMUNITY
WORKAROUND COST IS TOO LOW
PROBLEM FREQUENCY IS TOO LOW
```

A candidate that fails a kill criterion should be rejected or parked, not rationalized back into the ranking.

---

## 13. CONFIDENCE

Suggested confidence semantics:

```text
HIGH
= multiple independent Human signals
+ clear workaround / failure
+ strong or credible WTP
+ validated residual gap

MEDIUM
= real pain confirmed
but WTP, independence, or residual gap remains incomplete

LOW
= 1–2 primary signals
or evidence concentration
or inferred demand
or weak validation
```

`LOW CONFIDENCE` is a valid output and should not be treated as failure of the Radar.

Correct rejection is a success condition.

---

## 14. WHAT RUN 001 TAUGHT

RUN 001 proved that a scheduled/no-code workflow can perform:

```text
human-reported pain
→ clustering
→ workaround detection
→ paid-market check
→ existing-solution check
→ gap narrowing
→ TOP 3 deep validation
```

It also exposed domain/query bias because the results were heavily AI/devtools/automation-oriented.

Important result:

The workflow did not only generate ideas. It rejected broad categories:
- generic AI memory;
- generic cost caps;
- generic scheduler monitoring;

and narrowed them to specific residual gaps.

---

## 15. WHAT RUN 002 TAUGHT

RUN 002 applied anti-bias and diversity constraints.

Its TOP 3 changed to:

```text
1. Multichannel Inventory Continuity
2. Bank Import Safety Layer
3. Creator Rough-Cut + Personal Footage Retrieval
```

This materially reduced the concern that the Radar merely mirrors the Projektor ecosystem.

The most important methodological result:

```text
THE QUALIFICATION GATES CHANGED THE RANKING
```

Large or dramatic pains did not automatically win.

Examples that did NOT become TOP candidates:
- Meta Business lockout;
- Home Assistant failures;
- generic home asset apps;
- generic AI video editing.

This is desired behavior.

---

## 16. CURRENT RADAR MATURITY

Current evidence supports:

```text
REAL-WORLD NEED RADAR
= WORKING OPERATIONAL CAPABILITY

DISCOVERY
= PASS

ANTI-BIAS
= PASS

EVIDENCE PACKAGING
= PASS

SEPARATE CRAWLER / SCANNER
= NOT YET JUSTIFIED
```

The scheduled ChatGPT workflow is currently sufficient as the MVP implementation.

Do not build infrastructure simply because it is technically possible.

---

## 17. AUTOMATION / SCANNER GATE

A dedicated scanner should only be considered when all are true:

```text
USEFUL OPPORTUNITIES ARE FOUND REPEATEDLY
+
THE MANUAL / SCHEDULED WORK IS REPETITIVE
+
SOURCE ACCESS AND TERMS ALLOW AUTOMATION
+
DEDUPLICATION / SCORING CAN BE MADE RELIABLE
+
AUTOMATION REMOVES A MEASURED HUMAN COST
```

Until then:

```text
AVAILABLE TOOL != REQUIRED TOOL
```

and:

```text
SCHEDULED CHATGPT TASK
+ SEARCH
+ EVIDENCE RULES
= CURRENT MVP
```

---

## 18. PROJECTOR DEVELOPMENT CONSEQUENCE

The Radar is a case of the broader Projektor rule:

```text
PROJECTOR WORKS
→ REALITY RETURNS EVIDENCE
→ REPEATED / MEASURED BLOCKER?
    NO  → CONTINUE WORK
    YES → MINIMUM REPAIR
```

Do not convert a successful operational workflow into new architecture by default.

```text
WORKING CAPABILITY
!=
NEW COMPONENT REQUIRED
```

---

## 19. CURRENT NEXT QUESTION

The remaining proof is no longer:

```text
CAN THE RADAR FIND INTERESTING PROBLEMS?
```

The next question is:

```text
CAN ONE FINDING SURVIVE
BUYER / MARKET / COMPETITOR / TECHNICAL / EXECUTION VALIDATION
AND BECOME A DECISION-QUALITY OPPORTUNITY?
```

Current candidate for that test:

```text
MULTICHANNEL INVENTORY CONTINUITY
```

This candidate should be challenged using the full Deep Validation and Kill Criteria process before any product-development decision.

---

## 20. CANONICAL SHORT FORM

```text
REAL HUMAN PAIN
→ INDEPENDENT VALIDATION
→ DEDUP / CLUSTER
→ WORKAROUND
→ WTP
→ EXISTING SOLUTIONS
→ WHY THEY FAIL
→ RESIDUAL GAP
→ CONFIDENCE
→ TOP CANDIDATES
→ DEEP VALIDATION
→ KILL / PARK / GO DEEPER
```

And the two most important safeguards:

```text
BUILDER POST != HUMAN PAIN SIGNAL
FINDING != TASK
```
