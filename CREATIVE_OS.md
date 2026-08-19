---
system: creative-os-lean
version: 1.0
status: ACTIVE_LEAN_PILOT
updated_at: 2026-08-19
history: git
---

# Creative OS

Osobista pamięć projektów, pomysłów i wznowienia pracy. Szczegóły rozwiniętych projektów pozostają w ich lokalnych systemach. Pojedynczym entrypointem uruchomienia jest `START_HERE.md`.

## 1. Zasady

### Stan i decyzje

1. Rozmowa prowadzi proces; repozytorium zachowuje stan.
2. Najnowsza jawna decyzja użytkownika wygrywa nad starszym dokumentem, handoffem i pamięcią AI.
3. Każda informacja ma jednego właściciela. Creative OS nie kopiuje lokalnych backlogów ani kanonów.
4. Analiza zaczyna się jako `READ_ONLY`. Zmiana kierunku wymaga decyzji użytkownika; techniczne odzwierciedlenie zatwierdzonej decyzji może wykonać AI.
5. Rekomendacja AI nie jest decyzją. Pomysł pozostaje hipotezą do czasu mocniejszego dowodu.
6. Brak dowodu oznacza niepewność. Nazwa, atrakcyjna narracja ani zgodność modeli nie są dowodem.
7. Przed budową sprawdź projekty, Idea Inbox i gotowe rozwiązania.
8. Reguły zmieniaj na checkpointach, nie po każdym odkryciu.
9. Handoff jest nadpisywany; Git zachowuje historię.
10. `OK` wymaga obserwowalnego dowodu. Wynik częściowy pozostaje `PARTIAL`, a błąd pozostaje jawny.
11. Przed dodaniem funkcji wskaż problem, brak istniejącego rozwiązania, obserwowalny test i koszt utrzymania.
12. `START_HERE.md` jest mapą uruchomienia, nie właścicielem stanu.
13. Korekta lokalnego projektu nie zmienia automatycznie jego priorytetu lub aktywacji w portfelu.
14. COS posiada wyłącznie trwały stan wysokiego poziomu i przekrojowy, ciągłość, provenance oraz zaakceptowany stan cross-project; lokalna prawda komponentu pozostaje u jego semantycznego właściciela.
15. Umiejscowienie informacji w repo nie tworzy semantic ownership ani authority. Zapis decyzji nie jest jej źródłem ani nową zgodą na efekt.

Minimalny werdykt dla nowej informacji:

```text
ZMIENIA PLAN / NIE ZMIENIA PLANU / TRZEBA SPRAWDZIĆ
```

Minimalny status wykonania:

```text
STARTED / OK / PARTIAL / BLOCKED / FAILED
```

### Navigation Protocol Creative OS

Każdy nowy pomysł na poziomie portfela otrzymuje tag:

- `CORE` — potrzebny teraz do aktualnego rezultatu;
- `DETOUR` — wartościowy i powiązany, ale nie teraz;
- `PARKING` — na inny etap; wymaga warunku powrotu;
- `DRIFT` — nie służy jawnemu rezultatowi albo wynika głównie z atrakcyjności nowości.

Pytania: jaki rezultat przybliża, czy jest potrzebny teraz, czy to alias i jaki dowód uzasadnia aktywację.

Navigation Protocol jest mechanizmem globalnego COS. Nie wolno automatycznie przypisywać go lokalnym projektom ani zastępować nim ich własnych klasyfikacji.

Navigation Protocol dotyczy portfolio/project-state navigation. Nie jest właścicielem operacyjnego wyboru HOW, rankingu rozwiązań ani cognitive routingu należącego do Intelligence.

### Autonomia AI

AI samodzielnie przechwytuje pomysły, wykrywa aliasy i sprzeczności, proponuje tag, porządkuje dokumenty, prowadzi research, przygotowuje odwracalne testy oraz patche i PR.

AI pyta użytkownika, gdy zmienia się cel, priorytet, kanon, status końcowy, aktywacja projektu albo działanie jest kosztowne, publiczne, ryzykowne lub trudno odwracalne.

---

## 2. Projekty

| Projekt | Status | Gdzie stanąłem | Brak do wznowienia / zakończenia | Jeden następny krok | Źródło prawdy |
|---|---|---|---|---|---|
| Narzędzie pisarskie / ScriptOps | `QUEUED #1 / LOCAL PHASE 6 CONTROLLED WORKFLOW MECHANISM PASS / NO MATURITY CLAIM / POST-SADDLE STATE RECONCILED` | Lokalny `main@5af0cd8ac65e72ae534827c677fe4bd12b23e4ca` zachowuje kontrolowany workflow oparty na v2 i ma już pogodzone startup/current-state po zakończeniu późniejszych checkpointów Saddle. To nadal nie jest pełny ScriptOps v5 RC1 ani maturity claim. | Brak aktywnego lokalnego product-development gate wynikającego z Phase 6. Materially-different workload jest osią oceny, nie automatyczną aktywacją produktu ani maturity promotion. | Przy następnym jawnie uruchomionym bounded evaluation użyć istniejącego Phase-6 mechanism na materially-different workload, bez rewrite i bez new capability. | repo `JTJ07/scriptops`, przede wszystkim `PROJECT_STATE.md` |
| BPM:160 | `QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / SOURCE SUMMARY CONFIRMED / ORIGINAL FILES REQUIRED` | Skorygowano nadmierną rekonstrukcję. BPM:160 to projekt krótkich filmów i reklam opartych na ekstremalnych światach, rytmie i Peak Event. Bieżącą lokalną bramką jest Spike 001: World → Signal → Peak Event → Aftermath, montaż audio i Evidence Package. Testy widzów oraz pozostałe rozszerzenia są na PARKING. | Canon v1.2, LIVE TODO, handover, Decision Log, parking i materiały Spike 001 nie zostały jeszcze zaimportowane. | Wykonać import źródeł i `READ_ONLY RECONCILIATION`, a następnie wznowić pierwszy brakujący element Spike 001. | `projects/bpm160/PROJECT_STATE.md` |
| Creative OS | `ACTIVE / LEAN PILOT / START_HERE ACTIVE` | COS ownership/state/continuity closure jest `HUMAN ACCEPTED / CLOSED` i weszło do `main` przez PR #30. Bieżąca praca to wyłącznie post-closure continuity maintenance po nowych lokalnych merge'ach, bez ponownego otwierania zamkniętego scope. | Brak nowego blockera COS. P2 memory/repo recovery pozostaje inboxem oczekującym na evidence; może preemptować tylko po znalezieniu P0/P1 problemu. | Zachować wynik Reconstructor Run 001 jako evidence po osobnej Human merge authority, następnie przejść do materially-different ScriptOps workload, o ile P2 nie wniesie wyższego blockera. | ten plik |
| Creative OS Project Reconstructor | `ACTIVE / V1.0 STABILIZATION` | Prompt v1.0 pozostaje zamrożony na lokalnym `main`; technically verified Real-Value Run 001 istnieje jako niezintegrwany jeszcze kandydat PR #5 i nie zmienia sam z siebie local accepted state. | Brak długoterminowej walidacji na kolejnych niezależnych projektach; Run 001 nie wykazał potrzeby zmiany promptu. | Zachować wynik Run 001 przez osobną Human merge authority; prompt pozostawić bez zmian. | repo `JTJ07/creative-os-project-reconstructor`, przede wszystkim `PROJECT_STATE.md` |

Kilka projektów może istnieć jednocześnie, ale każdy ma najwyżej jeden aktualny rezultat. Lokalny stan pracy może istnieć przy projekcie pozostającym w kolejce; zmiana aktywacji wymaga jawnej decyzji użytkownika.

---

## 3. Kolejka testów

### GINSENG_TEST-003 — zamknięcie pojedynczej bramki

Status: `EXECUTED / INDEPENDENTLY_VERIFIED_PASS`.

Pliki aktualnego wyniku:

```text
tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md
tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md
```

Wynik zaakceptowany do dalszej oceny D0:

- zamknięto dokładnie jedną bramkę;
- liczba blokad spadła z 7 do 6;
- pozostałe bramki pozostały semantycznie bez zmian;
- baseline pozostał niezmieniony;
- `implementation_readiness` pozostało `BLOCKED`;
- źródła i pięć kontroli `NO_IMPACT` zostały zachowane;
- independent replay: `PASS`;
- `FALSE SUCCESS PATHS: 0` dla Test-003.

Test-003 nie stanowi sam w sobie claimu ukończenia Ginseng D0. Późniejszy pełny D0 closure został niezależnie zweryfikowany, zaakceptowany przez Human i zintegrowany przez PR #29. Aktualny stan: `GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED`. Źródła: `governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md` oraz `governance/GINSENG_D0_INTEGRATION_RECORD_2026-08-19.md`.

---

## 4. Idea Inbox

### IDEA-2026-001 — pełna architektura Creative OS / COS — `PARKING`

Nie teraz: brak dowodu, że Lean nie wystarcza. Powrót: dwie nazwane porażki, których nie naprawi mała korekta.

### IDEA-2026-002 — `workshop/YYYY-MM` — `PARKING`

Nie teraz: Git i branche wystarczają. Powrót: aktywne materiały, których nie da się utrzymać w branchu lub poza kanonem.

### IDEA-2026-003 — hybrydowa architektura API + WebAI — `PARKING`

Powrót: benchmark A/B/C na jednym rzeczywistym zadaniu, mierzący jakość, koszt, czas, interwencje, utratę decyzji i możliwość wznowienia.

### IDEA-2026-004 — Evidence-Guided Maintenance Loop — `PARKING`

Aktywny jest truthful execution. Scheduler, event log, retry, auto-heal i adaptery pozostają zaparkowane. Powrót: runtime albo dwa powtarzalne problemy wymagające ręcznej rekonstrukcji.

### IDEA-2026-005 — GitHub Issues / Projects jako widoki pochodne — `PARKING`

Nie teraz: tworzą drugie miejsce stanu. Powrót: dwa przypadki utraty, duplikacji lub kosztownej obsługi, których nie naprawi mała korekta.

### IDEA-2026-006 — ciągły Reconstructor monitorujący rozmowy — `PARKING`

Nie teraz: wymaga runtime, prywatności, checkpointów, zatwierdzania i obsługi konfliktów. Powrót: dwie udokumentowane porażki ręcznego trybu i gotowy kontrakt dostępu.

### IDEA-2026-007 — zewnętrzne skille jako warstwa pomocnicza — `PARKING`

Źródło: analiza Find Skills, Superpowers, Claude-Mem, Impeccable i Task Observer.

Decyzje:

- Find Skills — używać na żądanie, bez automatycznej instalacji;
- Superpowers — pilot wybranych wzorców w Ginseng;
- Claude-Mem — nie jako źródło prawdy; możliwy wyłącznie usuwalny cache;
- Impeccable — potencjalnie przyszły frontend Ginseng;
- Task Observer — alias Evidence-Guided Maintenance Loop; zachować mały checkpoint, nie pełny runtime.

Warunek powrotu: konkretny problem projektu, audyt kodu i uprawnień, instalacja project-local przypięta do wersji oraz test przed/po.

---

## 5. Aktualny Handoff

### DEC-2026-007 — Ginseng D0 closed; COS continuity closure

Status: `SUPERSEDED AS CURRENT HANDOFF / HISTORICAL BASIS PRESERVED`. Superseded operationally by accepted COS PR #30 and the later current-state maintenance below. The accepted BPM:160 correction and local ownership boundaries remain preserved.

Historical accepted basis:

1. `GINSENG_TEST-003`: `EXECUTED / INDEPENDENTLY_VERIFIED_PASS`.
2. `GINSENG_DONE_D0`: `HUMAN ACCEPTED / CLOSED`; PR #29 został scalony do accepted COS history.
3. Ginseng runtime, formal project activation i whole-project completion beyond frozen D0 pozostają nieautoryzowane.
4. COS posiada trwały high-level/cross-project state, continuity, provenance i accepted cross-project state; lokalna prawda pozostaje u lokalnego semantic ownera.
5. COS portfolio/project-state navigation nie jest operational HOW selection i nie przejmuje cognitive routingu od Intelligence.
6. Draft PR #18, #19 i #20 zostały zamknięte jako superseded historical/supporting candidates bez merge; ich Git provenance pozostaje zachowane.
7. Executor 1.0 pozostaje poza aktywnym developmentem bez nowego mierzalnego blockera.
8. Historyczny ScriptOps pointer z tego checkpointu pozostaje provenance, ale nie jest już current local state.

### CURRENT-2026-008 — Post-COS closure evaluation state

Classification: `REPO FACT / WORKING EVALUATION STATE / NOT HUMAN DECISION`.

Current verified facts:

1. COS ownership/state/continuity closure jest `HUMAN ACCEPTED / CLOSED`; PR #30 został scalony jako `main@23152cb1bf5443574da9ff44600a5a8c8c136025`.
2. ScriptOps Phase 6 pozostaje `CONTROLLED WORKFLOW MECHANISM PASS / NO MATURITY CLAIM`; current local `main@5af0cd8ac65e72ae534827c677fe4bd12b23e4ca` ma już pogodzone post-Saddle startup/current-state po merge PR #9.
3. Saddle P0 security hardening i P1 durable-state reconciliation są zintegrowane; post-merge work-state correction PR #34 jest na `main@a4d2721f3882a17438a36b8c9fc386b266376dc5`.
4. Reconstructor Real-Value Run 001 wykrył cztery realne current-state contradictions i nie wykazał potrzeby zmiany promptu v1.0; wynik jest technically verified w otwartym PR #5 i nie jest jeszcze local accepted history.
5. `governance/MEMORY_REPO_GAP_RECOVERY_RECORD_2026-08-19.md` pozostaje `RECOVERY_RECORD / NON_CANONICAL / NO_AUTHORITY_PROMOTION`; nowe evidence może zmienić priorytet tylko gdy ujawnia safety/authority/false-success/current-state blocker.

Stan:

```text
Creative OS: ACTIVE / LEAN PILOT / START_HERE ACTIVE
COS ownership/state/continuity: HUMAN ACCEPTED / CLOSED
Ginseng D0: HUMAN ACCEPTED / CLOSED
Ginseng runtime: NOT AUTHORIZED
Saddle P0 security maintenance: COMPLETE / MERGED
Saddle P1 durable-state reconciliation: COMPLETE / MERGED
P2 memory/repo recovery: WAITING_FOR_EVIDENCE
Project Reconstructor Run 001: TECHNICALLY VERIFIED EVIDENCE CANDIDATE / MERGE AUTHORITY PENDING
ScriptOps: QUEUED #1 / LOCAL PHASE 6 CONTROLLED WORKFLOW MECHANISM PASS / NO MATURITY CLAIM / POST-SADDLE STATE RECONCILED
BPM:160: QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / ORIGINAL FILES REQUIRED
```

Najbliższy globalny working item: zachować Reconstructor Run 001 jako local evidence po osobnej Human merge authority, następnie wykonać materially-different bounded ScriptOps workload. P2 może preemptować tę sekwencję wyłącznie po wykryciu P0/P1 problemu. To jest work-state/evaluation sequencing, nie nowy product roadmap i nie transfer HOW selection do COS.

---

### Ginseng D-08 durable evidence custody — 2026-08-19

Human selected Option B: preserve the exact `GINSENG_TEST-003` evidence bytes in durable repository custody and bind them to SHA-256.

Historical state at the time D-08 custody entered accepted history:

```text
artifact: tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.zip
manifest: tests/ginseng/evidence/GINSENG_TEST003_EXECUTION_EVIDENCE_2026-08-18.manifest.json
SHA-256: d9077d08012667a8a2a91e93912ee752bf991b50b5b01e4d2f80914cde315fdf
byte size: 95846
ZIP entries: 39
D-08: SATISFIED — DURABLE REPOSITORY CUSTODY / EXACT BYTES / SHA-256 BOUND
GINSENG D0 at custody time: BLOCKED — D-05 DECISION LINEAGE remained open; D-09 required final recheck after closure.
```

Current integrated state after PR #29: `GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED`.

This custody record does not itself prove D-05, activate runtime, or activate Ginseng as a formal project. It remains historical evidence inside the later accepted D0 closure chain.

## 6. Ewolucja systemu — append-only

- **EVOLUTION-2026-001 — BPM:160:** lokalny system posiadał WIP, parking, Decision Log, handover, QA i testy empiryczne. Status: `LOCAL SYSTEM`.
- **EVOLUTION-2026-002 — Creative OS:** powstał, ponieważ pomysły ginęły, a wznowienie wymagało składania kontekstu. Status: `ACTIVE / LEAN PILOT`.
- **EVOLUTION-2026-003 — Cognitive OS:** wartość reguł wchłonięta, ciężki system zarchiwizowany. Status: `ARCHIVED / ABSORBED`.
- **EVOLUTION-2026-004 — Navigation Protocol:** zachowany jako globalny filtr portfela. Status: `ACTIVE RULE`.
- **EVOLUTION-2026-005 — jeden plik:** cięższa architektura zaparkowana do dwóch konkretnych porażek. Status: `ACTIVE LEAN ARCHITECTURE`.
- **EVOLUTION-2026-006 — autonomia AI:** AI wykonuje operacje, użytkownik rozstrzyga kierunek. Status: `ACTIVE RULE`.
- **EVOLUTION-2026-007 — BPM:160:** wcześniejsza obserwacja o perfekcjonizmie wskazała ryzyko, lecz nie była kompletnym stanem projektu. Status: `PARTIALLY SUPERSEDED BY EVOLUTION-2026-013`.
- **EVOLUTION-2026-008 — sprzątanie repo:** stare rozwiązanie zachowano na branchach archiwalnych. Commit: `7cc2cf2b794d646527a4c5469fd7a764b4f9e190`.
- **EVOLUTION-2026-009 — truthful execution:** aktywne statusy wykonania i wymóg dowodu; cięższy runtime pozostaje PARKING.
- **EVOLUTION-2026-010 — cold start i walidator:** niezależne AI wznowiło ekosystem; wynik `PASS WITH FIXES`.
- **EVOLUTION-2026-011 — Feature Razor i stan BPM:** dodano filtr funkcji oraz pierwszy, później skorygowany punkt odzyskiwania BPM.
- **EVOLUTION-2026-012 — pojedyncza stacyjka:** `START_HERE.md` aktywny; test minimalnego klucza pozostaje wymagany.
- **EVOLUTION-2026-013 — korekta BPM i test Ginseng:** problemem było uznanie fragmentu BPM za całość oraz brak dowodu lokalnej propagacji decyzji w Ginseng. Decyzja: przywrócić Spike 001 jako bieżącą bramkę, zachować testy widza na parkingu, rozdzielić lokalne klasyfikacje od Navigation Protocol i zakolejkować test zamknięcia jednej bramki. Dowód: jawne sprostowanie użytkownika oraz wynik S001 z siedmioma blokadami. Zachowujemy kolejność portfela, źródłowość i baseline. Parkujemy globalne skille, frontend i dalsze rozszerzenia. Warunek powrotu: pliki pierwotne BPM oraz wykonany GINSENG_TEST-003. Supersedes: operacyjną część `EVOLUTION-2026-007` i błędny następny krok BPM zapisany w `EVOLUTION-2026-011`. Status: `SUPERSEDED OPERATIONALLY BY EVOLUTION-2026-014 / HISTORICAL EVIDENCE PRESERVED`.
- **EVOLUTION-2026-014 — Ginseng D0 closure i COS continuity reconciliation:** Ginseng D0 przeszedł source-bound D-05 proof, durable D-08 custody i finalny D-09 recheck; Human zaakceptował technical closure, a następnie osobno autoryzował merge PR #29. Problemem po integracji był stale cross-project handoff oraz pre-merge terminal state w validatorach COS. Decyzja: materializować aktualny accepted state bez przepisywania historycznych proof records, zamknąć stare drafty #18–#20 jako superseded i domknąć COS state/continuity najmniejszą korektą. Runtime i nowe capability pozostają poza zakresem. Status: `ACTIVE RECONCILIATION`.
- **EVOLUTION-2026-015 — ScriptOps current-state/locator reconciliation:** repo-level evidence potwierdziło `JTJ07/scriptops@daa6e5dc210e09171a530eeffe5601e0e74ae041` z lokalnym statusem `PHASE 6 CONTROLLED WORKFLOW MECHANISM PASS / NO MATURITY CLAIM / SADDLE LIVE MODEL EVIDENCE NEXT`. Problemem był stale cross-project pointer `ACCESS CHECK REQUIRED` i stare `litrgratis-pixel/...` locatory w COS. Korekta aktualizuje wyłącznie high-level state i locatory; nie kopiuje lokalnego backlogu, nie aktywuje ScriptOps i nie tworzy maturity claim. Status: `ACTIVE RECONCILIATION`.
- **EVOLUTION-2026-016 — post-closure continuity maintenance po Reconstructor Run 001:** po Human-accepted merge COS PR #30 i późniejszych merge'ach Saddle/ScriptOps Reconstructor real-value run ujawnił, że current-state owner, startup map i validator nadal kodowały wcześniejsze checkpointy jako bieżące. Korekta: zachować historyczne wpisy bez przepisywania, zaktualizować tylko current handoff, ScriptOps locator/status i fail-closed validator; lokalny ScriptOps pozostaje semantic ownerem własnego stanu. Dowód: COS `main@23152cb1bf5443574da9ff44600a5a8c8c136025`, Saddle `main@a4d2721f3882a17438a36b8c9fc386b266376dc5`, ScriptOps `main@5af0cd8ac65e72ae534827c677fe4bd12b23e4ca`, technically verified Reconstructor Run 001 PR #5. Zachowujemy ownership boundaries i `NO MATURITY CLAIM`; parkujemy nowe capability i generalizację. Warunek powrotu: kolejny realny contradiction lub nowy accepted local-state merge wymagający derived pointer update. Supersedes: wyłącznie current-state interpretation wpisów `EVOLUTION-2026-014` i `EVOLUTION-2026-015`; historyczne evidence pozostaje ważne. Status: `CURRENT CONTINUITY MAINTENANCE`.

Nowy wpis ewolucji musi podać problem, wcześniejszą postać, decyzję, dowód, co zachowujemy, co parkujemy, warunek powrotu i `SUPERSEDES`, gdy dotyczy.
