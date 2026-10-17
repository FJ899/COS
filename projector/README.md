# Projector

Projector zapisuje ścisły, odzyskiwalny łańcuch stanów. Nie jest plannerem i nie
tworzy samodzielnie twierdzeń ani dowodów.

## Rejestr przebiegu

```bash
python scripts/projector_run.py init --run-dir projector/runs/<run-id> --input init.json
python scripts/projector_run.py transition --run-dir projector/runs/<run-id> --input transition.json
python scripts/projector_run.py verify --run-dir projector/runs/<run-id>
python scripts/projector_run.py recover --run-dir projector/runs/<run-id>
```

Najważniejsze reguły:

- `run.json` oraz stany są append-only;
- JSON z powtórzonymi kluczami albo polami spoza schematu jest odrzucany;
- timestampy muszą zawierać strefę czasową;
- `DONE` jest stanem terminalnym — dalsza praca wymaga nowego runu z jawnym
  powiązaniem pochodzenia;
- pliki tymczasowe po przerwanym zapisie nie są traktowane jako stany.

## Public effects

`projector_public_effect_gate.py` buduje deterministyczne manifesty i sam nie
może wykonać zapisu. `projector_public_effect_trusted_runtime.py` wykonuje
ponowny odczyt Git, pobiera nieedytowany komentarz Human z GitHub i dopiero po
zgodności całej krotki może wywołać ograniczony wykonawca efektu.

Runtime dodatkowo:

- uznaje wyłącznie aktorów wpisanych w
  `governance/PROJECTOR_AUTHORITY_POLICY.json` i sprawdza zamrożony SHA-256 tej
  polityki;
- rezerwuje zgodę w lokalnym dzienniku Git przed wykonaniem zapisu, blokując jej
  ponowne użycie;
- wymaga dokładnej zgodności `observed_public_result` z
  `expected_public_result`;
- zapisuje wynik albo stan `RECONCILIATION_REQUIRED` w
  `.git/projector-public-effects/`;
- nie zezwala na ponowną próbę po niepewnym zapisie bez wcześniejszego
  uzgodnienia rzeczywistego stanu zdalnego.

## Testy

```bash
python -m unittest discover -s tests/projector -p 'test_projector_*.py'
```
