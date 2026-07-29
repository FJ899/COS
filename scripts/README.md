# Walidacja Creative OS

Uruchom z katalogu głównego repo:

```bash
python scripts/verify_creative_os.py
```

Walidator sprawdza deterministycznie:

- obecność kanonicznych plików i audytu ciągłości;
- nagłówek oraz status architektury Lean;
- kompletność tabeli projektów;
- status, źródło prawdy i jeden następny krok każdego projektu;
- warunek powrotu dla wpisów `PARKING`;
- zgodność Aktualnego Handoffu z tabelą;
- zachowanie branchy archiwalnych i triggera powrotu do cięższej architektury.

Skrypt nie ocenia jakości decyzji ani nie zmienia repozytorium. GitHub Actions uruchamia go przy pull requestach i zmianach na `main`.
