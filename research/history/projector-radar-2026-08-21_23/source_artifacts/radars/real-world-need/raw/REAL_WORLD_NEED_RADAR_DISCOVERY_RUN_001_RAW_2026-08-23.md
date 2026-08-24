Tak. Z tego wyszedł bardzo konkretny sygnał — i kilka rzeczy odpadło po głębszym sprawdzeniu.

Przyjąłem okno **24 lipca–23 sierpnia 2026**. Za „realny problem” liczyłem tylko taki, dla którego znalazłem **świeżą wypowiedź człowieka opisującego własny problem lub własny workaround**. Automatycznie generowane issue/digesty GitHuba wykorzystałem co najwyżej jako potwierdzenie techniczne, nie jako dowód istnienia potrzeby.

Ten przebieg jest celowo mocno **AI/devtools/automation-heavy**. Nie mieszałem do niego losowych problemów konsumenckich tylko po to, żeby uzyskać pozorną różnorodność — w badanej próbce właśnie tutaj wyszedł wyjątkowo gęsty klaster powtarzalnych problemów.

# 10 Opportunity Cards

### CARD 01 — „AI pamięta kod, ale nie pamięta dlaczego”

**Problem:** po wielu sesjach agent ponownie proponuje odrzucone biblioteki, tworzy komponent istniejący już w systemie, zmienia ustalone pojęcia albo omija wcześniejszą decyzję architektoniczną.

To nie jest hipotetyczne. 27 lipca użytkownik opisał duży projekt, w którym po kolejnych sesjach i branchach agent „gubi” wspólne rozumienie architektury i potrafi stworzyć drugi, równoległy mechanizm mimo poprawnych testów. 14 sierpnia inny użytkownik opisał dokładnie problem utraty powodów decyzji przechowywanych w PR-ach, Slacku i głowach ludzi; odpowiedzi potwierdzają, że dzieje się to regularnie. 

**Dzisiejszy workaround:** `CLAUDE.md`, decision log, markdown, ręczne przekazywanie kontekstu, RAG, Slack/Notion, automatyczne wstrzykiwanie ostatnich decyzji.

**Opportunity:** nie „kolejna pamięć AI”, tylko **Decision Provenance Layer**: `DECISION → WHY → SOURCE → REJECTED_ALTERNATIVES → VALID_FROM → SUPERSEDED_BY`, z automatycznym podawaniem agentowi właściwych decyzji przed wykonaniem pracy.

**Score: 9.0/10.**

---

### CARD 02 — Multi-agenty depczą sobie po nogach

**Problem:** Claude Code, Codex, Cursor itd. pracują równolegle, ale nie wiedzą wystarczająco dobrze, co robią pozostałe instancje.

1 sierpnia zespół opisał dwa agenty edytujące ten sam plik w odstępie godziny oraz **40 minut pracy zmarnowanej na problem rozwiązany dzień wcześniej przez innego agenta**. Workaround? Przypięty wątek na Slacku. 20 sierpnia inny użytkownik opisał merge hell po równoległym refaktorze i pisaniu testów przez dwie sesje. 

Na GitHubie w świeżej dyskusji o agent control-plane pojawia się bardzo podobny wymóg: stabilne session ID, event cursor i receipt przy handoffie, zamiast traktowania chat history jako przypadkowego source of truth. 

**Workaround:** worktrees, osobne branche, Slack, kanban, Vikunja, ręczne task assignment.

**Opportunity:** provider-agnostic **Agent Traffic Control**: claim/lease zadania, wykrywanie semantic overlap przed rozpoczęciem pracy, widoczność live, handoff i wspólny ledger.

**Score: 8.7/10.**

---

### CARD 03 — „Gdzie właściwie znikają moje tokeny?”

**Problem:** użytkownik nie potrafi przypisać zużycia do projektu, subagenta, hooka czy pluginu ani zatrzymać runaway consumption.

9 sierpnia użytkownik opisał przekroczenie ustawionego miesięcznego limitu overage i błyskawiczne zniknięcie dokupionych kredytów. 18 sierpnia ludzie pytali, czym w ogóle mierzyć zużycie między sesjami. 

10 sierpnia trafił na GitHub feature request wprost żądający **runtime-enforced spend caps per hooks/plugins/subagents**, a 12 sierpnia użytkownik zgłosił 17% wykorzystania nowego okna po zaledwie dwóch krótkich wiadomościach. 

**Opportunity:** koszt nie jako dashboard po fakcie, lecz **circuit breaker**: „ten agent może wydać maksymalnie $3 / 20% quota / 100k tokens”.

**Score: 8.6/10.**

---

### CARD 04 — Automatyzacja mówi „ustawione”, ale nie działa

To jest jeden z najmocniejszych sygnałów całego badania.

22 sierpnia płacący użytkownik opisał, że ChatGPT **dwukrotnie potwierdził utworzenie Scheduled Task**, a zadanie ani razu się nie uruchomiło; później okazało się wyłączone i bez historii wykonań. 

1 sierpnia użytkownik Claude opisał odwrotną awarię: scheduler pracował **8,5 godziny**, powtarzając tę samą konkluzję, ponieważ narzędzia wymagały approval. 

10 sierpnia inna osoba opisała zadanie, które wykonane ręcznie ma dostęp do connectorów, ale automatycznie już ich „nie widzi”. 

Na GitHubie jest również świeży przypadek, w którym scheduled occurrence zostało skonsumowane podczas DarkWake mimo nieudanego `thread/resume`, bez ponownej próby po pełnym wybudzeniu komputera. 

**Opportunity:** **Proof-of-Run / Automation Reliability Layer**.

Nie „czy cron się odpalił?”, tylko:

`CONFIGURED → ACTIVE → STARTED → TOOLS_AVAILABLE → ACTION_PERFORMED → RESULT_VERIFIED → DELIVERED`

**Score: 9.3/10. — mój numer 1.**

---

### CARD 05 — Retry twierdzi SUCCESS, ale operacja jest martwa

**Problem:** przy agentach wykonujących prawdziwe operacje zwykłe „spróbuj ponownie” przestaje być bezpieczne.

12 sierpnia użytkownik produkcyjnego agenta opisał timeout przy payment API, retry i **podwójne obciążenie klienta**. 

28 lipca w Hindsight zgłoszono bardzo konkretną odwrotność: endpoint retry zwraca `success`, ale operacja trafia do stanu `pending`, którego żaden worker nigdy już nie odbierze — przy okazji tracony jest oryginalny komunikat błędu. 

**Opportunity:** execution gateway zapewniający **idempotency keys + durable effect ledger + retry/recovery receipts**.

**Score: 8.5/10.**

---

### CARD 06 — MCP OAuth działa w curl, a w kliencie „unable to authenticate”

20–21 sierpnia użytkownik opisuje Cognito + MCP: przepływ OAuth przechodzi ręczne testy, logowanie w przeglądarce działa, po czym Claude Desktop wraca z ogólnym `unable to authenticate`. Problemem jest także brak przydatnej introspekcji. 

**Opportunity:** **MCP Auth Doctor** — conformance test dla OAuth 2.1/PKCE/resource metadata/callback/audience, porównujący zachowanie Claude, Codex itd. i mówiący dokładnie, który element handshake'u jest niezgodny.

**Workaround dziś:** curl + proxy + logi + forum.

**Score: 7.6/10.**

---

### CARD 07 — MCP zostawia zombie i psuje następne uruchomienie

14 sierpnia zgłoszono, że Claude Code ubija pierwszy start wolniejszego MCP po około 3 sekundach, po czym wykonuje retry; pod WSL proces Windows pozostaje zombie i blokuje następną instancję. 

5 sierpnia analogiczny problem pojawił się w Codex: synchronizacja marketplace'u potrafi przerwać uruchamianie MCP, zostawić child process i nie zrobić retry. 

To **dwa różne produkty i bardzo podobna klasa awarii**.

**Opportunity:** lekki MCP supervisor/watchdog: health, orphan detection, cleanup, startup sequencing, retry, port/lock diagnostics.

**Score: 7.5/10.**

---

### CARD 08 — Kod przechodzi testy, ale jest architektonicznie zły

To subtelnie inny problem niż pamięć.

Użytkownik dużego projektu opisuje, że test może być zielony, mimo iż agent w ogóle **nie powinien był stworzyć rozwiązania w tej formie**. 

W innym świeżym wątku pięcioosobowy zespół używający różnych agentów stwierdza, że potrzebuje review gate, bo dwa agenty potrafią zgodnie zaakceptować błędne rozwiązanie, podczas gdy problem zauważa dopiero człowiek czytający diff. 

Podczas sierpniowego outage'u GitHuba developer opisał też konieczność wielogodzinnego sprzątania klas adapterów, które agent bez potrzeby dołożył do głównego frameworka. 

**Opportunity:** **Intent/Architecture Review**, nie kolejny linter: „czy ta zmiana jest zgodna z istniejącym wzorcem i czy w ogóle powinna istnieć?”.

**Score: 8.4/10.**

---

### CARD 09 — Awaria GitHuba zatrzymuje nie tylko GitHuba

W ostatnich tygodniach sygnał był wyjątkowo mocny. 6 sierpnia ludzie nie mogli deployować przez Actions. 17 sierpnia kolejny outage zatrzymał coding agents; jeden użytkownik skarży się wprost na **utracone AI credits, bo zadania trzeba było wykonywać ponownie**. 

17 sierpnia wątek o awarii GitHuba zebrał ponad 2200 głosów, a użytkownicy dyskutowali o lokalnych buildach, GitLabie/Gitea i własnych ścieżkach deploymentu. 

**Opportunity:** nie „kolejny GitHub”, lecz **local-first continuity layer**: kolejkowanie agent work, lokalny mirror niezbędnego stanu, replay po powrocie usługi, awaryjna ścieżka CI/deploy.

**Score: 7.7/10.**

---

### CARD 10 — Context/tool tax: agent płaci zanim zacznie pracować

18 sierpnia użytkownicy analizują, ile kosztuje resend kontekstu, tool results i reasoning oraz jak w ogóle mierzyć ten narzut. 

W świeżym issue Claude Code użytkownik pokazał znaczące wykorzystanie quota po dwóch tekstowych wiadomościach i poprosił wprost o rozbicie „new work” vs „context replay”. 

Problem nasila się wraz z MCP, skills, pamięcią i subagentami.

**Opportunity:** **Context Profiler + Lazy Loader**: pokaż koszt każdej warstwy i wstrzykuj ją dopiero wtedy, kiedy jest potrzebna.

**Score: 8.0/10.**

---

# Ranking po pierwszym sicie

| #ProblemOpportunityOcena |                                                    |                                  |         |
| ------------------------ | -------------------------------------------------- | -------------------------------- | ------- |
| **1**                    | Scheduled automation bez wiarygodnego proof-of-run | **Automation Reliability Layer** | **9.3** |
| **2**                    | Utrata „dlaczego podjęliśmy tę decyzję”            | **Decision Provenance Memory**   | **9.0** |
| **3**                    | Nieprzewidywalny burn kosztu/quota                 | **Spend Circuit Breaker**        | **8.6** |
| 4                        | Multi-agent collisions                             | Agent Traffic Control            | 8.7\*   |
| 5                        | Retry / duplicate effects / false success          | Durable Action Gateway           | 8.5     |
| 6                        | Architektonicznie zły kod mimo zielonych testów    | Intent Review                    | 8.4     |
| 7                        | Context/tool tax                                   | Context Profiler                 | 8.0     |
| 8                        | GitHub dependency/outages                          | Continuity Layer                 | 7.7     |
| 9                        | MCP OAuth debugging                                | MCP Auth Doctor                  | 7.6     |
| 10                       | MCP zombie processes                               | MCP Supervisor                   | 7.5     |

\*Coordination ma bardzo mocny problem, ale obniżam pozycję biznesową ze względu na szybko rosnącą konkurencję.

---

# DEEP VALIDATION — TOP 3

## TOP 1 — Automation Reliability Layer

### Czy problem jest realny?

**Bardzo.**

Najbardziej interesujące jest to, że występują **oba przeciwne failure modes**:

-  zadanie potwierdzone jako aktywne → **nie uruchamia się**;  
-  zadanie powinno się zatrzymać → **pracuje 8,5 godziny w pętli**;  
-  manual run działa → scheduled run **traci connectory**;  
-  występuje też błąd recovery po przerwanym scheduled run.  

To nie jest kosmetyka UI. To problem **false confidence**.

### Czy ktoś już płaci za workaround?

**Tak — i to jest bardzo dobry sygnał.**

Nie zawsze płaci za identyczny produkt, ale rynek płaci już za warstwę obserwowalności i niezawodności AI: Langfuse ma płatne Core $29/mies. i Pro $199/mies., Helicone Pro kosztuje $79/mies., Braintrust Pro $249/mies. 

Czyli pytanie „czy firmy płacą za wiedzę, co agent naprawdę zrobił?” ma już odpowiedź **tak**.

### Czy rozwiązanie już istnieje?

**Częściowo.**

Langfuse/Braintrust/Helicone obserwują LLM calls i traces. LangSmith oferuje nawet durable execution i fault-tolerant agent runtime. 

Ale to nie jest dokładnie problem:

> „Claude/ChatGPT/Codex powiedział, że automatyzacja została ustawiona — udowodnij mi, że istnieje, ma właściwe uprawnienia, uruchomiła się, wykonała działanie i dostarczyła wynik.”

### Czy luka jest realna?

**TAK — 9/10**, ale z jednym ważnym zastrzeżeniem.

Najbardziej wartościowy produkt nie powinien być kolejnym systemem cron. Powinien dostarczać **zewnętrzny dowód wykonania**:

`EXPECTED RUN`

→ `ACTUAL RUN`

→ `PRECONDITIONS`

→ `SIDE EFFECTS`

→ `RESULT`

→ `DELIVERY`

→ `VERIFIED`

Ryzyko: zamknięte schedulery ChatGPT/Claude mogą nie wystawiać wszystkich potrzebnych danych. Dlatego pierwszy produkt należałoby skierować do **agent workflows, do których mamy hook/API/log**, a dopiero potem rozszerzać integracje.

**WERDYKT: DEEP VALIDATION PASS.**

---

# TOP 2 — Decision Provenance Memory

### Czy problem jest realny?

**Tak, i problem został bardzo dobrze nazwany przez użytkowników.**

Nie chodzi o „AI zapomniało nazwę użytkownika”. Chodzi o:

> agent nie wie, **dlaczego coś jest takie, jakie jest**.

Przy dużym projekcie prowadzi to do powielania implementacji, wskrzeszania odrzuconych pomysłów i łamania semantyki systemu. 

### Czy ktoś już płaci?

Tutaj odpowiedź jest bardzo mocna: **tak.**

Mem0 sprzedaje pamięć agentów za **$19 Starter / $249 Pro miesięcznie**. Zep ma płatne plany od około **$125/mies.** i wyżej. To nie jest już kategoria „może kiedyś będzie rynek”. 

### Czy rozwiązanie istnieje?

**Tak. I tutaj trzeba uważać, żeby nie zbudować rzeczy, która już istnieje.**

Mem0, Zep i inne warstwy pamięci rozwiązują persistent memory. Co więcej, Mem0 właśnie rozwija background consolidation: łączenie duplikatów i oznaczanie starych informacji jako superseded. 

Zatem produkt:

> „baza pamięci dla agenta”

**nie ma wystarczającej luki.**

### Gdzie pozostaje luka?

W dużo węższym mechanizmie:

**FACT MEMORY ≠ DECISION MEMORY.**

Potrzebne byłoby:

`decyzja`

- `kto/źródło` 
- `dowód` 
- `dlaczego` 
- `co odrzucono` 
- `jakich elementów dotyczy` 
- `co może ją unieważnić` 
- `która decyzja ją zastąpiła`. 

I — kluczowe — zapis z PR/Slack/meetingu nie powinien automatycznie stawać się kanonem tylko dlatego, że LLM go znalazł.

To jest bardziej **decision governance dla ludzi + agentów** niż klasyczne „AI memory”.

### Werdykt

**LUKA REALNA, ALE WĄSKA — 8.5/10.**

Budowanie ogólnej pamięci: **NO-GO**.

Budowanie **evidence-backed decision lineage + automatic context injection**: **GO DO DALSZEJ WALIDACJI**.

---

# TOP 3 — Spend Circuit Breaker

Tutaj deep validation przyniosło najważniejszą korektę.

### Czy problem jest realny?

**Zdecydowanie tak.**

Użytkownicy zgłaszają niespodziewany quota burn, brak atrybucji kosztu i potrzebę twardego zatrzymania automatyzacji. GitHub request z 10 sierpnia opisuje dokładnie potrzebę runtime-enforced limitu, a nie kolejnego ostrzeżenia. 

### Czy ktoś płaci?

**Tak.**

Langfuse, Helicone, Braintrust i inne platformy mają płatne warstwy cost/usage observability. 

### Czy istnieje rozwiązanie?

I tu pojawia się problem z Opportunity.

**Dla API — tak, i to całkiem dobre.**

Helicone potrafi ograniczać requesty i koszty. OpenRouter ma budget limits, które faktycznie odrzucają request po osiągnięciu limitu; pozwala ustawiać budżety na użytkownika/API key. 

Czyli szeroki pomysł:

> „stwórzmy budżety i hard caps dla LLM”

jest **za późny**.

### Gdzie pozostaje luka?

W **subscription-native coding agents**:

Claude Code / Codex / Cursor / inne narzędzia działające na planach użytkownika, gdzie nie wszystkie koszty i quota przechodzą przez kontrolowany przez nas API gateway.

Tutaj potrzebne jest:

`PROJECT → SESSION → AGENT → SUBAGENT → TOOL → COST/QUOTA → WORK PRODUCT`

i circuit breaker na poziomie **wykonywanej pracy**, a nie tylko API key.

Problem: jeżeli vendor nie udostępnia bieżącego licznika quota/API, egzekwowanie limitu może być technicznie niemożliwe albo przybliżone.

### Werdykt

**PROBLEM: PASS.**
**
GENERYCZNE ROZWIĄZANIE: FAIL — już istnieje.**
**
WĄSKA LUKA DLA CODING AGENTS: CONDITIONAL PASS — 7.5/10.**

Nie budowałbym tego jako pierwszego produktu bez najpierw udowodnienia, że możemy wiarygodnie przechwycić usage z minimum Claude Code + Codex + Cursor.

---

# Co zaskakująco wypada najlepiej

Po deep validation ranking zmienia się:

| PozycjaOpportunityProblem realnyLudzie płacąKonkurencjaLuka po walidacji |                                             |         |                    |                          |                         |
| ------------------------------------------------------------------------ | ------------------------------------------- | ------- | ------------------ | ------------------------ | ----------------------- |
| 🥇                                                                       | **Proof-of-Run / Automation Reliability**   | **TAK** | **TAK, pośrednio** | średnia                  | **DUŻA**                |
| 🥈                                                                       | **Decision Provenance Layer**               | **TAK** | **TAK**            | wysoka                   | **REALNA, jeśli wąska** |
| 🥉                                                                       | **Spend Circuit Breaker for coding agents** | **TAK** | **TAK**            | bardzo wysoka            | **WARUNKOWA**           |
| 4                                                                        | Multi-Agent Traffic Control                 | TAK     | częściowo          | **bardzo szybko rośnie** | średnia                 |
| 5                                                                        | Durable Action/Retry Gateway                | TAK     | TAK                | średnia                  | duża                    |

I jest tu jedna rzecz, która moim zdaniem zasługuje na **osobny Deep Dive**, bo pod powierzchnią wygląda większa niż pojedynczy „scheduler bug”:

> **AI potrafi dziś deklarować stan operacyjny bez niezależnego dowodu, że ten stan faktycznie istnieje.**

„Task utworzony”, „retry successful”, „agent completed”, „monitor działa”, „nic nowego nie znaleziono” — wszystkie te komunikaty należą do tej samej klasy problemu: **DECLARATION ≠ PROOF OF EXECUTION**.

To łączy CARD 04 i CARD 05, częściowo CARD 03, a nawet problemy z multi-agentami. I właśnie tutaj widzę potencjalnie **większą kategorię produktową niż samo monitorowanie automatyzacji**: niezależną warstwę *execution truth* dla pracy wykonywanej przez agentów. 

To jest znalezisko, którego **nie wrzucałbym jeszcze do zwykłego archiwum Opportunity Cards**. Jest wystarczająco mocne, żeby zrobić następny etap: **Deep Dive „Execution Truth Layer” → istniejące produkty → dokładna granica luki → kto jest buyerem → minimalny produkt → kill criteria**.