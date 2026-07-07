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

if ! command -v node >/dev/null 2>&1; then
    echo "ERROR: Node.js not found in PATH"
    exit 1
fi

# Check dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "  Installing dependencies (npm ci)..."
    npm ci
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

if ! command -v cargo >/dev/null 2>&1; then
    echo "ERROR: Rust/Cargo not found in PATH"
    exit 1
fi

echo "  Running cargo check..."
cargo check
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
cargo test
if [ $? -ne 0 ]; then
    echo "ERROR: Rust tests failed"
    exit 1
fi
echo "  ✓ Rust tests passed"
echo ""

echo "=== All validation checks passed ==="
