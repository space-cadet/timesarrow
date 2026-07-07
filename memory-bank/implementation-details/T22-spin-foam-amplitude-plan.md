# T22: Spin Foam Amplitude Calculation — Implementation Plan

*Created: 2026-06-28*
*Updated: 2026-07-08 02:50 IST*
*Task: T22*

## ⚠️ CORRECTION NOTICE (2026-07-08)

**The T22a implementation is a normalized SU(2) four-character group average, NOT a complete FK/EPRL spin-foam vertex amplitude.**

- The reported ratio is **R = 4/9 ≈ 0.444**, not a ~0.20 "probability ratio."
- The original code incorrectly applied an extra squaring step (0.45 → 0.20). **That squaring was an error and has been removed.**
- The **analytic result** is primary: G(j) = 1/(2j+1)².
- Monte Carlo is used only as validation.
- This calculation **does NOT establish j=1/2 dominance** for any physical model.

See T32 and the corrected T22a task page for details.

## Strategic Decision: Two-Path Approach

After discussion with Deepak (2026-06-28), we agreed on a two-path strategy:

**Path 1: Quick Estimate** → Immediate value for manuscript strengthening
**Path 2: Full Study** → Research-grade systematic validation

The choice between paths depends on how rigorously the manuscript needs the LQG → Wilson action connection.

---

## Path 1: Quick Estimate (1-2 Days)

### Goal
Compute |A_v(j=1)|² / |A_v(j=½)|² for a single 4-valent FK vertex with ~10% precision.

### Physics Setup

**FK Vertex Formula (4-valent):**

For a vertex v with 4 incident edges carrying spins j₁, j₂, j₃, j₄:

```
A_v^{FK}(j₁,j₂,j₃,j₄) = ∫_{SU(2)} ∏_{i=1}^4 dh_i δ(∏_i h_i) 
                         × ∫_{SU(2)} dg ∏_{i=1}^4 D^{j_i}_{m_i n_i}(g h_i g⁻¹)
                         × ι^{m₁ m₂ m₃ m₄} ι_{n₁ n₂ n₃ n₄}
```

For the simplified case (simple intertwiners, equal spins):

```
A_v^{FK}(j) = ∫_{SU(2)} dh D^j_{mn}(h) D^j_{mn}(h) D^j_{mn}(h) D^j_{mn}(h) × (intertwiner contractions)
```

**What we actually compute:**

For uniform spin j:
```
|A_v(j)|² = |∫_{SU(2)} dh [χ^j(h)]⁴ / (2j+1)³|²
```

where χ^j(h) = sin((2j+1)θ/2) / sin(θ/2) is the SU(2) character.

### Numerical Method

**Monte Carlo over SU(2):**

SU(2) elements can be parameterized by a unit vector n̂ and angle θ:
```
h = exp(i θ n̂ · σ/2) = cos(θ/2) I + i sin(θ/2) n̂ · σ
```

The Haar measure is:
```
dh = (1/2π²) sin²(θ/2) dθ dΩ_n̂
```

where θ ∈ [0, 2π], dΩ is the solid angle on S².

**Sampling algorithm:**
1. Sample θ with PDF ∝ sin²(θ/2) using inverse CDF
2. Sample n̂ uniformly on S²
3. Compute h = cos(θ/2) I + i sin(θ/2) n̂ · σ
4. Compute χ^j(h) = sin((2j+1)θ/2) / sin(θ/2)
5. Accumulate [χ^j(h)]⁴

**Expected samples needed:**
- For 10% precision: ~10⁶ samples
- Runtime: ~2-4 hours on MacBook Air (single thread)

### Deliverable

A single number with error bar:
```
R = |A_v(j=1)|² / |A_v(j=½)|² = 10^{-α±Δα}
```

If R ≪ 1, the manuscript can state: "Numerical evaluation of the FK vertex amplitude shows suppression of higher spins by factor ~10^{-α}, justifying the j=1/2 truncation."

### Limitations (Acknowledged)
- Single vertex (not full lattice)
- One model (FK, not EPRL)
- One γ value (not scanned)
- Simple intertwiners (not coherent states)

These limitations make the estimate conservative — the full path integral would have stronger suppression due to compounding.

---

## Path 2: Full Systematic Study (1-2 Weeks)

### Goal
Comprehensive validation of j=1/2 dominance across multiple parameters.

### Scope

**Models:**
- FK (Euclidean)
- EPRL (Lorentzian, simplified)

**Spin values:**
j = ½, 1, 3/2, 2, 5/2, 3

**Immurzi parameter:**
γ = 0.1, 0.237, 0.5, 1.0

**Intertwiner types:**
- Simple (EPRL/FK standard)
- Livine-Speziale coherent states

**Configurations:**
1. Uniform: (j,j,j,j)
2. Mixed: (½,½,½,j)
3. Checkerboard: alternating ½ and 1

### Implementation Architecture

**Phase 1: ts-quantum Core (T14)**
```
tsrc/
├── su2Haar.ts          # Haar measure sampling
├── representation.ts   # D^j(g) matrix elements
└── wignerD.ts          # Wigner D-matrices
```

**Phase 2: ts-quantum-spin-foam (T1-T5)**
```
tsrc/
├── fkVertex.ts         # FK vertex amplitude
├── eprlVertex.ts       # EPRL vertex amplitude
├── coherentStates.ts   # Livine-Speziale states
├── mcIntegrator.ts     # Monte Carlo with convergence checks
└── jDominanceCheck.ts  # Main analysis script
```

**Phase 3: Timesarrow Application**
- Import ts-quantum-spin-foam
- Run j=1/2 dominance check
- Generate plots and tables
- Update manuscript supplement

### Convergence Criteria

**Monte Carlo:**
- Target: <1% relative error on |A_v|²
- Method: Batch means with 10 batches
- Stopping: When std(batches) / mean < 0.01
- Typical samples: 10⁷ - 10⁸

**Asymptotic verification:**
- Fit A_v ~ j^{-α} for j ≥ 2
- Compare α with Donà et al. (2022) predictions
- Check: χ²/dof < 2 for fit quality

### Expected Results

**Hypothesis A (Strong suppression):**
- R = |A_v(j=1)|² / |A_v(j=½)|² ≈ 10^{-2} to 10^{-4}
- α ≈ 3-6 (asymptotic exponent)
- Conclusion: j=1/2 truncation well-justified

**Hypothesis B (Weak suppression):**
- R ≈ 10^{-1} to 10^{-0.5}
- α ≈ 1-2
- Conclusion: j=1/2 dominance needs additional arguments (thermal, entropy)

**Hypothesis C (Model-dependent):**
- FK: strong suppression
- EPRL: weak suppression
- Conclusion: Model choice matters for quantitative claims

---

## Comparison: Path 1 vs Path 2

| Aspect | Path 1 (Quick) | Path 2 (Full) |
|--------|---------------|---------------|
| Time | 1-2 days | 1-2 weeks |
| Spins | ½, 1 | ½, 1, 3/2, 2, 5/2, 3 |
| Models | FK only | FK + EPRL |
| γ scan | No | Yes |
| Coherent states | No | Yes |
| Precision | ~10% | <1% |
| Asymptotics | No | Yes (verify Donà et al.) |
| Value for manuscript | Good | Excellent |
| Research novelty | Low | Moderate |

---

## Recommendation

**Start with Path 1.** The quick estimate provides immediate value:
- Strengthens the manuscript with a concrete number
- Takes 1-2 days, not weeks
- Conservative bound (single vertex ≤ full lattice)
- Can always extend to Path 2 later if needed

**Upgrade to Path 2 if:**
- Path 1 shows weak suppression (R > 0.1)
- Reviewers demand stronger evidence
- The manuscript's central claim depends on j=1/2 uniqueness (not just approximation)

---

## References
- Donà, Fanizza, Sarno (2020): Numerical evaluation of spinfoam amplitudes
- Donà et al. (2022): Asymptotics of Lorentzian spinfoam amplitudes
- Perez (2013): The Spin-Foam Approach to Quantum Gravity (review)
- Engle, Pereira, Rovelli, Livine (EPRL, 2008)
- Freidel, Krasnov (FK, 2008)
