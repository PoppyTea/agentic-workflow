# Pytania do lekcji AI Devs 4 i AI Devs 3: pętla, kontekst, egzekwowanie reguł

Użycie: każde pytanie trafia osobno do NotebookLM, poprzedzone preambułą z sekcji „Preambuła".
Tagi przy numerze mówią, do którego notatnika idzie pytanie. Każde zapytanie musi iść w
nowej rozmowie (`nlm notebook query … -c <nowy uuid>`): bez tego CLI dokleja pytanie do
rozmowy notatnika, a odpowiedzi-kontynuacje wracają bez przypisów.

Uruchomiony 2026-09-26 (44 zapytania). Synteza:
`research/workflow/2026-09-26-aid-lessons-synthesis.md`. Surowy raport z przypisami i
weryfikacją cytatów leży lokalnie w `.help/aid-lessons/`, poza repo: zawiera setki dosłownych
fragmentów płatnego kursu, a repo jest publiczne.

Notatniki:

- **AID4U** — „LLM_aid4u_całe_lekcje_z_grafikami" (`d3b17e86-53d1-4a08-99a8-97c67b4c962d`),
  lekcje S01E01–S05E05, publikacja od marca 2026.
- **AID3R** — „LLM_AID3R_Wszystkie_Lekcje_i_zadania" (`0ff223d0-132b-4327-a39d-a11221be66a0`),
  lekcje S00E01–S05E05 z 2024/2025. Starsza edycja: zalecenia mogą być nieaktualne, więc
  każde twierdzenie z AID3R jest w syntezie oznaczone i porównane z AID4U.

## Skąd te pytania

Pytania powstały przed czytaniem lekcji, z trzech źródeł, żeby odpowiedzi nie ustawiały pytań:

- refleksje użytkownika po benchu DOX (`research/prompts/2026-09-24-dox-workflow-reflections.md`):
  reguły wstrzyknięte do kontekstu zawodzą; `strategy/` to „składzik" zamiast rozwiązania;
  metodyka powinna być skillem wywoływanym na żądanie; reguły z `qudo`/CodeRabbit są regułami
  recenzenta, nie autora; kierunek to deterministyczne lintery, testy i hooki;
- kierunek zgłoszony osobno: minimalny DOX + obowiązkowe docstringi (kod jako kontekst);
- wyniki benchu (`research/workflow/2026-09-21-dox-bench-note.md`): rozmiar łańcucha nie wpływa
  na sukces, tabela wskaźników prowadzi do `strategy/` (7/10), plik reguł otwiera się rzadko,
  część przebiegów wykoleja się na pracy w tle.

Pytanie jest sformułowane neutralnie i prosi też o fragmenty przeciwne, żeby NotebookLM nie
potwierdzał tezy, tylko relacjonował lekcje.

## Preambuła

> Kontekst: pracuję solo z agentem kodującym (Claude Code) w repozytoriach Pythona. Instrukcje
> dla agenta trzymam w plikach Markdown (hierarchia AGENTS.md, pliki reguł, dokumenty
> strategii). Zastanawiam się, które zasady trzymać w kontekście agenta, które udostępniać na
> żądanie, a które egzekwować kodem. Odpowiadaj wyłącznie na podstawie źródeł w notatniku.
> Przy każdym twierdzeniu podaj lekcję (np. S03E01). Jeśli lekcje mówią coś przeciwnego do
> sugestii zawartej w pytaniu, przytocz to. Jeśli źródła o czymś milczą, napisz to wprost,
> zamiast uzupełniać wiedzą ogólną.

## Blok 1. Gdzie żyją instrukcje: kontekst stały, na żądanie, kod

### Q01 [AID4U, AID3R] Stały kontekst czy na żądanie

**Pytanie:** Jakie kryteria podają lekcje przy decyzji, co umieścić w instrukcji systemowej agenta, a co udostępnić dopiero na żądanie (narzędzie, dokument, wczytanie pliku, umiejętność)? Jakie koszty i ryzyka każdej z tych opcji opisują?

**Po co:** rdzeń refleksji „składzik": co ma być wstrzyknięte, a co pobierane.

### Q02 [AID4U, AID3R] Składanie instrukcji z modułów

**Pytanie:** Czy lekcje opisują dynamiczne składanie instrukcji systemowej z modułów zależnie od zadania lub etapu pracy? Kto decyduje, że moduł trafia do kontekstu: model (sam prosi o dokument) czy kod (dokłada go według reguły)? Jakie przykłady implementacji podają?

**Po co:** użytkownik opisuje instrukcje jako zestawy składane pod zadanie; pytanie, czy składa je model, czy harness.

### Q03 [AID4U] Umiejętności (skills)

**Pytanie:** Co lekcje mówią o umiejętnościach (skills) agenta: czym są, kiedy trafiają do kontekstu, skąd agent wie, że istnieją, i czym różnią się od narzędzi oraz od instrukcji systemowej? Czy opisano przypadki, w których agent nie sięgnął po umiejętność, choć powinien?

**Po co:** propozycja przeniesienia metodyki ze `strategy/` do skilla.

### Q04 [AID4U, AID3R] Zakazy kontra opis pożądanego zachowania

**Pytanie:** Jak lekcje oceniają skuteczność instrukcji w formie zakazów („nigdy nie rób X") w porównaniu z opisem oczekiwanego zachowania, przykładami lub zmianą środowiska, która uniemożliwia błąd?

**Po co:** reguły z `qudo` są zakazami; Saraev radzi pozytywy. Sprawdzamy, co mówi kurs.

## Blok 2. Determinizm kontra instrukcja

### Q05 [AID4U, AID3R] Z promptu do kodu

**Pytanie:** W jakich sytuacjach lekcje zalecają przeniesienie reguły lub logiki z promptu do kodu (walidacja, twardy warunek, blokada, schemat)? Podaj przykłady z lekcji, gdzie ograniczenie modelu rozwiązano programistycznie zamiast instrukcją, i przykłady, gdzie celowo zostawiono decyzję modelowi.

**Po co:** „Nadejście deterministycznego autorytaryzmu" z refleksji.

### Q06 [AID4U] Informacja zwrotna ze środowiska

**Pytanie:** Jak lekcje opisują przekazywanie modelowi informacji zwrotnej z narzędzi i środowiska: komunikaty błędów, wyniki walidacji, wskazówki w odpowiedzi narzędzia? Jak powinien być zbudowany komunikat, żeby agent faktycznie poprawił działanie?

**Po co:** komunikat lintera lub testu podany w odpowiednim momencie to reguła dostarczona „just in time" zamiast z góry.

### Q07 [AID4U] Mechanizmy uruchamiane przez system w pętli

**Pytanie:** Czy lekcje opisują mechanizmy uruchamiane automatycznie przez aplikację w określonych momentach pętli agenta (przed wywołaniem narzędzia, po nim, przed zakończeniem odpowiedzi, na starcie sesji), niezależnie od decyzji modelu? Do czego ich używano?

**Po co:** odpowiednik hooków Claude Code; granica harness ↔ inżynieria kontekstu.

### Q08 [AID4U] Weryfikacja przed „gotowe"

**Pytanie:** Jak lekcje proponują weryfikować wynik pracy agenta, zanim zadanie zostanie uznane za skończone? Kto weryfikuje (ten sam model, inny model, kod, człowiek), na jakiej podstawie i co się dzieje, gdy weryfikacja nie przejdzie?

**Po co:** definicja „done" i to, kto ją egzekwuje.

## Blok 3. Kod jako kontekst

### Q09 [AID4U, AID3R] Dokumentacja w kodzie

**Pytanie:** Co lekcje mówią o dokumentacji i komentarzach w kodzie jako źródle kontekstu dla agenta programistycznego? Czy jest mowa o docstringach, opisach funkcji, nazewnictwie, typach, strukturze plików?

**Po co:** kierunek „minimalny DOX + obowiązkowe docstringi".

### Q10 [AID4U] Dryf dokumentacji

**Pytanie:** Jak lekcje opisują rozjazd między dokumentacją lub notatkami a faktycznym stanem kodu albo systemu? Jakie sposoby zapobiegania proponują?

**Po co:** argument Saraeva za kodem jako jedynym źródłem prawdy; ryzyko, które docstringi mają zmniejszyć.

### Q11 [AID4U] Opisy narzędzi jako wzór dla docstringów

**Pytanie:** Jakie zasady projektowania opisów narzędzi (nazwa, opis, parametry, format odpowiedzi, komunikaty błędów) podają lekcje, żeby model wiedział, kiedy i jak narzędzia użyć? Które z tych zasad dotyczą ogólnie opisywania kodu dla modelu?

**Po co:** docstring to opis funkcji czytany przez model; kurs ma gotowe zasady dla opisów narzędzi.

## Blok 4. Odkrywalność

### Q12 [AID4U] Skąd agent wie, co jest dostępne

**Pytanie:** Jak agent w lekcjach dowiaduje się, jakie dokumenty, narzędzia lub zasoby są dostępne, zanim ich użyje? Czy opisane są indeksy, mapy, drzewa katalogów, listy wskaźników? Jakie problemy z tym związane wymieniono?

**Po co:** tabela wskaźników z benchu działa (7/10), plik reguł prawie nigdy; szukamy wyjaśnienia.

### Q13 [AID4U] Za dużo narzędzi i instrukcji naraz

**Pytanie:** Co lekcje mówią o dużej liczbie narzędzi lub instrukcji dostępnych jednocześnie: jak to wpływa na trafność wyboru i jakie techniki filtrowania lub ograniczania zestawu opisano?

**Po co:** wcześniejszy pomysł bramki filtrującej opisy narzędzi; koszt MCP.

## Blok 5. Pętla agenta

### Q14 [AID4U, AID3R] Budowa pętli

**Pytanie:** Jak lekcje opisują budowę pętli agenta: planowanie, działanie, obserwacja, refleksja, warunek zakończenia? Jakie sposoby podają, żeby agent nie kończył za wcześnie i nie krążył w kółko?

**Po co:** pętla to główny przedmiot projektu.

### Q15 [AID4U] Workflow czy agent

**Pytanie:** Jak lekcje wyznaczają granicę między deterministycznym workflow (stała sekwencja kroków albo graf) a agentem, który sam decyduje o kolejnych krokach? Kiedy zalecają jedno, kiedy drugie, i jak je łączyć?

**Po co:** które części naszego procesu (DOX pass, testy, review) powinny być krokiem stałym, a nie decyzją agenta.

### Q16 [AID4U] Praca długotrwała i asynchroniczna

**Pytanie:** Co lekcje mówią o zadaniach długotrwałych i asynchronicznych: agent działający w tle, wznawianie po przerwie, harmonogramy, wybudzanie agenta, powiadamianie człowieka o potrzebie decyzji?

**Po co:** otwarty temat „budzika" dla agenta i nocnych przebiegów.

### Q17 [AID4U] Przekazanie stanu między sesjami

**Pytanie:** Jak lekcje opisują zapisywanie i przekazywanie stanu pracy między sesjami lub wątkami (podsumowania, notatki przekazania, kompresja kontekstu)? Co powinno się w nich znaleźć i co najczęściej ginie?

**Po co:** handoffy i kompaktowanie w naszych długich sesjach.

## Blok 6. Wielu agentów, izolacja

### Q18 [AID4U, AID3R] Jeden agent czy wielu

**Pytanie:** Kiedy lekcje zalecają podział pracy między wielu agentów lub subagentów, a kiedy jednego agenta? Jak przekazywany jest kontekst między nimi i co w tym przekazaniu zawodzi?

**Po co:** forki i subagenci pracujący na jednym drzewie w tej sesji.

### Q19 [AID4U] Izolacja kontekstu i uprawnień

**Pytanie:** Co lekcje mówią o izolacji kontekstu i uprawnień agentów (osobne środowiska, ograniczony zestaw narzędzi, sandbox, zatwierdzanie akcji przez człowieka)?

**Po co:** bench pokazał wycieki (`.env`, `git log --all`, cache); uprawnienia Claude Code.

## Blok 7. Pamięć i uczenie się

### Q20 [AID4U, AID3R] Pamięć długoterminowa

**Pytanie:** Jak lekcje projektują pamięć długoterminową agenta: co zapisywać, kto decyduje o zapisie, jak unikać zaśmiecenia i wpisów nieaktualnych?

**Po co:** łańcuch aid4u miał 45% stanu i historii, dopisanych przez wcześniejsze sesje.

### Q21 [AID4U] Uczenie się na błędach

**Pytanie:** Czy lekcje opisują mechanizm, w którym agent lub system poprawia się na podstawie własnych błędów (aktualizacja instrukcji, zasad albo przykładów po porażce, automatyczna optymalizacja promptu)? Jakie ryzyka i zabezpieczenia wskazują?

**Po co:** Saraev: „ucz CLAUDE.md na błędach"; nasza obserwacja: tak narosły pliki reguł.

## Blok 8. Ewaluacja i obserwowalność

### Q22 [AID4U, AID3R] Pomiar wpływu zmiany instrukcji

**Pytanie:** Jak lekcje zalecają mierzyć wpływ zmiany promptu, instrukcji lub opisu narzędzia na zachowanie agenta? Jakie zbiory testowe, metryki, liczbę powtórzeń i narzędzia opisują?

**Po co:** porównanie z metodyką naszego benchu (n=10, testy dokładne).

### Q23 [AID4U] Niedeterminizm jako przewaga

**Pytanie:** Co lekcje mówią o niedeterministycznej naturze modeli: jak ją ograniczać, a jak wykorzystać (wiele prób, głosowanie, wybór najlepszego wyniku)?

**Po co:** S03E05; czy wielokrotne przebiegi mają miejsce w codziennym workflow, nie tylko w benchu.

### Q24 [AID4U] Obserwowalność

**Pytanie:** Jak lekcje opisują obserwowanie działania agenta (logi, ślady wykonania, podgląd pełnych zapytań)? Co warto rejestrować, żeby później ustalić, dlaczego agent pominął instrukcję albo narzędzie?

**Po co:** dwa razy myliliśmy się, analizując transkrypty regexem; pytanie o dobre praktyki śladu.

### Q25 [AID4U] Model jako sędzia

**Pytanie:** Jak lekcje opisują użycie modelu jako oceniającego (LLM-as-judge) i jakie ograniczenia wskazują? Kiedy zalecają sprawdzenie deterministyczne zamiast oceny modelu?

**Po co:** granica między regułą dla recenzenta (model) a regułą dla lintera (kod).

## Blok 9. Człowiek w pętli i wiedza

### Q26 [AID4U] Tryby współpracy

**Pytanie:** Jakie tryby współpracy człowieka z agentem opisują lekcje? Kiedy agent powinien się zatrzymać i zapytać, a kiedy działać samodzielnie? Jak lekcje radzą ograniczać liczbę przerw bez utraty kontroli?

**Po co:** marker `#do dyskusji`, nocna praca bez użytkownika, pytania zostawiane na koniec.

### Q27 [AID4U] Baza wiedzy dla AI

**Pytanie:** Jak lekcje projektują bazę wiedzy przeznaczoną dla AI: struktura, metadane, wielkość i granulacja notatek, rozdział treści dla człowieka i dla agenta, utrzymanie aktualności?

**Po co:** `research/` i `strategy/` to de facto baza wiedzy; `AGENTS.md` pisane dla agenta, README dla człowieka.

## Blok 10. Limity i koszt

### Q28 [AID4U, AID3R] Rozmiar i kolejność kontekstu

**Pytanie:** Co lekcje mówią o wpływie rozmiaru i kolejności stałej części kontekstu (instrukcja systemowa, opisy narzędzi) na koszt, cache promptu i jakość odpowiedzi? Czy zalecają konkretny układ?

**Po co:** koszt łańcucha `CLAUDE.md` i to, czy dynamiczne wstrzykiwanie psuje cache.

### Q29 [AID4U] Limity istotne dla przestrzegania instrukcji

**Pytanie:** Które jawne i niejawne ograniczenia modeli lekcje uznają za najważniejsze przy projektowaniu agenta, szczególnie te wpływające na przestrzeganie instrukcji w długim kontekście?

**Po co:** „mucha na smyczy": czy kurs opisuje, dlaczego reguły z kontekstu zawodzą.

## Blok 11. Praktyka autorów i praca z bazą kodu

### Q30 [AID4U] Jak autorzy pracują z agentami kodującymi

**Pytanie:** Jak autorzy kursu sami pracują z agentami programistycznymi (Claude Code, Cursor, Codex lub podobne)? Jakie praktyki, konfiguracje, pliki instrukcji i nawyki opisują?

**Po co:** porównanie z praktyką użytkownika; kandydaci do skopiowania.

### Q31 [AID4U] Konwencje projektu przyjazne agentowi

**Pytanie:** Co lekcje z sezonu 5 (architektura, zestaw narzędzi, rozwój funkcjonalności, produkcja) mówią o strukturze projektu, konwencjach i dokumentacji, które ułatwiają agentowi pracę w bazie kodu?

**Po co:** bezpośrednio pod kierunek „kod jako kontekst".

### Q32 [AID4U] Co się zmieniło od poprzednich edycji

**Pytanie:** Czy lekcje wprost wskazują zalecenia, techniki lub narzędzia z wcześniejszych etapów rozwoju LLM (lub wcześniejszych edycji kursu), które uznają za przestarzałe albo zastąpione? Wymień je z uzasadnieniem.

**Po co:** filtr aktualności dla odpowiedzi z AID3R.

## Blok 12. Tylko AID3R: punkty odniesienia

### Q33 [AID3R] Umiejętności i logika agenta w AI Devs 3

**Pytanie:** Jak lekcje S05E01–S05E03 (Agent, Logika, Umiejętności) definiują agenta, jego logikę podejmowania decyzji i umiejętności? Jak agent wybiera, której umiejętności lub narzędzia użyć?

**Po co:** punkt odniesienia do Q03 i Q14; widać, co się zmieniło.

### Q34 [AID3R] Produkcja i optymalizacja

**Pytanie:** Co lekcje o produkcji i technikach optymalizacji mówią o utrzymaniu jakości promptów, testowaniu ich i kontroli kosztów w działającym systemie?

**Po co:** punkt odniesienia do Q22 i Q28.
