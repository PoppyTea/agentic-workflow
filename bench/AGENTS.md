# bench

## Purpose

- Reproducible measurement setups for claims made in `research/`; each sub-folder is one experiment with its own scripts, prompt and raw results

## Ownership

- `aid4u-dox/` — effect of the AGENTS.md chain on a Claude Code agent solving aid4u task s01e02; worktrees live outside this repo in `/home/lis/projekty/14_moje_workflow/02_aid4u-bench/` → `aid4u-dox/README.md`

## Local Contracts

- Scripts never modify the source repo they measure; they work on git worktrees and copies
- Raw run outputs stay local in `<experiment>/results/`, which is gitignored; only the scripts that produce them are committed
- Because the raw outputs are not in the repository, the note in `research/` is the only durable record of a measurement: it must carry the per-run table, not just averages, plus the behavioural coding behind any claim
- `AGENTS.md` files stored inside an experiment folder are measurement material for the repo under test, never contracts for this repository; the contract here is `bench/AGENTS.md`
- Every experiment README states what is measured, the variants, and the cost and side effects of a run

## Work Guidance

## Verification

## Child DOX Index

- none (experiment folders carry a README, not an AGENTS.md)
