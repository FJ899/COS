---
document: ECOSYSTEM_STATUS_REGISTRY
version: 1
status: CANONICAL
updated_at: 2026-08-04
owner: CREATIVE_OS
---

# Ecosystem Status Registry

Ten plik jest kanonicznym źródłem statusów wysokiego poziomu ekosystemu.

Nie zastępuje lokalnych `PROJECT_STATE.md`, backlogów ani statusów pojedynczych PR. Przechowuje wyłącznie rolę projektu, poziom, aktywny blocker, jeden następny krok i lokalne źródło prawdy.

## Statusy dokumentów

```text
DRAFT
REWORK
APPROVED
CANONICAL
SUPERSEDED
```

## Statusy wdrożenia

```text
NOT_STARTED
PENDING_IMPLEMENTATION
PARTIALLY_IMPLEMENTED
IMPLEMENTED
VERIFIED
```

## Statusy relacji z COS

```text
NOT_APPROVED
APPROVED_NOT_YET_IMPORTED
IMPORTED
ACTIVE_CANON
ARCHIVED
```

Status kanoniczny i status wdrożenia są niezależne. Dokument zatwierdzony, ale niewdrożony, nie może być przedstawiany jako `IMPLEMENTED`.

# Stan ekosystemu

## Executor

- **Repozytorium:** `litrgratis-pixel/Executor`
- **Rola:** kontrolowane wykonanie, izolacja, evidence, draft PR
- **Poziom:** `P0 → P1`
- **Status:** `ACTIVE / P1 BLOCKED`
- **Aktualny blocker:** brak ukończonej niezależnej granicy dowodu i powtarzalnego exact-SHA runtime
- **Aktywne bramki:** PR #32 i PR #29
- **Następny krok:** zamknąć najpierw PR #32, następnie ponownie zweryfikować PR #29
- **Zakazane rozszerzenia:** P2, M3, auto-merge, panel, multi-agent, platforma
- **Źródło prawdy:** repo `litrgratis-pixel/Executor`, dokumenty produktu i aktywne PR

## Creative OS

- **Repozytorium:** `litrgratis-pixel/COS`
- **Rola:** pamięć i konstytucja — określa, co jest prawdą, aktywne i kanoniczne dla projektu
- **Poziom:** `GOVERNANCE`
- **Status:** `ACTIVE / CANON IMPORT IN PROGRESS`
- **Aktualny blocker:** zatwierdzony pakiet v1.1 nie znajduje się jeszcze na `main`, a aktywny entrypoint nadal wskazuje starszy handoff
- **Następny krok:** review, minimalna aktualizacja entrypointu i merge governance PR po potwierdzeniu zgodności
- **Granica z Ginseng:** COS przechowuje kanon; Ginseng wyjaśnia powody, alternatywy i wpływ potencjalnych zmian
- **Źródło prawdy:** `CREATIVE_OS.md` oraz katalog `governance/` po merge

## Project Reconstructor

- **Repozytorium:** `litrgratis-pixel/creative-os-project-reconstructor`
- **Rola:** pierwszy pilot wartości
- **Poziom:** `P3A TARGET`
- **Status:** `WAITING FOR P1 AND P2`
- **Aktualny blocker:** Executor nie przeszedł P1 i nie wykonał pierwszego zadania P2
- **Następny krok:** po P2 wybrać jeden ograniczony realny problem i przygotować Project Contract oraz Task Contract
- **Źródło prawdy:** lokalny `PROJECT_STATE.md`

## ScriptOps

- **Repozytorium:** `litrgratis-pixel/scriptops`
- **Rola:** pierwszy pilot bezpiecznego wykonania technicznego
- **Poziom:** `P3B TARGET`
- **Status:** `FROZEN / WAITING FOR P3A`
- **Aktualny blocker:** brak ukończonych P1, P2 i P3A
- **Następny krok:** nie rozwijać; po P3A wybrać małą rzeczywistą zmianę kodową
- **Źródło prawdy:** lokalny `PROJECT_STATE.md`

## Executor Pilot Target

- **Repozytorium:** `litrgratis-pixel/executor-pilot-target`
- **Rola:** fixture i cel testów runtime
- **Poziom:** `P1 FIXTURE`
- **Status:** `ACTIVE AS FIXTURE / PRODUCT DEVELOPMENT FORBIDDEN`
- **Aktualny blocker:** nie dotyczy — repo nie jest produktem
- **Następny krok:** używać wyłącznie do testów P1
- **Źródło prawdy:** repo i kontrakty testów Executora

## Ginseng

- **Formalna rola:** `DECISION INTELLIGENCE LAYER`
- **Definicja wartości:** wersjonowana pamięć decyzji i analiza wpływu zmian; nie graf jako produkt
- **Odpowiedzialność:** wyjaśnia dlaczego stan istnieje, jakie były alternatywy, jakie funkcje tworzą skutki i co może zmienić się po naruszeniu przesłanki
- **Kanoniczne typy semantyczne:** `FACT`, `DECISION`, `HYPOTHESIS`, `FUNCTION / CAPABILITY`, Decision Lineage i niepotwierdzone relacje AI
- **Poziom:** `CANONICAL SEMANTICS NOW / KERNEL AFTER P1 / RUNTIME AFTER P3`
- **Status:** `STRATEGICALLY PRIMARY / CONTRACT CANONICAL_PENDING_MERGE / RUNTIME FROZEN`
- **Aktualny blocker:** Executor nie uzyskał P1 ACCEPT
- **Następny dozwolony krok po P1:** zdefiniować Minimal Kernel, Impact Class, confidence/uncertainty model i Creative OS self-test; bez wizualizacji
- **Warunek runtime:** pełne P3A i P3B oraz jawna decyzja użytkownika
- **Zakazane teraz:** implementacja runtime, wizualizacja, import zewnętrzny, automatyczne potwierdzanie relacji
- **Źródło prawdy:** `GINSENG_DECISION_INTELLIGENCE_CONTRACT.md`

## Company Loop

- **Rola:** potencjalna przyszła pętla organizacyjna
- **Poziom:** `POST-P4 CANDIDATE`
- **Status:** `FROZEN`
- **Warunek powrotu:** dowód potrzeby wynikający z realnych runów
- **Następny krok:** brak pracy

## M3

- **Rola:** potencjalny późniejszy poziom dojrzałości
- **Status:** `FROZEN`
- **Warunek powrotu:** zmierzony blocker niemożliwy do usunięcia w P1–P4
- **Następny krok:** brak pracy

## Panel, platforma i SaaS

- **Status:** `FROZEN`
- **Warunek powrotu:** ukończone P4 i osobny Human Decision Gate
- **Następny krok:** brak pracy

# Aktualny globalny priorytet

```text
PRIORITY: EXECUTOR P1
FIRST BLOCKER: PR #32
SECOND BLOCKER: PR #29
GINSENG: CONTRACT ONLY / RUNTIME FROZEN
ARCHITECTURE: FROZEN
ALLOWED WORK: IMPLEMENTATION ONLY
FALSE SUCCESS TARGET: 0
```

# Reguła aktualizacji

Wpis aktualizuje się wyłącznie, gdy zmienił się co najmniej jeden element:

- poziom;
- status;
- aktywny blocker;
- jeden następny krok;
- lokalne źródło prawdy;
- jawna decyzja użytkownika.
