# SOURCE_MANIFEST — BPM:160

## Dostępne źródła w repo

- `PROJECT_STATE.md` — właściciel aktualnego stanu wysokiego poziomu;
- `HANDOFF.md` — punkt wznowienia;
- `SOURCE_SUMMARY_2026-07-31.md` — jawne sprostowanie użytkownika;
- `DECISION_LOG.md` — potwierdzone decyzje semantyczne;
- `IDEA_ARCHIVE.md` — elementy pozostające poza Spike 001;
- `CREATIVE_OS.md` — karta portfelowa;
- historia Git repozytorium `litrgratis-pixel/COS`.

## Źródła pierwotne wskazane, ale jeszcze niezaimportowane

- Canon / Konstytucja BPM160 v1.2;
- bieżący LIVE TODO, prawdopodobnie `23_LIVE_TODO.md`;
- najnowszy zatwierdzony handover;
- Decision Log z odwróconymi decyzjami;
- parking z triggerami;
- materiały czterech ujęć Spike 001;
- Evidence Package;
- prompt `World` dla Higgsfield Cinema Studio;
- `bpm160-heartbeat-guide.wav`;
- konfiguracja albo potwierdzenie konektora MCP;
- dokumentacja wspólnej warstwy BPM:160 + Creative OS.

## Status źródeł

```text
HIGH-LEVEL USER SUMMARY: AVAILABLE
ORIGINAL PROJECT FILES: REQUIRED
SAFE EXECUTION RESUME: BLOCKED UNTIL RECONCILIATION
```

## Granica kompletności

Dostępne pliki pozwalają poprawnie:

- rozpoznać koncepcję i Brand Promise;
- ustalić główne reguły Canon v1.2;
- wskazać Spike 001 jako bieżącą bramkę;
- zachować zakres czterech ujęć;
- nie otwierać elementów z parkingu;
- rozdzielić trzy lokalne systemy klasyfikacji;
- nie przypisywać Navigation Protocol do BPM bez źródła.

Nie pozwalają jeszcze bezpiecznie ustalić:

- które ujęcia zostały faktycznie wygenerowane;
- jakie iteracje montażu i audio zakończono;
- aktualnych wyników QA;
- kosztu i czasu już zużytego przez Spike;
- zawartości Evidence Package;
- pierwszej dokładnie brakującej czynności;
- aktualności każdej wcześniejszej decyzji.

## Reguła importu

Odnalezione źródła należy najpierw przeanalizować `READ_ONLY` i sklasyfikować jako:

```text
CURRENT
PARTIALLY CURRENT
SUPERSEDED
EVIDENCE ONLY
UNKNOWN
```

Następnie należy przygotować minimalną deltę do `PROJECT_STATE.md`. Nie kopiować całego pakietu automatycznie i nie uznawać starszego dokumentu za aktualny wyłącznie dlatego, że istnieje.

## Wspólna warstwa BPM:160 + Creative OS

Istnienie wersjonowanego systemu Markdown obsługującego oba projekty jest częściowo potwierdzone. Nazwa, lokalizacja, struktura i aktualne użycie pozostają nieznane. Do czasu odnalezienia źródła nie należy utożsamiać tej warstwy z obecnym `CREATIVE_OS.md`.
