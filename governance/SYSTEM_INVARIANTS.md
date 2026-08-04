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

# Kontrola zgodności

Każda propozycja zmiany powinna odpowiedzieć:

```text
1. Który blocker usuwa?
2. Którego invariantu dotyka?
3. Czy wymaga Human Decision Gate?
4. Jaki dowód potwierdzi rozwiązanie?
5. Czy tworzy drogę do false success?
```
