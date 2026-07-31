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
        "STARTED / OK / PARTIAL / BLOCKED / FAILED",
        "Navigation Protocol jest mechanizmem globalnego COS",
        "GINSENG_TEST-003 — zamknięcie pojedynczej bramki",
        "IDEA-2026-007 — zewnętrzne skille jako warstwa pomocnicza",
        "DEC-2026-006 — kolejny test Ginseng i korekta BPM:160",
        "EVOLUTION-2026-013 — korekta BPM i test Ginseng",
        "archives/Archiwum09.md",
    ], "CREATIVE_OS.md")

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
    print("[PASS] CREATIVE_OS.md jest spójny")

    start = load("START_HERE.md")
    require(start, [
        'role: "single-entrypoint"', "BOOT | WORK | AUDIT | PORTFOLIO",
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
    print("[PASS] START_HERE.md jest spójny")

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
        'status: "QUEUED / NOT EXECUTED"', "SINGLE_GATE_CLOSURE",
        "VARIANT_A_KEEP_DEC002", "VARIANT_B_SUPERSEDE_DEC002",
        "blocking_gate_count_after = 6", "implementation_readiness_after = BLOCKED",
        "baseline_mutated_after = false", "systematic-debugging",
        "verification-before-completion", "S001_gate_closure_delta.json",
        "aktywuje Ginseng jako formalnego projektu",
    ], "GINSENG_TEST-003")
    if "Ten test nie:" not in test:
        fail("GINSENG_TEST-003 nie zapisuje granicy poza zakresem")
    print("[PASS] GINSENG_TEST-003 jest zakolejkowany")

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

    require(load("README.md"), ["Creative OS — instrukcja operacyjna", "Hierarchia źródeł"], "README.md")
    require(load(".github/pull_request_template.md"), ["Problem / porażka", "Obserwowalny dowód zaliczenia", "Dodany koszt utrzymania"], "PR template")
    require(load("continuity/COLD_START_AUDIT-001.md"), ["PASS WITH FIXES", "ScriptOps"], "cold start 001")
    require(load("continuity/COLD_START_AUDIT-002.md"), ["PASS WITH FIXES", "START_HERE"], "cold start 002")
    print("[PASS] wcześniejsze kontrakty są zachowane")
    print("[PASS] Creative OS Lean jest spójny po korekcie BPM:160 i kolejce Ginseng")


if __name__ == "__main__":
    main()
