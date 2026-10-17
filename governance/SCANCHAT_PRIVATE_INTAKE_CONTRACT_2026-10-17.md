# ScanChat -> COS private intake contract (candidate)

Status: IMPLEMENTATION PROTOTYPE / NOT ACCEPTED OR DEPLOYED.
Scope: PRIVATE / SINGLE-USER / ANALYSIS-ONLY. No public writes.

## Verified local prototype
- Source: user's ScanChat-2.0.0.zip (ScanChat 1.1 single-chat archive and 1.2 project archive formats).
- Offline adapter: `scanchat_bridge.py` (separately delivered as a ZIP), with six local unittest checks passing.
- Output: `cos-scanchat-intake/0.1` JSON with ordered messages, source keys, source SHA-256, unknown timestamps, metadata-only attachment markers and explicit lack of global completeness proof.
- No AI interpretation, Projector state transition, GitHub token, or network access.
- This PR documents the candidate interface; the separately delivered prototype is not yet integrated into this repository.

## Mandatory acceptance gates before claiming reliable intake
1. Verify ScanChat archive checksum manifest and all input entries, rejecting manipulated or incomplete archives.
2. Preserve stable source identifiers, raw input hashes, message order, attachment metadata, and scan diagnostics.
3. Detect duplicate messages and archive entries; ensure repeated import is idempotent.
4. Preserve uncertainty: incomplete scan, unavailable messages, dates, or attachment bytes must never become proof of absence.
5. Protect confidentiality: local-only by default, never check real transcripts into public COS history.
6. Run representative real single-chat and project ZIP fixtures, including negative tests for tampering, malformed data and missing parts.
7. Keep semantic analysis separate: every extracted claim, decision and proposed DONE criterion must cite source-message keys and be subject to Human review.
8. Only promote a derived Projector run through its existing schema 2.1 validator and evidence-to-DONE binding; never use conversion success as DONE evidence.

## Deliberately deferred
Multi-provider import, automatic GitHub sync, public effects, live browser automation, and unsupervised conversation conclusions.

## Roadmap
Verified ScanChat ZIP -> normalized read-only intake -> source-linked AI analysis -> Human review -> validated private Projector transitions.
