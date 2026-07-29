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
    "continuity/COLD_START_AUDIT-001.md",
    "continuity/COLD_START_TEST-002.md",
    "continuity/COLD_START_AUDIT-002.md",
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
        "Pojedynczym entrypointem uruchomienia jest `START_HERE.md`",
        "`START_HERE.md` jest mapą uruchomienia, nie właścicielem stanu",
    ]
    for marker in required:
        if marker not in content:
            fail(f"CREATIVE_OS.md nie zawiera wymaganej reguły: {marker}")
    if "prywatne repo" in content.lower():
        fail("CREATIVE_OS.md utrwala zmienną właściwość widoczności repozytorium")
    print("[PASS] nagłówek, właściciel stanu, truthful execution i stacyjka są spójne")


def check_start_here() -> None:
    start = read_text("START_HERE.md")

    required = [
        'role: "single-entrypoint"',
        'status: "ACTIVE"',
        'state_owner: "CREATIVE_OS.md"',
        "# START_HERE — Creative OS",
        "nie jest właścicielem stanu projektu",
        "BOOT | WORK | AUDIT | PORTFOLIO",
        "## 2. Sekwencja zapłonu",
        "Przeczytaj `README.md`",
        "Przeczytaj cały `CREATIVE_OS.md`",
        "## 3. Mapa entrypointów",
        "repo: litrgratis-pixel/scriptops",
        "entrypoint: README.md",
        "critical_scope: sources/RC1_SCOPE_LOCK.md",
        "root: projects/bpm160",
        "entrypoint: projects/bpm160/README.md",
        "repo: litrgratis-pixel/creative-os-project-reconstructor",
        "canonical_prompt: PROMPT_STARTOWY.md",
        "SOURCE RECOVERY FOUND",
        "READ_ONLY REVIEW",
        "SOURCE RECOVERY NOT FOUND",
        "PROCEED TO MINIMAL VIEWER TEST DEFINITION",
        "ACCESS BLOCKED",
        "SOURCE REQUIRED",
        "## 6. Wymagany raport startowy",
        "START SESSION",
        "STOPPED ON BLOCKER",
        "## 7. Minimalny klucz użytkownika",
        "continuity/COLD_START_*",
    ]
    for marker in required:
        if marker not in start:
            fail(f"START_HERE.md nie zawiera kontraktu: {marker}")

    for mode in ["### BOOT", "### WORK", "### AUDIT", "### PORTFOLIO"]:
        if mode not in start:
            fail(f"START_HERE.md nie definiuje trybu: {mode}")

    if "nie kopi" not in start.lower() and "nie zastępuje" not in start.lower():
        fail("START_HERE.md nie chroni przed utworzeniem drugiego źródła prawdy")

    print("[PASS] START_HERE.md definiuje pojedynczą stacyjkę i mapę entrypointów")


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
    if "FOUND" not in bpm[3] or "NOT FOUND" not in bpm[3]:
        fail("karta BPM:160 nie rozróżnia wyników odzyskiwania")

    scriptops = rows["Narzędzie pisarskie / ScriptOps"]
    if "legacy/scriptops-v2-single.py" not in scriptops[2] or "sources/RC1_SCOPE_LOCK.md" not in scriptops[3]:
        fail("karta ScriptOps nie wskazuje kanonicznego prototypu i aktualnej ścieżki zakresu")

    creative_os = rows["Creative OS"]
    if "START_HERE.md" not in creative_os[2]:
        fail("karta Creative OS nie zapisuje aktywnej stacyjki")
    if "minimalnego klucza" not in creative_os[3]:
        fail("karta Creative OS nie zachowuje brakującego testu stacyjki")

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
        "### DEC-2026-005 — pojedyncza stacyjka Creative OS",
        "Rootowy `START_HERE.md` jest jedynym standardowym entrypointem",
        "BOOT / WORK / AUDIT / PORTFOLIO",
        "Mapa entrypointów prowadzi do lokalnych README",
        "Cold start 002 otrzymał `PASS WITH FIXES`",
        "FOUND → REVIEW → STATE UPDATE",
        "NOT FOUND → VIEWER TEST DEFINITION",
        "continuity/COLD_START_*",
        "START_HERE ACTIVE",
        "test pojedynczej stacyjki `REQUIRED`",
        "Następny krok: uruchomić w nowej sesji minimalny klucz",
    ]
    for marker in required:
        if marker not in content:
            fail(f"Aktualny Handoff nie zawiera: {marker}")
    print("[PASS] Aktualny Handoff zachowuje decyzję o pojedynczej stacyjce")


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
        "### Gdy wynik to `FOUND`",
        "zaktualizować `PROJECT_STATE.md` minimalną deltą",
        "### Gdy wynik to `NOT FOUND`",
        "Można przejść bezpośrednio do definicji minimalnego testu widza",
        "Nie wolno uzupełniać szczegółów projektu z pamięci AI",
    ]:
        if marker not in state:
            fail(f"PROJECT_STATE BPM:160 nie zawiera: {marker}")

    for marker in [
        'blocker: "SOURCE RECOVERY REQUIRED"',
        'resume_contract: "READ_ONLY / RECOVERY FIRST"',
        "Nagłówek YAML jest maszynowym skrótem",
        "## Rozgałęzienie po wyniku",
        "READ_ONLY REVIEW",
        "aktualizacja PROJECT_STATE.md",
        "PROCEED TO MINIMAL VIEWER TEST DEFINITION",
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

    print("[PASS] BPM:160 ma jednoznaczne rozgałęzienie po odzyskaniu źródeł")


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
        "START_HERE.md",
        "BOOT / WORK / AUDIT / PORTFOLIO",
        "lokalnego stanu BPM:160",
        "SOURCE RECOVERY FOUND / NOT FOUND",
        "filtra użyteczności",
        "cold startu 002",
    ]:
        if marker not in validation:
            fail(f"scripts/README.md nie zawiera instrukcji: {marker}")
    print("[PASS] instrukcje startu, stacyjki i walidacji są dostępne")


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
    audit_001 = read_text("continuity/COLD_START_AUDIT-001.md")
    for marker in [
        "PUBLIC / NO PRIOR MEMORY / READ_ONLY",
        "PASS WITH FIXES",
        "ScriptOps — PASS",
        "BPM:160",
        "OPERATIONAL TEST REQUIRED",
    ]:
        if marker not in audit_001:
            fail(f"audyt ciągłości 001 nie zawiera: {marker}")

    test_002 = read_text("continuity/COLD_START_TEST-002.md")
    for marker in [
        "EXECUTED / PASS WITH FIXES",
        "continuity/COLD_START_AUDIT-002.md",
        "IDEA-2026-005",
        "projects/bpm160/PROJECT_STATE.md",
        "SOURCE RECOVERY REQUIRED",
        "legacy/scriptops-v2-single.py",
        "FOUND":
    ]:
        pass
