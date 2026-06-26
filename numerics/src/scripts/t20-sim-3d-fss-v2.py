#!/usr/bin/env python3
"""
T20 Phase 3b — 3D Z₂ LGT Finite-Size Scaling with Fine β Grid (V2 - Batched)

FIX: Passes ALL beta values to Rust in a single call, allowing rayon to
parallelize across all beta points. Achieves ~8× speedup on 8-core systems.

Usage:
  python3 t20-sim-3d-fss-v2.py [--test] [--L 8] [--resume]

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

REPO_ROOT = Path(__file__).resolve().parents[3]
BINARY = REPO_ROOT / "rust-lattice" / "target" / "release" / "z2-lattice-gauge"
OUTPUT_DIR = REPO_ROOT / "numerics" / "data" / "fss"

SIM_CONFIGS = [
    {"L": 8,  "beta_min": 0.70, "beta_max": 0.82, "delta_beta": 0.005,
     "thermal": 500_000, "sweeps": 1_000_000, "workers": 8},
    {"L": 16, "beta_min": 0.72, "beta_max": 0.80, "delta_beta": 0.003,
     "thermal": 500_000, "sweeps": 1_000_000, "workers": 8},
    {"L": 32, "beta_min": 0.74, "beta_max": 0.78, "delta_beta": 0.002,
     "thermal": 500_000, "sweeps": 1_500_000, "workers": 8},
    {"L": 48, "beta_min": 0.75, "beta_max": 0.77, "delta_beta": 0.0015,
     "thermal": 1_000_000, "sweeps": 2_000_000, "workers": 8},
    {"L": 64, "beta_min": 0.75, "beta_max": 0.77, "delta_beta": 0.001,
     "thermal": 1_000_000, "sweeps": 3_000_000, "workers": 8},
]

TEST_CONFIG = {"L": 8, "beta": 0.76, "thermal": 5_000, "sweeps": 10_000, "workers": 8}
LOOP_SIZES = "1x1,2x2,3x3"

# ─── UTILITIES ───────────────────────────────────────────────────────────────

def build_beta_grid(beta_min, beta_max, delta_beta):
    values = []
    beta = beta_min
    while beta <= beta_max + 1e-9:
        values.append(round(beta, 6))
        beta += delta_beta
    return values


def run_simulation_batch(l, betas, thermal, sweeps, workers, checkpoint_path=None, polyakov=True):
    """Run Rust binary with ALL beta values in a single call.
    
    This allows rayon to parallelize across beta points, achieving
    near-linear speedup with core count.
    """
    cmd = [
        str(BINARY),
        "--polyakov" if polyakov else "",
    ]
    
    # Add checkpoint if path provided
    if checkpoint_path:
        cmd.extend(["--checkpoint", str(checkpoint_path)])
    
    cmd.extend([
        str(l), "3", str(sweeps), str(thermal), str(workers),
        LOOP_SIZES,
    ])
    cmd.extend([str(b) for b in betas])
    cmd = [c for c in cmd if c != ""]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  ERROR: Rust binary failed for L={l}")
        print(f"  stderr: {result.stderr}")
        return None, elapsed

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed for L={l}: {e}")
        print(f"  stdout: {result.stdout[:500]}")
        return None, elapsed

    return data, elapsed


def load_existing_results(filepath):
    if not filepath.exists():
        return None
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  Warning: Could not load {filepath}: {e}")
        return None


def save_results(filepath, data):
    tmp = filepath.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(data, f, indent=2)
    tmp.rename(filepath)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def run_test():
    print("═" * 70)
    print("T20 Phase 3b — TEST RUN (V2 Batched)")
    print("═" * 70)

    cfg = TEST_CONFIG
    l = cfg["L"]
    beta = cfg["beta"]
    thermal = cfg["thermal"]
    sweeps = cfg["sweeps"]
    workers = cfg["workers"]

    print(f"Test: L={l}, β={beta}, thermal={thermal:,}, sweeps={sweeps:,}, workers={workers}")
    print(f"Calling Rust with 1 beta value...")

    data, elapsed = run_simulation_batch(l, [beta], thermal, sweeps, workers)

    if data is None or "results" not in data or not data["results"]:
        print("✗ TEST FAILED")
        return False

    res = data["results"][0]
    print(f"\n  meanPlaquette    = {res['meanPlaquette']:.6f} ± {res.get('errorPlaquette', 0):.6f}")
    print(f"  susceptibility   = {res['susceptibility']:.4f}")
    print(f"  specificHeat     = {res['specificHeat']:.4f}")
    print(f"  binderCumulant   = {res['binderCumulant']:.4f}")
    if "meanPolyakov" in res:
        print(f"  meanPolyakov     = {res['meanPolyakov']:.6f} ± {res.get('errorPolyakov', 0):.6f}")
    print(f"  wallTime         = {elapsed:.2f}s")
    print(f"  numMeasurements  = {res['numMeasurements']}")
    print("\n✓ TEST PASSED")
    return True


def run_full(resume=False, only_L=None):
    print("═" * 70)
    print("T20 Phase 3b — 3D Z₂ LGT FSS (V2 Batched, Parallel Beta)")
    print("═" * 70)
    print(f"Binary: {BINARY}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Date:   {datetime.now(timezone.utc).astimezone().isoformat()}")
    print("")

    configs = [c for c in SIM_CONFIGS if only_L is None or c["L"] == only_L]

    for cfg in configs:
        L = cfg["L"]
        betas = build_beta_grid(cfg["beta_min"], cfg["beta_max"], cfg["delta_beta"])
        
        date_str = datetime.now().strftime("%Y%m%d")
        outfile = OUTPUT_DIR / f"t20-p3b-L{L}-3D-fine-{date_str}.json"

        # Check for existing data
        existing = None
        if resume and outfile.exists():
            existing = load_existing_results(outfile)

        if existing and "results" in existing and len(existing["results"]) == len(betas):
            print(f"[L={L}] Already complete: {len(betas)}/{len(betas)} β values. Skipping.")
            continue

        # Filter out already-completed betas
        if existing and "results" in existing:
            completed_betas = {r["beta"] for r in existing["results"]}
            remaining_betas = [b for b in betas if b not in completed_betas]
            all_results = existing["results"]
            print(f"[L={L}] Resuming: {len(completed_betas)}/{len(betas)} done, {len(remaining_betas)} remaining.")
        else:
            remaining_betas = betas
            all_results = []
            print(f"[L={L}] Starting: {len(betas)} β values, {cfg['sweeps']:,} sweeps each")

        if not remaining_betas:
            continue

        print(f"  β range: [{cfg['beta_min']:.3f}, {cfg['beta_max']:.3f}], Δβ={cfg['delta_beta']}")
        print(f"  thermal={cfg['thermal']:,}, sweeps={cfg['sweeps']:,}, workers={cfg['workers']}")
        print(f"  Batch call: passing {len(remaining_betas)} β values to Rust...")

        # Build checkpoint path for Rust-level checkpointing
        checkpoint_path = OUTPUT_DIR / f".checkpoint-L{L}-{date_str}.json"

        # ─── KEY FIX: Pass ALL remaining betas in ONE call ───
        data, elapsed = run_simulation_batch(
            L, remaining_betas, cfg["thermal"], cfg["sweeps"], cfg["workers"],
            checkpoint_path=str(checkpoint_path)
        )

        if data is None:
            print(f"  ✗ Batch failed for L={L}")
            continue

        # Merge results
        if "results" in data:
            for res in data["results"]:
                all_results.append(res)
        
        print(f"  ✓ Got {len(data.get('results', []))} results in {elapsed:.1f}s")
        print(f"  → Total: {len(all_results)}/{len(betas)} β values complete")

        # Save
        save_data = {
            "parameters": {
                "L": L, "dimension": 3,
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
        print(f"  → Saved: {outfile.name}")
        print("")

    print("═" * 70)
    print("ALL DONE")
    print("═" * 70)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--L", type=int, default=None)
    args = parser.parse_args()

    if not BINARY.exists():
        print(f"ERROR: Binary not found at {BINARY}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.test:
        success = run_test()
        sys.exit(0 if success else 1)
    else:
        success = run_full(resume=args.resume, only_L=args.L)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
