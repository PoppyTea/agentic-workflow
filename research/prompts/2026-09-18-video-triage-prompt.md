# Prompt dla Gemini: triage pięciu wideo o workflow AI coding

Użycie: wklej do Gemini (wersja z dostępem do YouTube), a wynik zapisz w
`research/reports/`. Wykonane 2026-09-18, wyniki A i B tamże, synteza w
`research/videos/2026-09-18-video-triage-synthesis.md`. Film AI LABS (PLyRe6Zk--8) jest już
opracowany w `research/videos/`, dlatego nie ma go na liście.

---

Jesteś moim asystentem badawczym. Obejrzyj pięć filmów z YouTube, korzystając zarówno
ze ścieżki audio, jak i wizualnej (slajdy, terminal, kod, nazwy repozytoriów i narzędzi
widoczne na ekranie). Odpowiedz po polsku.

Filmy:

1. https://youtu.be/v4F1gFy-hqg — „Software Fundamentals Matter More Than Ever", Matt Pocock, AI Engineer, 18:26
2. https://youtu.be/CEvIs9y1uog — „Don't Build Agents, Build Skills Instead", Barry Zhang i Mahesh Murag (Anthropic), AI Engineer, 16:22
3. https://youtu.be/-QFHIoCo-Ko — „Full Walkthrough: Workflow for AI Coding", Matt Pocock, AI Engineer, 1:36:30
4. https://www.youtube.com/live/htM02KMNZnk — „WF2026: Software Factories & Keynotes", AI Engineer World's Fair 2026, dzień 1 (30 czerwca 2026), stream 8:36:51, występują m.in. Microsoft, OpenAI, OpenClaw, Z.ai, MiniMax, Hugging Face
5. https://www.youtube.com/live/I2cbIws9j10 — „WF26: Harness Engineering & Startup Battlefield", AI Engineer World's Fair 2026, dzień ostatni (2 lipca 2026), stream 9:11:15, występują m.in. Garry Tan, Mike Krieger, Theo (t3.gg), DSPy

Filmy 4 i 5 to całodniowe streamy bez agendy w opisie (tylko bloki: keynotes 9:00–10:30 PT,
program 10:45–12:25 i 13:30–16:05, keynotes 16:30–17:30). Dla nich zrób najpierw indeks:
tabela `start`, `koniec`, `prelegent`, `firma`, `tytuł wystąpienia`, na podstawie plansz
tytułowych i zapowiedzi prowadzących. Przerwy, muzykę i pustą scenę pomiń. Dopiero potem
oceniaj każde wystąpienie jak osobny film, w skali z punktu 2, i wskaż te, które warto
obejrzeć, z dokładnym czasem startu w streamie. Jeśli limit długości wideo nie pozwala Ci
przetworzyć całego streamu naraz, powiedz to i podaj, który zakres czasu przetworzyłeś;
wtedy zrobimy to w kilku podejściach.

Mój kontekst, względem którego oceniasz przydatność:

- Pracuję solo, głównie w Claude Code, z hierarchią plików AGENTS.md (framework DOX:
  każdy folder ma kontrakt pracy dla agenta), skillami, Linear do issues, CodeRabbit
  do review PR, docker-mcp-toolkit jako bramką MCP.
- Prowadzę audyt swoich workflow: chcę wiedzieć, co usunąć, co ujednolicić, jakich
  elementów brakuje, i wybrać ścieżkę od minimalistycznej po zaawansowaną.
- Cel bliski: minimum, które pozwala agentowi pracować faktycznie samodzielnie
  (spec, weryfikacja, pętla, kryterium „done").
- Cel dalszy: własny ekosystem skilli i ewentualne zastąpienie docker-mcp-toolkit.
- Nie buduję własnego agenta ani harnessu; interesuje mnie pętla i proces wokół niej.
- Uczę się na własnych błędach: w jednym z projektów przez brak wprawy z Linear
  zamieniłem go w dziennik pokładowy (osobny issue na każdy plik i decyzję). Dlatego
  cenię materiały, które pokazują, do czego dane narzędzie realnie służy i jak wygląda
  jego typowe, czytelne dla ludzi użycie, a nie tylko „co da się z nim zrobić".

Dla każdego filmu osobno podaj:

1. Werdykt: „obejrzyj w całości", „obejrzyj wybrane fragmenty", „daruj sobie", z jednym
   zdaniem uzasadnienia względem mojego kontekstu.
2. Mapę fragmentów: tabela z kolumnami `od`, `do`, `temat`, `wartość (1–5)`, `dlaczego`.
   Znacznik czasu ma wskazywać moment, w którym zaczyna się dana myśl, nie rozdział
   z opisu filmu. Segmenty sponsorskie, autopromocję i ogólniki oznacz jako
   „pomiń" bez streszczania.
3. Konkretne twierdzenia autora: lista tez wraz ze znacznikiem czasu i wskazaniem, czy
   autor podał dowód (demo, dane, przykład kodu) czy tylko opinię.
4. Rzeczy widoczne na ekranie, których nie ma w audio: nazwy repozytoriów, plików,
   komend, struktury folderów, treść slajdów z listami kontrolnymi. Przepisz je
   dosłownie ze znacznikiem czasu.
5. Mapowanie na mój kontekst: które elementy (a) już mam w innej formie, (b) mogę
   przyjąć bez zmiany konwencji, (c) kolidują z moimi założeniami. Przy każdym podaj
   znacznik czasu.
6. Ocenę marketingu: co jest sprzedażą produktu lub kursu, a co treścią merytoryczną.

Na końcu, przekrojowo dla wszystkich filmów:

- Gdzie autorzy sobie przeczą lub mówią to samo innymi słowami.
- Trzy najważniejsze rzeczy, których brakuje w opisanym wyżej moim workflow według
  tych filmów, z uzasadnieniem i znacznikami czasu jako dowodem.
- Kolejność oglądania, jeśli mam czas tylko na 30 minut łącznie, i osobno na 2 godziny.

Zasady:

- Nie wymyślaj znaczników czasu; jeśli nie jesteś pewien momentu, podaj zakres i to zaznacz.
- Nie streszczaj całego filmu w prozie; interesują mnie tabele i listy z czasami.
- Odróżniaj wyraźnie to, co mówi autor, od twojej oceny.
- Jeśli któryś film jest niedostępny lub nie możesz przetworzyć ścieżki wizualnej,
  napisz to wprost zamiast uzupełniać z pamięci.
