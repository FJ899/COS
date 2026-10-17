# COS — audyt funkcji i kierunek rozwoju, 2026-10-17

Zakres: jawne zlecenie użytkownika analizy, napraw i rozwoju COS.
Punkt odniesienia `main`: `76ed08cad8e3e94de1a5c97ea9136862a9303dc7`.
Dodatkowo odczytano otwarte implementacje: PR #47 na `6f8aa87de8a6e9de7fe53c8a013a77789abb2950`
i PR #48 na `1c14869c28fd0036e09a9da7e1b67d82ca5b391e`.
To audyt kodu, kontraktów i lokalnych testów; nie pełny test realnych projektów.
Nie zmienia historycznych akceptacji ani globalnej kolejności MASTER TODO.

## Ocena działania

COS na main prowadzi pamięć, nawigację, pomysły, handoff i kontrolę dowodów.
Nie ma tu działającego silnika rozumienia treści ani automatycznego wyłaniania
najlepszych pomysłów. Tę ocenę wykonuje model podczas rozmowy. Projector z PR #47
jest rejestratorem i walidatorem przejść pracy, nie samodzielnym kreatywnym plannerem.
To istotna różnica między opisanym zachowaniem ekosystemu a wykonującym je kodem.

Mocne strony: lokalni właściciele prawdy, jawne hipotezy, rozdzielenie akceptacji
od integracji, wiązanie historycznych dowodów skrótami oraz odtwarzalny stan.
Słabość ogólna: duża część mechanizmów sprawdza istnienie deklaracji, nie ich
prawdziwość lub użyteczność. Zielone CI nie dowodzi skutecznego prowadzenia projektu.

## Potwierdzone problemy

| Waga | Funkcja / mechanizm | Problem i skutek | Wynik pakietu |
|---|---|---|---|
| Wysoka | `_workflow_text` / bramka capability | Substring w dowolnym miejscu YAML uznawany za wykonanie testu; komentarz, echo i wyłączony krok mogą wystarczyć. | Parser YAML sprawdza rzeczywiste, proste kroki run, warunki, maskowanie błędów, katalog i trigger PR. |
| Wysoka | `_existing_paths` | Absolutna ścieżka, traversal lub symlink może dostarczyć „dowód” spoza repo. | Rozwiązanie ścieżki i kontrola zawierania przed odczytem. |
| Średnia | `validate_repository` | JSON root `[]` i status `[]` powodują wyjątki zamiast kontrolowanego błędu. Duplikaty kluczy pozwalają niejawnie zastępować dane. | Walidacja typów i odrzucanie powtórzonych kluczy. |
| Średnia | RELIABLE | `run.md` i `./run.md` liczą się jako dwa dowody. | Liczenie unikalnych rozwiązanych ścieżek. To nadal nie dowodzi niezależności semantycznej przebiegów. |
| Średnia | `parse_rows` | Drugi wiersz projektu po cichu zastępuje pierwszy w słowniku. | Odrzucanie duplikatów z testem regresji. |
| Wysoka | PR #47 `verify_bundle` | Odtwarzanie stosuje słabsze reguły niż zapis. Przeliczony hash nie zapobiega akceptacji przejścia bez evidence_basis. | Oddzielna gałąź poprawki względem PR #47: replay używa `validate_transition_input`. |
| Średnia | START_HERE WORK | „Jeden krok” wymusza powrót użytkownika nawet w zleconym pakiecie odwracalnej pracy. | Praca do rezultatu lub realnej bramki, z zachowaniem zakresu użytkownika. |
| Średnia | Idea Inbox | Tag nawigacji bywa mylony z jakością pomysłu; brak operacyjnego porównania alternatyw. | Procedura porównania i opcjonalny read-only helper Pareto. |

Reprodukcja błędu Projectora na odczytanym head PR #47:

1. `validate_init_input` oraz `validate_transition_input` tworzą poprawne stany 0 i 1.
2. Usuń `evidence_basis` oraz `route.evidence_basis` stanu 1, pozostawiając je jako puste listy.
3. Przelicz `state_sha256` przez istniejące `state_hash` i zapisz stan 1 w tymczasowym bundle.
4. Walidacja przejścia odrzuca: `every material transition requires a non-empty evidence_basis`.
5. `verify_bundle` tego samego bundle akceptuje dwa stany.

Poprawka ujednolica replay z live validation; nie tworzy podpisu ani ochrony przed
aktorem, który może przepisać wszystkie pliki. Hash chain wykrywa niespójność,
a nie uwierzytelnia samodzielnie autora decyzji lub prawdziwości dowodu.

## Usprawnienie analizy pomysłów

`compare_ideas.py` porównuje wyłącznie dostarczone, porównywalne miary.
Oddziela wykonalność od atrakcyjności, wskazuje dominację i kompromisy, zachowuje
nierozstrzygnięte warianty oraz nie przypisuje zer za brak danych. Nie stosuje
arbitralnej sumy punktów ani nie ogłasza zwycięzcy przy konflikcie kryteriów.

Status CAP-IDEA-001 pozostaje IMPLEMENTED; dołączone testy lokalne nie są dowodem
realnej skuteczności wyboru. Źródła danych są referencjami z wejścia i wymagają
oceny. Narzędzie nie ocenia samodzielnie scenariuszy, rynku ani kreatywności.

## Ograniczenia i dalsze rekomendacje

1. **Domknąć integrację istniejącej pracy.** PR #47 i #48 zawierają funkcje nieobecne
   na main; nie budować trzeciego odpowiednika. Poprawka replay ma osobny PR do
   gałęzi implementacji. Zmiany walidatora z tego pakietu i PR #48 wymagają
   wspólnej regresji przy integracji; obie gałęzie dotykają tych samych plików.
2. **Testy muszą zależeć od zachowania implementacji.** Main nadal akceptuje
   `assert True` jako plik testowy. PR #48 adresuje część tego problemu przez
   kontrolowane próby wykonania. Nie integrowano go po cichu ani nie zastąpiono
   szerszego problemu samym parserem YAML.
3. **Oddzielić historię od bieżącego obrazu.** CREATIVE_OS opisuje wcześniejszy
   ScriptOps, START_HERE późniejszą akceptację, MASTER TODO własny stan kolejki.
   Rozdzielenie źródeł jest słuszne, lecz snapshoty i historyczne handoffy
   spowalniają start. Następna korekta powinna wynikać z bieżącego odczytu lokalnych
   ownerów, nie z tego audytu COS. Nie zadeklarowano odświeżenia obcych projektów.
4. **Zmniejszyć sztywność walidatora ciągłości.** Dokładne zdania i historyczne SHA
   są przydatne przy zamrożonych dowodach; jako test aktualnego stanu wymuszają
   aktualizację kodu przy zmianach narracji. Rozdzielać testy historycznej integralności
   od bieżących niezmienników; nie przepisywać wszystkich dowodów naraz.
5. **Nie mylić stub detectora z analizą funkcji.** Każdy `pass` jest obecnie
   odrzucany, także w legalnej klasie wyjątku; `...` i semantyczny fake success
   nie są wiarygodnie rozpoznawane. Potrzebna jest ocena i test zachowania,
   nie coraz dłuższa lista słów zakazanych.
6. **Projector: realna walidacja efektu.** WORKLOAD_EXTERNAL jest typem referencji,
   a nie pobranym, niezależnie sprawdzonym wynikiem. Przy rozwoju preferować jeden
   adapter weryfikujący konkretny efekt rzeczywistego zadania. Nie budować
   uniwersalnego silnika dowodowego przed takim przypadkiem.

## Naturalny potencjał — propozycje kolejnego etapu

| Rozwiązanie | Efekt | Najmniejszy test / warunek wejścia |
|---|---|---|
| Pętla pomysł → próba → wynik → korekta | Uczy preferencji i poprawności hipotez z faktycznych efektów. | Jeden prawdziwy wybór 3 wariantów, zapis oczekiwania i wyniku; zmierzyć błąd prognozy. |
| Pamięć odrzuconych wariantów z warunkiem powrotu | Nie powtarza identycznych analiz i nie traci dobrych pomysłów odrzuconych z powodu czasu/budżetu. | Dodać źródło odrzucenia i trigger do istniejącego wpisu, bez nowej bazy. |
| Wykrywanie aliasów z potwierdzeniem | Ogranicza mnożenie tego samego pomysłu pod nową nazwą. | 20 rzeczywistych wpisów, ręcznie oznaczone pary; mierzyć fałszywe połączenia przed automatycznym scalaniem. |
| Kolejność testów według wartości informacji | Najpierw usuwa niewiadomą mogącą zmienić wybór. | Dla jednego porównania wskazać test, jego koszt i decyzję, którą wynik zmieni. |
| Pochodny widok bieżącego portfela | Pokazuje skąd pochodzi stan i kiedy go sprawdzono. | Dwa realne przypadki kosztownej rekonstrukcji; generować widok z ownerów zamiast drugiego ręcznego źródła prawdy. |

To propozycje, nie aktywacja globalnego backlogu. Pierwszeństwo ma realny rezultat
użytkownika, a nie kompletność powyższej listy.

## Weryfikacja

Przed zmianą: 6 testów capability na main PASS; kandydat PR #47: 36 testów Projectora
PASS; kandydat PR #48: 30 testów capability PASS. Zastosowano testy negatywne
pokazujące słabsze reguły main oraz różnicę live/replay Projectora.

Końcowe wyniki i tożsamość commitów podaje opis PR oraz GitHub Actions.
Nie wykonano pełnego przebiegu wszystkich zewnętrznych projektów, testów z użytkownikami
ani wdrożenia. Historyczne dowody Ginseng pozostają niezmienione.
