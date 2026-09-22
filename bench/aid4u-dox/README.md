# Pomiar wpływu DOX na agenta (aid4u, zadanie s01e02)

Dwa pomiary z notatki `research/workflow/2026-09-21-eth-agents-md-note.md`, sekcja Ocena.

## Warianty

| Wariant | Co zawiera |
|---|---|
| `with-dox` | aid4u jak jest, bez śladów rozwiązania s01e02 (folder zadania: tylko `doc/` i `__init__.py`; flaga, plan i wzmianki w innych plikach usunięte przez `scrub.py`) |
| `no-dox` | to samo minus wszystkie `AGENTS.md` i `CLAUDE.md` w repo; globalny `~/.claude/CLAUDE.md` zostaje w obu |
| `clean-dox` | with-dox z root i `tasks/AGENTS.md` podmienionymi na `clean-dox/` (DOX przycięty do reguły ETH: tylko to, czego nie ma w README i kodzie) oraz `strategy/**/AGENTS.md` z `strategy-routers/`; chain 4 107 tokenów wobec 11 946 |
| `strategy-dox` | clean-dox plus nakaz w root `AGENTS.md`: punkt w Core Contract czyniący `strategy/` wiążącym i kroki 7–8 w Read Before Editing (czytaj `strategy/` wg rodzaju pracy oraz `strategy/rules/common/`). Snapshoty obu wariantów różnią się wyłącznie tym plikiem; chain 4 217 wobec 4 107 |

`strategy-routers/` to wspólna nakładka `strategy/**/AGENTS.md` dla obu wariantów, żeby jedyną
zmienną między nimi był nakaz. W 6 przebiegach `with-dox` i `no-dox` nie padło ani jedno
wywołanie narzędzia dotykające `strategy/`, więc bez nakazu treść tych plików jest dla agenta
niewidoczna i nie wchodzi do chaina.

Snapshoty leżą w `/home/lis/projekty/14_moje_workflow/02_aid4u-bench/`, poza oboma repo, jako świeże repozytoria z jednym commitem. Pierwsza wersja używała `git worktree`, ale agent no-dox znalazł stare rozwiązanie przez `git log --all`; snapshot bez historii zamyka ten wyciek.
Wynik s01e01 (lista podejrzanych) nie jest w worktree, bo `.cache` i `data/run-history` są gitignored; agent musi sam odpalić s01e01.

## Kroki

```bash
./prepare.sh                       # buduje wszystkie 4 snapshoty (VARIANTS="..." zawęża), uv sync, kontrola wycieków, commit startowy
setsid nohup ./batch.sh clean-dox:1 strategy-dox:1 clean-dox:2 strategy-dox:2 clean-dox:3 strategy-dox:3 > results/batch.log 2>&1 < /dev/null &   # seria w tle
uvx --from tiktoken python3 count_chain.py /home/lis/projekty/14_moje_workflow/02_aid4u-bench/with-dox tasks/s01e02_findhim --sections   # pomiar 1
./run_agent.sh with-dox 1          # pomiar 2, jeden przebieg (domyślnie model sonnet)
./run_agent.sh no-dox 1
python3 analyze.py results/*.jsonl # tabela zbiorcza
```

Każdy przebieg zaczyna od `git reset --hard` w worktree, więc przebiegi są niezależne. Minimum sensowne: 3 przebiegi na wariant.

## Co mierzymy

- Pomiar 1: tokeny chaina instrukcji (globalny + root + `tasks/` + folder zadania), z podziałem na sekcje `##`, żeby oddzielić przeglądy od instrukcji operacyjnych. Tokenizer cl100k, przybliżenie rzędu 10–15% względem tokenizera Claude.
- Pomiar 2: z `stream-json`: liczba tur, koszt, czas, tokeny wejścia i wyjścia, liczba Read/Grep/Bash, ile razy pytest i `run.py solve`, ile plików `AGENTS.md` agent przeczytał, po ilu odczytach dotarł do `doc/` zadania, czy zdobył flagę.

## Wyniki

`results/` jest **gitignored** i zostaje tylko lokalnie: `<wariant>-<id>.jsonl` to surowy transkrypt,
`.meta` czas i flaga, `.diff` zmiany w repo, `<wariant>-<id>-files/` kod, który agent napisał.
Tabela zbiorcza: `python3 analyze.py results/*.jsonl`.

Trwałym zapisem pomiaru jest nota w `research/`, nie ten folder — musi zawierać tabelę per przebieg,
bo po skasowaniu `results/` nie da się jej odtworzyć bez powtórzenia przebiegów.

## Zastrzeżenia

- Przebieg wysyła prawdziwe odpowiedzi do `hub.ag3nts.org` i odpytuje Nominatim. Zadanie jest już zaliczone, więc powtórna flaga nic nie psuje.
- Narzędzia agenta są ograniczone białą listą w `run_agent.sh` (bez `rm`, `git push`, `git log`, `cat`). Pierwsza wersja przepuszczała `cat`, agent no-dox zrobił `cat .env` (sam zamaskował wartości). Snapshot ma własny `.venv` i kopię `.env`.
- `AGENTS_read` w `analyze.py` liczy tylko jawne odczyty plików instrukcji; chain ładowany automatycznie przy starcie nie jest w transkrypcie jako Read. Jego koszt widać pośrednio w `cache_read`.
- Model: Sonnet-4.5 jak w pracy ETH; zmiana przez trzeci argument `run_agent.sh`.
- Zatrzymanie: Ctrl-C w terminalu z `run_agent.sh`. Sprzątanie worktree: `git -C <aid4u> worktree remove --force <ścieżka>`.
