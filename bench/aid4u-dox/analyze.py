"""Streszcza przebiegi z run_agent.sh. Użycie: python3 analyze.py results/*.jsonl"""
import json, sys
from collections import Counter
from pathlib import Path

TASK_DOC = "tasks/s01e02_findhim/doc"
rows = []
for f in sys.argv[1:]:
    tools, reads, bashes, first_doc, turns = Counter(), [], [], None, 0
    res = {}
    for line in Path(f).read_text().splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            turns += 1
            for blk in ev.get("message", {}).get("content", []):
                if blk.get("type") == "tool_use":
                    name = blk.get("name"); inp = blk.get("input", {})
                    tools[name] += 1
                    if name == "Read":
                        reads.append(inp.get("file_path", ""))
                        if first_doc is None and TASK_DOC in inp.get("file_path", ""):
                            first_doc = len(reads)
                    if name == "Bash":
                        bashes.append(inp.get("command", ""))
        elif ev.get("type") == "result":
            res = ev
    u = res.get("usage", {})
    rows.append({
        "plik": Path(f).stem, "tury": res.get("num_turns", turns), "koszt_usd": round(res.get("total_cost_usd", 0), 3),
        "min": round(res.get("duration_ms", 0) / 60000, 1), "in_tok": u.get("input_tokens", 0),
        "cache_read": u.get("cache_read_input_tokens", 0), "out_tok": u.get("output_tokens", 0),
        "Read": tools["Read"], "Grep+Glob": tools["Grep"] + tools["Glob"], "Bash": tools["Bash"],
        "pytest": sum("pytest" in b for b in bashes), "solve": sum("run.py solve" in b for b in bashes),
        "AGENTS_read": sum("AGENTS.md" in r or "CLAUDE.md" in r for r in reads),
        "1szy_doc": first_doc, "wynik": "błąd" if res.get("is_error") else ("flaga" if "{FLG:" in str(res.get("result", "")) else "?"),
    })
if not rows:
    sys.exit("brak danych")
keys = list(rows[0])
print(" | ".join(keys)); print("|".join("---" for _ in keys))
for r in rows:
    print(" | ".join(str(r[k]) for k in keys))
