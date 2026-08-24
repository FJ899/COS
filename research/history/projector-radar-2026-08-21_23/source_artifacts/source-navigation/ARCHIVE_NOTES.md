# PROJECTOR TEST CAMPAIGN — RAW EVIDENCE ARCHIVE

Created: 2026-08-22

Purpose: preserve the exact bytes of every conversation attachment currently mounted from the Projektor test campaign (2026-08-21 → 2026-08-22), including test/session outputs, frozen creative input, screenshots, and the P1-D workbook artifact.

Integrity rule:
- files under `raw/` are byte-for-byte copies of the mounted conversation attachments;
- `MANIFEST_SHA256.txt` records SHA-256 for every preserved file;
- no content inside `raw/` was normalized, reformatted, summarized, or edited.

Coverage limitation:
- chat messages that existed only as inline conversation text and were never attached as files are NOT claimed as byte-for-byte preserved by this archive;
- they require a raw conversation export if exact character-level preservation of the complete chat transcript is required.
