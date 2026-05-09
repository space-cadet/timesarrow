#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PILOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$PILOT_DIR/build"

"$SCRIPT_DIR/render-z2-pilot.sh"

mkdir -p "$BUILD_DIR"

(
  cd "$PILOT_DIR"

  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$BUILD_DIR" z2-pilot.tex
  biber --input-directory "$BUILD_DIR" --output-directory "$BUILD_DIR" z2-pilot
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$BUILD_DIR" z2-pilot.tex
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$BUILD_DIR" z2-pilot.tex
)
