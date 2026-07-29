# COLD START AUDIT-002 — test operacyjny

## Status

`PASS WITH FIXES`

## Typ testu

`PUBLIC / NO PRIOR MEMORY / READ_ONLY / OPERATIONAL`

Badane AI nie otrzymało historii rozmowy ani klucza odpowiedzi. Repozytoria były jedynymi źródłami.

## Zakres

1. obsługa nowego pomysłu i wykrycie aliasu;
2. wznowienie BPM:160;
3. wznowienie ScriptOps;
4. ocena przejścia od Creative OS do lokalnych źródeł prawdy.

## A. Obsługa pomysłu — PASS

Pomysł przeniesienia Idea Inbox i statusów do GitHub Issues / Projects został poprawnie rozpoznany jako alias:

```text
IDEA-2026-005 — GitHub Issues / Projects jako widoki pochodne — PARKING
```

AI:

- zachowało tag `PARKING`;
- wskazało istniejące aliasy;
- przytoczyło warunek powrotu;
- nie utworzyło duplikatu;
- nie rozwinęło architektury dashboardu.

## B. Wznowienie BPM:160 — PASS WITH ONE CLARIFICATION

AI poprawnie wskazało:

- `PAUSED / QUEUED #2`;
- `SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED`;
- właściciela `projects/bpm160/PROJECT_STATE.md`;
- brak wcześniejszego Control Tower, `23_LIVE_TODO.md`, handoveru, WIP, QA i testów;
- zakaz odtwarzania świata, backlogu i kanonu przez zgadywanie;
- jeden następny krok: `SOURCE RECOVERY`.

### Wykryta niejednoznaczność

Odpowiedź sugerowała, że po każdym zamknięciu `SOURCE RECOVERY` można przejść bezpośrednio do testu widza.

Poprawny kontrakt:

```text
SOURCE RECOVERY FOUND
→ READ_ONLY REVIEW
→ klasyfikacja aktualności źródeł
→ aktualizacja PROJECT_STATE.md
→ dopiero potem definicja testu widza

SOURCE RECOVERY NOT FOUND
→ PROCEED TO MINIMAL VIEWER TEST DEFINITION
```

Nie była to niebezpieczna implementacja, ale dokumentacja wymagała doprecyzowania.

## C. Wznowienie ScriptOps — PASS

AI poprawnie wskazało:

- `QUEUED #1 / NOT ACTIVATED / ACCESS CHECK REQUIRED`;
- najmniejszą pętlę RC1;
- ostatnie obserwowalne rezultaty wcześniejszego workflow;
- prototyp v2 jako częściowy mechanizm, nie RC1;
- kanoniczny plik `legacy/scriptops-v2-single.py`;
- różnicę między v2 a zakresem v5 RC1;
- aktualną blokadę i jeden następny krok;
- funkcje wyłączone z RC1.

AI nie rozpoczęło implementacji i nie uznało Final Master Package za działający build.

## D. Mechanizm startowy — PASS WITH FRICTION

AI samodzielnie odtworzyło sekwencję:

```text
README.md
→ CREATIVE_OS.md
→ tabela projektów
→ lokalne źródło prawdy
→ PROJECT_STATE.md / HANDOFF.md
→ blokada
→ jeden następny krok
```

Potwierdzono:

- właściwą hierarchię źródeł;
- jednego właściciela informacji;
- zatrzymanie na rzeczywistych blokadach;
- wznowienie bez wcześniejszego czatu.

### Tarcie

- brakowało pojedynczego rootowego entrypointu;
- trzeba było ręcznie przechodzić przez lokalne README;
- mapa wymaganych plików była rozproszona między COS i lokalnymi repozytoriami;
- ścieżka `sources/RC1_SCOPE_LOCK.md` wymagała wejścia do lokalnej dokumentacji ScriptOps.

## E. Werdykt

```text
OBSŁUGA ALIASU: PASS
BPM:160: PASS WITH CLARIFICATION
SCRIPTOPS: PASS
PRZEJŚCIE MIĘDZY REPOZYTORIAMI: PASS
POJEDYNCZA STACYJKA: FIX REQUIRED

FINAL: PASS WITH FIXES
```

## F. Minimalne poprawki

1. utworzyć rootowy `START_HERE.md`;
2. zapisać mapę entrypointów bez kopiowania lokalnego stanu;
3. zdefiniować tryby `BOOT / WORK / AUDIT / PORTFOLIO`;
4. doprecyzować `SOURCE RECOVERY FOUND / NOT FOUND`;
5. objąć entrypoint kontrolą deterministycznego walidatora.

## G. Stan poprawek

Poprawki są realizowane w PR dodającym `START_HERE.md`. Audyt pozostaje dowodem stanu sprzed tej poprawki.
