# strategy

## Purpose

Wiążące kontrakty repo: jak wykonuje się dany rodzaj pracy w aid4u. Obowiązują w całym repozytorium,
nad lokalnymi `AGENTS.md`. Zmiana czegokolwiek w tym folderze wymaga jawnej zgody użytkownika.
Pliki trzymają wiedzę trwałą (reguły, procedury, uzasadnienia), nigdy stan.

## Ownership

Rodzaj pracy → plik do przeczytania przed startem:

| Robisz | Czytaj |
|---|---|
| nowe zadanie kursowe | `tasks/workflow.md` (pipeline, dekompozycja), `demo-processing-workflow.md` (jak korzystać z 4th-devs), `secret-flags.md` |
| wybór lub zmiana modelu LLM | `llm-selection.md` (identyfikatory modeli są w `core/llm/adapters/`, nie tutaj) |
| kod dotykający kluczy, `.env`, keyringu | `secrets-management.md` |
| pętla agentowa, retry, throttle, budżet kosztu | `agent-loop-safety.md` (powody; kontrakty w `core/AGENTS.md`) |
| instrumentacja Logfire/Langfuse, prompty w rejestrze | `observability.md` |
| nowy plik lub folder | `naming-conventions.md` |
| pisanie lub recenzja kodu, audyt | `rules/` (zawsze `rules/common/`, resztę wg rodzaju pracy) |
| zgłaszanie długu, issue, finding z rutyny | `issue-tracking.md` (Linear jest jedynym rejestrem) |
| rutyna, audyt, harmonogram, CodeRabbit | `quality-control.md` |
| użycie lub konflikt skilli | `skills/` |
| tworzenie artefaktu z szablonu (cheatsheet, karta dema) | `templates/` (kopiuj plik, nie przepisuj) |
| przejście między sezonami kursu | `season-transition.md` (instancje w `tasks/sXX/requirements/`) |
| decyzja bez sezonu | `open-decisions.md` |
| tryb nauki (wyłączony) | `learning-protocol.md` |

## Local Contracts

- **Zero stanu.** Bez checkboxów, list „do zrobienia", statusów ✅/❌ opisujących repo, dat wykonania. Dług żyje w Linear; w tekście najwyżej kotwica `(→ AID-XXX)`. Wyjątki: ✅/❌ jako przykłady dobrze/źle, trwałe właściwości rzeczy zewnętrznych, placeholdery w `templates/`, generyczne kryteria wyjścia z procedury. Jedyny plik stanu: `.issues.md`, generowany, nie edytować.
- **Szablony tylko w `templates/`, plik jest szablonem.** Test: czy ktoś to kopiuje, żeby stworzyć nowy artefakt? Tak → `templates/`. Nie → zostaje na miejscu.
- **Kontrakt osobno od uzasadnienia.** Co kod gwarantuje: `AGENTS.md` podsystemu. Dlaczego: plik tutaj (`agent-loop-safety.md`, `observability.md`).
- Zmiana konwencji nazewnictwa lub zarządzania sekretami zaczyna się od aktualizacji odpowiedniego pliku tutaj, potem kodu.

## Work Guidance

- Traktuj dokumentację jak kod: zwięźle, operacyjnie, bez narracji.
- Zakaz podglądu `.env`; sekrety pochodzą z keyringu (`secrets-management.md`). Wyciek klucza przerywa pracę i wymaga raportu.

## Verification

- `uv run python scripts/check_dox.py` (spójność kaskady) przed PR.
- Zmiana dotycząca sekretów: zgodność z `core/secrets.py` i `core/config.py`.

## Child DOX Index

- `rules/`: reguły recenzji i audytu, jedna reguła na plik, digest ERROR czytany przez CodeRabbit
- `skills/`: roster skilli, wyzwalacze, konflikty, kontrakty między skillami
- `tasks/`: pipeline implementacji zadania kursowego i dekompozycja na kroki
- `templates/`: szablony artefaktów; plik jest szablonem
