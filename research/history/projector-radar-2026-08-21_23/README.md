# PROJECTOR / RADAR HISTORICAL BACKFILL — 2026-08-21 → 2026-08-23

Status: `HISTORICAL / PROVENANCE-PRESERVING BACKFILL / DRAFT CANDIDATE`
Source Library path: `/Projektor/Test Archive/2026-08-21_22/`
Prepared: 2026-08-24

## Purpose

Preserve historical Projector and Real World Need Radar evidence in the repository-authoritative research subtree without rewriting old evidence to match later conclusions.

## Evidence boundaries

```text
RAW != EVALUATION
OBSERVATION != DECISION
CANDIDATE != ACTIVATED WORK
HISTORICAL STATUS != CURRENT AUTHORITY
FINDING != TASK
```

## Backfill classes to import

- `source-navigation/` — original archive navigation/integrity metadata.
- `evaluations/` — post-test reconciliation/synthesis.
- `observations/` — Projector real-work observations 001–011, preserved as historical observations.
- `candidates/` — parked benchmark proposal; not activation authority.
- `radars/real-world-need/raw/` — raw discovery-run records.
- `radars/real-world-need/evaluations/` — later run evaluations/comparisons/candidate scan.
- `radars/real-world-need/methodology/` — historical methodology evolution v1.0–v1.6.
- `raw/` — frozen raw campaign package.

## Current preparation state

The full textual corpus has been inventoried from the Library source and exact source-file sizes/SHA-256 values are recorded in `PROVENANCE_MANIFEST.md`.

The frozen source ZIP `PROJECTOR_TEST_CAMPAIGN_RAW_2026-08-21_22.zip` has SHA-256:

`43492be1f56d2db3e45c9cd49ff73bf45980c33b13b087e69a88ee64a349ff7c`

Its checksum has been reverified against the Library source.

A transport test detected a byte-integrity mismatch in a manually transported chunk and was stopped fail-closed. Therefore no historical source file is being claimed as repository-migrated until exact-byte import is independently verified.

```text
SOURCE INVENTORY = COMPLETE FOR /Projektor/Test Archive/2026-08-21_22/
PROVENANCE CLASSIFICATION = PREPARED
TEXTUAL EXACT-BYTE IMPORT = PENDING
FROZEN RAW ZIP EXACT-BYTE IMPORT = PENDING
HISTORICAL COVERAGE = STILL PARTIAL
READY TO MERGE = NO
```

## Privacy preflight

Before preparing this public-repository backfill, the frozen ZIP was inspected for obvious credentials/secrets and its screenshots were reviewed for visible identity data. No credentials or actual government-ID/address/PESEL values were identified. The workbook identifies its data as synthetic. This is a best-effort publication-safety preflight, not a guarantee that every byte has been independently classified.

## Merge gate

This draft is a backfill contract and provenance map. It MUST NOT be marked merge-ready until:

1. each historical source artifact selected for repository storage is imported byte-exact or explicitly classified as a non-byte-exact derived representation;
2. repository hashes are compared against the source manifest;
3. the frozen raw ZIP is imported byte-exact or an explicit Human decision excludes it;
4. a fresh exact-head read-only review returns `ACCEPT + MERGE`.
