# agentic-workflow

Meta-projekt: audyt, ewaluacja i synteza moich rozwiązań workflow pracy z agentami kodującymi
(Claude Code, DOX/AGENTS.md, skille, Linear, CodeRabbit, docker-mcp-toolkit), wdrożonych
dotąd rozproszenie w innych repozytoriach.

## Cel

1. Zebrać i ujednolicić rozwiązania z pozostałych repo, ocenić czy i jak działały, wyrzucić
   niepotrzebne, sprzeczne lub działające w niezamierzony sposób, zsyntetyzować resztę
   i zmapować obszary workflow, które pozostają otwarte.
2. Przejrzeć badania i praktykę społeczności: czego brakuje nam w workflow (albo w samym
   myśleniu o workflow) i które gotowe rozwiązania warto zaadaptować, zarówno całościowe
   (np. BMAD), jak i modułowe (np. DOX).

## Zakres

- `short-run`: audyt obecnych workflow na podstawie analizy repozytoriów, nie wrażeń;
  naprawa błędów krytycznych i blokujących rozwój; sprawdzenie, czy narzędzia są używane
  „poprawnie" (bez wymyślania nowych konwencji, czytelnie dla agentów i ludzi, bez
  antywzorców typu „wszystkie stany w Linear", z maksymalnym zwrotem przy tym samym
  nakładzie); przegląd workflow od minimalistycznych po zaawansowane i wybór ścieżki;
  minimum umożliwiające agentowi realnie samodzielną pracę.
- `long-run`: zależy od ścieżki wybranej w `short-run`; kandydaci: własny ekosystem
  skilli, odejście od docker-mcp-toolkit na rzecz rozwiązania łączącego się z „bazą skilli".
- Przekrojowo: wiedza z aid4u stosowana przy ewaluacji, budowie własnych elementów
  i wyborze gotowych systemów.
- Poza zakresem: własny agent lub cały harness. Pracujemy nad pętlą i procesem wokół niej.

## Struktura

- `research/` — materiały źródłowe i ich oceny (notatki z wideo, prompty dla zewnętrznych
  modeli, przeglądy workflow)
- `strategy/` — trwałe dokumenty kierunkowe: struktura folderów, nazewnictwo
- `AGENTS.md` (+ symlink `CLAUDE.md`) w każdym istotnym folderze — kontrakty pracy dla
  agentów (DOX), po angielsku, w formie wskaźników

## Status

- 2026-09-18: inicjalizacja repo i DOX. Notatka z krótkiego wideo AI LABS o loop
  engineering, które było triggerem projektu i ilustruje intencję, nie stanowi źródła
  wiedzy. Prompt dla Gemini do triage kolejnych materiałów; właściwy research zaczyna
  się po jego wynikach. Szkielet Pythona usunięty: nie miał uzasadnienia
- 2026-09-26: synteza lekcji AI_devs 4 i AI_devs 3 pod kątem granicy między harnessem a
  inżynierią kontekstu (hooki, minimalny DOX + docstringi, reguły jako kod),
  `research/workflow/2026-09-26-aid-lessons-synthesis.md`. Zaplanowane: przegląd repo
  4th-devs w poszukiwaniu wzorców do skopiowania; kandydaci w tej samej syntezie

#### Wsparcie
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/PoppyTea/agentic-workflow?utm_source=oss&utm_medium=github&utm_campaign=PoppyTea%2Fagentic-workflow&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
