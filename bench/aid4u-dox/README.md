# Pomiar wpływu DOX na agenta (aid4u, zadanie s01e02)

Dwa pomiary z notatki `research/workflow/2026-09-21-eth-agents-md-note.md`, sekcja Ocena.

## Warianty

| Wariant | Co zawiera |
|---|---|
| `with-dox` | aid4u jak jest, bez śladów rozwiązania s01e02 (folder zadania: tylko `doc/` i `__init__.py`; flaga, plan i wzmianki w innych plikach usunięte przez `scrub.py`) |
| `no-dox` | to samo minus wszystkie `AGENTS.md` i `CLAUDE.md` w repo; globalny `~/.claude/CLAUDE.md` zostaje w obu |
| `clean-dox` | with-dox z root i `tasks/AGENTS.md` podmienionymi na `clean-dox/` (DOX przycięty do reguły ETH: tylko to, czego nie ma w README i kodzie) oraz `strategy/**/AGENTS.md` z `strategy-routers/`; chain 4 107 tokenów wobec 11 946 |
| `strategy-dox` | clean-dox plus nakaz w root `AGENTS.md`: punkt w Core Contract czyniący `strategy/` wiążącym i kroki 7–8 w Read Before Editing (czytaj `strategy/` wg rodzaju pracy oraz `strategy/rules/common/`). Snapshoty obu wariantów różnią się wyłącznie tym plikiem; chain 4 217 wobec 4 107 |
| `pointer-dox` | clean-dox plus tabela wskaźników w root `AGENTS.md`: nazwa, co reguluje, plik, **w których folderach wiążące**, **przy jakiej pracy stosować**. Zastępuje dawną sekcję `### Index`, żeby nie dublować wskaźników; chain 4 797 |
| `symlink-dox` | clean-dox plus 90 symlinków `<nazwa>_strategy.md` w 33 folderach mających `AGENTS.md`, w tym `rules_strategy.md` → `strategy/rules/AGENTS.md`. Generuje `link_strategy.py` z mapy folder → dokumenty; chain 4 151 |

`strategy-routers/` to wspólna nakładka `strategy/**/AGENTS.md` dla wszystkich czterech wariantów
z przyciętym DOX, żeby jedyną zmienną między nimi był root `AGENTS.md` (w `symlink-dox` dodatkowo
symlinki). Pliki te nie leżą na ścieżce z roota do folderu zadania, więc nie wchodzą do chaina
ładowanego automatycznie — kosztują tylko wtedy, gdy agent do nich sięgnie.

Symlinki `*_strategy.md` celowo nie nazywają się `CLAUDE.md`: Claude Code wstrzykuje do promptu
tylko `CLAUDE.md`, więc agent musi je sam znaleźć i otworzyć. To jest cała hipoteza tego wariantu,
a `prepare.sh` tego pilnuje.

Snapshoty leżą w `/home/lis/projekty/14_moje_workflow/02_aid4u-bench/`, poza oboma repo, jako świeże repozytoria z jednym commitem. Pierwsza wersja używała `git worktree`, ale agent no-dox znalazł stare rozwiązanie przez `git log --all`; snapshot bez historii zamyka ten wyciek.
Wynik s01e01 (lista podejrzanych) nie jest w snapshocie, bo `.cache` i `data/run-history` są gitignored; agent musi sam odpalić s01e01.

## Kroki

```bash
./prepare.sh                       # buduje wszystkie 6 snapshotow (VARIANTS="..." zawęża), uv sync, kontrola wycieków, commit startowy
setsid nohup ./batch.sh results/PLAN.txt > results/batch.log 2>&1 < /dev/null &   # seria w tle; PLAN.txt to lista par wariant:id, po jednej na linię
uvx --from tiktoken python3 count_chain.py /home/lis/projekty/14_moje_workflow/02_aid4u-bench/with-dox tasks/s01e02_findhim --sections   # pomiar 1
./run_agent.sh with-dox 1          # pomiar 2, jeden przebieg (domyślnie model sonnet)
./run_agent.sh no-dox 1
python3 analyze.py results/*.jsonl # tabela zbiorcza
```

Każdy przebieg zaczyna od `git reset --hard` **i `git clean -fdx`** (z wyjątkiem `.env`, `.venv`,
`.flags.json`), więc startuje na zimno. Samo `-fd` nie wystarczało: `.cache/` i `data/run-history/`
są gitignored, więc przetrwały między przebiegami i przebieg N+1 zastawał dane pobrane przez N.
Ten błąd skaził rundę 1 pomiaru.

`batch.sh` jest wznawialny — pomija pary z domkniętym `.meta` — i po każdym przebiegu kopiuje
`results/` do `_results-backup/` poza repo. O statusie przebiegu decyduje `check_run.py`, czytając
pola `is_error`/`subtype` z linii `result`; nie wolno tego robić grepem po transkrypcie, bo agent
czyta pliki repo opisujące throttle i kod 429.

Minimum sensowne: 10 przebiegów na wariant. Przy n=3 rozrzut wewnątrz wariantu przekraczał
wszystkie różnice między wariantami.

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
- **Znany tryb awarii:** agent może zlecić pracę w tle (`run_in_background`, `Monitor`) i zakończyć turę, czekając na powiadomienie, którego tryb `-p` nie dostarcza. Przebieg kończy się przedwcześnie. W rundzie 2 dotyczyło to 3 z 10 przebiegów `with-dox` i żadnego w pozostałych wariantach.
- Zatrzymanie: `pkill -f batch.sh; pkill -f 'claude -p'`. Snapshoty to zwykłe katalogi, nie worktree — sprząta się je przez `rm -rf` i ponowne `prepare.sh`.
