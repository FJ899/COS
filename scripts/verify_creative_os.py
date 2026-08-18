#!/usr/bin/env python3
"""Deterministyczna kontrola spójności Creative OS Lean."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "START_HERE.md", "README.md", "CREATIVE_OS.md", "ARCHIVE_INDEX.md",
    ".gitignore", ".github/pull_request_template.md", "scripts/README.md",
    "continuity/COLD_START_AUDIT-001.md", "continuity/COLD_START_TEST-002.md",
    "continuity/COLD_START_AUDIT-002.md",
    "tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md",
    "tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md",
    "governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md",
    "governance/GINSENG_D0_INTEGRATION_RECORD_2026-08-19.md",
    "governance/COS_OWNERSHIP_STATE_CONTINUITY_AUDIT_2026-08-19.md",
    "archives/Archiwum09.md", "projects/bpm160/README.md",
    "projects/bpm160/PROJECT_STATE.md", "projects/bpm160/HANDOFF.md",
    "projects/bpm160/SOURCE_SUMMARY_2026-07-31.md",
    "projects/bpm160/DECISION_LOG.md", "projects/bpm160/SOURCE_MANIFEST.md",
    "projects/bpm160/IDEA_ARCHIVE.md",
]

EXPECTED = {
    "Narzędzie pisarskie / ScriptOps": "QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED",
    "BPM:160": "QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / SOURCE SUMMARY CONFIRMED / ORIGINAL FILES REQUIRED",
    "Creative OS": "ACTIVE / LEAN PILOT / START_HERE ACTIVE",
    "Creative OS Project Reconstructor": "ACTIVE / V1.0 STABILIZATION",
}

STALE_CURRENT_STATE = [
    "Ginseng D0: BLOCKED — D-05 DECISION LINEAGE PROOF GAP + D-08 EVIDENCE CUSTODY HUMAN DECISION",
    "GINSENG D0: BLOCKED — D-05 DECISION LINEAGE remains open; D-09 requires final recheck after closure.",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path} nie jest UTF-8: {exc}")
    raise AssertionError("unreachable")


def require(content: str, markers: list[str], owner: str) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} nie zawiera: {marker}")


def parse_rows(content: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    active = False
    for line in content.splitlines():
        if line.startswith("| Projekt | Status |"):
            active = True
            continue
        if active and line.startswith("|---"):
            continue
        if active and not line.startswith("|"):
            break
        if active:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 6:
                fail(f"wiersz tabeli nie ma 6 kolumn: {line}")
            result[cells[0]] = cells
    return result


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        fail("brak plików: " + ", ".join(missing))
    print(f"[PASS] wymagane pliki: {len(REQUIRED)}")

    cos = load("CREATIVE_OS.md")
    require(cos, [
        "system: creative-os-lean", "status: ACTIVE_LEAN_PILOT",
        "Rozmowa prowadzi proces; repozytorium zachowuje stan.",
        "Każda informacja ma jednego właściciela.",
        "COS posiada wyłącznie trwały stan wysokiego poziomu i przekrojowy",
        "Umiejscowienie informacji w repo nie tworzy semantic ownership ani authority.",
        "STARTED / OK / PARTIAL / BLOCKED / FAILED",
        "Navigation Protocol jest mechanizmem globalnego COS",
        "Nie jest właścicielem operacyjnego wyboru HOW",
        "GINSENG_TEST-003 — zamknięcie pojedynczej bramki",
        "GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED",
        "IDEA-2026-007 — zewnętrzne skille jako warstwa pomocnicza",
        "DEC-2026-007 — Ginseng D0 closed; COS continuity closure",
        "COS ownership/state/continuity: CLOSURE IN PROGRESS",
        "EVOLUTION-2026-014 — Ginseng D0 closure i COS continuity reconciliation",
        "archives/Archiwum09.md",
    ], "CREATIVE_OS.md")
    for stale in STALE_CURRENT_STATE:
        if stale in cos:
            fail(f"CREATIVE_OS.md nadal zawiera stale current-state marker: {stale}")

    project_rows = parse_rows(cos)
    if set(project_rows) != set(EXPECTED):
        fail(f"nieoczekiwane projekty: {sorted(project_rows)}")
    for project, expected in EXPECTED.items():
        if expected not in project_rows[project][1]:
            fail(f"niespójny status {project}: {project_rows[project][1]}")
        if not project_rows[project][4] or not project_rows[project][5]:
            fail(f"brak kroku lub źródła: {project}")
    bpm_row = " ".join(project_rows["BPM:160"]).lower()
    if "spike 001" not in bpm_row or "testy widzów" not in bpm_row or "read_only reconciliation" not in bpm_row:
        fail("karta BPM:160 nie zawiera Spike, parkingu testów widzów i reconciliation")
    if len(re.findall(r"^### IDEA-", cos, re.MULTILINE)) < 7:
        fail("Idea Inbox nie zawiera siedmiu wpisów")
    print("[PASS] CREATIVE_OS.md ma aktualny cross-project state bez stale Ginseng override")

    start = load("START_HERE.md")
    require(start, [
        'role: "single-entrypoint"', "BOOT | WORK | AUDIT | PORTFOLIO",
        'state_owner: "CREATIVE_OS.md"',
        "repo: litrgratis-pixel/scriptops", "critical_scope: sources/RC1_SCOPE_LOCK.md",
        "root: projects/bpm160", "source_summary: projects/bpm160/SOURCE_SUMMARY_2026-07-31.md",
        "SPIKE 001 IN PROGRESS", "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME",
        "READ_ONLY RECONCILIATION", "testów widzów",
        "CORE / SUPPORT / EDITORIAL / REJECT",
        "DOING NOW / NEXT / BACKLOG / PARKED / DONE", "active / superseded / unresolved",
        "repo: litrgratis-pixel/creative-os-project-reconstructor",
        "ACCESS BLOCKED", "SOURCE REQUIRED", "START SESSION", "continuity/COLD_START_*",
    ], "START_HERE.md")
    for mode in ["### BOOT", "### WORK", "### AUDIT", "### PORTFOLIO"]:
        if mode not in start:
            fail(f"brak trybu {mode}")
    print("[PASS] START_HERE.md wskazuje jeden cross-project state owner i lokalne źródła prawdy")

    bpm = "\n".join(load(p) for p in [
        "projects/bpm160/README.md", "projects/bpm160/PROJECT_STATE.md",
        "projects/bpm160/HANDOFF.md", "projects/bpm160/SOURCE_SUMMARY_2026-07-31.md",
        "projects/bpm160/DECISION_LOG.md", "projects/bpm160/SOURCE_MANIFEST.md",
        "projects/bpm160/IDEA_ARCHIVE.md",
    ])
    require(bpm, [
        "SPIKE 001 IN PROGRESS", "World → Signal → Peak Event → Aftermath",
        "Brand Promise oznacza adrenalinę i rytm", "Canon / Konstytucja BPM160 v1.2",
        "Czy BPM160 da się zrealizować przy akceptowalnej jakości, czasie i koszcie?",
        "CORE / SUPPORT / EDITORIAL / REJECT", "DOING NOW / NEXT / BACKLOG / PARKED / DONE",
        "active / superseded / unresolved", "UNCONFIRMED",
        "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME", "Higgsfield Cinema Studio",
        "bpm160-heartbeat-guide.wav", "Producent / Walidator / Turbo / QA",
        "Market Scan v0", "Testy widzów", "READ_ONLY RECONCILIATION",
        "USER_SUPPLIED_SOURCE_SUMMARY",
    ], "pakiet BPM:160")
    print("[PASS] BPM:160 ma właściwy zakres i klasyfikacje")

    test = load("tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md")
    require(test, [
        'status: "EXECUTED / INDEPENDENTLY_VERIFIED_PASS"',
        'result_record: "tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md"',
        "SINGLE_GATE_CLOSURE",
        "VARIANT_A_KEEP_DEC002", "VARIANT_B_SUPERSEDE_DEC002",
        "blocking_gate_count_after = 6", "implementation_readiness_after = BLOCKED",
        "baseline_mutated_after = false", "systematic-debugging",
        "verification-before-completion", "S001_gate_closure_delta.json",
        "aktywuje Ginseng jako formalnego projektu",
    ], "GINSENG_TEST-003")
    if "Ten test nie:" not in test:
        fail("GINSENG_TEST-003 nie zapisuje granicy poza zakresem")

    result = load("tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md")
    require(result, [
        "status: EXECUTED / INDEPENDENTLY_VERIFIED_PASS",
        "GINSENG_TEST-003: PASS",
        "FALSE SUCCESS PATHS: 0",
        "byte_identical_verdict_report: true",
        "FUNCTIONAL COMPLETION OF GINSENG: NOT CLAIMED",
    ], "GINSENG_TEST-003 result")
    print("[PASS] GINSENG_TEST-003 pozostaje niezależnie zweryfikowany")

    acceptance = load("governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md")
    require(acceptance, [
        "status: HUMAN_ACCEPTED_TECHNICAL_CLOSURE / MERGE_PENDING",
        "`AKCEPTUJĘ GINSENG D0 TECHNICAL CLOSURE`",
        "merge_authorized: false",
    ], "Ginseng D0 Human acceptance history")

    integration = load("governance/GINSENG_D0_INTEGRATION_RECORD_2026-08-19.md")
    require(integration, [
        "status: INTEGRATED / HUMAN_ACCEPTED_D0_CLOSED",
        "`AKCEPTUJĘ MERGE PR #29`",
        "accepted_technical_head: 05d6f48730b80052bdeab55b52f4a67de5828130",
        "merge_commit: a43a94c246112b72a54e952b52af1eacedaaeb3b",
        "merge_tree: ce7c542095ae243ce07be1e2ee9642cb8c7ea69e",
        "GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED",
        "runtime_authorized: false",
        "formal_project_activation: false",
    ], "Ginseng D0 integration record")
    print("[PASS] Ginseng D0 current accepted integration is explicit without rewriting prior authority")

    cos_audit = load("governance/COS_OWNERSHIP_STATE_CONTINUITY_AUDIT_2026-08-19.md")
    require(cos_audit, [
        "status: AUDIT / NOT CLOSURE",
        "SEMANTIC OWNERSHIP: durable high-level and cross-project state, continuity, provenance, and accepted cross-project state",
        "MUST NOT: own local project canon",
        "COS-C01 — state-owner drift",
        "COS-C02 — post-merge validator drift",
        "COS-C03 — open draft authority ambiguity",
        "COS OWNERSHIP / STATE / CONTINUITY: OPEN",
    ], "COS ownership/state/continuity audit")
    print("[PASS] COS ownership audit preserves local truth and rejects operational HOW ownership")

    index = load("ARCHIVE_INDEX.md")
    archive = load("archives/Archiwum09.md")
    require(index, ["archive/cos-v0-pilot-2026-07", "archive/cos-v0-pilot-pr3-2026-07", "archives/Archiwum09.md", "Warunek powrotu do cięższej architektury"], "ARCHIVE_INDEX.md")
    require(archive, [
        "GINSENG_TEST_2_S001_RESULT_v1_1.zip",
        "4abaf4696d4c7f832c99ccd3e7586e8618c45e893f5d0e2e3ce66c97206a36be",
        "GINSENG_TEST-003", "Find Skills", "Superpowers", "Claude-Mem",
        "Impeccable", "Task Observer", "Sprostowanie BPM:160", "SPIKE 001 IN PROGRESS",
    ], "Archiwum09.md")
    print("[PASS] Archiwum09 jest kompletne")

    require(load("README.md"), [
        "Creative OS — instrukcja operacyjna", "Hierarchia źródeł",
        "Aktywnym źródłem stanu przekrojowego jest jeden plik: [`CREATIVE_OS.md`](CREATIVE_OS.md).",
        "Lokalne systemy projektowe odpowiadają za",
    ], "README.md")
    require(load(".github/pull_request_template.md"), ["Problem / porażka", "Obserwowalny dowód zaliczenia", "Dodany koszt utrzymania"], "PR template")
    require(load("continuity/COLD_START_AUDIT-001.md"), ["PASS WITH FIXES", "ScriptOps"], "cold start 001")
    require(load("continuity/COLD_START_AUDIT-002.md"), ["PASS WITH FIXES", "START_HERE"], "cold start 002")
    print("[PASS] wcześniejsze kontrakty są zachowane")
    print("[PASS] Creative OS Lean jest spójny po Ginseng D0 integration i COS state-owner reconciliation")


if __name__ == "__main__":
    main()
