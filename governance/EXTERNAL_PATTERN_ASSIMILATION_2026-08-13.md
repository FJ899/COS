---
document: EXTERNAL_PATTERN_ASSIMILATION
version: 1
status: CANONICAL_DECISION_RECORD
updated_at: 2026-08-13
owner: USER
---

# External Pattern Assimilation — 2026-08-13

Ten rejestr zapisuje jawnie zatwierdzone decyzje dotyczące asymilacji wzorców zewnętrznych do Creative OS.

Zewnętrzne repozytorium jest `EVIDENCE`. Samo znalezienie wzorca nie czyni go częścią kanonu. Kanoniczna zmiana wynika wyłącznie z jawnej decyzji użytkownika.

```text
ARCHITECTURE CHANGE: NO
NEW COMPONENT: NO
NEW RUNTIME: NO
PRIORITY CHANGE: NO
GATE CHANGE: NO
GINSENG SEMANTICS CHANGE: NO
EXECUTOR CONTRACT CHANGE NOW: NO
```

Obowiązują bez zmian: `INV-001`–`INV-011`, `GIN-001`–`GIN-007`, `ARCH-001 — NO HYPOTHETICAL ARCHITECTURE`, `FALSE SUCCESS = 0` oraz priorytet `EXECUTOR P1`.

## EXT-001 — Progressive disclosure

- **PATTERN:** progressive disclosure / minimal relevant context
- **SOURCE:** `cathrynlavery/diagram-design`
- **DECISION:** `ADOPT_NOW`
- **WHAT WE ADOPT:** mały router / entrypoint oraz ładowanie szczegółowej wiedzy dopiero po ustaleniu konkretnego projektu i zadania.
- **WHAT IT REPLACES:** szerokie wyprzedzające ładowanie dokumentacji, która nie jest potrzebna do aktualnego zadania.
- **WHY:** mniejszy aktywny kontekst, mniej mieszania reguł, łatwiejsza identyfikacja źródła decyzji.
- **WHAT IT DOES NOT CHANGE:** hierarchii źródeł, obowiązkowego state owner, stop rules, wymaganych kontraktów ani architektury.
- **IMPLEMENTATION GATE:** none; dokumentacyjna reguła może obowiązywać teraz przy zachowaniu wszystkich obowiązkowych odczytów.
- **IMPLEMENTATION STATUS:** `IMPLEMENTED_IN_START_HERE_ON_THIS_BRANCH`

## EXT-002 — Complexity budget / deletion first

- **PATTERN:** przed dodaniem komponentu, warstwy lub abstrakcji sprawdź najpierw `DELETE → SIMPLIFY → SPLIT → REUSE EXISTING`.
- **SOURCE:** `cathrynlavery/diagram-design`
- **DECISION:** `ADAPT_EXISTING`
- **WHAT WE ADOPT:** deletion/simplification/reuse jako praktyczny test przed nową architekturą.
- **WHAT IT REPLACES:** odruch dodawania nowego komponentu jako pierwszego rozwiązania.
- **WHY:** ograniczenie złożoności i ryzyka hipotetycznej architektury.
- **WHAT IT DOES NOT CHANGE:** nie tworzy nowego invariantu; pozostaje interpretacją `ARCH-001 — NO HYPOTHETICAL ARCHITECTURE`.
- **IMPLEMENTATION GATE:** obowiązuje w bieżących decyzjach projektowych w ramach istniejących bramek.
- **IMPLEMENTATION STATUS:** `ADAPTED_TO_EXISTING_CANON`

## EXT-003 — Default value ≠ user decision

- **PATTERN:** wartość domyślna nie jest decyzją użytkownika.
- **SOURCE:** evidence z analizowanych wzorców zewnętrznych.
- **DECISION:** `REJECT_DUPLICATE`
- **WHAT WE ADOPT:** nic nowego.
- **WHAT IT REPLACES:** nic; zasada już istnieje.
- **WHY:** duplikacja osłabiłaby jednoznaczność kanonu.
- **WHAT IT DOES NOT CHANGE:** `INV-005` i Human Decision Gate pozostają jedynym obowiązującym mechanizmem dla tej zasady.
- **IMPLEMENTATION GATE:** none.
- **IMPLEMENTATION STATUS:** `REJECTED_AS_DUPLICATE`

## EXT-004 — Context Intermediate Representation

- **PATTERN:** `RAW / CHAOTIC CONTEXT → NORMALIZATION → MINIMAL EXECUTION REPRESENTATION`.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `ADAPT_WITHOUT_NEW_LAYER`
- **WHAT WE ADOPT:** zasadę normalizacji surowego kontekstu do minimalnej reprezentacji potrzebnej do wykonania.
- **WHAT IT REPLACES:** niekontrolowane przekazywanie szerokiego kontekstu bez normalizacji do granicy wykonawczej.
- **WHY:** istniejący przepływ już realizuje tę funkcję bez nowej warstwy.
- **WHAT IT DOES NOT CHANGE:** nie tworzy komponentu `Context-IR`; funkcję realizuje `Ginseng / COS → Project Contract → Task Contract → Executor`; architektura v1.1 pozostaje bez zmian.
- **IMPLEMENTATION GATE:** existing Project/Task Contract boundary; brak nowej bramki.
- **IMPLEMENTATION STATUS:** `ADAPTED_TO_EXISTING_BOUNDARY`

## EXT-005 — Source ≠ semantic knowledge atom

- **PATTERN:** jedno źródło może wspierać wiele niezależnych atomów semantycznych: `FACT`, `DECISION`, `HYPOTHESIS`, `RELATION`, `FUNCTION / CAPABILITY`.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `DEFER_UNTIL_EXECUTOR_P1_ACCEPT`
- **WHAT WE ADOPT:** po P1 przetestować rozdzielenie `SOURCE` od semantycznych atomów wiedzy w Ginseng Minimal Kernel.
- **WHAT IT REPLACES:** potencjalne utożsamianie źródła z pojedynczym atomem wiedzy.
- **WHY:** jedno źródło może wspierać wiele niezależnych twierdzeń i decyzji.
- **WHAT IT DOES NOT CHANGE:** obecnego modelu danych, semantyki `FACT / DECISION / HYPOTHESIS`, Decision Lineage ani architektury.
- **IMPLEMENTATION GATE:** `EXECUTOR P1 ACCEPT`.
- **IMPLEMENTATION STATUS:** `CANONICAL DECISION RECORDED / RUNTIME IMPLEMENTATION DEFERRED`

## EXT-006 — Retention analysis

- **PATTERN:** jawne ustalanie losu elementu wiedzy/decision pomiędzy wersjami: `FULLY_PRESERVED`, `PARTIALLY_PRESERVED`, `TRANSFERRED`, `DROPPED`, `SUPERSEDED`.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `DEFER_UNTIL_EXECUTOR_P1_ACCEPT`
- **WHAT WE ADOPT:** po P1 przetestować retention analysis jako przyszły widok nad `Decision Lineage`, `Version` i `Source`.
- **WHAT IT REPLACES:** brak jawnego widoku retencji pomiędzy wersjami.
- **WHY:** umożliwia audytowanie, co zostało zachowane, przeniesione, utracone lub zastąpione.
- **WHAT IT DOES NOT CHANGE:** nie tworzy nowego typu prawdy ani nowego źródła kanonu.
- **IMPLEMENTATION GATE:** `EXECUTOR P1 ACCEPT`.
- **IMPLEMENTATION STATUS:** `CANONICAL DECISION RECORDED / RUNTIME IMPLEMENTATION DEFERRED`

## EXT-007 — Latest-approved-version discipline

- **PATTERN:** zmiana zaakceptowanego upstream artifact, np. `A@3 → A@4`, wymaga oznaczenia zależnych downstream artifacts jako `STALE / REVALIDATION_REQUIRED` do ponownej walidacji.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `DEFER_UNTIL_EXECUTOR_P1_ACCEPT`
- **WHAT WE ADOPT:** po P1 przetestować jawne propagowanie stale/revalidation przy zmianie zatwierdzonej wersji upstream.
- **WHAT IT REPLACES:** ciche mieszanie starych i nowych wersji artefaktów.
- **WHY:** chroni spójność wersji i jawność zależności.
- **WHAT IT DOES NOT CHANGE:** obecnych bramek, modelu wersjonowania ani kontraktu Executora teraz.
- **IMPLEMENTATION GATE:** `EXECUTOR P1 ACCEPT`.
- **IMPLEMENTATION STATUS:** `CANONICAL DECISION RECORDED / RUNTIME IMPLEMENTATION DEFERRED`

## EXT-008 — State → Action → State

- **PATTERN:** `PRE_STATE → ACTION → POST_STATE → HANDOFF`.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `ADAPT_WHEN_REAL_BLOCKER_EXISTS`
- **WHAT WE ADOPT:** możliwość powrotu do formatu dla action-result binding, replay i continuity tylko wtedy, gdy P1/P2 ujawni konkretny blocker obecnego rozwiązania.
- **WHAT IT REPLACES:** nic teraz.
- **WHY:** wzorzec może być użyteczny, ale wdrożenie bez realnego problemu naruszałoby `ARCH-001`.
- **WHAT IT DOES NOT CHANGE:** kontraktu Executora, jego aktualnej implementacji ani priorytetu P1.
- **IMPLEMENTATION GATE:** realny, udokumentowany blocker w `P1/P2` + właściwa decyzja/gate.
- **IMPLEMENTATION STATUS:** `NOT_IMPLEMENTED / BLOCKER_REQUIRED`

## EXT-009 — Controlled fallback ladder

- **PATTERN:** fallback musi być jawny, ograniczony i audytowalny; brak sukcesu kończy się `REWORK`, `STOP` albo `Human Decision Gate`.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `ADAPT_EXISTING`
- **WHAT WE ADOPT:** kontrolowaną drabinę fallbacków jako interpretację istniejącej dyscypliny sukcesu.
- **WHAT IT REPLACES:** `ad-hoc retry` i `silent degradation`.
- **WHY:** kryterium nie może zostać obniżone po cichu, a wynik nadal nazwany sukcesem.
- **WHAT IT DOES NOT CHANGE:** nie tworzy frameworka fallbacków i nie zmienia kryteriów Executora; wzmacnia `FALSE SUCCESS = 0`.
- **IMPLEMENTATION GATE:** istniejące stop rules i Human Decision Gate.
- **IMPLEMENTATION STATUS:** `ADAPTED_TO_EXISTING_CANON / NO_NEW_FRAMEWORK`

## EXT-010 — Diagram runtime / visualization

- **PATTERN:** diagram runtime, graph UI, brand extraction, szeroki katalog diagramów, interaktywny panel.
- **SOURCE:** `cathrynlavery/diagram-design` oraz kontekst przyszłej wizualizacji Ginsenga.
- **DECISION:** `REJECT_SCOPE_NOW`
- **WHAT WE ADOPT:** nic teraz.
- **WHAT IT REPLACES:** nic.
- **WHY:** aktywnym priorytetem pozostaje Executor P1; wizualizacja Ginsenga jest zamrożona.
- **WHAT IT DOES NOT CHANGE:** Ginseng pozostaje `Decision Intelligence Layer`; jego runtime i wizualizacja pozostają zamrożone do pełnego P3 + Human Decision Gate.
- **IMPLEMENTATION GATE:** pełne `P3 ACCEPT` + `Human Decision Gate` dla Ginseng visualization.
- **IMPLEMENTATION STATUS:** `REJECTED_SCOPE_NOW`

## EXT-011 — H3 video-specific workflows

- **PATTERN:** shot tables, video model selection, storyboard pipelines i domenowe reguły animacji.
- **SOURCE:** `MiniMax-AI/MiniMax-H3`
- **DECISION:** `OUT_OF_SCOPE`
- **WHAT WE ADOPT:** nic do rdzenia COS/Executor/Ginseng.
- **WHAT IT REPLACES:** nic.
- **WHY:** to wartościowe evidence projektowe, ale dotyczy innej domeny.
- **WHAT IT DOES NOT CHANGE:** rdzenia COS, Executora, Ginsenga, architektury ani aktualnych priorytetów.
- **IMPLEMENTATION GATE:** none; poza zakresem tego systemowego PR.
- **IMPLEMENTATION STATUS:** `OUT_OF_SCOPE`

---

## Podsumowanie implementacyjne

### Wdrażamy teraz

- `EXT-001` — progressive disclosure w `START_HERE.md`.
- rejestr decyzji asymilacyjnych i `DEC-ECO-2026-022`.

### Adaptujemy do istniejącego kanonu

- `EXT-002` — complexity budget → `ARCH-001`.
- `EXT-003` — default value ≠ decision → `INV-005`, bez nowej zasady.
- `EXT-004` — Context-IR principle → istniejąca granica Project/Task Contract.
- `EXT-009` — controlled fallback → `FALSE SUCCESS = 0`.

### Odkładamy po Executor P1 ACCEPT

- `EXT-005` — Source vs semantic atom.
- `EXT-006` — retention analysis.
- `EXT-007` — latest-approved-version / STALE propagation.

### Tylko po realnym blockerze Executora

- `EXT-008` — State → Action → State.

### Odrzucamy teraz / poza zakresem

- `EXT-010` — diagram runtime i Ginseng visualization.
- external imports pozostają zamrożone zgodnie z istniejącym kanonem.
- `EXT-011` — H3 domain-specific video workflows.