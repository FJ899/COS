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
    "scripts/README.md",
]

EXPECTED_PROJECTS = {
    "Narzędzie pisarskie / ScriptOps": "QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED",
    "BPM:160": "PAUSED / QUEUED #2",
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
    ]
    for marker in required:
        if marker not in content:
            fail(f"CREATIVE_OS.md nie zawiera wymaganej reguły: {marker}")
    if "prywatne repo" in content.lower():
        fail("CREATIVE_OS.md utrwala zmienną właściwość widoczności repozytorium")
    print("[PASS] nagłówek, właściciel stanu i truthful execution są spójne")


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

    print(f"[PASS] tabela projektów: {len(rows)} spójne wpisy")


def check_idea_inbox(content: str) -> None:
    blocks = re.split(r"(?=^### IDEA-)", content, flags=re.MULTILINE)
    idea_blocks = [block for block in blocks if block.startswith("### IDEA-")]
    if len(idea_blocks) < 4:
        fail("Idea Inbox nie zawiera oczekiwanego zestawu pomysłów")

    for block in idea_blocks:
        title = block.splitlines()[0]
        if "PARKING" in title or "`PARKING`" in block:
            if "Warunek powrotu" not in block and "Powrót:" not in block:
                fail(f"wpis PARKING nie ma warunku powrotu: {title}")
    print(f"[PASS] Idea Inbox: {len(idea_blocks)} wpisy z warunkami powrotu")


def check_handoff(content: str) -> None:
    required = [
        "### DEC-2026-003 — uczciwe wykonanie w architekturze lean",
        "Stan: Creative OS `ACTIVE / LEAN PILOT / TRUTHFUL EXECUTION ACTIVE`",
        "ScriptOps `QUEUED #1 / NOT ACTIVATED / ACCESS CHECK REQUIRED`",
        "BPM:160 `PAUSED / SOURCE PATH REQUIRED`",
        "Evidence-Guided Maintenance Loop `PARKED / CONTRACT PREPARED`",
        "Następny krok: przeprowadzić operacyjny cold start",
    ]
    for marker in required:
        if marker not in content:
            fail(f"Aktualny Handoff nie zawiera: {marker}")
    print("[PASS] Aktualny Handoff zachowuje truthful execution i wynik cold startu")


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
    for marker in ["python scripts/verify_creative_os.py", "GitHub Actions", "PARKING"]:
        if marker not in validation:
            fail(f"scripts/README.md nie zawiera instrukcji: {marker}")
    print("[PASS] instrukcje startu, pomysłów i walidacji są dostępne")


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


def check_continuity_audit() -> None:
    audit = read_text("continuity/COLD_START_AUDIT-001.md")
    required = [
        "PUBLIC / NO PRIOR MEMORY / READ_ONLY",
        "PASS WITH FIXES",
        "ScriptOps — PASS",
        "BPM:160",
        "OPERATIONAL TEST REQUIRED",
    ]
    for marker in required:
        if marker not in audit:
            fail(f"audyt ciągłości nie zawiera: {marker}")
    print("[PASS] niezależny audyt ciągłości jest zapisany")


def main() -> None:
    check_required_files()
    content = read_text("CREATIVE_OS.md")
    check_header_and_lean_owner(content)
    check_projects(content)
    check_idea_inbox(content)
    check_handoff(content)
    check_instructions()
    check_archive()
    check_continuity_audit()
    print("[PASS] Creative OS Lean jest spójny i ma odtwarzalny punkt wejścia")


if __name__ == "__main__":
    main()
