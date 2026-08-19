---
system: "Creative OS"
role: "single-entrypoint"
version: "1.1"
status: "ACTIVE"
state_owner: "CREATIVE_OS.md"
---

# START_HERE — Creative OS

Ten plik jest pojedynczą stacyjką Creative OS. Uruchamia odczyt właściwego stanu i prowadzi do lokalnego źródła prawdy wybranego projektu.

`START_HERE.md` nie jest właścicielem stanu projektu. Stan przekrojowy należy do `CREATIVE_OS.md`, a szczegóły do lokalnych źródeł wskazanych niżej.

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
- `PORTFOLIO` — pokaż stan projektów wyłącznie na poziomie `CREATIVE_OS.md`.

## 2. Sekwencja zapłonu

1. Przeczytaj `README.md`.
2. Przeczytaj cały `CREATIVE_OS.md`.
3. Ustal projekt, tryb i oczekiwany rezultat.
4. Przy `PORTFOLIO` użyj wyłącznie tabeli projektów w `CREATIVE_OS.md`.
5. Dla pojedynczego projektu otwórz entrypoint z mapy poniżej.
6. Wykonaj lokalną kolejność startową.
7. Odczytaj co najmniej lokalny `PROJECT_STATE.md` i `HANDOFF.md`.
8. Porównaj stan lokalny z kartą projektu w COS.
9. Zastosuj hierarchię źródeł; nie rozwiązuj konfliktu przez zgadywanie.
10. Zwróć raport startowy, a dopiero potem zachowanie właściwe dla trybu.

Nie czytaj automatycznie branchy archiwalnych, pełnej dokumentacji innych projektów ani plików `continuity/COLD_START_*`, chyba że celem sesji jest audyt ciągłości.

## 3. Mapa entrypointów

### Creative OS

```text
repo: JTJ07/COS
entrypoint: START_HERE.md
state_owner: CREATIVE_OS.md
```

### ScriptOps

Alias: `Narzędzie pisarskie / ScriptOps`

```text
repo: JTJ07/scriptops
entrypoint: README.md
state_owner: PROJECT_STATE.md
handoff: HANDOFF.md
current_main: daa6e5dc210e09171a530eeffe5601e0e74ae041
phase6_evidence: evidence/PHASE6_CONTROLLED_WORKFLOW_PROOF_2026-08-10.md
```

Aktualny lokalny state owner raportuje:

```text
PHASE 6 CONTROLLED WORKFLOW MECHANISM PASS
NO MATURITY CLAIM
SADDLE LIVE MODEL EVIDENCE NEXT
```

Nie cofaj ScriptOps do historycznego `ACCESS CHECK REQUIRED`. Przed pracą odczytaj aktualny `PROJECT_STATE.md`; COS przechowuje tylko przekrojowy status i locator, nie lokalny backlog ani kanon.

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

Prompt v1.0 można zmienić tylko po konkretnej porażce i z testem regresji.

## 4. Reguły zatrzymania

Zatrzymaj pracę, gdy:

- lokalny stan zawiera aktywną blokadę;
- wymagany plik albo repo jest niedostępne;
- źródła są sprzeczne, a hierarchia nie rozstrzyga;
- `WORK` wymaga zmiany celu, priorytetu, kanonu albo statusu bez decyzji użytkownika;
- dostępna jest tylko specyfikacja, plan lub pamięć AI bez dowodu wykonania.

Brak dostępu raportuj jako `ACCESS BLOCKED`. Brak źródła raportuj jako `SOURCE REQUIRED`. Nie uzupełniaj danych z pamięci AI.

## 5. Zachowanie według trybu

### BOOT

- tylko odczyt;
- pokaż stan, blokadę i jeden następny krok;
- nie wykonuj następnego kroku.

### WORK

- najpierw pełny BOOT;
- przy blokadzie zatrzymaj się;
- bez blokady wykonaj jeden krok wynikający z lokalnego stanu i polecenia;
- zmiany semantyczne wymagają jawnej decyzji;
- repo zmieniaj przez branch, walidację, PR i merge zgodnie z poleceniem.

### AUDIT

- tylko odczyt;
- wskaż sprzeczności, braki źródeł, fałszywe deklaracje i niejednoznaczne ścieżki;
- nie aktualizuj stanu podczas tego samego audytu.

### PORTFOLIO

- użyj wyłącznie `CREATIVE_OS.md`;
- pokaż status, miejsce zatrzymania, brak, jeden następny krok i źródło prawdy;
- nie otwieraj lokalnych repo bez wskazania projektu.

## 6. Wymagany raport startowy

```text
START SESSION
PROJEKT:
TRYB:
STATUS:
ŹRÓDŁO STANU:
GDZIE STANĘLIŚMY:
BRAK / BLOKADA:
JEDEN NASTĘPNY KROK:
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
TRYB: WORK
ZADANIE: wykonaj aktualny zatwierdzony następny krok, ale zatrzymaj się na każdej aktywnej blokadzie.
```

### Portfel

```text
Uruchom Creative OS z repozytorium JTJ07/COS.
Wykonaj START_HERE.md.

PROJEKT: ALL
TRYB: PORTFOLIO
```
