---
system: creative-os-lean
version: 1.0
status: ACTIVE_LEAN_PILOT
updated_at: 2026-07-26
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

Minimalny werdykt dla nowej informacji: `ZMIENIA PLAN` / `NIE ZMIENIA PLANU` / `TRZEBA SPRAWDZIĆ`.

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
| BPM:160 | `PAUSED / WAITING`, priorytetowy | Presja stworzenia idealnego świata zaczęła dominować nad testem oczekiwań widza. Prostym kontrdowodem były krótkie materiały o podstawowym bodźcu z ogromnym zainteresowaniem. | Mały, publikowalny test widza bez wcześniejszego zbudowania idealnego świata. | Zdefiniować jeden minimalny test reakcji widza i porównać go z aktualnym planem. | lokalny system BPM:160, zwłaszcza `23_LIVE_TODO.md` i najnowszy zatwierdzony handover |
| Creative OS | `ACTIVE / LEAN PILOT` | Zatwierdzono jeden wersjonowany plik, wchłonięcie reguł COS i Navigation Protocol jako tagu. | Dowód, że system przechwytuje pomysł i umożliwia wznowienie bez archeologii stanu. | Wykonać pierwszy realny cykl: przechwycić pomysł, potem wznowić projekt z tej tabeli i lokalnego źródła. | ten plik |

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

---

## 4. Aktualny Handoff

### DEC-2026-002 — przejście na Creative OS Lean

Status: `ACTIVE`. Supersedes: `DEC-2026-000`, `DEC-2026-001`.

Wybrano:

1. Creative OS jest wspólną przestrzenią projektów, pomysłów i resume.
2. Pilot zaczyna jako jeden plik w GitHubie.
3. Cognitive OS nie jest rozwijany jako osobny system; jego sprawdzone reguły zostają wchłonięte.
4. Projekty zachowują lokalne systemy jako szczegółowe źródła prawdy.
5. Navigation Protocol jest filtrem nowych kierunków.
6. AI ma wysoką autonomię operacyjną; użytkownik zachowuje decyzje kierunkowe.
7. Rekomendacje pozostają hipotezami do czasu mocniejszego dowodu.

Nie wybrano: obowiązkowych dziesięciu sesji, domyślnego audytu A→B, osobnego governance kernel, pięciu plików, kopiowania lokalnych backlogów ani przechowywania starego COS w aktywnym workshopie.

Powód: checkpoint wykazał `SIMPLIFY`, użytkownik zatwierdził lean, a poprzednia struktura generowała koszt i sprzeczne statusy.

Warunek reopen: dwie konkretne i porównywalne porażki wersji jednoplikowej, których nie rozwiąże mała korekta.

Stan: Creative OS `ACTIVE / LEAN PILOT`; BPM:160 `PAUSED / WAITING`, priorytetowy; COS `ARCHIVED AS EXPERIMENT / ABSORBED AS RULES / NOT DEVELOPED AS SEPARATE SYSTEM`; Navigation Protocol `ACTIVE RULE`.

Następny krok: w następnej sesji przechwycić każdy nowy pomysł bez rozwijania, a potem sprawdzić wznowienie projektu na podstawie tabeli i lokalnego źródła.

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

Nowy wpis ewolucji musi podać: problem, wcześniejszą postać, decyzję, dowód, co zachowujemy, co parkujemy, warunek powrotu i `SUPERSEDES`, jeśli dotyczy.
