# strategy/skills

## Purpose

Kiedy który skill się uruchamia, co robić przy konflikcie i jakie dane skille przekazują sobie nawzajem.

## Ownership

- `skill-activation.md`: pełny roster zainstalowanych skilli, macierz wyzwalaczy, decyzja „bug w kodzie czy w prompcie", łańcuch obserwowalności, rozstrzyganie konfliktów. Skrócony roster dla efficiency mode jest w root `AGENTS.md`; w razie rozbieżności ten plik jest pełniejszy, root jest obowiązujący.
- `skill-contracts.md`: interfejsy między skillami (`aid4u-task-kickoff` → `001-papaver-tw-integration` → `neurodivergent-visual-org`, kickoff → `aid4u-learning-mode`): co jeden emituje, czego drugi oczekuje. Bloki wejść/wyjść ilustrują kontrakt, nie są szablonami.

## Local Contracts

- Nowy skill trafia do rosteru w `skill-activation.md` z wyzwalaczem i konfliktami w tym samym PR.
- Operacje TaskWarrior wyłącznie przez `001-papaver-tw-integration`.

## Work Guidance

## Verification

## Child DOX Index

- none
