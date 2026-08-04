---
document: GINSENG_DECISION_INTELLIGENCE_CONTRACT
version: 1
status: CANONICAL
owner: USER
approved_at: 2026-08-04
runtime_status: FROZEN
implementation_gate: EXECUTOR_P1_ACCEPT
supersedes_scope: NARROW_GINSENG_DESCRIPTION_IN_ECOSYSTEM_PACKAGE_SECTION_3
---

# Ginseng Decision Intelligence Contract v1

## 1. Zamrożona tożsamość

```text
GINSENG = DECISION INTELLIGENCE LAYER
```

Ginseng jest wersjonowanym systemem pamięci decyzji i analizy wpływu zmian.

Nie jest:

- zwykłym grafem zależności;
- mapą projektów;
- CMDB;
- dashboardem;
- narzędziem do wizualizacji dla samej wizualizacji;
- właścicielem kanonu;
- wykonawcą pracy.

Graf jest wyłącznie sposobem reprezentacji. Wartością Ginsenga jest odpowiedź na pytania:

```text
Dlaczego system wygląda tak, jak wygląda?
Które decyzje opierają się na tej przesłance?
Co zmieni się po usunięciu elementu lub funkcji?
Jakie konsekwencje są potwierdzone, a jakie tylko przewidywane?
Gdzie znajduje się największa niepewność?
Która zmiana wymaga Human Decision Gate?
```

## 2. Granica Ginseng — Creative OS

```text
CREATIVE OS
co jest prawdą, aktywne i kanoniczne dla projektu

GINSENG
z jakiego powodu ten stan istnieje i co stanie się po jego zmianie
```

Creative OS jest właścicielem kanonu, aktywnych decyzji, źródeł prawdy i statusu projektu.

Ginseng przechowuje i analizuje:

- decyzje;
- przesłanki;
- rozważane i odrzucone alternatywy;
- funkcje i capabilities;
- zależności;
- konsekwencje;
- niepewność;
- lineage zmian.

Ginseng nie może samodzielnie zmienić stanu kanonicznego w Creative OS. Wynik analizy może wywołać Human Decision Gate, ale nie zastępuje decyzji człowieka.

## 3. Trzy rodzaje prawdy

Każde twierdzenie istotne dla analizy musi być jawnie sklasyfikowane jako dokładnie jeden z typów:

```text
FACT
DECISION
HYPOTHESIS
```

### FACT

Fakt jest twierdzeniem opartym na wskazanym źródle lub zweryfikowanej obserwacji.

Minimalne pola:

```text
STATEMENT
SOURCE_ID
OBSERVED_AT
STATUS
```

Fakt bez źródła nie jest `CONFIRMED`.

### DECISION

Decyzja jest wyborem dokonanym przez uprawnionego właściciela decyzji.

Minimalne pola:

```text
DECISION_ID
DECISION_OWNER
DECISION_LINEAGE
DECIDED_AT
STATUS
```

Sugestia AI nie może zostać zapisana jako `DECISION` bez jawnego aktu człowieka.

### HYPOTHESIS

Hipoteza jest możliwym wyjaśnieniem, zależnością albo skutkiem, który nie został potwierdzony.

Minimalne pola:

```text
STATEMENT
PROPOSED_BY
SOURCE_OR_REASONING_REFERENCE
STATUS
```

Hipoteza wygenerowana przez AI pozostaje hipotezą aż do potwierdzenia przez człowieka albo autorytatywne źródło.

Nie wolno automatycznie promować:

```text
HYPOTHESIS → FACT
HYPOTHESIS → DECISION
AI_RECOMMENDATION → DECISION
```

## 4. FUNCTION / CAPABILITY jako typ semantyczny

Ginseng nie może ograniczać modelu do relacji pomiędzy rzeczami.

Kanoniczny łańcuch analizy wpływu:

```text
ELEMENT
   ↓
FUNCTION / CAPABILITY
   ↓
EFFECT
```

Przykłady:

```text
Dział Obsługi Klienta
   ↓
obsługa reklamacji
   ↓
utrzymanie SLA

Smartwatch
   ↓
nagrywanie dowodu
   ↓
ujawnienie prawdy w finale

Biblioteka auth
   ↓
uwierzytelnianie użytkownika
   ↓
dostęp do panelu
```

Relacja obiektowa `A DEPENDS_ON B` jest niewystarczająca, gdy nie wyjaśnia funkcji, dzięki której powstaje skutek.

Nie każda relacja musi posiadać osobny węzeł funkcji. Jednak każdy skutek uznany za istotny musi pozwalać ustalić:

```text
który element
realizuje jaką funkcję
prowadzącą do jakiego efektu
```

## 5. Decision Lineage

Każda ważna decyzja musi zachować odpowiedź na pytanie: „dlaczego ta decyzja istnieje?”.

Minimalny zapis:

```text
DECISION_ID
PROBLEM
PREMISES
CONSIDERED_OPTIONS
SELECTED_OPTION
SELECTION_REASON
REJECTED_OPTIONS
REJECTION_REASONS
EXPECTED_CONSEQUENCES
DECISION_OWNER
DECIDED_AT
SOURCE_REFERENCES
SUPERSEDES
SUPERSEDED_BY
STATUS
```

Usunięcie uzasadnienia, alternatyw lub przesłanek nie jest porządkowaniem danych. Jest utratą lineage decyzji.

## 6. Autorytet relacji

Ginseng i AI mogą wykryć potencjalną relację. Nie mogą samodzielnie ogłosić jej potwierdzoną.

Relacja musi posiadać co najmniej:

```text
RELATION_TYPE
SOURCE_ID
PROPOSED_BY
CONFIDENCE
STATUS
```

Dozwolone statusy semantyczne:

```text
CONFIRMED
UNCONFIRMED
AI_ESTIMATE
REJECTED
SUPERSEDED
```

Relacja proponowana przez AI musi przyjąć formę niewiążącą, na przykład:

```text
POSSIBLY_DEPENDS_ON
POSSIBLY_IMPACTS
POSSIBLY_ENABLES

PROPOSED_BY: AI
STATUS: UNCONFIRMED albo AI_ESTIMATE
```

Promocja do `CONFIRMED` wymaga:

- autorytatywnego źródła; albo
- jawnego potwierdzenia człowieka posiadającego prawo do decyzji.

Sama liczba `confidence` nie nadaje relacji autorytetu.

## 7. Zasada pytania przed grafem

Ginseng nie powinien generować pełnej mapy bez pytania analitycznego.

Dobre wejścia:

```text
Co stanie się, jeśli usuniemy ten element?
Które decyzje zależą od tej przesłanki?
Które funkcje są krytyczne dla tego efektu?
Gdzie mamy największą niepewność?
Która zmiana naruszy fundament lub kanon?
```

Słabe wejście:

```text
Pokaż wszystkie zależności.
```

Pełny graf bez pytania jest materiałem pomocniczym, nie wynikiem analizy.

## 8. Invariants Ginseng v1

### GIN-001 — DECISION INTELLIGENCE, NOT GRAPH PRODUCT

Ginseng jest warstwą inteligencji decyzji. Graf jest reprezentacją, nie definicją produktu.

### GIN-002 — TRUTH TYPES NEVER MIX

`FACT`, `DECISION` i `HYPOTHESIS` muszą pozostać rozdzielone w danych, analizie i prezentacji.

### GIN-003 — IMPORTANT DECISIONS REQUIRE LINEAGE

Ważna decyzja bez przesłanek, alternatyw, uzasadnienia i konsekwencji jest niekompletna.

### GIN-004 — AI CANNOT CONFIRM ITS OWN RELATION

Relacja wykryta przez AI pozostaje niepotwierdzona, dopóki nie potwierdzi jej człowiek albo autorytatywne źródło.

### GIN-005 — IMPACT MUST EXPLAIN FUNCTION

Istotny skutek musi być powiązany z funkcją lub capability, która go powoduje.

### GIN-006 — QUESTION PRECEDES MAP

Mapa bez pytania analitycznego nie może zostać przedstawiona jako wartościowy wynik Ginsenga.

### GIN-007 — COS OWNS CANON

Ginseng analizuje powody i wpływ zmian. Creative OS pozostaje właścicielem tego, co jest kanonicznie prawdą.

## 9. Minimalny zakres kanoniczny teraz

Przed zamknięciem pakietu v1.1 zamrożone zostają wyłącznie:

- formalna rola `Decision Intelligence Layer`;
- granica Ginseng — Creative OS;
- `FUNCTION / CAPABILITY` jako typ semantyczny;
- rozdzielenie `FACT / DECISION / HYPOTHESIS`;
- Decision Lineage;
- zakaz automatycznego potwierdzania relacji przez AI;
- invariants `GIN-001`–`GIN-007`.

To jest definicja i kontrakt. Nie jest to implementacja runtime.

## 10. Praca odłożona

### Dopiero po Executor P1 ACCEPT

Dozwolone będzie zdefiniowanie i przetestowanie:

```text
GINSENG MINIMAL KERNEL
Node
Relation
Source
Decision
Version
Scenario
Impact
Confidence
```

oraz:

- `Impact Class` 0–5;
- formalnego modelu confidence i uncertainty budget;
- trzeciego testu: Creative OS / ecosystem self-test;
- zapytań impact analysis działających na minimalnym kernelu.

### Dopiero po pełnym P3 ACCEPT

Dozwolone będą:

- wizualizacja;
- wielowariantowe scenariusze;
- import zewnętrzny;
- interaktywny graf;
- szersze zastosowania organizacyjne.

## 11. Zakaz implementacyjny

Do czasu przejścia wymaganych bramek nie wolno:

- budować runtime Ginseng;
- tworzyć interfejsu wizualnego;
- projektować platformy grafowej;
- dodawać importów CMDB lub systemów firmowych;
- uruchamiać automatycznego zapisu relacji;
- przedstawiać kontraktu danych jako działającego produktu.

Aktualny priorytet pozostaje bez zmian:

```text
EXECUTOR P1
PR #32
PR #29
FORMAL P1 VERDICT
```
