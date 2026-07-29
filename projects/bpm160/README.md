# BPM:160 — lokalne źródło odzyskiwania

Ten katalog jest dostępnym lokalnym źródłem stanu projektu BPM:160 do czasu odnalezienia i zaimportowania wcześniejszego lokalnego systemu.

## Status

`PAUSED / QUEUED #2 / SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED`

## Kolejność startu

1. `PROJECT_STATE.md`
2. `HANDOFF.md`
3. `DECISION_LOG.md`
4. `SOURCE_MANIFEST.md`
5. `IDEA_ARCHIVE.md`

## Granica

Pliki zapisują wyłącznie informacje potwierdzone w Creative OS i historii Git. Nie odtwarzają brakujących szczegółów fabuły, świata, backlogu ani decyzji z nieudostępnionego `23_LIVE_TODO.md` i najnowszego handoveru.

`PROJECT_STATE.md` jest obecnie właścicielem dostępnego stanu BPM:160. Po odnalezieniu oryginalnych źródeł należy je porównać w trybie `READ_ONLY`, a następnie uzupełnić ten stan minimalną deltą. Nie wolno utrzymywać dwóch równoległych kanonów.

## Jeden następny krok

Odnaleźć i zaimportować wcześniejsze źródła BPM:160, zwłaszcza `23_LIVE_TODO.md` i najnowszy zatwierdzony handover. Gdy źródła nie istnieją, zapisać jawnie `SOURCE RECOVERY NOT FOUND`, a dopiero potem przygotować jeden mały, publikowalny test reakcji widza.
