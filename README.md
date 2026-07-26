# Creative OS — instrukcja operacyjna

Creative OS jest osobistą, przekrojową pamięcią projektów, pomysłów i wznowienia pracy. Ma ograniczać utratę pomysłów i ponowne składanie kontekstu po przerwie, bez zastępowania lokalnych systemów projektowych.

Aktywnym źródłem stanu przekrojowego jest jeden plik: [`CREATIVE_OS.md`](CREATIVE_OS.md).

Pełna historia wcześniejszego eksperymentu znajduje się w branchach opisanych w [`ARCHIVE_INDEX.md`](ARCHIVE_INDEX.md).

---

## 1. Podział odpowiedzialności

### Użytkownik odpowiada za

- wybór kierunku;
- zmianę celu lub priorytetu;
- decyzję, czy nowy pomysł ma zastąpić aktualny rezultat;
- zamknięcie, odrzucenie albo połączenie projektu;
- działania kosztowne, publiczne, ryzykowne lub trudno odwracalne;
- ostateczne uznanie, że dowód wystarcza do trwałej zmiany reguły.

### AI odpowiada za

- odczyt i porządkowanie stanu;
- przechwytywanie każdego nowego pomysłu;
- wykrywanie aliasów, duplikatów i sprzeczności;
- proponowanie tagu `CORE / DETOUR / PARKING / DRIFT`;
- wyszukiwanie istniejących rozwiązań przed budową;
- przygotowanie minimalnych, odwracalnych testów;
- aktualizowanie opisu projektu, Idea Inbox i handoffu zgodnie z decyzjami użytkownika;
- przygotowywanie branchy, commitów i pull requestów;
- zadawanie pytań tylko wtedy, gdy potrzebna jest decyzja kierunkowa.

### Lokalne systemy projektowe odpowiadają za

- szczegółowy backlog;
- lokalny kanon;
- artefakty projektu;
- testy domenowe;
- dokładny stan wykonawczy;
- szczegółowe decyzje dotyczące jednego projektu.

Przykład: szczegóły BPM:160 pozostają w jego lokalnym systemie. Creative OS przechowuje tylko status wysokiego poziomu, miejsce zatrzymania, brak do wznowienia, następny krok i odnośnik do lokalnego źródła prawdy.

---

## 2. Hierarchia źródeł

Gdy informacje są sprzeczne, obowiązuje kolejność:

1. najnowsza jawna decyzja użytkownika;
2. zatwierdzony stan kanoniczny projektu;
3. najnowszy handoff opisujący zatwierdzoną decyzję;
4. bieżąca karta projektu w `CREATIVE_OS.md`;
5. starsze dokumenty i rozmowy;
6. pamięć AI.

AI nie rozwiązuje sprzeczności przez zgadywanie. Najpierw wskazuje konflikt. Pyta użytkownika tylko wtedy, gdy nie istnieje późniejsza jawna decyzja albo wybór zmieni kierunek.

---

## 3. Statusy projektów

- `ACTIVE` — projekt ma aktualny, wykonalny rezultat.
- `PAUSED / WAITING` — projekt pozostaje ważny, ale dalsza praca czeka na warunek, decyzję, zasób albo właściwy moment.
- `PARKED` — projekt lub kierunek nie jest obecnie planowany; powrót wymaga jawnego triggera.
- `CLOSED` — rezultat został osiągnięty albo projekt świadomie zakończono.

Każdy projekt ma najwyżej jeden aktualny rezultat. Pauza nie oznacza porzucenia.

---

# 4. Start każdej sesji

## Krok 1 — odczyt stanu

AI czyta cały `CREATIVE_OS.md`.

Nie czyta automatycznie wszystkich branchy archiwalnych ani pełnej dokumentacji wszystkich projektów.

## Krok 2 — ustalenie celu rozmowy

AI ustala:

```text
CEL SESJI:
PROJEKT:
OCZEKIWANY REZULTAT:
TRYB: READ_ONLY | WORK
```

Gdy użytkownik nie podał projektu, AI wskazuje najbardziej prawdopodobny projekt na podstawie rozmowy, ale nie zmienia statusu projektu bez decyzji użytkownika.

## Krok 3 — odczyt lokalnego źródła

AI czyta wyłącznie lokalne źródło prawdy projektu, którego dotyczy sesja.

Minimalny odczyt powinien pozwolić ustalić:

- gdzie projekt stanął;
- co obowiązuje;
- czego brakuje;
- jaki jest jeden następny krok;
- czego nie należy ponownie otwierać bez nowego dowodu.

## Krok 4 — kontrola sprzeczności

AI porównuje lokalny stan z kartą projektu w Creative OS.

Wynik startu:

```text
START SESSION
PROJEKT:
STATUS:
GDZIE STANĘLIŚMY:
BRAK DO WZNOWIENIA / ZAKOŃCZENIA:
JEDEN NASTĘPNY KROK:
SPRZECZNOŚCI: BRAK | LISTA
PYTANIE KIERUNKOWE: BRAK | JEDNO PYTANIE
```

Brak sprzeczności oznacza rozpoczęcie pracy bez dodatkowego pytania.

---

# 5. Praca nad aktualnym rezultatem

1. AI utrzymuje jeden jawny rezultat sesji.
2. Nowa informacja otrzymuje werdykt:
   - `ZMIENIA PLAN`;
   - `NIE ZMIENIA PLANU`;
   - `TRZEBA SPRAWDZIĆ`.
3. Rekomendacja AI pozostaje hipotezą roboczą.
4. Przed budową AI sprawdza:
   - kartę projektu;
   - Idea Inbox;
   - lokalny system projektu;
   - istniejące narzędzia lub rozwiązania.
5. AI preferuje najmniejszy test, który może zmienić decyzję.
6. Działania odwracalne i operacyjne wykonuje samodzielnie.
7. Pytanie do użytkownika pojawia się dopiero, gdy potrzebny jest wybór kierunku.

---

# 6. Obsługa każdego nowego pomysłu

Każdy semantycznie nowy pomysł zostaje zachowany. Powtórzenie albo inne sformułowanie tego samego pomysłu nie tworzy nowego wpisu — AI dopisuje źródło lub alias do istniejącego wpisu.

## Krok 1 — krótki zapis

AI nie rozwija pomysłu. Najpierw tworzy zapis:

```text
### IDEA-YYYY-NNN — nazwa — TAG

Projekt lub `UNASSIGNED`:
Źródło / bodziec:
Wartość w jednym zdaniu:
Dlaczego nie teraz:
Warunek powrotu: wymagany dla `PARKING`
Alias:
```

## Krok 2 — cztery pytania Navigation Protocol

1. Jaki aktualny rezultat ten pomysł przybliża?
2. Czy jest potrzebny do zakończenia obecnego etapu?
3. Czy jest nowym problemem, czy aliasem istniejącego pomysłu?
4. Jaki dowód albo warunek uzasadnia aktywację teraz?

## Krok 3 — tag

- `CORE` — pomysł jest potrzebny teraz do aktualnego rezultatu.
- `DETOUR` — pomysł jest wartościowy i powiązany, ale nie jest potrzebny teraz.
- `PARKING` — pomysł należy do innego czasu, etapu albo projektu; musi mieć warunek powrotu.
- `DRIFT` — pomysł nie służy jawnemu rezultatowi albo jego siłą jest głównie atrakcyjność nowości.

`DRIFT` nie oznacza usunięcia. Pomysł zostaje zachowany, ale nie jest rozwijany bez jawnej decyzji o zmianie kierunku.

## Krok 4 — powrót do pracy

Po zapisaniu pomysłu AI wraca do rezultatu sesji. Pomysł nie przejmuje rozmowy, chyba że użytkownik jawnie zdecyduje:

```text
TEN POMYSŁ ZASTĘPUJE AKTUALNY REZULTAT.
```

---

# 7. Dowód i zmiana planu

Za mocniejszy dowód może zostać uznany:

- własny obserwowalny wynik;
- test A/B z wyraźną różnicą;
- powtarzalne działanie;
- konkretna porażka wcześniejszego wariantu;
- nowe ograniczenie techniczne;
- prostsze rozwiązanie osiągające ten sam rezultat;
- nowa informacja zmieniająca możliwość, koszt albo sens wykonania.

Nie są samodzielnym dowodem:

- atrakcyjna nazwa;
- długi opis;
- zgodność kilku modeli;
- entuzjazm;
- nowość narzędzia;
- elegancja architektury.

Przy zmianie kierunku AI przedstawia:

```text
AKTUALNA HIPOTEZA:
NOWY DOWÓD:
WPŁYW: WSPIERA | DOPRECYZOWUJE | OSŁABIA | PRZECZY | BRAK DELTY
REKOMENDACJA: UTRZYMAJ | ZMODYFIKUJ | PRZETESTUJ | ZAPARKUJ | ODRZUĆ | ZASTĄP
DECYZJA UŻYTKOWNIKA: OCZEKUJE
```

---

# 8. Aktualizacja karty projektu

Karta projektu jest aktualizowana, gdy zmieniło się przynajmniej jedno z pól:

- status;
- miejsce zatrzymania;
- brak do wznowienia albo zakończenia;
- jeden następny krok;
- lokalne źródło prawdy.

Format:

```text
Projekt:
Status:
Gdzie stanąłem:
Brak do wznowienia / zakończenia:
Jeden następny krok:
Źródło prawdy:
```

Creative OS przechowuje tylko stan wysokiego poziomu. Szczegóły wykonawcze pozostają w systemie lokalnym.

---

# 9. Zakończenie sesji

Na końcu sesji AI nie zapisuje całej rozmowy. Destyluje tylko stan potrzebny do kontynuacji.

## Minimalny closer

```text
CLOSE SESSION
REZULTAT:
DECYZJE UŻYTKOWNIKA:
NOWE POMYSŁY I TAGI:
DOWÓD / WYNIK TESTU:
ZMIANA KARTY PROJEKTU:
JEDEN NASTĘPNY KROK:
STATE DELTA: BRAK | OPIS
```

## Aktualny Handoff

Handoff jest nadpisywany i ma zawierać:

- aktywny albo ostatnio obsługiwany projekt;
- aktualny status;
- najnowszą decyzję kierunkową;
- miejsce zatrzymania;
- brak do wznowienia;
- jeden następny krok;
- nierozstrzygniętą sprzeczność, jeżeli istnieje.

Historia poprzednich wersji handoffu pozostaje w Git. Nie tworzymy kolejnych plików handoff.

---

# 10. Zmiany w repozytorium

## Zmiana operacyjna

Przykłady:

- dopisanie pomysłu;
- aktualizacja karty projektu;
- aktualizacja handoffu;
- poprawienie statusu zgodnie z istniejącą decyzją;
- dopisanie źródła lub aliasu.

Proces:

1. AI zaczyna w `READ_ONLY`.
2. AI przygotowuje dokładną deltę.
3. Gdy zmiana odzwierciedla jawną decyzję użytkownika albo użytkownik polecił aktualizację repo, AI tworzy mały branch i commit.
4. AI może utworzyć pull request bez pytania o techniczne szczegóły.
5. Merge wykonuje AI, gdy użytkownik jawnie zlecił pełne wykonanie zmiany; w pozostałych przypadkach pozostawia PR do akceptacji.

## Zmiana architektury

Przykłady:

- nowy plik;
- nowy obowiązkowy status;
- zmiana odpowiedzialności między Creative OS i systemem lokalnym;
- zmiana hierarchii źródeł;
- ponowne otwarcie cięższej architektury.

Proces:

1. zapisać konkretną porażkę obecnego systemu;
2. sprawdzić, czy wystarczy mała korekta jednego pliku;
3. zaczekać do checkpointu, poza bezpieczeństwem i utratą danych;
4. utworzyć osobny PR;
5. dodać wpis do sekcji Ewolucja;
6. wymagać jawnej decyzji użytkownika przed merge.

## Zasada commitów

- jeden commit powinien odpowiadać jednej logicznej zmianie;
- wiadomość commitu opisuje rezultat, nie czynność techniczną;
- nie łączymy aktualizacji stanu projektu z przebudową architektury;
- `main` jest stanem aktywnym;
- branche archiwalne pozostają tylko do odczytu.

---

# 11. Wznowienie projektu po przerwie

AI wykonuje kolejno:

1. odczyt `CREATIVE_OS.md`;
2. wybór karty projektu;
3. odczyt wskazanego lokalnego źródła prawdy;
4. porównanie lokalnego i globalnego stanu;
5. wskazanie sprzeczności;
6. podanie jednego następnego kroku;
7. rozpoczęcie pracy bez ponownego opowiadania całej historii.

Wznowienie jest udane, gdy użytkownik nie musi rekonstruować toku myślenia i może od razu ocenić następny krok.

Gdy projekt czeka na zewnętrzną zależność, AI może zaproponować 2–3 inne projekty możliwe do wznowienia. Kandydaci są wybierani na podstawie:

- dostępnego czasu;
- energii;
- narzędzi;
- dostępnych materiałów;
- braku blokady;
- bliskości konkretnego rezultatu.

Użytkownik wybiera kierunek.

---

# 12. Konflikt stanu

Przykład:

```text
CREATIVE_OS.md: następny krok A
lokalny handover: następny krok B
najnowsza jawna decyzja użytkownika: krok C
```

Obowiązuje krok C.

AI:

1. wskazuje trzy źródła;
2. identyfikuje najnowszą jawną decyzję;
3. synchronizuje derived state;
4. nie pyta o rozstrzygnięcie, gdy hierarchia daje jednoznaczną odpowiedź;
5. pyta tylko przy rzeczywistej niejednoznaczności.

---

# 13. Ewolucja systemu

Sekcja Ewolucja w `CREATIVE_OS.md` jest append-only.

Nowy wpis musi zawierać:

```text
ID I NAZWA:
PROBLEM / BODZIEC:
WCZEŚNIEJSZA POSTAĆ:
DECYZJA:
DOWÓD:
CO ZACHOWUJEMY:
CO PARKUJEMY LUB ODRZUCAMY:
WARUNEK POWROTU:
SUPERSEDES:
STATUS:
```

Nie dodajemy wpisu ewolucji dla zwykłej korekty tekstu albo aktualizacji projektu. Wpis jest potrzebny przy zmianie architektury, reguły kierunkowej albo odpowiedzialności systemu.

---

# 14. Workshop i archiwum

## Archiwum

Archiwum służy do zachowania zamkniętych eksperymentów i pełnej historii. Nie jest czytane na starcie zwykłej sesji.

## Workshop

`workshop/YYYY-MM/` można utworzyć tylko dla aktywnych szkiców, których nie da się wygodnie utrzymać w `CREATIVE_OS.md` albo lokalnym systemie projektu.

Każdy materiał workshopu musi mieć:

- właściciela;
- cel;
- datę przeglądu;
- wynik końcowy: `PROMOTED`, `ARCHIVED` albo `DELETED`.

Workshop nie jest źródłem prawdy ani magazynem „może kiedyś”.

---

# 15. Checkpoint pilota

Po kilku rzeczywistych sesjach AI podsumowuje działanie systemu.

Dla każdej sesji wystarczy:

```text
CYKL:
CO ZADZIAŁAŁO:
CO ZAWIODŁO:
WERDYKT: KEEP | SMALL PATCH | FAILURE
```

Znaczenie:

- `KEEP` — system działa; nie zmieniamy architektury.
- `SMALL PATCH` — problem istnieje, ale naprawia go mała korekta obecnego pliku.
- `FAILURE` — system nie zachował pomysłu, nie umożliwił wznowienia albo spowodował istotną błędną zmianę stanu.

Cięższa architektura może wrócić dopiero po dwóch konkretnych, porównywalnych porażkach, których nie da się naprawić małą korektą.

---

# 16. Przykłady

## Nowy pomysł podczas pracy nad BPM:160

```text
Bodziec: nowe narzędzie potrafi automatycznie zmieniać kostium postaci.

AI:
1. sprawdza, czy narzędzie lub podobny pomysł jest już zapisany;
2. zapisuje ideę bez rozwijania;
3. nadaje `DETOUR` albo `PARKING`;
4. podaje warunek powrotu: narzędzie zachowuje twarz i ciągłość w małym teście;
5. wraca do aktualnego rezultatu BPM:160.
```

## Pomysł, który naprawdę zmienia plan

```text
Nowy dowód: obecna metoda trzykrotnie nie osiągnęła wymaganego rezultatu,
a prostsze narzędzie osiągnęło go w odwracalnym teście.

AI:
1. oznacza `ZMIENIA PLAN`;
2. przedstawia dowód i koszt alternatyw;
3. pyta użytkownika o zmianę kierunku;
4. po decyzji aktualizuje lokalny system i kartę projektu.
```

## Powrót po miesiącu

```text
AI czyta Creative OS i lokalny handover projektu.
Podaje status, miejsce zatrzymania, brak i jeden następny krok.
Nie otwiera ponownie zaparkowanych funkcji bez triggera.
```

---

# 17. Skróty używane w rozmowie

Użytkownik może użyć prostych poleceń:

```text
START: [projekt]
```

Odczytaj stan i rozpocznij sesję.

```text
CAPTURE: [pomysł]
```

Zapisz pomysł, sprawdź alias i nadaj tag bez rozwijania.

```text
RESUME: [projekt]
```

Odtwórz miejsce zatrzymania i podaj jeden następny krok.

```text
CLOSE
```

Wykonaj closer i przygotuj deltę stanu.

```text
APPLY
```

Zastosuj zatwierdzoną deltę w repo zgodnie z procesem Git.

```text
CHECKPOINT
```

Oceń rzeczywiste cykle jako `KEEP / SMALL PATCH / FAILURE`.

Polecenia są skrótami, nie obowiązkowym językiem. Zwykła rozmowa ma działać tak samo.

---

# 18. Lista kontrolna AI

## Przed pracą

- [ ] przeczytano `CREATIVE_OS.md`;
- [ ] wskazano projekt i rezultat;
- [ ] odczytano tylko potrzebne lokalne źródło;
- [ ] zgłoszono sprzeczności;
- [ ] nie zmieniono stanu w trybie `READ_ONLY`.

## W trakcie

- [ ] każdy nowy pomysł został przechwycony;
- [ ] sprawdzono alias i reuse;
- [ ] pomysł otrzymał tag;
- [ ] pomysł nie przejął pracy bez decyzji użytkownika;
- [ ] rekomendacje są odróżnione od decyzji;
- [ ] wskazano dowód albo niepewność.

## Na końcu

- [ ] zapisano rezultat i decyzje;
- [ ] zaktualizowano kartę projektu tylko na poziomie wysokim;
- [ ] nadpisano aktualny handoff;
- [ ] wskazano jeden następny krok;
- [ ] przygotowano małą, logiczną deltę Git;
- [ ] nie dodano nowej architektury bez dowodu.
