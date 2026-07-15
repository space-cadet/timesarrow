#!/usr/bin/env python3
"""
t31-polyakov-exponent-analysis.py
=================================
Extract critical exponents from Polyakov loop susceptibility data.
Updated finite-size check using the L=8,10,12 proof-of-principle data and
the corrected L=16 fine scan.

Outputs:
  - figures/t31-polyakov-chi-vs-beta.pdf
  - figures/t31-polyakov-loglog-fit.pdf
  - t31-polyakov-exponents.json
"""

import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ─── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data/t31-polyakov-proof-of-principle-20260714.json"
FINE_FILES = {
    8: ROOT / "data/t31-polyakov-L8-fine-20260715.json",
    10: ROOT / "data/t31-polyakov-L10-fine-20260715.json",
    12: ROOT / "data/t31-polyakov-L12-fine-20260715.json",
    16: ROOT / "data/t31-polyakov-L16-fine-20260715.json",
}
OUT_DIR = ROOT / "output"
FIG_DIR = OUT_DIR / "figures"
OUT_JSON = OUT_DIR / "t31-polyakov-exponents.json"

FIG_DIR.mkdir(parents=True, exist_ok=True)

# ─── Load data ───────────────────────────────────────────────────────────────
with open(DATA_FILE) as f:
    data = json.load(f)
L_vals = [8, 10, 12, 16]
L_keys = ["L8", "L10", "L12", "L16"]
for lattice_size, fine_file in FINE_FILES.items():
    with open(fine_file) as f:
        fine_data = json.load(f)
    data["results"][f"L{lattice_size}"] = {
        key: [row[field] for row in fine_data["results"]]
        for key, field in {
            "beta": "beta",
            "meanPlaquette": "meanPlaquette",
            "meanPolyakov": "meanPolyakov",
            "polyakovSusceptibility": "polyakovSusceptibility",
            "polyakovBinder": "polyakovBinder",
        }.items()
    }

# ─── 1. Peak susceptibility for each L ───────────────────────────────────────
peaks = {}
for L, key in zip(L_vals, L_keys):
    r = data["results"][key]
    beta = np.array(r["beta"])
    chi = np.array(r["polyakovSusceptibility"])
    idx_max = int(np.argmax(chi))
    peaks[L] = {
        "beta_peak": float(beta[idx_max]),
        "chi_max": float(chi[idx_max]),
        "beta_all": beta.tolist(),
        "chi_all": chi.tolist(),
    }
    print(f"L={L:2d}: χ_P^max = {chi[idx_max]:.1f} at β = {beta[idx_max]:.2f}")

# ─── 2. Power-law fit: χ_P^max ∝ L^{γ/ν} ─────────────────────────────────────
L_arr = np.array(L_vals, dtype=float)
chi_max_arr = np.array([peaks[L]["chi_max"] for L in L_vals])


def power_law(L, A, gamma_over_nu):
    return A * L ** gamma_over_nu


def log_log_fit(L, chi_max):
    """Linear fit in log-log space: log χ = log A + (γ/ν) log L."""
    logL = np.log(L)
    logChi = np.log(chi_max)
    coeffs = np.polyfit(logL, logChi, 1)
    gamma_over_nu = coeffs[0]
    logA = coeffs[1]
    A = np.exp(logA)
    # estimate covariance from residuals
    y_fit = np.polyval(coeffs, logL)
    residuals = logChi - y_fit
    mse = np.mean(residuals**2)
    # approximate stderr of slope for 3 points
    x_mean = np.mean(logL)
    ssx = np.sum((logL - x_mean) ** 2)
    slope_err = np.sqrt(mse / ssx) if ssx > 0 else np.nan
    return A, gamma_over_nu, slope_err


A_fit, gamma_over_nu_fit, gamma_over_nu_err = log_log_fit(L_arr, chi_max_arr)

# Also do nonlinear fit for comparison
popt, pcov = curve_fit(power_law, L_arr, chi_max_arr, p0=[1.0, 2.0])
A_nonlin, gamma_nonlin = popt
gamma_nonlin_err = np.sqrt(pcov[1, 1])

print(f"\n--- Fit: χ_P^max = A · L^(γ/ν) ---")
print(f"Log-log linear fit:  γ/ν = {gamma_over_nu_fit:.4f} ± {gamma_over_nu_err:.4f}")
print(f"Nonlinear fit:       γ/ν = {gamma_nonlin:.4f} ± {gamma_nonlin_err:.4f}")

# 3D Ising reference
ising_gamma_over_nu = 1.2372 / 0.6301
print(f"3D Ising reference:  γ/ν = {ising_gamma_over_nu:.4f}")

# ─── 3. Binder cumulant crossing (coarse estimate) ───────────────────────────
# Look for where Binder values for different L cross.
# With only 3 L values and coarse β grid, this is very limited.
binder_data = {}
for L, key in zip(L_vals, L_keys):
    r = data["results"][key]
    binder_data[L] = {
        "beta": np.array(r["beta"]),
        "binder": np.array(r["polyakovBinder"]),
    }

# Simple estimate: find β where adjacent L curves are closest
# For L=8 vs L=10, L=10 vs L=12
crossing_estimates = []
for L1, L2 in [(8, 10), (10, 12)]:
    b1 = binder_data[L1]["beta"]
    b2 = binder_data[L2]["beta"]
    # both have same beta grid
    diff = np.abs(binder_data[L1]["binder"] - binder_data[L2]["binder"])
    idx_min = int(np.argmin(diff))
    crossing_estimates.append({
        "L_pair": f"{L1}-{L2}",
        "beta_cross": float(b1[idx_min]),
        "binder_diff": float(diff[idx_min]),
    })
    print(f"Binder crossing {L1}-{L2}: closest at β={b1[idx_min]:.2f}, diff={diff[idx_min]:.4f}")

# Estimate β_c from the peak position (mean and spread)
beta_peaks = [peaks[L]["beta_peak"] for L in L_vals]
beta_c_from_peak = np.mean(beta_peaks)

# ─── 4. Plots ────────────────────────────────────────────────────────────────

# Plot 1: χ_P vs β for all L
fig, ax = plt.subplots(figsize=(7, 5))
colors = {8: "C0", 10: "C1", 12: "C2", 16: "C3"}
markers = {8: "o", 10: "s", 12: "^", 16: "D"}
for L in L_vals:
    ax.plot(
        peaks[L]["beta_all"],
        peaks[L]["chi_all"],
        marker=markers[L],
        color=colors[L],
        label=f"L = {L}",
        markersize=6,
        linewidth=1.2,
    )
    # mark peak
    ax.axvline(peaks[L]["beta_peak"], color=colors[L], ls="--", alpha=0.4)

ax.set_xlabel(r"$\beta$")
ax.set_ylabel(r"$\chi_P = L^3 \, (\langle |P|^2 \rangle - \langle |P| \rangle^2)$")
ax.set_title("Polyakov Loop Susceptibility — Proof of Principle")
ax.legend(loc="upper left")
ax.set_ylim(bottom=0)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(FIG_DIR / "t31-polyakov-chi-vs-beta.pdf", dpi=300)
fig.savefig(FIG_DIR / "t31-polyakov-chi-vs-beta.png", dpi=300)
plt.close(fig)

# Plot 2: log-log fit
fig, ax = plt.subplots(figsize=(7, 5))
logL = np.log(L_arr)
logChi = np.log(chi_max_arr)
ax.scatter(logL, logChi, color="C3", s=80, zorder=3, label="Data")

# fit line
L_fine = np.linspace(7, 13, 200)
chi_fit = A_fit * L_fine ** gamma_over_nu_fit
ax.plot(np.log(L_fine), np.log(chi_fit), "k--", linewidth=1.5,
        label=rf"Fit: $\chi_P^{{\max}} \propto L^{{{gamma_over_nu_fit:.3f}}}$")

# 3D Ising reference line
chi_ising = chi_max_arr[0] * (L_arr / L_arr[0]) ** ising_gamma_over_nu
# normalise to pass through first data point for visual comparison
chi_ising_line = chi_max_arr[0] * (L_fine / L_arr[0]) ** ising_gamma_over_nu
ax.plot(np.log(L_fine), np.log(chi_ising_line), "g-.", linewidth=1.2, alpha=0.7,
        label=rf"3D Ising: $\gamma/\nu = {ising_gamma_over_nu:.3f}$")

ax.set_xlabel(r"$\ln L$")
ax.set_ylabel(r"$\ln \chi_P^{\max}$")
ax.set_title(r"Peak Susceptibility Scaling: $\chi_P^{\max} \propto L^{\gamma/\nu}$")
ax.legend(loc="lower right")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(FIG_DIR / "t31-polyakov-loglog-fit.pdf", dpi=300)
fig.savefig(FIG_DIR / "t31-polyakov-loglog-fit.png", dpi=300)
plt.close(fig)

print(f"\nPlots saved to {FIG_DIR}")

# ─── 5. Summary JSON ─────────────────────────────────────────────────────────
result = {
    "description": "Critical exponent extraction from Polyakov loop susceptibility (proof-of-principle)",
    "date": data["date"],
    "input_file": str(DATA_FILE),
    "peak_susceptibility": {
        str(L): {
            "beta_peak": peaks[L]["beta_peak"],
            "chi_max": peaks[L]["chi_max"],
        }
        for L in L_vals
    },
    "scaling_fit": {
        "model": "chi_P^max = A * L^(gamma/nu)",
        "method": "log-log linear regression",
        "L_used": L_vals,
        "A": float(A_fit),
        "gamma_over_nu": float(gamma_over_nu_fit),
        "gamma_over_nu_err": float(gamma_over_nu_err),
        "nonlinear_fit": {
            "A": float(A_nonlin),
            "gamma_over_nu": float(gamma_nonlin),
            "gamma_over_nu_err": float(gamma_nonlin_err),
        },
        "reduced_chi2": None,  # 3 data points, 2 params → 1 dof, not meaningful
    },
    "reference_3d_ising": {
        "gamma": 1.2372,
        "nu": 0.6301,
        "gamma_over_nu": ising_gamma_over_nu,
    },
    "comparison": {
        "measured_gamma_over_nu": float(gamma_over_nu_fit),
        "ising_gamma_over_nu": ising_gamma_over_nu,
        "relative_difference": float((gamma_over_nu_fit - ising_gamma_over_nu) / ising_gamma_over_nu),
        "agreement": "Provisional comparison only; the L=16 point is from a finer beta grid and has no matched-grid Binder crossing.",
    },
    "critical_beta": {
        "from_peak_position": {
            "beta_c": beta_c_from_peak,
            "note": "All peaks at β=0.76; no finite-size shift visible at this precision",
        },
        "from_binder_crossing": {
            "estimates": crossing_estimates,
            "note": "Crossing estimate uses the matched coarse grid for L=8,10,12. L=16 uses a finer grid and is excluded from this simple crossing calculation.",
        },
    },
    "caveats": [
        "L=8,10,12 use 10k thermal + 10k measure sweeps; L=16 uses 50k + 50k sweeps.",
        "β grid is coarse (Δβ=0.02 near peak); peak position may shift with finer grid.",
        "No jackknife or bootstrap error bars on χ_P — fit errors are formal only.",
        "Binder cumulant does not show clean crossing; L=12 binder at β=0.74 is anomalously low (0.094).",
        "3D Ising universality is expected for 3D Z₂ gauge theory; this enlarged scan remains provisional and is not a precision exponent extraction.",
    ],
    "plots": {
        "chi_vs_beta": str(FIG_DIR / "t31-polyakov-chi-vs-beta.pdf"),
        "loglog_fit": str(FIG_DIR / "t31-polyakov-loglog-fit.pdf"),
    },
}

with open(OUT_JSON, "w") as f:
    json.dump(result, f, indent=2)

print(f"\nSummary JSON saved to {OUT_JSON}")
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  γ/ν (measured)  = {gamma_over_nu_fit:.4f} ± {gamma_over_nu_err:.4f}")
print(f"  γ/ν (3D Ising)  = {ising_gamma_over_nu:.4f}")
print(f"  Relative diff   = {(gamma_over_nu_fit - ising_gamma_over_nu) / ising_gamma_over_nu * 100:+.1f}%")
print(f"  β_c (from peak) = {beta_c_from_peak:.2f}")
print("=" * 60)
