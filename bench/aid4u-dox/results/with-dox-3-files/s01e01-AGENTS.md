# s01e01_people Module

## Purpose
Filtruje `data/main_story/people.csv` (mężczyźni, 20-40 lat w
`tasks/common/const.py::REFERENCE_YEAR`, urodzeni w Grudziądzu), taguje zawody
przez LLM i wysyła do huba tych z tagiem `transport`. Pierwsze zadanie kursu.

## Ownership
- `solution.py`: `PeopleTask` (`hub_name="people"`) — czyste funkcje
  (`parse_csv`, `filter_candidates`, `build_tagging_prompt`, `apply_tags`,
  `filter_by_tag`, `format_answer`) + stałe (`MIN_AGE`/`MAX_AGE`/`TARGET_CITY`/
  `TARGET_GENDER`/`TARGET_TAG`).
- `prompts.py`: `SYSTEM_TAGGING`/`USER_TAGGING` dla tagowania zawodów.
- `doc/`: materiały kursu — nieużywane w runtime.

## Local Contracts
- **`data/output/s01e01_people/suspects.json` to skonsumowany przez S01E02
  wynik `format_answer(filter_by_tag(...))`** — dokładnie ta sama lista, którą
  wysyła `solve()` do huba (imię/nazwisko/płeć/rok urodzenia/miasto/tagi).
  Zapisywany przez `s01e02_findhim.solution._load_or_build_suspects()`
  (`../s01e02_findhim/AGENTS.md`), nie przez ten task bezpośrednio — jeśli plik
  nie istnieje, S01E02 odtwarza ten sam pipeline importując czyste funkcje
  stąd, więc nie duplikuje logiki filtrowania/tagowania.
- Zmiana `filter_candidates()`/`format_answer()`/kryteriów demograficznych w
  tym pliku unieważnia zapisany `suspects.json` — usuń go ręcznie, żeby S01E02
  przeliczył listę od nowa.

## Work Guidance
- (brak specyficznych wskazówek poza ogólnymi z `tasks/AGENTS.md`)

## Verification
- `uv run run.py solve s01e01 --dry-run` do podglądu listy kandydatów przed
  tagowaniem/wysyłką.
- Live-verified against the real hub: `{FLG:SURVIVORS}` (patrz `.flags.json`).

## Child DOX Index
- None.
