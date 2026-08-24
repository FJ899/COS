# RESEARCH MASTER INDEX

Updated: 2026-08-24

## Canonical archive rule

Repository records are authoritative. Library copies are mirrors only.

## Historical coverage

```text
CURRENT HISTORICAL COVERAGE = PARTIAL
HISTORICAL RADAR / PROJECTOR BACKFILL = PREPARED / IMPORT PENDING
ABSENCE FROM INDEX != ABSENCE FROM HISTORY
```

This index is authoritative for records already archived in the repository, but it is not yet historically complete.

## Archived runs

### 2026-08-23 — Claude Blocked Intent Radar

- RAW artifact: `research/radars/blocked-intent/runs/2026-08-23/raw/CLAUDE_BLOCKED_INTENT_RADAR_RAW.docx`
- Review: `research/radars/blocked-intent/runs/2026-08-23/evaluations/CLAUDE_BLOCKED_INTENT_RADAR_REVIEW_2026-08-24.md`
- Original source filename: `Test 2 Claude(1).docx`
- Original source size: `40168 bytes`
- Original source SHA-256: `e7d7bd886810902630892009646271aec526fc86365274b111d97dd72d84bf92`
- Repository RAW Git blob SHA: `579b0261116ded8a4aec38b0afc10a1b06599633`
- RAW byte identity: `VERIFIED`
- Source environment: Claude independent/blind run as reported in source artifact.
- Reported search/fetch calls: 42.
- Qualified cases retained by source run: 4.
- Source limitation: Reddit unavailable; discovery shifted heavily toward GitHub/technical sources.

Disposition from later review:

```text
KEEP
- BIR-02 Open WebUI accessibility
- BIR-01 OOMWOO

WATCH
- BIR-03 Hubspace BLE

DROP
- BIR-04 utahexpungements parser
```

Key methodological observation:

`LONGER SEARCH DID NOT PRODUCE PROPORTIONALLY MORE VALUE.`

Candidate methodology lesson:

`QUALITY STOP CONDITION` — stop discovery when marginal searches mostly return stale, duplicate, solved, or weak-signal cases; do not pad output to a target count.

Status:

```text
RAW SOURCE = ARCHIVED IN REPOSITORY
EVALUATION = ARCHIVED IN REPOSITORY
NEW DEVELOPMENT TASK = NO
NEW PRODUCT DECISION = NO
FINDING != TASK
```

## Historical backfill preparation

### Projector / Real World Need Radar — 2026-08-21 → 2026-08-23

Backfill contract:
`research/history/projector-radar-2026-08-21_23/README.md`

Provenance manifest:
`research/history/projector-radar-2026-08-21_23/PROVENANCE_MANIFEST.md`

Decision/status provenance index:
`research/history/projector-radar-2026-08-21_23/DECISION_PROVENANCE_INDEX.md`

Source Library root:
`/Projektor/Test Archive/2026-08-21_22/`

Prepared inventory covers:
- Projector real-work observations 001–011;
- frozen test campaign archive metadata;
- post-test reconciliation;
- parked benchmark proposal;
- Real World Need Radar discovery RAW runs 001–002;
- run evaluations and five-run comparison;
- final Projector candidate scan;
- methodology evolution v1.0–v1.6.

Current status:

```text
SOURCE INVENTORY = PREPARED
PROVENANCE HASHES = RECORDED
SOURCE ARTIFACT EXACT-BYTE IMPORT = PENDING
FROZEN RAW ZIP EXACT-BYTE IMPORT = PENDING
BACKFILL READY TO MERGE = NO
```

A failed transport attempt was stopped because one manually transported chunk did not reproduce the expected Git blob SHA. No source artifact from that failed transport is claimed as migrated.
