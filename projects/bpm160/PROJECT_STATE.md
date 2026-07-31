---
project: "BPM:160"
portfolio_status: "QUEUED #2"
local_work_state: "SPIKE 001 IN PROGRESS"
status: "SOURCE SUMMARY CONFIRMED / ORIGINAL SOURCE FILES REQUIRED"
state_owner: "projects/bpm160/PROJECT_STATE.md"
source_summary: "projects/bpm160/SOURCE_SUMMARY_2026-07-31.md"
updated_at: "2026-07-31"
---

# PROJECT_STATE — BPM:160

## 1. Korekta rekonstrukcji

Poprzedni stan potraktował fragment dotyczący perfekcjonizmu świata i przyszłego testu widza jako opis całego projektu. Była to nadmierna generalizacja.

Aktualny stan wysokiego poziomu został skorygowany na podstawie jawnego zestawienia użytkownika zapisanego w `SOURCE_SUMMARY_2026-07-31.md`.

Zestawienie jest źródłem bieżącej korekty, ale nie zastępuje pierwotnych plików projektu. Canon v1.2, LIVE TODO, handover, Decision Log, parking i Evidence Package Spike 001 nadal powinny zostać odnalezione oraz zaimportowane.

## 2. Tożsamość projektu

BPM:160 jest projektem produkcji kreatywnej obejmującym krótkie filmy kinowe i reklamy oparte na:

- ekstremalnych środowiskach;
- rytmicznym montażu;
- narastającym sygnale;
- szczytowym zdarzeniu adrenaliny;
- wyraźnym aftermath.

Brand Promise oznacza adrenalinę i rytm. Nazwa nie definiuje dosłownego celu medycznego 160 BPM.

Projekt wykorzystuje AI do world generation w metodologii „dokumentacja najpierw”.

## 3. Canon v1.2

Potwierdzono istnienie formalnego dokumentu `Canon / Konstytucja BPM160 v1.2`, obejmującego co najmniej:

- Brand Promise;
- Series Rule — brak ludzi w Canon;
- Camera Rule;
- Audio Rule;
- World Bank Rule;
- Peak Event Rule;
- QA Rule;
- Minimal Montage Rule;
- Layer Separation Rule;
- Definition of Done.

Minimal Montage Rule — P0:

```text
World = najwolniejsze cięcia
→ Signal = skracanie
→ Peak Event = najszybsze
→ Aftermath = twarda cisza
```

## 4. Aktualny rezultat — Spike 001

Bieżącą jednostką pracy jest `Spike 001`.

Zakres:

1. `World`;
2. `Signal`;
3. `Peak Event`;
4. `Aftermath`;
5. sceneria lodowcowego kanionu;
6. montaż próbny z audio;
7. Evidence Package.

Pytanie bramkowe:

> Czy BPM160 da się zrealizować przy akceptowalnej jakości, czasie i koszcie?

Dopóki Spike 001 nie odpowie na to pytanie, nie otwieramy nowych analiz ani rozszerzeń.

## 5. Status portfelowy i lokalny

- status w portfelu Creative OS: `QUEUED #2`;
- potwierdzony lokalny stan pracy: `SPIKE 001 IN PROGRESS`;
- aktywacja projektu jako bieżącego projektu wykonawczego COS nie została w tej korekcie zmieniona;
- korekta usuwa błędny opis `PAUSED → VIEWER TEST`, ale nie zmienia samodzielnie kolejności portfela.

## 6. Przygotowane zasoby

Potwierdzone w zestawieniu użytkownika:

- prompt ujęcia `World` dla Higgsfield Cinema Studio;
- `bpm160-heartbeat-guide.wav`;
- konektor MCP narzędzi world-generation oczekujący na potwierdzenie w UI.

## 7. Model ról

Solo-proces wykorzystuje role:

- Producent;
- Walidator;
- Turbo;
- QA.

## 8. Zarządzanie stanem

Potwierdzona architektura lokalna:

- zamrożone dokumenty jako baza wiedzy;
- jeden żywy LIVE TODO;
- handover między sesjami;
- log decyzji z uzasadnieniami i odwróconymi decyzjami;
- parking z powodami i triggerami;
- limit WIP;
- wersjonowanie i supersedowanie;
- użytkownik wyznacza kierunek, AI porządkuje i wykonuje działania operacyjne;
- sesja zaczyna się od odczytu stanu i kończy aktualizacją;
- rozdzielenie deep storage / handoff / pamięć podręczna AI.

## 9. Trzy lokalne systemy klasyfikacji

Nie wolno łączyć ich w jeden protokół.

### Klasyfikacja materiałów

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

## 10. Navigation Protocol

`CORE / DETOUR / PARKING / DRIFT` pozostaje aktywnym protokołem globalnego Creative OS.

Nie ma obecnie źródła potwierdzającego, że był on historycznym wewnętrznym protokołem BPM:160. Nie należy zastępować nim trzech lokalnych systemów z sekcji 9 ani przypisywać go BPM jako faktu.

Status lokalny: `UNCONFIRMED / SOURCE REQUIRED`.

## 11. Elementy na PARKING

Do czasu zamknięcia bramki Spike 001 pozostają zaparkowane:

- Market Scan v0;
- testy widzów;
- pomiar fizjologiczny;
- rozszerzenie Canon;
- dodatkowe światy.

Warunek rozważenia powrotu:

```text
Spike 001 zakończony
→ Evidence Package kompletny
→ odpowiedź na jakość / czas / koszt
→ jawna decyzja użytkownika o następnym kierunku
```

## 12. Status źródeł

### Dostępne

- `SOURCE_SUMMARY_2026-07-31.md` — jawna korekta wysokiego poziomu użytkownika;
- obecne pliki `projects/bpm160/` — stan przejściowy i mapa odzyskiwania;
- karta portfelowa w `CREATIVE_OS.md`.

### Nadal wymagane

- Canon v1.2;
- bieżący LIVE TODO, prawdopodobnie `23_LIVE_TODO.md`;
- najnowszy handover;
- Decision Log;
- parking;
- aktualne materiały Spike 001;
- Evidence Package;
- prompt `World`;
- plik audio-guide;
- dokładna dokumentacja wspólnej warstwy BPM:160 + Creative OS.

## 13. Rzeczywista blokada wznowienia

`ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME`

Koncepcja, Canon i bieżąca bramka są już znane na poziomie zbiorczym. Brakuje jednak plików pierwotnych potrzebnych do bezpiecznego podjęcia pracy dokładnie w miejscu, w którym zatrzymał się Spike 001.

## 14. Jeden następny krok

Odnaleźć lub przekazać pakiet źródłowy BPM:160, a następnie wykonać `READ_ONLY RECONCILIATION`:

1. porównać Canon v1.2 z zestawieniem;
2. odczytać bieżący LIVE TODO i handover;
3. ustalić dokładny stan czterech ujęć, audio i Evidence Package;
4. zidentyfikować ostatnią zakończoną czynność i pierwszy brak;
5. zaktualizować ten plik minimalną deltą;
6. wznowić wyłącznie Spike 001.

## 15. Zakaz dryfu

Do czasu zamknięcia Spike 001 nie należy:

- rozpoczynać testów widzów;
- wykonywać Market Scan v0;
- otwierać pomiaru fizjologicznego;
- rozszerzać Canon;
- dodawać światów poza zakresem Spike;
- budować nowego systemu zarządzania stanem;
- przypisywać Navigation Protocol do BPM bez źródła;
- zastępować brakujących plików pamięcią AI.
