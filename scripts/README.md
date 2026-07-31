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
