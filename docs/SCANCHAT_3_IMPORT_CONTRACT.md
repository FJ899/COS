# ScanChat 3.0 → COS: import contract (ALPHA, NOT APPROVED)

## Problem observed
The legacy ScanChat 2.0.9 DOM export of "Rozpoznanie technologii MP" reported STABLE_FIRST_TRY but included unrelated medical, JACK FEQ, and animation chats. A green repeated scan is not proof of conversation isolation. Never ingest that data as a verified COS conversation.

## Scope
Profile: PRIVATE / SINGLE-USER / ANALYSIS-ONLY. No public side effects, no production GitHub sync, no automatic merge. COS remains the reasoning layer; ScanChat is the acquisition and preservation layer.

## New core implementation
An offline Node.js reference module was built and tested in the user-facing artifact `ScanChat-3.0-core-alpha.zip`. Contents:
- `lib/core.js`: source-specific importers, message and conversation identities, content SHA-256, quarantine;
- `cli.mjs`: import to v3 archive;
- `test/core.test.js`: 5 regression tests;
- `README.md`: usage, limitations and remaining gates.

This PR contains the contract only, **not** the executable code. Do not treat this document as proof that the code has been merged into COS.

## Core design contract
- Each message belongs to exactly one immutable `conversation_id`.
- Source graph message IDs and parent links must be preserved. Branches are not flattened into a claimed canonical linear timeline.
- Repeated identical user text is not automatically deduplicated.
- DOM-only legacy exports are QUARANTINED, even when ScanChat 2.x reports STABLE_FIRST_TRY.
- Missing identity, suspicious structure, provenance gaps, branch ambiguities or checksum mismatch fail closed.
- The verification gate reports PASS only when its narrow, documented internal predicates hold. Do not conflate structural verification with independent proof that a complete ChatGPT account export was obtained.
- File attachments and structured multimodal content are not yet losslessly captured.
- No credentials, conversation JSON or private data should be committed to the public COS repository.

## Test evidence (local, 2026-10-18)
`node --test test/*.test.js`: 5 PASS, 0 FAIL.
Regression input `ScanChat_Rozpoznanie technologii MP_2026-10-17T23-04-23-803Z.json` yielded QUARANTINED / BLOCKED: 23 extracted rows (17 user / 6 assistant), not an acceptable archive. Raw user data was not included in this branch.

## Gates before COS production integration
1. Import a trusted ChatGPT `conversations.json` from user data export, retaining per-conversation IDs and branch lineage.
2. Compare observed legacy DOM results to the exact source conversations and report cross-chat contamination.
3. Implement a LIVE Chrome adapter that rejects unrelated conversation roots instead of querying global DOM.
4. Preserve rich block structure and explicitly inventory binary attachments.
5. Validate project-wide indexing and repeated exports/idempotency.
6. Independent audit of tests on actual Chrome and controlled corpus.
7. Only after owner acceptance may a separate PR wire verified records into COS. Keep GitHub sink disabled.

Status: PARTIAL — core alpha implemented locally; browser adapter and production connection NOT IMPLEMENTED.