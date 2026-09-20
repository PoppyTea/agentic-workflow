Zrozumiałem. Oto wynik triage'u pięciu materiałów wideo w oparciu o ich warstwę audio i wizualną (z uwzględnieniem technicznego ograniczenia przy strumieniach 8-godzinnych).

Wynik możesz skopiować do pliku 2026-09-18-video-triage-gemini.output.md.
Raport analityczny: Workflow AI Coding (Triage)

Uwaga techniczna: Filmy 4 i 5 to kilkugodzinne streamy na żywo (odpowiednio ~8,5h i ~9h). Z powodu limitów czasowych narzędzi do ekstrakcji tokenów wizualnych, opierałem się w ich przypadku na pełnej transkrypcji audio i przeanalizowałem dwa konkretne wycinki czasowe: początek dnia 1. (00:00:00 - 02:00:00) oraz koniec dnia ostatniego (07:40:00 - koniec). Jeśli zechcesz przeanalizować ich środkowe części (np. panele dyskusyjne), zrobimy to w kolejnym podejściu.
Film 1: "Software Fundamentals Matter More Than Ever" (Matt Pocock)

Werdykt: Obejrzyj w całości. Materiał idealnie wpisuje się w Twój cel weryfikacji i ustrukturyzowania pracy; mocno rezonuje z unikaniem chaosu w wieloplikowych zmianach.

**Mapa fragmentów:**

Od,Do,Temat,Wartość,Dlaczego
00:00:29,00:04:20,"Pułapka ""Specs to Code""",5,"Obala mit o tanim kodzie i wielokrotnym ""ślepy"" puszczaniu kompilatora. To nie działa bez kontroli człowieka."
00:05:43,00:07:20,Skill /grill-me,5,"Pokazuje interaktywne odpytywanie, aż do uzyskania shared design concept. Chroni przed ""zrozumieniem inaczej"" przez agenta."
00:08:13,00:09:43,Skill /ubiquitous-language,4,"Generowanie ujednoliconego słownika dla domen w Markdown. Zapobiega ""gadatliwości"" modelu."
00:10:03,00:11:31,"TDD jako ""ogranicznik prędkości""",5,Agent potrzebuje sprzężenia zwrotnego. TDD zmusza go do małych kroków zamiast pisania 1000 linii naraz.
00:12:38,00:15:03,Płytkie vs głębokie moduły,5,Wyjaśnienie dlaczego mikromoduły niszczą możliwości rozumowania AI. Skill /improve-codebase-architecture.
00:15:04,00:18:26,Szare skrzynki i delegacja,4,Projektujesz tylko interfejsy i testy z zewnątrz modułu; AI pisze to co w środku. Chroni to Twoje zdrowie psychiczne jako rewievera.

**Konkretne twierdzenia autora:**

    "Specs to code movement... kończy się produkowaniem śmieciowego kodu" (00:01:46) — Opinia poparta własnym testowaniem.

    "Zły kod jest droższy niż kiedykolwiek" (00:04:00) — Opinia.

    "TDD zmusza LLM do robienia małych kroków i hamuje go przed napisaniem zbyt dużej ilości kodu bez weryfikacji" (00:11:13) — Twierdzenie poparte logiką.

    "System oparty na płytkich modułach uniemożliwia AI zrozumienie całości logiki" (00:13:18) — Logiczne uzasadnienie oparte na literaturze (John Ousterhout).

**Wizualia (brak w audio):**

    00:05:43: Tekst skilla /grill-me: "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one."

    00:08:57: Prik UBIQUITOUS_LANGUAGE.md jako wynik /ubiquitous-language.

    00:12:57: Tabela porównawcza: Deep Modules (Lots of functionality, Simple interface, Hides complexity) vs Shallow Modules (Not much functionality, Complex interface, Surfaces complexity).

    00:17:46: Link do skilli: mattpocock/skills na GitHubie.

**Mapowanie na Twój kontekst:**

    (b) 00:05:43 /grill-me: Świetny dodatek do Twoich kontraktów w folderach. Wymusza dokładną weryfikację specyfikacji, zanim agent podejmie akcję.

    (b) 00:15:04 Szare skrzynki: Podejście "zaplanuj interfejs, zignoruj środek" odciąży Cię przy CodeRabbit PR review.

    (c) 00:11:13 TDD: Podejście "Test first" wymagałoby od Ciebie zmiany sposobu definiowania zadań w Linear.

Ocena marketingu:
Bardzo merytoryczne wystąpienie. Krótka autopromocja newslettera (aihero.dev) na samym końcu (00:17:58).
Film 2: "Don't Build Agents, Build Skills Instead" (Anthropic)

Werdykt: Obejrzyj wybrane fragmenty (pierwsze 5 i ostatnie 3 minuty). Zrozumiesz jak architekci z Anthropic widzą modularność agentów (co rezonuje z Twoim frameworkiem DOX). Środek to chwalenie się partnerami.

**Mapa fragmentów:**

Od,Do,Temat,Wartość,Dlaczego
00:01:21,00:02:40,Claude Code jako uniwersalny agent,4,"Kod to natywny ""interfejs do świata"" dla agenta. Nie potrzebujesz ""Agenta Księgowego"" i ""Agenta Programisty"" - jeden agent używa różnych skilli."
00:02:53,00:04:21,Skille = foldery,5,Skille to foldery z plikiem instrukcji (.md) i pomocniczymi skryptami-narzędziami. Idealnie komponuje się z Twoim AGENTS.md.
00:04:21,00:04:53,Progressive disclosure,5,"Mechanizm oszczędzania okna kontekstu. Ładuj nazwy skilli, nie ich treść."
00:05:00,00:11:00,Ekosystem partnerów,1,Pomiń. Ogólniki o startupach używających Claude.
00:13:20,00:14:32,Zapisywanie pamięci jako Skille,4,"Gwarancja ciągłego uczenia: agent dnia 30 jest mądrzejszy, bo potrafi sam wyeksportować to co zrobił w powtarzalny Skill."

**Konkretne twierdzenia autora:**

    "Wiedza proceduralna dla agentów to po prostu ustrukturyzowane foldery" (00:03:04) — Twierdzenie poparte architekturą Claude.

    "Skrypty w plikach chronią przed problemem zimnego startu u agenta w porównaniu do klasycznych Tool Calls" (00:03:38) — Opinia/Wnioski z budowy infrastruktury.

**Wizualia (brak w audio):**

    00:03:00: Struktura: anthropic_brand/ zawierająca pliki SKILL.md, docs.md, slide-decks.md, apply_template.py.

    00:04:33: Metadane w SKILL.md ładujące się do agenta: name: Anthropic Brand Style Guidelines, description: Anthropic's official brand colors and typography.

**Mapowanie na Twój kontekst:**

    (a) Skille jako foldery: Twój framework DOX w zasadzie realizuje już postulat "Skille = Foldery z Markdownem".

    (b) 00:04:21 Progressive disclosure: Pomoże Ci przy zastępowaniu bramki docker-mcp-toolkit by nie "rozsadzić" kontekstu modelu.

    (b) 00:13:20 Agent uczy się poprzez tworzenie skilli: To może być Twój dalszy cel; agent sam modyfikuje swoje kontrakty pracy.

**Ocena marketingu:**
Mocno ewangelizacyjny środek filmu ("zobacz jak wspaniale działają nasi partnerzy"). Początek i koniec to czysty konkret o architekturze.
Film 3: "Full Walkthrough: Workflow for AI Coding" (Matt Pocock)

**Werdykt:** 
Obejrzyj tylko kluczowe momenty. To jest 1,5-godzinny stream typu "live coding" z zadawaniem pytań widowni. Esencja odpowiadająca Twoim potrzebom to zaledwie ~20 minut, w szczególności pętla w tle i krojenie tasków.

**Mapa fragmentów:**

Od,Do,Temat,Wartość,Dlaczego
00:03:07,00:05:42,Smart zone vs Dumb zone,4,Dlaczego wielkie plany psują AI i trzeba dbać o krótki kontekst (~100k tokenów to bezpieczna strefa).
00:07:31,00:10:58,Memento / Compacting,4,"Lepiej resetować agenta niż ""kompresować"" długą rozmowę (co gubi niuanse)."
00:29:41,00:36:00,PRD jako punkt docelowy,3,Omawianie tworzenia Product Requirements Document.
00:42:00,00:46:18,Vertical Slices,5,"KRYTYCZNE. Dlaczego AI nie powinno programować ""horyzontalnie"" (najpierw cała baza, potem całe API)."
00:53:51,01:02:10,Pętla AFK (Ralph),5,Skrypt wykonujący zadania w tle i generujący proste zlecenia dla Claude'a na podstawie plików Markdown.
01:28:43,01:31:30,Push vs Pull coding standards,4,Zastosowanie narzędzia Sand Castle do izolowania agentów (reviewer vs koder).

**Konkretne twierdzenia autora:**

    "Powyżej 100k tokenów model wchodzi w dumb zone i jakość spada dramatycznie" (00:04:04) — Heurystyka/Obserwacja.

    "Używanie Kanban board do planowania (Directed Acyclic Graphs) to klucz do uruchamiania agentów równolegle" (00:50:34) — Obserwacja poparta narzędziem.

    "LLMy kodujące warstwa po warstwie (horyzontalnie) to proszenie się o brak pętli zwrotnej z testów aż do samego końca" (00:43:03) — Logika i doświadczenie deweloperskie.

**Wizualia (brak w audio):**

    00:45:16: Polecenie dla Claude: break-a-prd-into-issues by wygenerować Vertical Slices.

    00:54:18: Skrypt bash once.sh pobierający issue, 5 ostatnich commitów i uruchamiający: claude --permission-mode accept-edits.

    01:29:56: Repozytorium biblioteki Sand Castle dla architektury potoku: Planner -> Implementer -> Merger.

**Mapowanie na Twój kontekst:**

    (c) 00:10:36 Zrzucanie okna kontekstu: Zaprzeczenie "zapisywaniu wszystkiego" w Lineearze i długim rozmowom w Claude Code. Zaczynaj "na świeżo".

    (b) 00:42:00 Vertical Slices vs Linear: Ten fragment perfekcyjnie diagnozuje Twój problem "dziennika pokładowego". Zamiast ticketu "plik API", rób ticket na mikrofunkcjonalność "baza+api+frontend".

    (b) 00:53:51 Pętla AFK: Koncepcja autonomicznej pętli uruchamianej skryptem pomoże Ci stworzyć faktycznie samodzielne środowisko ("done criteria").

**Ocena marketingu:**
Długi live stream bazujący po części na promocji kursu AI Hero, z dużą ilością "wypełniaczy".
Film 4: WF2026 Day 1 (Stream - początkowe 2 godziny)

**Indeks pierwszej części streamu:**

Start,Koniec,Prelegent,Firma,Tytuł wystąpienia
00:01:46,00:08:22,Swyx,Latent Space,Welcome & Loopcraft
00:12:34,00:28:29,Pablo Castro,Microsoft,On AI and Knowledge
00:28:57,00:43:32,R. Huet & A. Embiricos,OpenAI,The New Engineer
00:48:18,00:54:21,Peter Steinberger,OpenAI,Manager of Agents
00:55:00,01:09:01,Zishuan Lee,Z.ai,GLM 5.2
01:11:20,01:31:14,Thomas Wolf & Olive,Hugging Face,MiniMax M3 Architecture
01:33:34,01:37:11,Randall Degges,Snyk,State of AI Security
01:37:42,01:45:31,Tisha & Sushin,Chronicle,Replaying Agent Runs
01:45:31,01:46:52,Kushan,SARAM,Browser Agents

**Ocena 2 wybranych wystąpień z tego bloku:**
Wystąpienie: Peter Steinberger (OpenAI) - Manager of Agents

**Werdykt:** 
Obejrzyj w całości (6 min). Genialne wpasowanie w Twój cel "minimum pozwalające pracować samodzielnie".Mapa fragmentów:

    00:48:18 - 00:50:05 | Koniec mikrozarządzania agentami (5) | Zamiast bycia nadzorcą 10 terminali, zarządzaj pojedynczym agentem-menedżerem.

    00:51:32 - 00:52:37 | Przykładowy workflow menedżera (5) | Agent-manager ocenia zgłoszenie, podnosi agenta-workera do zakodowania, następnie agenta-reviewera, a na końcu wyrzuca Ci gotowe PR.Wpływ na Twój workflow:

    (b) Obecnie używasz Claude Code jako "workera". Utworzenie nadrzędnej pętli (Menedżera) pomoże zautomatyzować weryfikację.

**Wystąpienie:**
 Tisha & Sushin (Chronicle) - Reproducing Agent Runs

**Werdykt:**
 Obejrzyj fragment o logowaniu na granicach (od 01:43:07). Przydatne, jeśli zastąpisz MCP Toolkit.Mapa fragmentów:

    01:38:00 - 01:43:07 | Sprzętowy niedeterminizm i Temperatura=0 (4) | Dlaczego pętli agenta nie da się idealnie odtworzyć ze względu na operacje GPU (batch invariance).

    01:43:07 - 01:45:31 | Rejestracja w miejscach styku (Boundaries) (5) | Nie loguj "sieci". Rejestruj dane wejściowe i wyjściowe z narzędzi systemowych, żeby w razie "wywrotki" móc idealnie zdebugować przebieg offline.Wpływ na Twój workflow:

    (b) Gdy zaczniesz budować własny ekosystem skilli i uciekać od MCP, musisz zapewnić przechwytywanie stanu wejścia/wyjścia (I/O).

(Pozostałe wystąpienia w zindeksowanym zakresie to głównie nowości dotyczące konkretnych modeli [GLM, MiniMax] - ich wpływ na Twój "workflow z narzędziami i konwencjami" jest niski).
**Film 5:** WF2026 Day Last (Stream - ostatnie ~1,5 godziny)

**Indeks ostatniej części streamu (od 07:42:00 do 09:11:15):**
Start,Koniec,Prelegent,Firma,Tytuł wystąpienia
07:42:34,07:58:10,Theo,Ping / t3.gg,Time to Think Wider
07:58:10,08:19:24,Garry Tan,Y Combinator,Build the AI Native Company
08:19:24,08:37:09,Howie Liu,Airtable,Hiring Employable Agents
08:37:09,09:11:15,Wiele osób,Wiele,"Startup Battlefield Finals (Kamad, Comment.io, Foundry)"

**Ocena 2 wybranych wystąpień z tego bloku:**
Wystąpienie: Garry Tan (Y Combinator) - Build the AI Native Company

**Werdykt:**
Obejrzyj w całości. Wybitne, wizjonerskie spojrzenie na zastąpienie całej struktury narzędzi w coś, co Tan nazywa "Company Brain".Mapa fragmentów:

    08:02:32 - 08:04:35 | Infrastruktura z plików Markdown (5) | Skille to poszczególni "pracownicy", reguły to polityki, tabele resolverów to hierarchia organizacyjna.

    08:08:29 - 08:11:19 | Latent space vs Deterministic space (4) | Nie zlecaj agentowi utrzymywania macierzy danych; LLM to osąd i gust (Latent). Reszta to czysty kod.

    08:11:19 - 08:16:46 | GBrain (5) | Pojemność pamięci agenta to 3 grube książki, Twoja baza wiedzy to wielka biblioteka. Najważniejszy jest system doboru trzech właściwych książek w locie. "Skillify it".Wpływ na Twój workflow:

    (a/b) Masz już AGENTS.md (kontrakty to "pracownicy").

    (b) Reguła "Skillify it": Jeżeli raz wykonasz coś ręcznie w Claude Code (np. spięcie bazy z konkretnym API), eksportuj to natychmiast jako gotowy, zwięzły skill.

**Wystąpienie:** Theo (t3.gg) - Time to Think Wider

**Werdykt:** 
Obejrzyj wybrane fragmenty (pierwsze 10 minut). Leczy z sentymentu do własnego kodu.Mapa fragmentów:

    07:48:49 - 07:51:43 | Skeumorfizm i strach przed usuwaniem kodu (4) | Dlaczego nadal myślimy o programowaniu tak jak przed AI i winimy się za odrzucanie MRów.

    07:51:49 - 07:55:15 | Zmiana progu skomplikowania projektów (4) | Dzisiejszy startup byłby 3 lata temu niewyobrażalnie wielki, a to co było kiedyś "dużym side-projectem" dziś mieści się w jednym pliku Markdown i zadaniu w CRON-ie.

**Analiza Przekrojowa**

Gdzie autorzy mówią to samo lub sobie przeczą:

    Zgodność (Wiedza w Markdownie): Wszyscy (Pocock, Anthropic, Garry Tan z YC) są wyjątkowo zgodni, że przyszłością wiedzy agentowej są proste pliki tekstowe. Tan nazywa to "hiring markdown workforce", Zhang (Anthropic) "folders as skills", a Pocock UBIQUITOUS_LANGUAGE.md.

    Sprzeczności: Matt Pocock wierzy w sztywną kontrolę i konieczność tworzenia deterministycznego TDD jako ograniczników (bad code is expensive). Z kolei Theo (t3.gg) reprezentuje opozycyjne podejście: kodu można się w każdej chwili pozbyć, nie należy się do niego przywiązywać, stary kod (nawet "zły") nie ma już takiego znaczenia.

**Trzy najważniejsze braki w Twoim workflow:**

    Vertical Slices w środowisku z Linear:
    Zmieniłeś Linear w "dziennik pokładowy" dzieląc taski horyzontalnie (osobny ticket na plik/decyzję). Według Pococka (Video 3: 00:42:00), to całkowicie odbiera agentowi szansę na testowanie zintegrowanego kawałka i powoduje spiętrzenie problemów. Agent musi tworzyć plaster ("Vertical Slice": interfejs + API + baza) na jednym tickecie, by go sfotografować (zweryfikować) testem.

    Brak "Zewnętrznej Pętli" (Menedżera):
    Budujesz agenta-workera. Steinberger (Video 4: 00:48:18) i Pocock (Skrypt AFK, Video 3: 00:53:51) wskazują, że faktyczna samodzielność wynika ze stworzenia prostej pętli bash/ts dookoła agenta, która pobiera za niego zadania, wyzwala testy i wystawia ostateczny PR, zamiast Twojej ciągłej interakcji z chatem.

    Brak pętli kompilacji skilli (Skillify it):
    Jeśli szukasz ekosystemu zastępującego MCP, według G. Tana (Video 5: 08:14:42), nie buduj gigantycznych systemów na start. Za każdym razem, gdy zrobisz wartościową sesję w środowisku, musisz mieć nawyk eksportowania tego do osobnego, małego skilla w markdownie, który poszerza "Bibliotekę" (GBrain).

**Kolejność Oglądania:**

**Opcja 1:** Masz tylko 30 minut łącznie (tylko crème de la crème):

    Garry Tan z Y Combinator (Video 5, 07:58:10 - 08:16:46) ~ 18 minut. (Czysta wizja budowy z plików Markdown).

    Matt Pocock: Vertical Slices (Video 3, 00:42:00 - 00:46:18) ~ 4 minuty.

    P. Steinberger: Menedżer Agentów (Video 4, 00:48:18 - 00:52:37) ~ 4 minuty.

    Anthropic: Anatomia Skilli (Video 2, 00:02:53 - 00:04:53) ~ 2 minuty.

**Opcja 2:** Masz 2 godziny:

    Matt Pocock (Całe Video 1) ~ 18 min.

    Anthropic (Video 2, pominąć partnerów) ~ 10 min.

    Garry Tan & Theo (Video 5, 07:42:34 - 08:16:46) ~ 34 min.

    Matt Pocock Workflow (Video 3, wskazane fragmenty z tabeli) ~ 30 min.

    Steinberger & Tisha/Sushin (Video 4, z tabeli) ~ 12 min.

(Zakończenie: Gotowe. Skopiuj ten tekst do wskazanego pliku wyjściowego. Jeśli w przyszłości zechcesz zbadać głębiej środek 8-godzinnych strumieni np. pod kątem debat na temat Loop Engineering, po prostu podaj zakres czasu do przetworzenia w nowym prompcie).