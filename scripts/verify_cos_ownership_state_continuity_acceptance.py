#!/usr/bin/env python3
"""Fail-closed verification of historical Human acceptance and current integrated COS closure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / "governance/COS_OWNERSHIP_STATE_CONTINUITY_HUMAN_ACCEPTANCE_2026-08-19.md"
COS_VERIFY = ROOT / "scripts/verify_creative_os.py"
COS_STATE = ROOT / "CREATIVE_OS.md"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(content: str, markers: list[str], owner: str = "COS acceptance record") -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} missing marker: {marker}")


def main() -> None:
    if not ACCEPTANCE.is_file():
        fail("COS Human acceptance record missing")
    if not COS_VERIFY.is_file():
        fail("Creative OS continuity verifier missing")
    if not COS_STATE.is_file():
        fail("Creative OS current state owner missing")

    # Historical Human acceptance is immutable evidence of what was authorized at that time.
    content = ACCEPTANCE.read_text(encoding="utf-8")
    require(
        content,
        [
            "status: HUMAN_ACCEPTED_CLOSURE / MERGE_PENDING",
            "owner: USER",
            "accepted_at: 2026-08-19",
            "accepted_candidate_head: 3b7384eb94ff4919e2907cdf5dde69d3e7c55361",
            "accepted_candidate_ci_run: 72",
            "merge_authorized: false",
            "runtime_authorized: false",
            "project_activation_authorized: false",
            "release_deploy_tag_authorized: false",
            "memory_to_canon_promotion_authorized: false",
            "new_capability_authorized: false",
            "`AKCEPTUJĘ COS OWNERSHIP/STATE/CONTINUITY CLOSURE`",
            "COS OWNERSHIP / STATE / CONTINUITY: HUMAN ACCEPTED",
            "MERGE PR #30: NOT YET AUTHORIZED BY THIS DECISION",
            "ACCEPTED COS HISTORY: PENDING PR #30 MERGE",
        ],
    )

    forbidden = [
        "merge_authorized: true",
        "runtime_authorized: true",
        "project_activation_authorized: true",
        "release_deploy_tag_authorized: true",
        "memory_to_canon_promotion_authorized: true",
        "new_capability_authorized: true",
        "MERGE PR #30: AUTHORIZED",
        "WHOLE ECOSYSTEM: COMPLETE",
    ]
    for marker in forbidden:
        if marker in content:
            fail(f"unauthorized escalation in COS acceptance record: {marker}")

    # Current continuity must still pass independently after later factual maintenance.
    # The required stdout markers track the current verifier contract; they do not rewrite
    # the historical Human acceptance record above or create new authority.
    completed = subprocess.run(
        [sys.executable, str(COS_VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        fail("Creative OS continuity verifier no longer passes")

    required_output = [
        "[PASS] CREATIVE_OS.md ma post-Run003 cross-project state bez local-owner override",
        "[PASS] START_HERE.md używa local-owner live resolution i post-Run003 high-level locator state",
        "[PASS] COS ownership audit remains historical evidence",
    ]
    for marker in required_output:
        if marker not in completed.stdout:
            fail(f"Creative OS verifier missing expected current-state marker: {marker}")

    current = COS_STATE.read_text(encoding="utf-8")
    require(
        current,
        [
            "CURRENT-2026-008 — Post-COS closure evaluation state",
            "CURRENT-2026-009 — ScriptOps post-Run003 continuity state",
            "COS ownership/state/continuity: HUMAN ACCEPTED / CLOSED",
            "PR #30 został scalony jako `main@23152cb1bf5443574da9ff44600a5a8c8c136025`",
            "RECOVERY_RECORD / NON_CANONICAL / NO_AUTHORITY_PROMOTION",
            "WAITING_FOR_EVIDENCE / HUMAN_SEMANTIC_DECISION",
        ],
        "Creative OS current state",
    )
    if "COS ownership/state/continuity: CLOSURE IN PROGRESS" in current:
        fail("Creative OS current state regressed to pre-merge COS closure")

    print("[PASS] historical COS Human acceptance remains immutable and correctly scoped")
    print("[PASS] current post-closure continuity remains independently fail-closed")
    print("[PASS] no runtime/project-activation/memory-promotion authority was inferred")
    print("COS_OWNERSHIP_STATE_CONTINUITY_ACCEPTANCE_HISTORY: PASS")
    print("CURRENT_COS_CLOSURE_STATE: HUMAN_ACCEPTED / CLOSED")
    print("PR_30_INTEGRATION: MERGED")


if __name__ == "__main__":
    main()