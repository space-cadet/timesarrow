#!/usr/bin/env bash
set -euo pipefail

# TimesArrow Reproducible Build Validation Script
# Runs: TypeScript build check → Rust build check → Rust unit tests
# Exits with non-zero status if any step fails.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== TimesArrow Build Validation ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# --- TypeScript build check ---
echo "[1/3] TypeScript build check (numerics/)"
cd "$PROJECT_ROOT/numerics"

NODE_BIN="$(command -v node || true)"
if [ -z "$NODE_BIN" ]; then
    for candidate in /opt/homebrew/bin/node /usr/local/bin/node; do
        if [ -x "$candidate" ]; then
            NODE_BIN="$candidate"
            export PATH="$(dirname "$candidate"):$PATH"
            break
        fi
    done
fi

if [ -z "$NODE_BIN" ]; then
    echo "ERROR: Node.js not found in PATH or common local install locations"
    exit 1
fi

TS_QUANTUM_DIR="${TS_QUANTUM_DIR:-}"
if [ -z "$TS_QUANTUM_DIR" ]; then
    for candidate in "$PROJECT_ROOT/../ts-quantum" /Users/deepak/code/ts-quantum; do
        if [ -d "$candidate" ]; then
            TS_QUANTUM_DIR="$candidate"
            break
        fi
    done
fi

# Check dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "  Installing dependencies (npm ci)..."
    npm ci
fi

if [ -n "$TS_QUANTUM_DIR" ]; then
    if [ ! -e "node_modules/ts-quantum" ] || [ ! -e "$(python3 - <<'PY'
from pathlib import Path
p = Path('node_modules/ts-quantum')
try:
    print(p.resolve(strict=True))
except Exception:
    print('')
PY
)" ]; then
        echo "  Repairing ts-quantum link -> $TS_QUANTUM_DIR"
        ln -sfn "$TS_QUANTUM_DIR" node_modules/ts-quantum
    fi
fi

echo "  Running tsc --strict --noEmit..."
npx tsc --strict --noEmit
if [ $? -ne 0 ]; then
    echo "ERROR: TypeScript build failed"
    exit 1
fi
echo "  ✓ TypeScript build passed"
echo ""

# --- Rust build check ---
echo "[2/3] Rust build check (rust-lattice/)"
cd "$PROJECT_ROOT/rust-lattice"

if ! command -v cargo >/dev/null 2>&1 && ! command -v rustup >/dev/null 2>&1; then
    echo "ERROR: Rust/Cargo not found in PATH"
    exit 1
fi

RUST_TOOLCHAIN="1.92.0-aarch64-apple-darwin"
if command -v rustup >/dev/null 2>&1 && rustup toolchain list | grep -q "^$RUST_TOOLCHAIN"; then
    CARGO_CMD=(rustup run "$RUST_TOOLCHAIN" cargo)
    echo "  Using rustup toolchain: $RUST_TOOLCHAIN"
else
    CARGO_CMD=(cargo)
    echo "  Using default cargo from PATH"
fi

echo "  Running cargo check..."
"${CARGO_CMD[@]}" check
if [ $? -ne 0 ]; then
    echo "ERROR: Rust build check failed"
    exit 1
fi
echo "  ✓ Rust build check passed"
echo ""

# --- Rust unit tests ---
echo "[3/3] Rust unit tests (rust-lattice/)"
cd "$PROJECT_ROOT/rust-lattice"

echo "  Running cargo test..."
"${CARGO_CMD[@]}" test
if [ $? -ne 0 ]; then
    echo "ERROR: Rust tests failed"
    exit 1
fi
echo "  ✓ Rust tests passed"
echo ""

echo "=== All validation checks passed ==="
