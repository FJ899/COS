# Walidacja Creative OS

Uruchom z katalogu głównego repo:

```bash
python scripts/verify_creative_os.py
```

Walidator sprawdza deterministycznie:

- obecność `START_HERE.md`, kanonicznych plików i audytów ciągłości;
- kontrakt pojedynczej stacyjki, tryby `BOOT / WORK / AUDIT / PORTFOLIO` i mapę entrypointów;
- rozdzielenie mapy uruchomienia od właścicieli stanu;
- nagłówek oraz status architektury Lean;
- kompletność tabeli projektów;
- status, źródło prawdy i jeden następny krok każdego projektu;
- dostępność minimalnego lokalnego stanu BPM:160;
- rozgałęzienie `SOURCE RECOVERY FOUND / NOT FOUND`;
- spójność maszynowego i opisowego handoffu BPM:160;
- warunek powrotu dla wpisów `PARKING`;
- zachowanie lekkiego filtra użyteczności dla nowych funkcji;
- zgodność Aktualnego Handoffu z tabelą;
- zapis wyniku cold startu 002;
- zachowanie branchy archiwalnych i triggera powrotu do cięższej architektury;
- obecność filtra w szablonie pull requestu.

Skrypt nie ocenia jakości decyzji, nie zastępuje niezależnego testu stacyjki i nie zmienia repozytorium. GitHub Actions uruchamia go przy pull requestach i zmianach na `main`.
