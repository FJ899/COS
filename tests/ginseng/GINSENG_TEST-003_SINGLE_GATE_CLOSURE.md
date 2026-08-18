---
test_id: "GINSENG_TEST-003"
status: "EXECUTED / INDEPENDENTLY_VERIFIED_PASS"
project: "Ginseng — scenario impact engine"
test_type: "SINGLE_GATE_CLOSURE / REGRESSION"
baseline: "BASELINE_2026_07"
source_result: "GINSENG_TEST_2_S001_RESULT_v1_1.zip"
method_pilot: "selected Superpowers patterns"
executed_at: "2026-08-18"
result_record: "tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md"
---

# GINSENG TEST-003 — zamknięcie jednej bramki bez efektów ubocznych

## 1. Po co wykonujemy ten test

Test 2 potwierdził, że Ginseng potrafi:

- zachować niezmieniony baseline;
- wykryć skutki bezpośrednie i pośrednie;
- udowodnić `NO_IMPACT`;
- wykryć konflikt `ACT002 ↔ DEC002`;
- zatrzymać wdrożenie na siedmiu bramkach.

Nie wiemy jeszcze, czy po podjęciu jednej decyzji system potrafi przeliczyć scenariusz **lokalnie**, zamknąć dokładnie właściwą bramkę i nie zmienić pozostałych wyników bez podstawy. To jest najważniejsza cecha do sprawdzenia przed rozwijaniem interfejsu, automatyzacji albo kolejnych scenariuszy.

## 2. Hipoteza

Po formalnym rozstrzygnięciu jednej bramki Ginseng:

1. zamknie dokładnie tę bramkę;
2. zaktualizuje tylko zależne wpływy i ścieżki;
3. pozostawi pozostałe sześć bramek bez zmian;
4. nie zmieni baseline;
5. zachowa pełną identyfikowalność źródeł;
6. nie podniesie gotowości wdrożeniowej do `READY`, dopóki istnieją inne blokady.

## 3. Wybrana bramka

Pierwszy wariant testowy dotyczy konfliktu:

```text
ACT002
→ przeniesienie właściciela reklamacji

DEC002
→ właściciel procesu reklamacji pozostaje w Obsłudze Klienta
```

### Decyzja testowa

Zastosować jeden z dwóch wariantów, ale nie oba jednocześnie:

- `VARIANT_A_KEEP_DEC002` — zachować `DEC002` i wyodrębnioną funkcję Obsługi Klienta z rolą `R003` w nowej jednostce;
- `VARIANT_B_SUPERSEDE_DEC002` — dodać formalną decyzję zastępującą `DEC002` i przenoszącą odpowiedzialność do nowej roli.

Domyślnym wariantem pierwszego uruchomienia jest `VARIANT_A_KEEP_DEC002`, ponieważ nie wymaga zmiany zatwierdzonej decyzji bazowej.

## 4. Metoda — pilot wybranych elementów Superpowers

Nie instalujemy całego frameworka jako globalnej architektury. Test wykorzystuje tylko cztery wzorce:

1. **writing-plans** — przed zmianą zapisać oczekiwany zakres delty;
2. **test-driven-development** — najpierw zapisać warunki, które obecny wynik ma nie spełniać, a wynik po decyzji ma spełniać;
3. **systematic-debugging** — przy rozjeździe znaleźć pierwszą błędną zależność zamiast dopisywać wyjątki;
4. **verification-before-completion** — nie ogłaszać sukcesu bez porównania artefaktów przed i po.

Celem pilota jest sprawdzenie, czy te wzorce poprawiają rzetelność pracy Ginseng bez tworzenia nowej warstwy zarządzania.

## 5. Przygotowanie

Wejście:

- oryginalny pakiet blind input testu 2;
- poprawiony pakiet wynikowy `GINSENG_TEST_2_S001_RESULT_v1_1.zip`;
- `S001_test2_source_index.json`;
- decyzja testowa dla jednej bramki;
- kopia baseline `BASELINE_2026_07` z potwierdzonym SHA-256.

Przed zmianą zapisać:

```text
analysis_verdict_before: CONDITIONAL_GO
implementation_readiness_before: BLOCKED
blocking_gate_count_before: 7
baseline_mutated_before: false
```

## 6. Kroki testu

1. Utworzyć nowy logiczny overlay pochodny od S001; nie zmieniać istniejącego overlayu testu 2.
2. Dodać wyłącznie jedną decyzję testową dotyczącą `R003 / P002 / DEC002`.
3. Przeliczyć pełny graf wpływu od początku, bez ręcznego usuwania wpisu z listy bramek.
4. Wygenerować nowy wynik, raport, overlay, evidence i indeks źródeł.
5. Porównać wynik z testem 2 na poziomie:
   - bramek;
   - 36 wpływów;
   - ścieżek zależności;
   - poziomów wpływu;
   - źródeł;
   - `NO_IMPACT`;
   - baseline;
   - hashy artefaktów.
6. Wskazać każdą zmianę inną niż oczekiwana i podać jej ścieżkę przyczynową.
7. Nie podejmować żadnej z pozostałych sześciu decyzji.

## 7. Kryteria PASS

Test otrzymuje `PASS`, gdy łącznie:

- konflikt `ACT002 ↔ DEC002` jest rozstrzygnięty zgodnie z wybranym wariantem;
- `blocking_gate_count_after = 6`;
- bramka reklamacji zmienia status z `BLOCKING` na `RESOLVED` albo znika z aktywnych blokad z jawnym śladem decyzji;
- pozostałe sześć bramek zachowuje status i treść semantyczną;
- `implementation_readiness_after = BLOCKED`;
- `analysis_verdict_after` pozostaje uzasadniony źródłami;
- `baseline_mutated_after = false`;
- pięć kontroli `NO_IMPACT` pozostaje niezmienionych, o ile nowa decyzja nie tworzy jawnej ścieżki wpływu;
- każdy zmieniony wpływ ma ścieżkę prowadzącą do decyzji testowej;
- indeks źródeł pozostaje kompletny;
- ZIP i JSON przechodzą walidację integralności;
- raport odróżnia logiczny overlay od fizycznego brancha Git.

## 8. Kryteria FAIL

Test otrzymuje `FAIL`, gdy wystąpi choć jeden przypadek:

- zamknięto więcej niż jedną bramkę bez nowej decyzji;
- zniknęła blokada niepowiązana z `R003 / P002 / DEC002`;
- baseline został zmieniony;
- system uznał scenariusz za gotowy do wdrożenia przy sześciu otwartych bramkach;
- zmieniono `NO_IMPACT` bez wykazanej ścieżki;
- wynik został poprawiony ręcznie zamiast przez ponowne przeliczenie;
- źródło lub decyzja nie ma identyfikatora;
- artefakty przed i po nie pozwalają odtworzyć delty.

## 9. Wynik częściowy

`PASS WITH FIXES` jest dozwolony tylko wtedy, gdy logika bramki jest poprawna, baseline pozostaje nienaruszony, a problem dotyczy wyłącznie formatu, nazewnictwa lub kompletności raportu.

## 10. Oczekiwane artefakty

```text
GINSENG_TEST_3_S001_GATE_RESULT.zip
S001_gate_closure_report.md
S001_gate_closure_result.json
S001_gate_closure_overlay.json
S001_gate_closure_evidence.json
S001_gate_closure_source_index.json
S001_gate_closure_delta.json
```

`S001_gate_closure_delta.json` ma zawierać listę pól i wpływów zmienionych względem testu 2 wraz z przyczyną.

## 11. Poza zakresem

Ten test nie:

- aktywuje Ginseng jako formalnego projektu w tabeli Creative OS;
- buduje frontendu;
- instaluje pełnego Superpowers;
- rozstrzyga pozostałych sześciu bramek;
- modyfikuje baseline;
- bada wydajności na dużej organizacji;
- porównuje wielu modeli AI.

## 12. Decyzja po teście

- `PASS` — przejść do testu drugiej, innego typu bramki, najlepiej SoD/RODO;
- `PASS WITH FIXES` — wykonać jedną małą korektę kontraktu wyniku i powtórzyć;
- `FAIL` — zatrzymać rozwój interfejsu i automatyzacji, znaleźć pierwszą błędną zależność w grafie.
