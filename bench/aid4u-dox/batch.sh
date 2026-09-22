#!/usr/bin/env bash
# Seria przebiegów agenta, w podanej kolejności. Warianty przeplataj, żeby ewentualny
# dryf po stronie API albo huba rozłożył się równo.
# Użycie (odłączone od terminala):
#   setsid nohup ./batch.sh clean-dox:1 strategy-dox:1 clean-dox:2 strategy-dox:2 > results/batch.log 2>&1 < /dev/null &
set -uo pipefail
cd "$(dirname "$0")"
[ $# -gt 0 ] || { echo "użycie: $0 <wariant>:<id> [<wariant>:<id> ...]"; exit 1; }
mkdir -p results
for pair in "$@"; do
  v=${pair%%:*}; id=${pair##*:}
  echo "=== $v $id $(date -Is)"
  ./run_agent.sh "$v" "$id" 2>&1 | grep -v mcp-sdk | tail -6
done
echo "=== WSZYSTKIE ZAKOŃCZONE $(date -Is)"
python3 analyze.py results/*.jsonl
