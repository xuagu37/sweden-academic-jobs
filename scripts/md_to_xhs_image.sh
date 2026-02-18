#!/usr/bin/env bash
set -euo pipefail

# Get absolute path to this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Project root = parent of scripts/
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

RAW_DIR="$PROJECT_ROOT/data/raw"
OUT_DIR="$PROJECT_ROOT/data/images"
PY_SCRIPT="$SCRIPT_DIR/md_to_xhs_image.py"

FONT="/System/Library/Fonts/Helvetica.ttc"

mkdir -p "$OUT_DIR"
rm -rf "$OUT_DIR"/*

for f in "$RAW_DIR"/*.md; do
  uni=$(basename "$f" .md)

  # skip combined file if needed
  if [[ "$uni" == "all_current_jobs" ]]; then
    continue
  fi

  echo "Processing $uni ..."

  python "$PY_SCRIPT" "$f" \
    -o "$OUT_DIR/${uni}.png" \
    --font "$FONT" \
    --max-height 1440 \
    --header-font 48

done

echo "All done."
