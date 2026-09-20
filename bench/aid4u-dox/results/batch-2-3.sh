#!/usr/bin/env bash
cd "$(dirname "$0")/.."
for pair in with-dox:2 no-dox:2 with-dox:3 no-dox:3; do
  v=${pair%%:*}; id=${pair##*:}
  echo "=== $v $id $(date -Is)"
  ./run_agent.sh "$v" "$id" 2>&1 | grep -v mcp-sdk | tail -6
done
echo "=== WSZYSTKIE ZAKOŃCZONE $(date -Is)"
python3 analyze.py results/*.jsonl
