# timesarrow — Active Context

*Updated: 2026-07-21 19:05 IST*

## T33a Foundation Validated 🔄

The reusable Z₂ boundary-operator API and connected diamond 2-skeleton are built and tested. Diamond 3-cells and general-complex Monte Carlo integration remain open; see `implementation/T33a-cell-complex-api.md` for the exact boundary.

## T35a CZX Construction — Many-Body Results ✅

Explicit construction of the CZX SPT state completed on single plaquette and 2×2 torus (16 qubits). Key results:
- Single plaquette: $|\Psi\rangle = (|0000\rangle + |1111\rangle)/\sqrt2$ is exact +1 eigenvector of $U_{CZX}$
- Open plaquette: boundary signature shows relative sign ($\langle\Psi|U|\Psi\rangle = 0$)
- 2×2 torus: **global** $\prod_s U_{CZX,s}$ preserves state; single-site does NOT
- CZ cancellation on shared links is the mechanism (each link gets CZ twice)

Code: `numerics/scripts/t35a-czx-construction-verify.py` (numpy, exact state-vector).
Theory doc updated: `theory/docs/czx-intertwiner-analysis.md`.

## T35a Thread 2: Parent Hamiltonian ✅ COMPLETE

**Completed: 2026-07-21**

Verified the parent Hamiltonian for the 2×2 torus CZX state using Rust matrix-free Lanczos eigensolver.

### Results

**Hamiltonian**: H = Σ_p h_p where h_p = (1/2)[(I-XXXX) + (I-ZZII) + (I-IZZI) + (I-IIZZ)]

| Check | Result | Value |
|-------|--------|-------|
| H\|Ψ₀⟩ = 0 | ✅ PASS | \|\|H\|Ψ₀⟩\| = 0 |
| Unique ground state | ✅ PASS | 1 zero eigenvalue |
| Gapped | ✅ PASS | Gap = **1.0** |
| Positive semidefinite | ✅ PASS | E_min = 0 |
| Local terms commute | ✅ PASS | All [hᵢ, hⱼ] ≈ 0 |

**Spectrum**: E₀=0, E₁=1, E₂=2, E₃=3, E₄=4, ... (equally spaced!)

This confirms the CZX state is the **unique gapped ground state** of a **commuting projector Hamiltonian** — the hallmark of a topologically trivial SPT phase.

### Implementation
- **Rust**: `rust-lattice/src/t35a_thread2.rs` — matrix-free Lanczos, 17 iterations to convergence
- **Python**: `numerics/scripts/t35a-thread2-parent-hamiltonian.py` — matrix-free stabilizer version
- **TypeScript**: `numerics/scripts/t35a-thread2-verify.ts` — ts-quantum sparse eigensolver (pending build fix)

### Key Finding
The equal spacing (gap = 1.0) indicates independent plaquette contributions. Each plaquette's ground state is a 4-qubit GHZ state, and the full ground state is their tensor product. The Hamiltonian is frustration-free.

**Open threads:** boundary MPUO / 3-cocycle, ts-quantum cross-check, 3D generalization.

## T35b Diamond-Lattice Existence Test 🔄 **BLOCKED — Edge-Qubit Model Fails**

T35b makes the 3D construction question explicit. It first requires a correct four-valent square-lattice vertex/edge mapping and intertwiner-preservation test, then a minimal periodic diamond-cluster test.

### Gate 1 Results (2026-07-21): Four-Valent Square-Lattice Test

**L=2 (Dense exact diagonalization):**
- Hilbert space: 8 edge-qubits, dim = 256
- Ground state energy: E₀ ≈ 1.2×10⁻¹² ≈ 0 ✅
- Intertwiner subspace dimension: 1
- <ψ|U_X|ψ> = +1.000000 ✅
- <ψ|U_CZ|ψ> = +1.000000 ✅
- First excited state: E₁ ≈ 2.20, gap ΔE ≈ 2.20

**L=3 (Power iteration, converged):**
- Hilbert space: 18 edge-qubits, dim = 262,144
- Ground state energy: E₀ ≈ 3.684 (converged, stable)
- **No exact intertwiner subspace exists** ❌

**Critical Finding:** The edge-qubit model is incompatible with simultaneous singlet constraints at all vertices for L≥3. The intersection of all vertex singlet projectors is EMPTY for L=3.

**Hamiltonian Bug Fixed:** Initial implementations computed `H = I - ΣPᵥ` instead of `H = Nᵥ·I - ΣPᵥ`.

**Realization:** The qubit placement needs reconsideration. T35a uses **vertex-qubits** (qubits at plaquette corners), not edge-qubits. The diamond-lattice CZX construction likely requires vertex-qubits or vertex-hexagon incidence, not the edge-qubit Levin-Wen type model that was tested.

**Code:**
- `rust-lattice/src/t35b_gate1.rs` — dense (L=2) + Lanczos (L=3)
- `rust-lattice/src/t35b_power.rs` — power iteration for L=3
- `rust-lattice/src/t35b_verify.rs` — L=2 dense verification
- Results: `memory-bank/implementation/t35b-gate1-results.md`

### Next Steps
- [ ] Reconsider qubit placement: vertex-qubits (T35a-style) vs edge-qubits vs vertex-hexagon incidence
- [ ] Design new Gate 1 test with vertex-qubit placement
- [ ] Document this negative result and pivot direction

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35b Pivot** | Reconsider qubit placement for CZX construction | 🔄 | T35a |
| 2 | **T35a Thread 3** | ts-quantum cross-check + boundary MPUO | 🔄 | — |
| 3 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 4 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 5 | T32 | Rust 2024 reproducibility | 🔄 | — |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
