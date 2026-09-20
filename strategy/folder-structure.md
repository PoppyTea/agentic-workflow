# Struktura folderów

Zasady robocze na czas projektu. Do rewizji, gdy wybierzemy docelowy workflow.
Nazewnictwo plików i folderów jest w `naming.md`.

## Trzy warstwy

- `AGENTS.md` w folderze: kontrakt operacyjny dla agenta (co tu jest, jakie reguły, gdzie
  szukać). Po angielsku, wskaźnikowo.
- `strategy/`: trwałe dokumenty kierunkowe (zasady, decyzje, słownik). Po polsku.
  Agent sięga po nie tylko wtedy, gdy wykonuje czynność, której dotyczą; `AGENTS.md`
  wskazuje, kiedy.
- Stan pracy (spec bieżącego zadania, kolejka, postęp): w artefakcie, którego dotyczy,
  albo w trackerze. Nigdy w `AGENTS.md` ani w `strategy/`.

## W repo

- Root: wyłącznie `AGENTS.md` z symlinkiem `CLAUDE.md`, `README.md`, `LICENSE`,
  `.gitignore` i foldery domenowe. Żadnych luźnych plików roboczych.
- `research/`: materiały źródłowe i ich oceny.
  - `videos/`: notatki z materiałów wideo i syntezy ich triage'u.
  - `prompts/`: prompty przekazywane zewnętrznym modelom.
  - `reports/`: surowe, nieedytowane wyjścia zewnętrznych modeli.
- `strategy/`: dokumenty kierunkowe, płaska lista plików.
- `.help/`: lokalny scratch, gitignored. Nic trwałego.
- Nowy folder powstaje, gdy ma własny cel i przynajmniej dwa pliki albo własne reguły.
  Wtedy dostaje `AGENTS.md` i symlink; wpis w indeksie rodzica.
- Folder na jeden typ artefaktu (`prompts/`, `reports/`), nie na jeden temat. Temat
  łączy pliki przez wspólny człon nazwy (patrz `naming.md`).

## Poza repo

- Dysk Google, folder „🔬Deep Research GEM": materiały o Gemini Deep Research. Repo
  trzyma wskaźniki (tytuł, id), nie kopie.
- Nowe ustalenia dla Dysku zapisujemy jako nowy dokument w folderze źródłowym, w jego
  konwencji (identyfikatory ODK/HEU/HIP/POM), do scalenia przez człowieka.

## Otwarte

- Wstrzykiwanie tych zasad przez własne narzędzie przy tworzeniu pliku (zamiast
  powtarzania ich w każdym `AGENTS.md`). Kandydat na long-run.
