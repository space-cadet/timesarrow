# timesarrow — Active Context

*Updated: 2026-07-21 16:45 IST*

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

## T35b Diamond-Lattice Existence Test 🔄

T35b now makes the 3D construction question explicit. It first requires a correct four-valent square-lattice vertex/edge mapping and intertwiner-preservation test, then a minimal periodic diamond-cluster test. The diamond 2-skeleton is sufficient for these first gates; missing 3-cells block bulk-topology claims.

### Gate 1 Results (2026-07-21): Four-Valent Square-Lattice Test ✅

**Specification drafted:** `memory-bank/implementation/t35b-gate1-specification.md`

**Test cluster:** $L=2$ periodic square lattice (4 vertices, 8 edge-qubits, Hilbert space dim 256)

**Key findings:**
- Gate 1 **passes**: $U = X^{\otimes 8} \cdot U_{CZ}$ preserves the intertwiner subspace exactly ($[U, P_{\text{int}}] = 0$, no leakage)
- **Surprise:** The intertwiner subspace is **1-dimensional** for $L=2$ — unexpectedly small
- Vertex projectors **do not commute** (norm ~1.54 for adjacent vertices); global projector is intersection, not product
- Both $U$ (with CZ) and $U_X = X^{\otimes 8}$ (without CZ) preserve the intertwiner subspace — the CZ is not probed on $L=2$
- Larger clusters needed to distinguish operators

**Open question:** Does the intertwiner subspace grow for $L=3, 4$? Is the edge-qubit model the right placement?

**Files:**
- Script: `numerics/scripts/t35b-gate1-square-lattice.py`
- Results: `memory-bank/implementation/t35b-gate1-results.md`

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35a Thread 3** | ts-quantum cross-check + boundary MPUO | 🔄 | — |
| 2 | **T35b** | Diamond CZX existence test | 🔄 | T33a, T35a |
| 3 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 4 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 5 | T32 | Rust 2024 reproducibility | 🔄 | — |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
