#!/usr/bin/env bash
# Rebuild every deck as an editable PowerPoint file.
#
#   cd src && ./pptx-all.sh            (serves the repo root on :8766 itself)
#
# Needs: node with playwright, python3 with python-pptx.
set -e
DECKS="opening block1 block2 costing block3a block3b modelling block3c"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${TMPDIR:-/tmp}/ee-pptx"
mkdir -p "$WORK"

( cd "$ROOT" && python3 -m http.server 8766 >/dev/null 2>&1 & echo $! > "$WORK/server.pid" )
trap 'kill "$(cat "$WORK/server.pid")" 2>/dev/null || true' EXIT
sleep 2

for d in $DECKS; do
  node "$ROOT/src/pptx-extract.mjs" "$d" "$WORK"
  python3 "$ROOT/src/pptx-build.py" "$d" "$WORK" "$ROOT/slides"
done
echo "Done. Eight .pptx files in slides/."
