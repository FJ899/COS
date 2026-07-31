#!/usr/bin/env python3
"""Deterministyczna kontrola spójności Creative OS Lean."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "START_HERE.md",
    "README.md",
    "CREATIVE_OS.md",
    "ARCHIVE_INDEX.md",
    ".gitignore",
    ".github/pull_request_template.md",
    "scripts/README.md",
    "continuity/COLD_START_AUDIT-001.md",
    "continuity/COLD_START_TEST-002.md",
    "continuity/COLD_START_AUDIT-002.md",
    "tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md",
    "archives/Archiwum09.md",
    "projects/bpm160/README.md",
    "projects/bpm160/PROJECT_STATE.md",
    "projects/bpm160/HANDOFF.md",
    "projects/bpm160/SOURCE_SUMMARY_2026-07-31.md",
    "projects/bpm160/DECISION_LOG.md",
    "projects/bpm160/SOURCE_MANIFEST.md",
    "projects/bpm160/IDEA_ARCHIVE.md",
]

EXPECTED_PROJECTS = {
    "Narzędzie pisarskie / ScriptOps": "QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED",
    "BPM:160": "QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / SOURCE SUMMARY CONFIRMED / ORIGINAL FILES REQUIRED",
    "Creative OS": "ACTIVE / LEAN PILOT / START_HERE ACTIVE",
    "Creative OS Project Reconstructor": "ACTIVE / V1.0 STABILIZATION",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path} nie jest poprawnym UTF-8: {exc}")
    raise AssertionError("unreachable")


def require_markers(content: str, markers: list[str], owner: str) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} nie zawiera: {marker}")


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("brak wymaganych plików: " + ", ".join(missing))
    print(f"[PASS] wymagane pliki: {len(REQUIRED_FILES)}")


def extract_project_rows(content: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    in_table = False
    for line in content.splitlines():
        if line.startswith("| Projekt | Status |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and not line.startswith("|"):
            break
        if in_table:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 6:
                fail(f"wiersz tabeli projektów nie ma 6 kolumn: {line}")
            rows[cells[0]] = cells
    return rows


def check_creative_os() -> None:
    content = read_text("CREATIVE_OS.md")
    require_markers(
        content,
        [
            "system: creative-os-lean",
            "status: ACTIVE_LEAN_PILOT",
            "Rozmowa prowadzi proces; repozytorium zachowuje stan.",
            "Każda informacja ma jednego właściciela.",
            "STARTED / OK / PARTIAL / BLOCKED / FAILED",
            "Pojedynczym entrypointem uruchomienia jest `START_HERE.md`",
            "Navigation Protocol jest mechanizmem globalnego COS",
            "## 3. Kolejka testów",
            "GINSENG_TEST-003 — zamknięcie pojedynczej bramki",
            "blocking_gate_count",
            "IDEA-2026-007 — zewnętrzne skille jako warstwa pomocnicza",
            "### DEC-2026-006 — kolejny test Ginseng i korekta BPM:160",
            "EVOLUTION-2026-013 — korekta BPM i test Ginseng",
            "archives/Archiwum09.md",
        ],
        "CREATIVE_OS.md",
    )

    rows = extract_project_rows(content)
    if set(rows) != set(EXPECTED_PROJECTS):
        fail(f"nieoczekiwany zestaw projektów: {sorted(rows)}")

    for project, expected_status in EXPECTED_PROJECTS.items():
        cells = rows[project]
        if expected_status not in cells[1]:
            fail(f"projekt {project} ma niespójny status: {cells[1]}")
        if not cells[4] or not cells[5]:
            fail(f"projekt {project} nie ma następnego kroku albo źródła")

    bpm = rows["BPM:160"]
    if "Spike 001" not in bpm[2] or "testów widzów" not in bpm[2]:
        fail("karta BPM:160 nie zapisuje Spike 001 i parkingu testów widzów")
    if "READ_ONLY RECONCILIATION" not in bpm[4]:
        fail("karta BPM:160 nie wskazuje reconciliation")

    ideas = re.findall(r"^### IDEA-", content, flags=re.MULTILINE)
    if len(ideas) < 7:
        fail("Idea Inbox nie zawiera co najmniej siedmiu wpisów")

    print("[PASS] CREATIVE_OS.md ma spójną tabelę, kolejkę testów i handoff")


def check_start_here() -> None:
    start = read_text("START_HERE.md")
    require_markers(
        start,
        [
            'role: "single-entrypoint"',
            "BOOT | WORK | AUDIT | PORTFOLIO",
            "## 2. Sekwencja zapłonu",
            "repo: litrgratis-pixel/scriptops",
            "critical_scope: sources/RC1_SCOPE_LOCK.md",
            "root: projects/bpm160",
            "source_summary: projects/bpm160/SOURCE_SUMMARY_2026-07-31.md",
            "SPIKE 001 IN PROGRESS",
            "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME",
            "SOURCE IMPORT",
            "READ_ONLY RECONCILIATION",
            "Market Scan",
            "testów widzów",
            "CORE / SUPPORT / EDITORIAL / REJECT",
            "DOING NOW / NEXT / BACKLOG / PARKED / DONE",
            "active / superseded / unresolved",
            "repo: litrgratis-pixel/creative-os-project-reconstructor",
            "ACCESS BLOCKED",
            "SOURCE REQUIRED",
            "START SESSION",
            "continuity/COLD_START_*",
        ],
        "START_HERE.md",
    )
    for mode in ["### BOOT", "### WORK", "### AUDIT", "### PORTFOLIO"]:
        if mode not in start:
            fail(f"START_HERE.md nie definiuje trybu: {mode}")
    print("[PASS] START_HERE.md prowadzi do skorygowanego BPM:160")


def check_bpm() -> None:
    readme = read_text("projects/bpm160/README.md")
    state = read_text("projects/bpm160/PROJECT_STATE.md")
    handoff = read_text("projects/bpm160/HANDOFF.md")
    summary = read_text("projects/bpm160/SOURCE_SUMMARY_2026-07-31.md")
    decisions = read_text("projects/bpm160/DECISION_LOG.md")
    manifest = read_text("projects/bpm160/SOURCE_MANIFEST.md")
    ideas = read_text("projects/bpm160/IDEA_ARCHIVE.md")

    require_markers(
        readme,
        ["SPIKE 001 IN PROGRESS", "World → Signal → Peak Event → Aftermath", "testy widzów", "READ_ONLY RECONCILIATION"],
        "BPM README",
    )
    require_markers(
        state,
        [
            'portfolio_status: "QUEUED #2"',
            'local_work_state: "SPIKE 001 IN PROGRESS"',
            'status: "SOURCE SUMMARY CONFIRMED / ORIGINAL SOURCE FILES REQUIRED"',
            "Brand Promise oznacza adrenalinę i rytm",
            "Canon / Konstytucja BPM160 v1.2",
            "Czy BPM160 da się zrealizować przy akceptowalnej jakości, czasie i koszcie?",
            "CORE / SUPPORT / EDITORIAL / REJECT",
            "DOING NOW / NEXT / BACKLOG / PARKED / DONE",
            "active / superseded / unresolved",
            "UNCONFIRMED / SOURCE REQUIRED",
            "Market Scan v0",
            "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME",
        ],
        "BPM PROJECT_STATE",
    )
    require_markers(
        handoff,
        [
            'blocker: "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME"',
            'resume_contract: "READ_ONLY RECONCILIATION / SPIKE FIRST"',
            "SPIKE 001 IN PROGRESS",
            "Producent / Walidator / Turbo / QA",
            "Navigation Protocol",
        ],
        "BPM HANDOFF",
    )
    require_markers(
        summary,
        [
            "USER_SUPPLIED_SOURCE_SUMMARY",
            "Brand Promise oznacza adrenalinę i rytm",
            "Minimal Montage Rule",
            "Spike 001",
            "Higgsfield Cinema Studio",
            "bpm160-heartbeat-guide.wav",
            "Trzy różne osie",
            "UNCONFIRMED AS BPM:160 INTERNAL MECHANISM",
            "PARTIALLY CONFIRMED",
        ],
        "BPM SOURCE SUMMARY",
    )
    require_markers(decisions, ["DEC-BPM-009", "Spike 001", "testy widzów", "Navigation Protocol"], "BPM DECISION_LOG")
    require_markers(manifest, ["ORIGINAL PROJECT FILES: REQUIRED", "Canon / Konstytucja", "Reguła importu"], "BPM SOURCE_MANIFEST")
    require_markers(ideas, ["## DOING NOW", "## PARKED", "Market Scan v0", "Testy widzów", "Pomiar fizjologiczny"], "BPM IDEA_ARCHIVE")

    print("[PASS] BPM:160 ma skorygowany zakres, klasyfikacje i bramkę Spike 001")


def check_ginseng_test() -> None:
    test = read_text("tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md")
    require_markers(
        test,
        [
            'status: "QUEUED / NOT EXECUTED"',
            "SINGLE_GATE_CLOSURE",
            "VARIANT_A_KEEP_DEC002",
            "VARIANT_B_SUPERSEDE_DEC002",
            "blocking_gate_count_after = 6",
            "implementation_readiness_after = BLOCKED",
            "baseline_mutated_after = false",
            "systematic-debugging",
            "verification-before-completion",
            "S001_gate_closure_delta.json",
            "nie aktywuje Ginseng jako formalnego projektu",
        ],
        "GINSENG_TEST-003",
    )
    print("[PASS] GINSENG_TEST-003 jest zakolejkowany z kryteriami celu i regresji")


def check_archive() -> None:
    index = read_text("ARCHIVE_INDEX.md")
    archive = read_text("archives/Archiwum09.md")

    require_markers(
        index,
        [
            "archive/cos-v0-pilot-2026-07",
            "77a2544409a0cd56c9ddc4fb341ec0e721b29919",
            "archive/cos-v0-pilot-pr3-2026-07",
            "2f888d61ba582a766b4e245553cdae1a9373af79",
            "archives/Archiwum09.md",
            "Warunek powrotu do cięższej architektury",
        ],
        "ARCHIVE_INDEX.md",
    )
    require_markers(
        archive,
        [
            "GINSENG_TEST_2_S001_RESULT_v1_1.zip",
            "4abaf4696d4c7f832c99ccd3e7586e8618c45e893f5d0e2e3ce66c97206a36be",
            "GINSENG_TEST-003",
            "Find Skills",
            "Superpowers",
            "Claude-Mem",
            "Impeccable",
            "Task Observer",
            "Sprostowanie BPM:160",
            "SPIKE 001 IN PROGRESS",
        ],
        "Archiwum09.md",
    )
    print("[PASS] Archiwum09 jest zapisane i zindeksowane")


def check_existing_contracts() -> None:
    readme = read_text("README.md")
    template = read_text(".github/pull_request_template.md")
    audit_001 = read_text("continuity/COLD_START_AUDIT-001.md")
    audit_002 = read_text("continuity/COLD_START_AUDIT-002.md")

    require_markers(readme, ["Creative OS — instrukcja operacyjna", "Hierarchia źródeł"], "README.md")
    require_markers(template, ["Problem / porażka", "Obserwowalny dowód zaliczenia", "Dodany koszt utrzymania"], "PR template")
    require_markers(audit_001, ["PASS WITH FIXES", "ScriptOps"], "COLD_START_AUDIT-001")
    require_markers(audit_002, ["PASS WITH FIXES", "START_HERE"], "COLD_START_AUDIT-002")
    print("[PASS] wcześniejsze kontrakty ciągłości i Feature Razor są zachowane")


def main() -> None:
    check_required_files()
    check_creative_os()
    check_start_here()
    check_bpm()
    check_ginseng_test()
    check_archive()
    check_existing_contracts()
    print("[PASS] Creative OS Lean jest spójny po korekcie BPM:160 i zakolejkowaniu testu Ginseng")


if __name__ == "__main__":
    main()
