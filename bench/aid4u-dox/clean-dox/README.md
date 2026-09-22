# clean-dox: AGENTS.md przycięte do reguły ETH

Reguła: tylko instrukcje, których nie da się wyprowadzić z README i kodu. Wycięte: stan
(flagi, certyfikat, postęp), historia (daty, numery PR, przebiegi sezonów), mapa repo
i opisy architektury wynikające z kodu, narracje w User Preferences. Zachowane: Local
Contracts, Work Guidance, Verification, ramy DOX (skrócone), preferencje jako reguły.

| plik | oryginał (tokeny) | clean | |
|---|---|---|---|
| root `AGENTS.md` | 6 377 | 2 347 | 37% |
| `tasks/AGENTS.md` | 4 953 | 1 052 | 21% |

Oryginały (po scrubie s01e02) w `original/`. `prepare.sh` buduje ten wariant, podmieniając
oba pliki; wariant nie zawiera nakazu czytania `strategy/` (to różnica wobec `strategy-dox/`).
