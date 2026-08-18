#!/usr/bin/env python3
"""Fail-closed verification of Ginseng D0 Human acceptance history and accepted integration."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE = ROOT / "governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md"
INTEGRATION = ROOT / "governance/GINSENG_D0_INTEGRATION_RECORD_2026-08-19.md"
D09 = ROOT / "scripts/verify_ginseng_d09_d0_closure.py"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(content: str, markers: list[str], owner: str) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} missing marker: {marker}")


def main() -> None:
    if not ACCEPTANCE.is_file():
        fail("Human acceptance record missing")
    if not INTEGRATION.is_file():
        fail("accepted integration record missing")
    if not D09.is_file():
        fail("D-09 verifier missing")

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    require(
        acceptance,
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
        "historical Human acceptance record",
    )

    for marker in [
        "merge_authorized: true",
        "runtime_authorized: true",
        "formal_project_activation: true",
        "project_completion_claim: PASS",
        "MERGE PR #29: AUTHORIZED",
        "RUNTIME: AUTHORIZED",
    ]:
        if marker in acceptance:
            fail(f"historical acceptance record was rewritten or escalated: {marker}")

    integration = INTEGRATION.read_text(encoding="utf-8")
    require(
        integration,
        [
            "status: INTEGRATED / HUMAN_ACCEPTED_D0_CLOSED",
            "`AKCEPTUJĘ GINSENG D0 TECHNICAL CLOSURE`",
            "`AKCEPTUJĘ MERGE PR #29`",
            "accepted_technical_head: 05d6f48730b80052bdeab55b52f4a67de5828130",
            "merge_commit: a43a94c246112b72a54e952b52af1eacedaaeb3b",
            "merge_tree: ce7c542095ae243ce07be1e2ee9642cb8c7ea69e",
            "GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED",
            "runtime_authorized: false",
            "formal_project_activation: false",
            "whole_project_completion_claim: false",
        ],
        "accepted integration record",
    )
    for marker in [
        "runtime_authorized: true",
        "formal_project_activation: true",
        "whole_project_completion_claim: true",
    ]:
        if marker in integration:
            fail(f"unauthorized escalation in accepted integration record: {marker}")

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
        fail("technical D-09/integration verifier no longer passes")
    for marker in [
        "GINSENG_D09_FINAL_RECHECK: PASS",
        "GINSENG_D0_TECHNICAL_CLOSURE_PROOF: PASS",
        "CURRENT_GINSENG_D0_STATE: HUMAN_ACCEPTED / CLOSED",
        "PR_29_INTEGRATION: MERGED",
    ]:
        if marker not in completed.stdout:
            fail(f"D-09 verifier missing expected current-state marker: {marker}")

    print("[PASS] historical Human acceptance remains immutable and correctly scoped")
    print("[PASS] separate Human merge authority and accepted integration are explicit")
    print("[PASS] technical closure proof remains independently fail-closed")
    print("[PASS] no runtime/formal-project/whole-project authority was inferred")
    print("GINSENG_D0_TECHNICAL_CLOSURE_ACCEPTANCE: PASS")
    print("GINSENG_DONE_D0_CURRENT_STATE: HUMAN_ACCEPTED / CLOSED")
    print("MERGE_PR_29_INTEGRATION: PASS")


if __name__ == "__main__":
    main()
