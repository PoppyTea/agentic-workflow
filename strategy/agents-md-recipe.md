# Przepis: wybebeszenie AGENTS.md i zastąpienie treści wskaźnikami

Instrukcja do przeniesienia na inne repo. Oparta na pomiarze z `bench/aid4u-dox/`:
runda 1 (12 przebiegów, n=3 na wariant) i runda 2 (40 przebiegów, n=10), zadanie
s01e02 w aid4u. Pełne liczby i zastrzeżenia w
`research/workflow/2026-09-21-dox-bench-note.md` — **wyniki rundy 2 wchodzą do tej
noty dopiero z PR #11**, więc dopóki nie jest zmergowany, część liczb poniżej nie
ma pokrycia w wersji noty leżącej na `main`.

Zasada przewodnia, która wyszła z pomiaru: **agent wykonuje instrukcje konkretne
i ignoruje proceduralne.** Wszystko poniżej jest konsekwencją tego jednego zdania.

## Co wyszło balastem

Przycięcie chaina z 11 946 do 4 107 tokenów nie zmieniło ani skuteczności
(flaga w każdym wariancie), ani zachowań procesowych. Wycięte elementy:

| Element | Ile ważył | Co się stało po usunięciu |
|---|---|---|
| Child DOX Index z narracją (opis każdego rozwiązanego epizodu) | 2 939 tok., 60% pliku `tasks/AGENTS.md` | nic; agent i tak czytał foldery zadań bezpośrednio |
| User Preferences jako opowieść (historia ustaleń o CodeRabbit) | 2 446 tok., 38% roota | nic wykrywalnego — poza jednym punktem, patrz niżej |
| Stan: flagi, postęp certyfikatu, „sezon zamknięty" | rozproszone | nic; stan i tak jest w `.flags.json` i w trackerze |
| Historia: daty, numery PR, przebiegi sezonów | rozproszone | nic |
| Mapa repo i opisy architektury wyprowadzalne z kodu | rozproszone | nic; agent czytał `core/tasks/base.py` i sąsiednie zadania niezależnie od tego, co pisał AGENTS.md |
| Ramy DOX rozpisane na punkty (Update After Editing) | ~200 tok. | nic; ten sam efekt po skróceniu do akapitu |
| Nakaz „zidentyfikuj rodzaj pracy i doczytaj `strategy/`" | 110 tok. | **gorzej niż nic**: 0/3 odczytów wskazanego routera, wyższy koszt, więcej odczytów |

Jeden wycięty fragment jest **podejrzany o szkodliwość**, nie tylko o bezużyteczność:
preferencja o kill switchu („przy starcie czegokolwiek długotrwałego podaj komendę
zatrzymania") występuje tylko w wariancie pełnym — i tylko w nim 3 przebiegi na 10
zleciły pracę w tle, po czym zakończyły się, czekając na powiadomienie, którego
tryb nieinteraktywny nie dostarcza (Fisher p = 0,0121). Korelacja, nie dowód.

## Co okazało się nośne

| Element | Dowód |
|---|---|
| Local Contracts — numerowane, konkretne reguły | bez DOX agent nie robi przeglądu dokumentacji **nigdy** (0/10); z przyciętym DOX 9/10 |
| Verification — dosłowne komendy bramek | pełny `pytest` 3/3 z DOX wobec 1/3 bez |
| Punktowe wskazanie pliku w Work Guidance | jedyna forma odsyłacza, po którą agent sięgał w rundzie 1 |
| Tabela wskaźników z kolumną wyzwalacza | 7/10 kontaktu ze `strategy/` wobec 0/7 przy pełnym DOX (p = 0,0098) |

Warto zauważyć, czego **nie** ma na tej liście: rozmiaru. Wariant przycięty
najagresywniej miał najwięcej tur — agent nadrabiał czytaniem to, czego nie
dostał z góry. Tokeny wejścia siedzą w cache i są tanie; każdy dodatkowy odczyt
to nowa tura z pełnym kontekstem. **Nie tnij dla samego cięcia.**

## Tabela 1 — wskaźniki do dokumentów

Wstawiana do roota `AGENTS.md`, czyli do łańcucha ładowanego automatycznie.
**Zastępuje** istniejący spis treści albo indeks, nie dokłada się do niego.

| Nazwa | Co reguluje | Plik | Wiążące w | Stosować przy |
|---|---|---|---|---|
| naming-conventions | konwencje nazw plików i katalogów | `strategy/naming-conventions.md` | całe repo | tworzenie pliku lub folderu |
| observability | span i generacja dla każdego wywołania LLM | `strategy/observability.md` | `core/llm/`, `tasks/*/prompts.py` | dodanie lub zmiana wywołania LLM |
| tasks-workflow | wzorzec implementacji zadania | `strategy/tasks/workflow.md` | `tasks/`, `core/tasks/` | tworzenie folderu zadania |

Trzy wiersze wyżej to przykład z aid4u; pełna miała trzynaście i kosztowała
690 tokenów.

### Dlaczego akurat te kolumny

- **Wiążące w** pozwala agentowi pominąć wiersz **bez otwierania pliku**. To jest
  cecha, nie wada: nieprzeczytanie nieistotnej reguły to sukces wskaźnika. Dlatego
  „ile plików przeczytał" nie jest miarą jakości — mierzy posłuszeństwo, nie trafność.
- **Stosować przy** jest składnikiem czynnym. Wiersz, który agent otwierał
  najczęściej (7 na 10 przebiegów), to ten, którego wyzwalacz opisywał robotę
  wykonywaną w tym momencie. Nakaz z rundy 1 mówił dokładnie to samo ogólnie
  („zidentyfikuj rodzaj pracy") i nie zadziałał ani razu.

### Reguły pisania wierszy

1. **Wyzwalacz to czynność, nie dziedzina.** „tworzenie folderu zadania", nie
   „zadania kursowe". Agent dopasowuje do tego, co właśnie robi, nie do tematu.
2. **Jeden wiersz na plik.** Jeśli dokument obsługuje dwie niezwiązane czynności,
   to są dwa dokumenty.
3. **Ścieżka dosłowna**, do skopiowania. Bez „patrz dokumentacja strategii".
4. **Bez uzasadnień w tabeli.** Powód czytania jest w pliku docelowym.
5. **Nie dubluj.** Jeśli ten sam plik jest wskazany też punktowo w Work Guidance,
   zostaw jedno miejsce — najlepiej tabelę.
6. **Tabela mieszka w roocie**, w pliku, który ładuje się sam. Wskaźnik w pliku,
   po który trzeba sięgnąć, żeby go zobaczyć, jest bezużyteczny.

## Tabela 2 — operacje i reguły

Osobna tabela, bo reguły zachowują się inaczej niż dokumenty kierunkowe. Ta idzie
do `AGENTS.md` folderu, którego dotyczy, nie do roota.

| Operacja | Reguły | Severity | Plik | Jak sprawdzić |
|---|---|---|---|---|
| pisanie lub zmiana kodu zadania | pojedyncza submisja, obsługa błędów HTTP | ERROR | `rules_strategy.md` (w tym folderze) | `uv run pytest` |
| recenzja diffa PR-a | opis strategii wejścia, docstringi publicznych symboli | WARNING | `strategy/rules/pr-review/` | recenzja ręczna |
| tworzenie nowego `.md` | zakaz lokalnych rejestrów długu poza trackerem | ERROR | `rules_strategy.md` | `scripts/check_dox.py` |

### Wynik, który zmienia sposób wdrożenia

W 52 przebiegach obu rund **żaden wskaźnik nigdy nie doprowadził agenta do pliku
reguł.** Ani nakaz, ani tabela, ani pełny DOX: zero kontaktów.

Zadziałało jedno: położenie pliku reguł **w folderze, w którym agent pracuje**,
jako `rules_strategy.md`, **w parze z instrukcją, żeby go tam szukać**. Trzy
przebiegi na dziesięć go otworzyły — jedyne kontakty z regułami w całym pomiarze.

Uczciwe zastrzeżenie: wariant symlinkowy dostał oba zabiegi naraz (pliki na
miejscu oraz krok „wylistuj `./*_strategy.md` i przeczytaj każdy"), a wariant
z samą tabelą nie dostał żadnego z nich. Pomiar nie rozdziela, który składnik
odpowiada za wynik. Wdrażaj więc oba i nie licz na to, że sama obecność pliku
w folderze wystarczy.

Stąd wdrożenie dwuczęściowe:

- **tabela** mówi, które reguły obowiązują przy której operacji — to jest
  potrzebne, żeby agent wiedział, czego szukać i co pominąć;
- **plik albo symlink leży na miejscu**, w folderze roboczym — bo sama tabela
  do reguł nie doprowadza;
- **jeden krok w Read Before Editing** każe te pliki wylistować i przeczytać —
  bo w zmierzonym wariancie oba te elementy występowały razem.

Nazwa pliku nie może być `CLAUDE.md` ani `AGENTS.md`, jeśli chcesz mierzyć, czy
agent sam do niego sięga: te dwie nazwy harness wstrzykuje do promptu automatycznie.
Wzorzec `<nazwa>_strategy.md` przeszedł test.

Cena: wariant z symlinkami miał medianę kosztu 2,48 wobec 2,03 u wariantu z samą
tabelą (p = 0,044). Dziewięćdziesiąt symlinków w drzewie nie jest darmowe — kładź
je tam, gdzie reguła naprawdę obowiązuje, nie wszędzie.

## Procedura

1. **Zmierz chain**, zanim zaczniesz ciąć: ile tokenów ładuje się automatycznie dla
   typowej ścieżki roboczej, z podziałem na sekcje. Bez tego nie wiesz, co jest duże.
2. **Oznacz sekcje** jako: kontrakt (zostaje), bramka weryfikacji (zostaje),
   wskaźnik (idzie do tabeli), stan (wypada), historia (wypada), opis wyprowadzalny
   z kodu (wypada).
3. **Zbuduj tabelę 1** z tego, co było wskaźnikiem — z kolumną wyzwalacza.
   Zastąp nią stary indeks.
4. **Zbuduj tabelę 2** per folder i **połóż pliki reguł na miejscu**.
5. **Nie wprowadzaj nakazów proceduralnych.** „Zidentyfikuj rodzaj pracy i doczytaj"
   jest zmierzone jako nieskuteczne i kosztowne.
6. **Przejrzyj User Preferences pod kątem zachowań, nie tylko rozmiaru.** Preferencja
   może być aktywnie szkodliwa; szukaj takich, które normalizują zachowanie
   niedostępne w Twoim trybie uruchamiania.
7. **Zmierz po zmianie.** Minimum 10 przebiegów na wariant; przy 3 rozrzut wewnątrz
   wariantu przekracza wszystkie różnice między wariantami.

## Czego ten przepis nie dowodzi

- **Jedno zadanie, jeden model, jedno repo.** s01e02 w aid4u na Sonnecie. Zadanie
  nie dotyka żadnej z reguł ERROR, więc pomiar reguł mierzy dotarcie, nie zastosowanie.
- **Kontakt ≠ zgodność.** Nie wiemy, czy agent, który otworzył plik, zastosował się
  do niego. Bloki rozumowania mają w transkrypcie pustą treść, więc „rozważył
  i odrzucił" jest nieodróżnialne od „nie zauważył".
- **Koszt jest wyceną**, nie wydatkiem: maszyna logowała się subskrypcją.
- **Wynik dotyczący nakazu pochodzi z rundy 1** (n=3, ciepły cache, węższy punkt
  końcowy) i nie został powtórzony w rundzie 2. Nie zestawiaj go wprost z 7/10
  tabeli — to dwie różne miary z dwóch różnych serii. Traktuj „nie wprowadzaj
  nakazu proceduralnego" jako mocną przesłankę, nie jako wynik dowiedziony.
- **Wyniki pozytywne** (tabela 7/10, reguły 3/10) stoją na n=10 z jednej serii
  i wymagają powtórzenia na innym repo, zanim uznasz je za regułę ogólną.
