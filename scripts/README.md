# Walidacja Creative OS

Uruchom z katalogu głównego repo:

```bash
python scripts/verify_creative_os.py
```

Walidator sprawdza deterministycznie:

- obecność `START_HERE.md`, kanonicznych plików i audytów ciągłości;
- tryby `BOOT / WORK / AUDIT / PORTFOLIO` i mapę entrypointów;
- rozdzielenie mapy uruchomienia od właścicieli stanu;
- kompletność tabeli projektów;
- skorygowany status BPM:160: `SPIKE 001 IN PROGRESS` i wymagane pliki pierwotne;
- Brand Promise, Canon v1.2, bieżącą bramkę i parking BPM:160;
- rozdzielenie trzech lokalnych klasyfikacji BPM od Navigation Protocol COS;
- obecność `SOURCE_SUMMARY_2026-07-31.md`;
- kolejkę i kryteria `GINSENG_TEST-003`;
- rozdzielenie werdyktu analitycznego od gotowości wdrożeniowej w kontrakcie testu;
- zapis i indeks `archives/Archiwum09.md`;
- Idea Inbox, Feature Razor i warunki powrotu;
- wcześniejsze audyty cold start;
- branche archiwalne i warunek powrotu do cięższej architektury.

Skrypt nie ocenia jakości artystycznej BPM:160, nie wykonuje testu Ginseng, nie uruchamia zewnętrznych skilli i nie zmienia repozytorium. GitHub Actions uruchamia go przy pull requestach i zmianach na `main`.

## Instalacja i zakres bramki dowodowej

```bash
python -m pip install -r scripts/requirements.txt
python -m unittest discover -s tests/capability -p 'test_*.py'
python scripts/verify_capability_evidence.py
```

Bramka odrzuca niepoprawne kształty JSON, zduplikowane klucze JSON,
ścieżki wychodzące poza repo (także symlinki) oraz wielokrotne wskazanie
tego samego pliku jako dwóch dowodów RELIABLE.

Deklaracje CI są odczytywane z YAML, z rzeczywistych bezwarunkowych kroków
`run` workflow uruchamianego na `pull_request`. Obsługiwane są proste komendy
`python`/`python3`, shell `bash`, katalog główny repo; cudzysłowy i komentarz
końcowy są dozwolone. Komentarz, `echo`, warunek, `continue-on-error`, inny katalog,
wrapper powłoki lub `|| true` nie stanowią dowodu uruchomienia. Złożone workflow
wymagają osobnej oceny i rozszerzenia parsera z testem. Obecność deklaracji
nie dowodzi faktycznego sukcesu CI, pokrycia testami ani poprawności semantycznej.
Dwa różne pliki również nie dowodzą niezależności dwóch realnych przebiegów.

## Porównywanie pomysłów na podstawie dostarczonych danych

CAPABILITY CLAIM: CAP-IDEA-001

```bash
python scripts/compare_ideas.py comparison.json
```

Przykładowe wejście (dane demonstracyjne, nie dowody rynkowe):

```json
{
  "goal": "Wybrać wariant prototypu",
  "criteria": {"hours": "minimize", "verified_requirements": "maximize"},
  "ideas": [
    {
      "id": "A", "feasible": true, "feasibility_evidence": "kontrola ograniczeń A",
      "metrics": {
        "hours": {"value": 4, "evidence": "pomiar próby A"},
        "verified_requirements": {"value": 3, "evidence": "test A"}
      }
    },
    {
      "id": "B", "feasible": true, "feasibility_evidence": "kontrola ograniczeń B",
      "metrics": {
        "hours": {"value": 8, "evidence": "pomiar próby B"},
        "verified_requirements": {"value": 5, "evidence": "test B"}
      }
    }
  ]
}
```

Każde kryterium musi mieć tę samą jednostkę, skalę i sposób pomiaru dla wszystkich
wariantów. Narzędzie nie potrafi sprawdzić tego za użytkownika. W przykładzie A
oszczędza czas, a B spełnia więcej wymagań: oba pozostają na froncie porównania.
Wariant dominuje inny tylko wtedy, gdy nie jest gorszy w żadnym kryterium i jest
lepszy w co najmniej jednym. Remis nie tworzy zwycięzcy. Nie sumujemy arbitralnych
punktów. Brak miary lub źródła daje `NEEDS_EVIDENCE`; potwierdzona niewykonalność
daje `INFEASIBLE`. Niepotwierdzona wykonalność również wymaga danych.

Wynik JSON zawiera `dominated_by`, `frontier_among_evidenced`, `unresolved`
i granicę `HUMAN_REVIEW_REQUIRED`. Front jest warunkowy względem dostarczonych,
kompletnych danych. Pomysł bez danych może okazać się lepszy od całego frontu.
Źródła są referencjami dostarczonymi w wejściu, nie uwierzytelnionymi dowodami.
Narzędzie niczego nie zapisuje, nie aktywuje projektów, nie zmienia tagów ani
priorytetów i nie analizuje samodzielnie jakości tekstu lub kreatywności.
