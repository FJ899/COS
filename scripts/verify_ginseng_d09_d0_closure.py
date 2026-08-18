#!/usr/bin/env python3
"""Fail-closed final D-09 recheck for the frozen Ginseng D0 candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DONE_FREEZE = "governance/GINSENG_DONE_D0_FREEZE_2026-08-18.md"
D0_AUDIT = "governance/GINSENG_D0_EVIDENCE_AUDIT_2026-08-18.md"
D05_PROOF = "governance/GINSENG_D05_DECISION_LINEAGE_PROOF_2026-08-19.json"
CLOSURE = "governance/GINSENG_D0_TECHNICAL_CLOSURE_CANDIDATE_2026-08-19.md"
RESULT = "tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md"
CUSTODY_MANIFEST = "tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.manifest.json"
CUSTODY_ZIP = "tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.zip"
COS = "CREATIVE_OS.md"

BOUND_TEXT_BLOBS = {
    DONE_FREEZE: "eafc5d21729c393801ee3f1c7e3d57e7da883ee3",
    D0_AUDIT: "48065e555c338ba68f309d879080dfcdf81ba3c2",
    D05_PROOF: "8361c664c1ff31017b0facbcfd7a2074f860d5a5",
    RESULT: "4ca0bb2065d3914e73b5ec8f3283894b681f9d54",
    CUSTODY_MANIFEST: "b0cd9f14ae012381dc9781c13efc7aeb96d2b8e7",
}

EXPECTED_EVIDENCE_SHA256 = "d9077d08012667a8a2a91e93912ee752bf991b50b5b01e4d2f80914cde315fdf"
EXPECTED_EVIDENCE_GIT_BLOB = "b82e442678766ca3fa0d0dd8180cb1b0ae9f162d"
EXPECTED_EVIDENCE_SIZE = 95846
EXPECTED_EVIDENCE_ENTRIES = 39


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    raise AssertionError("unreachable")


def load_json(path: str) -> dict:
    try:
        value = json.loads(load_text(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def git_blob_sha(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def require(content: str, markers: list[str], owner: str) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} missing marker: {marker}")


def verify_bound_sources() -> None:
    for path, expected in BOUND_TEXT_BLOBS.items():
        if not (ROOT / path).is_file():
            fail(f"missing bound source: {path}")
        actual = git_blob_sha(path)
        if actual != expected:
            fail(f"bound source changed: {path} expected={expected} actual={actual}")
    print("[PASS] frozen D0 evidence sources retain exact accepted bytes")


def verify_d01() -> None:
    cos = load_text(COS)
    closure = load_text(CLOSURE)
    require(
        cos,
        [
            "Status: `EXECUTED / INDEPENDENTLY_VERIFIED_PASS`.",
            "D-08: SATISFIED — DURABLE REPOSITORY CUSTODY / EXACT BYTES / SHA-256 BOUND",
            "Ginseng D0: BLOCKED — D-05 DECISION LINEAGE PROOF GAP + D-08 EVIDENCE CUSTODY HUMAN DECISION",
        ],
        COS,
    )
    require(
        closure,
        [
            "## 5. D-01 current-state reconciliation",
            "those two operational current-state statements are explicitly superseded by this later closure record",
            "the next remaining boundary becomes final Human D0 acceptance",
            "Historical append-only statements remain historical and are not rewritten.",
        ],
        CLOSURE,
    )
    print("[PASS] D-01 current-state conflict is explicitly superseded, not hidden")


def require_gate_satisfied(audit: str, gate: str, next_gate: str) -> None:
    start = audit.find(f"### {gate}")
    end = audit.find(f"### {next_gate}", start + 1)
    if start < 0 or end < 0:
        fail(f"cannot isolate audit section {gate}")
    section = audit[start:end]
    if "`SATISFIED`" not in section:
        fail(f"{gate} is not SATISFIED in the accepted audit")


def verify_d02_d04_d06_d07() -> None:
    audit = load_text(D0_AUDIT)
    require_gate_satisfied(audit, "D-02 — DECISION-SPACE ANALYSIS", "D-03 — CHANGE PROPAGATION / LOCAL RECALCULATION")
    require_gate_satisfied(audit, "D-03 — CHANGE PROPAGATION / LOCAL RECALCULATION", "D-04 — TRUTH TYPES / RELATION AUTHORITY")
    require_gate_satisfied(audit, "D-04 — TRUTH TYPES / RELATION AUTHORITY", "D-05 — DECISION LINEAGE")
    require_gate_satisfied(audit, "D-06 — ELEMENT -> FUNCTION / CAPABILITY -> EFFECT", "D-07 — UNCERTAINTY / HUMAN DECISION NEED")
    require_gate_satisfied(audit, "D-07 — UNCERTAINTY / HUMAN DECISION NEED", "D-08 — DURABLE EVIDENCE / REPLAY")
    print("[PASS] D-02/D-03/D-04/D-06/D-07 remain satisfied by accepted audit evidence")


def verify_d05() -> None:
    proof = load_json(D05_PROOF)
    if proof.get("record_status") != "D05_SATISFIED_IF_VERIFIED_AND_ACCEPTED":
        fail("D-05 proof status mismatch")
    negatives = proof.get("negative_assertions")
    if negatives != {
        "production_decision_created": False,
        "baseline_change_claimed": False,
        "runtime_required": False,
        "new_normative_meaning_added": False,
        "known_superseder_in_current_accepted_d0_evidence": False,
    }:
        fail("D-05 negative assertions changed")

    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_ginseng_d05_lineage.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        fail("dedicated D-05 verifier failed inside final D-09 recheck")
    if "GINSENG_D05_DECISION_LINEAGE: PASS" not in completed.stdout:
        fail("dedicated D-05 verifier did not emit terminal PASS")
    print("[PASS] D-05 complete source-bound lineage independently reverified")


def verify_d08() -> None:
    manifest = load_json(CUSTODY_MANIFEST)
    artifact = manifest.get("artifact")
    if artifact != {
        "filename": "GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.zip",
        "repository_path": CUSTODY_ZIP,
        "sha256": EXPECTED_EVIDENCE_SHA256,
        "byte_size": EXPECTED_EVIDENCE_SIZE,
        "zip_entry_count": EXPECTED_EVIDENCE_ENTRIES,
    }:
        fail("D-08 custody manifest identity mismatch")
    custody = manifest.get("custody", {})
    if custody.get("status") != "DURABLE_REPOSITORY_CUSTODY / EXACT_BYTES / SHA256_BOUND":
        fail("D-08 custody status mismatch")

    path = ROOT / CUSTODY_ZIP
    if not path.is_file():
        fail("D-08 exact evidence ZIP is missing")
    raw = path.read_bytes()
    if len(raw) != EXPECTED_EVIDENCE_SIZE:
        fail(f"D-08 ZIP size mismatch: {len(raw)}")
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_sha256 != EXPECTED_EVIDENCE_SHA256:
        fail(f"D-08 ZIP SHA-256 mismatch: {actual_sha256}")
    actual_git_blob = git_blob_sha(CUSTODY_ZIP)
    if actual_git_blob != EXPECTED_EVIDENCE_GIT_BLOB:
        fail(f"D-08 ZIP Git blob mismatch: {actual_git_blob}")
    try:
        with zipfile.ZipFile(path, "r") as archive:
            if len(archive.infolist()) != EXPECTED_EVIDENCE_ENTRIES:
                fail(f"D-08 ZIP entry count mismatch: {len(archive.infolist())}")
            bad = archive.testzip()
            if bad is not None:
                fail(f"D-08 ZIP integrity failed at entry: {bad}")
    except zipfile.BadZipFile as exc:
        fail(f"D-08 artifact is not a valid ZIP: {exc}")
    print("[PASS] D-08 exact repository bytes independently match SHA/size/39-entry ZIP custody")


def verify_d09_no_false_success() -> None:
    done = load_text(DONE_FREEZE)
    result = load_text(RESULT)
    closure = load_text(CLOSURE)

    require(
        done,
        [
            "### D-09 — FALSE SUCCESS",
            "No terminal DONE/PASS may be reached through a known false-success path.",
            "Final D0 closure must confirm that no newly discovered unresolved D0 gate is being bypassed by the completion claim.",
        ],
        DONE_FREEZE,
    )
    require(
        result,
        [
            "FALSE SUCCESS PATHS: 0",
            "GINSENG_TEST-003: PASS",
            "FUNCTIONAL COMPLETION OF GINSENG: NOT CLAIMED",
            "PROJECT COMPLETION: NOT CLAIMED",
        ],
        RESULT,
    )
    require(
        closure,
        [
            "status: TECHNICAL_CLOSURE_CANDIDATE / HUMAN_ACCEPTANCE_PENDING",
            "Final Human acceptance remains pending",
            "A candidate-authored PASS string is not evidence.",
            "HUMAN D0 ACCEPTANCE: PENDING",
            "RUNTIME: NOT AUTHORIZED",
            "FORMAL PROJECT ACTIVATION: NO",
            "PROJECT COMPLETION CLAIM: NONE",
            "No D0 criterion is added, removed, weakened, or reinterpreted by this closure record.",
        ],
        CLOSURE,
    )

    forbidden = [
        "status: HUMAN_ACCEPTED",
        "HUMAN D0 ACCEPTANCE: ACCEPTED",
        "RUNTIME: AUTHORIZED",
        "FORMAL PROJECT ACTIVATION: YES",
        "PROJECT COMPLETION CLAIM: PASS",
    ]
    for marker in forbidden:
        if marker in closure:
            fail(f"false-success terminal escalation present in closure candidate: {marker}")

    gate_lines = {
        "D-01": "SATISFIED IF THIS VERIFIED CANDIDATE ENTERS ACCEPTED HISTORY",
        "D-02": "SATISFIED",
        "D-03": "SATISFIED",
        "D-04": "SATISFIED",
        "D-05": "SATISFIED IF VERIFIED D-05 PROOF ENTERS ACCEPTED HISTORY",
        "D-06": "SATISFIED",
        "D-07": "SATISFIED",
        "D-08": "SATISFIED",
        "D-09": "PASS ONLY IF INDEPENDENT CLOSURE VERIFIER PASSES EXACT PR HEAD",
    }
    for gate, state in gate_lines.items():
        if not re.search(rf"^{re.escape(gate)}[^\n]*{re.escape(state)}", closure, re.MULTILINE):
            fail(f"closure map missing fail-closed state for {gate}")

    print("[PASS] D-09 found no unresolved-gate bypass or authority escalation")


def main() -> None:
    required = [
        DONE_FREEZE,
        D0_AUDIT,
        D05_PROOF,
        CLOSURE,
        RESULT,
        CUSTODY_MANIFEST,
        CUSTODY_ZIP,
        COS,
        "scripts/verify_ginseng_d05_lineage.py",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        fail("missing closure inputs: " + ", ".join(missing))

    verify_bound_sources()
    verify_d01()
    verify_d02_d04_d06_d07()
    verify_d05()
    verify_d08()
    verify_d09_no_false_success()

    print("GINSENG_D09_FINAL_RECHECK: PASS")
    print("GINSENG_D0_TECHNICAL_CLOSURE: PASS_IF_MERGED")
    print("HUMAN_D0_ACCEPTANCE: PENDING")


if __name__ == "__main__":
    main()
