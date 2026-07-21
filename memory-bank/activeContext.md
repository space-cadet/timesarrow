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

## T35b Diamond-Lattice CZX Existence Test 🔄 **PIVOT — Encoded Tetrahedral Specification Written**

T35b makes the 3D construction question explicit. After the edge-qubit model failed at L=3, Terra's analysis clarified that the issue was the **gluing rule**, not the qubit placement. The correct approach uses **virtual legs + singlet contraction**, not shared physical edge qubits.

**New spec written**: `memory-bank/implementation/t35b-encoded-tetrahedral-czx-spec.md`

### What Changed
- Physical DOF: one **intertwiner qubit** per tetrahedron (2D invariant subspace of 4 virtual spin-1/2 legs)
- Gluing: ε_mn contraction on shared faces (no shared physical qubit)
- Symmetry: **encoded CZX** on logical intertwiner qubits, lifted via W_v
- Key insight: code-space preservation is automatic, but **gluing compatibility** is the non-trivial test

### Hard Gates (from spec)
- Gate A: Explicit intertwiner basis and encoding map W_v
- Gate B: Locality and gluing compatibility (commutation with edge singlet constraints)
- Gate C: Global symmetry on small closed patch
- Gate D: Parent Hamiltonian
- Gate E: Boundary anomaly / MPUO

### Next Steps
- [ ] Implement Gate A: Write W_v explicitly in recoupling basis, verify numerically
- [ ] Implement Gate B: Test [U_CZX, ε_gluing] = 0 on 2×2 torus
- [ ] If Gates A-B pass, proceed to Gate C (global symmetry) and Gate D (parent Hamiltonian)

**Code**: New Rust module `rust-lattice/src/t35b_encoded/` (to be created)
**Old code preserved**: `rust-lattice/src/t35b_gate1.rs`, `t35b_power.rs`, `t35b_verify.rs` (documented negative result)

## What's Next

| Priority | Task | Status | Depends On |
|----------|------|--------|------------|
| 1 | **T35b Gate A** | Implement explicit W_v encoding map | 🔄 | — |
| 2 | **T35b Gate B** | Test gluing compatibility on 2×2 torus | ⏳ | Gate A |
| 3 | **T35a Thread 3** | ts-quantum cross-check + boundary MPUO | 🔄 | — |
| 4 | **T33b** | Diamond lattice Polyakov scan | ⏳ | T33a |
| 5 | **T34a** | Configuration snapshot output mode | ⏳ | — |
| 6 | T32 | Rust 2024 reproducibility | 🔄 | — |

**Key principle:** Gauge-transition numerics are control physics; the explicit microscopic CZX realization is the actual unresolved claim.

---

*Historical context for detailed sessions: see `implementation/` docs and `memory/YYYY-MM-DD.md` files.*
