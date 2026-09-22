# Tasks Module

## Purpose

Zadania kursu AI_Devs 4, jedno na folder `sXXeYY_nazwa`. Szczegóły epizodu (dane, model,
pułapki) żyją w jego własnym `AGENTS.md`, nie tutaj. Postęp i flagi: `uv run run.py status`.
Procedura przejścia między sezonami: `strategy/season-transition.md`.

## Ownership

- Każdy folder `sXXeYY_*` to domena jednego zadania.
- Foldery sezonowe `sNN/` (np. `s03/`, `s04/`) zawierają wyłącznie `requirements/` (raport gotowości, checklisty), nie implementacje.
- `common/`: kod używany przez co najmniej dwa zadania (`class.py`, `const.py`, `function.py`, `prompts.py`); jednorazowy helper zostaje w folderze zadania.

## Local Contracts

- Każde rozwiązanie zawiera `solution.py` z klasą zarejestrowaną przez `@task`. Wyjątek: świeżo założone foldery przy starcie sezonu (`AGENTS.md` + `doc/` + `__init__.py`).
- Uruchomienie: `uv run run.py solve sXXeYY`.
- `test_solution.py` opcjonalny; pisz po działającym rozwiązaniu, tylko gdy weryfikuje coś nietrywialnego. Realne uruchomienie (`--dry-run`, hub) liczy się bardziej.
- Zadania oparte na żywym serwerze (np. `s01e03_proxy`): `solve()` musi jawnie odmówić (`raise RuntimeError` z instrukcją), zamiast wysyłać pustą odpowiedź. Taki folder ma własny `AGENTS.md` z kontraktem endpointu.

## Work Guidance

- Przed projektowaniem od zera sprawdź `../4th-devs/` i NotebookLM (komentarze kursu).
- Sposób rozwiązania nie musi być zgodny z założeniem zadania; liczy się flaga.
- **Start sezonu:** najpierw dla wszystkich epizodów ustal sposób zdobycia danych wejściowych (endpoint, auth, statyczne czy żywe, cache czy nie) i zapisz w ich `AGENTS.md` (Ownership); dopiero potem implementuj po kolei.
- **Gdzie zapisywać dane** (`data/AGENTS.md`): `.cache/` to wyłącznie efemeryczny cache. Wszystko, co może przydać się w późniejszym epizodzie, idzie do `data/input/sXXeYY_nazwa/` (pobrane) lub `data/output/sXXeYY_nazwa/` (wyliczone), commitowane. `data/run-history/` jest automatyczne i jednorazowe; nie czytaj go jako źródła danych.
- **Fabuła jest treścią zadania.** Bywa, że zawiera dane potrzebne do rozwiązania albo fabuła jednego epizodu rozstrzyga niejednoznaczność w innym.

## Verification

- Ostateczna weryfikacja: flaga z huba, nie zielone testy.

## Child DOX Index

- Sezon 1: `s01e01_people/`, `s01e03_proxy/` (żywy serwer), `s01e04_sendit/`, `s01e05_railway/`
- Sezon 2: `s02e01_categorize/`, `s02e02_electricity/`, `s02e03_failure/`, `s02e04_mailbox/`, `s02e05_drone/`
- Sezon 3: `s03/` (requirements), `s03e01_evaluation/`, `s03e02_firmware/`, `s03e03_reactor/`, `s03e04_negotiations/`, `s03e05_savethem/`
- Sezon 4: `s04/` (requirements dla S04+S05), `s04e03_domatowo/`, `s04e04_filesystem/`, `s04e05_foodwarehouse/`
- Sezon 5: `s05e03_shellaccess/`, `s05e04_goingthere/`
- `common/`: kod współdzielony; `common/information-gathering/`: preprocessing komentarzy kursu dla NotebookLM
