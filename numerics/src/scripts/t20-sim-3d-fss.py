#!/usr/bin/env python3
"""
T20 Phase 3b — 3D Z₂ LGT Finite-Size Scaling with Fine β Grid

Re-run 3D Z₂ LGT Monte Carlo simulations with:
  - Fine β grid near β_c (Δβ = 0.001–0.005)
  - Larger lattice sizes (L = 8, 16, 32, 48, 64)
  - More sweeps (1M–3M per β)
  - Polyakov loop observable (deconfinement order parameter)

Observables measured:
  - Plaquette ⟨P⟩
  - Polyakov loop magnitude ⟨|P|⟩
  - Polyakov loop susceptibility χ_P = L³(⟨P²⟩ - ⟨P⟩²)
  - Energy E (via plaquette)
  - Specific heat C = L³(⟨E²⟩ - ⟨E⟩²)
  - Binder cumulant U_P = 1 - ⟨P⁴⟩/(3⟨P²⟩²) for Polyakov loop

Usage:
  python3 t20-sim-3d-fss.py [--test] [--L 8] [--resume]

Output:
  numerics/data/fss/t20-p3b-L{L}-3D-fine-YYYYMMDD.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ─── CONFIGURATION ───────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[3]  # numerics/src/scripts -> repo root
BINARY = REPO_ROOT / "rust-lattice" / "target" / "release" / "z2-lattice-gauge"
OUTPUT_DIR = REPO_ROOT / "numerics" / "data" / "fss"

# Simulation parameters per lattice size
# Format: (L, beta_min, beta_max, delta_beta, thermal_sweeps, measure_sweeps, workers)
SIM_CONFIGS = [
    # L=8:  β ∈ [0.70, 0.82], Δβ = 0.005,  thermal = 500k, sweeps = 1M
    {"L": 8,  "beta_min": 0.70, "beta_max": 0.82, "delta_beta": 0.005,
     "thermal": 500_000, "sweeps": 1_000_000, "workers": 8},

    # L=16: β ∈ [0.72, 0.80], Δβ = 0.003,  thermal = 500k, sweeps = 1M
    {"L": 16, "beta_min": 0.72, "beta_max": 0.80, "delta_beta": 0.003,
     "thermal": 500_000, "sweeps": 1_000_000, "workers": 8},

    # L=32: β ∈ [0.74, 0.78], Δβ = 0.002,  thermal = 500k, sweeps = 1.5M
    {"L": 32, "beta_min": 0.74, "beta_max": 0.78, "delta_beta": 0.002,
     "thermal": 500_000, "sweeps": 1_500_000, "workers": 8},

    # L=48: β ∈ [0.75, 0.77], Δβ = 0.0015, thermal = 1M,   sweeps = 2M
    # ⚠️  Memory: L³ = 110,592 sites, links = 331,776
    {"L": 48, "beta_min": 0.75, "beta_max": 0.77, "delta_beta": 0.0015,
     "thermal": 1_000_000, "sweeps": 2_000_000, "workers": 6},

    # L=64: β ∈ [0.75, 0.77], Δβ = 0.001,  thermal = 1M,   sweeps = 3M
    # ⚠️  Memory: L³ = 262,144 sites, links = 786,432
    {"L": 64, "beta_min": 0.75, "beta_max": 0.77, "delta_beta": 0.001,
     "thermal": 1_000_000, "sweeps": 3_000_000, "workers": 4},
]

# For test mode: just one β value
TEST_CONFIG = {"L": 8, "beta": 0.76, "thermal": 5_000, "sweeps": 10_000, "workers": 4}

LOOP_SIZES = "1x1,2x2,3x3"

# ─── UTILITIES ───────────────────────────────────────────────────────────────

def build_beta_grid(beta_min, beta_max, delta_beta):
    """Generate sorted list of beta values."""
    values = []
    beta = beta_min
    while beta <= beta_max + 1e-9:
        values.append(round(beta, 6))
        beta += delta_beta
    return values


def run_simulation(l, beta, thermal, sweeps, workers, polyakov=True):
    """Run the Rust binary for a single (L, β) point. Returns parsed JSON."""
    cmd = [
        str(BINARY),
        "--polyakov" if polyakov else "",
        str(l), "3", str(sweeps), str(thermal), str(workers),
        LOOP_SIZES,
        str(beta),
    ]
    # Remove empty string if polyakov is False
    cmd = [c for c in cmd if c != ""]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  ERROR: Rust binary failed for L={l} β={beta}")
        print(f"  stderr: {result.stderr}")
        return None, elapsed

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed for L={l} β={beta}: {e}")
        print(f"  stdout: {result.stdout[:500]}")
        return None, elapsed

    return data, elapsed


def load_existing_results(filepath):
    """Load existing results file if present, for resuming."""
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_results(filepath, data):
    """Save results atomically."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    tmp = filepath.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    tmp.replace(filepath)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def run_test():
    """Quick test run for L=8, β=0.76."""
    print("═" * 60)
    print("T20 Phase 3b — TEST RUN")
    print("═" * 60)

    cfg = TEST_CONFIG
    print(f"\nTest: L={cfg['L']}, β={cfg['beta']}, "
          f"thermal={cfg['thermal']:,}, sweeps={cfg['sweeps']:,}, workers={cfg['workers']}")
    print("─" * 60)

    data, elapsed = run_simulation(
        cfg["L"], cfg["beta"], cfg["thermal"], cfg["sweeps"], cfg["workers"]
    )

    if data is None:
        print("TEST FAILED")
        sys.exit(1)

    res = data["results"][0]
    print(f"  meanPlaquette    = {res['meanPlaquette']:.6f} ± {res['errorPlaquette']:.6f}")
    print(f"  susceptibility   = {res['susceptibility']:.4f}")
    print(f"  specificHeat     = {res['specificHeat']:.4f}")
    print(f"  binderCumulant   = {res['binderCumulant']:.4f}")
    if "meanPolyakov" in res:
        print(f"  meanPolyakov     = {res['meanPolyakov']:.6f} ± {res.get('errorPolyakov', 0):.6f}")
        print(f"  polyakovSuscept  = {res.get('polyakovSusceptibility', 0):.4f}")
        print(f"  polyakovBinder   = {res.get('polyakovBinder', 0):.4f}")
    print(f"  wallTime         = {elapsed:.2f}s")
    print(f"  numMeasurements  = {res['numMeasurements']}")
    print("\n✓ TEST PASSED")
    return True


def run_full(resume=False):
    """Run the full fine-grid finite-size scaling simulation."""
    print("═" * 70)
    print("T20 Phase 3b — 3D Z₂ LGT Finite-Size Scaling (Fine β Grid)")
    print("═" * 70)
    print(f"Binary: {BINARY}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Date:   {datetime.now(timezone.utc).astimezone().isoformat()}")
    print("")

    # Warn about large lattices
    for cfg in SIM_CONFIGS:
        if cfg["L"] >= 48:
            sites = cfg["L"] ** 3
            links = 3 * sites
            print(f"⚠️  WARNING: L={cfg['L']} requires {links:,} links ({sites:,} sites). "
                  f"Ensure sufficient RAM (~{links * 8 / 1024 / 1024:.0f} MB for field + working memory).")
    print("")

    total_start = time.time()
    total_simulations = 0
    completed_simulations = 0

    for cfg in SIM_CONFIGS:
        L = cfg["L"]
        betas = build_beta_grid(cfg["beta_min"], cfg["beta_max"], cfg["delta_beta"])
        total_simulations += len(betas)

        date_str = datetime.now().strftime("%Y%m%d")
        outfile = OUTPUT_DIR / f"t20-p3b-L{L}-3D-fine-{date_str}.json"

        # Load existing results for resume
        existing = load_existing_results(outfile) if resume else None
        completed_betas = set()
        all_results = []

        if existing and "results" in existing:
            all_results = existing["results"]
            completed_betas = {r["beta"] for r in all_results}
            print(f"[L={L}] Resuming: {len(completed_betas)}/{len(betas)} β values already done.")
        else:
            print(f"[L={L}] Starting fresh: {len(betas)} β values to simulate.")

        print(f"  β grid: [{cfg['beta_min']:.3f}, {cfg['beta_max']:.3f}] "
              f"Δβ={cfg['delta_beta']}, {len(betas)} points")
        print(f"  thermal={cfg['thermal']:,}, sweeps={cfg['sweeps']:,}, workers={cfg['workers']}")

        for beta in betas:
            if round(beta, 6) in completed_betas or beta in completed_betas:
                print(f"  β={beta:.4f} — skipped (already done)")
                completed_simulations += 1
                continue

            print(f"  β={beta:.4f} ... ", end="", flush=True)
            data, elapsed = run_simulation(
                L, beta, cfg["thermal"], cfg["sweeps"], cfg["workers"]
            )

            if data is None:
                print("FAILED")
                continue

            res = data["results"][0]
            print(f"⟨P⟩={res['meanPlaquette']:.4f} "
                  f"χ={res['susceptibility']:.2f} "
                  f"U={res['binderCumulant']:.3f} "
                  f"⟨|P|⟩={res.get('meanPolyakov', 0):.4f} "
                  f"({elapsed:.1f}s)")

            all_results.append(res)
            completed_simulations += 1

            # Save after each β to allow resuming
            save_data = {
                "parameters": {
                    "L": L,
                    "dimension": 3,
                    "thermalSweeps": cfg["thermal"],
                    "measureSweeps": cfg["sweeps"],
                    "measureEvery": 10,
                    "workers": cfg["workers"],
                    "betaValues": betas,
                    "loopSizes": LOOP_SIZES,
                    "polyakov": True,
                },
                "results": all_results,
                "metadata": {
                    "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
                    "completed": len(all_results),
                    "total": len(betas),
                }
            }
            save_results(outfile, save_data)

        print(f"  → Saved: {outfile.name} ({len(all_results)}/{len(betas)} β values)")
        print("")

    total_elapsed = time.time() - total_start
    print("═" * 70)
    print(f"COMPLETED {completed_simulations}/{total_simulations} simulations "
          f"in {total_elapsed/60:.1f} minutes")
    print("═" * 70)

    # Print compute time estimate for remaining runs
    remaining = total_simulations - completed_simulations
    if remaining > 0:
        avg_time = total_elapsed / max(completed_simulations, 1)
        est_remaining = avg_time * remaining
        print(f"\nEstimated remaining time: {est_remaining/3600:.1f} hours")
        print(f"(based on {avg_time:.1f}s average per β point)")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="T20 Phase 3b — 3D Z₂ LGT Fine-Grid FSS Simulations"
    )
    parser.add_argument("--test", action="store_true",
                        help="Run a quick test (L=8, β=0.76, 10k sweeps)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from existing output files")
    parser.add_argument("--L", type=int, default=None,
                        help="Run only for a specific lattice size")
    args = parser.parse_args()

    # Ensure binary exists
    if not BINARY.exists():
        print(f"ERROR: Binary not found at {BINARY}")
        print("Run: cd rust-lattice && cargo build --release")
        sys.exit(1)

    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.test:
        run_test()
    else:
        run_full(resume=args.resume)


if __name__ == "__main__":
    main()
