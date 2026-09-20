#!/usr/bin/env bash
# Buduje dwa izolowane snapshoty aid4u (świeże repo git z jednym commitem, bez historii) do pomiaru wpływu DOX na agenta:
#   with-dox : repo jak jest, ale bez śladów rozwiązania s01e02
#   no-dox   : to samo minus wszystkie AGENTS.md/CLAUDE.md w repo
# Użycie: ./prepare.sh [REF]   (domyślnie HEAD repo aid4u)
set -euo pipefail
SRC=${SRC:-/home/lis/projekty/10_izolowane_projekty/00_aid4u/aid4u}
BENCH=${BENCH:-/home/lis/projekty/14_moje_workflow/02_aid4u-bench}
REF=${1:-HEAD}
HERE=$(cd "$(dirname "$0")" && pwd)
TASK=tasks/s01e02_findhim

mkdir -p "$BENCH"
for v in with-dox no-dox; do
  dst=$BENCH/$v
  if [ -e "$dst" ]; then
    echo "istnieje: $dst  (usuń: rm -rf $dst; stare worktree: git -C $SRC worktree prune)"; exit 1
  fi
  echo "== $v: snapshot $REF bez historii gita"
  mkdir -p "$dst" && git -C "$SRC" archive "$REF" | tar -x -C "$dst"
  git -C "$dst" init -q
  cp "$SRC/.env" "$dst/.env"
  rm -rf "$dst/$TASK/doc" && cp -r "$SRC/$TASK/doc" "$dst/$TASK/doc"
  # folder zadania: zostaje doc/ i __init__.py
  (cd "$dst/$TASK" && find . -mindepth 1 -maxdepth 1 ! -name doc ! -name __init__.py -exec rm -rf {} +)
  rm -f "$dst/doc/superpowers/plans/s01e02.md"
  find "$dst" -name __pycache__ -type d -prune -exec rm -rf {} +
  python3 "$HERE/scrub.py" "$dst"
  if [ "$v" = no-dox ]; then
    find "$dst" -path "$dst/.venv" -prune -o \( -name AGENTS.md -o -name CLAUDE.md \) -print0 | xargs -0 rm -f
  fi
  # kontrola wycieków (doc/ zadania i dane wejściowe innych epizodów są dozwolone)
  if grep -rIl -i -E "findhim|BUSTED|s01e02" "$dst" --exclude-dir=.git --exclude-dir=.venv --exclude-dir=doc --exclude-dir=input --exclude=.gitignore | grep -v "$TASK/__init__.py" ; then
    echo "WYCIEK: powyższe pliki nadal wspominają s01e02"; exit 1
  fi
  (cd "$dst" && uv sync -q && git add -A && git -c user.name=bench -c user.email=bench@local commit -qm "bench: prepared $v")
  echo "   ok: $dst"
done
echo "gotowe. Pomiar 1: python3 $HERE/count_chain.py $BENCH/with-dox tasks/s01e02_findhim"
