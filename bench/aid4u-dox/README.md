# Pomiar wpływu DOX na agenta (aid4u, zadanie s01e02)

Dwa pomiary z notatki `research/workflow/2026-09-21-eth-agents-md-note.md`, sekcja Ocena.

## Warianty

| Wariant | Co zawiera |
|---|---|
| `with-dox` | aid4u jak jest, bez śladów rozwiązania s01e02 (folder zadania: tylko `doc/` i `__init__.py`; flaga, plan i wzmianki w innych plikach usunięte przez `scrub.py`) |
| `no-dox` | to samo minus wszystkie `AGENTS.md` i `CLAUDE.md` w repo; globalny `~/.claude/CLAUDE.md` zostaje w obu |
| `clean-dox` | (nieutworzony) DOX przycięty do definicji ETH: tylko to, czego nie ma w README i kodzie. Do zbudowania ręcznie, gdy zapadnie decyzja |

Snapshoty leżą w `/home/lis/projekty/14_moje_workflow/02_aid4u-bench/`, poza oboma repo, jako świeże repozytoria z jednym commitem. Pierwsza wersja używała `git worktree`, ale agent no-dox znalazł stare rozwiązanie przez `git log --all`; snapshot bez historii zamyka ten wyciek.
Wynik s01e01 (lista podejrzanych) nie jest w worktree, bo `.cache` i `data/run-history` są gitignored; agent musi sam odpalić s01e01.

## Kroki

```bash
./prepare.sh                       # buduje oba worktree, uv sync, kontrola wycieków, commit startowy
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

`results/<wariant>-<id>.jsonl` to surowy transkrypt, `.meta` czas i flaga, `.diff` zmiany w repo, `<wariant>-<id>-files/` kod, który agent napisał. Tabela zbiorcza: `python3 analyze.py results/*.jsonl`.

## Zastrzeżenia

- Przebieg wysyła prawdziwe odpowiedzi do `hub.ag3nts.org` i odpytuje Nominatim. Zadanie jest już zaliczone, więc powtórna flaga nic nie psuje.
- Narzędzia agenta są ograniczone białą listą w `run_agent.sh` (bez `rm`, `git push`, `git log`, `cat`). Pierwsza wersja przepuszczała `cat`, agent no-dox zrobił `cat .env` (sam zamaskował wartości). Snapshot ma własny `.venv` i kopię `.env`.
- `AGENTS_read` w `analyze.py` liczy tylko jawne odczyty plików instrukcji; chain ładowany automatycznie przy starcie nie jest w transkrypcie jako Read. Jego koszt widać pośrednio w `cache_read`.
- Model: Sonnet-4.5 jak w pracy ETH; zmiana przez trzeci argument `run_agent.sh`.
- Zatrzymanie: Ctrl-C w terminalu z `run_agent.sh`. Sprzątanie worktree: `git -C <aid4u> worktree remove --force <ścieżka>`.
