# Synteza triage'u wideo (Gemini, dwa raporty A i B)

- Źródła: `research/reports/2026-09-18-video-triage-report-a.md`, `-report-b.md`, `-pass2-report.md` (drugie podejście, wystąpienia 3, 6, 8)
- Prompt: `research/prompts/2026-09-18-video-triage-prompt.md`
- Przetworzone: Gemini dał dwie odpowiedzi w teście A/B; obie analizują filmy 1–3 w całości,
  a streamy 4–5 częściowo. A zbudował pełny indeks obu streamów z audio, B przeanalizował
  wizualnie tylko pierwsze 2 h dnia 1 i ostatnie 1,5 h dnia ostatniego. Raporty się
  uzupełniają, nie przeczą.
- Zastrzeżenie: timestampy w streamach pochodzą z audio, przesunięcia rzędu kilkudziesięciu
  sekund między A i B są normalne. Nic z tego nie zweryfikowałem sam `[do weryfikacji]`.

## Treść

### Werdykty per film (zgodne w A i B)

| Film | Werdykt | Kluczowe fragmenty |
|---|---|---|
| 1. Pocock, Software Fundamentals (18 min) | Obejrzyj w całości | 04:22–07:20 `/grill-me`; 09:41–11:30 TDD jako ogranicznik; 11:31–16:32 głębokie moduły |
| 2. Anthropic, Build Skills (16 min) | Obejrzyj początek i koniec, środek (05:00–11:00) to partnerzy | 02:57–04:53 skille = foldery, progressive disclosure; 07:34–09:12 MCP vs skille; 13:20–14:32 agent zapisuje własne skille |
| 3. Pocock, Full Walkthrough (1h36) | Tylko fragmenty, ok. 25–30 min | 03:06–08:45 smart/dumb zone; 39:39–49:20 vertical slices i issues jako pliki; 53:51–01:04:00 pętla AFK (`once.sh`); 01:14–01:33 push vs pull standardów |
| 4. WF2026 dzień 1 (8h37) | Wybrane wystąpienia | Steinberger (OpenAI) 00:48 „Manager of Agents"; Chronicle 01:37 logowanie na granicach; Factory.com 02:10 kryteria wyjścia z pętli; Kyle/Human Layer 06:46 teoria sterowania; Zach Lloyd/Warp 04:55 self-improving factories |
| 5. WF26 dzień ostatni (9h11) | Wybrane wystąpienia | Nikita/Salesforce 02:20 CLI vs MCP vs skille; Anthropic 01:56 „Tokens should have jobs"; Great Loops Debate 03:40 (60 min); Garry Tan 07:59 „Markdown is the workforce", GBrain; Theo 07:42 |

Indeks obu streamów z czasami startu wystąpień jest w raporcie A. Dwie różne listy
„na 30 minut": A daje film 2 plus film 1, B daje Tana, vertical slices, Steinbergera
i anatomię skilli.

### Sygnały wspólne dla obu raportów i wielu prelegentów

1. **Plik na dysku jako jedyna abstrakcja.** Pocock (`UBIQUITOUS_LANGUAGE.md`, issues jako
   `.md`), Anthropic (`SKILL.md` w folderach), Tan („markdown workforce": skille to
   pracownicy, reguły to polityki). Nikt nie proponuje Pythona ani bazy jako spoiwa.
2. **Dopytanie przed pracą.** `/grill-me` (film 1, 05:43): „Interview me relentlessly
   about every aspect of this plan until we reach a shared understanding." Plan Mode
   w Claude Code oceniony jako zbyt pochopny (06:55).
3. **Pionowe plastry zamiast warstw.** Agent koduje warstwowo (cała baza, potem całe
   API) i sprzężenie zwrotne przychodzi dopiero na końcu; ticket ma obejmować
   przekrój baza+API+UI (film 3, 42:57).
4. **Krótki kontekst, świeży weryfikator.** Powyżej ~100k tokenów jakość spada (film 3,
   04:10); reset zamiast kompaktowania (07:31); review ze świeżego kontekstu, bo
   recenzent w starym kontekście jest „głupszy" od implementatora (01:05:32).
5. **Pętla zewnętrzna wokół agenta.** `once.sh` (film 3, 54:24): pobierz jeden plik
   zadania, ostatnie 5 commitów, uruchom `claude --permission-mode accept-edits`, zakończ.
   Steinberger (WF4, 00:48): agent-menedżer podnosi workera, potem reviewera, oddaje PR.
6. **Wykonawca ≠ czujnik.** Kyle/Human Layer (WF4, 06:46): teoria sterowania, testy
   i grep jako czujniki, agent jako aktuator. Zbieżne z regułą z wideo AI LABS.
7. **MCP dostarcza I/O, skill mówi co z tym zrobić.** Anthropic (film 2, 08:22);
   Nikita/Salesforce (WF5, 02:20) o wyborze CLI vs MCP vs skill.
8. **„Skillify it".** Tan (WF5, 08:14): każdą wartościową sesję eksportuj jako mały
   skill; Anthropic (film 2, 13:35): agent sam zapisuje skrypt wielokrotnego użytku.
9. **Latent vs deterministic.** Tan (08:08): LLM to osąd i gust, resztę robi zwykły kod.

### Drugie podejście (B2): Human Layer, Salesforce, Loops Debate

Gemini przetworzył tylko trzy z dziesięciu wskazanych wystąpień i przyznał, że
„wizualia" zrekonstruował z narracji, nie z obrazu. Wnioski cementują pierwszy triage,
dokładają trzy konkrety:

- **Kyle, Human Layer (WF4, 06:46–07:03).** Pętla jako układ sterowania: czujnik →
  kontroler → aktuator. Czujnikiem ma być kod deterministyczny (`ast-grep`, lintery),
  nie ocena LLM: „nigdy nie wysyłaj agenta do pracy, którą może wykonać kod
  deterministyczny" (06:57:56). Stan pętli to plik `feedback.md` w repo, pętla w GitHub
  Actions blokuje się, gdy poprzedni PR jest jeszcze otwarty (07:00:21).
- **Nikita, Salesforce (WF5, 02:20–02:33).** Taksonomia: CLI to śrubokręt, MCP to hub
  USB-C, skill to runbook. 50 schematów narzędzi MCP potrafi zjeść 60% okna kontekstu
  przed startem zadania (02:22:03). Heurystyka: jeśli inżynier robi to w terminalu,
  agent ma użyć CLI, nie serwera MCP (02:24:38). Izolację bezpieczeństwa robi się
  w infrastrukturze, nie w prompcie (02:29:24). Pytanie decyzyjne: „kto jeszcze tego
  potrzebuje?" rozstrzyga, co zostaje w bramce MCP, a co idzie do lokalnego CLI.
- **The Great Loops Debate (WF5, 03:40–04:40).** Jedynie Jeff Huntley (Ralph Loop)
  broni merge bez czytania kodu, opierając się na typach i pre-commit hookach (04:37:29).
  Horthy, Greg z Sentry i Livingstone: człowiek czyta kod, bo test ≠ jakość, agenci
  produkują złożoność, a odpowiedzialność prawna i tak spada na człowieka. Kryterium
  done: narzędzia domykają rzeczy deterministyczne, człowiek domyka architekturę.

### Sprzeczności wskazane przez Gemini

- **Czytać kod czy nie.** Pocock i Dex Horthy (Loops Debate): człowiek musi czytać kod
  przed merge, „lights-off factory" to kłopoty. Anthropic, Jeff Huntley, Theo: kod jako
  czarna skrzynka, nie przywiązuj się, stary kod nie ma znaczenia.
- **TDD jako ogranicznik vs kod jednorazowy.** Pocock: zły kod jest droższy niż
  kiedykolwiek. Theo: kod można wyrzucić w każdej chwili.

### Braki w naszym workflow według Gemini (A i B razem)

- **Bufor dekompozycji przed pętlą:** po `/grill-me` zrzut małych zadań do plików `.md`
  w repo; pętla je zjada po kolei; Linear dostaje co najwyżej poziom epiku.
- **Pętla zewnętrzna (menedżer):** skrypt, który pobiera zadanie, odpala agenta,
  uruchamia testy, wystawia PR. Bez tego Claude Code jest tylko workerem.
- **Czujnik oddzielony od aktuatora:** kryterium done nie może definiować agent-koder.
- **Progressive disclosure w DOX:** do kontekstu trafiają nagłówki, treść ciągnięta
  na żądanie. Gemini sugeruje, że DOX ładuje za dużo „od wejścia" `[do weryfikacji]`.
- **Pętla kompilacji skilli:** nawyk eksportu sesji do skilla.

## Ocena

### Co z tego wynika dla projektu

- Trzy elementy pokrywają się w pięciu niezależnych źródłach i z wideo AI LABS:
  spec przed pracą, pionowe plastry jako jednostka pracy, weryfikator ze świeżym
  kontekstem. To jest kandydat na „minimum do samodzielnej pracy" i powinien być
  pierwszym kierunkiem pogłębienia.
- Antywzorzec z ZPO-Manager (Linear jako dziennik) jest dokładnie tym, co Pocock
  nazywa cięciem horyzontalnym. Naprawa to nie „mniej issues", tylko inna jednostka:
  plaster funkcjonalności, a nie plik czy decyzja.
- **Pliki strategii wpisują się w sygnały** z paneli: Tan rozdziela skille (pracownicy),
  reguły (polityki) i tabele resolverów (hierarchia); Pocock ma osobny słownik
  `UBIQUITOUS_LANGUAGE.md`; Anthropic trzyma wiedzę proceduralną w folderach z krótkim
  nagłówkiem. Wspólny mianownik: trwałe dokumenty kierunkowe żyją osobno od stanu
  pracy i osobno od instrukcji operacyjnych. To potwierdza, że rozdział
  „AGENTS.md = kontrakt, strategia = kierunek, stan = w artefakcie" jest sensowny.
  Do sprawdzenia na przykładach z ZPO i AID4U, czy nasze pliki strategii faktycznie
  nie przemycają stanu.
- Progressive disclosure jako zarzut wobec DOX wymaga pomiaru, nie wiary: ile tokenów
  ładuje chain AGENTS.md w aid4u przy typowej sesji.
- Skrypty Pococka (Sand Castle, TypeScript) Gemini ocenia jako zbyt ciężkie dla nas;
  `once.sh` jako wzorzec minimalny jest wystarczający na start.
- Po B2 sprzeczność „czytać kod czy nie" przestaje być symetryczna: trzech z czterech
  panelistów i Pocock są po stronie czytania, a jedyny głos przeciw warunkuje to silnym
  typowaniem, którego w naszych projektach (Python) nie ma. Ostrożne podejście
  z CodeRabbit i człowiekiem na końcu nie jest zaległością.
- Taksonomia CLI/MCP/skill daje gotowe kryterium do audytu docker-mcp-toolkit: każdy
  serwer w bramce przepuścić przez pytanie „czy robię to w terminalu" i „kto jeszcze
  tego potrzebuje". To zadanie na short-run, nie long-run.
- `feedback.md` jako stan pętli w repo to kolejny argument za trzema warstwami
  (kontrakt, kierunek, stan) i przeciw stanowi w trackerze.

### Nieprzetworzone

Z listy w `research/prompts/2026-09-18-video-triage-pass2-prompt.md` zostały punkty
1, 2, 4, 5, 7, 9, 10 (Factory.com, Warp, Resonate, Graptile, Anthropic „Tokens should
have jobs", DSPy, Amnara). Wrócić do nich tylko, jeśli zwiad Deep Research wskaże
lukę, której nie zamykają wystąpienia 3, 6, 8.
