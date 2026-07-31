---
document: "BPM:160 — dane zbiorcze"
source_kind: "USER_SUPPLIED_SOURCE_SUMMARY"
date: "2026-07-31"
status: "CURRENT HIGH-LEVEL CORRECTION / ORIGINAL FILES NOT IMPORTED"
---

# BPM:160 — dane zbiorcze z korekty użytkownika

Legenda:

- ✅ potwierdzone przez użytkownika posiadającego źródło;
- ⚠️ niepotwierdzone albo wymagające odnalezienia źródła pierwotnego.

Ten dokument koryguje wcześniejszą rekonstrukcję, która potraktowała jedną obserwację o testach widza i perfekcjonizmie jako opis całego projektu. Nie zastępuje plików pierwotnych: Canon v1.2, LIVE TODO, handoveru, Decision Logu, parkingu ani Evidence Package Spike 001.

## 1. Koncepcja i marka

- ✅ Projekt produkcji kreatywnej: krótkie filmy kinowe i reklamy oparte o ekstremalne środowiska, rytmiczny montaż i momenty szczytowej adrenaliny.
- ✅ Brand Promise oznacza adrenalinę i rytm, a nie dosłowny cel medyczny 160 BPM.
- ✅ Projekt wykorzystuje AI do generowania światów w metodologii „dokumentacja najpierw”.

## 2. Canon v1.2 — Konstytucja BPM160

- ✅ Formalny Canon koduje: Brand Promise, Series Rule, Camera Rule, Audio Rule, World Bank Rule, Peak Event Rule, QA Rule, Minimal Montage Rule, Layer Separation Rule i Definition of Done.
- ✅ Series Rule: brak ludzi w Canon.
- ✅ Minimal Montage Rule — P0:

```text
World = najwolniejsze cięcia
→ Signal = skracanie
→ Peak Event = najszybsze
→ Aftermath = twarda cisza
```

## 3. Status bieżący — Spike 001

- ✅ W toku są cztery ujęcia: `World`, `Signal`, `Peak Event`, `Aftermath` w scenerii lodowcowego kanionu.
- ✅ Zakres Spike obejmuje montaż próbny z audio i Evidence Package.
- ✅ Pytanie bramkowe:

> Czy BPM160 da się zrealizować przy akceptowalnej jakości, czasie i koszcie?

- ✅ Żadna nowa analiza ani rozszerzenie nie otwiera się, dopóki Spike 001 nie odpowie na to pytanie.
- ✅ Poza Spike 001 na `PARKING` pozostają: Market Scan v0, testy widzów, pomiar fizjologiczny, rozszerzenie Canon i dodatkowe światy.

## 4. Przygotowane zasoby

- ✅ Gotowy prompt do generowania ujęcia `World`, sformatowany pod Higgsfield Cinema Studio.
- ✅ Zsyntezowana ścieżka `bpm160-heartbeat-guide.wav`.
- ✅ Dostęp do konektora MCP narzędzi world-generation oczekuje na potwierdzenie w UI.

## 5. Model ról

- ✅ Producent.
- ✅ Walidator.
- ✅ Turbo.
- ✅ QA.

Model służy zarządzaniu solo-procesem, a nie wieloosobowej organizacji.

## 6. Architektura zarządzania stanem

- ✅ Zamrożone dokumenty jako baza wiedzy.
- ✅ Jeden żywy plik bieżącego stanu — LIVE TODO.
- ✅ Handover przekazujący kontekst między sesjami.
- ✅ Log decyzji z uzasadnieniami i odwróconymi decyzjami.
- ✅ Parking z powodami i warunkami aktywacji.
- ✅ Limit WIP.
- ✅ Hierarchia wersji i zasada supersedowania.
- ✅ Kontrakt: użytkownik wyznacza kierunek, AI porządkuje i wykonuje działania operacyjne.
- ✅ Sesja zaczyna się od odczytu stanu i kończy jego aktualizacją.
- ✅ Wyzwalacze reaktywacji zaparkowanych elementów.
- ✅ Rozdzielenie: deep storage / handoff / pamięć podręczna AI.

## 7. Rzeczywiste systemy klasyfikacji

To trzy różne osie. Nie wolno sklejać ich w jeden protokół.

### Materiały

```text
CORE / SUPPORT / EDITORIAL / REJECT
```

### Stan pracy

```text
DOING NOW / NEXT / BACKLOG / PARKED / DONE
```

### Stan decyzji i wersji

```text
active / superseded / unresolved
```

## 8. Navigation Protocol

Status: ⚠️ `UNCONFIRMED AS BPM:160 INTERNAL MECHANISM`.

Wcześniej zapisana wzmianka o `CORE / DETOUR / PARKING / DRIFT` i czterech pytaniach może być:

- protokołem globalnego Creative OS;
- skrótem późniejszej rozmowy;
- błędnym połączeniem trzech lokalnych systemów klasyfikacji.

Do czasu odnalezienia źródła nie przedstawiać Navigation Protocol jako historycznej, działającej części BPM:160. Creative OS może nadal stosować własny Navigation Protocol na poziomie portfela, lecz nie wolno przypisywać go lokalnemu BPM bez dowodu.

## 9. Wspólna warstwa BPM:160 + Creative OS

Status: ⚠️ `PARTIALLY CONFIRMED`.

Potwierdzone:

- istniał wersjonowany system Markdown;
- przechowywał logi decyzji, odrzuceń i założeń;
- działał append-only;
- obejmował cotygodniowy przegląd;
- obsługiwał oba projekty.

Nieznane:

- nazwa;
- lokalizacja;
- dokładna struktura plików;
- czy nadal jest aktywnie używany;
- relacja do obecnego repo `litrgratis-pixel/COS`.

## 10. Konsekwencja dla aktualnego stanu

Wcześniejszy opis:

```text
perfekcjonizm świata
→ następny krok: test widza
```

był fragmentem problemu lub późniejszej rekomendacji, a nie pełnym stanem BPM:160.

Aktualna sekwencja brzmi:

```text
odnalezienie i import źródeł pierwotnych
→ READ_ONLY RECONCILIATION
→ potwierdzenie bieżącego LIVE TODO
→ dokończenie Spike 001
→ odpowiedź na bramkę jakości / czasu / kosztu
→ dopiero potem decyzja, co wraca z PARKING
```
