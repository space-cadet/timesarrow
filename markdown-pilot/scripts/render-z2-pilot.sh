#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PILOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
NORMALIZER="$SCRIPT_DIR/normalize_inline_math.py"

mkdir -p "$PILOT_DIR/generated"

TMP_SOURCE="$(mktemp)"
trap 'rm -f "$TMP_SOURCE"' EXIT

python3 "$NORMALIZER" "$PILOT_DIR/z2-action.md" > "$TMP_SOURCE"

pandoc \
  "$TMP_SOURCE" \
  --from 'markdown+raw_tex+tex_math_dollars-smart' \
  --to latex \
  --wrap=preserve \
  --output "$PILOT_DIR/generated/z2-action.tex"
