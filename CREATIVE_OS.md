---
system: creative-os-lean
version: 1.0
status: ACTIVE_LEAN_PILOT
updated_at: 2026-07-29
history: git
---

# Creative OS

Osobista pamięć projektów, pomysłów i wznowienia pracy. Szczegóły rozwiniętych projektów pozostają w ich lokalnych systemach.

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
| Narzędzie pisarskie / ScriptOps | `QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED` | Zrekonstruowano rozwój od działającego workflow Liścionka przez Mądry Warsztat / S2 Studio do ScriptOps. Proces źródłowy dał obserwowalne rezultaty, istnieje częściowo wykonywalny prototyp v2, a zakres v5 RC1 został zamknięty w pakiecie implementacyjnym. Zatwierdzony `PROJECT_STATE.md` zapisano w prywatnym repo. Brak dowodu, że v5 RC1 został zbudowany. | Ustalić, czy istnieje późniejsza implementacja lub wynik pracy Codex; jeśli nie, porównać `scriptops-v2-single.py` z `RC1_SCOPE_LOCK.md`, a następnie wykonać test pełnej pętli RC1. | Sprawdzić notatki, lokalne foldery i dostępne repozytoria pod kątem późniejszej implementacji ScriptOps RC1. | prywatne repo `litrgratis-pixel/scriptops`, przede wszystkim `PROJECT_STATE.md` |
| BPM:160 | `PAUSED / QUEUED #2`, priorytet zachowany | Presja stworzenia idealnego świata zaczęła dominować nad testem oczekiwań widza. Prostym kontrdowodem były krótkie materiały o podstawowym bodźcu z ogromnym zainteresowaniem. | Mały, publikowalny test widza bez wcześniejszego zbudowania idealnego świata. | Zdefiniować jeden minimalny test reakcji widza i porównać go z aktualnym planem. | lokalny system BPM:160, zwłaszcza `23_LIVE_TODO.md` i najnowszy zatwierdzony handover |
| Creative OS | `ACTIVE / LEAN PILOT` | Wchłonięto kontrakt uczciwego wykonania: `STARTED / OK / PARTIAL / BLOCKED / FAILED`, obowiązek obserwowalnego dowodu oraz zakaz nazywania wyniku częściowego pełnym sukcesem. Zachowano jeden plik i rozdział odpowiedzialności między Creative OS a lokalne systemy wykonawcze. | Dowód z rzeczywistych zadań, że kontrakt poprawia prawdziwość raportowania i wznowienie bez tworzenia zbędnego narzutu. | Zastosować kontrakt w następnym rzeczywistym zadaniu wykonawczym i ocenić cykl jako `KEEP / SMALL PATCH / FAILURE`. | ten plik |
| Creative OS Project Reconstructor | `ACTIVE / V1.0 STABILIZATION` | Prompt v1.0, stan projektu, archiwum ewolucji, parking pomysłów i pięć testów regresji zostały zapisane w prywatnym repo. | Dowód stabilności z kolejnych rzeczywistych rekonstrukcji; brak długoterminowej walidacji. | Użyć wersji v1.0 na następnym rzeczywistym projekcie i zapisać tylko konkretną porażkę, jeżeli wystąpi. | prywatne repo `litrgratis-pixel/creative-os-project-reconstructor`, przede wszystkim `PROJECT_STATE.md` |

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

---

## 4. Aktualny Handoff

### DEC-2026-003 — uczciwe wykonanie w architekturze lean

Status: `ACTIVE`. Extends: `DEC-2026-002`; nie zastępuje decyzji o Creative OS Lean.

Wybrano:

1. Praca wykonawcza otrzymuje status `STARTED / OK / PARTIAL / BLOCKED / FAILED`.
2. `OK` wymaga obserwowalnego dowodu; deklaracja AI nie wystarcza.
3. `PARTIAL` zachowuje niewykonane elementy i błędy zamiast udawać pełny sukces.
4. Błędy o wpływie na wynik, bezpieczeństwo albo wznowienie mają pierwszeństwo przed rozwijaniem nowych funkcji.
5. Creative OS przechowuje tylko stan wysokiego poziomu; szczegółowe logi, retry, checkpointy i auto-heal należą do lokalnych systemów wykonawczych.
6. Evidence-Guided Maintenance Loop oraz adapter NotebookLM są zachowane jako `PARKING`, bez aktywacji schedulera lub nowego kernela.

Nie wybrano: dobowego schedulera, trwałego event logu w Creative OS, automatycznego samoprzepisywania, automatycznego wdrażania nowych funkcji, NotebookLM jako zależności rdzenia ani zmiany zamrożonego Reconstructora v1.0 bez przypadku regresyjnego.

Powód: analiza działającego kontraktu `notebooklm-skill`, przypomnienie wcześniejszego mechanizmu auto-heal i jawna decyzja użytkownika o wchłonięciu najwartościowszych zasad. Najmniejsza użyteczna delta mieści się w istniejących plikach i nie wymaga cięższej architektury.

Warunek dalszej rozbudowy: automatyczny runtime albo dwa konkretne i porównywalne przypadki, których nie rozwiąże kontrakt wykonania i mała korekta lean.

Stan: Creative OS `ACTIVE / LEAN PILOT / TRUTHFUL EXECUTION ACTIVE`; Evidence-Guided Maintenance Loop `PARKED / CONTRACT PREPARED`; NotebookLM adapter `PARKED / OPTIONAL PILOT`; Creative OS Project Reconstructor `ACTIVE / V1.0 STABILIZATION / UNCHANGED`.

Następny krok: zastosować kontrakt wykonania w następnym rzeczywistym zadaniu i zapisać wyłącznie obserwowalny wynik checkpointu.

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

Nowy wpis ewolucji musi podać: problem, wcześniejszą postać, decyzję, dowód, co zachowujemy, co parkujemy, warunek powrotu i `SUPERSEDES`, jeśli dotyczy.
