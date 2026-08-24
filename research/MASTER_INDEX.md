# RESEARCH MASTER INDEX

Updated: 2026-08-24

## Canonical archive rule

Repository records are authoritative. Library copies are mirrors only.

## Historical coverage

```text
CURRENT HISTORICAL COVERAGE = PARTIAL
HISTORICAL RADAR / PROJECTOR BACKFILL = EXACT-BYTE IMPORT COMPLETE / MERGED
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

## Historical backfill

### Projector / Real World Need Radar — 2026-08-21 → 2026-08-23

Backfill contract:
`research/history/projector-radar-2026-08-21_23/README.md`

Provenance manifest:
`research/history/projector-radar-2026-08-21_23/PROVENANCE_MANIFEST.md`

Decision/status provenance index:
`research/history/projector-radar-2026-08-21_23/DECISION_PROVENANCE_INDEX.md`

Imported source-artifact root:
`research/history/projector-radar-2026-08-21_23/source_artifacts/`

Historical Library source root:
`/Projektor/Test Archive/2026-08-21_22/`

Imported inventory covers:
- Projector real-work observations 001–011;
- frozen test campaign archive + checksum/navigation metadata;
- post-test reconciliation;
- parked benchmark proposal;
- Real World Need Radar discovery RAW runs 001–002;
- run evaluations and five-run comparison;
- final Projector candidate scan;
- methodology evolution v1.0–v1.6.

Current status:

```text
SOURCE INVENTORY = COMPLETE
PROVENANCE HASHES = RECORDED
SOURCE ARTIFACT EXACT-BYTE IMPORT = COMPLETE / 31 OF 31
FROZEN RAW ZIP EXACT-BYTE IMPORT = COMPLETE / VERIFIED
REPOSITORY OBJECT SIZE / IDENTITY VERIFICATION = PASS
HISTORICAL COVERAGE = PARTIAL BY DOCUMENTED CHAT-ONLY LIMITATION
EXACT-HEAD REVIEW = PASS ON 9943d3caeb19f56d7547cdfc032cf3ce8432bffa
HUMAN MERGE AUTHORITY = GRANTED + CONSUMED FOR EXACT HEAD 9943d3caeb19f56d7547cdfc032cf3ce8432bffa
PR #42 = MERGED
MERGE COMMIT = 632eb5f86f0356820ab165bcf1c7df70e466e0d8
```

An earlier manual chunk transport failed an expected Git blob identity check and was stopped fail-closed. No artifact from that failed attempt is claimed as migrated. The completed import used exact source bytes independently verified against the provenance package and manifest.
