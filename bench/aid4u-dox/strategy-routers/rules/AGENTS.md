# strategy/rules

## Purpose

Reguły recenzji i audytu kodu, jedna reguła na plik `rNN-slug.md`. Folder jest `AGENTS.md`, bo
`.coderabbit.yaml` czyta `**/AGENTS.md` jako `code_guidelines`; digest ERROR niżej jest tym, co
widzi CodeRabbit.

## Ownership

- Numeracja globalna i ciągła. Frontmatter obowiązkowy: `id`, `severity` (ERROR | WARNING | RECOMMENDATION | RETIRED), `scope` (globy), `zrodlo`.
- `common/`: egzekwowane przez każdą rutynę czytającą kod (pisanie, `pr-review`, `contract-audit`).
- `pr-review/`: mają sens tylko przy diffie PR-a.
- `contract-audit/`: meta-reguły audytu całego repo.
- `cleanup/`: higiena repo, nazewnictwo, zakaz lokalnych rejestrów issues.
- `coderabbit-ingest/`: triage wyników CodeRabbit → Linear; referencja do `.coderabbit.yaml`, które jest autorytatywne.
- `proposed-rules-*.md`: kwarantanna propozycji; nic tu nie obowiązuje, dopóki nie stanie się `rNN` po jawnej akceptacji użytkownika.

## Local Contracts

### Egzekwowanie wg severity

| Severity | Przy pisaniu kodu | W recenzji PR |
|---|---|---|
| `ERROR` | nienegocjowalne; przy zastosowaniu dopisz komentarz o zgodności | `Action_required` |
| `WARNING` | stosuj domyślnie; pominięcie wymaga jednozdaniowego uzasadnienia | `Review_recommended` |
| `RECOMMENDATION` | rozważ, gdy pasuje | `Optional` |
| `RETIRED` | poza egzekwowaniem i digestem; plik-marker | – |

### Digest reguł ERROR (czyta CodeRabbit)

| id | Reguła | Dowód `plik:linia` |
|---|---|---|
| `r13` | Zadanie wołające `hub.submit()` wewnątrz `solve()` musi nadpisać `_submit()` albo `run()`, inaczej `BaseTask.run()` wysyła flagę drugi raz. | `tasks/s02e03_failure/solution.py:223,269` |
| `r14` | `except httpx.HTTPStatusError` sprawdza konkretny udokumentowany kod, resztę re-raise'uje; `response.json()` na ścieżce błędu zawsze w `try/except ValueError`. | `tasks/s02e03_failure/solution.py:270-271` |
| `r18` | Zakaz nowych lokalnych rejestrów długu/TODO poza Linear (`strategy/issue-tracking.md`). | wzorzec: nowy `.md` z tabelą Priorytet/Status poza `.issues.md` |

Reguła `r05` jest `RETIRED`; jej intencja żyje jako commit-routing w root `AGENTS.md`.

## Work Guidance

- Dodanie reguły: plik w właściwym podfolderze, kolejny numer globalny, pełny frontmatter, treść i sekcja `## Jak zgłaszać` z labelami Linear z `strategy/issue-tracking.md`. Jeśli `ERROR`, dopisz wiersz do digestu.
- Retirement: reguła stale i świadomie odrzucana nie zostaje jako martwy `ERROR`/`WARNING`; skodyfikuj wyjątek gdzie indziej i usuń plik, albo obniż do `RECOMMENDATION` z adnotacją dlaczego.

## Verification

## Child DOX Index

- `common/`: r09, r12–r15 (+ r05 RETIRED)
- `pr-review/`: r10, r11
- `contract-audit/`: r16, r17
- `cleanup/`: r18–r20
- `coderabbit-ingest/`: r21, r22
