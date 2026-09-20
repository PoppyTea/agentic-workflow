"""Pomiar 1: ile tokenów ładuje chain plików instrukcji dla danej ścieżki roboczej.

Użycie: python3 count_chain.py <worktree> <ścieżka względna> [--sections]
Liczy: ~/.claude/CLAUDE.md + każdy AGENTS.md/CLAUDE.md od root do ścieżki (jak Claude Code
przy starcie sesji w tym katalogu). Tokenizer cl100k_base (przybliżenie, Claude ma własny).
"""
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    sys.exit("brak tiktoken: uruchom przez  uvx --from tiktoken python3 count_chain.py ...")

enc = tiktoken.get_encoding("cl100k_base")
root = Path(sys.argv[1]).resolve()
target = (root / sys.argv[2]).resolve() if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else root
sections = "--sections" in sys.argv


def pick(d: Path):
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = d / name
        if p.exists():
            return p.resolve()
    return None


files = []
g = Path.home() / ".claude" / "CLAUDE.md"
if g.exists():
    files.append(("~/.claude/CLAUDE.md", g))
rel = target.relative_to(root)
chain = [root] + [root / p for p in reversed(rel.parents) if str(p) != "."] + ([target] if target != root else [])
seen = set()
for d in chain:
    p = pick(d)
    if p and p not in seen:
        seen.add(p)
        files.append((str(d.relative_to(root)) or ".", p))

total = 0
print(f"{'tokeny':>8}  {'słowa':>6}  plik")
for label, p in files:
    text = p.read_text()
    t = len(enc.encode(text))
    total += t
    print(f"{t:>8}  {len(text.split()):>6}  {label}")
    if sections:
        cur, buf = "(nagłówek)", []
        for line in text.splitlines(keepends=True):
            if line.startswith("## "):
                if buf:
                    print(f"{len(enc.encode(''.join(buf))):>8}          {cur}")
                cur, buf = line.strip(), []
            buf.append(line)
        if buf:
            print(f"{len(enc.encode(''.join(buf))):>8}          {cur}")
print(f"{total:>8}          RAZEM (chain do {target.relative_to(root) if target != root else '.'})")
