# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## Repository Purpose

- Meta-project: audit, evaluate and consolidate the owner's agentic coding workflows (Claude Code, DOX, skills, Linear, CodeRabbit, docker-mcp-toolkit) as used in their other repos, then choose one target workflow path
- Goals, phases and status are human-facing and live in `README.md` (Polish); this file holds rules and pointers only
- Out of scope: building a custom agent or harness. Work targets the agent loop and the process around it

## Repository Map

- `README.md` — goals, phases, status
- `research/` — source material and evaluations (video notes, prompts for external models, workflow surveys) → `research/AGENTS.md`
- `.help/` — gitignored local scratch; nothing durable lives there
- `LICENSE` — MIT

## Local Contracts

- Every `AGENTS.md` has a sibling `CLAUDE.md` symlink created from inside its folder as `ln -s ./AGENTS.md ./CLAUDE.md`; the link target must stay exactly `./AGENTS.md` so the pair survives folder moves
- `AGENTS.md` files are pointer-first: rules, ownership, paths. Narrative and explanations go to `README.md` or to the owning folder's own docs
- Detail depth follows nesting: root stays repo-wide, each child doc carries the concrete details of its own files
- `README.md` owns the basic description of this repo; do not restate it here

## User Preferences

- `AGENTS.md` files are written in English; every other file is in Polish unless it quotes English source material
- Keep `AGENTS.md` information density high; trim anything derivable from the files themselves
- Refer to Linear issues in user-facing messages as markdown links (global rule in `~/.claude/CLAUDE.md`)
- Guardrail: when the user proposes an unusual use of a tool (a convention that tool's typical users would not recognise), say so before implementing; reference case: Linear used as a logbook in ZPO-Manager, fixed in IncreMental
- `AGENTS.md` and strategy docs never hold work state (progress, todo lists, done markers); state lives in the artifact it describes or in the tracker built for it

## Child DOX Index

- `research/AGENTS.md` — collected sources and their evaluations: `research/videos/`, `research/prompts/`
