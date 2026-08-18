#!/usr/bin/env python3
"""Fail-closed verification of the Human acceptance record for Ginseng D0 technical closure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / "governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md"
D09 = ROOT / "scripts/verify_ginseng_d09_d0_closure.py"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(content: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"Human acceptance record missing marker: {marker}")


def main() -> None:
    if not ACCEPTANCE.is_file():
        fail("Human acceptance record missing")
    if not D09.is_file():
        fail("D-09 verifier missing")

    content = ACCEPTANCE.read_text(encoding="utf-8")
    require(
        content,
        [
            "status: HUMAN_ACCEPTED_TECHNICAL_CLOSURE / MERGE_PENDING",
            "owner: USER",
            "accepted_at: 2026-08-19",
            "accepted_technical_head: ed4c7031a03c27ff5b8d68aba3fb9d6340a55469",
            "accepted_technical_ci_run: 61",
            "merge_authorized: false",
            "runtime_authorized: false",
            "formal_project_activation: false",
            "project_completion_claim: NONE",
            "`AKCEPTUJĘ GINSENG D0 TECHNICAL CLOSURE`",
            "GINSENG D0 TECHNICAL CLOSURE: HUMAN ACCEPTED",
            "GINSENG_DONE_D0: ACCEPTED AS SATISFIED IF THE VERIFIED CLOSURE ENTERS ACCEPTED COS HISTORY",
            "MERGE PR #29: NOT YET AUTHORIZED BY THIS DECISION",
            "whole-project completion beyond the frozen D0 scope",
            "That merge remains separately Human-owned and requires explicit merge authorization.",
        ],
    )

    forbidden = [
        "merge_authorized: true",
        "runtime_authorized: true",
        "formal_project_activation: true",
        "project_completion_claim: PASS",
        "MERGE PR #29: AUTHORIZED",
        "RUNTIME: AUTHORIZED",
    ]
    for marker in forbidden:
        if marker in content:
            fail(f"unauthorized escalation in Human acceptance record: {marker}")

    completed = subprocess.run(
        [sys.executable, str(D09)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        fail("technical D-09 verifier no longer passes")
    for marker in [
        "GINSENG_D09_FINAL_RECHECK: PASS",
        "GINSENG_D0_TECHNICAL_CLOSURE: PASS_IF_MERGED",
        "HUMAN_D0_ACCEPTANCE: PENDING",
    ]:
        if marker not in completed.stdout:
            fail(f"technical verifier missing expected pre-acceptance marker: {marker}")

    print("[PASS] Human acceptance is explicit and bound to the verified technical candidate")
    print("[PASS] technical closure proof remains independently fail-closed")
    print("[PASS] no merge/runtime/project-completion authority was inferred")
    print("GINSENG_D0_TECHNICAL_CLOSURE_ACCEPTANCE: PASS")
    print("MERGE_PR_29_AUTHORITY: PENDING")


if __name__ == "__main__":
    main()
