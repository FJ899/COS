---
protocol: cognitive-os-v0
type: handoff_snapshot
version: 0.1
status: active
generated_at: 2026-07-23
source_commit_or_hash: 5c86b01ba2e949c0f22ae3fb7040798995a123d7
valid_until: 2026-07-30
---

# HANDOFF — pakiet startowy nowej sesji

To jest skrót do uruchomienia nowej rozmowy. Nie jest źródłem prawdy; w razie konfliktu wygrywa kanon i zatwierdzone decyzje.

## Jak pracować z użytkownikiem

- Krytycznie, konkretnie, bez zgadywania.
- Przed budową sprawdź istniejące rozwiązania.
- Oznaczaj `FACT`, `HYPOTHESIS`, `PREFERENCE`, `RECOMMENDATION`, `DECISION` i `PROPOSAL`.
- Rozmowę traktuj jako materiał, repozytorium jako stan.
- Analizę rozpoczynaj `READ_ONLY`.
- Nie zmieniaj stanu bez zgody użytkownika.
- Kończ sesję jednym następnym krokiem albo `NO_STATE_CHANGE`.

## Bootstrap wymagany przed pracą

1. przeczytaj `README.md` i `PILOT/README.md`;
2. przeczytaj pliki źródłowe wskazane niżej;
3. przeczytaj ostatni raport `COS/SESJE/2026-07-23-002.md`;
4. wykonaj `BOOT_ACK` z `PILOT/README.md`;
5. podaj commit bazowy i niepewności.

## Aktualny cel

Przeprowadzić dziesięć rzeczywistych sesji, w tym serię zróżnicowanych audytów rozmów, i na danych skonfigurować najmniejszą końcową wersję COS, która poprawia ciągłość pracy bez nadmiernego kosztu.

## Obowiązujące decyzje

- `DEC-2026-000` — pilot Cognitive OS v0 jest aktywny.
- `DEC-2026-001` — analizujemy kilka rozmów dwuetapowo i finalizujemy COS dopiero na podstawie checkpointów oraz metryk.

## Aktualny postęp

- zakończono 2 audyty rozmów z wymaganych minimum 3 przed pierwszym checkpointem;
- `AUD-2026-001`: długi, sekwencyjny scope creep i overclaimy techniczne;
- `AUD-2026-002`: krótsza rozmowa, szybka formalizacja rozbudowanego systemu normatywnego;
- nie zmierzono jeszcze czasu bootstrapu, analizy ani protokołu;
- nie zmieniono protokołu po drugim audycie.

## Najważniejsza lekcja z dwóch audytów

Prompt 1 i Prompt 2 pełnią różne funkcje:

```text
Prompt 1 → ślepy inwentarz rozmowy
Prompt 2 → audyt rozmowy względem aktualnego repozytorium
```

Pierwszy etap ogranicza dopasowanie materiału do istniejącej teorii. Drugi etap wskazuje konflikty, duplikaty i minimalną deltę względem obowiązującego stanu.

Wspólny wzorzec dwóch rozmów:

```text
potrzeba uporządkowania pracy z AI
→ szeroka architektura i terminologia
→ system przedstawiany jako uniwersalny
→ brak pomiaru kosztu i prostszej alternatywy
```

Nadmierna architektura może narastać przez wiele rund albo pojawić się od razu jako elegancki, pozornie kompletny system.

## Czego nie otwierać ponownie bez nowych danych

- budowa pełnego produktu COS — warunek: zakończony pilot i decyzja końcowa;
- wieloagentowa orkiestracja, routing i debate jako funkcja — warunek: benchmark po pilocie;
- pełny AI Collaboration Operating System i jedenastofazowy workflow — warunek: dowód przewagi nad minimalnym COS i pomiar kosztu;
- self-heal, daily AI review i automatyczne zmiany — warunek: stabilny rdzeń, testy, rollback i human approval;
- ogłoszenie v1 — warunek: kryteria `PILOT/FINALIZACJA_V1.md`;
- zapis surowych rozmów do publicznego repo — warunek: redakcja, klasyfikacja danych i jawna zgoda.

Przed reopenem sprawdź `WNIOSKI_I_POMYSLY/MAPA_ALIASOW.md`. Nowa nazwa nie jest nowym dowodem.

## Aktywny obiekt

- ID: `WORK-2026-07-21-001`.
- Rezultat: dowód po 10 sesjach i konfiguracja najmniejszej użytecznej wersji końcowej.
- Aktualny stan: 2 audyty rozmów zakończone; pierwszy checkpoint po trzecim.
- Definition of Done: `COS/03_AKTYWNY.md`.

## Ostatni rezultat i dowód

- raport sesji: `COS/SESJE/2026-07-23-002.md`;
- audyt: `PILOT/AUDYTY/AUD-2026-002_AI_COLLABORATION_OS.md`;
- rejestr: `PILOT/REJESTR_ROZMOW.md`;
- metryki: `PILOT/METRYKI.md`.

## Kandydat oczekujący na checkpoint

Nie jest jeszcze regułą:

- lekka karta wejściowa dla złożonych tematów:
  `RESULT / LEVEL / READINESS_STATE / TARGET_ARTIFACT / GATE`.

## Jeden następny krok

Wybrać trzeci przypadek o maksymalnym kontraście:

- inna domena niż projektowanie systemów AI;
- rozmowa przebiegająca dobrze albo bez dużego dryfu;
- jasno określony rezultat;
- zmierzone `bootstrap_minutes`, `analysis_minutes` i `protocol_minutes`.

## Pliki źródłowe

- `00_KONTRAKT_PRACY_Z_AI.md`
- `01_KOMPAS.md`
- `02_KANON.md`
- `03_AKTYWNY.md`
- `DECYZJE.md`
- `PARKING.md`
- `DOWODY.md`
- `INCYDENTY.md`
- `99_HANDOFF.md`
- `SESJE/2026-07-23-002.md`
- `../PILOT/README.md`
- `../PILOT/REJESTR_ROZMOW.md`
- `../PILOT/METRYKI.md`
- `../PILOT/AUDYTY/AUD-2026-002_AI_COLLABORATION_OS.md`
- `../PILOT/FINALIZACJA_V1.md`
- `../WNIOSKI_I_POMYSLY/README.md`
- `../WNIOSKI_I_POMYSLY/MAPA_ALIASOW.md`

## BOOT_ACK wymagany od modelu

```text
BOOT_ACK
repozytorium:
gałąź:
commit bazowy:
aktywne decyzje:
aktywny rezultat:
tryb:
jeden następny krok:
niepewności:
```
