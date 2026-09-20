# Nazewnictwo plików i folderów

Zasady robocze na czas projektu. Struktura folderów jest w `folder-structure.md`.

## Foldery

- kebab-case, po angielsku.
- Kolekcje artefaktów w liczbie mnogiej: `reports/`, `prompts/`, `videos/`.
- Bez dat i numerów w nazwach folderów.

## Pliki

- Wyjątki pisane wielkimi literami: `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`.
- Artefakty datowane (notatka, prompt, raport, synteza):
  `YYYY-MM-DD-<temat>-<rodzaj>[-<wariant>].md`
  - data: dzień powstania artefaktu; dla raportu dzień uruchomienia promptu.
  - temat: kebab-case, po angielsku, 2–4 słowa; prompt i jego raport mają ten sam temat.
  - rodzaj: `note`, `prompt`, `report`, `synthesis`.
  - wariant: `a`, `b`, `pass2` i podobne, tylko gdy istnieje więcej niż jeden.
- Dokumenty trwałe (strategia, przewodniki): kebab-case, bez daty.
- Nazwa narzędzia lub modelu (gemini, claude) nie wchodzi do nazwy pliku; należy do
  nagłówka wewnątrz pliku.
- Nazwy zawsze po angielsku, niezależnie od języka treści.

## Przykłady

- `2026-09-18-video-triage-prompt.md` → `2026-09-18-video-triage-report-a.md`,
  `2026-09-18-video-triage-report-b.md`
- `2026-09-18-video-triage-pass2-prompt.md` → `2026-09-18-video-triage-pass2-report.md`
- `2026-09-18-workflow-recon-prompt.md` → `2026-09-18-workflow-recon-report.md`
- `2026-09-18-ai-labs-loop-engineering-note.md`
- `2026-09-18-video-triage-synthesis.md`
