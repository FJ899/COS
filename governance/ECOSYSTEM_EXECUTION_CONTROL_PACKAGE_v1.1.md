---
document: ECOSYSTEM_EXECUTION_CONTROL_PACKAGE
version: 1.1
strategic_direction: ACCEPTED
document_status: CANONICAL
cos_status: IMPORTED_PENDING_MERGE
implementation_status: PENDING_IMPLEMENTATION
architecture_status: FROZEN
approved_at: 2026-08-04
owner: USER
next_action: IMPLEMENTATION_ONLY
---

# Ecosystem Execution Control Package v1.1

## 1. Misja

Budujemy osobisty system operacyjny do bezpiecznej współpracy człowieka i AI.

Nie budujemy „firmy AI”. Nie budujemy platformy, SaaS ani autonomicznej organizacji przed udowodnieniem jednej działającej jednostki pracy.

Kanoniczny przepływ:

```text
Użytkownik określa cel
        ↓
Ginseng chroni intencję i ujawnia rozwidlenia
        ↓
Creative OS przechowuje pamięć, kanon i zależności
        ↓
PROJECT CONTRACT
        ↓
TASK CONTRACT
        ↓
Executor wykonuje zatwierdzoną pracę
        ↓
Verifier dostarcza niezależny dowód
        ↓
Użytkownik otrzymuje wynik i następny krok
```

## 2. Minimalny produkt widziany przez użytkownika

```text
INPUT
„Napraw problem X”

OUTPUT
✓ draft PR
✓ dowód wykonania
✓ lista zmian
✓ ujawnione ryzyka
✓ werdykt ACCEPT / REWORK / STOP
✓ następny krok
```

Każda nowa funkcja musi pomagać dostarczyć jeden z tych elementów albo usuwać konkretny, zmierzony blocker.

## 3. Role komponentów

### Ginseng

Rola przyszłej warstwy decyzyjnej:

- utrzymuje intencję;
- wykrywa dryf;
- ujawnia rozwidlenia i konsekwencje;
- chroni cel przed przypadkową optymalizacją.

Ginseng nie wykonuje pracy i nie podejmuje decyzji za użytkownika. Runtime Ginseng pozostaje zamrożony do czasu ukończenia P3A i P3B.

### Creative OS

Rola pamięci i konstytucji:

- przechowuje kanon;
- przechowuje decyzje i ich status;
- utrzymuje mapę projektów i zależności;
- wskazuje źródła prawdy;
- odróżnia decyzję użytkownika od rekomendacji AI.

Creative OS nie wykonuje zmian technicznych w projektach i nie wydaje dowodu wykonania.

### Executor

Rola kontrolowanego systemu wykonawczego:

- przyjmuje zatwierdzony Task Contract;
- egzekwuje zakres;
- przygotowuje środowisko;
- uruchamia Reasoning Provider i Tool Worker;
- zbiera surowe evidence;
- tworzy draft PR;
- przekazuje materiał do niezależnej weryfikacji.

Executor nie wybiera celu, nie zmienia kanonu, nie zmienia priorytetów i nie wydaje autorytatywnego ACCEPT dla własnej pracy.

### Verifier

Verifier jest niezależnym właścicielem technicznego werdyktu. Sprawdza exact SHA, zakres, środowisko, testy, integralność evidence, replay i drogi do false success.

Kandydat może dostarczyć dane i obserwacje. Nie może dostarczyć wiążącego PASS.

### Człowiek

Człowiek pozostaje właścicielem:

- celu;
- kanonu;
- priorytetów;
- akceptacji ryzyka;
- merge;
- publikacji;
- produkcji;
- sekretów;
- usuwania danych.

## 4. Kontrakty

### PROJECT_CONTRACT.md

Project Contract opisuje trwałą tożsamość projektu. Musi zawierać:

```text
PROJECT_ID
PROJECT_GOAL
USER_VALUE
BOUNDARIES
SUCCESS_DEFINITION
FORBIDDEN_DIRECTIONS
DECISION_OWNER
CANONICAL_SOURCES
CLOSURE_CONDITIONS
```

Project Contract nie opisuje pojedynczej operacji.

### TASK CONTRACT

Task Contract opisuje jedną operację. Minimalne pola:

```text
TASK_ID
PROJECT_ID
REPOSITORY
BASE_SHA
GOAL
ALLOWED_SCOPE
FORBIDDEN_SCOPE
ACCEPTANCE_TEST
EXPECTED_OUTPUT
EVIDENCE_REQUIREMENTS
HUMAN_APPROVAL_BOUNDARY
```

Task Contract nie może zmienić Project Contract. Konflikt oznacza STOP i przejście przez Human Decision Gate.

## 5. Human Decision Gate

Formalna bramka jest obowiązkowa przed:

- zmianą celu;
- zmianą zakresu;
- zmianą architektury;
- zmianą priorytetu;
- zmianą Project Contract;
- odwieszeniem zamrożonego komponentu;
- zaakceptowaniem nowego istotnego ryzyka;
- zmianą System Invariants.

Przepływ:

```text
Executor wykrywa konflikt
        ↓
Ginseng przedstawia warianty i skutki
        ↓
Człowiek podejmuje decyzję
        ↓
Creative OS zapisuje decyzję
        ↓
Powstaje zmieniony kontrakt albo STOP
        ↓
Executor może kontynuować
```

Executor nie może kontynuować na podstawie własnej interpretacji decyzji.

## 6. Architektura wykonania

```text
Executor
    ↓
Reasoning Provider
    ↓
Tool Worker
    ↓
Execution Environment
```

Reasoning Provider może być modelem zewnętrznym, lokalnym albo narzędziem specjalistycznym. Tool Worker wykonuje konkretne operacje. Execution Environment zapewnia izolację. Kontrakt Executora pozostaje niezależny od dostawcy modelu.

## 7. Model zaufania P1

```text
TRUSTED CONTROLLER
        ↓
UNTRUSTED CANDIDATE EXECUTION
        ↓
TRUSTED AUTHORITATIVE VERIFIER
```

Trusted Controller ustanawia exact SHA, zakres i kontrakt. Candidate Execution nie ma prawa zmieniać kontrolera, verifiera ani kryteriów sukcesu. Authoritative Verifier działa poza przestrzenią kontrolowaną przez kandydata.

## 8. Minimalny niezależny ledger

P1 wymaga minimalnego ledgeru operacji poza kontrolą kandydata. To nie jest jeszcze Evidence Vault.

Minimalny wpis:

```text
EVENT_ID
TASK_ID
TIMESTAMP
OPERATION_TYPE
INPUT_SHA
RESULT_SHA
ENVIRONMENT_ID
ACTOR
PREVIOUS_EVENT_HASH
EVENT_HASH
RAW_EVIDENCE_HASHES
```

Wymagania:

- append-only;
- wykrywalne nadpisanie lub usunięcie;
- zapis przez zaufany komponent;
- możliwość replay bez pamięci procesu;
- action-result binding.

Evidence Vault może zostać zaprojektowany dopiero po co najmniej trzech prawdziwych runach.

## 9. Kolejność rozwoju

```text
P0 FOUNDATION
      ↓
P1 TRUSTED RUNTIME
      ↓
P2 AI WORKER
      ↓
P3A REAL USER VALUE
      ↓
P3B SAFE TECHNICAL EXECUTION
      ↓
P4 EXECUTOR 1.0
      ↓
GINSENG RUNTIME
      ↓
COMPANY LOOP
      ↓
PLATFORMA
      ↓
SAAS
```

Kolejność jest zamrożona.

## 10. Definicje poziomów

### P1 — Trusted Runtime

Executor potrafi udowodnić:

> Wykonałem dokładnie tę operację, na tym kodzie, w tym środowisku, zgodnie z kontraktem.

Warunki:

- PR #32 ACCEPT;
- PR #29 ACCEPT;
- exact SHA verification;
- niezależny ledger;
- raw evidence;
- action-result binding;
- replay bez pamięci procesu;
- autorytatywny verifier;
- formalny runtime decision packet;
- brak drogi do samopotwierdzenia.

### P2 — AI Worker

Pierwsze zadanie:

```text
jedna funkcja
jeden plik
jeden błąd
istniejący test regresyjny
```

Worker nie może zmieniać celu, rozszerzać zakresu, refaktoryzować „przy okazji” ani osłabiać kryterium sukcesu.

### P3A — Value Pilot

Projekt: Project Reconstructor.

Pytanie: czy system dostarcza realną wartość użytkownikowi?

### P3B — Execution Pilot

Projekt: ScriptOps albo mała rzeczywista zmiana kodowa.

Pytanie: czy Executor potrafi bezpiecznie wykonać realną pracę techniczną?

Pełne P3 ACCEPT wymaga obu bramek.

### P4 — Executor 1.0

Minimalny produkt:

```text
repo + kontrakt + zadanie + worker + test + evidence = draft PR
```

Cele 12-miesięczne:

- 20 prawdziwych zadań;
- co najmniej 50% redukcji pracy człowieka;
- większość PR zaakceptowana;
- FALSE SUCCESS = 0.

## 11. Werdykty

### ACCEPT

Dozwolony tylko, gdy kontrakt, exact SHA, zakres, środowisko, testy, evidence, replay i niezależność verifiera są potwierdzone.

ACCEPT nie oznacza automatycznego merge.

### REWORK

Kierunek jest poprawny, ale istnieje ograniczony, naprawialny blocker. Raport musi wskazać:

```text
BLOCKER
REQUIRED_CHANGE
ALLOWED_SCOPE
FORBIDDEN_SCOPE
RETEST_REQUIREMENT
```

### STOP

Wymagany, gdy cel jest niejasny, potrzebna jest decyzja biznesowa, kontrakt narusza kanon, nie można utworzyć niezależnej granicy dowodu albo dalsza praca utrwala błędną architekturę.

## 12. Polityka bezpieczeństwa

AI może bez dodatkowej zgody:

- utworzyć branch;
- zmienić zatwierdzone pliki;
- uruchomić testy;
- utworzyć commit;
- utworzyć draft PR;
- zebrać evidence;
- przygotować raport.

Zawsze wymaga decyzji człowieka:

- merge;
- publikacja;
- produkcja;
- sekrety;
- zmiana celu;
- zmiana kanonu;
- zmiana priorytetów;
- usuwanie danych;
- rozszerzenie zakresu.

## 13. Zakaz rozszerzeń przed P3

Zamrożone:

- Ginseng runtime;
- Company Loop;
- M3;
- panel;
- wieloagentowość;
- auto-merge;
- multi-repository execution;
- multi-provider framework;
- platforma;
- SaaS;
- Evidence Vault;
- automatyczny deployment.

Nie wolno dodawać abstrakcji, warstw ani frameworków uzasadnionych wyłącznie hipotetyczną przyszłą potrzebą. Obowiązuje `ARCH-001` z `SYSTEM_INVARIANTS.md`.

## 14. Definition of Ecosystem Working

Ekosystem działa, gdy:

1. użytkownik ustanawia cel;
2. cel zostaje zapisany jako decyzja kanoniczna;
3. istnieje zgodny Project Contract i Task Contract;
4. Executor wykonuje zadanie bez zmiany celu;
5. niezależny Verifier dostarcza odtwarzalny dowód;
6. powstaje draft PR;
7. człowiek wykonuje review;
8. powstaje RUN_REPORT.md;
9. użytkownik otrzymuje wynik i jeden następny krok;
10. nie występuje false success.

## 15. RUN_REPORT.md

Każdy run P3 i każdy run zaliczany do P4 musi zawierać:

- zadanie i kryterium sukcesu;
- koszt;
- czas procesu i człowieka;
- udział ręcznej implementacji;
- wynik testów;
- evidence i ledger entry;
- błędy;
- werdykt;
- następny krok.

## 16. Roadmapa 90 dni

### Dni 1–30

- zaimportować kanon do COS;
- ustanowić invariants, failure modes, status registry i decision register;
- zamknąć PR #32;
- zamknąć PR #29;
- wydać formalny P1 verdict.

### Dni 31–50

- wykonać jedno ograniczone zadanie P2;
- wygenerować zweryfikowany draft PR bez ręcznej implementacji rozwiązania.

### Dni 51–75

- wykonać P3A na Project Reconstructor;
- wykonać P3B na ScriptOps albo małej zmianie kodowej;
- utworzyć RUN_REPORT.md dla obu runów.

### Dni 76–90

- powtórzyć runy bez rozszerzania architektury;
- ocenić powtarzalność i gotowość do P4.

## 17. Aktualna decyzja wykonawcza

```text
ACTIVE PRIORITY: EXECUTOR P1
ARCHITECTURE: FROZEN
ALLOWED NEXT WORK: IMPLEMENTATION ONLY
```

Następna dozwolona sekwencja:

```text
1. Import governance do COS.
2. Zamknięcie PR #32.
3. Zamknięcie PR #29.
4. Formalny werdykt P1.
5. Dopiero potem P2.
```

## 18. Końcowa zasada

> Architektura ekosystemu jest wystarczająca do implementacji. Dalsze rozszerzanie jej przed przejściem P3 jest większym ryzykiem niż źródłem wartości.
