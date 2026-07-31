---
project: "BPM:160"
portfolio_status: "QUEUED #2"
local_work_state: "SPIKE 001 IN PROGRESS"
state_owner: "projects/bpm160/PROJECT_STATE.md"
blocker: "ORIGINAL SOURCE FILES REQUIRED FOR SAFE RESUME"
next_step: "read_only_reconciliation_then_resume_spike_001"
resume_contract: "READ_ONLY RECONCILIATION / SPIKE FIRST"
---

# HANDOFF — BPM:160

## Stan wejściowy

- Creative OS zachowuje pozycję `QUEUED #2`.
- Lokalnym, potwierdzonym etapem jest `SPIKE 001 IN PROGRESS`.
- Wysokopoziomowa korekta użytkownika jest zapisana w `SOURCE_SUMMARY_2026-07-31.md`.
- Pierwotne pliki projektu nie zostały jeszcze zaimportowane.
- Poprzedni opis `PAUSED → test widza` był nadmiernym uogólnieniem fragmentu projektu.

Nagłówek YAML jest maszynowym skrótem tego samego handoffu. `PROJECT_STATE.md` pozostaje właścicielem aktualnego stanu.

## Gdzie stanęliśmy

BPM:160 realizuje Spike 001 w lodowcowym kanionie:

```text
World
→ Signal
→ Peak Event
→ Aftermath
→ montaż próbny z audio
→ Evidence Package
```

Pytanie bramkowe:

> Czy BPM160 da się zrealizować przy akceptowalnej jakości, czasie i koszcie?

Dopóki nie ma odpowiedzi, nie otwieramy rozszerzeń projektu.

## Co jest potwierdzone

- Brand Promise = adrenalina i rytm, nie dosłowny medyczny cel 160 BPM;
- Canon v1.2 i jego główne reguły;
- brak ludzi w Canon;
- Minimal Montage Rule;
- prompt `World` dla Higgsfield Cinema Studio;
- `bpm160-heartbeat-guide.wav`;
- model ról Producent / Walidator / Turbo / QA;
- architektura LIVE TODO / handover / Decision Log / parking / WIP / superseding;
- trzy odrębne systemy klasyfikacji lokalnej.

## Czego brakuje do bezpiecznego wznowienia

- Canon v1.2 jako plik;
- bieżący LIVE TODO;
- najnowszy handover;
- Decision Log;
- parking;
- materiały ujęć Spike 001;
- Evidence Package;
- prompt `World` i audio-guide;
- dokumentacja wspólnej warstwy BPM:160 + Creative OS.

## Jeden następny krok

Przeprowadzić:

```text
SOURCE IMPORT
→ READ_ONLY RECONCILIATION
→ ustalenie dokładnego stanu Spike 001
→ minimalna aktualizacja PROJECT_STATE.md
→ wznowienie pierwszego brakującego elementu Spike 001
```

## Zakaz dryfu

Do zamknięcia Spike 001 nie uruchamiać:

- Market Scan v0;
- testów widzów;
- pomiaru fizjologicznego;
- rozszerzenia Canon;
- dodatkowych światów;
- nowego systemu zarządzania projektem.

## Navigation Protocol

`CORE / DETOUR / PARKING / DRIFT` należy do globalnego Creative OS. Nie ma dowodu, że był wewnętrznym protokołem BPM:160. Lokalnie obowiązują trzy osobne osie:

```text
CORE / SUPPORT / EDITORIAL / REJECT
DOING NOW / NEXT / BACKLOG / PARKED / DONE
active / superseded / unresolved
```

## Kryterium poprawnego wznowienia

Nowa sesja działa poprawnie, gdy AI:

1. rozpoznaje Spike 001 jako bieżącą bramkę;
2. nie proponuje testu widza jako następnego kroku;
3. nie miesza trzech lokalnych klasyfikacji z Navigation Protocol COS;
4. zaczyna od plików źródłowych i reconciliation;
5. wznawia tylko pierwszy brakujący element Spike 001;
6. nie aktywuje elementów z PARKING.
