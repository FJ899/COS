# Walidacja Creative OS

Uruchom z katalogu głównego repo:

```bash
python scripts/verify_creative_os.py
```

Walidator sprawdza deterministycznie:

- obecność kanonicznych plików, audytu ciągłości i testu operacyjnego;
- nagłówek oraz status architektury Lean;
- kompletność tabeli projektów;
- status, źródło prawdy i jeden następny krok każdego projektu;
- dostępność minimalnego lokalnego stanu BPM:160;
- spójność maszynowego i opisowego handoffu BPM:160;
- warunek powrotu dla wpisów `PARKING`;
- zachowanie lekkiego filtra użyteczności dla nowych funkcji;
- zgodność Aktualnego Handoffu z tabelą;
- zachowanie branchy archiwalnych i triggera powrotu do cięższej architektury;
- obecność filtra w szablonie pull requestu.

Skrypt nie ocenia jakości decyzji, nie zastępuje niezależnego cold startu i nie zmienia repozytorium. GitHub Actions uruchamia go przy pull requestach i zmianach na `main`.
