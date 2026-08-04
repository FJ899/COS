---
document: SYSTEM_INVARIANTS
version: 1
status: CANONICAL
owner: USER
approved_at: 2026-08-04
change_gate: NEW_CANONICAL_USER_DECISION
---

# System Invariants v1

Invariants są zasadami nadrzędnymi ekosystemu. Nie mogą zostać zmienione przez kod, pojedynczy Task Contract, rekomendację AI, decyzję Executora ani historyczny dokument.

Zmiana invariantu wymaga jawnej decyzji użytkownika, Human Decision Gate i zapisu w `ECOSYSTEM_DECISION_REGISTER.md`.

## INV-001 — HUMAN OWNS THE GOAL

Człowiek jest właścicielem celu.

Żaden komponent systemu nie może samodzielnie ustanowić, zmienić ani zastąpić celu użytkownika.

## INV-002 — EXECUTOR EXECUTES, NOT DECIDES

Executor nie może zmienić celu. Wykonuje wyłącznie zatwierdzony kontrakt.

Konflikt, niejasność albo potrzeba rozszerzenia zakresu oznaczają zatrzymanie i Human Decision Gate.

## INV-003 — NO INDEPENDENT PROOF, NO ACCEPT

Brak niezależnego dowodu oznacza brak `ACCEPT`.

Deklaracja wykonawcy, kandydat kontrolujący plik `PASS`, lokalny raport albo kod wyjścia kontrolowany przez kandydata nie są niezależnym dowodem.

## INV-004 — CODE CANNOT OVERRIDE CANON

Kod nie może nadpisać kanonu.

Implementacja nie staje się decyzją tylko dlatego, że istnieje w repozytorium. W przypadku konfliktu pierwszeństwo ma najnowsza jawna decyzja użytkownika i aktywny kanon.

## INV-005 — AI RECOMMENDATION IS NOT A USER DECISION

Rekomendacja AI nie jest decyzją użytkownika.

Creative OS musi rozróżniać co najmniej:

```text
USER_DECISION
AI_RECOMMENDATION
HYPOTHESIS
EVIDENCE
OPEN_QUESTION
REJECTED_DIRECTION
```

## INV-006 — ARCHITECTURE CHANGE REQUIRES A MEASURED BLOCKER

Każda zmiana architektury musi usuwać konkretny, udokumentowany i zmierzony blocker.

Nie wolno zmieniać architektury wyłącznie dlatego, że nowa warstwa może być potrzebna w przyszłości.

## INV-007 — FALSE SUCCESS = 0

Najważniejszą metryką ekosystemu jest:

```text
FALSE SUCCESS = 0
```

Brak wystarczającego prawa lub dowodu oznacza `REWORK` albo `STOP`, nigdy domyślny sukces.

## INV-008 — DECISION TRUTH MUST BE TYPED

Twierdzenia używane do sterowania projektem albo analizy wpływu muszą pozostać rozdzielone jako:

```text
FACT
DECISION
HYPOTHESIS
```

Hipoteza, analiza AI lub rekomendacja nie mogą zostać automatycznie przedstawione jako fakt albo decyzja.

## INV-009 — AI CANNOT CONFIRM ITS OWN RELATION

AI może wykryć i zaproponować potencjalną relację. Nie może samodzielnie nadać jej statusu `CONFIRMED`.

Relacja proponowana przez AI musi pozostać `UNCONFIRMED` albo `AI_ESTIMATE` do czasu potwierdzenia przez autorytatywne źródło lub uprawnionego człowieka.

## INV-010 — IMPORTANT DECISIONS REQUIRE LINEAGE

Każda ważna decyzja musi zachować problem, przesłanki, rozważane opcje, wybraną opcję, powód wyboru, odrzucone alternatywy i oczekiwane konsekwencje.

Usunięcie tych danych jest utratą Decision Lineage, a nie neutralnym uproszczeniem dokumentacji.

## INV-011 — IMPACT MUST EXPLAIN FUNCTION

Istotny skutek nie może być wyjaśniony wyłącznie relacją pomiędzy obiektami.

Analiza musi pozwalać ustalić:

```text
ELEMENT
   ↓
FUNCTION / CAPABILITY
   ↓
EFFECT
```

Dla Ginsenga szczegółowe invariants `GIN-001`–`GIN-007` określa `GINSENG_DECISION_INTELLIGENCE_CONTRACT.md`.

# Governance Control Rules

## ARCH-001 — NO HYPOTHETICAL ARCHITECTURE

Nie wolno dodawać abstrakcji, warstw, frameworków, providerów, interfejsów, systemów wieloagentowych ani infrastruktury skalującej, jeżeli ich jedynym uzasadnieniem jest hipotetyczna przyszła potrzeba.

Dozwolony przebieg:

```text
realny problem
    ↓
udokumentowany przypadek
    ↓
pomiar skutków
    ↓
dowód, że obecna architektura nie wystarcza
    ↓
minimalna zmiana
    ↓
test potwierdzający usunięcie problemu
```

## GOV-001 — PROJECT CONTRACT PRECEDES TASK CONTRACT

Task Contract musi być zgodny z aktywnym Project Contract.

Task Contract nie może zmienić celu, granic, zakazanych kierunków, właściciela decyzji ani definicji sukcesu projektu.

## GOV-002 — HUMAN DECISION GATE

Human Decision Gate jest obowiązkowy przed zmianą celu, zakresu, architektury, priorytetu, Project Contract, system invariants albo statusu zamrożonego komponentu.

Executor nie może kontynuować na podstawie własnej interpretacji decyzji człowieka.

## GOV-003 — GINSENG ANALYZES, COS OWNS CANON

Ginseng analizuje powody, alternatywy, zależności, konsekwencje i niepewność.

Creative OS pozostaje właścicielem aktywnego kanonu, statusu projektu i zapisanych decyzji człowieka. Analiza Ginsenga może uruchomić Human Decision Gate, ale nie może sama zmienić kanonu.

# Kontrola zgodności

Każda propozycja zmiany powinna odpowiedzieć:

```text
1. Który blocker usuwa?
2. Którego invariantu dotyka?
3. Czy wymaga Human Decision Gate?
4. Jaki dowód potwierdzi rozwiązanie?
5. Czy tworzy drogę do false success?
6. Czy FACT, DECISION i HYPOTHESIS są rozdzielone?
7. Czy relacja AI pozostaje niepotwierdzona?
8. Czy ważna decyzja zachowuje lineage?
```
