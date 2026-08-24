# REAL-WORLD NEED RADAR — METHODOLOGY v1.2
## Multi-System / Model-vs-Retrieval Control
Date: 2026-08-23

## Purpose of this revision

The Radar experiment was expanded from an environment A/B test into a five-arm comparison:

- Run A
- Run B
- Gemini
- Genspark
- Grok

The purpose is now twofold:

1. test whether the working environment/context changes Radar output;
2. test whether different AI systems produce materially different discovery and validation results under the same nominal prompt.

This extension exposed a critical methodological distinction:

```text
AI MODEL EFFECT
!=
AI SYSTEM EFFECT
```

A real external AI product is not only a model. It is:

```text
AI SYSTEM
= MODEL
+ SEARCH / RETRIEVAL ENGINE
+ INDEX / CRAWL ACCESS
+ TOOL LIMITS
+ RATE LIMITS
+ SOURCE ACCESSIBILITY
+ QUERY GENERATION
+ EVIDENCE PARSING
+ REASONING / CLUSTERING / RANKING
```

Therefore cross-provider differences in blind web discovery must initially be classified as SYSTEM EFFECT, not pure MODEL EFFECT.

---

## Observed five-run portfolio

### RUN A

Qualified clusters: 8.

Top:
1. Prior authorization workload & denial escalation — GO DEEPER
2. M365 tenant lockout — PARK
3. AI coding session/work durability — WATCH

Characteristics:
- broad category distribution;
- Reddit dominant but not one community;
- deep validation materially changed opportunity ranking;
- context-influence self-check: NO.

### RUN B

Qualified clusters: 7.

Top:
1. Agent-driven destructive actions / silent work-state loss — GO DEEPER
2. Cloud billing/remediation traps — WATCH
3. Delivery-platform disruption of restaurant front-of-house — WATCH

Characteristics:
- moderate concentration in software/platform/cloud/identity/workplace IT;
- Reddit dominant, GitHub exceptionally strong for C01;
- problem confidence frequently remained HIGH while opportunity confidence fell;
- context-influence self-check: NO.

### GEMINI

Qualified clusters: 3.

Top:
1. Unrecovered CI/CD deadlocks & runner wedges — WATCH
2. Local AI agent shell / credential context bleed — WATCH
3. KV-cache / MoE memory paging latency — DROP

Characteristics:
- very strong infrastructure/devtools concentration;
- very narrow portfolio;
- deep validation correctly killed low-software-WTP / incumbent-fix candidates;
- context-influence self-check: NO.

Important methodology concern:
some card-level `VALIDATION SOURCE` fields cite third-party/post-mortem/security-comparison material rather than only independent Reddit/GitHub Human pain. This should be treated as weaker compliance with the frozen source protocol, even if such sources are useful as background evidence.

### GENSPARK

Qualified clusters: 9.

Top:
1. SaaS acquisition/repricing → logic-preserving migration — GO DEEPER
2. eBay ad-fee opacity — PARK
3. SharePoint Alerts retirement without 1:1 replacement — WATCH

Characteristics:
- strong `platform risk` fingerprint;
- Reddit ~85% of evidence;
- strong kill logic on platform-controlled ground truth;
- context-influence self-check: NO.

Important methodology concern:
the run openly relied on substantial AUX evidence outside the strict window. One cited cross-community validation item is dated/updated before 24 July while being discussed as in-window support. This does not invalidate the full run, but reduces comparability with stricter runs.

### GROK

Qualified clusters: 7.

Top:
1. Paid AI-coding usage opacity / hidden quota burn — WATCH
2. Prior authorization workload despite ePA — PARK
3. Copay accumulator/maximizer pain — WATCH

Characteristics:
- devtools/AI coding + healthcare concentration;
- no TOP-3 candidate survived as GO DEEPER;
- strong adversarial kill discipline;
- source accessibility materially shaped the portfolio;
- context-influence self-check: NO.

---

## Cross-run recurrence

### Strong exact / near-exact recurrence

#### PRIOR AUTHORIZATION

Appears independently in:
- Run A — TOP 1 / GO DEEPER
- Grok — TOP 2 / PARK

Interpretation:

```text
PROBLEM RECURRENCE = STRONGER
OPPORTUNITY VERDICT = UNSTABLE
```

This is especially valuable because different systems agree that the pain is real but disagree on how much monetizable residual gap survives validation.

This is the kind of cross-system disagreement the Radar should preserve rather than average away.

### AI CODING / AGENT FAILURE FAMILY

Appears across:
- Run A — session/work durability;
- Run B — destructive actions / state loss;
- Gemini — shell/credential context bleed;
- Grok — hidden quota / usage opacity.

These are not one exact cluster.

They share a domain and a higher-level failure family:

```text
AGENTIC TOOL
→ CONSEQUENCE / STATE / COST
→ USER HAS INCOMPLETE CONTROL OR GROUND TRUTH
```

Do NOT merge these automatically.

Classification:

```text
DOMAIN RECURRENCE = HIGH
EXACT PROBLEM RECURRENCE = PARTIAL
SOURCE-DENSITY RISK = HIGH
```

Reddit + GitHub naturally over-represent developer problems, so repeated AI/devtool findings cannot by themselves prove context contamination or a giant unified market.

### TENANT / IDENTITY / PLATFORM LOCKOUT

Related mechanisms recur across:
- Run A — M365 tenant lockout;
- Run B — mission-critical SaaS tenant lockout / account recovery;
- Grok — identity-provider lockout with no working human recovery path.

This supports a broader repeated pain mechanism:

```text
DEPENDENCY ON VENDOR CONTROL PLANE
+
FAILURE OF NORMAL RECOVERY / ESCALATION
```

But monetizable third-party opportunity remains weak when the incumbent alone controls reactivation.

---

## Environment effect — current interpretation

The A/B pair does NOT show simple deterministic environment lock-in.

The two outputs differ materially in top-ranked domains, but also share meaningful mechanisms.

Therefore:

```text
ENVIRONMENT EFFECT = POSSIBLE / NON-ZERO
ENVIRONMENT DOMINANCE = NOT ESTABLISHED
```

A different context may alter:
- which generic queries are generated first;
- which source branch is followed;
- which cluster receives enough early evidence to trigger expansion;
- naming and interpretation.

But the current evidence does not show that one environment forces the Radar to reproduce the user's existing project topics.

---

## System effect — clearly observed

The five runs show major differences in:

- number of qualified clusters (3–9);
- category distribution;
- Reddit vs GitHub weighting;
- strictness of temporal filtering;
- external-source use;
- candidate survival after deep validation;
- ability to find non-technical problems.

This demonstrates:

```text
AI SYSTEM EFFECT = LARGE
```

But it does NOT isolate pure model reasoning.

The search/retrieval layer clearly differed between systems:
- some reported GitHub rate limits;
- some relied on public web search rather than API-like access;
- some could not fully enumerate Reddit threads;
- some could load GitHub Community pages more reliably than Reddit;
- some used outside background sources differently.

Therefore no conclusion like:

```text
"MODEL X IS BETTER AT OPPORTUNITY DISCOVERY"
```

is yet justified from this experiment alone.

The correct current claim is:

```text
"SYSTEM X PRODUCED THIS PORTFOLIO
UNDER ITS OWN RETRIEVAL / TOOL CONDITIONS."
```

---

## Two-stage test required to separate discovery from reasoning

### STAGE 1 — SYSTEM DISCOVERY TEST

Each AI system receives the identical frozen prompt and searches independently.

Purpose:

```text
MEASURE FULL PRODUCT / SYSTEM PERFORMANCE
```

This intentionally includes:
- search quality;
- access;
- query generation;
- browsing;
- filtering;
- clustering;
- validation.

Metrics:

```text
QUALIFIED CLUSTERS
VALID IN-WINDOW EVIDENCE RATE
INDEPENDENT-HUMAN-SIGNAL RATE
RAW-EVIDENCE COMPLETENESS
SOURCE-PROTOCOL COMPLIANCE
PROBLEM CONFIDENCE QUALITY
OPPORTUNITY CONFIDENCE QUALITY
TOP-3 SURVIVAL AFTER KILL
PRODUCT-DEFECT FALSE PROMOTION RATE
```

### STAGE 2 — FROZEN EVIDENCE MODEL TEST

Build one deduplicated UNION EVIDENCE CORPUS from all Stage-1 runs.

No system is allowed to search the web.

Every AI receives exactly the same:
- sources;
- dates;
- quotes;
- engagement;
- WTP evidence;
- workaround evidence;
- competitor facts;
- technical constraints.

Then each system must independently:

```text
CLUSTER
→ SCORE
→ RANK
→ DEEP VALIDATE
→ KILL / WATCH / GO DEEPER
```

Purpose:

```text
REMOVE RETRIEVAL DIFFERENCES
AND TEST REASONING / JUDGMENT
```

Interpretation:

```text
DIFFERENT DISCOVERY SET
+ SAME RANKING ON FROZEN EVIDENCE
→ RETRIEVAL / SEARCH EFFECT DOMINATES

SIMILAR DISCOVERY SET
+ DIFFERENT RANKING ON FROZEN EVIDENCE
→ REASONING / MODEL EFFECT IS LARGE

DIFFERENT BOTH
→ BOTH RETRIEVAL AND REASONING MATTER

SIMILAR BOTH
→ METHODOLOGY IS ROBUST ACROSS SYSTEMS
```

---

## New mandatory metadata

Every future run must record:

```text
RUN_ID
AI_SYSTEM
MODEL_IF_KNOWN
ENVIRONMENT_CLASS
CONTEXT_AVAILABLE = YES / NO / UNKNOWN
SEARCH_STACK / BROWSING_MODE
REDDIT_ACCESS_MODE
GITHUB_ACCESS_MODE
RATE_LIMITS_OBSERVED
EXTERNAL_BACKGROUND_SOURCES_ALLOWED = YES / NO
PROMPT_HASH
TIME_STARTED
TIME_WINDOW
```

Do not rely on a model's self-report alone for context independence.

`CONTEXT-INFLUENCE SELF-CHECK = NO` is useful metadata but not proof.

---

## Compliance score

Cross-system comparison requires a separate `METHODOLOGY_COMPLIANCE` score.

Suggested checks:

```text
C1 strict time-window compliance
C2 Human pain only
C3 builder != validation
C4 minimum independent signal rule
C5 Reddit/GitHub source protocol
C6 no padding to 10
C7 problem != opportunity confidence
C8 bug != opportunity
C9 WTP status discipline
C10 adversarial deep validation / kill criteria
```

Report:

```text
METHODOLOGY_COMPLIANCE = X / 10
```

A brilliant opportunity found by violating the frozen protocol must not be compared as if it were produced under identical conditions.

---

## Cross-run overlap taxonomy

Do not use one crude overlap number.

Classify matches as:

```text
EXACT
same pain + same user class + same failure mechanism

SEMANTIC
same pain and mechanism, different product/community

MECHANISM
different problem surface, same deeper causal pattern

DOMAIN ONLY
same industry/technology, different pain

NONE
```

Only EXACT and SEMANTIC should materially strengthen independent problem recurrence.

MECHANISM overlap is useful for theory-building but must not inflate Human signal counts.

DOMAIN ONLY must never be merged.

---

## Strongest current methodological conclusion

The five-run experiment suggests:

```text
METHODOLOGY FINGERPRINT
= RELATIVELY STABLE

DISCOVERY PORTFOLIO
= HIGHLY SYSTEM / RETRIEVAL SENSITIVE

CONTEXT LOCK-IN
= NOT ESTABLISHED

PURE MODEL EFFECT
= NOT YET ISOLATED
```

Across very different portfolios, the better runs repeatedly distinguish:

```text
REAL PAIN
FROM
MONETIZABLE GAP
```

and deep validation often downgrades initially dramatic candidates.

That stability is more important than obtaining identical opportunity lists.

---

## Canonical decision rule

Do not ask:

```text
"Which AI found the same ideas?"
```

Ask three separate questions:

```text
1. WHICH SYSTEM FOUND THE BEST VALID EVIDENCE?

2. GIVEN THE SAME EVIDENCE,
   WHICH MODEL MADE THE BEST DECISIONS?

3. WHICH FINDINGS RECUR ACROSS
   INDEPENDENT SYSTEMS WITHOUT BEING
   EXPLAINED BY SOURCE-DENSITY BIAS?
```

Only after answering all three should the Radar treat cross-AI agreement as strong external confirmation.
