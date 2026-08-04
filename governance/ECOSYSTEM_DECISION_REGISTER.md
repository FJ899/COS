---
document: ECOSYSTEM_DECISION_REGISTER
version: 1
status: CANONICAL
updated_at: 2026-08-04
owner: USER
---

# Ecosystem Decision Register

Rejestr przechowuje jawne decyzje użytkownika dotyczące całego ekosystemu.

Rekomendacja AI, hipoteza albo istniejąca implementacja nie są decyzją użytkownika.

## Typy wpisów

```text
USER_DECISION
AI_RECOMMENDATION
HYPOTHESIS
EVIDENCE
OPEN_QUESTION
REJECTED_DIRECTION
```

W tym rejestrze kanoniczne decyzje muszą mieć typ `USER_DECISION`.

---

## DEC-ECO-2026-001 — Misja ekosystemu

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** budujemy osobisty system operacyjny do bezpiecznej współpracy człowieka i AI; nie budujemy „firmy AI”.
- **Zakres:** cały ekosystem
- **Konsekwencje:** funkcje organizacyjne, platformowe i SaaS pozostają poza aktywnym zakresem.
- **Status wdrożenia:** `PARTIALLY_IMPLEMENTED`

## DEC-ECO-2026-002 — Podział odpowiedzialności

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** Ginseng chroni intencję, Creative OS przechowuje kanon, Executor wykonuje kontrakt, Verifier dostarcza niezależny dowód, a człowiek pozostaje właścicielem decyzji.
- **Nie zmienia:** lokalnych obowiązków repozytoriów projektowych.
- **Status wdrożenia:** `PENDING_IMPLEMENTATION`

## DEC-ECO-2026-003 — Kolejność rozwoju

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** obowiązuje kolejność `P0 → P1 → P2 → P3A → P3B → P4`; dopiero później Ginseng runtime, Company Loop, platforma i SaaS.
- **Konsekwencje:** nie rozpoczynać późniejszych poziomów przed formalnym werdyktem poziomu wcześniejszego.
- **Status wdrożenia:** `ACTIVE_RULE`

## DEC-ECO-2026-004 — Aktualny globalny priorytet

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** jedynym aktywnym priorytetem produktowym jest Executor P1.
- **Kolejność:** najpierw PR #32, następnie PR #29, potem formalny werdykt P1.
- **Konsekwencje:** nie budować nowych komponentów.
- **Status wdrożenia:** `ACTIVE`

## DEC-ECO-2026-005 — Definicja P1 ACCEPT

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** P1 oznacza, że Executor potrafi udowodnić wykonanie dokładnie wskazanej operacji na wskazanym kodzie i środowisku zgodnie z kontraktem.
- **Wymagania:** exact SHA, niezależny ledger, raw evidence, action-result binding, replay i brak samopotwierdzenia.
- **Status wdrożenia:** `BLOCKED`

## DEC-ECO-2026-006 — Project Contract i Task Contract

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** Project Contract opisuje projekt, a Task Contract pojedynczą operację. Task Contract nie może zmieniać Project Contract.
- **Konsekwencje:** konflikt wymaga Human Decision Gate albo STOP.
- **Status wdrożenia:** `CANONICAL_PENDING_RUNTIME_ENFORCEMENT`

## DEC-ECO-2026-007 — Human Decision Gate

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** zmiana celu, zakresu, architektury, priorytetu, ryzyka albo kanonu wymaga formalnej decyzji człowieka zapisanej w COS przed kontynuacją Executora.
- **Invariant:** Executor nie może kontynuować na podstawie własnej interpretacji decyzji.
- **Status wdrożenia:** `CANONICAL_PENDING_RUNTIME_ENFORCEMENT`

## DEC-ECO-2026-008 — Piloty P3

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** P3A zostanie przeprowadzone na Project Reconstructor, a P3B na ScriptOps albo małej rzeczywistej zmianie kodowej.
- **Konsekwencje:** pełne P3 ACCEPT wymaga wartości użytkowej i bezpiecznego wykonania technicznego.
- **Status wdrożenia:** `WAITING_FOR_P1_AND_P2`

## DEC-ECO-2026-009 — Ledger i Evidence Vault

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** P1 wymaga minimalnego niezależnego ledgeru. Evidence Vault nie może być budowany przed co najmniej trzema prawdziwymi runami.
- **Konsekwencje:** nie łączyć integralności historii operacji z przyszłym zarządzaniem dużą ilością evidence.
- **Status wdrożenia:** `LEDGER_BLOCKED / VAULT_FROZEN`

## DEC-ECO-2026-010 — Abstrakcja wykonania

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** rozdzielamy Executor, Reasoning Provider, Tool Worker i Execution Environment.
- **Konsekwencje:** architektura nie może zakładać jednego modelu AI, ale nie wolno teraz budować frameworku wielu providerów.
- **Status wdrożenia:** `CANONICAL / IMPLEMENTATION_DEFERRED_UNTIL_NEEDED`

## DEC-ECO-2026-011 — Zakaz hipotetycznej architektury

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** nie wolno dodawać abstrakcji, warstw ani frameworków uzasadnionych wyłącznie hipotetyczną przyszłą potrzebą.
- **Reguła:** `ARCH-001`
- **Status wdrożenia:** `ACTIVE_RULE`

## DEC-ECO-2026-012 — System Invariants v1

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** zatwierdzono `INV-001`–`INV-007` jako fundament systemu.
- **Zmiana:** wymaga nowej decyzji kanonicznej i Human Decision Gate.
- **Status wdrożenia:** `CANONICAL_PENDING_MERGE`

## DEC-ECO-2026-013 — Architektura zamrożona

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** po v1.1 dalsza dyskusja architektoniczna jest większym ryzykiem niż wartością. Dozwolona jest wyłącznie implementacja zatwierdzonej architektury.
- **Zamrożone:** Ginseng runtime, Company Loop, M3, panel, multi-agent, platforma, SaaS, Evidence Vault, auto-merge i multi-repository execution.
- **Status wdrożenia:** `ACTIVE_RULE`

## DEC-ECO-2026-014 — Rozdzielenie statusu kanonicznego i wdrożenia

- **Data:** 2026-08-04
- **Typ:** `USER_DECISION`
- **Decyzja:** zatwierdzenie dokumentu, import do COS i wdrożenie techniczne są niezależnymi stanami.
- **Konsekwencje:** `APPROVED_NOT_YET_IMPORTED` nie może być przedstawiane jako `IMPLEMENTED`.
- **Status wdrożenia:** `IMPLEMENTED_IN_GOVERNANCE_FILES_PENDING_MERGE`

---

# Format nowej decyzji

```markdown
## DEC-ECO-YYYY-NNN — Nazwa

- Data:
- Typ: USER_DECISION
- Decyzja:
- Właściciel:
- Powód:
- Zakres:
- Zastępuje:
- Nie zmienia:
- Konsekwencje:
- Status wdrożenia:
- Powiązane repozytoria:
- Powiązane PR:
```

# Reguła rozstrzygania konfliktów

W przypadku konfliktu obowiązuje:

1. najnowsza jawna decyzja użytkownika;
2. aktywny pakiet kanoniczny;
3. ten rejestr;
4. aktywny Project Contract;
5. aktywny Task Contract;
6. kod i dokumentacja implementacyjna;
7. starsze rozmowy i rekomendacje AI.
