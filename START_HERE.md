---
system: "Creative OS"
role: "single-entrypoint"
version: "1.0"
status: "ACTIVE"
state_owner: "CREATIVE_OS.md"
---

# START_HERE — Creative OS

Ten plik jest pojedynczą stacyjką Creative OS. Uruchamia odczyt właściwego stanu i prowadzi do lokalnego źródła prawdy wybranego projektu.

`START_HERE.md` nie jest właścicielem stanu projektu. Jest wyłącznie mapą uruchomienia. Stan przekrojowy należy do `CREATIVE_OS.md`, a szczegóły do lokalnych źródeł wskazanych niżej.

## 1. Kontrakt wejścia

Użytkownik może podać:

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

Znaczenie trybów:

- `BOOT` — odtwórz stan, pokaż blokadę i jeden następny krok; niczego nie zmieniaj;
- `WORK` — odtwórz stan i wykonaj jeden jawnie zlecony, odwracalny krok, o ile nie istnieje blokada;
- `AUDIT` — odtwórz i oceń spójność; nie twórz zmian;
- `PORTFOLIO` — pokaż stan wszystkich projektów wyłącznie na poziomie Creative OS.

## 2. Sekwencja zapłonu

Wykonaj kolejno:

1. Przeczytaj `README.md`.
2. Przeczytaj cały `CREATIVE_OS.md`.
3. Ustal `PROJEKT`, `TRYB` i oczekiwany rezultat sesji.
4. Przy `PORTFOLIO` użyj tabeli projektów w `CREATIVE_OS.md` i nie otwieraj wszystkich lokalnych repozytoriów.
5. Dla pojedynczego projektu otwórz jego entrypoint z mapy poniżej.
6. W lokalnym systemie wykonaj kolejność startową podaną w lokalnym `README.md`.
7. Odczytaj co najmniej lokalny `PROJECT_STATE.md` i `HANDOFF.md`, gdy istnieją.
8. Porównaj lokalny stan z kartą projektu w `CREATIVE_OS.md`.
9. Zastosuj hierarchię źródeł z `README.md`; nie rozwiązuj konfliktu przez zgadywanie.
10. Zwróć raport startowy. Dopiero potem zastosuj zachowanie właściwe dla trybu.

Nie czytaj automatycznie branchy archiwalnych, pełnej dokumentacji innych projektów ani plików `continuity/COLD_START_*`, chyba że celem sesji jest audyt ciągłości.

## 3. Mapa entrypointów

### Creative OS

```text
repo: litrgratis-pixel/COS
entrypoint: START_HERE.md
state_owner: CREATIVE_OS.md
```

### Narzędzie pisarskie / ScriptOps

Alias: `ScriptOps`

```text
repo: litrgratis-pixel/scriptops
entrypoint: README.md
state_owner: PROJECT_STATE.md
handoff: HANDOFF.md
critical_scope: sources/RC1_SCOPE_LOCK.md
```

Po wejściu do repo wykonaj lokalną kolejność z `README.md`. Aktywna blokada `ACCESS CHECK REQUIRED` zatrzymuje implementację RC1.

### BPM:160

```text
repo: litrgratis-pixel/COS
root: projects/bpm160
entrypoint: projects/bpm160/README.md
state_owner: projects/bpm160/PROJECT_STATE.md
handoff: projects/bpm160/HANDOFF.md
```

Aktywna blokada `SOURCE RECOVERY REQUIRED` zatrzymuje rekonstrukcję świata, backlogu i produkcję.

Przy wyniku odzyskiwania:

```text
SOURCE RECOVERY FOUND
→ READ_ONLY REVIEW
→ klasyfikacja aktualności źródeł
→ aktualizacja PROJECT_STATE.md
→ dopiero potem definicja testu widza

SOURCE RECOVERY NOT FOUND
→ PROCEED TO MINIMAL VIEWER TEST DEFINITION
```

### Creative OS Project Reconstructor

Alias: `Project Reconstructor`

```text
repo: litrgratis-pixel/creative-os-project-reconstructor
entrypoint: README.md
state_owner: PROJECT_STATE.md
canonical_prompt: PROMPT_STARTOWY.md
```

Po wejściu do repo wykonaj lokalną kolejność z `README.md`. Zamrożony prompt może zostać zmieniony wyłącznie po konkretnej porażce i z testem regresji.

## 4. Reguły zatrzymania

Zatrzymaj pracę i nie przechodź do implementacji, gdy:

- lokalny stan zawiera aktywną blokadę;
- repozytorium albo wymagany plik jest niedostępny;
- źródła są sprzeczne i hierarchia nie rozstrzyga konfliktu;
- `WORK` wymaga zmiany celu, priorytetu, kanonu albo statusu projektu bez jawnej decyzji użytkownika;
- dostępne są wyłącznie spekulacje, plan lub specyfikacja bez dowodu wykonania.

Brak dostępu raportuj jako `ACCESS BLOCKED`. Brak źródła raportuj jako `SOURCE REQUIRED`. Nie uzupełniaj danych z pamięci AI.

## 5. Zachowanie według trybu

### BOOT

- tylko odczyt;
- pokaż stan, blokadę i jeden następny krok;
- nie wykonuj następnego kroku.

### WORK

- najpierw wykonaj pełny `BOOT`;
- przy aktywnej blokadzie zatrzymaj się;
- bez blokady wykonaj wyłącznie jeden krok wynikający z lokalnego stanu i polecenia użytkownika;
- zmiany semantyczne wymagają jawnej decyzji użytkownika;
- operacje w repo wykonuj przez branch, walidację, PR i merge zgodnie z poleceniem użytkownika.

### AUDIT

- tylko odczyt;
- wskaż sprzeczności, brakujące źródła, fałszywe deklaracje rezultatu i niejednoznaczne ścieżki;
- nie aktualizuj stanu podczas tego samego audytu.

### PORTFOLIO

- użyj wyłącznie `CREATIVE_OS.md`;
- dla każdego projektu pokaż status, miejsce zatrzymania, brak, jeden następny krok i źródło prawdy;
- nie otwieraj lokalnych źródeł bez wskazania konkretnego projektu.

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

`READY FOR ONE STEP` nie oznacza automatycznej zgody na zmianę kierunku. `EXECUTED` wymaga obserwowalnego dowodu.

## 7. Minimalny klucz użytkownika

```text
Uruchom Creative OS z repozytorium litrgratis-pixel/COS.
Wykonaj START_HERE.md.

PROJEKT: BPM:160
TRYB: BOOT
```

Przykład pracy:

```text
Uruchom Creative OS z repozytorium litrgratis-pixel/COS.
Wykonaj START_HERE.md.

PROJEKT: ScriptOps
TRYB: WORK
ZADANIE: wykonaj aktualny zatwierdzony następny krok, ale zatrzymaj się na każdej aktywnej blokadzie.
```

Przykład portfela:

```text
Uruchom Creative OS z repozytorium litrgratis-pixel/COS.
Wykonaj START_HERE.md.

PROJEKT: ALL
TRYB: PORTFOLIO
```
