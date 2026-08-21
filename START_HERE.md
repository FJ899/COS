---
system: "Creative OS"
role: "single-entrypoint"
version: "1.1"
status: "ACTIVE"
state_owner: "CREATIVE_OS.md"
---

# START_HERE — Creative OS

Ten plik jest pojedynczą stacyjką Creative OS. Uruchamia odczyt właściwego stanu i prowadzi do lokalnego źródła prawdy wybranego projektu.

`START_HERE.md` nie jest właścicielem stanu projektu. Stan przekrojowy należy do `CREATIVE_OS.md`, szczegóły do lokalnych źródeł wskazanych niżej, a Human-owned global North Star + priority order są trwale zachowywane w `MASTER_TODO.md`.

`MASTER_TODO.md` nie jest schedulerem/routerem ani właścicielem priorytetów. Human jest semantic ownerem North Star i globalnej kolejności; COS tylko zachowuje tę decyzję.

## 1. Kontrakt wejścia

```text
PROJEKT: nazwa projektu | AUTO | ALL
TRYB: BOOT | WORK | AUDIT | PORTFOLIO
ZADANIE: opcjonalne polecenie
```

Domyślnie:

```text
PROJEKT: AUTO
TRYB: BOOT
```

Tryby:

- `BOOT` — odtwórz stan, blokadę i jeden następny krok; bez zmian;
- `WORK` — wykonaj jeden jawnie zlecony, odwracalny krok po pełnym BOOT, o ile nie ma blokady;
- `AUDIT` — oceń spójność i dowody; bez zmian;
- `PORTFOLIO` — pokaż Human-owned global priority/order z `MASTER_TODO.md` oraz high-level portfolio continuity z `CREATIVE_OS.md`; lokalne next steps nie stają się globalnym priorytetem.

## 2. Sekwencja zapłonu

1. Przeczytaj `README.md`.
2. Przeczytaj cały `CREATIVE_OS.md`.
3. Przeczytaj `MASTER_TODO.md` dla Human-owned North Star + global priority order.
4. Ustal projekt, tryb i oczekiwany rezultat.
5. Przy `PORTFOLIO` użyj `MASTER_TODO.md` dla globalnego order/intentu i `CREATIVE_OS.md` dla high-level continuity; nie promuj lokalnego `next step` do ecosystem `CURRENT PRIORITY`.
6. Dla pojedynczego projektu otwórz entrypoint z mapy poniżej.
7. Wykonaj lokalną kolejność startową.
8. Odczytaj co najmniej lokalny `PROJECT_STATE.md` i `HANDOFF.md`.
9. Porównaj stan lokalny z kartą projektu w COS i globalnym statusem klasy w `MASTER_TODO.md`.
10. Zastosuj hierarchię źródeł; nie rozwiązuj konfliktu przez zgadywanie.
11. Zwróć raport startowy, a dopiero potem zachowanie właściwe dla trybu.

Nie czytaj automatycznie branchy archiwalnych, pełnej dokumentacji innych projektów ani plików `continuity/COLD_START_*`, chyba że celem sesji jest audyt ciągłości.

Twarda zasada:

```text
LOCAL NEXT STEP
!=
ECOSYSTEM NEXT STEP
```

## 3. Mapa entrypointów

### Creative OS

```text
repo: JTJ07/COS
entrypoint: START_HERE.md
state_owner: CREATIVE_OS.md
global_priority_memory: MASTER_TODO.md
priority_semantic_owner: HUMAN
```

### ScriptOps

Alias: `Narzędzie pisarskie / ScriptOps`

```text
repo: JTJ07/scriptops
entrypoint: README.md
state_owner: PROJECT_STATE.md
handoff: HANDOFF.md
live_main: RESOLVE_FROM_LOCAL_REPO_AT_READ_TIME
last_observed_run003_integration_checkpoint: 43ab980d4e0af33bc9a628f3d8b70617a14fb9db
phase6_evidence: evidence/PHASE6_CONTROLLED_WORKFLOW_PROOF_2026-08-10.md
latest_bounded_evidence: evidence/P3_REAL_WORKLOAD_003_SCENE12_27_2026-08-19.md
```

Current high-level local meaning after the later Human semantic decision and PR #19 integration must be recovered from local `PROJECT_STATE.md`/`HANDOFF.md`. The accepted state includes:

```text
PHASE 6 CONTROLLED WORKFLOW MECHANISM PASS
BOUNDED PROPOSAL VIEW INTEGRATED
P3 RUN003 CROSS-SCENE PROPOSAL COHERENCE: OBSERVED PASS
SCN-012 + SCN-027 HUMAN SEMANTIC ACCEPTED
NO-CARRIER GOAL FOR BOUNDED SCOPE: SEMANTICALLY SATISFIED
CANONICAL EFFECT: PREPARED / NOT APPLIED
NO MATURITY CLAIM
```

The evaluation workload lived in a temporary ScriptOps project. Do not manufacture a fake canonical project merely to continue the test. Global `MASTER_TODO.md` classifies ScriptOps as `WAITING FOR REAL TARGET`; a real canonical target plus Human selection is required before this item re-enters global work.

Before consequential work resolve live `main` from the local repo and read current `PROJECT_STATE.md` + `HANDOFF.md`.

### BPM:160

```text
repo: JTJ07/COS
root: projects/bpm160
entrypoint: projects/bpm160/README.md
state_owner: projects/bpm160/PROJECT_STATE.md
handoff: projects/bpm160/HANDOFF.md
source_summary: projects/bpm160/SOURCE_SUMMARY_2026-07-31.md
```

Bieżąca lokalna bramka to `SPIKE 001 IN PROGRESS`:

```text
World → Signal → Peak Event → Aftermath
→ montaż próbny z audio
→ Evidence Package
```

Aktywna blokada wznowienia:

```text
ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME
```

Poprawna sekwencja:

```text
SOURCE IMPORT
→ READ_ONLY RECONCILIATION
→ ustalenie dokładnego stanu Spike 001
→ aktualizacja PROJECT_STATE.md
→ wznowienie pierwszego brakującego elementu Spike 001
```

Do zamknięcia Spike 001 nie otwieraj Market Scan, testów widzów, pomiaru fizjologicznego, rozszerzenia Canon ani dodatkowych światów.

`CORE / DETOUR / PARKING / DRIFT` jest protokołem globalnego COS. Nie przypisuj go jako historycznego protokołu BPM bez źródła. Lokalnie BPM używa trzech odrębnych osi:

```text
CORE / SUPPORT / EDITORIAL / REJECT
DOING NOW / NEXT / BACKLOG / PARKED / DONE
active / superseded / unresolved
```

### Creative OS Project Reconstructor

Alias: `Project Reconstructor`

```text
repo: JTJ07/creative-os-project-reconstructor
entrypoint: README.md
state_owner: PROJECT_STATE.md
canonical_prompt: PROMPT_STARTOWY.md
```

Run 001 jest zintegrowanym observed evidence; późniejszy P0 root-containment hardening również został Human-authorized i scalony. Prompt v1.0 można zmienić tylko po konkretnej porażce i z testem regresji. Przed consequential work resolve'uj live stan z lokalnego repo; COS nie traktuje zapisanych historycznych SHA jako perpetual current truth.

## 4. Reguły zatrzymania

Zatrzymaj pracę, gdy:

- pojawia się ryzyko utraty danych, złamania authority/security boundary, nieodwracalnego efektu albo utraty integrity/provenance;
- lokalny stan zawiera aktywną blokadę;
- wymagany plik albo repo jest niedostępne;
- źródła są sprzeczne, a hierarchia nie rozstrzyga;
- `WORK` wymaga zmiany celu, globalnego priorytetu, kanonu albo statusu bez decyzji użytkownika;
- dostępna jest tylko specyfikacja, plan lub pamięć AI bez dowodu wykonania.

Brak dostępu raportuj jako `ACCESS BLOCKED`. Brak źródła raportuj jako `SOURCE REQUIRED`. Nie uzupełniaj danych z pamięci AI.

Nowy finding nie staje się automatycznie zadaniem. Stosuj `MASTER_TODO.md` → `NIE GOŃ LISKA`.

## 5. Zachowanie według trybu

### BOOT

- tylko odczyt;
- pokaż lokalny stan, blokadę i lokalny next step;
- pokaż globalny priority status z `MASTER_TODO.md`, jeśli ma znaczenie dla decyzji czy w ogóle zaczynać pracę w tym repo;
- nie wykonuj następnego kroku.

### WORK

- najpierw pełny BOOT;
- potwierdź, że projekt/task jest zgodny z Human-owned `CURRENT PRIORITY` albo został jawnie wybrany przez Human;
- przy blokadzie zatrzymaj się;
- bez blokady wykonaj jeden krok wynikający z lokalnego stanu i polecenia;
- zmiany semantyczne wymagają jawnej decyzji;
- repo zmieniaj przez branch, walidację, PR i merge zgodnie z poleceniem.

### AUDIT

- tylko odczyt;
- wskaż sprzeczności, braki źródeł, fałszywe deklaracje i niejednoznaczne ścieżki;
- finding sam w sobie nie tworzy task authority;
- nie aktualizuj stanu podczas tego samego audytu.

### PORTFOLIO

- użyj `MASTER_TODO.md` jako trwałej pamięci Human-owned North Star i globalnego order;
- użyj `CREATIVE_OS.md` jako high-level cross-project continuity;
- pokaż CURRENT PRIORITY, NEXT, WAITING i PARKING oraz source-of-truth locators;
- nie promuj lokalnego `next step` do globalnego order;
- nie otwieraj lokalnych repo bez wskazania projektu lub potrzeby rozstrzygnięcia jawnej sprzeczności.

## 6. Wymagany raport startowy

```text
START SESSION
PROJEKT:
TRYB:
GLOBAL PRIORITY STATUS:
STATUS:
ŹRÓDŁO STANU:
GDZIE STANĘLIŚMY:
BRAK / BLOKADA:
JEDEN LOKALNY NASTĘPNY KROK:
SPRZECZNOŚCI: BRAK | LISTA
DZIAŁANIE: REPORT ONLY | STOPPED ON BLOCKER | READY FOR ONE STEP | EXECUTED
PYTANIE KIERUNKOWE: BRAK | JEDNO PYTANIE
```

`READY FOR ONE STEP` nie jest zgodą na zmianę kierunku. `EXECUTED` wymaga obserwowalnego dowodu.

## 7. Minimalne klucze

### BPM:160

```text
Uruchom Creative OS z repozytorium JTJ07/COS.
Wykonaj START_HERE.md.

PROJEKT: BPM:160
TRYB: BOOT
```

### ScriptOps

```text
Uruchom Creative OS z repozytorium JTJ07/COS.
Wykonaj START_HERE.md.

PROJEKT: ScriptOps
TRYB: BOOT
```

### Portfel

```text
Uruchom Creative OS z repozytorium JTJ07/COS.
Wykonaj START_HERE.md.

PROJEKT: ALL
TRYB: PORTFOLIO
```
