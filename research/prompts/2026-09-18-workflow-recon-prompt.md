# Prompt zwiadowczy dla Gemini Deep Research: mapa powierzchni badawczej workflow agentowego

Użycie: wklej do Gemini z włączonym Deep Research. Przed zatwierdzeniem planu sprawdź listę kontrolną na końcu tego pliku. Wynik zapisz w `research/reports/`.

Wersja 2 (po triage'u wideo, synteza w `research/videos/2026-09-18-video-triage-synthesis.md`): dodane nazwane sygnały z konferencji, punkt o dokumentach kierunkowych, pytanie o pomiar kosztu plików instrukcji.

Prompt zbudowany według heurystyk z projektu DR GEM (Dysk Google, folder „🔬Deep Research GEM"): temat w pierwszym zdaniu, nagłówki jako pola formularza, listy zamiast prozy, jawne wykluczenia, whitelist i blacklist źródeł, wymuszone artefakty, pytania analityczne, podejście eksploracyjne z prośbą o 3–5 kierunków do pogłębienia.

---

Zmapuj powierzchnię badawczą tematu: **workflow pracy solo dewelopera z agentami kodującymi (Claude Code i podobne), od minimalistycznych po zaawansowane, ze szczególnym uwzględnieniem pętli agentowej: specyfikacja → wykonanie → weryfikacja → kryterium ukończenia.**

## Rola

Jesteś architektem procesów wytwarzania oprogramowania specjalizującym się w praktykach pracy z agentami kodującymi. Piszesz raport rozpoznawczy dla jednego doświadczonego dewelopera, który ma podjąć decyzję o kierunku dalszych, węższych badań.

## Kontekst

- Odbiorca pracuje solo, głównie w Claude Code, i utrzymuje kilka repozytoriów.
- Posiada już: hierarchię plików `AGENTS.md` (framework DOX: każdy folder ma kontrakt pracy dla agenta), zestaw skilli, Linear jako tracker issues, CodeRabbit do review PR, docker-mcp-toolkit jako bramkę MCP.
- Raport ma posłużyć do wyboru 3–5 kierunków, w które zostaną wysłane osobne, głębokie badania. Nie ma dawać gotowych rekomendacji wdrożeniowych.
- Wstępny triage wystąpień z AI Engineer World's Fair 2026 wskazał sygnały, które traktuj jako punkt wyjścia, nie jako tezę do potwierdzenia: pionowe plastry funkcjonalności jako jednostka pracy (Matt Pocock), pętla zewnętrzna wokół agenta („manager of agents", Peter Steinberger; skrypt `once.sh` Pococka), separacja czujnika od aktuatora w pętli (Kyle, Human Layer), skille jako foldery z progressive disclosure (Anthropic), „markdown is the workforce" i GBrain (Garry Tan), CLI vs MCP vs skille (Nikita, Salesforce: „jeśli inżynier robi to w terminalu, agent ma użyć CLI"), czujniki deterministyczne zamiast oceny LLM i stan pętli w pliku `feedback.md` w repo (Human Layer), spór „czy człowiek musi czytać kod przed merge" (The Great Loops Debate: trzech z czterech panelistów za czytaniem, Jeff Huntley przeciw pod warunkiem silnego typowania). Poszukaj niezależnych źródeł za i przeciw każdemu z nich.
- Definicje terminów, których używam: - „workflow agentowy": powtarzalny proces, w którym agent LLM wykonuje zadania  programistyczne w repozytorium, a człowiek ustala cel i zatwierdza wynik; - „harness": kod uruchamiający agenta (Claude Code, Codex CLI, Cursor). Poza zakresem; - „pętla": mechanizm, w którym agent po wykonaniu pracy sam weryfikuje ją względem  spisanego kryterium i iteruje, aż warunek jest spełniony; - „BMAD": BMAD-METHOD, framework agentowy z rolami (analityk, PM, architekt, dev, QA)  i szablonami dokumentów; - „AGENTS.md": otwarty standard pliku instrukcji dla agentów kodujących w repozytorium.

## Zadanie

Stwórz mapę obszaru: jakie podejścia, frameworki, moduły i praktyki istnieją, jak są dojrzałe, kto ich używa, co o nich mówią użytkownicy po kilku miesiącach, i gdzie są luki.

## Zakres

Zbadaj kolejno, w tej kolejności:

1. Kompletne frameworki workflow agentowego (BMAD-METHOD, Agent OS, Spec Kit od GitHub, Kiro i podobne): założenia, wymagane artefakty, koszt wejścia, opinie użytkowników po dłuższym użyciu, najczęstsze powody porzucenia.
2. Modułowe elementy, które można przyjąć osobno: standard `AGENTS.md` i hierarchie plików instrukcji, skille (Agent Skills od Anthropic i ich otwarte katalogi), reguły per folder, hooki i komendy slash, MCP jako warstwa narzędzi.
3. Pętle weryfikacji: jak praktycy zapisują kryterium „done" przed startem, separacja wykonawcy od weryfikatora (świeży kontekst, recenzja adwersaryjna), sub-agenci, kolejki feature'ów, komendy typu loop/goal/ralph, ograniczenia weryfikacji przez screenshoty i testy.
4. Warstwa specyfikacji: spec-driven development, prototypy klikalne jako wzorzec weryfikacji, techniki dopytywania przed startem (grill me, PRD w dialogu), gdzie spec żyje w repo.
5. Zarządzanie stanem i wiedzą w repo: rozdział trzech warstw, czyli instrukcji operacyjnych dla agenta (`AGENTS.md`, reguły), trwałych dokumentów kierunkowych (strategia, słownik pojęć, decyzje architektoniczne, polityki) i stanu pracy (spec bieżącego zadania, kolejka, postęp); co z tego trzymać w repo, co w trackerze (Linear, GitHub Issues); udokumentowane antywzorce, w tym tracker używany jako dziennik i pliki instrukcji z zapomnianymi listami todo; jak praktycy mierzą koszt tokenów ładowanych przez hierarchie plików instrukcji i czy progressive disclosure to rozwiązuje.
6. Ekosystemy skilli i narzędzi: katalogi skilli, sposoby dystrybucji między repo, alternatywy dla bramek MCP w stylu docker-mcp-toolkit, koszt utrzymania; rubryki decyzyjne CLI vs MCP vs skill i dane o koszcie kontekstu schematów narzędzi MCP.
7. Badania i dane: publikacje oraz raporty inżynieryjne (Anthropic, OpenAI, Google, METR, zespoły akademickie) o skuteczności długich sesji agentowych, degradacji jakości przy długim kontekście („dumb zone"), self-verification, multi-agent review, wpływie plików instrukcji na jakość, jakości PR generowanych przez agentów versus ludzkich (np. dane Graptile).
8. Skala minimalizmu: opisane w praktyce „najmniejsze działające zestawy" dla solo dewelopera versus pełne systemy; co użytkownicy uznają za nadmiar.

## Ograniczenia

- NIE opisuj budowy własnego agenta ani harnessu (architektura agentów, pętle tool-calling, SDK). Interesuje mnie proces wokół gotowego agenta.
- NIE uwzględniaj materiałów sprzed stycznia 2025, chyba że są cytowane jako źródło pierwotne przez nowsze.
- NIE oceniaj modeli LLM między sobą ani cen subskrypcji.
- NIE streszczaj marketingu producentów bez konfrontacji z opiniami użytkowników.
- Jeśli nie znajdziesz danych liczbowych ze źródłem, wpisz „brak danych"; nie szacuj.

## Źródła

Priorytet (whitelist): dokumentacja producentów (Anthropic, GitHub, OpenAI), repozytoria na GitHub z README i issues, raporty inżynieryjne firm, publikacje arXiv i konferencyjne, blogi praktyków z opisanym własnym wdrożeniem, transkrypty i nagrania wystąpień z AI Engineer World's Fair 2026 (w tym Steinberger, Human Layer, Factory.com, Warp, Salesforce, Anthropic „Tokens should have jobs", The Great Loops Debate, Garry Tan).

Do pominięcia (blacklist): listy „10 najlepszych narzędzi", kursy i społeczności płatne bez publicznej treści, artykuły bez autora i daty, treści generowane masowo.

## Pytania analityczne

Odpowiedz na nie w osobnej sekcji, nie tylko opisuj:

- Dlaczego użytkownicy porzucają kompletne frameworki, a zostają przy modułach? Jakie są dowody?
- Które elementy z punktów 2–5 są wymieniane jako niezbędne przez niezależne od siebie źródła, a które tylko przez ich autorów?
- Czy podział na warstwę operacyjną, kierunkową i stan (punkt 5) ma odpowiedniki w opisanych praktykach, czy jest konstrukcją odbiorcy bez potwierdzenia w źródłach?
- Gdzie źródła są ze sobą sprzeczne?
- Jakie alternatywne podejścia do pętli weryfikacji istnieją poza tymi, które wymieniłem w Zakresie? Czego mogłem nie brać pod uwagę?
- Czego brakuje w opisanym w Kontekście zestawie odbiorcy według zebranych źródeł?

## Format

Raport w Markdown, nagłówki `##` dla każdego punktu Zakresu, potem sekcja Pytania analityczne, potem trzy artefakty:

- **Artefakt A, mapa obszaru:** tabela z kolumnami `obszar`, `reprezentatywne rozwiązania`, `dojrzałość (eksperyment / wczesne / ugruntowane)`, `koszt wejścia (niski / średni / wysoki)`, `główne źródła`.
- **Artefakt B, luki i sprzeczności:** lista punktowana, każdy punkt ze wskazaniem źródeł po obu stronach.
- **Artefakt C, kierunki do pogłębienia:** 3–5 kandydatów na osobne badania, każdy z jednym zdaniem pytania decyzyjnego, które ma rozstrzygnąć, i uzasadnieniem, dlaczego sam zwiad nie wystarczył.

Przy każdym twierdzeniu podaj źródło. Odróżniaj wyraźnie to, co mówią źródła, od własnej syntezy.

---

## Lista kontrolna przed zatwierdzeniem planu badawczego

Z Twoich badań DR GEM: prompt ustala jakość wyniku, plan ustala jakość danych wejściowych. Sprawdź plan, zanim go zatwierdzisz:

- Plan odwzorowuje punkty 1–8 z Zakresu. Jeśli któryś zniknął lub się zlał, dopisz go (dawny limit 8 punktów głównych już nie obowiązuje).
- Punkt 3 (pętle weryfikacji) jest rozwinięty najbardziej. Jeśli plan traktuje go ogólnikowo, dodaj podpunkty: kryterium done, separacja ról, sub-agenci, kolejki.
- W planie nie ma nic o budowie agentów ani porównaniach modeli. Jeśli jest, usuń.
- Plan zawiera krok „zidentyfikuj sprzeczności między źródłami" i krok „wskaż 3–5 kierunków do pogłębienia". Jeśli brak, dopisz jako podpunkty ostatniego punktu.
- Persona z sekcji Rola jest przywołana w pierwszym punkcie planu. Jeśli nie, zostaw: Twoje testy pokazały, że persona i forma są pamiętane z promptu niezależnie od planu.

Po otrzymaniu raportu: Artefakt C staje się wejściem do kolejnych badań, po jednym na przebieg, w Claude Research (wąsko, głęboko) lub ponownie w Gemini Deep Research
(gdy kierunek jest nadal szeroki).
