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
- nowe runy używają schematu 2.1 i deklarują niepustą listę
  `done_criteria`; każde kryterium musi wskazać dopuszczalny zakres dowodu,
  a przejście do `DONE` musi zawierać aktualny dowód, którego `supports`
  wymienia identyfikator tego kryterium;
- historyczne runy 2.0 pozostają weryfikowalne bez przepisywania ich
  zahaszowanych manifestów i stanów;
- definicja `DONE` i jej kryteria są w runie 2.1 nierozdzielną, niezmienną
  parą; zmiana wymaga nowego runu z jawnym powiązaniem pochodzenia;
- `DONE` jest stanem terminalnym — dalsza praca wymaga nowego runu z jawnym
  powiązaniem pochodzenia;
- pliki tymczasowe po przerwanym zapisie nie są traktowane jako stany.

## Public effects

Domyślny profil operacyjny to `PRIVATE_SINGLE_USER_ANALYSIS_ONLY`. Publiczne
efekty są w nim technicznie wyłączone przez zamrożoną politykę; zarówno
przygotowanie żądania autoryzacji, jak i próba wykonania kończą się bez zapisu
statusem `BLOCKED / PUBLIC_EFFECTS_DISABLED_BY_OPERATIONAL_PROFILE`.

Kod bramki pozostaje jako nieaktywna, testowana granica dla ewentualnej
przyszłej wersji. Nie jest częścią zaakceptowanego prywatnego zastosowania.

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

Granice nieaktywnej warstwy efektów są istotne: dziennik wykorzystania zgody jest lokalny
dla danego klonu, a `observed_public_result` jest raportem wykonawcy zapisu,
nie niezależnym odczytem GitHub. Z tego powodu warstwa publicznych efektów nie
nie otrzymuje akceptacji P4 ani uprawnienia do automatycznego merge.
Kolejna wersja musi użyć współdzielonej idempotencji i niezależnego odczytu
stanu zdalnego po zapisie.

## Testy

```bash
python -m unittest discover -s tests/projector -p 'test_projector_*.py'
```
