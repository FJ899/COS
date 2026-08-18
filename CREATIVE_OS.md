---
system: creative-os-lean
version: 1.0
status: ACTIVE_LEAN_PILOT
updated_at: 2026-08-18
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

### Autonomia AI

AI samodzielnie przechwytuje pomysły, wykrywa aliasy i sprzeczności, proponuje tag, porządkuje dokumenty, prowadzi research, przygotowuje odwracalne testy oraz patche i PR.

AI pyta użytkownika, gdy zmienia się cel, priorytet, kanon, status końcowy, aktywacja projektu albo działanie jest kosztowne, publiczne, ryzykowne lub trudno odwracalne.

---

## 2. Projekty

| Projekt | Status | Gdzie stanąłem | Brak do wznowienia / zakończenia | Jeden następny krok | Źródło prawdy |
|---|---|---|---|---|---|
| Narzędzie pisarskie / ScriptOps | `QUEUED #1 / NOT ACTIVATED / SOURCE OF TRUTH ACTIVE / ACCESS CHECK REQUIRED` | Zrekonstruowano historię, zabezpieczono zakres RC1 i pełny prototyp `legacy/scriptops-v2-single.py`. Brak dowodu implementacji v5 RC1. | Ustalić, czy istnieje późniejszy kod lub wynik Codex; gdy nie istnieje, porównać prototyp z `sources/RC1_SCOPE_LOCK.md`. | Przeprowadzić `ACCESS CHECK`. | repo `litrgratis-pixel/scriptops`, przede wszystkim `PROJECT_STATE.md` |
| BPM:160 | `QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / SOURCE SUMMARY CONFIRMED / ORIGINAL FILES REQUIRED` | Skorygowano nadmierną rekonstrukcję. BPM:160 to projekt krótkich filmów i reklam opartych na ekstremalnych światach, rytmie i Peak Event. Bieżącą lokalną bramką jest Spike 001: World → Signal → Peak Event → Aftermath, montaż audio i Evidence Package. Testy widzów oraz pozostałe rozszerzenia są na PARKING. | Canon v1.2, LIVE TODO, handover, Decision Log, parking i materiały Spike 001 nie zostały jeszcze zaimportowane. | Wykonać import źródeł i `READ_ONLY RECONCILIATION`, a następnie wznowić pierwszy brakujący element Spike 001. | `projects/bpm160/PROJECT_STATE.md` |
| Creative OS | `ACTIVE / LEAN PILOT / START_HERE ACTIVE` | Cold start 002 przeszedł `PASS WITH FIXES`; pojedyncza stacyjka jest aktywna. Zakolejkowano test Ginseng zamknięcia jednej bramki oraz zapisano Archiwum09. | Nadal brakuje niezależnego testu minimalnego klucza `START_HERE.md`. | Uruchomić minimalny klucz w nowej sesji dla jednego projektu bez dodatkowego promptu. | ten plik |
| Creative OS Project Reconstructor | `ACTIVE / V1.0 STABILIZATION` | Prompt v1.0, stan, ewolucja, parking, pięć testów regresji i walidator znajdują się w repo. | Brak długoterminowej walidacji na kolejnych projektach. | Użyć v1.0 na następnym rzeczywistym projekcie i zapisać tylko konkretną porażkę. | repo `litrgratis-pixel/creative-os-project-reconstructor`, przede wszystkim `PROJECT_STATE.md` |

Kilka projektów może istnieć jednocześnie, ale każdy ma najwyżej jeden aktualny rezultat. Lokalny stan pracy może istnieć przy projekcie pozostającym w kolejce; zmiana aktywacji wymaga jawnej decyzji użytkownika.

---

## 3. Kolejka testów

### GINSENG_TEST-003 — zamknięcie pojedynczej bramki

Status: `QUEUED / NOT EXECUTED`.

Plik:

```text
tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md
```

Sprawdzamy, czy formalne rozstrzygnięcie `ACT002 ↔ DEC002`:

- zamknie dokładnie jedną bramkę;
- zmniejszy liczbę blokad z 7 do 6;
- pozostawi pozostałe bramki bez zmian;
- nie zmieni baseline;
- nie podniesie gotowości wdrożeniowej powyżej `BLOCKED`;
- zachowa źródła i `NO_IMPACT`.

Po co: to najkrótszy test, czy Ginseng wykonuje lokalną propagację zmiany zamiast ręcznie poprawiać raport albo przebudowywać cały scenariusz.

Metoda pilotażowa: wybrane wzorce Superpowers — plan, test przed zmianą, systematyczne debugowanie i weryfikacja przed ogłoszeniem sukcesu. Pełny framework nie jest instalowany globalnie.

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

### IDEA-2026-008 — Radar Deep Dive Escalation — `PARKING`

Po co: okresowy `ECOSYSTEM CAPABILITY RADAR` może znaleźć obiecujący mechanizm, ale krótki skan nie wystarcza do decyzji o asymilacji.

Kandydat do przyszłej funkcji: gdy znalezisko przekroczy próg wartości, uruchomić ukierunkowany deep dive jego kodu, architektury, dokumentacji, testów, issue/failure modes i granic zaufania. Wynik ma odpowiedzieć: co przejąć, co zastąpić, czego nie kopiować, jaki jest koszt integracji, jakie regresje są możliwe i czy można dzięki temu usunąć część naszej przyszłej architektury.

Nie teraz: radar pozostaje mechanizmem obserwacji; deep dive nie może automatycznie prowadzić do adopcji ani zmiany kanonu.

Powrót: znalezisko z radaru otrzyma `INVESTIGATE_FURTHER` lub równoważny wysoki priorytet i będzie miało konkretną relację do istniejącego problemu COS / Ginseng / Executor.

### IDEA-2026-009 — Component Impact & Integration Testing — `PARKING`

Analogicznie do testowania nowej części bolidu: przed adopcją zewnętrznego komponentu najpierw określić pełny wektor wpływu zamiast testować cały system bez kierunku.

Kandydat do przyszłej funkcji:

```text
COMPONENT / CHANGE
      ↓
FUNCTION / CAPABILITY IMPACT
      ↓
DIRECT + TRANSITIVE DEPENDENCIES
      ↓
INVARIANTS / CONTRACTS AT RISK
      ↓
TARGETED TEST PLAN
      ↓
ISOLATED CANDIDATE
      ↓
EXECUTOR + INDEPENDENT VERIFIER
```

Cel: `impact-before-adoption`, targeted regression i jawne `NO_KNOWN_IMPACT` tam, gdzie brak drogi zależności, zamiast pełnego ręcznego retestu wszystkiego albo swobodnego zgadywania przez AI.

Nie teraz: nie tworzyć nowego Impact Engine przed dowodem, że istniejące Ginseng / lineage / testy nie wystarczają.

Powrót: po Executor P1 ACCEPT i przy pierwszej rzeczywistej zmianie o nieoczywistym blast radius albo gdy dwa przypadki pokażą koszt pełnego retestu / ręcznej analizy zależności.

### IDEA-2026-010 — Same Capability, Smaller Footprint — `PARKING`

Zasada inżynierska: postęp nie musi oznaczać „nowsze” lub „więcej”. Czasami najlepsze rozwiązanie daje tę samą wymaganą funkcję przy mniejszym silniku, mniejszej architekturze i mniejszym koszcie utrzymania.

Radar i przyszłe audyty powinny aktywnie szukać nie tylko nowych capability, ale również funkcjonalnie równoważnych mechanizmów o mniejszym:

- runtime footprint;
- dependency footprint;
- state surface;
- context footprint;
- attack surface;
- koszcie operacyjnym i utrzymaniowym;
- złożoności architektury.

Warunek: „mniejsze” jest ulepszeniem tylko wtedy, gdy zachowuje wymagane capability, invariants, trust boundary i obserwowalną jakość.

Potencjalny wynik może brzmieć `REPLACE_WITH_SMALLER_EQUIVALENT` albo `DELETE_CUSTOM_COMPONENT`, ale dopiero po teście równoważności.

Powrót: radar znajdzie konkretną parę obecne/projektowane rozwiązanie ↔ mniejszy odpowiednik albo istniejący komponent wykaże mierzalny koszt złożoności, wydajności, bezpieczeństwa lub utrzymania.

### IDEA-2026-011 — Evidence Package: small stable core + extensible facets — `PARKING`

Źródło pomysłu: kandydat z `ECOSYSTEM CAPABILITY RADAR 001`, zainspirowany wzorcem małego stabilnego rdzenia i rozszerzalnych facetów spotykanym m.in. w OpenLineage.

Hipoteza: przyszły Evidence Package może być łatwiejszy do utrzymania jako minimalny stabilny envelope (tożsamość działania, wejścia/wyjścia, hashe, provenance, czas, verifier) plus opcjonalne typowane rozszerzenia, zamiast jednego stale rosnącego gigantycznego schema-object.

Potencjalne korzyści: kompatybilność, mniejszy blast radius zmian schematu, możliwość domenowych rozszerzeń bez przebudowy rdzenia oraz progressive disclosure także na poziomie evidence.

Nie teraz: brak dowodu, że obecny Evidence Package cierpi z powodu monolitycznego schematu. Nie zmieniać kontraktu Executora ani Verifiera na podstawie samej analogii.

Powrót: pierwszy realny przypadek, w którym trzeba dodać domenowy rodzaj evidence bez naruszania istniejącego rdzenia, albo deep dive wykaże dojrzały wzorzec możliwy do adaptacji bez nowej warstwy runtime.

Źródłowy snapshot: `governance/ECOSYSTEM_CAPABILITY_RADAR_001_2026-08-17.md`.

### IDEA-2026-012 — Verified Cross-Domain Transfer — `PARKING`

**Cel:** rozszerzyć przyszły `ECOSYSTEM CAPABILITY RADAR` z wyszukiwania podobnych technologii o wyszukiwanie **sprawdzonych mechanizmów z innych domen**, które rozwiązują problem o tej samej strukturze i mogą zostać zaadaptowane do COS / Ginseng / Executor.

Nie szukamy wyłącznie `AI tools`. Źródłami mogą być m.in. lotnictwo, automotive, F1, space, wojsko, energetyka jądrowa, bankowość, medtech, przemysł, distributed systems, databases, compilers, build systems, supply-chain security i inne dziedziny z dojrzałymi mechanizmami kontroli, redundancji, weryfikacji, propagacji zmian lub odtwarzania stanu.

**Zasada podstawowa:** nie przenosić powierzchownego rozwiązania ani nazwy technologii. Najpierw odtworzyć abstrakcyjny problem i mechanizm, który faktycznie odpowiada za wynik.

```text
SOURCE DOMAIN
      ↓
ABSTRACT PROBLEM
      ↓
PROVEN MECHANISM
      ↓
BOUNDARIES + ASSUMPTIONS
      ↓
TRANSFER HYPOTHESIS
      ↓
LOCAL CANDIDATE
      ↓
LOCAL TEST + INDEPENDENT PROOF
```

Przykładowe transfery strukturalne:

- build-system dependency invalidation → Ginseng `STALE / REVALIDATION_REQUIRED`;
- software supply-chain attestations → Executor action-result evidence;
- four-eyes / separation-of-duties → Human Decision Gate / independent verifier;
- event sourcing / crash recovery → COS/Reconstructor state reconstruction;
- safety-critical change impact analysis → Component Impact & Integration Testing.

**Poziomy dojrzałości znaleziska:**

```text
INTERESTING_IDEA
→ PROVEN_MECHANISM
→ TRANSFER_CANDIDATE
→ LOCAL_CANDIDATE
→ LOCALLY_VERIFIED
```

`PROVEN_MECHANISM` oznacza wyłącznie, że mechanizm ma wiarygodny dowód działania w domenie źródłowej. Nie wolno utożsamiać tego z `LOCALLY_VERIFIED`.

`TRANSFER_CANDIDATE` oznacza: mechanizm jest wystarczająco dobrze udokumentowany i zweryfikowany u źródła, a istnieje rozsądna hipoteza, że kluczowe założenia mogą przetrwać zmianę domeny. Nadal **nie jest to decyzja o adopcji**.

**Minimalny TRANSFER EVIDENCE PACKAGE:**

- `SOURCE / ORIGINAL_DOMAIN` — skąd pochodzi mechanizm i w jakim środowisku działa;
- `PROBLEM_SOLVED` — jaki konkretny problem rzeczywiście rozwiązuje;
- `MECHANISM` — jaka przyczynowa zasada / konstrukcja daje wynik;
- `IMPLEMENTATION_EVIDENCE` — czy istnieje rzeczywista implementacja, nie tylko koncepcja;
- `TEST_EVIDENCE` — jak i przez kogo została przetestowana;
- `OPERATING_HISTORY` — jeżeli dostępne: rzeczywiste użycie, skala, czas działania;
- `FAILURE_MODES` — znane sposoby awarii i błędnego użycia;
- `BOUNDARIES` — czego rozwiązanie świadomie nie rozwiązuje;
- `CONSTRAINTS` — wymagania środowiskowe, organizacyjne, fizyczne lub techniczne;
- `TRADE_OFFS` — co zyskuje się kosztem czego;
- `SECURITY / SAFETY MODEL` — jakie zagrożenia uwzględnia i jakich nie uwzględnia;
- `MAINTENANCE COST` — koszt operacyjny, aktualizacje, zależności i kompetencje;
- `TRANSFER_HYPOTHESIS` — co dokładnie chcemy przenieść do naszej domeny;
- `TRANSFER_DISTANCE` — jak daleka jest domena źródłowa od docelowej i które różnice są istotne;
- `ASSUMPTIONS_THAT_MUST_HOLD` — jakie warunki odpowiedzialne za skuteczność muszą pozostać prawdziwe po transferze;
- `WHAT_COULD_REPLACE` — własny komponent, mechanizm lub przyszłą pracę, którą kandydat może ograniczyć albo usunąć;
- `LOCAL_PROOF_REQUIRED` — jaki test odróżni udany transfer od atrakcyjnej analogii.

**Kryterium transferowalności:** nie wystarczy udowodnić `TO DZIAŁA`. Trzeba wykazać, że **powód, dla którego działa w źródle, ma nadal zastosowanie w naszej domenie**. Jeżeli kluczowe założenie znika po transferze, kandydat wraca do `INTERESTING_IDEA` albo jest odrzucany.

**Powiązanie z Same Capability, Smaller Footprint:** kandydaci cross-domain otrzymują dodatkowy priorytet, jeżeli pozwalają zachować tę samą wymaganą capability przy mniejszym runtime, mniejszej liczbie komponentów, zależności, stanie, attack surface lub koszcie utrzymania. Najlepszym wynikiem transferu może być nie nowa funkcja, lecz `REPLACE_WITH_SMALLER_EQUIVALENT` albo `DELETE_CUSTOM_COMPONENT`.

**Anti-patterns:**

- kopiowanie technologii zamiast mechanizmu;
- traktowanie popularności albo prestiżu branży jako dowodu;
- przenoszenie wyniku bez warunków brzegowych;
- utożsamianie testów źródłowych z naszymi testami;
- ignorowanie skali, fizyki, threat modelu lub modelu organizacyjnego źródła;
- używanie analogii jako uzasadnienia `ACCEPT`;
- automatyczna adopcja przez radar bez Human Decision Gate;
- zwiększanie architektury tylko dlatego, że rozwiązanie źródłowe jest rozbudowane.

**Docelowy werdykt badawczy:**

```text
NOT_TRANSFERABLE
INTERESTING_IDEA
PROVEN_MECHANISM
TRANSFER_CANDIDATE
DEEP_DIVE_REQUIRED
LOCAL_TEST_REQUIRED
```

Dopiero lokalny test zgodny z architekturą może później prowadzić do istniejących decyzji `ADOPT_NOW / ADAPT_EXISTING / DEFER_UNTIL_GATE / REJECT_DUPLICATE / REJECT_SCOPE`.

**Granice:** to jest przyszły tryb badawczy radaru, nie nowy komponent architektury. Nie zmienia Ginseng semantics, kontraktu Executora, Verifiera, P0–P4 ani priorytetów. Radar zbiera evidence i hipotezy; nie tworzy samodzielnie kanonu ani decyzji adopcyjnych.

**Nie teraz:** nie budować osobnego `technology-transfer engine`, bazy wiedzy ani runtime. Pierwszy etap może być realizowany jako metoda research + ustandaryzowany rekord evidence.

**Powrót:** pierwszy kandydat znaleziony poza bezpośrednią domeną AI/software, który ma wiarygodne implementation/test evidence, pasuje strukturalnie do realnego problemu COS / Ginseng / Executor i daje możliwość usunięcia pracy własnej, zmniejszenia footprintu albo wzmocnienia trust boundary. Taki przypadek powinien uruchomić `IDEA-2026-008 — Radar Deep Dive Escalation` i zakończyć się jawnie `TRANSFER_CANDIDATE` albo `NOT_TRANSFERABLE`, bez automatycznej adopcji.

---

## 5. Aktualny Handoff

### DEC-2026-006 — kolejny test Ginseng i korekta BPM:160

Status: `ACTIVE`. Extends: `DEC-2026-005`.

Wybrano:

1. Zakolejkować Ginseng Test 003 jako test zamknięcia dokładnie jednej bramki.
2. Użyć wybranych wzorców Superpowers tylko wewnątrz testu, bez globalnej instalacji.
3. Zachować poprawiony kontrakt wyniku Ginseng: `analysis_verdict` osobno od `implementation_readiness`.
4. Traktować logiczny scenario overlay jako artefakt danych, nie branch Git.
5. Skorygować BPM:160: bieżąca bramka to Spike 001, a test widza pozostaje na parkingu.
6. Zachować trzy lokalne osie klasyfikacji BPM i nie utożsamiać ich z Navigation Protocol COS.
7. Zapisać `SOURCE_SUMMARY_2026-07-31.md` jako jawne sprostowanie, ale nadal wymagać plików pierwotnych.
8. Zachować rozmowę w `archives/Archiwum09.md`.

Nie wybrano: aktywacji Ginseng jako projektu, globalnej instalacji Superpowers, automatycznej pamięci Claude-Mem, frontendu Ginseng, testu widza BPM ani zmiany kolejności portfela.

Powód: najkrótszym dowodem wartości Ginseng jest kontrolowana lokalna propagacja jednej decyzji. W BPM wcześniejsza rekonstrukcja pomyliła fragment projektu z całością i otworzyła zły następny krok.

Stan:

```text
Creative OS: ACTIVE / LEAN PILOT / START_HERE ACTIVE
Ginseng Test 003: QUEUED / NOT EXECUTED
ScriptOps: QUEUED #1 / ACCESS CHECK REQUIRED
BPM:160: QUEUED #2 / LOCAL SPIKE 001 IN PROGRESS / ORIGINAL FILES REQUIRED
Project Reconstructor: ACTIVE / V1.0 STABILIZATION
```

Następny krok globalny: niezależny test minimalnego klucza stacyjki. Następny krok testowy: wykonać GINSENG_TEST-003 po przygotowaniu jednego kontrolowanego wariantu decyzji.

---

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
- **EVOLUTION-2026-013 — korekta BPM i test Ginseng:** problemem było uznanie fragmentu BPM za całość oraz brak dowodu lokalnej propagacji decyzji w Ginseng. Decyzja: przywrócić Spike 001 jako bieżącą bramkę, zachować testy widza na parkingu, rozdzielić lokalne klasyfikacje od Navigation Protocol i zakolejkować test zamknięcia jednej bramki. Dowód: jawne sprostowanie użytkownika oraz wynik S001 z siedmioma blokadami. Zachowujemy kolejność portfela, źródłowość i baseline. Parkujemy globalne skille, frontend i dalsze rozszerzenia. Warunek powrotu: pliki pierwotne BPM oraz wykonany GINSENG_TEST-003. Supersedes: operacyjną część `EVOLUTION-2026-007` i błędny następny krok BPM zapisany w `EVOLUTION-2026-011`. Status: `ACTIVE CORRECTION / TEST QUEUED`.

Nowy wpis ewolucji musi podać problem, wcześniejszą postać, decyzję, dowód, co zachowujemy, co parkujemy, warunek powrotu i `SUPERSEDES`, gdy dotyczy.