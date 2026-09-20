## Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?

- URL: https://arxiv.org/abs/2602.11988 (PDF: https://arxiv.org/pdf/2602.11988, wersja v2 wg nagłówka PDF, choć polecenie wskazywało v1)
- Autorzy: Thibaud Gloaguen, Niels Mündler, Mark Müller (LogicStar.ai), Veselin Raychev (LogicStar.ai), Martin Vechev — Department of Computer Science, ETH Zurich (+ LogicStar.ai)
- Data: PDF nosi znak wodny "23 Jun 2026" (arXiv preprint); w poleceniu wskazano luty 2026 — [do weryfikacji], sam PDF pokazuje inną datę niż podana w zadaniu
- Jak zdobyto: `WebFetch` na `https://arxiv.org/html/2602.11988v1` zwrócił jedynie streszczenie wygenerowane przez mały model (z błędnymi liczbami i błędną nazwą benchmarku "AGENTbench" zamiast rzeczywistej "CtxBench") — **nie użyto go jako źródła faktów**. Właściwe dane pobrano przez `curl` do `/tmp/.../scratchpad/eth-agents-md.pdf` (11 stron, potwierdzony prawdziwy PDF arXiv) i odczytano narzędziem Read (strony 1–11, wszystkie).

### Treść

**Co dokładnie mierzono**

- Dwa komplementarne benchmarki:
  - **SWE-bench Lite**: 300 zadań z 11 popularnych repozytoriów Python na GitHubie, żadne nie zawiera commitowanego pliku kontekstowego natywnie (kontekst generowany przez LLM na potrzeby eksperymentu).
  - **CtxBench** (nowy benchmark autorów): 138 instancji z 12 niszowych/nowszych repozytoriów Python, które faktycznie mają committed plik kontekstowy (AGENTS.md/CLAUDE.md) od deweloperów. Zbudowany z puli 5694 PR-ów, pięcioetapowy proces (wyszukiwanie repo z plikiem kontekstowym w root + testami + ≥400 udokumentowanych PR-ów → filtrowanie PR-ów → setup środowiska wykonawczego → generowanie standaryzowanych opisów zadań przez LLM → generowanie testów jednostkowych przez LLM, ręcznie zweryfikowanych). Pokrycie testów: średnio 75% zmodyfikowanego kodu.
  - Statystyki CtxBench (Tabela 1, średnia/min/max): PR body ~415 słów; Issue ~212 słów; kodebase ~3337 plików; PR patch ~118.9 linii / 2.5 pliku; plik kontekstowy ~641 słów / 9.7 sekcji (max 2003 słów / 29 sekcji).
- **Agenci i modele**: Claude Code (Sonnet-4.5), Codex (GPT-5.2 oraz GPT-5.1 mini), Qwen Code (Qwen3-30B-Coder, wdrożony lokalnie przez vLLM). Domyślne ustawienia agentów, temperatura 0 dla Sonnet-4.5/GPT-5.2/GPT-5.1 mini; dla Qwen3-30B-Coder temperatura 0.7, top-p 0.8, kompresja kontekstu przy 60% limitu.
- **Trzy warunki (settings)**:
  - **NONE** — brak pliku kontekstowego (dla CtxBench developer-provided pliki są usuwane).
  - **LLM** — plik kontekstowy wygenerowany automatycznie przez zalecaną komendę inicjalizacyjną danego agenta/modelu na stanie repo sprzed patcha.
  - **DEV** — plik kontekstowy faktycznie dostarczony przez deweloperów (tylko dla CtxBench).

**Dokładne liczby (z podanymi przedziałami niepewności, jak w tekście/tabelach)**

- Tabela 2 (kroki i koszt USD, ± to przedziały błędu podane w tabeli, nie sprecyzowano czy SD czy 95% CI — [do weryfikacji]):
  - SWE-bench, NONE: Sonnet-4.5: 54.4±2.2 kroków, $1.30±0.07; GPT-5.2: 12.5±0.8, $0.32±0.05; GPT-5.1 Mini: 40.9±4.2, $0.18±0.03; Qwen3-30B: 29.7±1.9, $0.12±0.01.
  - SWE-bench, LLM: Sonnet-4.5: 57.2±2.3, $1.51±0.08; GPT-5.2: 12.7±0.8, $0.43±0.05; GPT-5.1 Mini: 45.2±4.2, $0.22±0.03; Qwen3-30B: 32.2±1.9, $0.13±0.01.
  - CtxBench, NONE: Sonnet-4.5: 40.7±3.0, $1.15±0.10; GPT-5.2: 12.1±1.6, $0.38±0.11; GPT-5.1 Mini: 40.6±6.7, $0.18±0.05; Qwen3-30B: 31.5±3.1 [$0.13±0.02] — uwaga: OCR z rysunku tabeli, liczba kroków "31.5" odczytana jako "29.7" w innym miejscu może być błędna, [do weryfikacji].
  - CtxBench, LLM: Sonnet-4.5: 46.5±3.9, $1.33±0.14; GPT-5.2: 13.1±1.5, $0.57±0.18; GPT-5.1 Mini: 46.9±6.4, $0.20±0.04; Qwen3-30B: 34.2±3.4, $0.15±0.02.
  - CtxBench, DEV: Sonnet-4.5: 45.3±3.6, $1.30±0.13; GPT-5.2: 13.6±1.7, $0.54±0.23; GPT-5.1 Mini: 46.6±7.1, $0.19±0.04; Qwen3-30B: 32.8±3.7, $0.15±0.03.
- Sekcja 4.2 (główne wyniki):
  - Pliki kontekstowe generowane przez LLM powodują spadek wyniku w 5 z 8 ustawień (kombinacje benchmark×model).
  - Średni spadek resolution rate: **0.5% na SWE-bench i 2% na CtxBench** (LLM vs NONE), przy p-wartościach **87% i 37%** (dwustronny test) — brak istotności statystycznej.
  - Liczba kroków rośnie w każdym ustawieniu, średnio **o 2.45 (SWE-bench) i 3.92 (CtxBench)**, prowadząc do istotnego (p<0.001) wzrostu kosztów o **20% i 23%** średnio.
  - Pliki developer-provided (DEV) poprawiają wynik agentów średnio o **2.4%** (p=21%, nieistotne), ale istotnie przewyższają pliki LLM-generated (**p=3.8%**, czyli p=0.038 wg Tabeli 3). W abstrakcie/intro sformułowano to też jako "outperform LLM-generated ones by a significant margin of 7% on average".
  - DEV zwiększa liczbę kroków średnio o 3.34 i koszt o maksymalnie 19%.
- Tabela 3 (test Cochrana-Mantela-Haenszla, dwustronny, H0: równe resolution rates):
  - SWE-bench, None vs LLM: p = 0.87
  - CtxBench, None vs LLM: p = 0.37
  - CtxBench, None vs Dev: p = 0.21
  - CtxBench, **LLM vs Dev: p = 0.038** (pogrubione jako istotne)
- Reasoning tokens (Rys. 6, dopasowane instancje, względem baseline NONE):
  - LLM-generated: GPT-5.2 **+22%** na SWE-bench (**+14%** na CtxBench); GPT-5.1 Mini **+10%** na SWE-bench (**+10%** na CtxBench).
  - Developer-provided (tylko CtxBench): GPT-5.2 **+20%**; GPT-5.1 Mini **+2%**.
- Wykrywalność overview w plikach LLM-generated (sędzia: GPT-OSS-120B): **100%** plików generowanych przez Sonnet-4.5 oznaczonych jako zawierające overview, **95%** dla Qwen3-30B-Coder, **99%** dla GPT-5.2, tylko **36%** dla GPT-5.1 Mini.
- Użycie narzędzi specyficznych dla repo: `uv` używane średnio **1.6 razy/instancję** gdy wspomniane w pliku kontekstowym, vs **<0.01 razy** gdy nie wspomniane; narzędzia repo-specific ogólnie **2.5 razy/instancję** gdy wspomniane vs **<0.05 razy** gdy nie.
- Ablacje: modele generujące silniejsze (GPT-5.2+Codex, Sonnet-4.5+Claude Code) pliki kontekstowe dla słabszych agentów (GPT-5.1 Mini, Qwen3-30B) poprawiają wynik o **2% średnio na SWE-bench**, ale **pogarszają o 3% na CtxBench** — silniejsze modele nie generują lepszych plików kontekstowych. Wybór promptu (Codex vs Claude Code) do generowania pliku też nie ma spójnego wpływu.
- Wg §B (nieodczytane w pełni — treść appendixu poza pobranymi 11 stronami, [do weryfikacji na szczegóły]): długość pliku kontekstowego i usuwanie konkretnych kategorii instrukcji nie mają istotnego wpływu na wynik; kontaminacja wiedzą specyficzną dla zadania nie tłumaczy braku poprawy.

**Mechanizm, dlaczego wygenerowane pliki szkodzą (wg autorów)**

- Instrukcje zawarte w plikach kontekstowych są **dobrze przestrzegane** przez agentów (nie jest to problem "instruction-following").
- Prowadzi to do: więcej testowania, szerszej eksploracji repozytorium (więcej `grep`, więcej odczytów i zapisów plików), więcej użycia narzędzi specyficznych dla repo.
- To zwiększa liczbę kroków i liczbę tokenów rozumowania (reasoning tokens) — stąd wyższy koszt — **bez odpowiadającej poprawy skuteczności**.
- Kluczowe zastrzeżenie: pliki kontekstowe **nie skracają** liczby kroków potrzebnych do pierwszej interakcji z plikiem faktycznie istotnym dla zadania (mierzone jako liczba kroków przed pierwszą interakcją z plikiem zmodyfikowanym w oryginalnym PR) — czyli **nie działają jako skuteczne "overview" repozytorium**, mimo że większość z nich takie overview zawiera i mimo że dostawcy modeli/harnessów to rekomendują.
- Dla GPT-5.1 Mini zaobserwowano wprost, że wzrost liczby kroków bierze się z wielokrotnego wydawania poleceń w celu odnalezienia/odczytania pliku kontekstowego (mimo że już jest w kontekście agenta) — zachowanie zaobserwowane tylko gdy plik kontekstowy istnieje.

**Co według autorów zawiera DOBRY plik kontekstowy**

- Cytat (wniosek, sekcja 6): plik kontekstowy powinien zawierać **"only specific additional instructions beyond what is already available in the codebase"**.
- Z sekcji abstrakt/intro: pliki kontekstowe są przydatne do specyfikowania **niestandardowych praktyk kodowania** (non-standard coding practices), a NIE do dawania ogólnego przeglądu repozytorium.
- Cytat (intro): **"Human-written context files should only include instructions required for coding agents that are not already present in the README (e.g., specific conventions or non-functional requirements), and be rigorously evaluated before adoption."**
- Rekomendacja: **pomijać pliki kontekstowe generowane przez LLM** (wbrew rekomendacjom twórców agentów), dopóki nie zostaną lepiej zwalidowane.

**Przykłady plików AGENTS.md (weryfikacja repo z przykładami)**

- W przeczytanych 11 stronach PDF (cały główny tekst + referencje) **nie znaleziono** linku do publicznego repozytorium GitHub z surowymi plikami AGENTS.md użytymi w CtxBench, ani dosłownych fragmentów przykładowych plików kontekstowych (cytaty verbatim). Praca opisuje strukturę statystyczną plików (Tabela 1: liczba słów/sekcji), ale nie cytuje treści.
- [do weryfikacji] — możliwe, że link do datasetu/repo znajduje się w części Appendix (§A–§E), które są wzmiankowane w tekście (np. §E — prompty użyte do konstrukcji CtxBench, §A — szczegóły setupu, §B — analiza długości pliku), ale te strony nie zostały pobrane w tym 11-stronicowym PDF (dokument kończy się na referencjach, strona 11). Nie potwierdzono istnienia dodatkowego appendixu poza tymi 11 stronami.

**Ograniczenia wskazane przez autorów (Sekcja 5)**

- **Języki programowania**: ewaluacja ograniczona do Pythona — języka silnie reprezentowanego w danych treningowych modeli, więc szczegółowa wiedza o tooling/zależnościach może już być w wiedzy parametrycznej modeli, co neutralizuje efekt plików kontekstowych. Niszowe języki/toolchainy mogą dawać inny wynik.
- **Zakres oceny**: praca ocenia tylko wskaźnik ukończenia zadania (task resolution rate); inne aspekty (np. efektywność kodu, bezpieczeństwo) nie były badane — bezpieczeństwo w szczególności okazało się wrażliwe na zmiany promptu w innej pracy (cytowanej jako [37]).
- **Poprawa generowania plików kontekstowych**: otwarty kierunek na przyszłość — wykorzystanie technik planowania i ciągłego uczenia się (continuous learning) z wcześniejszych zadań do generowania bardziej użytecznych plików; praca ta może służyć jako baseline do rygorystycznej oceny takich metod.

### Ocena

**Raport Gemini przekłamał wynik.** Podał „−3% sukcesu" i „+4% dla ręcznych" jako fakty; w pracy spadek to 0,5% i 2% przy p = 0,87 i 0,37, czyli statystycznie nic, a zysk z plików deweloperskich to 2,4% przy p = 0,21, też nieistotny. Jedyny istotny wynik to koszt (+20% i +23%, p < 0,001) oraz przewaga plików ręcznych nad generowanymi (p = 0,038). Prawdziwa teza pracy brzmi więc: **pliki kontekstowe nie pomagają w rozwiązywaniu zadań, a kosztują**, a nie „szkodzą". Kolejny dowód, że liczby z Deep Research trzeba czytać w źródle.

**Co to znaczy dla DOX:**

- Potwierdzenie kierunku „tylko to, czego nie ma w README i kodzie": niestandardowe konwencje, wymagania niefunkcjonalne. Sekcje przeglądowe (mapa repo, opis architektury) nie skracają drogi agenta do właściwego pliku, a to je autorzy wskazują jako zbędne. Nasze Repository Map w root `AGENTS.md` jest dokładnie takim przeglądem; kandydat do wycięcia lub skrócenia po pomiarze.
- Mechanizm jest jasny: agent wykonuje instrukcje sumiennie, więc każda instrukcja typu „uruchom testy", „sprawdź X" to dodatkowe kroki. DOX ma sekcje Read Before Editing i Closeout, które nakazują czytać cały chain i robić przegląd po każdej zmianie. To jest wprost ten mechanizm; koszt trzeba zmierzyć na aid4u.
- Praca mierzy pojedynczy plik w root, 641 słów średnio, do 2003. Hierarchia DOX z kilkunastoma plikami jest poza zakresem badania, w obie strony. Nie da się z niej wyczytać, czy DOX jest lepszy czy gorszy; da się wyczytać, że każdy plik w chainie ma zawierać wyłącznie rzeczy niewyprowadzalne z kodu.
- Ograniczenie do Pythona jest dla nas istotne: nasze repo są w Pythonie, więc modele znają tooling i pliki kontekstowe wnoszą mniej niż w niszowym stacku.
- Silniejsze modele nie piszą lepszych plików kontekstowych. Argument przeciw generowaniu AGENTS.md przez `/init` i za pisaniem ręcznym, co jest zgodne z praktyką użytkownika.

**Do zrobienia:** pobrać appendix (§A–§E), bo tam mogą być przykłady plików i dane o wpływie długości; policzyć tokeny chain AGENTS.md w aid4u dla trzech typowych ścieżek; przejrzeć root `AGENTS.md` tego repo pod kątem sekcji przeglądowych.
