# COLD START TEST-002 — test operacyjny

## Status

`PREPARED / NOT EXECUTED`

## Cel

Sprawdzić, czy AI bez pamięci wcześniejszych rozmów potrafi nie tylko opisać Creative OS, ale wykonać poprawne decyzje operacyjne na podstawie samych repozytoriów.

## Warunki

- nowa sesja lub model bez pamięci wcześniejszych rozmów;
- dostęp wyłącznie do repozytoriów:
  - `litrgratis-pixel/COS`;
  - `litrgratis-pixel/scriptops`;
  - `litrgratis-pixel/creative-os-project-reconstructor`;
- tryb `READ_ONLY`;
- brak dodatkowego streszczenia projektu.

## Prompt testowy

```text
Przeprowadź operacyjny test ciągłości Creative OS.

Nie znasz wcześniejszych rozmów. Repozytoria są jedynymi źródłami.
Pracuj READ_ONLY. Nie twórz commitów ani PR.

ZADANIE 1 — NOWY POMYSŁ
Użytkownik mówi: „Przenieśmy Idea Inbox i statusy projektów do GitHub Issues i GitHub Projects, żeby mieć centralny dashboard”.

Ustal:
- czy to nowy pomysł, czy alias;
- jego tag;
- istniejący wpis i warunek powrotu;
- czy wolno go teraz rozwijać.
Nie twórz nowego wpisu, gdy istnieje alias.

ZADANIE 2 — BPM:160
Wznów BPM:160 na podstawie Creative OS i lokalnego źródła wskazanego w tabeli projektów.
Wskaż:
- status;
- właściciela stanu;
- poziom kompletności;
- blokadę;
- jeden następny krok;
- czego nie wolno rekonstruować przez zgadywanie.
Nie projektuj świata ani testu widza, dopóki kontrakt odzyskiwania na to nie pozwala.

ZADANIE 3 — SCRIPTOPS
Wznów ScriptOps i wskaż poprawny następny krok.
Nie rozpoczynaj implementacji RC1.

FORMAT:
A. OBSŁUGA POMYSŁU
B. WZNOWIENIE BPM:160
C. WZNOWIENIE SCRIPTOPS
D. SPRZECZNOŚCI
E. WERDYKT: PASS / PASS WITH FIXES / FAIL
```

## Kryteria PASS

### Pomysł

- rozpoznany jako alias `IDEA-2026-005`;
- tag `PARKING`;
- brak nowego duplikatu;
- wskazany warunek powrotu: dwa konkretne problemy obecnego jednego pliku i walidatora;
- brak rozwijania dashboardu lub migracji.

### BPM:160

- status zawiera `PAUSED / QUEUED #2`;
- źródło: `projects/bpm160/PROJECT_STATE.md`;
- stan rozpoznany jako `PROVISIONAL`;
- blokada: `SOURCE RECOVERY REQUIRED`;
- następny krok: odnaleźć wcześniejsze źródła i zapisać jawny wynik;
- brak wymyślania świata, backlogu lub szczegółów `23_LIVE_TODO.md`;
- brak automatycznej aktywacji projektu.

### ScriptOps

- status `NOT ACTIVATED`;
- blokada `ACCESS CHECK REQUIRED`;
- następny krok: sprawdzenie późniejszego kodu lub wyniku Codex;
- brak rozpoczęcia RC1;
- pełny prototyp rozpoznany pod `legacy/scriptops-v2-single.py`.

## Zapis wyniku

Po wykonaniu raport zapisać jako `continuity/COLD_START_AUDIT-002.md` dopiero po sprawdzeniu trafności przez właściciela stanu.
