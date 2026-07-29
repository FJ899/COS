#!/usr/bin/env python3
"""Deterministyczna kontrola spójności Creative OS Lean."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CREATIVE_OS.md",
    "ARCHIVE_INDEX.md",
    ".gitignore",
    "continuity/COLD_START_AUDIT-001.md",
    "continuity/COLD_START_TEST-002.md",
    "scripts/README.md",
    ".github/pull_request_template.md",
    "projects/bpm160/README.md",
    "projects/bpm160/PROJECT_STATE.md",
    "projects/bpm160/HANDOFF.md",
    "projects/bpm160/DECISION_LOG.md",
    "projects/bpm160/SOURCE_MANIFEST.md",
    "projects/bpm160/IDEA_ARCHIVE.md",
]

EXPECTED_PROJECTS = {
    "Narzędzie pisarskie / ScriptOps": "QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED",
    "BPM:160": "PAUSED / QUEUED #2 / SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED",
    "Creative OS": "ACTIVE / LEAN PILOT",
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


def check_header_and_lean_owner(content: str) -> None:
    required = [
        "system: creative-os-lean",
        "version: 1.0",
        "status: ACTIVE_LEAN_PILOT",
        "Rozmowa prowadzi proces; repozytorium zachowuje stan.",
        "Każda informacja ma jednego właściciela.",
        "STARTED` / `OK` / `PARTIAL` / `BLOCKED` / `FAILED",
        "Przed dodaniem nowej funkcji lub warstwy",
        "obserwowalny test zaliczenia",
        "nowy koszt utrzymania",
    ]
    for marker in required:
        if marker not in content:
            fail(f"CREATIVE_OS.md nie zawiera wymaganej reguły: {marker}")
    if "prywatne repo" in content.lower():
        fail("CREATIVE_OS.md utrwala zmienną właściwość widoczności repozytorium")
    print("[PASS] nagłówek, właściciel stanu, truthful execution i Feature Razor są spójne")


def check_projects(content: str) -> None:
    rows = extract_project_rows(content)
    if set(rows) != set(EXPECTED_PROJECTS):
        fail(
            "tabela projektów ma nieoczekiwany zestaw: "
            f"expected={sorted(EXPECTED_PROJECTS)}, actual={sorted(rows)}"
        )

    for project, status_fragment in EXPECTED_PROJECTS.items():
        cells = rows[project]
        if status_fragment not in cells[1]:
            fail(f"projekt {project} ma niespójny status: {cells[1]}")
        if not cells[4] or cells[4] == "-":
            fail(f"projekt {project} nie ma jednego następnego kroku")
        if not cells[5] or cells[5] == "-":
            fail(f"projekt {project} nie ma źródła prawdy")

    bpm = rows["BPM:160"]
    if "projects/bpm160/PROJECT_STATE.md" not in bpm[5]:
        fail("BPM:160 nie wskazuje dostępnego lokalnego źródła prawdy")

    scriptops = rows["Narzędzie pisarskie / ScriptOps"]
    if "legacy/scriptops-v2-single.py" not in scriptops[2] or "sources/RC1_SCOPE_LOCK.md" not in scriptops[3]:
        fail("karta ScriptOps nie wskazuje kanonicznego prototypu i aktualnej ścieżki zakresu")

    print(f"[PASS] tabela projektów: {len(rows)} spójne wpisy")


def check_idea_inbox(content: str) -> None:
    blocks = re.split(r"(?=^### IDEA-)", content, flags=re.MULTILINE)
    idea_blocks = [block for block in blocks if block.startswith("### IDEA-")]
    if len(idea_blocks) < 6:
        fail("Idea Inbox nie zawiera oczekiwanego zestawu pomysłów")

    for block in idea_blocks:
        title = block.splitlines()[0]
        if "PARKING" in title or "`PARKING`" in block:
            if "Warunek powrotu" not in block and "Powrót:" not in block:
                fail(f"wpis PARKING nie ma warunku powrotu: {title}")

    for marker in [
        "IDEA-2026-005 — GitHub Issues / Projects jako widoki pochodne",
        "IDEA-2026-006 — ciągły Reconstructor monitorujący rozmowy",
    ]:
        if marker not in content:
            fail(f"Idea Inbox nie zachowuje pomysłu z analiz: {marker}")

    print(f"[PASS] Idea Inbox: {len(idea_blocks)} wpisów z warunkami powrotu")


def check_handoff(content: str) -> None:
    required = [
        "### DEC-2026-004 — Lean Feature Razor i odzyskiwanie BPM:160",
        "Decision Logi przechowują decyzje semantyczne",
        "Maszynowy nagłówek YAML jest testowany",
        "GitHub Issues, GitHub Projects, centralny dashboard i ciągły Reconstructor pozostają `PARKING`",
        "cold start 002 `PREPARED / NOT EXECUTED`",
        "BPM:160 `PAUSED / SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED`",
        "Następny krok: wykonać operacyjny cold start 002",
    ]
    for marker in required:
        if marker not in content:
            fail(f"Aktualny Handoff nie zawiera: {marker}")
    print("[PASS] Aktualny Handoff zachowuje decyzje Lean po analizach")


def check_bpm_source() -> None:
    state = read_text("projects/bpm160/PROJECT_STATE.md")
    handoff = read_text("projects/bpm160/HANDOFF.md")
    decisions = read_text("projects/bpm160/DECISION_LOG.md")
    sources = read_text("projects/bpm160/SOURCE_MANIFEST.md")
    ideas = read_text("projects/bpm160/IDEA_ARCHIVE.md")

    for marker in [
        'project: "BPM:160"',
        'status: "SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED"',
        'state_owner: "projects/bpm160/PROJECT_STATE.md"',
        "SOURCE RECOVERY FOUND — READ_ONLY REVIEW REQUIRED",
        "SOURCE RECOVERY NOT FOUND — PROCEED TO MINIMAL VIEWER TEST DEFINITION",
        "Nie wolno uzupełniać szczegółów projektu z pamięci AI",
    ]:
        if marker not in state:
            fail(f"PROJECT_STATE BPM:160 nie zawiera: {marker}")

    for marker in [
        'blocker: "SOURCE RECOVERY REQUIRED"',
        'resume_contract: "READ_ONLY / RECOVERY FIRST"',
        "Nagłówek YAML jest maszynowym skrótem",
    ]:
        if marker not in handoff:
            fail(f"HANDOFF BPM:160 nie zawiera: {marker}")

    for marker in ["DEC-BPM-001", "DEC-BPM-005", "test widza", "nie wolno odtwarzać przez zgadywanie"]:
        if marker not in decisions:
            fail(f"DECISION_LOG BPM:160 nie zawiera: {marker}")

    for marker in ["23_LIVE_TODO.md", "niedostępne", "Reguła importu"]:
        if marker not in sources:
            fail(f"SOURCE_MANIFEST BPM:160 nie zawiera: {marker}")

    if "Brak dostępnych lokalnych źródeł" not in ideas or "nie mogą zastępować odzyskiwania źródeł" not in ideas:
        fail("IDEA_ARCHIVE BPM:160 nie zachowuje granicy niepewności")

    print("[PASS] BPM:160 ma dostępny, jawnie niepełny i bezpieczny punkt wznowienia")


def check_instructions() -> None:
    readme = read_text("README.md")
    required_readme = [
        "Creative OS — instrukcja operacyjna",
        "# 4. Start każdej sesji",
        "# 6. Obsługa każdego nowego pomysłu",
        "Hierarchia źródeł",
    ]
    for marker in required_readme:
        if marker not in readme:
            fail(f"README.md nie zawiera wymaganej instrukcji: {marker}")

    validation = read_text("scripts/README.md")
    for marker in [
        "python scripts/verify_creative_os.py",
        "GitHub Actions",
        "PARKING",
        "lokalnego stanu BPM:160",
        "filtra użyteczności",
    ]:
        if marker not in validation:
            fail(f"scripts/README.md nie zawiera instrukcji: {marker}")
    print("[PASS] instrukcje startu, pomysłów i walidacji są dostępne")


def check_pull_request_filter() -> None:
    template = read_text(".github/pull_request_template.md")
    required = [
        "Problem / porażka",
        "Dlaczego obecny mechanizm nie wystarcza",
        "Obserwowalny dowód zaliczenia",
        "Dodany koszt utrzymania",
        "Poza zakresem",
        "Wpływ na stan semantyczny",
    ]
    for marker in required:
        if marker not in template:
            fail(f"szablon PR nie zawiera filtra: {marker}")
    print("[PASS] filtr PR chroni przed rozbudową bez dowodu")


def check_archive() -> None:
    archive = read_text("ARCHIVE_INDEX.md")
    required = [
        "archive/cos-v0-pilot-2026-07",
        "77a2544409a0cd56c9ddc4fb341ec0e721b29919",
        "archive/cos-v0-pilot-pr3-2026-07",
        "2f888d61ba582a766b4e245553cdae1a9373af79",
        "Warunek powrotu do cięższej architektury",
    ]
    for marker in required:
        if marker not in archive:
            fail(f"ARCHIVE_INDEX.md nie zawiera: {marker}")
    print("[PASS] archiwum i warunek reopen są zabezpieczone")


def check_continuity() -> None:
    audit = read_text("continuity/COLD_START_AUDIT-001.md")
    required_audit = [
        "PUBLIC / NO PRIOR MEMORY / READ_ONLY",
        "PASS WITH FIXES",
        "ScriptOps — PASS",
        "BPM:160",
        "OPERATIONAL TEST REQUIRED",
    ]
    for marker in required_audit:
        if marker not in audit:
            fail(f"audyt ciągłości nie zawiera: {marker}")

    test = read_text("continuity/COLD_START_TEST-002.md")
    required_test = [
        "PREPARED / NOT EXECUTED",
        "IDEA-2026-005",
        "projects/bpm160/PROJECT_STATE.md",
        "SOURCE RECOVERY REQUIRED",
        "legacy/scriptops-v2-single.py",
        "COLD_START_AUDIT-002.md",
    ]
    for marker in required_test:
        if marker not in test:
            fail(f"test operacyjny 002 nie zawiera: {marker}")

    print("[PASS] audyt 001 jest zapisany, a test operacyjny 002 gotowy")


def main() -> None:
    check_required_files()
    content = read_text("CREATIVE_OS.md")
    check_header_and_lean_owner(content)
    check_projects(content)
    check_idea_inbox(content)
    check_handoff(content)
    check_bpm_source()
    check_instructions()
    check_pull_request_filter()
    check_archive()
    check_continuity()
    print("[PASS] Creative OS Lean jest spójny i ma odtwarzalne punkty wejścia")


if __name__ == "__main__":
    main()
