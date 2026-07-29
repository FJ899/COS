---
project: "BPM:160"
portfolio_status: "PAUSED / QUEUED #2"
activation: "PAUSED"
state_owner: "projects/bpm160/PROJECT_STATE.md"
blocker: "SOURCE RECOVERY REQUIRED"
next_step: "locate_previous_local_sources"
resume_contract: "READ_ONLY / RECOVERY FIRST"
---

# HANDOFF — BPM:160

## Stan wejściowy

- Projekt pozostaje priorytetem numer 2.
- Projekt jest wstrzymany, a nie porzucony.
- Dostępny stan jest niepełny i ma status `SOURCE OF TRUTH PROVISIONAL`.
- Szczegółów brakujących plików nie wolno odtwarzać przez zgadywanie.

Nagłówek YAML jest maszynowym skrótem tego samego handoffu. `PROJECT_STATE.md` pozostaje właścicielem dostępnego stanu.

## Gdzie stanęliśmy

Presja stworzenia idealnego świata zaczęła dominować nad testem oczekiwań widza. Kierunek powrotu został zawężony do małego, publikowalnego testu zamiast dalszego polerowania.

## Brak do wznowienia

Brakuje dostępnego wcześniejszego lokalnego systemu, przede wszystkim:

- `23_LIVE_TODO.md`;
- najnowszego zatwierdzonego handoveru;
- Control Tower;
- Decision Logu;
- WIP i parkingu;
- materiałów QA i testów.

## Jeden następny krok

Przeprowadzić `SOURCE RECOVERY` i zapisać wynik jako:

- `SOURCE RECOVERY FOUND — READ_ONLY REVIEW REQUIRED`, albo
- `SOURCE RECOVERY NOT FOUND — PROCEED TO MINIMAL VIEWER TEST DEFINITION`.

## Rozgałęzienie po wyniku

### `FOUND`

```text
READ_ONLY REVIEW
→ klasyfikacja aktualności i sprzeczności
→ aktualizacja PROJECT_STATE.md
→ dopiero potem definicja testu widza
```

### `NOT FOUND`

```text
PROCEED TO MINIMAL VIEWER TEST DEFINITION
```

Test ma wyprzedzać dalszą rozbudowę świata i zakończyć się obserwowalnym wynikiem `KEEP / SMALL PATCH / FAILURE`.

## Kryterium poprawnego wznowienia

Nowa sesja działa poprawnie, gdy AI:

1. rozpoznaje pauzę i kolejkę numer 2;
2. nie dopisuje brakującego kanonu;
3. zaczyna od odzyskania źródeł;
4. przy `FOUND` najpierw analizuje źródła i aktualizuje stan;
5. przy `NOT FOUND` proponuje jeden minimalny test, nie pełną rozbudowę projektu.
