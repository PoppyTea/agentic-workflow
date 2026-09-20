#!/usr/bin/env bash
# Pomiar 2: jeden przebieg agenta w wybranym wariancie.
# Użycie: ./run_agent.sh <with-dox|no-dox> <id-przebiegu> [model]
# Wynik: results/<wariant>-<id>.jsonl (stream-json) + results/<wariant>-<id>.diff
# Przerwanie: Ctrl-C. Przebieg wysyła prawdziwe odpowiedzi do hub.ag3nts.org.
set -euo pipefail
BENCH=${BENCH:-/home/lis/projekty/14_moje_workflow/02_aid4u-bench}
HERE=$(cd "$(dirname "$0")" && pwd)
v=$1; id=$2; model=${3:-sonnet}
wt=$BENCH/$v
out=$HERE/results/$v-$id
[ -d "$wt" ] || { echo "brak $wt, odpal prepare.sh"; exit 1; }
cd "$wt"
git reset -q --hard && git clean -qfd -e .env -e .venv
echo "start $(date -Is) wariant=$v model=$model" | tee "$out.meta"
claude -p "$(cat "$HERE/prompt.md")" \
  --model "$model" --max-turns 80 --no-session-persistence \
  --output-format stream-json --verbose \
  --allowedTools "Read,Grep,Glob,Edit,Write,Bash(uv *),Bash(cat *),Bash(ls *),Bash(curl *),Bash(python3 *),Bash(git status*),Bash(git diff*),Bash(git log*),Bash(grep *),Bash(find *),Bash(head *),Bash(tail *),Bash(wc *),Bash(jq *)" \
  > "$out.jsonl" || true
echo "koniec $(date -Is)" | tee -a "$out.meta"
git diff --stat > "$out.diff"; git status --short >> "$out.diff"
grep -q '"s01e02"' .flags.json && echo "FLAGA: tak" | tee -a "$out.meta" || echo "FLAGA: nie" | tee -a "$out.meta"
python3 "$HERE/analyze.py" "$out.jsonl"
