#!/usr/bin/env bash
# Seria przebiegów agenta, sekwencyjnie, w podanej kolejności. Warianty przeplataj,
# żeby ewentualny dryf po stronie API albo huba rozłożył się równo.
#
# Wznawialny: pomija pary, które mają już domknięty przebieg (.meta z linią "koniec").
# Po każdym przebiegu robi kopię results/ poza repo, bo results/ jest gitignored
# i transkrypty istnieją w jednym egzemplarzu.
# Przy trafieniu w limit zapisuje results/RATE_LIMIT i kończy czysto, zamiast
# marnować kolejne wywołania.
#
# Użycie (odłączone od terminala):
#   setsid nohup ./batch.sh results/PLAN.txt > results/batch.log 2>&1 < /dev/null &
set -uo pipefail
cd "$(dirname "$0")"
# Pary bierzemy z pliku (jedna na linie), nie z argumentow: powloka uzytkownika to zsh,
# ktory nie dzieli nieujetej zmiennej na slowa, wiec lista przekazana przez $PAIRS
# trafialaby tu jako jeden argument i skrypt zrobilby jeden przebieg z bledym id.
[ $# -eq 1 ] || { echo "uzycie: $0 <plik-z-parami>   (jedna para wariant:id na linie)"; exit 1; }
[ -f "$1" ] || { echo "brak pliku z parami: $1"; exit 1; }
mapfile -t PAIRS < <(grep -vE '^[[:space:]]*(#|$)' "$1")
[ ${#PAIRS[@]} -gt 0 ] || { echo "pusta lista par"; exit 1; }
echo "=== plan: ${#PAIRS[@]} przebiegow"

BACKUP=${BACKUP:-/home/lis/projekty/14_moje_workflow/02_aid4u-bench/_results-backup/round-2}
mkdir -p results "$BACKUP"
rm -f results/RATE_LIMIT

done_already=0
for pair in "${PAIRS[@]}"; do
  v=${pair%%:*}; id=${pair##*:}
  meta=results/$v-$id.meta

  if [ -f "$meta" ] && grep -q '^koniec' "$meta"; then
    done_already=$((done_already + 1))
    continue
  fi

  echo "=== $v $id $(date -Is)"
  ./run_agent.sh "$v" "$id" 2>&1 | grep -v mcp-sdk | tail -6

  # limit albo inna awaria: brak linii result w transkrypcie, albo jawny komunikat
  jsonl=results/$v-$id.jsonl
  if ! grep -q '"type":"result"' "$jsonl" 2>/dev/null \
     || grep -qiE 'rate.?limit|usage limit|429|quota' "$jsonl" 2>/dev/null; then
    { echo "wariant=$v id=$id"; date -Is; tail -c 2000 "$jsonl" 2>/dev/null; } > results/RATE_LIMIT
    echo "=== PRZERWANE: limit albo awaria przy $v $id, patrz results/RATE_LIMIT"
    rsync -a results/ "$BACKUP/"
    exit 2
  fi

  rsync -a results/ "$BACKUP/"
done

[ "$done_already" -gt 0 ] && echo "=== pominięto $done_already już zrobionych"
echo "=== WSZYSTKIE ZAKOŃCZONE $(date -Is)"
python3 analyze.py results/*.jsonl
