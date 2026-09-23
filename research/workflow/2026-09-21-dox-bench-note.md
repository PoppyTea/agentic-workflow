---
tags: [research, workflow, dox, bench, aid4u]
bench: bench/aid4u-dox/
date: 2026-09-21
status: 4 warianty po 3 przebiegi; rozrzut między przebiegami większy niż większość różnic
---

# Pomiar: wpływ chaina AGENTS.md na Claude Code w aid4u (zadanie s01e02)

- Środowisko i skrypty: `bench/aid4u-dox/README.md`. **Surowe transkrypty nie są w repo** (`results/` jest gitignored), więc ta nota jest jedynym trwałym zapisem pomiaru; tabela per przebieg poniżej jest nieodtwarzalna bez powtórzenia serii.
- Metoda: `claude -p` (pełny Claude Code w trybie nieinteraktywnym), model Sonnet, ten sam prompt, świeży snapshot repo bez historii gita i bez śladów rozwiązania. Globalny `~/.claude/CLAUDE.md` (708 tokenów) obecny we wszystkich wariantach.
- **Koszt jest hipotetyczny.** Maszyna loguje się subskrypcją (`claudeAiOauth`, brak `ANTHROPIC_API_KEY`), więc `total_cost_usd` ze `stream-json` to wycena po cenniku API, nie wydatek. Jako miara porównawcza zużycia tokenów jest ważna, jako kwota — nie. Realnym ograniczeniem przy zwiększaniu `n` jest rate limit, nie budżet.
- **Wada metodyczna wykryta po serii: przebiegi nie były niezależne.** `run_agent.sh` czyścił snapshot przez `git clean -fd`, które nie rusza plików ignorowanych, a `.cache/` i `data/run-history/` są w `.gitignore`. W efekcie przebieg 1 każdego wariantu startował na zimno, a przebiegi 2 i 3 zastawały w cache listę podejrzanych z s01e01 i wyniki poprzedniego przebiegu. Liczby niżej trzeba czytać z tą świadomością; część rozrzutu wewnątrz wariantu może pochodzić stąd, a nie z wariancji modelu. Naprawione (`git clean -fdx`) dla rundy 2, która idzie w całości na zimno przy n=10 i której wyniki będą porównywalne wewnątrz siebie, ale nie wprost z liczbami z tej rundy.
- Zastrzeżenia: przebieg 1 wariantów `with-dox` i `no-dox` szedł na worktree z widoczną historią gita (`no-dox-1` zajrzał do `git log --all`, nie użył znalezionego kodu); reszta na snapshotach bez historii. Trzy przebiegi na wariant to za mało na test statystyczny.

## Treść

### Warianty

| Wariant | Chain do `tasks/s01e02_findhim` | Czym się różni |
|---|---|---|
| `with-dox` | 11 946 | aid4u jak jest |
| `no-dox` | 708 | żadnego `AGENTS.md`/`CLAUDE.md` w repo |
| `clean-dox` | 4 107 | root i `tasks/AGENTS.md` przycięte do reguły ETH, wspólny zestaw `strategy/**/AGENTS.md` |
| `strategy-dox` | 4 217 | `clean-dox` **plus nakaz** czytania `strategy/`; snapshoty różnią się wyłącznie root `AGENTS.md` |

Nakaz: punkt w Core Contract czyniący `strategy/` wiążącym plus kroki 7–8 w Read Before Editing. Kosztuje 110 tokenów wejścia.

### Pomiar 1: koszt chaina na wejściu

| Plik | Tokeny (cl100k) |
|---|---|
| `~/.claude/CLAUDE.md` | 708 |
| root `AGENTS.md` (oryginał) | 6 377 |
| `tasks/AGENTS.md` (oryginał) | 4 861 |
| razem `with-dox` | 11 946 |

45% chaina to dwie sekcje: root User Preferences (2 446, narracja o CodeRabbit) i tasks Child DOX Index (2 939, opisy rozwiązanych epizodów). Instrukcje operacyjne obu plików to ok. 3 400 tokenów. Po przycięciu: root 2 347, tasks 1 052.

### Pomiar 2: dwanaście przebiegów

| przebieg | tury | koszt* | min | out tok | Read | Bash | pytest | AGENTS.md czytane | flaga |
|---|---|---|---|---|---|---|---|---|---|
| with-dox-1 | 55 | 2,02 | 8,1 | 25 241 | 12 | 34 | 1 | 4 | tak |
| with-dox-2 | 62 | 2,68 | 9,4 | 31 552 | 5 | 48 | 1 | 2 | tak |
| with-dox-3 | 54 | 2,18 | 12,2 | 36 785 | 11 | 33 | 1 | 3 | tak |
| no-dox-1 | 58 | 1,65 | 6,9 | 28 878 | 14 | 40 | 3 | 0 | tak |
| no-dox-2 | 65 | 2,37 | 11,9 | 32 090 | 11 | 41 | 1 | 0 | tak |
| no-dox-3 | 56 | 2,42 | 14,2 | 35 999 | 11 | 41 | 0 | 0 | tak |
| clean-dox-1 | 74 | 2,60 | 9,0 | 37 945 | 17 | 39 | 1 | 2 | tak |
| clean-dox-2 | 63 | 2,74 | 10,3 | 36 789 | 20 | 32 | 1 | 1 | tak |
| clean-dox-3 | 72 | 2,28 | 9,7 | 38 970 | 11 | 43 | 1 | 4 | tak |
| strategy-dox-1 | 61 | 2,89 | 11,7 | 40 802 | 18 | 33 | 3 | 6 | tak |
| strategy-dox-2 | 63 | 2,89 | 8,3 | 36 711 | 15 | 35 | 2 | 3 | tak |
| strategy-dox-3 | 53 | 2,03 | 5,8 | 25 215 | 21 | 25 | 1 | 4 | tak |

\* wycena hipotetyczna, patrz zastrzeżenie wyżej.

| średnia | chain | tury | koszt* | min | Read | AGENTS.md czytane |
|---|---|---|---|---|---|---|
| with-dox | 11 946 | 57,0 | 2,29 | 9,9 | 9,3 | 3,0 |
| no-dox | 708 | 59,7 | 2,15 | 11,0 | 12,0 | 0,0 |
| clean-dox | 4 107 | 69,7 | 2,54 | 9,7 | 16,0 | 2,3 |
| strategy-dox | 4 217 | 59,0 | 2,60 | 8,6 | 18,0 | 4,3 |

**Flaga: 12 na 12.** Każdy wariant, każdy przebieg.

### Co robili inaczej

| Zachowanie | with-dox | no-dox | clean-dox | strategy-dox |
|---|---|---|---|---|
| Flaga | 3/3 | 3/3 | 3/3 | 3/3 |
| Konwencja repo (`@task`, `run.py solve`) | 3/3 | 3/3 | 3/3 | 3/3 |
| DOX pass (utworzył lub uzupełnił `AGENTS.md`) | 3/3 | 0/3 | 2/3 | 3/3 |
| Wynik s01e01 zapisany w `data/output/` | 2/3 | 0/3 | 2/3 | 3/3 |
| Napisał własne testy | 0/3 | 2/3 | 1/3 | 2/3 |
| Pełny `pytest` na koniec | 3/3 | 1/3 | 3/3 | 3/3 |

### Czy nakaz `strategy/` zadziałał

Nie tak, jak zakładał. Odczyty plików pod `strategy/`:

| przebieg | co przeczytał |
|---|---|
| clean-dox-1 | `naming-conventions.md` |
| clean-dox-2 | `llm-selection.md` |
| clean-dox-3 | nic |
| strategy-dox-1 | `naming-conventions.md` |
| strategy-dox-2 | nic |
| strategy-dox-3 | `naming-conventions.md`, `tasks/workflow.md` |

**Żaden przebieg nie przeczytał `strategy/AGENTS.md`** — routera „rodzaj pracy → plik", po który nakaz wysyła wprost. Jeden przebieg (`strategy-dox-3`) dotarł do `strategy/tasks/workflow.md`, czyli do podfolderu wskazanego przez krok 7. Wariant bez nakazu sięgał do `strategy/` równie często (2/3), tyle że po pliki wskazane punktowo w Work Guidance.

**Granica tego miernika.** „Ile plików instrukcji przeczytał" mierzy posłuszeństwo, nie trafność. Pominięcie pliku może być ignorowaniem instrukcji albo poprawną decyzją, że reguła nie dotyczy tej pracy — i te dwie rzeczy liczą się tu tak samo. Rozstrzygnięcie wymaga wskaźnika, który niesie informację o zakresie (tabela z kolumnami „wiążące w" i „stosować przy" ją niesie, nazwa pliku `rules_strategy.md` nie), albo zadania, w którym reguła faktycznie obowiązuje, bo wtedy zgodność jest zachowaniem obserwowalnym niezależnie od odczytu.

Nie da się tego obejść czytaniem rozumowania agenta: bloki `thinking` są w transkrypcie obecne (29 w przebiegu), ale ich treść jest pusta, zostaje sam podpis. „Rozważył i odrzucił" jest na tych danych niefalsyfikowalne.

Zastrzeżenie metodyczne: liczone są jawne wywołania `Read`. Claude Code dociąga `CLAUDE.md` z folderu czytanego pliku bez wpisu w transkrypcie, więc przebiegi, które czytały cokolwiek ze `strategy/`, mogły zobaczyć router mimo braku odczytu. Dla `clean-dox-3` i `strategy-dox-2` (zero odczytów pod `strategy/`) ta furtka jest zamknięta i wniosek jest pewny.

Wniosek: **nakaz w ramach DOX nie przekierowuje uwagi agenta.** Punktowe wskazanie pliku w Work Guidance („nazewnictwo: `strategy/naming-conventions.md`") działa lepiej niż ogólna reguła „zidentyfikuj rodzaj pracy i doczytaj". To jest ta sama obserwacja co przy sekcjach przeglądowych: agent wykonuje instrukcje konkretne, ignoruje proceduralne.

## Ocena

- **Na skuteczność chain nie ma wpływu.** Dwanaście na dwanaście flag, przy chainie od 708 do 11 946 tokenów. Konwencje repo są wyprowadzalne z kodu. Zgodne z ETH.
- **Na koszt też nie, w tym `n`.** Rozrzut wewnątrz wariantu (np. `strategy-dox` 2,03–2,89) przekracza różnice między wariantami. Żadna para nie rozdziela się na koszcie.
- **Dwie różnice są rozdzielone całkowicie**, czyli wszystkie trzy przebiegi jednego wariantu leżą poza zakresem drugiego. Test permutacyjny przy n=3 na n=3 daje dla pełnej separacji p=0,05 jednostronnie — to granica istotności, nie dowód:
  - `clean-dox` potrzebuje **więcej tur** niż `with-dox` (63–74 wobec 54–62),
  - `strategy-dox` robi **więcej odczytów** niż `with-dox` (15–21 wobec 5–12).
- **Przycięcie chaina nie potaniło pracy, tylko przesunęło koszt.** To jest najmniej intuicyjny wynik serii. Ucięcie 66% chaina (11 946 → 4 107) dało wariant z najwyższą liczbą tur i wysokim kosztem. Agent nadrabia czytaniem to, czego nie dostał z góry: `with-dox` czyta 9,3 pliku, `clean-dox` 16,0. Tokeny wejścia są tańsze niż tury, bo chain siedzi w cache, a każdy dodatkowy `Read` to nowa tura z pełnym kontekstem.
- **Zachowania procesowe wracają wraz z przyciętym DOX.** `clean-dox` i `strategy-dox` odtwarzają DOX pass, zapis do `data/output/` i pełny `pytest` — czyli te reguły przeżyły przycięcie, bo były w Local Contracts i Verification, a nie w sekcjach przeglądowych. To potwierdza tezę z pierwszej serii: DOX działa jako instrukcja procesowa.
- **Sekcje przeglądowe nadal bez wykrywalnego efektu.** Ich usunięcie nie zmieniło ani skuteczności, ani zachowań.

### Co z tego wynika dla „dobrego AGENTS.md"

| Element | Werdykt | Podstawa |
|---|---|---|
| Local Contracts, Verification | zachować | zachowania procesowe zanikają bez nich (no-dox 0/3 DOX pass) |
| Punktowe wskazania pliku w Work Guidance | zachować | jedyna forma odsyłacza, po którą agent faktycznie sięga |
| Child DOX Index z narracją, opisy stanu, historia | usunąć | zero wykrywalnego efektu, 45% chaina |
| Nakaz „zidentyfikuj rodzaj pracy i doczytaj `strategy/`" | **nie wprowadzać** | 0/3 odczytów routera, koszt 110 tokenów i więcej odczytów |
| Agresywne przycinanie chaina | ostrożnie | oszczędność na wejściu wraca jako więcej tur |

### Otwarte

- `n=3` nie wystarcza. Przy limicie subskrypcji zamiast budżetu `n=10` jest osiągalne; wąskim gardłem staje się ręczne kodowanie zachowań z transkryptów.
- Tokenizer: pomiar chaina w cl100k, Claude liczy polski inaczej. Nieskalibrowane.
- Hipoteza do sprawdzenia: skoro nakaz ogólny nie działa, a wskazanie punktowe tak, to czy `strategy/` w ogóle powinno być osobną warstwą, czy raczej rozdzielone na punktowe odsyłacze w miejscach, gdzie dana praca się zaczyna.
