# Weryfikacja liczb: nota o benchu DOX

Wszystko policzone Pythonem (scipy 1.17.1 / numpy) z niezależnej ekstrakcji transkryptów: parsowanie bloków `tool_use`, nie regex po tekście JSON. Każde p liczone dwiema drogami — scipy i ręczna enumeracja/kombinatoryka — zgodność do 1e-9.

## Podsumowanie

| Co | Wynik |
|---|---|
| komórki tabel per przebieg (runda 1 i 2) | 404 sprawdzonych, 2 niezgodnych |
| twierdzenia zbiorcze | 92 ✓, 1 ✗, 14 ⚑ (kwestia metody) |
| tokeny chaina (6 wariantów + sekcje) | wszystkie zgodne co do tokena |

**Arytmetyka noty jest poprawna.** Jest jeden błąd liczbowy i dwa zaokrąglenia. Problemy leżą w metodzie: dwie pary liczb zestawione obok siebie mierzą różne rzeczy, a korekta na wiele porównań zmienia to, które wyniki można nazwać istotnymi.

## ✗ Błędy liczbowe

- **mediana tur no-dox**: nota `48`, przeliczone `48.5`. Przy n=10 mediana to średnia 5. i 6. wartości.
- **pointer-dox-8 / koszt**: nota `2.23`, surowa wartość `2.2247`. Podwójne zaokrąglenie (najpierw do 3 miejsc przez `analyze.py`, potem do 2).
- **symlink-dox-10 / koszt**: nota `2.44`, surowa wartość `2.4452`. Podwójne zaokrąglenie (najpierw do 3 miejsc przez `analyze.py`, potem do 2).

## ⚑ Metoda

### 1. p-wartości kosztu liczone na średnich, a stoją obok median

Nota pisze „mediana 2,48 wobec 2,03 (p = 0,044)”. To p pochodzi z testu na różnicy **średnich**. Test na różnicy median daje co innego:

| Porównanie kosztu | p (średnie) | p (mediany) | Mann-Whitney |
|---|---|---|---|
| pointer vs symlink | 0.0436 | 0.1024 | 0.0630 |
| no vs symlink | 0.0465 | 0.0113 | 0.0433 |

Wniosek „`symlink-dox` droższy od `pointer-dox`” traci istotność przy medianach (0,10) i przy Mann-Whitneyu (0,06). Wniosek „droższy od `no-dox`” się wzmacnia. Trzeba albo raportować średnie przy tych p, albo p z testu na medianach.

### 2. Brak korekty na wiele porównań

Nota podaje pięć p-wartości jako osobne odkrycia. Korekta Holma–Bonferroniego (α = 0,05):

| Test | p w nocie | p Holm | Wersja spójna* | p Holm |
|---|---|---|---|---|
| kontakt pointer vs with (n=7) | 0.0098 | 0.0491 ✓ | kontakt pointer vs with (n=10): 0.0031 | 0.0155 ✓ |
| kontakt pointer vs no | 0.0198 | 0.0593 ✗ | kontakt pointer vs no: 0.0198 | 0.0451 ✓ |
| wykolejenia with vs reszta | 0.0121 | 0.0491 ✓ | wykolejenia with vs reszta: 0.0121 | 0.0451 ✓ |
| koszt pointer vs symlink (średnie) | 0.0436 | 0.0871 ✗ | koszt pointer vs symlink (mediany): 0.1024 | 0.1024 ✗ |
| koszt no vs symlink (średnie) | 0.0465 | 0.0871 ✗ | koszt no vs symlink (mediany): 0.0113 | 0.0451 ✓ |

\* wersja spójna: `with-dox` z n=10 w teście binarnym (niżej, pkt 3) i koszt na medianach, zgodnie z tym, co nota raportuje.

W wersji z noty po korekcie przeżywa 2 z 5: kontakt pointer vs with (n=7) (p_Holm = 0.0491); wykolejenia with vs reszta (p_Holm = 0.0491). W wersji spójnej przeżywa 4 z 5: kontakt pointer vs with (n=10) (p_Holm = 0.0155); kontakt pointer vs no (p_Holm = 0.0451); wykolejenia with vs reszta (p_Holm = 0.0451); koszt no vs symlink (mediany) (p_Holm = 0.0451).

Uwaga: prawdziwa rodzina porównań jest większa niż pięć, bo przeglądaliśmy wiele miar i par wariantów, zanim wybraliśmy te do raportu. Korekta na pięć testów jest więc dolnym ograniczeniem ostrożności, nie górnym.

### 3. `with-dox` n=7 w teście binarnym

Wykolejone przebiegi też mają obserwację „kontakt ze `strategy/`” — zero. Wyrzucenie ich ma sens dla kosztu i tur, nie dla zmiennej binarnej. Przy n=10: p = 0.0031 zamiast 0,0098. Wynik się wzmacnia, więc nota zaniżała siłę swojego głównego twierdzenia.

### 4. Wykolejenia: pula 0/30

3/10 wobec 0/30 daje p = 0,0121, ale łączy trzy warianty w jedną grupę kontrolną. Parami każde porównanie `with-dox` z innym wariantem daje p = 0.2105. Pula jest uprawniona, jeśli hipoteza brzmi „pełny DOX wobec wszystkiego innego”, a tak ją postawiono (preferencja o kill switchu jest tylko w `with-dox`). Trzeba to jednak napisać wprost.

### 5. Korelacja r = 0,93 zależy od wykluczenia

Na 37 ważnych przebiegach r = 0.9317. Na wszystkich 40: r = 0.5838, bo `with-dox-4` ma jedną turę przy koszcie 3,15. Liczba jest poprawna, ale nota powinna podać, że liczono ją bez wykolejonych.

### 6. Definicja „kontaktu ze `strategy/`”

Nota liczy kontakt z dowolnego wejścia narzędzia (Read, Grep, Glob, polecenie Bash). Jeśli liczyć tylko jawne `Read`, `symlink-dox` ma 5/10 zamiast 6/10, a pozostałe warianty się nie zmieniają. Warto to zdefiniować w nocie.

### 7. quadrantChart

Oś X jest liniowym przeskalowaniem mediany kosztu na przedział ok. [1,46; 2,84] (odchyłka od prostej ≤ 0,0001), więc spójna. Oś Y `with-dox` = 0,04 przy faktycznym 0/7: przesunięcie, żeby punkt nie leżał na krawędzi. Warto dopisać, że to zabieg graficzny.

## ✓ Potwierdzone

- chain: 11946 = 708 + 6377 + 4861; sekcje przeglądowe 2446 + 2939 = 45,08% chaina; clean 4107, strategy 4217 (nakaz = 110), pointer 4797, symlink 4151
- 38/40 flag, 37 ważnych, 52 przebiegi obu rund, wykolejone = dokładnie trzy przebiegi z `run_in_background`/`Monitor`
- wszystkie mediany kosztu i zakresy, mediany tur poza `no-dox`, średnie rundy 1 i średnie z mojej wiadomości
- zliczenia zachowań rundy 2 (kontakt, reguły, DOX pass, testy, `data/output`) i rundy 1
- Fisher 0,0098 / 0,0198 / 0,0121; permutacje (średnie) 0,0436 / 0,0465 / 0,0926; separacje rundy 1 i p = 1/20 = 0,05

## Pełna lista twierdzeń

| Sekcja | Twierdzenie | Nota | Przeliczone | Status |
|---|---|---|---|---|
| runda 2 | liczba przebiegów rundy 2 | 40 | 40 | ✓ |
| runda 2 | przebiegi obu rund | 52 | 52 | ✓ |
| runda 2 | flagi w rundzie 2 | 38/40 | 38/40 | ✓ |
| runda 2 | ważne przebiegi (bez wykolejonych) | 37 | 37 | ✓ |
| runda 2 | wykolejone = te z pracą w tle | with-dox-4,5,10 | with-dox-10,with-dox-4,with-dox-5 | ✓ |
| runda 2 | mediana kosztu with-dox (n=7) | 2.62 | 2.6235 | ✓ |
| runda 2 | mediana tur with-dox | 57 | 57.0 | ✓ |
| runda 2 | zakres kosztu with-dox | 2.08–2.84 | 2.0840–2.8381 | ✓ |
| runda 2 | średnia tur with-dox (moja wiadomość) | 60.3 | 60.286 | ✓ |
| runda 2 | średnia kosztu with-dox (moja wiadomość) | 2.49 | 2.4925 | ✓ |
| runda 2 | mediana kosztu no-dox (n=10) | 1.7 | 1.7008 | ✓ |
| runda 2 | mediana tur no-dox | 48 | 48.5 | ✗ |
| runda 2 | zakres kosztu no-dox | 1.39–3.19 | 1.3873–3.1909 | ✓ |
| runda 2 | średnia tur no-dox (moja wiadomość) | 52.8 | 52.8 | ✓ |
| runda 2 | średnia kosztu no-dox (moja wiadomość) | 1.95 | 1.9489 | ✓ |
| runda 2 | mediana kosztu pointer-dox (n=10) | 2.03 | 2.0274 | ✓ |
| runda 2 | mediana tur pointer-dox | 53 | 53.0 | ✓ |
| runda 2 | zakres kosztu pointer-dox | 1.28–2.8 | 1.2838–2.8031 | ✓ |
| runda 2 | średnia tur pointer-dox (moja wiadomość) | 52.0 | 52.0 | ✓ |
| runda 2 | średnia kosztu pointer-dox (moja wiadomość) | 2.0 | 1.9988 | ✓ |
| runda 2 | mediana kosztu symlink-dox (n=10) | 2.48 | 2.478 | ✓ |
| runda 2 | mediana tur symlink-dox | 58 | 58.0 | ✓ |
| runda 2 | zakres kosztu symlink-dox | 1.83–3.87 | 1.8279–3.8693 | ✓ |
| runda 2 | średnia tur symlink-dox (moja wiadomość) | 61.9 | 61.9 | ✓ |
| runda 2 | średnia kosztu symlink-dox (moja wiadomość) | 2.52 | 2.5187 | ✓ |
| runda 2 | contact_any with-dox | 0/7 | 0/7 | ✓ |
| runda 2 | contact_any no-dox | 1/10 | 1/10 | ✓ |
| runda 2 | contact_any pointer-dox | 7/10 | 7/10 | ✓ |
| runda 2 | contact_any symlink-dox | 6/10 | 6/10 | ✓ |
| runda 2 | rules_any with-dox | 0/7 | 0/7 | ✓ |
| runda 2 | rules_any no-dox | 0/10 | 0/10 | ✓ |
| runda 2 | rules_any pointer-dox | 0/10 | 0/10 | ✓ |
| runda 2 | rules_any symlink-dox | 3/10 | 3/10 | ✓ |
| runda 2 | dox_pass with-dox | 7/7 | 7/7 | ✓ |
| runda 2 | dox_pass no-dox | 0/10 | 0/10 | ✓ |
| runda 2 | dox_pass pointer-dox | 9/10 | 9/10 | ✓ |
| runda 2 | dox_pass symlink-dox | 9/10 | 9/10 | ✓ |
| runda 2 | own_tests with-dox | 1/7 | 1/7 | ✓ |
| runda 2 | own_tests no-dox | 9/10 | 9/10 | ✓ |
| runda 2 | own_tests pointer-dox | 0/10 | 0/10 | ✓ |
| runda 2 | own_tests symlink-dox | 2/10 | 2/10 | ✓ |
| runda 2 | data_output with-dox | 3/7 | 3/7 | ✓ |
| runda 2 | data_output no-dox | 1/10 | 1/10 | ✓ |
| runda 2 | data_output pointer-dox | 2/10 | 2/10 | ✓ |
| runda 2 | data_output symlink-dox | 5/10 | 5/10 | ✓ |
| runda 2 | kontakt tylko przez Read with-dox (kontrola definicji) | 0/7 | 0/7 | ✓ |
| runda 2 | kontakt tylko przez Read no-dox (kontrola definicji) | 1/10 | 1/10 | ✓ |
| runda 2 | kontakt tylko przez Read pointer-dox (kontrola definicji) | 7/10 | 7/10 | ✓ |
| runda 2 | kontakt tylko przez Read symlink-dox (kontrola definicji) | 6/10 | 5/10 | ⚑ |
| runda 2 | symlink-dox otworzył *_strategy.md (moja wiadomość: 5/10) | 5/10 | 5/10 | ✓ |
| runda 2 | Fisher kontakt pointer vs with (7/10 vs 0/7) | 0.0098 | 0.009821 (ręcznie 0.009821) | ✓ |
| runda 2 | Fisher kontakt pointer vs no (7/10 vs 1/10) | 0.0198 | 0.019767 (ręcznie 0.019767) | ✓ |
| runda 2 | Fisher wykolejenia with 3/10 vs reszta 0/30 | 0.0121 | 0.012146 (ręcznie 0.012146) | ✓ |
| runda 2 | Fisher pointer vs with, gdy with-dox n=10 (wykolejone też 0 kontaktu) | — | 0.003096 | ⚑ |
| runda 2 | wykolejenia parami with vs no-dox (3/10 vs 0/10) | — | 0.210526 | ⚑ |
| runda 2 | wykolejenia parami with vs pointer-dox (3/10 vs 0/10) | — | 0.210526 | ⚑ |
| runda 2 | wykolejenia parami with vs symlink-dox (3/10 vs 0/10) | — | 0.210526 | ⚑ |
| runda 2 | permutacja koszt pointer vs symlink, różnica ŚREDNICH | 0.0436 | 0.043571 (8050/184756; scipy 0.043571) | ✓ |
| runda 2 | permutacja koszt no vs symlink, różnica ŚREDNICH | 0.0465 | 0.046526 (8596/184756; scipy 0.046526) | ✓ |
| runda 2 | permutacja tury pointer vs symlink, różnica ŚREDNICH | 0.0926 | 0.092598 (17108/184756; scipy 0.092598) | ✓ |
| runda 2 | permutacja koszt pointer vs symlink, różnica MEDIAN | — | 0.102449 (18928/184756; scipy 0.102449) | ⚑ |
| runda 2 | permutacja koszt no vs symlink, różnica MEDIAN | — | 0.011269 (2082/184756; scipy 0.011269) | ⚑ |
| runda 2 | Mann-Whitney koszt pointer vs symlink | — | 0.063013 | ⚑ |
| runda 2 | Mann-Whitney koszt no vs symlink | — | 0.043257 | ⚑ |
| runda 2 | korelacja koszt–tury (37 ważnych) | 0.93 | 0.931684 (numpy 0.931684) | ✓ |
| runda 2 | korelacja koszt–tury gdyby liczyć wszystkie 40 | — | 0.583760 | ⚑ |
| runda 2 | quadrantChart x = liniowa funkcja mediany kosztu | 0.845/0.173/0.411/0.739 | max odchyłka od prostej 0.0001; skala ≈ [1.463, 2.836] | ✓ |
| runda 2 | quadrantChart y with-dox = odsetek kontaktu | 0.04 | 0.0 | ⚑ |
| runda 2 | quadrantChart y no-dox = odsetek kontaktu | 0.1 | 0.1 | ✓ |
| runda 2 | quadrantChart y pointer-dox = odsetek kontaktu | 0.7 | 0.7 | ✓ |
| runda 2 | quadrantChart y symlink-dox = odsetek kontaktu | 0.6 | 0.6 | ✓ |
| runda 2 | Holm (rodzina 5 p z noty): pointer vs with (kontakt) | bez korekty | p=0.0098 → p_Holm=0.0491 | ✓ |
| runda 2 | Holm (rodzina 5 p z noty): pointer vs no (kontakt) | bez korekty | p=0.0198 → p_Holm=0.0593 | ⚑ |
| runda 2 | Holm (rodzina 5 p z noty): wykolejenia | bez korekty | p=0.0121 → p_Holm=0.0491 | ✓ |
| runda 2 | Holm (rodzina 5 p z noty): koszt pointer vs symlink | bez korekty | p=0.0436 → p_Holm=0.0871 | ⚑ |
| runda 2 | Holm (rodzina 5 p z noty): koszt no vs symlink | bez korekty | p=0.0465 → p_Holm=0.0871 | ⚑ |
| runda 1 | średnia tury with-dox (n=3) | 57.0 | 57.0 | ✓ |
| runda 1 | średnia koszt with-dox (n=3) | 2.29 | 2.2934 | ✓ |
| runda 1 | średnia min with-dox (n=3) | 9.9 | 9.9 | ✓ |
| runda 1 | średnia Read with-dox (n=3) | 9.3 | 9.3333 | ✓ |
| runda 1 | średnia tury no-dox (n=3) | 59.7 | 59.6667 | ✓ |
| runda 1 | średnia koszt no-dox (n=3) | 2.15 | 2.1466 | ✓ |
| runda 1 | średnia min no-dox (n=3) | 11.0 | 11.0 | ✓ |
| runda 1 | średnia Read no-dox (n=3) | 12.0 | 12.0 | ✓ |
| runda 1 | średnia tury clean-dox (n=3) | 69.7 | 69.6667 | ✓ |
| runda 1 | średnia koszt clean-dox (n=3) | 2.54 | 2.5385 | ✓ |
| runda 1 | średnia min clean-dox (n=3) | 9.7 | 9.6667 | ✓ |
| runda 1 | średnia Read clean-dox (n=3) | 16.0 | 16.0 | ✓ |
| runda 1 | średnia tury strategy-dox (n=3) | 59.0 | 59.0 | ✓ |
| runda 1 | średnia koszt strategy-dox (n=3) | 2.6 | 2.6023 | ✓ |
| runda 1 | średnia min strategy-dox (n=3) | 8.6 | 8.6 | ✓ |
| runda 1 | średnia Read strategy-dox (n=3) | 18.0 | 18.0 | ✓ |
| runda 1 | clean-dox tury 63–74 vs with-dox 54–62, pełna separacja | 63–74 / 54–62 | 63–74 / 54–62; separacja=True | ✓ |
| runda 1 | strategy-dox Read 15–21 vs with-dox 5–12, pełna separacja | 15–21 / 5–12 | 15–21 / 5–12; separacja=True | ✓ |
| runda 1 | pełna separacja 3 vs 3 → p jednostronne | 0.05 | 0.050000 (MW exact 0.050000) | ✓ |
| runda 1 | dox_pass with-dox | 3/3 | 3/3 | ✓ |
| runda 1 | dox_pass no-dox | 0/3 | 0/3 | ✓ |
| runda 1 | dox_pass clean-dox | 2/3 | 2/3 | ✓ |
| runda 1 | dox_pass strategy-dox | 3/3 | 3/3 | ✓ |
| runda 1 | data_output with-dox | 2/3 | 2/3 | ✓ |
| runda 1 | data_output no-dox | 0/3 | 0/3 | ✓ |
| runda 1 | data_output clean-dox | 2/3 | 2/3 | ✓ |
| runda 1 | data_output strategy-dox | 3/3 | 3/3 | ✓ |
| runda 1 | own_tests with-dox | 0/3 | 0/3 | ✓ |
| runda 1 | own_tests no-dox | 2/3 | 2/3 | ✓ |
| runda 1 | own_tests clean-dox | 1/3 | 1/3 | ✓ |
| runda 1 | own_tests strategy-dox | 2/3 | 2/3 | ✓ |
