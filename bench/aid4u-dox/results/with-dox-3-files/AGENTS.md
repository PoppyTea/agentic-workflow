# s01e02_findhim Module

## Purpose
Ustala, który z podejrzanych transportowych z S01E01 był widziany najbliżej
jednej z siedmiu elektrowni atomowych, jego poziom dostępu i kod elektrowni.
Zero LLM w samym `solve()` — jedyne wywołanie LLM (tagowanie zawodów) jest
odziedziczone z S01E01 i uruchamiane tylko gdy brak zapisanego wyniku.

## Ownership
- `solution.py`: `FindhimTask` (`hub_name="findhim"`) — `POWER_PLANT_CITY_COORDS`
  (współrzędne miast dołożone ręcznie, patrz Local Contracts), `haversine_km()`,
  `parse_power_plants()`, `find_closest_match()` (czysta funkcja, testowalna
  bez mocków), `_load_or_build_suspects()`.
- `doc/`: materiały kursu (fabuła, transkrypcja, komentarze) — nieużywane w
  runtime.

## Local Contracts
- **Lista podejrzanych = S01E01, tag `transport`, nic więcej.** Ładowana z
  `data/output/s01e01_people/suspects.json` (patrz `../s01e01_people/AGENTS.md`
  i `../../data/output/AGENTS.md`); jeśli plik nie istnieje, `_load_or_build_suspects()`
  odtwarza dokładnie pipeline `PeopleTask.solve()` (import czystych funkcji z
  `tasks.s01e01_people.solution`, nie duplikacja logiki) i zapisuje wynik do
  ponownego użycia.
- **`findhim_locations.json` NIE zawiera współrzędnych elektrowni** — tylko
  nazwę miasta, `is_active` i `code` (format `PWR0000PL`). `POWER_PLANT_CITY_COORDS`
  to ręcznie dołożone współrzędne centroidów tych siedmiu miast (Wikipedia),
  potrzebne żeby w ogóle policzyć odległość do lokalizacji z `/api/location`.
  Klucze MUSZĄ być identyczne ze stringami z JSON-a huba, w tym `"Chelmno"`
  bez `ł` — tak zapisane jest po stronie huba, nie literówka w tym repo.
- **Dopasowanie = globalne minimum odległości**, nie próg/threshold. Dla
  każdego (podejrzany × zaobserwowany punkt × elektrownia) liczona jest
  odległość haversine; wygrywa najmniejsza. Zmierzone na żywych danych
  (2026-09-20): zwycięzca (Wojciech Bielik, Chełmno) miał 1.25 km, drugi
  najbliższy kandydat (Cezary Żurek, Zabrze) 2.63 km, reszta 7.9 km+ — margines
  wystarczający, żeby kilkusetmetrowa niedokładność ręcznie wpisanych
  współrzędnych miast nie zmieniała wyniku.
- `/api/location` zwraca listę (nie dict) współrzędnych — `HubClient.post_api()`
  ma typ zwracany `dict` tylko orientacyjnie, w praktyce przekazuje surowy JSON.
- `/api/accesslevel` wymaga `birthYear` jako int — bierz `suspect["born"]`
  (już wyekstrahowany rok w `s01e01_people.solution.format_answer()`), nie
  surowe pole z CSV.

## Work Guidance
- Jeśli `findhim_locations.json` kiedyś zmieni zestaw miast/elektrowni,
  `POWER_PLANT_CITY_COORDS` trzeba ręcznie dołożyć dla nowych miast — to jedyne
  miejsce niezweryfikowane automatycznie względem huba.

## Verification
- `uv run run.py solve s01e02 --dry-run` — zweryfikowane (2026-09-20):
  odtwarza identyczny wynik co ręczna analiza odległości poza runem
  (`{'name': 'Wojciech', 'surname': 'Bielik', 'accessLevel': 7, 'powerPlant': 'PWR2758PL'}`).
- Live-verified against the real hub (2026-09-20): `{FLG:BUSTED}`.

## Child DOX Index
- None.
