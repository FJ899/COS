---
protocol: cognitive-os-v0
artifact: pilot_metrics
version: 0.1
status: active
last_updated: 2026-07-23
---

# METRYKI PILOTA

Celem metryk jest wykrycie, czy protokół zmienia jakość pracy, a nie udowodnienie z góry, że COS działa.

## 1. Baseline

| Metryka | Baseline | Źródło | Pewność |
|---|---:|---|---|
| czas odzyskania kontekstu bez COS | UNKNOWN | brak pomiaru historycznego | low |
| liczba reopenów bez nowych danych | co najmniej kilka w `AUD-2026-001`; dokładna normalizacja jeszcze nieustalona | audyt rozmowy 4-AI | medium |
| liczba semantycznych duplikatów pomysłów | wysoka w `AUD-2026-001`; klastry HRM/routing/debate i self-heal/meta-loop | audyt rozmowy 4-AI | medium |
| czas administracyjny protokołu | UNKNOWN | pierwsze dwie sesje nie były mierzone zegarem | low |
| false pass | co najmniej dwa ważne wzorce: mock jako funkcja i analiza kodu bez kodu | `AUD-2026-001` | high |
| false stop | 0 potwierdzonych; ryzyka w obu audytach | audyty 001–002 | low |

Baseline retrospektywny jest niepełny. Od następnej sesji należy mierzyć czas rzeczywisty.

## 2. Metryki pojedynczego audytu

| Pole | Definicja |
|---|---|
| `bootstrap_minutes` | czas od rozpoczęcia do poprawnego `BOOT_ACK` |
| `analysis_minutes` | czas analizy materiału, bez zmian repo |
| `protocol_minutes` | czas klasyfikacji, closera, aktualizacji plików i walidacji |
| `source_coverage` | full / partial / metadata_only / summary_only |
| `explicit_decisions` | jawne decyzje użytkownika |
| `pseudo_decisions` | rekomendacje lub twierdzenia AI brzmiące jak decyzje/fakty |
| `semantic_reopens` | powrót zamkniętego kierunku pod tą samą lub inną nazwą bez nowych danych |
| `idea_aliases` | liczba nazw należących do istniejącego klastra pomysłów |
| `false_pass` | zgoda lub claim przepuszczony przed dowodem, wykryty później |
| `false_stop` | zatrzymanie, które nie zmniejszyło ryzyka ani kosztu |
| `parked` | pomysły zachowane bez zmiany aktywnego celu |
| `accepted_changes` | propozycje zatwierdzone do stanu |
| `rejected_changes` | propozycje jawnie odrzucone |
| `protocol_changes` | liczba zmian samego COS po sesji |
| `resume_minutes_next_session` | czas wznowienia przy następnym użyciu handoffu |

## 3. Dziennik wyników

| Sesja | Audyt | Bootstrap min | Analiza min | Protokół min | Decyzje | Pseudo-decyzje / reguły normatywne | Reopeny | False pass | False stop | Zaparkowane | Zmiany COS | Uwagi |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| SES-2026-07-23-001 | AUD-2026-001 | UNKNOWN | UNKNOWN | UNKNOWN | 6–7 historycznych | 10+ | 6+ | 2 kluczowe | UNKNOWN | 12 klastrów/kandydatów | 0 podczas audytu; konfiguracja pilota po decyzji użytkownika | pierwsza sesja daje jakościowy baseline, ale nie pozwala ocenić kosztu czasowego |
| SES-2026-07-23-002 | AUD-2026-002 | UNKNOWN | UNKNOWN | UNKNOWN | nieustalone | 15 reguł przedstawionych jako obowiązujące | 1 klaster / 5 nazw | 0 potwierdzonych | 0 potwierdzonych; 4 ryzyka | 7 kandydatów, 0 formalnych | 0 zmian protokołu; tylko logowanie postępu | krótsza rozmowa na podobny temat; szybka formalizacja pełnego systemu bez pomiaru kosztu |

## 4. Wstępne porównanie po dwóch audytach

### Wzorzec wspólny

Obie rozmowy przekształciły potrzebę uporządkowania pracy z AI w szeroki system przed pomiarem prostszej alternatywy.

### Różnica przebiegu

- `AUD-2026-001`: stopniowy scope creep w wielu rundach, kod i overclaimy techniczne;
- `AUD-2026-002`: skompresowany scope creep w szybko sformalizowanym systemie normatywnym.

### Wniosek tymczasowy

Długość rozmowy nie chroni przed nadmiarem. Krótka rozmowa może szybko wygenerować elegancki, lecz niezweryfikowany system o wysokim koszcie proceduralnym.

Nie jest to jeszcze checkpoint. Potrzebny jest trzeci przypadek z innej domeny.

## 5. Checkpointy

### Po 3 audytach

- sprawdź, które awarie powtarzają się w co najmniej dwóch rozmowach;
- usuń propozycje oparte wyłącznie na jednym nietypowym przypadku;
- oceń średni koszt protokołu;
- rozstrzygnij, czy lekka karta wejściowa wnosi wartość;
- nie zmieniaj jeszcze statusu na wersję końcową.

### Po 6 audytach lub sesjach

- wybierz reguły rdzeniowe i kandydatów do usunięcia;
- sprawdź rozmowy dobre i złe, krótkie i długie;
- oceń, czy raporty umożliwiają bootstrap bez instrukcji zewnętrznej;
- przygotuj wersję `v1-rc` jako propozycję.

### Po 10 sesjach

- porównaj z baseline;
- wykonaj decyzję `GO`, `SIMPLIFY`, `STOP` albo `EXTEND_PILOT`;
- zatwierdź najwyżej jedną warstwę automatyzacji do kolejnego etapu;
- zamknij albo superseduj aktywne decyzje pilota.

## 6. Ochrona przed Goodhartem

- większa liczba wykrytych błędów nie oznacza automatycznie lepszego audytu;
- dłuższy raport nie oznacza większej wartości;
- zgodność dwóch modeli nie jest dowodem;
- kompletność formularzy nie zastępuje zmiany zachowania;
- metryka sukcesu musi uwzględniać koszt protokołu;
- po każdej sesji wskaż jedną rzecz do uproszczenia, nawet gdy wynik był dobry.

## 7. Braki do uzupełnienia w następnej sesji

1. zmierzyć zegarem `bootstrap_minutes`, `analysis_minutes` i `protocol_minutes`;
2. ustalić prostą normalizację reopenów na 100 stron lub 100 wiadomości;
3. zapisać czas wznowienia po co najmniej jednodniowej przerwie;
4. wybrać trzecią rozmowę z innej domeny, najlepiej przebiegającą dobrze.
