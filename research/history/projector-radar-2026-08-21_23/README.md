# PROJECTOR / RADAR HISTORICAL BACKFILL — 2026-08-21 → 2026-08-23

Status: `HISTORICAL / PROVENANCE-PRESERVING BACKFILL / EXACT-BYTE IMPORT COMPLETE`
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

## Imported backfill classes

- `source-navigation/` — original archive navigation/integrity metadata.
- `evaluations/` — post-test reconciliation/synthesis.
- `observations/` — Projector real-work observations 001–011, preserved as historical observations.
- `candidates/` — parked benchmark proposal; not activation authority.
- `radars/real-world-need/raw/` — raw discovery-run records.
- `radars/real-world-need/evaluations/` — later run evaluations/comparisons/candidate scan.
- `radars/real-world-need/methodology/` — historical methodology evolution v1.0–v1.6.
- `raw/` — frozen raw campaign package and checksum metadata.

## Current backfill state

The full selected source-artifact corpus has been inventoried from the Library source and exact source-file sizes/SHA-256 values are recorded in `PROVENANCE_MANIFEST.md`.

The frozen source ZIP `PROJECTOR_TEST_CAMPAIGN_RAW_2026-08-21_22.zip` has SHA-256:

`43492be1f56d2db3e45c9cd49ff73bf45980c33b13b087e69a88ee64a349ff7c`

Its checksum was reverified before import. The repository copy has the same exact Git blob identity as the independently verified source bytes.

An earlier manual chunk transport detected a byte-integrity mismatch and was stopped fail-closed. No artifact from that failed transport is claimed as migrated. The later import used independently verified source bytes; repository path, byte-size and Git object identity were then checked against the prepared provenance package and manifest.

```text
SOURCE INVENTORY = COMPLETE FOR /Projektor/Test Archive/2026-08-21_22/
PROVENANCE CLASSIFICATION = COMPLETE FOR SELECTED 31 ARTIFACTS
TEXTUAL EXACT-BYTE IMPORT = COMPLETE
FROZEN RAW ZIP EXACT-BYTE IMPORT = COMPLETE / VERIFIED
REPOSITORY OBJECT SIZE / IDENTITY VERIFICATION = PASS
HISTORICAL COVERAGE = PARTIAL BY DOCUMENTED CHAT-ONLY LIMITATION
MERGE READINESS = CONDITIONAL ON FRESH EXACT-HEAD READ-ONLY REVIEW
HUMAN MERGE AUTHORITY = NO
```

## Privacy preflight

Before preparing this public-repository backfill, the frozen ZIP was inspected for obvious credentials/secrets and its screenshots were reviewed for visible identity data. No credentials or actual government-ID/address/PESEL values were identified. The workbook identifies its data as synthetic. This is a best-effort publication-safety preflight, not a guarantee that every byte has been independently classified.

## Merge gate

This backfill MUST NOT be merged until:

1. each selected historical source artifact is present at the manifest-defined repository path with the expected byte identity;
2. repository object sizes/identities are checked against the independently SHA-256-verified source package and provenance manifest;
3. the frozen raw ZIP remains byte-exact;
4. a fresh exact-head read-only review returns `ACCEPT + MERGE`;
5. separate Human merge authority is given for that exact reviewed head.
