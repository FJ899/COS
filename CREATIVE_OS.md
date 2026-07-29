---
system: creative-os-lean
version: 1.0
status: ACTIVE_LEAN_PILOT
updated_at: 2026-07-29
history: git
---

# Creative OS

Osobista pamięć projektów, pomysłów i wznowienia pracy. Szczegóły rozwiniętych projektów pozostają w ich lokalnych systemach. Pojedynczym entrypointem uruchomienia jest `START_HERE.md`.

## 1. Zasady

### Stan i decyzje

1. Rozmowa prowadzi proces; repozytorium zachowuje stan.
2. Najnowsza jawna decyzja użytkownika wygrywa nad starszym dokumentem, handoffem i pamięcią AI.
3. Każda informacja ma jednego właściciela. Creative OS nie kopiuje lokalnych backlogów ani kanonów.
4. Analiza zaczyna się jako `READ_ONLY`. Zmiana kierunku wymaga decyzji użytkownika; techniczne odzwierciedlenie już zatwierdzonej decyzji może wykonać AI.
5. Rekomendacja AI nie jest decyzją. Pomysł i rekomendacja pozostają hipotezą roboczą do czasu mocniejszego dowodu.
6. Brak dowodu oznacza niepewność. Nowa nazwa, atrakcyjna narracja ani zgodność modeli nie są dowodem.
7. Przed budową sprawdź projekty, Idea Inbox i gotowe rozwiązania.
8. Reguły zmieniaj na checkpointach, nie po każdym odkryciu, poza bezpieczeństwem i utratą danych.
9. Handoff jest nadpisywany; Git zachowuje historię. Pełny audyt jest wyjątkiem.
10. AI nie uznaje działania za zakończone wyłącznie na podstawie własnej deklaracji. `OK` wymaga obserwowalnego dowodu; wynik częściowy pozostaje `PARTIAL`, a błędy i elementy niewykonane pozostają jawne do naprawy albo świadomego zamknięcia.
11. Przed dodaniem nowej funkcji lub warstwy AI wskazuje: konkretny problem albo porażkę; dlaczego Git, GitHub, istniejący plik, walidator lub obecny proces nie wystarcza; obserwowalny test zaliczenia; nowy koszt utrzymania. Zwykła korekta techniczna bez zmiany zachowania lub stanu nie wymaga osobnej ceremonii.
12. `START_HERE.md` jest mapą uruchomienia, nie właścicielem stanu. Prowadzi do `CREATIVE_OS.md` i lokalnych źródeł, ale ich nie zastępuje.

Minimalny werdykt dla nowej informacji: `ZMIENIA PLAN` / `NIE ZMIENIA PLANU` / `TRZEBA SPRAWDZIĆ`.

Minimalny status pracy wykonawczej: `STARTED` / `OK` / `PARTIAL` / `BLOCKED` / `FAILED`. Szczegółowe logi, retry, checkpointy i auto-heal należą do lokalnego systemu wykonawczego projektu.

### Navigation Protocol

Każdy nowy pomysł otrzymuje tag:

- `CORE` — potrzebny teraz do aktualnego rezultatu;
- `DETOUR` — wartościowy i powiązany, ale nie teraz;
- `PARKING` — na inny czas, etap lub projekt; wymaga warunku powrotu;
- `DRIFT` — nie służy jawnemu rezultatowi albo wynika głównie z atrakcyjności nowości.

Pytania: jaki rezultat przybliża; czy jest potrzebny teraz; czy to alias; jaki dowód uzasadnia aktywację. `DRIFT` nie oznacza złego pomysłu — oznacza zakaz rozwijania go bez decyzji o zmianie kierunku.

### Autonomia AI

AI samodzielnie przechwytuje pomysły, wykrywa aliasy i sprzeczności, proponuje tag, porządkuje dokumenty, aktualizuje handoff i derived state, prowadzi research, przygotowuje odwracalne testy oraz patche/PR.

AI pyta użytkownika, gdy nowy kierunek zastępuje aktualny rezultat; kilka opcji ma podobną wartość; zmienia się cel, priorytet lub status końcowy; projekt ma być scalony, odrzucony lub zamknięty; działanie jest kosztowne, publiczne, ryzykowne albo trudno odwracalne; źródła są sprzeczne bez późniejszej jawnej decyzji.

---

## 2. Projekty

| Projekt | Status | Gdzie stanąłem | Brak do wznowienia / zakończenia | Jeden następny krok | Źródło prawdy |
|---|---|---|---|---|---|
| Narzędzie pisarskie / ScriptOps | `QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED` | Zrekonstruowano rozwój od działającego workflow Liścionka przez Mądry Warsztat / S2 Studio do ScriptOps. Proces źródłowy dał obserwowalne rezultaty, istnieje częściowo wykonywalny prototyp v2, a zakres v5 RC1 został zamknięty w pakiecie implementacyjnym. Zatwierdzony `PROJECT_STATE.md` zapisano w repo projektu. Niezależny cold start poprawnie wznowił projekt i zatrzymał się na blokadzie. Pełny prototyp jest dostępny jako `legacy/scriptops-v2-single.py`. Brak dowodu, że v5 RC1 został zbudowany. | Ustalić, czy istnieje późniejsza implementacja lub wynik pracy Codex; jeśli nie, porównać `legacy/scriptops-v2-single.py` z `sources/RC1_SCOPE_LOCK.md`, a następnie wykonać test pełnej pętli RC1. | Sprawdzić notatki, lokalne foldery i dostępne repozytoria pod kątem późniejszej implementacji ScriptOps RC1. | repo `litrgratis-pixel/scriptops`, przede wszystkim `PROJECT_STATE.md` |
| BPM:160 | `PAUSED / QUEUED #2 / SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED` | Presja stworzenia idealnego świata zaczęła dominować nad testem oczekiwań widza. Prostym kontrdowodem były krótkie materiały o podstawowym bodźcu z ogromnym zainteresowaniem. Utworzono dostępny minimalny stan odzyskiwania, ale wcześniejszy `23_LIVE_TODO.md`, handover i Control Tower pozostają nieodnalezione. | Odnalezienie albo jawne zamknięcie odzyskiwania wcześniejszych źródeł. Przy `FOUND` najpierw review i aktualizacja stanu; przy `NOT FOUND` definicja małego publikowalnego testu widza. | Przeprowadzić `SOURCE RECOVERY` i zastosować rozgałęzienie zapisane w `projects/bpm160/PROJECT_STATE.md`. | `projects/bpm160/PROJECT_STATE.md` |
| Creative OS | `ACTIVE / LEAN PILOT` | Cold start 002 wykonał pełną obsługę aliasu, wznowił BPM:160 i ScriptOps oraz zatrzymał oba projekty na właściwych blokadach. Wynik `PASS WITH FIXES` zapisano w `continuity/COLD_START_AUDIT-002.md`. Dodano `START_HERE.md` jako pojedynczą stacyjkę z trybami i mapą entrypointów. | Niezależny test samej stacyjki przy użyciu wyłącznie minimalnego klucza oraz wynik `SOURCE RECOVERY` BPM:160. | W nowej sesji wykonać tylko `START_HERE.md` w trybie `BOOT` dla jednego projektu i sprawdzić, czy cały łańcuch uruchomi się bez dodatkowego promptu. | ten plik |
| Creative OS Project Reconstructor | `ACTIVE / V1.0 STABILIZATION` | Prompt v1.0, stan projektu, archiwum ewolucji, parking pomysłów i pięć testów regresji zostały zapisane w repo projektu. Niezależne AI poprawnie odtworzyło rolę narzędzia. | Dowód stabilności z kolejnych rzeczywistych rekonstrukcji; brak długoterminowej walidacji. | Użyć wersji v1.0 na następnym rzeczywistym projekcie i zapisać tylko konkretną porażkę, jeżeli wystąpi. | repo `litrgratis-pixel/creative-os-project-reconstructor`, przede wszystkim `PROJECT_STATE.md` |

Kilka projektów może istnieć jednocześnie, ale każdy ma najwyżej jeden aktualny rezultat. Pauza nie oznacza porzucenia.

---

## 3. Idea Inbox

Zapisujemy każdy pomysł, lecz bez automatycznego rozwijania.

```text
[DATA] POMYSŁ — CORE | DETOUR | PARKING | DRIFT
Projekt lub UNASSIGNED:
Źródło / bodziec:
Dlaczego nie teraz:
Warunek powrotu: wymagany dla PARKING
Alias:
```

### IDEA-2026-001 — pełna architektura Creative OS / COS — `PARKING`

Pięć plików, osobny kernel COS i dodatkowe warstwy. Nie teraz: brak dowodu, że jeden plik nie wystarcza; cięższa wersja odtwarza idea expansion. Powrót: dwie nazwane porażki systemu jednoplikowego, których nie naprawi mała korekta.

### IDEA-2026-002 — `workshop/YYYY-MM` — `PARKING`

Miesięczny katalog bieżących szkiców. Nie teraz: Git, branche i jeden plik mogą wystarczyć; workshop nie może stać się cmentarzyskiem. Powrót: pojawią się aktywne materiały, których nie da się sensownie utrzymać w branchu lub poza kanonem.

### IDEA-2026-003 — hybrydowa architektura API + WebAI — `PARKING`

Połączyć modele frontier dostępne przez interfejs webowy jako warstwę planowania, krytyki i pracy na dużym kontekście z kontrolowaną orkiestracją oraz tańszymi modelami wykonawczymi przez API. Źródło: wcześniejszy pomysł `hybrid API/WebView`, doświadczenie użytkownika z WebAI oraz obserwacje z eksperymentów planner–worker. Nie teraz: brak porównywalnego benchmarku WebAI kontra API, konkretnego zadania wymagającego tej architektury oraz sprawdzenia bezpieczeństwa, zgodności, odtwarzalności i kosztu obsługi. Warunek powrotu: wykonać na jednym rzeczywistym zadaniu porównanie trzech wariantów — jeden model frontier przez API; WebAI frontier jako planner plus tani worker API; frontier API jako planner plus tani worker API — mierząc jakość wyniku, koszt, czas, liczbę interwencji człowieka, utratę decyzji i możliwość wznowienia. Alias: `hybrid API/WebView`. Werdykt: warto zachować, nie budować pełnego systemu bez wyniku testu.

### IDEA-2026-004 — Evidence-Guided Maintenance Loop — `PARKING`

Projekt: Creative OS. Źródło / bodziec: wcześniejszy system dobowych logów i auto-heal oraz analiza `notebooklm-skill`. Wartość: wykrywanie fałszywego sukcesu, powtarzalnych błędów i rozwijanie systemu na podstawie dowodów operacyjnych. Nie teraz: Creative OS nie ma stałego runtime, a jednoplikowa architektura nie wykazała potrzeby osobnego mechanizmu utrzymaniowego. Warunek powrotu: uruchomienie automatycznych workflow albo dwa powtarzalne przypadki błędu, niewykonania lub utraty stanu wymagające ręcznej rekonstrukcji. Alias: `daily review`, `auto-heal`, `self-improvement loop`, `maintenance engine`. Werdykt: kontrakt uczciwego wykonania jest aktywny; scheduler, event log, bounded auto-heal i adapter NotebookLM pozostają zaparkowane.

### IDEA-2026-005 — GitHub Issues / Projects jako widoki pochodne — `PARKING`

Projekt: Creative OS. Źródło / bodziec: analizy redundancji i roadmapa Lean Integration. Wartość: wizualizacja pomysłów oraz statusów bez budowania własnego dashboardu. Nie teraz: stworzyłoby drugie miejsce stanu i konieczność synchronizacji z `CREATIVE_OS.md`; obecny jeden plik i walidator nie wykazały porażki skalowania. Warunek powrotu: dwa konkretne przypadki utraty, duplikacji lub kosztownej obsługi pomysłów albo statusów, których nie naprawi mała korekta jednego pliku. Alias: `GitHub dashboard`, `Issues Idea Inbox`, `Projects portfolio view`.

### IDEA-2026-006 — ciągły Reconstructor monitorujący rozmowy — `PARKING`

Projekt: Creative OS Project Reconstructor. Źródło / bodziec: roadmapa automatycznej aktualizacji `PROJECT_STATE.md`. Wartość: proponowanie aktualizacji stanu bez ręcznego uruchamiania rekonstrukcji. Nie teraz: wymaga stałego runtime, dostępu do rozmów, kontraktu prywatności, wykrywania checkpointów, zatwierdzania, retry i rozwiązywania konfliktów; brak powtarzalnego dowodu, że ręczny tryb zawiódł. Warunek powrotu: co najmniej dwa udokumentowane przypadki utraty lub kosztownego odtworzenia stanu mimo obecnego handoffu i walidatorów oraz gotowy kontrakt dostępu i zatwierdzania. Alias: `Continuous Reconstruction`, `background Project Reconstructor`, `conversation monitor`.

---

## 4. Aktualny Handoff

### DEC-2026-005 — pojedyncza stacyjka Creative OS

Status: `ACTIVE`. Extends: `DEC-2026-004`; nie zastępuje jednego właściciela stanu, hierarchii źródeł ani lokalnych systemów projektowych.

Wybrano:

1. Rootowy `START_HERE.md` jest jedynym standardowym entrypointem użytkownika i AI.
2. Entry point definiuje tryby `BOOT / WORK / AUDIT / PORTFOLIO` oraz jeden raport startowy.
3. Mapa entrypointów prowadzi do lokalnych README i właścicieli stanu, ale nie kopiuje ich statusów ani backlogów.
4. Aktywna blokada zatrzymuje `WORK`; specyfikacja lub plan bez dowodu nie uruchamia implementacji.
5. Cold start 002 otrzymał `PASS WITH FIXES`; wynik i tarcie zapisano w `continuity/COLD_START_AUDIT-002.md`.
6. Kontrakt BPM:160 rozróżnia `FOUND → REVIEW → STATE UPDATE` od `NOT FOUND → VIEWER TEST DEFINITION`.
7. Pliki `continuity/COLD_START_*` nie należą do zwykłego bootu i są czytane tylko podczas audytu ciągłości.

Nie wybrano: nowego runtime, centralnego dashboardu, automatycznej synchronizacji repozytoriów, kopiowania lokalnych stanów do `START_HERE.md` ani automatycznego przechodzenia przez aktywne blokady.

Powód: test operacyjny potwierdził działanie domina między repozytoriami, ale wykazał tarcie wynikające z rozproszonej ścieżki wejścia. Jedna mapa startowa usuwa to tarcie bez tworzenia drugiego źródła prawdy.

Warunek dalszej rozbudowy: niezależny test minimalnego klucza wykaże konkretny błąd, którego nie naprawi mała korekta `START_HERE.md`.

Stan: Creative OS `ACTIVE / LEAN PILOT / START_HERE ACTIVE`; cold start 001 `PASS WITH FIXES`; cold start 002 `PASS WITH FIXES / EXECUTED`; test pojedynczej stacyjki `REQUIRED`; ScriptOps `QUEUED #1 / NOT ACTIVATED / ACCESS CHECK REQUIRED`; BPM:160 `PAUSED / SOURCE OF TRUTH PROVISIONAL / SOURCE RECOVERY REQUIRED`; Creative OS Project Reconstructor `ACTIVE / V1.0 STABILIZATION / UNCHANGED`.

Następny krok: uruchomić w nowej sesji minimalny klucz z `START_HERE.md` dla jednego projektu, bez dodatkowego promptu testowego.

---

## 5. Ewolucja systemu — append-only

Git pokazuje diff; ta sekcja wyjaśnia problem, decyzję, dowód, zachowane elementy i warunek powrotu.

- **EVOLUTION-2026-001 — BPM:160:** lokalny Control Tower pozostaje właścicielem szczegółowego stanu. Zachowujemy WIP, parking z triggerem, Decision Log, handover, QA i testy empiryczne. Nie kopiujemy go globalnie. Status: `ACTIVE LOCAL SYSTEM`.
- **EVOLUTION-2026-002 — Creative OS:** powstał, bo pomysły ginęły, a wznowienie wymagało składania kontekstu z wielu źródeł. Każdy pomysł przechwytujemy, ale nie aktywujemy automatycznie. Status: `ACTIVE / LEAN PILOT`.
- **EVOLUTION-2026-003 — Cognitive OS:** eksperyment potwierdził wartość repo jako stanu, `READ_ONLY`, human approval, checkpointów, minimalnej delty i jawnej niepewności. Pełny audyt był zbyt ciężki. Status: `ARCHIVED AS EXPERIMENT / ABSORBED AS RULES / NOT DEVELOPED AS SEPARATE SYSTEM`.
- **EVOLUTION-2026-004 — Navigation Protocol:** zachowany jako tag. Zawiodło utrwalenie historycznej definicji, nie ma dowodu, że zawiódł filtr. Status: `ACTIVE RULE`.
- **EVOLUTION-2026-005 — jeden plik:** pięć plików i osobny kernel zaparkowano, bo brak dowodu, że mniejsza wersja nie wystarcza. Git zapewnia historię. Status: `ACTIVE LEAN ARCHITECTURE`.
- **EVOLUTION-2026-006 — autonomia AI:** AI wykonuje pracę operacyjną, użytkownik rozstrzyga kierunek. Korekta, gdy AI dwukrotnie zmieni semantyczny stan bez podstawy albo nadmiar pytań przerzuci pracę na użytkownika. Status: `ACTIVE RULE`.
- **EVOLUTION-2026-007 — BPM:160:** pauza wynika z perfekcjonizmu silniejszego niż test widza. Powrót ma nastąpić przez mały publikowalny test, nie dalsze bezterminowe polerowanie. Status: `PROJECT PAUSED / PRIORITY PRESERVED`.
- **EVOLUTION-2026-008 — sprzątanie repo:** pełny stary system zachowujemy na branchach archiwalnych; aktywne drzewo zredukowano do czterech plików. Nie utworzono workshopu jako cmentarzyska. Status: `COMPLETED / MERGED`; commit: `7cc2cf2b794d646527a4c5469fd7a764b4f9e190`.
- **EVOLUTION-2026-009 — truthful execution:** problemem była możliwość opisania pracy jako wykonanej bez rozróżnienia wyniku rozpoczętego, częściowego, zablokowanego i nieudanego. Wcześniej Creative OS wymagał dowodu przy zmianie planu, ale nie miał jawnego kontraktu pojedynczego wykonania. Decyzja: wchłonąć statusy `STARTED / OK / PARTIAL / BLOCKED / FAILED`, obowiązek obserwowalnego dowodu, zachowanie wyników cząstkowych oraz kontrolę operacji destrukcyjnych. Dowód: kontrakty i stany częściowe przeanalizowane w `notebooklm-skill`, historyczny mechanizm dobowych logów i auto-heal użytkownika oraz jawna decyzja wdrożeniowa. Zachowujemy lean, jeden plik, lokalną własność szczegółowych logów i pierwszeństwo błędów przed rozwojem. Parkujemy scheduler 24h, event log, retry engine, bounded auto-heal, MCP i adapter NotebookLM. Warunek powrotu: automatyczny runtime albo dwa porównywalne problemy, których nie rozwiąże mała korekta obecnych plików. Supersedes: brak; extends `EVOLUTION-2026-003` i `EVOLUTION-2026-006`. Status: `ACTIVE RULE / HEAVIER RUNTIME PARKED`.
- **EVOLUTION-2026-010 — niezależny cold start i walidator:** problemem była niezweryfikowana deklaracja, że repo wystarczy do wznowienia bez rozmowy. Wcześniej istniały instrukcje, lecz brak niezależnego wykonania. Decyzja: zachować raport cold startu, dodać deterministyczny walidator i poprawić wyłącznie wykryte rozjazdy. Dowód: obce AI bez wcześniejszej pamięci odtworzyło ekosystem, wznowiło ScriptOps i odmówiło implementacji bez dowodu; wykryło brak ścieżki BPM:160. Zachowujemy jednoplikowego właściciela stanu; skrypt i workflow są kontrolą, nie nowym kernelem. Parkujemy automatyczny runner wielu modeli i centralny dashboard. Warunek powrotu: dwie regresje niewykryte przez obecną kontrolę albo potrzeba cyklicznego runtime. Supersedes: brak; extends `EVOLUTION-2026-009`. Status: `OBSERVED WORKING RESULT / PARTIAL PORTFOLIO CONTINUITY`.
- **EVOLUTION-2026-011 — Feature Razor i źródło odzyskiwania BPM:160:** problemem były jednocześnie ryzyko duplikowania funkcji Git/GitHub oraz realny brak dostępnego źródła BPM:160. Wcześniej analizy proponowały zarówno trafne uproszczenia, jak i regresje: usuwanie semantycznych logów, równoległe statusy w Projects oraz stały monitor rozmów. Decyzja: wchłonąć czteropunktowy filtr użyteczności i szablon PR, pozostawić decyzje semantyczne poza technicznym `git log`, przetestować YAML w tym samym handoffie oraz utworzyć minimalne, jawnie niepełne źródło odzyskiwania BPM:160. Dowód: niezależny cold start wykazał tarcie odtwarzania prototypu i brak ścieżki BPM; analizy redundancji wskazały ryzyko drugich źródeł prawdy. Zachowujemy Navigation Protocol, hierarchię źródeł, Resume Protocol, Decision Logi semantyczne i walidatory. Parkujemy Issues/Projects jako derived views, centralny dashboard, automatyczną synchronizację i ciągły Reconstructor. Warunek powrotu: dwie porównywalne porażki obecnego Lean albo wynik testu operacyjnego pokazujący konkretną potrzebę. Supersedes: brak; extends `EVOLUTION-2026-007` i `EVOLUTION-2026-010`. Status: `ACTIVE SMALL PATCH / BPM SOURCE RECOVERY ENABLED`.
- **EVOLUTION-2026-012 — pojedyncza stacyjka:** problemem było działające, ale rozproszone uruchomienie wymagające długiego promptu i ręcznego przejścia do lokalnych README. Wcześniej cold start 002 potwierdził poprawne domino, lecz ocenił mechanizm jako `PASS WITH FIXES`. Decyzja: dodać `START_HERE.md` z czterema trybami, mapą entrypointów, regułami zatrzymania i jednym raportem startowym; nie kopiować do niego lokalnego stanu. Dowód: zewnętrzne AI poprawnie obsłużyło alias, BPM:160 i ScriptOps, a jako główne tarcie wskazało brak pojedynczego entrypointu. Zachowujemy jeden właściciel stanu, lokalne README, blokady i walidatory. Parkujemy runtime, dashboard oraz automatyczną orkiestrację. Warunek powrotu: test minimalnego klucza wykaże konkretną porażkę sekwencji. Supersedes: brak; extends `EVOLUTION-2026-010` i `EVOLUTION-2026-011`. Status: `START_HERE ACTIVE / EXTERNAL IGNITION TEST REQUIRED`.

Nowy wpis ewolucji musi podać: problem, wcześniejszą postać, decyzję, dowód, co zachowujemy, co parkujemy, warunek powrotu i `SUPERSEDES`, jeśli dotyczy.
