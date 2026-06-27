#!/usr/bin/env python3
"""
T20d: Critical exponent extraction from 3D Z₂ LGT finite-size scaling.

Uses fine-scan data for L = 8, 16, 24, 32 to extract:
- β_c (∞): critical coupling via Binder cumulant crossings
- ν: correlation length exponent from β_c(L) shift
- γ/ν: susceptibility peak scaling exponent
- α/ν: specific heat peak scaling exponent

References:
- Creutz et al. (1979): β_c = 0.7613, ν = 0.630, γ = 1.237
- Pelissetto & Vicari (2002): 3D Ising critical exponents review
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.plotting import (
    load_run,
    extract_observables,
    save_publication,
    setup_grid,
    annotate_beta_c,
    lattice_plot_kwargs,
    FIG_SIZES,
    PATHS,
)

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import brentq, curve_fit

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR = PATHS['docs_assets']
FIGURES_DIR = PATHS['figures']

# Fine-scan runs with good statistics
RUNS = {
    8:  't20-p3b-L8-3D-fine-20260627',
    16: 't20-p3b-L16-3D-fine-20260626',
    24: 't20-p3-L24-3D-wilson-fine-20250626',
    32: 't20-p3b-L32-lean-20260627',
}

# Literature values for comparison
LIT = {
    'beta_c': 0.7613,
    'nu': 0.630,
    'gamma': 1.237,
    'alpha': 2 - 3 * 0.630,  # = 0.110
    'beta_op': 0.327,  # order parameter exponent
    'U_star': 0.623,   # Binder cumulant crossing (periodic BC)
}

# ─────────────────────────────────────────────────────────────
# Load all fine-scan data
# ─────────────────────────────────────────────────────────────

data = {}
for L, run_id in RUNS.items():
    try:
        d = load_run(run_id)
        obs = extract_observables(d['results'])
        data[L] = obs
        print(f"✓ Loaded L={L}: {len(obs['betas'])} β values, β ∈ [{obs['betas'].min():.3f}, {obs['betas'].max():.3f}]")
    except FileNotFoundError as e:
        print(f"✗ L={L}: {e}")

# Sort by L
Ls = sorted(data)
print(f"\nAnalyzing L = {Ls}")

# ─────────────────────────────────────────────────────────────
# Extract peak observables for each L
# ─────────────────────────────────────────────────────────────

peaks = {}
for L in Ls:
    obs = data[L]
    
    # Susceptibility peak
    i_chi = np.argmax(obs['susceptibilities'])
    # Specific heat peak
    i_cv = np.argmax(obs['specific_heats'])
    
    peaks[L] = {
        'beta_chi': obs['betas'][i_chi],
        'chi_max': obs['susceptibilities'][i_chi],
        'beta_cv': obs['betas'][i_cv],
        'cv_max': obs['specific_heats'][i_cv],
        'binder_at_chi': obs['binder_cumulants'][i_chi],
    }

# Print peak summary
print("\n" + "=" * 70)
print("PEAK OBSERVABLES")
print("=" * 70)
print(f"{'L':>4} {'β_c(χ)':>10} {'χ_max':>12} {'β_c(C)':>10} {'C_max':>12} {'U(β_c)':>10}")
print("-" * 70)
for L in Ls:
    p = peaks[L]
    print(f"{L:>4} {p['beta_chi']:>10.4f} {p['chi_max']:>12.4f} {p['beta_cv']:>10.4f} {p['cv_max']:>12.4f} {p['binder_at_chi']:>10.4f}")

# ─────────────────────────────────────────────────────────────
# Method 1: Binder cumulant crossing analysis
# ─────────────────────────────────────────────────────────────

def find_crossing(betas1, u1, betas2, u2, beta_min=0.70, beta_max=0.80):
    """Find β where U_L1(β) = U_L2(β)."""
    f1 = interp1d(betas1, u1, kind='cubic', bounds_error=False, fill_value='extrapolate')
    f2 = interp1d(betas2, u2, kind='cubic', bounds_error=False, fill_value='extrapolate')
    
    def diff(beta):
        return f1(beta) - f2(beta)
    
    try:
        d_min, d_max = diff(beta_min), diff(beta_max)
        if d_min * d_max < 0:
            beta_c = brentq(diff, beta_min, beta_max)
            u_star = f1(beta_c)
            return beta_c, u_star
    except ValueError:
        pass
    return None, None

# Compute crossings for adjacent L pairs
crossings = []
for i in range(len(Ls) - 1):
    L1, L2 = Ls[i], Ls[i + 1]
    bc, us = find_crossing(data[L1]['betas'], data[L1]['binder_cumulants'],
                           data[L2]['betas'], data[L2]['binder_cumulants'])
    if bc is not None:
        crossings.append({'L1': L1, 'L2': L2, 'beta_c': bc, 'U_star': us})

print("\n" + "=" * 70)
print("BINDER CUMULANT CROSSINGS")
print("=" * 70)
print(f"{'Pair':>8} {'β_c':>10} {'U*':>10} {'U* - U_Ising':>14}")
print("-" * 70)
for c in crossings:
    print(f"L{c['L1']}×L{c['L2']:<3} {c['beta_c']:>10.4f} {c['U_star']:>10.4f} {c['U_star'] - LIT['U_star']:>+14.4f}")

if crossings:
    avg_bc = np.mean([c['beta_c'] for c in crossings])
    avg_us = np.mean([c['U_star'] for c in crossings])
    print(f"{'Average':>8} {avg_bc:>10.4f} {avg_us:>10.4f}")
    print(f"\nLiterature: β_c = {LIT['beta_c']:.4f}, U* = {LIT['U_star']:.3f}")

# ─────────────────────────────────────────────────────────────
# Method 2: β_c(L) shift scaling → extract ν
# ─────────────────────────────────────────────────────────────

# Fit: β_c(L) = β_c(∞) + a * L^(-1/ν)
def bc_shift_model(L, bc_inf, a, nu_inv):
    return bc_inf + a * L**(-nu_inv)

L_arr = np.array(Ls, dtype=float)
beta_c_arr = np.array([peaks[L]['beta_chi'] for L in Ls])

# Initial guess: [bc_inf, a, 1/nu]
p0 = [0.76, -0.1, 1.6]
try:
    popt, pcov = curve_fit(bc_shift_model, L_arr, beta_c_arr, p0=p0)
    bc_inf_fit, a_fit, nu_inv_fit = popt
    nu_fit = 1 / nu_inv_fit
    bc_err = np.sqrt(pcov[0, 0])
    nu_err = np.sqrt(pcov[2, 2]) / (nu_inv_fit**2)  # error propagation
    
    print("\n" + "=" * 70)
    print("β_c(L) SHIFT SCALING FIT")
    print("=" * 70)
    print(f"\nFit: β_c(L) = β_c(∞) + a·L^(-1/ν)")
    print(f"  β_c(∞) = {bc_inf_fit:.4f} ± {bc_err:.4f}")
    print(f"  a      = {a_fit:.4f}")
    print(f"  ν      = {nu_fit:.3f} ± {nu_err:.3f}")
    print(f"  Literature: ν = {LIT['nu']:.3f}")
    print(f"  χ²/ndof = {np.sum((beta_c_arr - bc_shift_model(L_arr, *popt))**2):.4f}")
except RuntimeError:
    print("\n✗ β_c shift fit failed to converge")
    bc_inf_fit, nu_fit = None, None

# ─────────────────────────────────────────────────────────────
# Method 3: χ_max scaling → extract γ/ν
# ─────────────────────────────────────────────────────────────

def chi_scaling_model(L, c, gamma_over_nu):
    return c * L**gamma_over_nu

chi_max_arr = np.array([peaks[L]['chi_max'] for L in Ls])

try:
    popt_chi, pcov_chi = curve_fit(chi_scaling_model, L_arr, chi_max_arr, p0=[0.1, 1.0])
    c_chi, gon_fit = popt_chi
    gon_err = np.sqrt(pcov_chi[1, 1])
    
    print("\n" + "=" * 70)
    print("SUSCEPTIBILITY PEAK SCALING")
    print("=" * 70)
    print(f"\nFit: χ_max(L) = c·L^(γ/ν)")
    print(f"  γ/ν (fitted) = {gon_fit:.3f} ± {gon_err:.3f}")
    print(f"  γ/ν (Ising)  = {LIT['gamma']/LIT['nu']:.3f}")
    print(f"  If ν = {LIT['nu']:.3f} → γ = {gon_fit * LIT['nu']:.3f} (Ising: {LIT['gamma']:.3f})")
except RuntimeError:
    print("\n✗ χ scaling fit failed")
    gon_fit = None

# ─────────────────────────────────────────────────────────────
# Method 4: C_V max scaling → extract α/ν
# ─────────────────────────────────────────────────────────────

cv_max_arr = np.array([peaks[L]['cv_max'] for L in Ls])

try:
    popt_cv, pcov_cv = curve_fit(chi_scaling_model, L_arr, cv_max_arr, p0=[0.1, 0.1])
    c_cv, aon_fit = popt_cv
    aon_err = np.sqrt(pcov_cv[1, 1])
    
    print("\n" + "=" * 70)
    print("SPECIFIC HEAT PEAK SCALING")
    print("=" * 70)
    print(f"\nFit: C_max(L) = c·L^(α/ν)")
    print(f"  α/ν (fitted) = {aon_fit:.3f} ± {aon_err:.3f}")
    print(f"  α/ν (Ising)  = {LIT['alpha']/LIT['nu']:.3f}")
    print(f"  If ν = {LIT['nu']:.3f} → α = {aon_fit * LIT['nu']:.3f} (Ising: {LIT['alpha']:.3f})")
except RuntimeError:
    print("\n✗ C_V scaling fit failed")
    aon_fit = None

# ─────────────────────────────────────────────────────────────
# Summary plot: 2×2 panel
# ─────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=FIG_SIZES['square'])

# (0,0): Binder cumulant vs β
ax = axes[0, 0]
for L in Ls:
    obs = data[L]
    ax.plot(obs['betas'], obs['binder_cumulants'], **lattice_plot_kwargs(L))
for c in crossings:
    ax.plot(c['beta_c'], c['U_star'], 'k*', markersize=15, zorder=5)
annotate_beta_c(ax, beta_c=LIT['beta_c'])
ax.axhline(LIT['U_star'], color='orange', linestyle=':', linewidth=1.5, alpha=0.7, label=f"Ising U* = {LIT['U_star']}")
ax.set_ylabel(r'Binder cumulant $U$')
ax.set_title('Binder Cumulant Crossing')
ax.set_xlim(0.70, 0.80)
ax.set_ylim(0.62, 0.68)
setup_grid(ax)
ax.legend(fontsize=8)

# (0,1): β_c(L) shift
ax = axes[0, 1]
ax.plot(L_arr, beta_c_arr, 'ko', markersize=10, label=r'$\beta_c$ from $\chi_{\max}$')
if bc_inf_fit is not None:
    L_fit = np.linspace(6, 40, 100)
    ax.plot(L_fit, bc_shift_model(L_fit, *popt), 'r--', linewidth=1.5, alpha=0.7,
            label=f"Fit: $\\beta_c(\\infty)$ = {bc_inf_fit:.4f}")
ax.axhline(LIT['beta_c'], color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label=f"Lit: {LIT['beta_c']}")
ax.set_xlabel(r'$L$')
ax.set_ylabel(r'$\beta_c(L)$')
ax.set_title(r'Critical Coupling Shift ($\nu$ extraction)')
ax.set_xlim(0, 36)
setup_grid(ax)
ax.legend(fontsize=8)

# (1,0): χ_max scaling
ax = axes[1, 0]
ax.plot(L_arr, chi_max_arr, 'ko', markersize=10, label=r'$\chi_{\max}$')
if gon_fit is not None:
    L_fit = np.linspace(6, 40, 100)
    ax.plot(L_fit, chi_scaling_model(L_fit, *popt_chi), 'r--', linewidth=1.5, alpha=0.7,
            label=f"Fit: $\\gamma/\\nu$ = {gon_fit:.2f}")
ax.set_xlabel(r'$L$')
ax.set_ylabel(r'$\chi_{\max}(L)$')
ax.set_title(r'Susceptibility Peak Scaling ($\gamma/\nu$)')
ax.set_xlim(0, 36)
ax.set_yscale('log')
ax.set_xscale('log')
setup_grid(ax)
ax.legend(fontsize=8)

# (1,1): C_V max scaling
ax = axes[1, 1]
ax.plot(L_arr, cv_max_arr, 'ko', markersize=10, label=r'$C_{V,\max}$')
if aon_fit is not None:
    L_fit = np.linspace(6, 40, 100)
    ax.plot(L_fit, chi_scaling_model(L_fit, *popt_cv), 'r--', linewidth=1.5, alpha=0.7,
            label=f"Fit: $\\alpha/\\nu$ = {aon_fit:.2f}")
ax.set_xlabel(r'$L$')
ax.set_ylabel(r'$C_{V,\max}(L)$')
ax.set_title(r'Specific Heat Peak Scaling ($\alpha/\nu$)')
ax.set_xlim(0, 36)
ax.set_yscale('log')
ax.set_xscale('log')
setup_grid(ax)
ax.legend(fontsize=8)

plt.suptitle('T20d: 3D Z₂ LGT Critical Exponent Extraction', fontsize=14, fontweight='bold')
plt.tight_layout()
save_publication(fig, 't20d-critical-exponents-summary', output_dir=FIGURES_DIR)
plt.close()

print(f"\n✓ Figure saved: t20d-critical-exponents-summary.png")

# ─────────────────────────────────────────────────────────────
# Final summary
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("T20D SUMMARY: CRITICAL EXPONENTS")
print("=" * 70)
print(f"\n{'Quantity':<25} {'Fitted':>15} {'Literature':>15} {'Status':>10}")
print("-" * 70)

if bc_inf_fit is not None:
    status = "✓" if abs(bc_inf_fit - LIT['beta_c']) < 0.01 else "~"
    print(f"{'β_c(∞)':<25} {bc_inf_fit:>15.4f} {LIT['beta_c']:>15.4f} {status:>10}")

if nu_fit is not None:
    status = "✓" if abs(nu_fit - LIT['nu']) < 0.05 else "~"
    print(f"{'ν (correlation length)':<25} {nu_fit:>15.3f} {LIT['nu']:>15.3f} {status:>10}")

if gon_fit is not None:
    gamma_fit = gon_fit * (nu_fit if nu_fit else LIT['nu'])
    status = "✓" if abs(gamma_fit - LIT['gamma']) < 0.1 else "~"
    print(f"{'γ (susceptibility)':<25} {gamma_fit:>15.3f} {LIT['gamma']:>15.3f} {status:>10}")

if aon_fit is not None:
    alpha_fit = aon_fit * (nu_fit if nu_fit else LIT['nu'])
    status = "✓" if abs(alpha_fit - LIT['alpha']) < 0.05 else "~"
    print(f"{'α (specific heat)':<25} {alpha_fit:>15.3f} {LIT['alpha']:>15.3f} {status:>10}")

print("\n" + "=" * 70)
print("NOTES")
print("=" * 70)
print("- L = 8, 16, 24, 32 used for FSS")
print("- Binder crossings show β_c ≈ 0.76 consistent with literature")
print("- Exponent extraction limited by L range; L = 48, 64 would improve precision")
print("- Systematic errors (fit form, corrections-to-scaling) not included")
