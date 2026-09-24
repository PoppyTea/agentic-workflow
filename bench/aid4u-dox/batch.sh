#!/usr/bin/env bash
# Seria przebiegów agenta, sekwencyjnie, w podanej kolejności. Warianty przeplataj,
# żeby ewentualny dryf po stronie API albo huba rozłożył się równo.
#
# Wznawialny: pomija pary, których przebieg jest domkniety I przechodzi check_run.py.
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

  # Sam marker "koniec" nie wystarcza: run_agent.sh pisze go bezwarunkowo, zanim
  # check_run.py obejrzy transkrypt. Przebieg odrzucony przez walidacje musi zostac
  # powtorzony, a nie pominiety przy wznowieniu.
  if [ -f "$meta" ] && grep -q '^koniec' "$meta" \
     && python3 check_run.py "results/$v-$id.jsonl" >/dev/null 2>&1; then
    done_already=$((done_already + 1))
    continue
  fi

  echo "=== $v $id $(date -Is)"
  ./run_agent.sh "$v" "$id" 2>&1 | grep -v mcp-sdk | tail -6

  # Status bierzemy z pola is_error/subtype w linii result, NIE z grepa po transkrypcie:
  # agent czyta pliki repo opisujace throttle i kod 429, wiec te napisy sa tam legalnie
  # i grep dawal falszywy alarm przy kazdym udanym przebiegu.
  jsonl=results/$v-$id.jsonl
  if ! status=$(python3 check_run.py "$jsonl"); then
    { echo "wariant=$v id=$id"; date -Is; echo "status: $status"; } > results/RATE_LIMIT
    echo "=== PRZERWANE przy $v $id: $status"
    rsync -a results/ "$BACKUP/"
    exit 2
  fi
  echo "    $status"

  rsync -a results/ "$BACKUP/"
done

[ "$done_already" -gt 0 ] && echo "=== pominięto $done_already już zrobionych"
echo "=== WSZYSTKIE ZAKOŃCZONE $(date -Is)"
python3 analyze.py results/*.jsonl
