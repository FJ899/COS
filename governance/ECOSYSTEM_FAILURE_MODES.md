---
document: ECOSYSTEM_FAILURE_MODES
version: 1
status: CANONICAL
owner: USER
updated_at: 2026-08-04
---

# Ecosystem Failure Modes v1

Failure modes są elementem governance. Nie są listą luźnych ryzyk.

Każdy aktywny wpis powinien docelowo posiadać:

```text
FAILURE_MODE_ID
DESCRIPTION
DETECTION_SIGNAL
PREVENTION_CONTROL
VERIFICATION_EVIDENCE
ALLOWED_VERDICT
OWNER
STATUS
```

## FM-001 — LOCAL OPTIMIZATION DESTROYS GLOBAL INTENT

**Opis:** AI optymalizuje lokalne zadanie, ale wynik oddala projekt od celu globalnego.

**Sygnał:** Task Contract nie potrafi wskazać, jaki element Project Contract realizuje.

**Kontrola:** zgodność Project Contract → Task Contract oraz Human Decision Gate.

**Werdykt przy braku kontroli:** `STOP`.

## FM-002 — VERIFIER TRUSTS CANDIDATE-CONTROLLED EVIDENCE

**Opis:** Verifier ufa raportowi, artefaktowi, znacznikowi sukcesu albo testowi kontrolowanemu przez wykonawcę.

**Sygnał:** kandydat może zmienić finalny raport, test akceptacyjny lub źródło evidence.

**Kontrola:** trusted controller, untrusted execution, authoritative verifier i ledger poza przestrzenią kandydata.

**Werdykt:** `REWORK` albo `STOP`; nigdy `ACCEPT`.

## FM-003 — COS AND REPOSITORY STATE DIVERGE

**Opis:** Creative OS przechowuje stan sprzeczny ze stanem repozytorium lub aktywnym Project Contract.

**Sygnał:** status, SHA, następny krok albo źródło prawdy różnią się bez jawnej decyzji.

**Kontrola:** status registry, decision register i jawne rozstrzygnięcie konfliktu.

**Werdykt:** `REWORK` do czasu uzgodnienia stanu.

## FM-004 — CORRECT EXECUTION OF THE WRONG GOAL

**Opis:** Executor poprawnie wykonuje technicznie zadanie, którego nie powinien wykonywać.

**Sygnał:** testy przechodzą, ale zadanie narusza cel, granice albo zakazane kierunki projektu.

**Kontrola:** Project Contract, Task Contract i Human Decision Gate.

**Werdykt:** `STOP` niezależnie od jakości implementacji.

## FM-005 — EVIDENCE VOLUME PREVENTS REAL REVIEW

**Opis:** System generuje tak dużo evidence, że człowiek ani Verifier nie są w stanie realnie go przeanalizować.

**Sygnał:** brak indeksu, brak minimalnego pakietu decyzji albo dowód wymaga ręcznego czytania nieograniczonych logów.

**Kontrola:** runtime decision packet, indeks hashy i minimalny zestaw autorytatywnych faktów.

**Werdykt:** `REWORK`.

## FM-006 — TASK CONTRACT VIOLATES PROJECT CONTRACT

**Opis:** Pojedyncze zadanie jest technicznie poprawne, ale narusza granice projektu.

**Sygnał:** Task Contract zmienia cel, sukces projektu, zakazane kierunki albo właściciela decyzji.

**Kontrola:** `GOV-001`.

**Werdykt:** `STOP`.

## FM-007 — AI RECOMMENDATION RECORDED AS USER DECISION

**Opis:** Sugestia AI zostaje błędnie zapisana jako decyzja użytkownika i steruje dalszą pracą.

**Sygnał:** brak źródła jawnej decyzji albo wpis nie rozróżnia `AI_RECOMMENDATION` i `USER_DECISION`.

**Kontrola:** typed decision register i `INV-005`.

**Werdykt:** `REWORK`; skażone decyzje nie mogą sterować Executorem.

## FM-008 — ARCHITECTURE EXPANDS FOR A HYPOTHETICAL NEED

**Opis:** System otrzymuje nowe warstwy, abstrakcje lub frameworki bez zmierzonego problemu.

**Sygnał:** uzasadnienie używa wyłącznie „może kiedyś”, „na przyszłość” albo „żeby było skalowalne”.

**Kontrola:** `ARCH-001` i `INV-006`.

**Werdykt:** `STOP`.

## FM-009 — HUMAN WORK IS HIDDEN INSIDE AN AI SUCCESS

**Opis:** System deklaruje, że AI wykonało zadanie, mimo że rozwiązanie zostało faktycznie zaprojektowane lub napisane przez człowieka.

**Sygnał:** brak pomiaru udziału człowieka, gotowy patch przekazany workerowi albo ręczna poprawka nieuwzględniona w RUN_REPORT.

**Kontrola:** jawny pomiar human vs AI, zakaz ręcznej implementacji w runie P2/P3 i pełny RUN_REPORT.

**Werdykt:** run nie może być zaliczony do metryk P2–P4.

## FM-010 — REPEATABLE RESULT IN THE WRONG ENVIRONMENT

**Opis:** Wynik jest powtarzalny, ale został uzyskany w środowisku innym niż zatwierdzone przez kontrakt.

**Sygnał:** brak environment manifest albo hash środowiska nie zgadza się z kontraktem.

**Kontrola:** environment binding i niezależny replay.

**Werdykt:** `REWORK` albo `STOP`.

## FM-011 — AUTHORIZATION IS NOT BOUND TO THE RESULT

**Opis:** Istnieje autoryzacja operacji, ale nie można udowodnić, który wynik powstał z jej użycia.

**Sygnał:** brak `AUTHORIZATION_ID`, `RESULT_SHA` albo `EVIDENCE_ROOT_HASH` w jednym wiążącym rekordzie.

**Kontrola:** action-result binding i atomowe zużycie autoryzacji.

**Werdykt:** brak `ACCEPT`.

## FM-012 — CANDIDATE REUSES OR RACES AN AUTHORIZATION

**Opis:** Ten sam pakiet autoryzacji zostaje użyty więcej niż raz albo równolegle.

**Sygnał:** dwa wyniki odnoszą się do tego samego nieatomowo zużytego identyfikatora.

**Kontrola:** niezależny atomowy ledger zużycia.

**Werdykt:** `STOP` i unieważnienie wyników.

# Zasada dodawania failure mode

Nowy failure mode może zostać dodany, gdy:

1. wystąpił konkretny przypadek lub wiarygodny kontrprzykład;
2. istnieje obserwowalny sygnał;
3. można wskazać kontrolę albo jawnie oznaczyć jej brak;
4. wpis nie jest aliasem istniejącego failure mode.
