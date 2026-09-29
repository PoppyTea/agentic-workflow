# Spostrzeżenia

## DOX & CLAUDE.md & Strategy/rule files

### Perspektywa

Od razu chcę zaznaczyć, że tytuł paragrafu celowo mieści te wszystkie rozbite części i opisuje je zbiorowo.
Wszystkie z tych plików są bowiem z punktu widzenia technicznej budowy workflow są tym samym - kontekstem który powinien zostać wstrzyknięty przed wiadomością użytkownika.
Widziałem je jednak osobno nie dlatego, że ich podział jest zły sam w sobie.
Izolacja takich kontekstów jest lepsza niż jeden wielki plik, choćby ze względu na dopasowanie konfiguracji do danego problemu.
Po prostu patrzyłem na nie z pespektywy inżynierii kontekstu od strony znaczeniowej, pomijając "mechaniczny" aspekt przesuwania kontekstu w odpowiednie miejsca.
Próbowałem całą tę pracę zrzucić na agenta, który miałby najpierw wnioskować gdzie sięgnąć po A, B, C ... i przy każdej operacji zastanawiać się też czy któraś z opcji podanych przy pointerach klasyfikuje się jako problem z specjalnym zestawem instrukcji.
Hiperbolizuję tutaj, jednak wydaje mi się mało realne, żeby można było na czymś takim realnie polegać.

### Wspólny problem

Patrząc na to od strony technicznej otrzymujemy rozbite na części instrukcje, które musimy mieć możliwość składać w różne zestawy w zależności od tego co jest aktualnie potrzenbne. Dodatkowo ten zbiór ma trafiać do kontekstu agenta przed promptem użytkownika.

#### Kamuflarz dla problemu zarządzania kontekstem

Mamy już coś takiego co jest wstrzykiwane przed promptem użytkownika. `CLAUDE.md`
Więc patrząc na to teraz wydaje mi się, żesystem który budowałem nie jest rozwiązaniem problemu z obszernymi CLAUDE.md. Przypomina to sprzątanie radioaktywnych narzędzi z chałdy na środku pokoju przez przeniesienie problemu obok do składziku. Wszystko jest lepiej poukładane i lepiej wygląda - więc faktycznie jeśli już komuś zechce się pójść do składziku to łatwiej coś tam znajdzie. Nawet promieniowania się mniej dostaje do domu. Ale jednak promieniowanie nie znika tylko okresowo maleje i wzrasta.
Na tej zasadnie pliki `strategy` nie rozwiązują to problemu np. obszernych opisów metodyki i czynności - de fakto esencji plików `strategy`.
Patrząc na to w ten sposób wydaje mi się, że powinno to być zadanie oddelegowane nie do wstrzykiwanego kontekstu, ale dla **wywoływanego skilla**

## Pliki reguł

Inną częścią radioaktywnych plików, wyłowionych z tego starego systemu są pliki reguł/zasad.

[**Przegląd reguł egzekwowaneych przy każdym czytaniu kodu**](<2026-09-24-strategy-rules-overview-note#Reguły egzekwowane przy każdym czytaniu kodu>)
Poniższy wyciąg z pliku [[2026-09-24-strategy-rules-overview-note]]

- Folder: `common/`

### `common/r05-retired.md`

Plik-marker po emerytowanej regule R5 ("non-code tylko na `main`"). Nieaktywna,
`severity: RETIRED`, zachowana wyłącznie jako ślad historyczny procesu retirement —
intencja żyje dalej jako commit-routing w root `AGENTS.md`.

- **Funkcja:** Reguła wycofana (marker)
- **Confidency lvl:** 6

### `common/r09-agents-md-contracts.md`

Wymaga aktualizacji najbliższego `AGENTS.md` w kaskadzie przy każdej zmianie zachowania
lub kontraktu komponentu (nowy tryb błędu, zmiana sygnatury, zmiana semantyki zwrotu).

- **Funkcja:** Aktualizacja AGENTS.md
- **Confidency lvl:** 6

### `common/r12-unit-tests-same-pr.md`

Wymaga testów jednostkowych dla nowego/zmodyfikowanego kodu produkcyjnego w tym samym
PR, z udokumentowanym wyjątkiem dla `tasks/**/solution.py` (weryfikacja przez realny hub
liczy się bardziej niż rytuał testowy).

- **Funkcja:** Wymóg testów jednostkowych
- **Confidency lvl:** 6

### `common/r13-single-submission-contract.md`

Zadanie wołające `hub.submit()` wewnątrz `solve()` musi nadpisać `_submit()` albo `run()`,
inaczej `BaseTask.run()` wyśle flagę drugi raz; wymaga też respektowania `self.dry_run`.
`ERROR`, z udokumentowanym potwierdzonym naruszeniem historycznym w `s02e03_failure`.

- **Funkcja:** Kontrakt jednej submisji
- **Confidency lvl:** 6

### `common/r14-narrowed-http-exception-handling.md`

Wymaga zawężonej obsługi `httpx.HTTPStatusError` (sprawdzenie konkretnego kodu, reszta
re-raise), `try/except ValueError` wokół `response.json()` na ścieżce błędu, defensywnego
parsowania `retry_after` i `reraise=True` (albo jawnej obsługi `RetryError`) przy `@retry`.

- **Funkcja:** Obsługa wyjątków HTTP
- **Confidency lvl:** 6

### `common/r15-retry-reraise-consistency.md`

Wymaga spójnego kontraktu wyjątków między wszystkimi metodami `@retry` jednej klasy —
albo wszędzie `reraise=True`, albo wszędzie jawna obsługa `RetryError`, nigdy mieszanka
(udokumentowana niespójność historyczna w `core/hub/client.py`).

- **Funkcja:** Spójność retry/reraise
- **Confidency lvl:** 6

#### Problem treści

Zawartość tych plików jest inna więc i podejście powinno być inne. Większość z tych reguł została skopiowana żywcem od `qudo`.
Jednak zasady dla `qudo` i `coderabbit` to zasady dla recenzji - nie dla piszącego - to po pierwsze. Więc sam kształt tych reguł powinien zostać sprawdzony i sprawwdzone kiedy mają być stosowane.

#### Funkcja reguł

skoro wiemy już, że obecne pliki nie powinny służyć za wzór i były napisane pod pełnienie innej funkcji - warto zapytać się: **Jaką w ogóle funkcję powinny pełnić pliki reguł?** (to pytanie warto zadać dla każdego z omawianych plików)
Spójrzymy więc na to co mamy:

- 5 folderów
    - 4 z nich zawierają zasady dla rutyn wykonujących różnego rodzaju przeglądy
        - te wypadają poza zakres naszej _obecnej_ dyskusji i _uzasadniają użycie reguł z `qudo` wewnątrz tej czwórki._ Mniej za to z `coderabbit` - ponieważ **`coderabbit` i tak dokonuje recenzji**.
    - 1 zawiera dziwny mix reguł, zapisów historycznych... wszystko tam znajdziesz. W zamyśle jednak miały to być "reguły stosowane przy każdym pisaniu kodu" (funkcjonalny odpowiednik `CLAUDE.md`. Poniżej jest lista opisująca każdy z plików w tym folderze.
    - oprócz tego mamy jeszcze pliki:
        - `CLUDE.md` / `AGENTS.md`
        - `proposed-rules-2026-08-18.md` - losowo pozostawiony plik z pomysłami przyszłych zasad. Miejsce tej treści to na dzień dzisiejszy terminal.

## Pytania diagnostyczne

_Zbiór pytań, który pomógł mi ocenić przydatność i co wazniejsze wytypować kierunek w szukaniu rozwiązań - **nie tylko w przypadku plików z regułami.**_

Wskazówki:

- Odpowiadamy w jeden z poniższych sposobów:
    - TAK/NIE
    - za pomocą skali:
        - Skala 1-10 gdzie: // _podane opisy to tylko przykłady, nie warunki_
            - `1` -> `Tragedia` Aktywnie szkodliwe,
            - `5` -> `Ujdzie` Brak stabilności wyników,
            - `10` -> `Pełen Sukces` Wszystkie oczekiwania spełnione.
    - W krótki zwięzły sposób. Optymalnie **\~3 słów**
- Dopiero odpowiedziawszy w ten sposób możesz zacząć rozwijać swój opis.
    - Uzyskujemy w ten sposób wysoką gęstośc informacyjną, zamiast mglistego vibe'u.

- Pytania o funkcję:
    - Jaką funkcję miał pełnić [podmiot]?
    - Czy faktycznie pełnił tę funkcję?
    - Zapisz funkcje:
        - Oczekiwane.
        - Realne pełnione.
    - Zaznacz przestrzeń wspólną pomiędzy realnymi i oczekiwanymi funkcjami. To są elementy które chcesz wyeliminować. #diagram_oczekiwań
- Konstrukcja i Granularność:
    - Czy [podmiot] składa się z mniejszych elementów (np. agentów, reguł)?
        - **TAK:** -> Przejdź do pytania z tagiem #Konstrukcja
    - #Konstrukcja Czy [podmiot] jest czymś więcej niż suma jego części?
        - **TAK** -> Zastosuj podejście: _Od ogółu do szczegółu._
            - Zacznij od zdefiniowania [podmiotu].
            - Dopiero później przejdź do pojedynczych elementów.
            - Zwracaj uwagę na synergie/konflikty zachodzące pomiędzy elementami.
        - **NIE** -> Zastosuj podejście: _Od szczegółu do ogółu._
            - Zacznij od rozłożenia go na części i upewnienia się, które z nich faktycznie Cię interesują.
            - Resztę elemetów zostaw.
                - Możesz wrócić do nich potem, aby dopasować je do reszty/znormalizować.
            - Systematycznie analizuj jedną część po drugiej.
- Pytania o **eval** i sposób wykonania:
    - #eval_emocjonalny pomaga często znaleźć mniej oczywiste, lub nieproporcjonalnie ważne elementy - których ważność nie wyszłaby na żadnych testach. Pomaga też w przy szukaniu rozwiązań.
        - Jakie słabe strony/problemy tego rozwiązania?
            - Co Cię najbardziej wkurza?
            - Kiedy to wkurzenie występuje?
            - Najbardziej czasochłonna część, to?
            - Najbardziej kosztowna część, to?
            - Jakie straty przyniosło to rozwiązanie?
    - #eval_techniczny daje precyzyjne mierzalne odpowiedzi. Będzie miarą pewności jaką masz w swoje rozwiązanie. Jednak pamiętaj, że eval jest tylko tak dobry, jak ustalenie sposobu pomiaru.
        - Czy możemy skwantyfikować poziom skuteczności [podmiotu]?
        - Jak radziły sobie z powierzonymi zadaniami?
            - Co udawało im się osiągnąć?
                - Pamiętasz jakieś konkretne przykłady?
            - Gdzie sobie nie radziły?
                - Pamiętasz jakieś konkretne przykłady?
        - Czy jest to najlepsze narzędzie do zadania które pełni?
            - Jakich innych rozwiązań używają:
                - Profesjonaliści?
                - Osoby hobbistycznie zajmujące się dziedziną związaną z [podmiotem] i funkcją jaką pełni?
            - Jakie rozwiązania polecają społeczności skupione dziedziny, do której [podmiot] należy?
        - Jakie inne rozwiązania przychodzą Ci do głowy?
        - Jakie inne rozwiązania są opisane w literaturze?
        - Do ich oceny możesz użyć #diagram_oczekiwań rozrysowując go dla wybranych opcji i porównując/zestawiając je ze sobą.

## Koniec proszenia się - Nadejście Deterministynego Autorytaryzmu

Z praktycznie wszystkich źródeł i moich własnych przemyśleń przekaz jest jasny: **reguły wstrzyknięte do kontekstu zawodzą.**
Czasem mniej czasem bardziej i można to oczywiście optymalizować - robiliśmy to przed chwilą w kontekście DOX.
Czy oznacza to, że nasz agent zawsze będzie miotał się jak mucha na smyczy? Na szczęście nie wszystko jest jednak stracone.
Na pomoc przychodzi stary sprawdzony deterministyczny kod.
Przy obecnych harnessach wymuszenie determistyczngo przebiegu lintera/ów, testów, wstrzyknięcia skillu, wywołanie review... jest stosunkowo proste - w naszym przypadku będziemy mówić o claude-code. Oferuje on szeroką gamę hooków, które można łączyć z czym tylko zechcemy. Pozostaje "tylko" najistotniejsza część: wymyślić **jak wyrazić regułę w sposób deterministyczny**.
Możemy to zrobić przynajmniej na kilka sposobów:

- spróbować przepisać nasze obecne reguły na deterministyczny kod // 4/10 jako główna metoda. Jako wsparcie solidne 7/10 ale trzeba pamiętać, że część z tych reguł może być zakazami konkretnych zachowań - a nie o to nam chodzi
- poszukać w sieci kodu, który odpowiada naszym potrzebom - wymaga jasnego sprecyzowania potrzeb i to akurat zaleta, ponieważ pozwoli to osiągnąć najlepsze wyniki. // 8/10 przy większym wysiłku. Potencjał 10/10 w połączeniu z następną opcją
- Zainstalować na ślepo rozwiązanie, które zdobyło uznanie w społeczności i jest szeroko zaadoptowane - licząc na "mądrość tłumu" i liczyć na możliwość dostosowania się do naszych potrzeb. // 5/10 - rzut monetą... Warto jednak zastosować tego typu rozwiązanie jako świetny punkt startowy - daje to wysoką podłogę - nie będzie gorzej niż standard który znaleźliśmy, a potencjalny sufit sięga często 10/10+.

## Materiały do zapoznania się:

[Pierwszy transkrypt](/home/lis/projekty/14_moje_workflow/03_Learning_Materials_Collection/YouTube-Transcripts/Nick_Saraev/2026-09-25_45K3zHckCnQ_I_spended_30k_on_claude_transcript-no-timestamps.txt)

[Drugi Transkrypt](/home/lis/projekty/14_moje_workflow/03_Learning_Materials_Collection/YouTube-Transcripts/Nick_Saraev/20260925-8rVQuZlRaqo-Steal_My_Actual_AI_Agent_Workflow_2027-transcript-no-timestamps.txt)
