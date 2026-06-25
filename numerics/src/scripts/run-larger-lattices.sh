#!/bin/bash
# Benchmark and run larger lattices for 3D Z2 LGT finite-size scaling
# L=16, 24, 32 with fine-grained beta grid (21 values)

set -e

BETA_GRID="0.3 0.4 0.5 0.55 0.6 0.65 0.68 0.7 0.72 0.74 0.76 0.78 0.8 0.82 0.84 0.86 0.9 0.95 1 1.1 1.2"
LOOP_SIZES="1x1,2x2,3x3"
OUTPUT_DIR="/Users/sage/.openclaw/workspace/code/timesarrow/numerics/output"
BINARY="/Users/sage/.openclaw/workspace/code/timesarrow/rust-lattice/target/release/z2-lattice-gauge"

# Benchmark log file
BENCHMARK_LOG="$OUTPUT_DIR/benchmark-lattice-sizes-20250626.json"

# Start JSON array
{
echo "{"
echo '  "date": "2026-06-26T03:18:00+05:30",'
echo '  "runs": ['

FIRST=1
for L in 16 24 32; do
    if [ "$FIRST" -eq 0 ]; then
        echo "    ,"
    fi
    FIRST=0
    
    OUTFILE="$OUTPUT_DIR/t20-p3-L${L}-3D-wilson-fine-20250626.json"
    
    echo "Running L=$L..." >&2
    START=$(date +%s)
    
    $BINARY $L 3 100000 10000 8 "$LOOP_SIZES" $BETA_GRID > "$OUTFILE" 2>&1
    
    END=$(date +%s)
    ELAPSED=$((END - START))
    
    # Extract per-beta timing from output (number of beta values)
    NUM_BETAS=$(echo $BETA_GRID | wc -w | tr -d ' ')
    AVG_TIME=$(echo "scale=2; $ELAPSED / $NUM_BETAS" | bc)
    
    echo "    {"
    echo "      \"L\": $L,"
    echo "      \"dimension\": 3,"
    echo "      \"measureSweeps\": 100000,"
    echo "      \"thermalSweeps\": 10000,"
    echo "      \"workers\": 8,"
    echo "      \"numBetas\": $NUM_BETAS,"
    echo "      \"totalTimeSeconds\": $ELAPSED,"
    echo "      \"avgTimePerBetaSeconds\": $AVG_TIME,"
    echo "      \"outputFile\": \"$(basename $OUTFILE)\""
    echo "    }"
    
    echo "  L=$L completed in ${ELAPSED}s (avg ${AVG_TIME}s per β)" >&2
done

echo "  ]"
echo "}"

} > "$BENCHMARK_LOG" 2>&1

echo "Benchmark saved to $BENCHMARK_LOG"