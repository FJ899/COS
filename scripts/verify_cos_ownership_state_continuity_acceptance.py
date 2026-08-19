#!/usr/bin/env python3
"""Fail-closed verification of Human acceptance for COS ownership/state/continuity closure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / "governance/COS_OWNERSHIP_STATE_CONTINUITY_HUMAN_ACCEPTANCE_2026-08-19.md"
COS_VERIFY = ROOT / "scripts/verify_creative_os.py"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(content: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"COS acceptance record missing marker: {marker}")


def main() -> None:
    if not ACCEPTANCE.is_file():
        fail("COS Human acceptance record missing")
    if not COS_VERIFY.is_file():
        fail("Creative OS continuity verifier missing")

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
        "[PASS] CREATIVE_OS.md ma aktualny cross-project state",
        "[PASS] START_HERE.md wskazuje aktualne repo locators",
        "[PASS] COS ownership audit preserves local truth",
    ]
    for marker in required_output:
        if marker not in completed.stdout:
            fail(f"Creative OS verifier missing expected closure marker: {marker}")

    print("[PASS] COS closure Human acceptance is explicit and source-bound")
    print("[PASS] accepted technical candidate remains independently fail-closed")
    print("[PASS] no merge/runtime/project-activation/memory-promotion authority was inferred")
    print("COS_OWNERSHIP_STATE_CONTINUITY_ACCEPTANCE: PASS")
    print("MERGE_PR_30_AUTHORITY: PENDING")


if __name__ == "__main__":
    main()
