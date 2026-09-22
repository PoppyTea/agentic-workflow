# Projekt AI_Devs 4 (aid4u)

## Purpose

Rozwiązania zadań kursu AI_Devs 4 plus własna infrastruktura do ich uruchamiania (`core/`).
Ten plik trzyma reguły obowiązujące w całym repo i wskazuje, gdzie są szczegóły; nie powtarza ich.

Tryb pracy: **efficiency mode**. Liczy się zdobyta flaga, nie zgodność z duchem zadania.
Tryb nauki (TDD-first, pełne planowanie) jest wyłączony; przywraca go `scripts/learning_mode_on_off.py on`.

## Ownership

Korzeń: reguły ogólnorepozytoryjne, preferencje użytkownika, kaskada DOX. Wszystko, co dotyczy
jednego podsystemu, należy do `AGENTS.md` tego podsystemu (Child DOX Index).

Poza kaskadą, bez własnego `AGENTS.md`: `scripts/` (narzędzia repo; `scripts/panic.sh` podlega
kontraktowi kill switcha z `core/AGENTS.md`), `.claude/` (konfiguracja Claude Code), `.game/`
(stan gamifikacji, czytany wyłącznie spoza repo), `doc/` (gitignored scratch).

## Local Contracts

1. **Efekt > droga.** TDD i planowanie są dozwolone, nie wymagane.
2. **4th-devs najpierw.** Przed projektowaniem sprawdź `../4th-devs/` (fork, TypeScript); gotowe demo do przepisania bije projektowanie od zera.
3. **LLM tylko przez `LLMClient`** z `core/llm/`, nigdy bezpośrednio przez SDK.
4. **`setup_observability()`** jako pierwsza linia każdego skryptu.
5. **`503`** z huba → `hub.get_data(path, tolerate_503=True)`.
6. **Jeden task TW naraz.** `task focus`, nie `task list`, nie pamięć.
7. **Flagi sekretne** (`{FLG:...}` zdobywane ukrytą drogą) zapisuj w `.flags.json` pod kluczem `sXXeYY_secret`; `run.py status` liczy je osobno. Nie projektuj rozwiązań pod nie; bierz, jeśli wpadną po drodze. Jak ich szukać: `strategy/secret-flags.md`.

## Strategia

Kontrakty repo. Wiersz obowiązuje, gdy pracujesz w wymienionych folderach; przeczytaj plik, zanim zaczniesz.

| Nazwa | Co reguluje | Plik | Wiążące w | Stosować przy |
|---|---|---|---|---|
| naming-conventions | konwencje nazw plików i katalogów, jedyne źródło prawdy | `strategy/naming-conventions.md` | całe repo | tworzenie pliku lub folderu |
| secrets-management | keyring zamiast `.env`, zakaz podglądu sekretów, obfuskacja wydruków | `strategy/secrets-management.md` | `core/`, `deploy/` | klucze, `.env`, konfiguracja |
| observability | span i generacja dla każdego wywołania LLM, rejestr promptów | `strategy/observability.md` | `core/llm/`, `core/observability/`, `tasks/*/prompts.py` | dodanie lub zmiana wywołania LLM |
| llm-selection | drabina `fast` → `balanced` → `powerful` → `flagship`, tier Gemini | `strategy/llm-selection.md` | `core/llm/adapters/`, `tasks/` | wybór lub eskalacja modelu |
| agent-loop-safety | dlaczego istnieją osłony pętli: błąd do modelu, budżet, kill switch, throttle | `strategy/agent-loop-safety.md` | `core/llm/`, `core/runtime/`, `core/hub/` | zmiana retry, throttle, budżetu, kill switcha |
| tasks-workflow | wzorzec implementacji zadania, `BaseTask`, minimalna struktura folderu | `strategy/tasks/workflow.md` | `tasks/`, `core/tasks/` | tworzenie folderu zadania |
| secret-flags | jak polować na flagi sekretne poza główną ścieżką | `strategy/secret-flags.md` | `tasks/`, `.flags.json` | trop flagi sekretnej |
| season-transition | procedura przystanku S(n) → S(n+1), rozdział `sXX-prep` od `sXXeYY-prep` | `strategy/season-transition.md` | `tasks/sXX/requirements/` | przełom sezonów, start epizodu |
| issue-tracking | Linear jedynym rejestrem długu, cykl życia issue, priorytety | `strategy/issue-tracking.md` | całe repo, `.issues/` | issue, dług, pokusa lokalnej listy TODO |
| quality-control | governance rutyn audytowych, anatomia samowystarczalnego promptu | `strategy/quality-control.md` | całe repo, `.claude/state/` | tworzenie lub zmiana rutyny |
| rules-common | reguły egzekwowane przez każdą rutynę czytającą kod | `strategy/rules/common/` | `core/**`, `tasks/**` | pisanie lub recenzja kodu |
| rules-pr-review | reguły sensowne tylko przy diffie PR-a | `strategy/rules/pr-review/` | `tasks/**/AGENTS.md`, `core/**/*.py` | recenzja PR |
| skill-activation | roster skilli, macierz wyzwalaczy, rozstrzyganie konfliktów | `strategy/skills/skill-activation.md` | całe repo | wybór skilla |

## Work Guidance

### Nowe zadanie kursowe, przed pisaniem czegokolwiek

1. Sprawdź `../4th-devs/` pod kątem gotowego demo dla tematu.
2. Skonsultuj NotebookLM (komentarze kursu + notatnik zadań); to pierwsze źródło, nie ostatnie.
3. Dopiero potem projektuj sam, najkrótszą ścieżką do flagi.
4. Uruchomienie: `uv run run.py solve sXXeYY`.

### Modele LLM

- Identyfikatorów nie wpisuj z pamięci: źródłem prawdy są rostery w `core/llm/adapters/`; `create_provider()` odrzuca inne i podaje poprawne.
- Wybór i eskalacja (`fast` → `balanced` → `powerful` → `flagship`, kiedy Gemini): `strategy/llm-selection.md`. Jeśli zadanie skorzystałoby na mocniejszym modelu, zgłoś to od razu.
- Rekomendacja modelu z komentarzy kursu bije drabinę przy pierwszym podejściu.
- Zadanie na pewno w zasięgu Haiku 4.5 → zaproponuj subagenta albo go wyślij.

### Pozostałe

- Nazewnictwo plików: `strategy/naming-conventions.md`, czytaj przed tworzeniem nowych plików.
- Skille: `verification-before-completion` przed każdym `task done`; `systematic-debugging` po 2+ nieudanych próbach; `langfuse-observability` przy instrumentacji; `api-testing` przy REST/hub; `001-papaver-tw-integration` przy każdej operacji TW. Pełny roster i konflikty: `strategy/skills/skill-activation.md`.
- Struktura infrastruktury: `README.md`. Serwery MCP: `.claude/settings.json`.
- Stack: Python 3.12+, `uv`. Komendy: `uv sync`, `uv run run.py solve sXXeYY`, `uv run pytest`, `./deploy/deploy.sh`, `task focus`.

## Verification

```bash
uv run pytest                       # bramka przed PR
uv run ruff check .                 # bramka przed PR
uv run python scripts/check_dox.py  # spójność kaskady AGENTS.md, bramka przed PR
```

`ruff format --check` i `pyrefly check` nie są bramkami: formatuj i typuj tylko pliki, które i tak zmieniasz.
Ostateczną weryfikacją zadania jest flaga z huba, nie zielone testy.

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Change into the folder you are about to edit and list it; read what is there before editing
5. Read every AGENTS.md found along each route
6. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
7. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
8. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

## Update After Editing

Every meaningful change requires a DOX pass before the task is done. Update the closest owning AGENTS.md when a change affects purpose, scope, ownership, durable structure, contracts, workflows, required inputs or outputs, user preferences, or the child index. Update parents when parent-level structure or index changes. Remove stale or contradictory text immediately. Never describe history or past changes.

## Style

- Keep docs concise, current, and operational; document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs; do not duplicate
- Delete stale notes instead of explaining history

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children; refresh affected Child DOX Index
3. Run existing verification when relevant
4. Report any docs intentionally left unchanged and why

## User Preferences

- **Commit routing:** zmiany w plikach `.py` idą przez feature branch + PR (uruchamia CodeRabbit). Wszystko inne (markdown, konfiguracja, symlinki, dane) commituje się prosto na `main`. Doc opisujący kod z tego samego PR może jechać razem z nim.
- **Praca wsadowa:** gdy użytkownik dzieli implementację na niezależne jednostki („jedna funkcja na PR"), każda dostaje własny branch, testy i PR, otwarty przed rozpoczęciem następnej; commituj w trakcie, nie tylko na końcu.
- **CodeRabbit:** auto-recenzje wyłączone; `@coderabbitai review` tylko po jawnej zgodzie użytkownika na dany PR. Po otwarciu PR sprawdź komentarze po 5 i po 10 minutach, potem przestań i poproś użytkownika o ping. Brak uwag zostawia ślad tylko w `issues/<N>/comments` („No actionable comments"), nie w `reviews`. Wytwory CodeRabbita (poprawki, testy, docstringi) to szkic do sprawdzenia; nie oddawaj mu docstringów i testów kodujących zmierzone fakty o świecie.
- **Docstringi domyślnie tak** dla każdej funkcji, metody i klasy. **Komentarze inline domyślnie nie**, tylko gdy „dlaczego" albo zysk z danego „jak" nie wynika z kodu.
- **Kill switch:** przy starcie czegokolwiek długotrwałego podaj w tej samej wiadomości komendę zatrzymania: `bash scripts/panic.sh` (twardo) lub `uv run run.py panic --graceful`. Kontrakt: `core/AGENTS.md`.
- **Linear (team Aid4u, klucz `AID`) jest jedynym źródłem prawdy o issues.** PR zamykający issue ma w opisie `Fixes AID-XXX`. Polityka: `strategy/issue-tracking.md`.

## Child DOX Index

- `core/`: architektura, LLM, bazowa obsługa zadań
- `strategy/`: dokumenty strategiczne i workflow
- `tasks/`: zadania kursu
- `tests/`: testy
- `data/`: dane zadań (`data/input/`, `data/output/`)
- `deploy/`: VPS, systemd, tunele
- `.issues/`: archiwum triage'u sprzed migracji do Linear i `summaries-4-human/`
