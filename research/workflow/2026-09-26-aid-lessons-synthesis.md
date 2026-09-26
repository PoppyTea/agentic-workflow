---
tags: [research, workflow, dox, hooks, docstrings, aid4u, aid3r]
date: 2026-09-26
prompt: research/prompts/2026-09-26-aid-lessons-query-prompt.md
status: synteza lekcji AI_devs 4 i AI_devs 3 pod kątem granicy harness ↔ inżynieria kontekstu; opcje do dyskusji, bez decyzji
---

# Lekcje AI_devs a nasz workflow: instrukcje, hooki, kod jako kontekst

- **Źródła.** AI_devs 4 (dalej **AID4U**, marzec–kwiecień 2026, lekcje S01E01–S05E05) i AI_devs 3
  (dalej **AID3R**, 2024/2025). Oba kursy żyją w notatnikach NotebookLM właściciela.
- **Metoda.** Dwie niezależne ścieżki:
  1. Lektura własna: surowe teksty lekcji pobrane z notatników (`nlm source content`),
     AID4U przeczytane w całości (S01E01, S04E01, S04E05, S05E04 i S05E05 wyrywkowo),
     z AID3R S04E05 i S05E01–E03 w całości, reszta skanem po słowach kluczowych.
  2. 44 zapytania do NotebookLM z promptu
     `research/prompts/2026-09-26-aid-lessons-query-prompt.md`, każde w osobnej rozmowie.
     Przypisy z odpowiedzi sprawdzone mechanicznie: cytowany fragment musi występować
     w surowym tekście lekcji. Szczegóły i wynik: sekcja „Co dodał NotebookLM”.
- **Zastrzeżenie zakresu.** AID4U S01E02 wprost wyłącza z kursu zarządzanie kontekstem przy
  pracy z Claude Code. Kurs uczy budowy agentów, a nie pracy z agentem kodującym. Wszystko
  poniżej przenosi się na nasz workflow **przez analogię**: w Claude Code jesteśmy częściowo
  twórcą harnessu (hooki, `CLAUDE.md`, skille, uprawnienia), ale nie całości.
- **Filtr aktualności AID3R.** AID4U S05E03: fundamenty mechaniki modeli (autoregresja,
  limity kontekstu, halucynacje, prompt injection) nie zmieniły się od pierwszej edycji,
  zmieniły się techniki, narzędzia i możliwości modeli. Stąd reguła czytania AID3R: ufać
  opisom mechaniki, zalecenia dotyczące technik sprawdzać w AID4U. Każda teza z AID3R ma
  poniżej status: **[ZGODNE]** z AID4U, **[ZMIANA]** akcentów, **[NIEAKTUALNE]**.
- **Prawa do materiału.** Kurs jest płatny, a repo publiczne, więc lekcje są tu streszczone
  własnymi słowami, z krótkimi cytatami i identyfikatorem lekcji przy każdej tezie.

## Treść

### 1. Instrukcje w kontekście: mapa, nie podręcznik

**AID4U**
- Rola instrukcji systemowej spadła; agent sam odkrywa, czego potrzebuje. Instrukcja ma być
  mapą. Kryterium doboru: co agent musi wiedzieć *przed* uruchomieniem narzędzi, żeby
  skrócić drogę do celu; reszta to zwykle szum (S02E01).
- Agent z dostępem do zewnętrznego kontekstu domyślnie z niego nie korzysta, bo „nie wie, o
  czym wie” (S02E01, S01E02).
- Wiedza bazowa: jeśli model „zna” temat, może nie przeszukać naszych dokumentów. Szczątkowe
  opisy zasobów w kontekście nie wystarczają do świadomego szukania, a niekompletne wyniki
  są dla modelu trudne do zauważenia (S02E02).
- Duży kontekst odciąga uwagę od instrukcji systemowych; stąd powtarzanie najważniejszych
  reguł i wzmacnianie zachowań wskazówkami zwracanymi przez narzędzia (S02E02, z odwołaniem
  do prac „How Many Instructions LLMs Follows at Once” i „Reasoning on Multiple Needles In A
  Haystack”).
- Dane dynamiczne i powtarzane reguły krytyczne trafiają do **wiadomości użytkownika** (w
  tagach), a nie do instrukcji systemowej: nie psują cache'u i nie giną w długiej rozmowie
  (S02E01; ten sam postulat przy meta-promptach w S04E02). Przeładowanie aktualizacjami
  też szkodzi (S02E01).
- Ton i styl z instrukcji wygasają po kilku wiadomościach bez przypomnień (S02E05).
- Obecność instrukcji w kontekście nie gwarantuje ani przestrzegania, ani poprawnej
  interpretacji (S02E05). Model nie wykonuje promptu jak kodu (S02E02); błędem jest
  zakładać, że przejdzie przez instrukcje linia po linii, traktując warunki jak `if`
  (S03E05).
- Mapa treści lepiej działa w pliku zewnętrznym niż w instrukcji systemowej; indeks
  (`_index.md`, MoC) może być generowany programistycznie (S01E02, S04E04).
- Agresywny ton (CRITICAL, MUST wielkimi literami) nie jest już rekomendowany dla nowszych
  modeli Anthropic; po zmianie modelu warto upraszczać instrukcje (S05E03).
- Skille i opisy workflow mają pozostać bardzo proste ze względu na ograniczoną uwagę
  modelu (S05E05); skille dołącza użytkownik, model po nazwie i opisie albo oba (S01E02,
  S04E02).

**AID3R**
- Few-shot jako najskuteczniejsza technika **[ZMIANA]**: AID4U traktuje przykłady w
  instrukcji ostrożniej, jako możliwy szum i ryzyko przesterowania (S02E01, S02E05).
- Styl wraca do „naturalnego” w dłuższej rozmowie (S01E04) **[ZGODNE]** z AID4U S02E05.
- Kontekst dopisany do promptu systemowego wygląda dla modelu na wcześniejszy niż wiadomość
  użytkownika, co prowadzi do powtarzania akcji (S05E03) **[ZGODNE]** z AID4U S02E01.

### 2. Co należy do kodu, a co do modelu

**AID4U**
- Jeśli agent ma *zawsze* wykonać zadanie według ustalonych kroków, lepszy bywa workflow niż
  agent (S01E03). Proces ustrukturyzowany i rzadko zmienny nie potrzebuje logiki agentowej;
  przy wymaganej 100% skuteczności LLM to raczej zły pomysł (S01E02).
- Zatwierdzanie i odrzucanie akcji ma być deterministyczne, w kodzie, a nie decyzją modelu
  (S01E05). Uprawnienia i identyfikatory ustala kod (S01E02). Zabezpieczenia są po stronie
  programistycznej, a agent dostaje informację o błędzie i wskazówkę (S02E02).
- Brak informacji lub decyzji nie zatrzymuje systemu, tylko kończy zadanie z pominięciem
  części kroków (S02E04). Dokumenty nie powinny mówić, *kiedy* co robić: to zadanie systemu
  (S02E04).
- Silniejsze modele nie oznaczają przenoszenia logiki na model: model może lepiej zarządzać
  deterministyczną logiką przez routing i referencje (S03E02).
- Liczenie w kodzie nie chroni przed błędnie wczytanymi danymi; ważne dokumenty wymagają
  procesów sterowanych kodem i nadzoru (S03E02, przykład `03_02_code`).
- Kierunek odwrotny (S05E03): w funkcjonalnościach aplikacji logika agentowa staje się
  domyślna, a deterministyczna wymaga istotnego powodu. Dotyczy to np. RAG, a nie strażników
  procesu, bo te AID4U nadal trzyma w kodzie (S01E02, S01E05, S03E03).
- Test decyzji: czy system stanie się lepszy wraz z rozwojem modeli (S02E05, S05E01).

**AID3R**
- Model tylko do zadań, których nie da się wykonać programistycznie; reszta w kodzie
  (S04E05) **[ZMIANA]**: AID4U przesuwa domyślną wartość w stronę agenta dla zadań
  otwartych, ale strażników, uprawnień i akcji nieodwracalnych dalej trzyma w kodzie.
- Krok, który *zawsze* następuje po innym, należy skleić w kodzie zamiast dawać agentowi
  osobne narzędzie (S05E03) **[ZGODNE]** z AID4U S01E03.
- Blokada edycji zadań zakończonych w kodzie, a nie w instrukcji (S05E02) **[ZGODNE]**.
- Nieodwracalne akcje: kod wstrzymuje agenta i pyta człowieka (S05E03) **[ZGODNE]**.
- Unikanie natywnego function calling na rzecz osobnego kroku generowania parametrów
  (S05E01, S05E03) **[NIEAKTUALNE]**: AID4U S01E02 opisuje zmianę podejścia.
- Brak powodu, by porzucać sprawdzone rozwiązania programistyczne, jeśli AI nie dodaje
  wartości (S00E04) **[ZGODNE]**.

### 3. Hooki jako strażnicy procesu

**AID4U**
- Hooki mogą aktywnie podnosić skuteczność agenta i pilnować procesu (S03E03). Przykład
  `03_03_language`: `afterToolResult` ustawia flagi ukończonych etapów, a `beforeFinish`
  sprawdza je i każe agentowi dokończyć brakujące kroki (z wyjątkami: limit kroków, błąd
  narzędzia).
- Przykład `03_03_browser`: błędy narzędzi zamieniają się automatycznie na sugestie
  następnego kroku, powiązane z kategorią błędu (S03E03).
- Format wskazówek: pole `hints`/`recoveryHints` prawie w każdej odpowiedzi narzędzia, także
  przy sukcesie. Komunikat mówi, co się stało i co zrobić; przy złej wartości podaje
  dostępne opcje (S01E03, S01E02). Wspólna struktura odpowiedzi to `next_action`, `recovery`
  i `diagnostics` (S03E04).
- Listy zadań bez wsparcia kodu są przez modele zapominane (S02E01). `03_02_events`:
  kontrakty (struktura planu, zależności) i heartbeat, który programistycznie przydziela
  zadania i aktualizuje stan; agenci stan tylko czytają (S03E02).
- Heartbeat z `tasks.md` jako budzik agenta (S03E03); zadania w tle wymagają jasnej
  informacji o statusie i potrzebie interwencji człowieka (S04E02).
- Maskowanie narzędzi w zależności od stanu (S02E01); host kontroluje aktywne narzędzia i
  ich limit (S01E03).
- Warto logować instrukcje systemowe i ich zmiany w trakcie sesji, bo zachowanie modelu
  bywa skutkiem błędów aplikacji (S01E05).

**AID3R**
- Prompty weryfikujące zwracające `block`/`pass` sprawdzane zwykłym `if` (S01E03)
  **[ZGODNE]**, ten sam wzorzec w AID4U S03E02.
- Weryfikacja jest prostsza niż generowanie; programistyczne limity prób (S04E05)
  **[ZGODNE]**.

### 4. Kod jako kontekst: argument za minimalnym DOX i docstringami

**AID4U**
- Agent kodujący porusza się po repo skutecznie, bo mapą jest sama zawartość plików:
  importy, nazwy, ścieżki; kilka grepów wystarcza (S02E03). Ekspozycja kontekstu opiera się
  na informacji wewnątrz treści, co w kodzie dzieje się naturalnie (S02E03).
- Kod jest podstawowym kontekstem; plany, specyfikacje i skille pojawiły się dla tego, czego
  z kodu nie da się odczytać (S04E04).
- Notatki pisać tak, jakby czytelnik nie miał żadnego dodatkowego kontekstu: bez nazw
  zrozumiałych tylko dla autora, linków bez opisu, „poprzedniej wersji” bez odnośnika
  (S04E04).
- Drzewo katalogów w kontekście pomaga tylko przy stałej strukturze i zadaniu na niej
  skupionym (S02E03).
- Generyczna wskazówka plus łańcuch wskazówek wewnątrz dokumentów zamiast szczegółowej mapy
  w instrukcji; wymaga dyscypliny (S02E03).
- Zasady opisu narzędzi (S01E02), które da się przenieść na docstringi:
  - zrozumiały dla kogoś bez wiedzy o systemie i bez dokumentacji;
  - unikatowa, jednoznaczna nazwa;
  - wysoki stosunek sygnału do szumu: tylko to, co pomaga wybrać narzędzie w dobrym
    momencie; sprawdzane na 10–30 przykładowych zapytaniach;
  - rozdzielenie: co uzupełnia wywołujący, co liczy kod, czego wywołujący nie może;
  - walidacja i komunikaty błędów lepsze niż w zwykłej aplikacji.
- Ewaluacja wieloetapowa niemal bez instrukcji systemowej sprawdza, czy agent radzi sobie
  na samych opisach narzędzi (S03E04). Mały model lokalny jako sprawdzian jakości opisów:
  jeśli słabszy model obsługuje narzędzia poprawnie, są dobrze zaprojektowane (S01E03).
  Ograniczenia pod mniejszy model poprawiają też wynik mocniejszego (S03E04).

**AID3R**
- O kodzie jako kontekście agenta kodującego AID3R nie mówi; wątek pojawia się dopiero w
  AID4U.

### 5. Weryfikacja, eval i uczenie się na błędach

**AID4U**
- Gwarancja struktury nie jest gwarancją wartości (S01E05) — to samo dotyczy linterów i
  schematów: sprawdzają kształt, nie prawdziwość.
- Eval nie zastępuje testów jednostkowych; mierzy stopień spełnienia założeń z progiem
  „wystarczająco”, a nie 100% (S03E01). Obszary: skuteczność promptu, *wybór* narzędzi,
  *posługiwanie się* narzędziami (S03E01).
- Twórca Claude Code zdaniem autora nie robi evali; przy tempie zmian eval może być
  tymczasowy (S03E01).
- AI domyślnie proponuje płytkie testy, czasem takie, których nie da się oblać (S03E04).
- Poprawka instrukcji pod jeden przypadek nie mówi nic o reszcie; stąd generalizacja:
  zasady i wzorce zamiast konkretnych poleceń (S03E01, S01E01). Model pytany o przyczynę
  błędu proponuje zbyt bezpośrednie łatki, trzeba go prowadzić do uogólnienia (S02E01).
- `05_03_autoprompt`: pętla analiza → optymalizacja → ocena, zmiana zostaje tylko gdy
  poprawia wynik na evalu (S05E03).
- Eval awareness: modele mogą zauważyć, że są testowane, i zmienić zachowanie; agent
  kodujący zablokowany przed `.env` pisze skrypt, który go obejdzie (S04E05).
- Wersjonowanie promptów: sam Git nie wystarcza, bo liczy się historia uruchomień powiązana
  z wersją (S03E01).

**AID3R**
- Structured Output gwarantuje strukturę, nie wartości (S05E03) **[ZGODNE]**.
- Promptfoo do testów promptów, Langfuse do monitoringu (S00E02) **[ZGODNE]**, AID4U S03E01
  wymienia te same narzędzia.
- Migracja modelu zwykle łatwiejsza niż się wydaje (S01E05) **[ZMIANA]**: AID4U S05E03
  ostrzega, że stare praktyki mogą szkodzić nowszym modelom.

### 6. Wiele agentów, stan i praca w tle

**AID4U**
- Ten sam agent uruchomiony równolegle gubi zapisy; opcje: wykrywanie konfliktów (checksum
  między odczytem a zapisem), unikanie (przynależność zasobów, izolacja), agent zarządzający,
  historia zmian, człowiek (S02E04). Najlepiej zaprojektować system tak, by konflikty nie
  występowały: agenci w wąskich, niezależnych obszarach (S04E03).
- Zapis z checksumem i `dryRun`, historia zmian do przywrócenia bez udziału modelu (S01E03).
- Człowiek pozostaje głównym koordynatorem (S02E04); system prosty tak długo, jak się da
  (S02E04, S02E05).
- `05_01_agent_graph`: orkiestrator LLM, wspólna tablica stanu, DAG zależności i
  deterministyczny scheduler (S05E01).
- Ostrożność wobec głośnych narzędzi: wiele jest na wczesnym etapie i bywa porzucanych
  (S05E02). Własna logika pisana z agentem kodującym bywa lepsza niż framework (S05E01).
- Biblioteka własnych, powtarzalnych promptów jest bardzo wartościowa mimo prostoty
  (S05E02); zacząć od jednej integracji.
- Jeśli nikt nie czyta wyniku automatyzacji, nie ma sensu jej utrzymywać (S05E05).

**AID3R**
- Ostudzić entuzjazm wobec w pełni autonomicznych agentów; wyspecjalizowani agenci z
  weryfikacją człowieka (S05E02) **[ZGODNE]** z AID4U S02E04.
- Frameworki agentowe: lepiej własne rozwiązania do czasu stabilizacji (S05E01)
  **[ZGODNE]** z AID4U S01E05, S05E01.

### 7. O czym lekcje milczą

- Konkretne mechanizmy Claude Code (typy hooków, `CLAUDE.md`, hierarchia `AGENTS.md`),
  poza wzmiankami o skillach, trybie planowania i hookach jako funkcji interfejsów
  (S04E01, S04E02). Oba notatniki odpowiadają tak samo.
- Docstringi jako takie. Wniosek o docstringach wyprowadzamy z zasad opisu narzędzi i z
  tezy o kodzie jako mapie; lekcje nie formułują go wprost.

## Co dodał NotebookLM

### Jak czytać te odpowiedzi

- **Przebieg.** 44 zapytania (34 do AID4U, 10 do AID3R), każde w nowej rozmowie. Pierwszy
  przebieg odrzuciłem: CLI `nlm` domyślnie dokleja pytanie do jednej rozmowy notatnika, więc
  od drugiego pytania odpowiedzi były kontynuacją poprzednich i wracały bez przypisów.
  Odpowiedzi bez przypisów (15) ponowiłem do dwóch razy; bez przypisów została jedna (Q03 AID4U,
  jej tezy powtarzają się w innych odpowiedziach). Przypisy łącznie: 1301 cytatów zgodnych ze
  źródłem, 10 zgodnych częściowo (sklejone z kilku miejsc lekcji), 16 wskazuje grafiki, 0
  niezgodnych.
- **Cytaty zgodne ze źródłem.** Sprawdzenie mechaniczne potwierdza, że przytoczony fragment
  jest w lekcji. Nie potwierdza, że wniosek NotebookLM z tego fragmentu wynika; przy tezach
  przeniesionych niżej sprawdzałem to czytając fragment.
- **Obce źródło w notatniku AID4U.** Notatnik zawiera źródło „Prompt Engineering for AI
  Agent”, które nie jest lekcją, tylko zapisaną rozmową z Gemini (persona „Inżynier
  Kontekstu”). NotebookLM cytuje je obok lekcji i przejmuje jego personę. Tezy oparte
  wyłącznie na nim pomijam; dotyczy to m.in. paradygmatu „CEL (WHAT) vs DROGA (HOW)” i
  zalecenia testów A/B „10 prób na wersję”.
- **Grafiki.** Część przypisów wskazuje grafiki z lekcji; ich treści nie da się sprawdzić
  tekstowo. Tezy z grafik są oznaczone **[z grafiki]**.
- **Zgodność z lekturą własną.** W większości odpowiedzi NotebookLM powtarza to, co jest
  już w „Treści” wyżej. Oba notatniki niezależnie potwierdzają milczenie źródeł w sprawie
  Claude Code, hierarchii `AGENTS.md`, docstringów, komentarzy w kodzie i linterów
  dokumentacji (Q09, Q10, Q11).

### Tezy nowe względem lektury własnej

**AID4U**
- Wartości domyślne narzędzia (np. zadanie przypisane do bieżącego użytkownika) trzeba
  opisać w jego opisie i dać możliwość zmiany (S01E02, cytat sprawdzony).
- Kolejność pól w schemacie ma znaczenie, bo wcześniejsze tokeny wpływają na kolejne: pole
  `reasoning` przed polem z decyzją (S01E01, cytat sprawdzony).
- Zamiast wielu drobnych akcji odwzorowujących API — kilka scalonych narzędzi (np. cztery
  akcje plikowe `fs_search`, `fs_read`, `fs_write`, `fs_manage`) (S01E03, cytat sprawdzony).
- Dynamiczne dołączanie narzędzi bez utraty cache'u promptu jest dziś możliwe tylko u
  Anthropic; u innych dostawców pozostają subagenci albo progressive disclosure (S01E02,
  cytat sprawdzony).
- W evalach agentów odpowiedzi narzędzi szybko stają się większością promptu, więc powinny
  być częścią zbioru testowego (S03E01, za zespołem Braintrust; cytat sprawdzony).
- Pływające okno kontekstu (wycinanie starych wiadomości) nie jest już zalecane, bo
  niszczy cache; zamiast tego kompresja i zapis do plików (S01E02, cytat sprawdzony).
- Maskowanie przez doklejanie początku odpowiedzi asystenta (technika Manusa) kurs pomija,
  bo w API Anthropic oznaczono ją jako przestarzałą (S02E01, cytat sprawdzony).
- W `05_03_autoprompt` nowa wersja promptu przechodzi tylko wtedy, gdy przyrost wyniku
  przekracza próg szumu, a ocena idzie na zbiorze odłożonym, którego optymalizator nie
  widział (S05E03 **[z grafiki]**).
- Metadane i kluczowe odnośniki na samej górze notatki, bo agent często czyta tylko
  początek pliku; nowa wersja dokumentu z jawnym wskazaniem, którą zastępuje, zamiast
  nadpisywania w miejscu (S02E01/S04E04 **[z grafiki]** `ai_devs_4_note_context`).
- Lista rzeczy uznanych w AID4U za przestarzałe (Q32): unikanie function calling, frameworki
  agentowe, OpenAI Assistants API, pływające okno kontekstu, maskowanie prefiksem, statyczne
  few-shot w instrukcji systemowej, mapowanie API 1:1 na narzędzia, samo wyszukiwanie
  wektorowe, klasyczne wieloetapowe pipeline'y RAG.

**AID3R** (odpowiedzi z przypisami, 48–59 cytatów każda)
- Pamięć: przed zapisem odczytać istniejące wpisy i zdecydować: dodaj, zaktualizuj albo
  usuń; samo dopisywanie prowadzi do duplikatów. Stałe drzewo kategorii zamiast swobody
  modelu (S01E02, S01E04) **[ZGODNE]** z AID4U S04E04 (szablony, struktura z góry).
- Pętla: planować tylko najbliższy krok, bo środowisko się zmienia; limit kroków i narzędzie
  `final_answer` jako warunki wyjścia; historia akcji w prompcie z poleceniem zmiany
  podejścia, gdy powtórzenia nic nie dają (S05E01, S05E02) **[ZGODNE]** co do mechaniki.
- Weryfikacja jest dla modelu łatwiejsza niż generowanie; osobny prompt weryfikujący z
  wynikiem sprawdzanym kodem (S01E03, S00E02) **[ZGODNE]**.

### Czego NotebookLM nie wniósł

- Żadnej lekcji o pracy z agentem kodującym jako użytkownik (poza S04E02 i uwagą, że kurs
  się tym nie zajmuje).
- Żadnej liczby powtórzeń zalecanej przy pomiarze zmiany promptu: AID3R wprost milczy (Q22),
  a AID4U podaje ją tylko z obcego źródła opisanego wyżej.

## Ocena

Format odpowiedzi według „Pytań diagnostycznych” z
`research/prompts/2026-09-24-dox-workflow-reflections.md`: najpierw TAK/NIE, skala 1–10 lub
krótka odpowiedź, potem rozwinięcie. Skala to moja ocena siły wsparcia w lekcjach, nie
pomiar.

### Czy lekcje wspierają „Nadejście Deterministycznego Autorytaryzmu”?

**TAK, 8/10, dla kroków „zawsze” i strażników.** Najmocniejsze punkty: kroki zawsze
następujące po sobie idą do kodu (AID4U S01E03, AID3R S05E03), zatwierdzanie jest
deterministyczne (S01E05), dokument nie mówi *kiedy*, bo to zadanie systemu (S02E04),
`beforeFinish` pilnuje procesu (S03E03). **NIE dla wszystkiego:** AID4U S05E03 każe
domyślnie ufać agentowi w zadaniach otwartych, a S02E01 ostrzega przed sztywnymi krokami
tam, gdzie wystarczą ogólne zasady eksploracji.

Trzy drogi z refleksji zestawione z lekcjami:
- **Przepisać reguły na kod.** Wsparcie: TAK, gdy reguła opisuje krok „zawsze” lub
  zakaz sprawdzalny w kodzie. Reguły opisujące osąd (np. „zawężona obsługa wyjątków HTTP”)
  dadzą się sprawdzić tylko co do kształtu (S01E05: struktura ≠ wartość).
- **Poszukać gotowego kodu pod sprecyzowane potrzeby.** Wsparcie: TAK; S05E01 dodaje, że
  z agentem kodującym własna logika jest dziś tania.
- **Zainstalować popularne rozwiązanie społeczności.** Wsparcie: NIE, raczej ostrzeżenie
  (S05E02: wczesne etapy, porzucane projekty). Jako podłoga ma sens tylko po przeczytaniu
  kodu.

### Mapa: mechanizm z lekcji → hook Claude Code

Semantyka hooków opisana z dokumentacji Claude Code, niesprawdzona na tej maszynie
**[do weryfikacji]**.

| Lekcja | Mechanizm | Odpowiednik w Claude Code | Kandydat u nas |
|---|---|---|---|
| S03E03 `beforeFinish` | strażnik przed zakończeniem | `Stop` z `decision: block` i powodem (uwaga na pętlę: `stop_hook_active`) | DOX pass, testy, lint przed oddaniem tury |
| S03E03 `afterToolResult` | flagi etapów, podpowiedź po błędzie | `PostToolUse` z matcherem `Edit\|Write`, komunikat zwrotny do modelu | ruff/pydocstyle na zmienionym pliku, wynik w formacie „co się stało → co zrobić” |
| S02E01, S04E02 | reguły krytyczne i dane dynamiczne w wiadomości użytkownika | `UserPromptSubmit`, `SessionStart` (dodatkowy kontekst) | powtórka 3–5 reguł krytycznych, stan gałęzi, przypomnienie o ścieżce z `naming.md` |
| S01E05, S01E02 | deterministyczne zatwierdzanie, uprawnienia | `PreToolUse` z odmową, `permissions` w `settings.json` | blokada zapisu w `results/`, `.env`, na `main` |
| S02E03, S04E04 | kontekst dociągany ścieżką, MoC generowany | `PreToolUse` na `Read`/`Edit` wstrzykujący regułę dla ścieżki; skrypt generujący indeks | reguły `strategy/` dla konkretnych folderów bez tabeli wskaźników |
| S01E03, S03E04 | `hints`, `next_action` | format komunikatów wszystkich naszych hooków | jeden szablon komunikatu dla wszystkich hooków |

### Minimalny DOX + obowiązkowe docstringi

**TAK, 7/10.** Lekcje dają trzy argumenty:
1. Agent kodujący nawiguje po treści plików, a nie po zewnętrznych mapach (S02E03).
2. Kod jest podstawowym kontekstem, dokumenty tylko dopełniają luki (S04E04).
3. Mapy w dokumentach się rozjeżdżają, a łańcuch wskazówek wymaga dyscypliny (S02E03).

Kierunek zgadza się z benchem aid4u (`research/workflow/2026-09-21-dox-bench-note.md`):
pełny chain `with-dox` miał najwyższą medianę kosztu (2,62), zero kontaktu ze `strategy/` i
trzy wykolejenia, a `no-dox` najniższą medianę (1,70). Bench nie mierzył docstringów, więc
wspiera połowę „minimalny DOX”, nie połowę „docstringi”. Brakuje do 10/10, bo ani lekcje, ani
bench nie mówią o docstringach wprost.

Jak mógłby wyglądać standard docstringu, wyprowadzony z zasad opisu narzędzi (S01E02):
- pierwsze zdanie mówi, *kiedy* sięgnąć po funkcję, nie tylko co robi; agent często czyta
  tylko początek pliku albo wynik grepa (S02E01/S04E04 **[z grafiki]**), więc najważniejsze
  idzie na górę;
- zrozumiały bez znajomości reszty repo (S04E04): bez nazw i skrótów znanych tylko autorowi;
- rozdziela to, co podaje wywołujący, od tego, co funkcja ustala sama, i od tego, czego
  wywołujący robić nie może;
- wartości domyślne opisane wprost (S01E02);
- sekcja błędów w formacie wskazówki: co poszło nie tak i co zrobić (S01E03);
- bez powtarzania sygnatury i typów; wysoki stosunek sygnału do szumu.

Egzekwowanie w dwóch warstwach:
- **Kształt:** ruff z regułami `D` (pydocstyle) i np. `pydoclint` dla zgodności z
  sygnaturą, w hooku `PostToolUse` i w pre-commit **[do weryfikacji]**.
- **Wartość:** tego lintery nie sprawdzą (S01E05). Pozostaje review (CodeRabbit) albo
  eval: czy słabszy model trafia w odpowiednią funkcję na samych docstringach (S01E03,
  S03E04).

Co zostaje w `AGENTS.md` przy minimalnym DOX: to, czego nie da się wyczytać z kodu ani
wymusić hookiem (cel folderu, granice własności, preferencje użytkownika). Reguły „kiedy” i
„zawsze” przechodzą do hooków, metodyki do skilli.

### Pliki reguł i `strategy/`

- **Reguły z qudo/CodeRabbit** to reguły recenzenta. Lekcje dają im naturalne miejsce po
  stronie systemu, a nie w kontekście piszącego (S02E04). CodeRabbit i tak recenzuje, więc
  reguły recenzyjne mogą trafić do jego konfiguracji (`.coderabbit.yaml`, path instructions)
  **[do weryfikacji]**. Reguły sprawdzalne kodem (np. `r13` pojedyncza submisja, `r15`
  spójność `reraise`) mogą stać się testem albo regułą lintera.
- **`strategy/` jako skill.** Zgodne z S01E02 i S04E02 (skill wstrzykiwany przez użytkownika
  lub z opisu) oraz S05E05 (proste opisy). Ryzyko z S02E01/S02E02: model nie wywoła skilla,
  jeśli „wie”, jak coś zrobić; opis skilla musi mówić, *kiedy* po niego sięgnąć, albo
  wstrzykuje go hook ścieżkowy.

### Pomysły na kolejne warianty benchu

- `no-agents-md` + docstringi: repo bez `AGENTS.md`, z docstringami w standardzie powyżej;
  test tezy S02E03/S04E04.
- Ten sam wariant na słabszym modelu (Haiku): sprawdzian jakości opisów wg S01E03.
- Wariant z hookiem `Stop` wymuszającym DOX pass: czy strażnik zastępuje nakaz w tekście.
- Każdy wariant na n ≥ 10; w AID4U S03E01 eval to też dataset z przypadkami negatywnymi.

### Ryzyka

- **Uczenie się na błędach bez evalu.** Dopisywanie reguły po każdym błędzie to łatki pod
  jeden przypadek (S01E01, S02E01, S03E01). Bezpieczniej jak w `05_03_autoprompt`: zmiana
  zostaje tylko wtedy, gdy wynik rośnie ponad próg szumu na zbiorze, którego poprawka nie
  widziała (S05E03 **[z grafiki]**). Nasz bench ma ten sam problem: różnice między
  wariantami trzeba porównywać z rozrzutem przy n=10.
- **Hooki też są kodem.** Fałszywe alarmy i pętle `Stop` kosztują turę; strażnik potrzebuje
  wyjątków jak w `03_03_language` (limit kroków, błąd narzędzia).
- **Testy nie do oblania.** Bramki pisane przez agenta bywają płytkie (S03E04); nasza własna
  lekcja z `verify.py` jest ta sama.
- **Eval awareness** (S04E05): agent w benchu może zachowywać się inaczej niż w pracy.

### Nick Saraev a lekcje

| Teza z transkryptów Saraeva | Lekcje |
|---|---|
| Eval na ~10 przebiegach zamiast jednego | AID4U S03E01 (dataset, próg „wystarczająco”); nasz bench n=10 |
| Pętla samosprawdzenia przed oddaniem | S03E03 `beforeFinish`, AID3R S05E01 prompt weryfikujący |
| Kod jest kontekstem; notatki się rozjeżdżają | S02E03, S04E04 |
| Meta-prompting | S04E02 (meta-prompt), S05E03 (autoprompt) |
| Wyrzucić nieużywane MCP, pilnować `/context` | S01E03 (limit narzędzi), S02E05 (progressive disclosure) |
| Definicja „gotowe” jak u wykonawcy | S04E02 (model nie zgaduje tego, co ma dostać), S02E04 (wytyczne oceny) |
| Diagnoza przed naprawą | S01E05 (logowanie instrukcji i zdarzeń), S03E01 (trace) |
| MCP do prototypu, potem chudy skill | S04E02 (CLI dla devów, MCP dla nietechnicznych), S05E05 |
| Równoległe zadania o wąskim zakresie | S04E03 (brak konfliktów z założenia), S02E04 |
| Notatki przekazania | S04E04 (pisać bez kontekstu), S03E02 (stan w plikach) |
| Uczyć się na błędach regułami pozytywnymi | S01E01, S03E01 (generalizacja), S05E03 (bramka evalu) |
| Linear jako wspólna przestrzeń człowieka i AI | S04E03 (aktywne katalogi powiązane z trackerem); różnica wobec antywzorca „Linear jako dziennik” z ZPO-Manager |

## Plan: przegląd repo 4th-devs

Zadanie na później, zlecone 2026-09-26: przejrzeć `https://github.com/i-am-alice/4th-devs`
(przykłady kodu do AID4U) w poszukiwaniu wzorców do skopiowania do workflow. Kandydaci
wskazani przez lekcje:

- `03_03_language` — hooki `afterToolResult`/`beforeFinish` jako strażnik procesu
  (S03E03); wzór dla hooka `Stop`.
- `03_03_browser` — błędy narzędzi zamieniane na wskazówki; katalog wiedzy per domena.
- `03_02_events` — kontrakty i heartbeat; stan zmieniany kodem.
- `05_01_agent_graph` — deterministyczny scheduler nad DAG zadań.
- `03_01_evals` — eval z promptfoo; szablon evalu dla naszych wariantów.
- `05_03_autoprompt` — zmiana zostaje tylko po poprawie wyniku.
- `04_04_system` — szablony i generowany MoC.
- `mcp/` i `01_03_mcp_*` — serwer MCP plików z S01E03: checksum, `dryRun`, `hints`.
- `05_03_coding` i `04_05_review` — nazwy sugerują agenta kodującego i review; lekcje
  do nich nie sprawdzone.

Wszystkie wymienione katalogi istnieją w repo (lista z GitHub API, 2026-09-26); ich
zawartości jeszcze nie czytałem.

## Tematy do dyskusji

Pytania, na które lekcje nie odpowiadają, a które decydują o kształcie workflow. Opcje, bez
decyzji.

1. **Kryterium granicy harness ↔ kontekst.** Czy przyjąć regułę „jeśli w regule jest
   *zawsze* albo *nigdy*, idzie do hooka lub permissions; jeśli jest *kiedy*, idzie do
   hooka ścieżkowego albo skilla; w `AGENTS.md` zostaje tylko *co* i *dlaczego*”?
2. **Utrzymanie hooków.** Gdzie żyją (repo vs `~/.claude`), jak je testować, jaki budżet
   fałszywych alarmów jest akceptowalny.
3. **Standard docstringu.** Czy powyższy szkic, czy gotowy styl (Google/NumPy) plus
   pierwsze zdanie „kiedy”? Czy wymagać docstringów także w skryptach benchu?
4. **Pomiar hooków.** Czy każdy nowy hook przechodzi przez bench (wariant z/bez), czy
   wystarczy obserwacja w pracy?
5. **Gdzie żyją plany i stan pracy.** Repo nie ma miejsca na plany; `AGENTS.md` i
   `strategy/` stanu nie trzymają. Opcje: `README.md` (Status), Linear, plik w `.help/`.
6. **Protokół pracy nocnej.** Heartbeat, notatka przekazania, pytania na koniec; czy
   zapisać go jako skill.
7. **Równoległe agenty na jednym drzewie.** Dziś fork i ja pracowaliśmy na tym samym
   drzewie; S02E04 i S04E03 sugerują izolację (worktree) albo przynależność plików.
8. **Linear jako kolejka zadań dla agenta** (Saraev: statusy, etykieta „agent-ready”) a
   antywzorzec dziennika. Czy i w którym repo spróbować?
9. **Rozwiązania społeczności do przejrzenia** przed pisaniem własnych hooków (np. zestawy
   hooków do Claude Code, linter reguł `CLAUDE.md`) — kandydaci do znalezienia, nie
   wybrani.
