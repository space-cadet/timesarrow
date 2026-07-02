#!/bin/bash
# Run signed volume simulation for a given L
# Usage: ./run-signed-volume.sh <L> <thermal> <measure> <workers>

set -e

L=${1:-8}
THERMAL=${2:-5000}
MEASURE=${3:-20000}
WORKERS=${4:-4}

BETA_RANGE="0.4 0.5 0.6 0.7 0.76 0.8 0.85 0.9 1.0 1.1 1.2 1.5"
LOOP_SIZES="1x1,2x2,4x4"

OUTPUT_DIR="$HOME/.openclaw/workspace/code/timesarrow/numerics/data/signed-volume"
mkdir -p "$OUTPUT_DIR"

CHECKPOINT="$OUTPUT_DIR/sv-L${L}.json"
OUTPUT="$OUTPUT_DIR/sv-L${L}-$(date +%Y%m%d-%H%M%S).json"

BINARY="$HOME/.openclaw/workspace/code/timesarrow/rust-lattice/target/release/z2-lattice-gauge"

echo "=== Signed Volume Run ==="
echo "L=$L, thermal=$THERMAL, measure=$MEASURE, workers=$WORKERS"
echo "Beta range: $BETA_RANGE"
echo "Checkpoint: $CHECKPOINT"
echo "Output: $OUTPUT"
echo ""

# Run with checkpointing and redirect output
$BINARY --signed-volume --checkpoint "$CHECKPOINT" \
    "$L" 3 "$MEASURE" "$THERMAL" "$WORKERS" "$LOOP_SIZES" $BETA_RANGE \
    > "$OUTPUT" 2>"$OUTPUT_DIR/sv-L${L}.log"

echo "=== Run complete ==="
echo "Output saved to: $OUTPUT"
echo "Log saved to: $OUTPUT_DIR/sv-L${L}.log"
