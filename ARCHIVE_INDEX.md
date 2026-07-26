# Indeks archiwum

Aktywny `main` ma pozostać mały. Pełna historia poprzednich rozwiązań jest zachowana przez Git i branche archiwalne.

## Cognitive OS v0 — stan pilota przed uproszczeniem

- Branch: `archive/cos-v0-pilot-2026-07`
- Commit: `77a2544409a0cd56c9ddc4fb341ec0e721b29919`
- Zawartość: pełny stan `COS/`, `PILOT/`, `WNIOSKI_I_POMYSLY/`, dokumentacja, schematy, skrypty, szablony i pierwszy audyt.
- Powód archiwizacji: checkpoint wykazał `SIMPLIFY`; aktywna struktura zaczęła generować koszt, sprzeczności i archeologię stanu.
- Status: `ARCHIVED AS EXPERIMENT / ABSORBED AS RULES / NOT DEVELOPED AS SEPARATE SYSTEM`.

## Drugi audyt z zamkniętego PR #3

- Branch: `archive/cos-v0-pilot-pr3-2026-07`
- Commit: `2f888d61ba582a766b4e245553cdae1a9373af79`
- Zawartość: drugi audyt, raport sesji, zaktualizowane metryki, rejestr rozmów i handoff.
- Powód osobnego zachowania: materiały były merytorycznie wartościowe, ale nie powinny być scalone do nowego aktywnego systemu.

## Co zostało wchłonięte do Creative OS

- rozmowa jest procesorem, repo zachowuje stan;
- rekomendacja AI nie jest decyzją użytkownika;
- najnowsza jawna decyzja użytkownika wygrywa;
- analiza zaczyna się w trybie `READ_ONLY`;
- brak dowodu oznacza jawną niepewność;
- sprawdź istniejące rozwiązanie przed budową;
- nowa nazwa nie jest nowym dowodem;
- parking wymaga warunku powrotu;
- zmiany architektury zapisujemy wraz z powodem i warunkiem ponownego otwarcia;
- protokół zmieniamy na checkpointach, nie po każdym odkryciu.

## Warunek powrotu do cięższej architektury

Wersja jednoplikowa musi zawieść co najmniej dwa razy w konkretny, nazwany i porównywalny sposób, którego nie da się usunąć małą korektą wewnątrz `CREATIVE_OS.md`.
