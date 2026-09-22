# strategy-routers: uproszczone `strategy/**/AGENTS.md`

Nakładka na `strategy/` w snapshocie, wspólna dla wariantów `clean-dox` i `strategy-dox`.
Dzięki temu jedyną różnicą między nimi jest nakaz czytania `strategy/` w root `AGENTS.md`.

Ta sama reguła co w `clean-dox/`: zostaje kontrakt i router „rodzaj pracy → plik", wypada
historia, stan i opisy wynikające z plików obok.

| plik | oryginał (tokeny) | tutaj |
|---|---|---|
| `AGENTS.md` | 1 717 | 1 081 |
| `rules/AGENTS.md` | 2 031 | 955 |
| `skills/AGENTS.md` | brak | 317 |
| `tasks/AGENTS.md` | brak | 221 |
| `templates/AGENTS.md` | brak | 284 |

Pliki nie wchodzą do automatycznego chaina (`strategy/` nie leży na ścieżce z roota do
`tasks/s01e02_findhim`), więc kosztują tylko wtedy, gdy agent do nich sięgnie.
