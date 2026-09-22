#!/usr/bin/env bash
# 3 przebiegi clean-dox i 3 strategy-dox, naprzemiennie. Uruchamiaj odłączone:
#   setsid nohup results/batch-clean-strategy.sh > results/batch-clean-strategy.log 2>&1 < /dev/null &
cd "$(dirname "$0")/.."
for pair in clean-dox:1 strategy-dox:1 clean-dox:2 strategy-dox:2 clean-dox:3 strategy-dox:3; do
  v=${pair%%:*}; id=${pair##*:}
  echo "=== $v $id $(date -Is)"
  ./run_agent.sh "$v" "$id" 2>&1 | grep -v mcp-sdk | tail -6
done
echo "=== WSZYSTKIE ZAKOŃCZONE $(date -Is)"
python3 analyze.py results/*.jsonl
