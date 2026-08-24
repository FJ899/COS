# PROJECTOR REAL-WORK OBSERVATION 008 — USEME TARGET 143120 QUALIFICATION — 2026-08-23

## Source

Human-supplied live Useme screenshots for:

`Data & Evaluation Specialist B+R, AI i analiza mediów`
Useme job ID: `143120`
Client shown: `Stelvo Sp. z o.o.`

## Live offer facts visible in screenshots

- Budget: `Do negocjacji`
- Valid for: `30 dni`
- Copyright: `Przeniesienie praw autorskich`
- Sent offers visible: `14`
- Published: `wczoraj`
- Start: small paid qualification task
- Further cooperation may begin after project funding

### Scope

The client wants a credible evaluation process from source data through a reference set to honest model-quality measurement, including:

- preparing and documenting datasets for experiments;
- designing reference datasets and labeling rules;
- quality/completeness/duplicate/provenance controls;
- model evaluation using precision, recall, F1, calibration, errors and confidence intervals;
- repeatable reports and benchmarks;
- detecting data leakage, methodological errors and deceptively good results;
- collaboration with ML and technical staff.

### Explicit requirements

The offer explicitly requires practical experience in:

- Python;
- SQL;
- data analysis.

Nice-to-have areas include statistics, A/B experiments, time series, NLP, text/audio data, pandas, NumPy, PostgreSQL, Jupyter and BI.

Application asks for:
- CV or LinkedIn/GitHub;
- 2–3 examples of analyses;
- net rate;
- monthly availability;
- a short answer naming three controls that would prevent model performance from being an artifact of leakage or bad sampling.

## Qualification verdict

```text
CONCEPTUAL FIT WITH PROJECTOR METHODS = VERY HIGH
PROVEN PERSONAL QUALIFICATION FIT = NOT ESTABLISHED
FIRST-REVENUE FIT = MEDIUM / LOW
CURRENT APPLY VERDICT = CONDITIONAL
```

Reason:

The work strongly matches evidence discipline, reference-set design, provenance, leakage detection, honest evaluation and benchmark thinking.

However, the client explicitly asks for practical Python and SQL experience plus portfolio evidence. The current Useme profile path does not establish those credentials. They must not be invented or inferred from AI assistance.

## Decision rule

```text
IF HUMAN CAN TRUTHFULLY DOCUMENT
PRACTICAL PYTHON + SQL EXPERIENCE
AND PROVIDE 2–3 REAL ANALYSIS EXAMPLES
→ APPLY IS REASONABLE

ELSE
→ DO NOT MISREPRESENT
→ REJECT FOR THIS FIRST-REVENUE ATTEMPT
```

The presence of a paid qualification task is positive, but it does not remove the explicit qualification requirement.

## Strong application answer if qualification is genuine

Three controls against data leakage / bad sampling:

1. **Split by the true prediction boundary before feature engineering** — create train/validation/test partitions using time/entity/source-aware grouping as appropriate, and fit preprocessing only on training data.
2. **Duplicate / near-duplicate and provenance audit across splits** — hash/entity/content similarity checks plus source lineage to prevent the same underlying observation from appearing in both train and evaluation sets.
3. **Frozen holdout + slice/baseline checks** — keep an untouched final holdout, compare against simple baselines, and report performance/calibration by meaningful slices to expose sample-selection artifacts and unstable aggregate metrics.

These are technically relevant, but should only be submitted as part of an application that is otherwise truthful about the Human's own qualifications.

## Lesson

```text
HIGH CAPABILITY FIT
!=
HONEST CREDENTIAL FIT
```

For marketplace work, Projektor must distinguish:
- work the Human+AI system can potentially execute;
- qualifications the client explicitly requires the applicant to personally possess and evidence.

## Status

`TARGET 143120 = INTERESTING / CONDITIONAL, NOT AUTO-APPLY`

No new product, component or infrastructure work is justified by this offer.
