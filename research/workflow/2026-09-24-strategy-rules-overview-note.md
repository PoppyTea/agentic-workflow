# Przegląd `aid4u/strategy/rules/`

Opisy plików z folderu `strategy/rules/` (aid4u), pogrupowane wg przypisanej funkcji.
`confidency lvl` w skali 1–6 (6 = wiedza poparta metadanymi w pliku, nie domysł).

## Meta / indeks reguł

### `AGENTS.md`

Korzeń DOX dla całego folderu `rules/` — opisuje format pojedynczej reguły (jedna reguła
= jeden plik `rNN-slug.md`, frontmatter `id/severity/scope/zrodlo`), tabelę egzekwowania
severity i powód, dla którego folder w ogóle istnieje jako `AGENTS.md` (CodeRabbit czyta
`knowledge_base.code_guidelines` po `**/AGENTS.md`). Zawiera też digest reguł `ERROR` w
pełnej treści, czytany bezpośrednio przez CodeRabbit.

- **Funkcja:** Indeks kontraktu reguł
- **Confidency lvl:** 6

### `proposed-rules-2026-08-18.md`

Kwarantanna pięciu kandydatów na nowe reguły (timeout na klientach LLM, spójność
structured loggingu, idempotency przy retry, zakaz logowania sekretów, audyt zależności)
z timeboxowanego rozpoznania 2026-08-18. Jawnie oznaczony jako nieaktywny — wymaga
akceptacji usera przed migracją do `rNN`.

- **Funkcja:** Propozycje reguł
- **Confidency lvl:** 6

## Reguły egzekwowane przy każdym czytaniu kodu

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

## Reguły znaczące tylko przy diffie PR-a (`pr-review/`)

### `pr-review/r10-input-acquisition-strategy.md`

Sekcja `Ownership` nowego `AGENTS.md` zadania musi opisać źródło/typ wejścia, mechanizm
uwierzytelnienia, zmienność danych i cache'owanie, zanim `solve()` zostanie
zaimplementowane.

- **Funkcja:** Dokumentacja źródeł danych
- **Confidency lvl:** 6

### `pr-review/r11-public-docstrings.md`

Każda publiczna funkcja/metoda/klasa (w tym klasy testowe i nadpisania metod bazowych)
wymaga niepustego docstringa jako pierwszej instrukcji — egzekwowanie na poziomie PR-a
decyzji "Docstringi default ON" z root `AGENTS.md`.

- **Funkcja:** Wymóg docstringów
- **Confidency lvl:** 6

## Meta-reguły audytu całego repo (`contract-audit/`)

### `contract-audit/r16-fix-propagation-gaps.md`

Meta-reguła uzasadniająca istnienie rutyny `contract-audit`: szuka miejsc, gdzie
zabezpieczenie przyjęte w jednym miejscu repo (np. `reraise=True`, sprawdzanie
`status_code`, respektowanie `dry_run`) nie zostało powielone w analogicznych miejscach.

- **Funkcja:** Audyt rozjazdów poprawek
- **Confidency lvl:** 6

### `contract-audit/r17-silent-failure-filter.md`

Filtr stosowany po r16 przed zgłoszeniem — przepuszcza tylko naruszenia nieujęte w
`accepted` z `contract_audit.json`, mogące zawieść cicho, i dotyczące realnie
wykonywanego kodu; twardy limit 3 zgłoszeń na przebieg.

- **Funkcja:** Filtr cichych awarii
- **Confidency lvl:** 6

## Higiena repo i rejestr długu (`cleanup/`)

### `cleanup/r18-no-local-issue-registers.md`

Zakaz nowych lokalnych rejestrów długu/TODO poza Linear (jedyne źródło prawdy) — wykrywa
nowe pliki `.md` z tabelą Priorytet/Status poza dozwolonymi wyjątkami (`.issues.md`,
żywe checklisty sezonu, inline kotwice).

- **Funkcja:** Zakaz rejestrów issues
- **Confidency lvl:** 6

### `cleanup/r19-naming-conventions.md`

Wskaźnik egzekwujący `strategy/naming-conventions.md` (jedyne źródło prawdy nazewnictwa)
wobec nowych/zmienionych plików — nie duplikuje treści zasad.

- **Funkcja:** Zgodność nazewnictwa
- **Confidency lvl:** 6

### `cleanup/r20-issues-md-freshness.md`

Sprawdza, czy 10 generowanych plików `.issues.md` odzwierciedla bieżący stan Linear
(re-query po `area/*` i diff) — rozjazd oznacza brak regeneracji albo ręczną edycję
pliku, która sama jest naruszeniem.

- **Funkcja:** Świeżość pointerów issues
- **Confidency lvl:** 6

## Triage wyników CodeRabbit (`coderabbit-ingest/`)

### `coderabbit-ingest/r21-severity-remap.md`

Zakazuje bezmyślnego kopiowania severity CodeRabbit (Major/Minor/Nit) na priorytet Linear
— wymaga oceny realnego ryzyka w tym repo i zapisania uzasadnienia w opisie issue.

- **Funkcja:** Remap severity CodeRabbit
- **Confidency lvl:** 6

### `coderabbit-ingest/r22-known-false-positives.md`

Referencja (nie duplikat `.coderabbit.yaml`) nazywająca znane wzorce fałszywych
pozytywów CodeRabbit w tym repo (granica telemetrii w `core/llm/client.py`, sugestie
`setup_observability()` w modułach bibliotecznych, nitpicki na materiałach kursu,
sugestie usunięcia nagłówka statusu epizodu), żeby `review-ingest` wiedziała, co
downgradować.

- **Funkcja:** Fałszywe pozytywy CodeRabbit
- **Confidency lvl:** 6
