"""Wariant symlink-dox: przynosi dokumenty strategii do folderów, których dotyczą.

Użycie: python3 link_strategy.py <snapshot>

W każdym folderze mającym własny AGENTS.md tworzy symlinki `<nazwa>_strategy.md`
wskazujące (ścieżką względną) na właściwe pliki w `strategy/`. Symlinki celowo NIE
nazywają się CLAUDE.md ani AGENTS.md: Claude Code wstrzykuje do promptu tylko CLAUDE.md,
więc te pliki są niewidoczne, dopóki agent sam ich nie znajdzie. To jest hipoteza wariantu.
"""

import os
import re
import sys
from pathlib import Path

# nazwa symlinku -> ścieżka dokumentu względem korzenia repo
DOCS = {
    "naming-conventions": "strategy/naming-conventions.md",
    "secrets-management": "strategy/secrets-management.md",
    "observability": "strategy/observability.md",
    "llm-selection": "strategy/llm-selection.md",
    "agent-loop-safety": "strategy/agent-loop-safety.md",
    "workflow": "strategy/tasks/workflow.md",
    "secret-flags": "strategy/secret-flags.md",
    "season-transition": "strategy/season-transition.md",
    "issue-tracking": "strategy/issue-tracking.md",
    "quality-control": "strategy/quality-control.md",
    "open-decisions": "strategy/open-decisions.md",
    "rules": "strategy/rules/AGENTS.md",
}

# reguły przypisania: (dopasowanie folderu, lista kluczy z DOCS)
ROOT = ["naming-conventions", "issue-tracking", "quality-control", "open-decisions", "rules"]
BY_FOLDER = {
    "core": ["secrets-management", "observability", "agent-loop-safety", "llm-selection", "rules"],
    "tasks": ["workflow", "season-transition", "secret-flags", "llm-selection", "rules"],
    "tests": ["rules"],
    "data": ["naming-conventions"],
    "data/input": ["naming-conventions"],
    "data/output": ["naming-conventions"],
    "deploy": ["secrets-management", "rules"],
    ".issues": ["issue-tracking"],
}
TASK_EPISODE = ["workflow", "secret-flags", "rules"]      # tasks/sXXeYY_*
TASK_SEASON = ["season-transition", "rules"]              # tasks/sXX i tasks/sXX/requirements
SKIP = {"strategy", "strategy/rules"}                     # dokumenty są na miejscu

EPISODE_RE = re.compile(r"^tasks/s\d+e\d+_")
SEASON_RE = re.compile(r"^tasks/s\d+(/requirements)?$")


def docs_for(rel: str) -> list[str]:
    if rel == ".":
        return ROOT
    if rel in SKIP:
        return []
    if rel in BY_FOLDER:
        return BY_FOLDER[rel]
    if EPISODE_RE.match(rel):
        return TASK_EPISODE
    if SEASON_RE.match(rel):
        return TASK_SEASON
    return []


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    made = skipped = 0
    folders = {a.parent for a in root.rglob("AGENTS.md") if ".venv" not in a.parts}
    # Folder mierzonego zadania w prawdziwym aid4u ma AGENTS.md, ale scrub go usuwa,
    # bo opisuje rozwiązanie. Bez tego wyjątku folder, w którym agent pracuje, nie
    # dostałby żadnego symlinku i wariant nie testowałby tego, co ma testować.
    folders |= {d for d in root.glob("tasks/s*e*_*") if d.is_dir()}
    for folder in sorted(folders):
        rel = os.path.relpath(folder, root)
        keys = docs_for(rel)
        if not keys:
            skipped += 1
            continue
        for key in keys:
            target = root / DOCS[key]
            if not target.exists():
                sys.exit(f"brak dokumentu: {target}")
            link = folder / f"{key}_strategy.md"
            if link.name in ("AGENTS.md", "CLAUDE.md"):
                sys.exit(f"symlink nie może nazywać się {link.name}")
            if link.exists() or link.is_symlink():
                continue
            link.symlink_to(os.path.relpath(target, folder))
            made += 1
    print(f"symlinki: {made} utworzonych, {skipped} folderów pominiętych")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
