#!/usr/bin/env python3
"""
T20d Fine-Scan Runner — L=16 and L=24 with high statistics
Monitors progress and reports every 15 minutes.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BINARY = REPO_ROOT / "rust-lattice" / "target" / "release" / "z2-lattice-gauge"
OUTPUT_DIR = REPO_ROOT / "numerics" / "data" / "fss"
LOG_DIR = REPO_ROOT / "numerics" / "data" / "fss"

# Fine-scan configs matching L=32 quality
CONFIGS = [
    {
        "L": 16,
        "beta_min": 0.74, "beta_max": 0.78, "delta_beta": 0.002,
        "thermal": 500_000, "sweeps": 1_000_000, "workers": 8,
    },
    {
        "L": 24,
        "beta_min": 0.74, "beta_max": 0.78, "delta_beta": 0.002,
        "thermal": 500_000, "sweeps": 1_000_000, "workers": 8,
    },
]

LOOP_SIZES = "1x1,2x2,3x3"


def build_beta_grid(beta_min, beta_max, delta_beta):
    values = []
    beta = beta_min
    while beta <= beta_max + 1e-9:
        values.append(round(beta, 6))
        beta += delta_beta
    return values


def run_simulation_batch(l, betas, thermal, sweeps, workers, checkpoint_path=None):
    cmd = [str(BINARY), "--polyakov"]
    if checkpoint_path:
        cmd.extend(["--checkpoint", str(checkpoint_path)])
    cmd.extend([str(l), "3", str(sweeps), str(thermal), str(workers), LOOP_SIZES])
    cmd.extend([str(b) for b in betas])
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode != 0:
        print(f"  ERROR: Rust binary failed for L={l}")
        print(f"  stderr: {result.stderr[:500]}")
        return None, elapsed
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed: {e}")
        print(f"  stdout: {result.stdout[:500]}")
        return None, elapsed
    
    return data, elapsed


def log_progress(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_DIR / ".monitor-t20d-fine-20260629.log", "a") as f:
        f.write(line + "\n")


def run_fine_scan(L, beta_min, beta_max, delta_beta, thermal, sweeps, workers):
    betas = build_beta_grid(beta_min, beta_max, delta_beta)
    date_str = "20260629"
    outfile = OUTPUT_DIR / f"t20-p3b-L{L}-fine-{date_str}.json"
    checkpoint = OUTPUT_DIR / f".checkpoint-L{L}-{date_str}.json"
    
    log_progress(f"[L={L}] Starting fine scan: {len(betas)} β values")
    log_progress(f"[L={L}] β ∈ [{beta_min:.3f}, {beta_max:.3f}], Δβ={delta_beta}")
    log_progress(f"[L={L}] thermal={thermal:,}, sweeps={sweeps:,}, workers={workers}")
    
    data, elapsed = run_simulation_batch(L, betas, thermal, sweeps, workers, checkpoint_path=str(checkpoint))
    
    if data is None:
        log_progress(f"[L={L}] ✗ FAILED after {elapsed:.1f}s")
        return False
    
    results = data.get("results", [])
    log_progress(f"[L={L}] ✓ Got {len(results)} results in {elapsed:.1f}s")
    
    save_data = {
        "parameters": {
            "L": L, "dimension": 3,
            "thermalSweeps": thermal,
            "measureSweeps": sweeps,
            "measureEvery": 10,
            "workers": workers,
            "betaValues": betas,
            "loopSizes": LOOP_SIZES,
            "polyakov": True,
        },
        "results": results,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
            "completed": len(results),
            "total": len(betas),
            "wallTimeMs": int(elapsed * 1000),
        }
    }
    
    tmp = outfile.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(save_data, f, indent=2)
    tmp.rename(outfile)
    
    log_progress(f"[L={L}] → Saved: {outfile.name}")
    
    # Summary
    if results:
        chi_max = max(results, key=lambda r: r.get('susceptibility', 0))
        c_max = max(results, key=lambda r: r.get('specificHeat', 0))
        log_progress(f"[L={L}] Peak χ = {chi_max['susceptibility']:.4f} at β={chi_max['beta']}")
        log_progress(f"[L={L}] Peak C = {c_max['specificHeat']:.4f} at β={c_max['beta']}")
    
    return True


def main():
    if not BINARY.exists():
        log_progress(f"ERROR: Binary not found at {BINARY}")
        sys.exit(1)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    log_progress("=" * 60)
    log_progress("T20d Fine Scan — L=16, L=24 (High Statistics)")
    log_progress("=" * 60)
    
    for cfg in CONFIGS:
        success = run_fine_scan(
            cfg["L"], cfg["beta_min"], cfg["beta_max"], cfg["delta_beta"],
            cfg["thermal"], cfg["sweeps"], cfg["workers"]
        )
        if not success:
            log_progress(f"[L={cfg['L']}] Failed, continuing...")
    
    log_progress("=" * 60)
    log_progress("ALL DONE")
    log_progress("=" * 60)


if __name__ == "__main__":
    main()
