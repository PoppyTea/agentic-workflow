"""Usuwa z worktree ślady rozwiązania s01e02 poza folderem zadania. Wywoływane przez prepare.sh."""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])

# 1. flaga
flags = root / ".flags.json"
d = json.loads(flags.read_text())
d.pop("s01e02", None)
flags.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

# 2. podmiany celowane (zachowują sens zdania)
subs = {
    "tasks/AGENTS.md": [
        (r"\(np\. s01e03 pozwala wywnioskować element\s+odpowiedzi z s01e02\)", "(np. fabuła jednego epizodu bywa kluczem do innego)"),
        (r"s01e02, ", ""),
        (r"`s01e02_findhim/` \([^)]*\) ·\s*", ""),
    ],
    "AGENTS.md": [
        (r"`tasks/s01e02_findhim/AGENTS\.md`", "`tasks/<epizod>/AGENTS.md`"),
    ],
    "strategy/llm-selection.md": [(r"s01e02", "sXXeYY")],
    "tasks/s02e04_mailbox/AGENTS.md": [(r"wzorzec z `s01e02_findhim`", "wzorzec z wcześniejszego epizodu")],
    "tasks/s02e04_mailbox/solution.py": [(r"\(ten sam mechanizm co `s01e02_findhim`\)", "(mechanizm współdzielony z wcześniejszym epizodem)")],
    "tasks/s03/requirements/core-stack-decision.md": [(r"`s01e02`, ", "")],
    "tasks/s03/requirements/source/tool-inventory.md": [(r"s01e02", "sXX")],
    "data/output/AGENTS.md": [(r"`s01e02_findhim`", "`sXXeYY`"), (r"s01e02_findhim", "sXXeYY_example")],
}
for rel, pairs in subs.items():
    p = root / rel
    if not p.exists():
        continue
    s = p.read_text()
    for pat, rep in pairs:
        s = re.sub(pat, rep, s)
    p.write_text(s)

# 3. wszystko, co zostało: usuń całe linie (pliki archiwalne / listy issues)
for rel in ["AGENTS.md", "tasks/AGENTS.md", "tests/.issues.md", ".issues/archive/triage-runs/closed-prs-qodo-triage.md"]:
    p = root / rel
    if not p.exists():
        continue
    lines = [l for l in p.read_text().splitlines(keepends=True) if not re.search(r"s01e02|findhim|BUSTED|GeoPoint", l, re.I)]
    p.write_text("".join(lines))
