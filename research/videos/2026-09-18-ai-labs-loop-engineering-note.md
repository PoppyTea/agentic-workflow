# Every Level Of Claude Code Loop Engineering Explained (AI LABS)

- URL: https://youtu.be/PLyRe6Zk--8
- Kanał: AI LABS · 23:04 · publikacja 2026-08-18
- Przetworzone: transkrypt automatyczny YouTube + opis i rozdziały (bez ścieżki wideo)
- Rola: trigger, który skłonił do założenia projektu, i ilustracja tego, co „mniej więcej
  mamy na myśli". Szczegóły są poza jego zakresem; właściwy research zaczyna się od
  analizy Gemini (`research/prompts/`) i osobnych źródeł
- Materiały autora: skille Grill Me (mattpocock/skills), GSAP (greensock/gsap-skills),
  Vercel (vercel-labs/agent-skills), Supabase (supabase/agent-skills), app Paseo (paseo.sh);
  reszta skilli (goal-writer, new-feature, functional-ui, feature-batch, mobile-preview)
  tylko w płatnej społeczności AI Labs Pro

## Treść

### Definicja (00:46)

- Pętla istnieje od zawsze: prompt → agent buduje → człowiek weryfikuje → prompt. „Loop
  engineering" to oddanie agentowi kroku weryfikacji; człowiekowi zostaje wyłącznie
  decyzja „skończone czy dalej".
- Elementy pętli: wyzwalacz, ciało pętli, warunek stopu. Warunek stopu definiuje człowiek
  przed startem, bo agent weryfikuje tylko wtedy, gdy zna oczekiwany wynik.
- Uzasadnienie „dlaczego teraz": modele potrafią pracować godzinami bez nadzoru (01:56).

### Przygotowanie projektu (02:08)

- `CLAUDE.md` zawiera tylko wskaźnik na `AGENTS.md`, żeby repo nie było przywiązane do
  jednego agenta (03:00). Zbieżne z naszą konwencją symlinku.
- `design.functional.md` opisuje każdy klikalny element aplikacji (03:26).
- Skill Grill Me: dopytuje aż spec jest jednoznaczny (03:41).
- MVP buduje się ręcznie, nie w pętli: warunek „done" trzeba znać przed startem, a przy MVP
  jeszcze go nie ma (03:55).

### Poziom 1: jedna pętla, jeden cel (04:32)

- Sygnał, że coś wymaga pętli: dużo iteracji tam i z powrotem z agentem (05:11).
- `/loop` odpala prompt na timerze; `/goal` pracuje aż cel osiągnięty. Loop engineering to
  `/goal` (05:18). Weryfikację po każdej turze robi mniejszy model czytający rozmowę (05:58).
- Struktura: folder `features/`, w nim jeden folder na feature: `spec.md` + pusty folder
  `verification/` wypełniany w trakcie pętli (06:14).
- Spec jest jednocześnie checklistą weryfikacji; narzędzie do screenshotów wskazane
  w globalnym `CLAUDE.md`, bo jest szybsze niż pełna przeglądarka (06:54).
- Zdanie „zapisz spec jako goal" przekształca spec w cel uruchamialny `/goal`; skill
  goal-writer automatyzuje to dla każdego feature (07:40, 07:58).
- Wynik: 38 min bez nadzoru, jeden błąd (mruganie maskotki), którego screenshot nie
  jest w stanie wykryć, bo łapie pojedynczy moment (08:19).

### Setup GitHub, Supabase, Vercel (08:57)

- Człowiek zakłada trzy konta przez Google; wszystko dalej robi agent przez CLI (09:58).
- Auth: agent podaje komendę, człowiek uruchamia ją w drugim terminalu (10:33).
- Skille platform (deploy-to-vercel, supabase, supabase-best-practices) wywołują się same
  (11:11). Segment sponsora 11:53–12:46 (Hedra), pomijalny.

### Poziom 2: fabryka (12:46)

- Wiele feature'ów planowanych razem i wykonywanych jako jedna kolejka; pętla kończy się,
  gdy wszystkie odhaczone (12:49).
- Przed implementacją buduje się klikalny prototyp HTML (folder `mocks/`): sprawdza, czy
  opisana rzecz to ta chciana, i daje pętli wzorzec do weryfikacji (13:13).
- Agent główny nie buduje sam: deleguje do sub-agenta pracującego na branchu (13:50).
- Reguła kluczowa: agent wykonujący pracę nigdy jej nie weryfikuje; weryfikuje osobny
  agent ze świeżym kontekstem, nastawiony adwersaryjnie („zakładaj, że jest błąd") (14:08).
- Pętla build → adversarial review → build trwa aż wiersz w kolejce jest odhaczony; potem
  PR ze screenshotami, człowiek merguje, Vercel wdraża (14:34, 14:59).
- Skille są powiązane: goal-writer → new-feature → functional-ui (16:03). feature-batch
  prowadzi `queue.md` (jedna tabela statusów); `/goal` kończy się, gdy nie ma wierszy
  w `todo`/`building` (17:51, 18:22). Przykład: około 3 h pracy na pierwszym feature (18:45).

### Poziom 3: bez laptopa (20:13)

- Zostają dwa zadania człowieka: planowanie feature i zatwierdzenie merge (20:13).
- Paseo: darmowa aplikacja, agent dalej na własnej maszynie (skille, zalogowane CLI),
  okno z telefonu; obsługuje też zdalny Mac mini (20:43).
- Autor odrzuca wbudowany remote control Claude Code, bo nie daje menu skilli (20:59)
  `[do weryfikacji]`.
- mobile-preview: publikuje mocki HTML jako darmowe linki Vercel, żeby klikać prototyp
  na telefonie zamiast oglądać obrazki (22:34).

## Ocena

Wartość dla naszego projektu:

- Najmocniejszy element to reguła separacji: wykonawca ≠ weryfikator, weryfikator ma
  świeży kontekst i nastawienie adwersaryjne. To wprost odpowiada celowi „minimum do
  samodzielnej pracy agenta" i jest tanie do wdrożenia w istniejącym DOX.
- Drugi: kryterium „done" spisane przed startem jako część specu, a spec = checklista
  weryfikacji. Nasz DOX ma sekcję Verification, ale nie ma konwencji specu per feature.
- Trzeci: heurystyka kiedy pętla się opłaca (dużo iteracji) i kiedy nie (MVP, jednorazowe
  ekrany). Przydatna przy audycie, czy nie przeautomatyzowaliśmy czegoś.
- Struktura `features/<nazwa>/spec.md + verification/` i `queue.md` to prosty stan
  w repo, nie w zewnętrznym narzędziu, zgodny z naszym „nie trzymamy stanów w Linear".

Zastrzeżenia:

- Kluczowe skille (goal-writer, new-feature, functional-ui, feature-batch) są za paywallem;
  film pokazuje ich efekty, nie treść. Trzeba je odtworzyć samodzielnie albo znaleźć
  otwarte odpowiedniki.
- `/goal` jako komenda Claude Code `[do weryfikacji]`: w naszej instalacji widoczny jest
  `/loop` z trybem dynamicznym (samodzielne tempo), komendy `/goal` nie widać. Możliwe, że
  autor używa nowszej wersji, pluginu lub własnego skilla nazwanego tak samo.
- Weryfikacja przez screenshoty jest słaba dla wszystkiego, co dynamiczne (animacje,
  stany pośrednie); film sam to przyznaje, ale nie proponuje alternatywy.
- Poziom 3 to głównie reklama Paseo; nie wnosi nic do samego workflow.
- Brak jakiegokolwiek pomiaru kosztu tokenów za 3 h pętli z sub-agentami i reviewerem.
