#!/usr/bin/env python3
"""
T20 Multi-Run Orchestrator: Run 3-5 independent simulations per (L, β) configuration
with different random seeds, for variance estimation.

Blocker 5 for T20-Phase3b.

Usage:
    python t20-multi-run.py --L 8 --beta 0.76 --n-runs 3 --base-seed 12345
    python t20-multi-run.py --L 8 --beta 0.76 --n-runs 5 --parallel --dry-run
    python t20-multi-run.py --L 8 --betas 0.70 0.72 0.74 0.76 0.78 --n-runs 3 --parallel
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
import numpy as np


# Binary path (relative to repo root)
DEFAULT_BINARY = Path(__file__).parent.parent.parent.parent / "rust-lattice" / "target" / "release" / "z2-lattice-gauge"
DEFAULT_DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "fss" / "multi"


def run_single_simulation(
    L: int,
    beta: float,
    seed: int,
    run_idx: int,
    measure_sweeps: int = 100000,
    thermal_sweeps: int = 10000,
    workers: int = 4,
    loop_sizes: str = "1x1,2x2,3x3",
    binary: Path = DEFAULT_BINARY,
    data_dir: Path = DEFAULT_DATA_DIR,
    dimension: int = 3,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Run a single simulation at (L, β) with given seed."""

    out_dir = data_dir / f"L{L}" / f"beta_{beta:.4f}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"run_{run_idx}.json"

    cmd = [
        str(binary),
        str(L),
        str(dimension),
        str(measure_sweeps),
        str(thermal_sweeps),
        str(workers),
        loop_sizes,
        str(beta),
        "--seed",
        str(seed),
    ]

    result = {
        "run_idx": run_idx,
        "L": L,
        "beta": beta,
        "seed": seed,
        "command": " ".join(cmd),
        "output_file": str(out_file),
        "success": False,
        "wall_time_ms": None,
    }

    if dry_run:
        print(f"[DRY-RUN] {' '.join(cmd)}")
        result["success"] = True
        return result

    print(f"[RUN {run_idx}] L={L}, β={beta}, seed={seed}")
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        elapsed_ms = int((time.time() - start) * 1000)

        # Parse and save JSON output
        data = json.loads(proc.stdout)
        with open(out_file, "w") as f:
            json.dump(data, f, indent=2)

        result["success"] = True
        result["wall_time_ms"] = elapsed_ms
        result["data"] = data
        print(f"[RUN {run_idx}] ✓ Completed in {elapsed_ms}ms → {out_file}")

    except subprocess.CalledProcessError as e:
        elapsed_ms = int((time.time() - start) * 1000)
        result["wall_time_ms"] = elapsed_ms
        result["stderr"] = e.stderr
        print(f"[RUN {run_idx}] ✗ Failed in {elapsed_ms}ms")
        print(f"  stderr: {e.stderr[:500]}")

    except json.JSONDecodeError as e:
        elapsed_ms = int((time.time() - start) * 1000)
        result["wall_time_ms"] = elapsed_ms
        result["stderr"] = f"JSON parse error: {e}"
        print(f"[RUN {run_idx}] ✗ JSON parse error: {e}")

    return result


def compute_jackknife_error(values: np.ndarray) -> float:
    """Compute jackknife standard error for a set of values."""
    n = len(values)
    if n < 2:
        return np.nan

    # Leave-one-out means
    jack_means = np.zeros(n)
    for i in range(n):
        jack_means[i] = np.mean(np.delete(values, i))

    overall_mean = np.mean(values)
    # Jackknife variance estimate
    jack_var = (n - 1) / n * np.sum((jack_means - overall_mean) ** 2)
    return np.sqrt(jack_var)


def compute_cross_run_statistics(results: List[Dict[str, Any]], betas: List[float]) -> Dict[str, Any]:
    """Compute mean, standard error, variance, and jackknife estimates across independent runs."""

    stats = {
        "n_runs": len(results),
        "L": results[0]["L"],
        "betas": betas,
        "observables": {},
        "peak_analysis": None,
    }

    # For single-β: compute stats for each observable across runs
    if len(betas) == 1:
        beta = betas[0]
        observables = {
            "meanPlaquette": [],
            "susceptibility": [],
            "specificHeat": [],
            "binderCumulant": [],
            "errorPlaquette": [],
        }

        for r in results:
            if not r.get("success") or "data" not in r:
                continue
            res_list = r["data"].get("results", [])
            if not res_list:
                continue
            # Single beta: take the first (and only) result
            res = res_list[0]
            for obs in observables:
                if obs in res:
                    observables[obs].append(res[obs])

        for obs, vals in observables.items():
            arr = np.array(vals)
            if len(arr) == 0:
                continue
            stats["observables"][obs] = {
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr, ddof=1)),
                "stderr": float(np.std(arr, ddof=1) / np.sqrt(len(arr))),
                "variance": float(np.var(arr, ddof=1)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "jackknife_error": float(compute_jackknife_error(arr)),
                "values": [float(v) for v in arr],
                "n": len(arr),
            }

    # For multi-β: also compute χ_max and β_c per run, then variance across runs
    if len(betas) > 1:
        chi_max_per_run = []
        beta_c_per_run = []
        binder_min_per_run = []

        for r in results:
            if not r.get("success") or "data" not in r:
                continue
            res_list = r["data"].get("results", [])
            if len(res_list) < 3:
                continue

            betas_run = [res["beta"] for res in res_list]
            chis = [res["susceptibility"] for res in res_list]
            binders = [res["binderCumulant"] for res in res_list]

            peak_idx = int(np.argmax(chis))
            chi_max_per_run.append(chis[peak_idx])
            beta_c_per_run.append(betas_run[peak_idx])

            min_idx = int(np.argmin(binders))
            binder_min_per_run.append(binders[min_idx])

        peak_stats = {}
        for name, vals in [
            ("chi_max", chi_max_per_run),
            ("beta_c", beta_c_per_run),
            ("binder_min", binder_min_per_run),
        ]:
            arr = np.array(vals)
            if len(arr) == 0:
                continue
            peak_stats[name] = {
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr, ddof=1)),
                "stderr": float(np.std(arr, ddof=1) / np.sqrt(len(arr))),
                "variance": float(np.var(arr, ddof=1)),
                "jackknife_error": float(compute_jackknife_error(arr)),
                "values": [float(v) for v in arr],
                "n": len(arr),
            }

        stats["peak_analysis"] = peak_stats

        # Also compute per-β observables
        for beta in betas:
            observables = {
                "meanPlaquette": [],
                "susceptibility": [],
                "specificHeat": [],
                "binderCumulant": [],
            }
            for r in results:
                if not r.get("success") or "data" not in r:
                    continue
                for res in r["data"].get("results", []):
                    if abs(res["beta"] - beta) < 1e-6:
                        for obs in observables:
                            if obs in res:
                                observables[obs].append(res[obs])
                        break

            beta_key = f"beta_{beta:.4f}"
            stats["observables"][beta_key] = {}
            for obs, vals in observables.items():
                arr = np.array(vals)
                if len(arr) == 0:
                    continue
                stats["observables"][beta_key][obs] = {
                    "mean": float(np.mean(arr)),
                    "stderr": float(np.std(arr, ddof=1) / np.sqrt(len(arr))),
                    "variance": float(np.var(arr, ddof=1)),
                    "jackknife_error": float(compute_jackknife_error(arr)),
                    "values": [float(v) for v in arr],
                    "n": len(arr),
                }

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Run multiple independent simulations per (L, β) configuration for variance estimation."
    )
    parser.add_argument("--L", type=int, required=True, help="Lattice size")
    parser.add_argument(
        "--beta", type=float, default=None, help="Single beta value"
    )
    parser.add_argument(
        "--betas",
        type=float,
        nargs="+",
        default=None,
        help="Multiple beta values (space-separated)",
    )
    parser.add_argument(
        "--n-runs", type=int, default=3, help="Number of independent runs (default: 3)"
    )
    parser.add_argument(
        "--base-seed", type=int, default=12345, help="Base random seed (default: 12345)"
    )
    parser.add_argument(
        "--measure-sweeps", type=int, default=100000, help="Measurement sweeps per run"
    )
    parser.add_argument(
        "--thermal-sweeps", type=int, default=10000, help="Thermalization sweeps per run"
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Parallel workers per simulation"
    )
    parser.add_argument(
        "--loop-sizes", type=str, default="1x1,2x2,3x3", help="Wilson loop sizes"
    )
    parser.add_argument(
        "--binary",
        type=str,
        default=None,
        help="Path to z2-lattice-gauge binary",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Output data directory",
    )
    parser.add_argument(
        "--dimension", type=int, default=3, help="Lattice dimension (default: 3)"
    )
    parser.add_argument(
        "--parallel", action="store_true", help="Run all simulations in parallel"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print commands without executing"
    )
    parser.add_argument(
        "--output-stats",
        type=str,
        default=None,
        help="Path to write cross-run statistics JSON",
    )

    args = parser.parse_args()

    # Determine beta list
    if args.beta is not None and args.betas is not None:
        print("Error: specify either --beta or --betas, not both", file=sys.stderr)
        sys.exit(1)
    if args.beta is None and args.betas is None:
        print("Error: specify either --beta or --betas", file=sys.stderr)
        sys.exit(1)

    betas = [args.beta] if args.beta is not None else args.betas
    L = args.L
    n_runs = args.n_runs
    base_seed = args.base_seed

    binary = Path(args.binary) if args.binary else DEFAULT_BINARY
    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR

    if not binary.exists():
        print(f"Error: binary not found at {binary}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("T20 Multi-Run Orchestrator")
    print("=" * 60)
    print(f"L = {L}, dimension = {args.dimension}")
    print(f"β values = {betas}")
    print(f"n_runs = {n_runs}, base_seed = {base_seed}")
    print(f"measure_sweeps = {args.measure_sweeps}, thermal_sweeps = {args.thermal_sweeps}")
    print(f"workers = {args.workers}, loop_sizes = {args.loop_sizes}")
    print(f"binary = {binary}")
    print(f"data_dir = {data_dir}")
    print(f"parallel = {args.parallel}, dry_run = {args.dry_run}")
    print("=" * 60)

    # Build task list: (run_idx, beta, seed)
    # Each independent simulation gets a unique seed
    tasks = []
    for run_idx in range(n_runs):
        for beta_idx, beta in enumerate(betas):
            seed = base_seed + run_idx * 1000 + beta_idx
            tasks.append((run_idx, beta, seed))

    print(f"Total tasks: {len(tasks)}")
    print()

    if args.dry_run:
        for run_idx, beta, seed in tasks:
            run_single_simulation(
                L=L,
                beta=beta,
                seed=seed,
                run_idx=run_idx,
                measure_sweeps=args.measure_sweeps,
                thermal_sweeps=args.thermal_sweeps,
                workers=args.workers,
                loop_sizes=args.loop_sizes,
                binary=binary,
                data_dir=data_dir,
                dimension=args.dimension,
                dry_run=True,
            )
        print("\n[Dry run complete — no simulations executed]")
        return

    # Execute runs
    all_results = []
    start_all = time.time()

    if args.parallel:
        # Use ThreadPoolExecutor for parallel execution
        # (subprocess calls are IO-bound from Python's perspective)
        max_workers = min(len(tasks), os.cpu_count() or 4)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for task in tasks:
                run_idx, beta, seed = task
                future = executor.submit(
                    run_single_simulation,
                    L=L,
                    beta=beta,
                    seed=seed,
                    run_idx=run_idx,
                    measure_sweeps=args.measure_sweeps,
                    thermal_sweeps=args.thermal_sweeps,
                    workers=args.workers,
                    loop_sizes=args.loop_sizes,
                    binary=binary,
                    data_dir=data_dir,
                    dimension=args.dimension,
                    dry_run=False,
                )
                futures.append(future)

            for future in as_completed(futures):
                all_results.append(future.result())
    else:
        for task in tasks:
            run_idx, beta, seed = task
            result = run_single_simulation(
                L=L,
                beta=beta,
                seed=seed,
                run_idx=run_idx,
                measure_sweeps=args.measure_sweeps,
                thermal_sweeps=args.thermal_sweeps,
                workers=args.workers,
                loop_sizes=args.loop_sizes,
                binary=binary,
                data_dir=data_dir,
                dimension=args.dimension,
                dry_run=False,
            )
            all_results.append(result)

    total_time = time.time() - start_all
    successful = sum(1 for r in all_results if r["success"])
    print()
    print("=" * 60)
    print(f"All runs complete: {successful}/{len(tasks)} successful in {total_time:.1f}s")
    print("=" * 60)

    # Compute cross-run statistics
    stats = compute_cross_run_statistics(all_results, betas)

    # Save statistics
    stats_dir = data_dir / f"L{L}"
    stats_dir.mkdir(parents=True, exist_ok=True)

    if args.output_stats:
        stats_file = Path(args.output_stats)
    else:
        beta_tag = f"{betas[0]:.4f}" if len(betas) == 1 else "multi"
        stats_file = stats_dir / f"stats_{beta_tag}_n{n_runs}.json"

    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Cross-run statistics saved to {stats_file}")

    # Print summary
    print()
    print("OBSERVABLE SUMMARY")
    print("-" * 40)
    if len(betas) == 1:
        for obs_name, obs_stats in stats["observables"].items():
            print(f"  {obs_name}:")
            print(f"    mean = {obs_stats['mean']:.6f}")
            print(f"    stderr = {obs_stats['stderr']:.6f}")
            print(f"    variance = {obs_stats['variance']:.6e}")
            print(f"    jackknife_err = {obs_stats['jackknife_error']:.6f}")
            print(f"    n = {obs_stats['n']}")
    else:
        for beta_key, obs_dict in stats["observables"].items():
            print(f"  {beta_key}:")
            for obs_name, obs_stats in obs_dict.items():
                print(f"    {obs_name}: mean={obs_stats['mean']:.6f} ± {obs_stats['stderr']:.6f}")

    if stats.get("peak_analysis"):
        print()
        print("PEAK ANALYSIS (across runs)")
        print("-" * 40)
        for name, peak_stats in stats["peak_analysis"].items():
            print(f"  {name}:")
            print(f"    mean = {peak_stats['mean']:.6f}")
            print(f"    std = {peak_stats['std']:.6f}")
            print(f"    stderr = {peak_stats['stderr']:.6f}")
            print(f"    variance = {peak_stats['variance']:.6e}")
            print(f"    jackknife_err = {peak_stats['jackknife_error']:.6f}")
            print(f"    n = {peak_stats['n']}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
