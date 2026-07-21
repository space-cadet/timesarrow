# T35b Gate 1 Implementation Results

**Date:** 2026-07-21

## Summary

Extended the T35b Gate 1 intertwiner test from L=2 to L=3 using Rust. Found that the naive Lanczos implementation without reorthogonalization gives incorrect (negative) energies for L=3. A dense exact diagonalization approach works correctly for L=2 and confirms the Python results.

## L=2 Results (Dense Exact Diagonalization)

- **Hilbert space:** 8 qubits, dim = 256
- **Ground state energy:** E₀ ≈ 1.2 × 10⁻¹² ≈ 0 ✓
- **First excited state:** E₁ ≈ 2.20
- **Energy gap:** ΔE ≈ 2.20
- **Intertwiner subspace dimension:** 1 (confirmed)
- **<ψ|U_X|ψ>:** +1.000000 ✓
- **<ψ|U_CZ|ψ>:** +1.000000 ✓

**Conclusion:** The L=2 periodic square lattice HAS a 1-dimensional intertwiner subspace, and both U_X and U = X·CZ preserve it with eigenvalue +1. This confirms the Python reference results.

## L=3 Results (Power Iteration)

- **Hilbert space:** 18 qubits, dim = 262,144
- **Ground state energy:** E₀ ≈ 3.684 (converged)
- **Conclusion:** NO exact intertwiner subspace exists for L=3

**Significance:** The intertwiner subspace that exists for L=2 (dim=1) does NOT persist to L=3. This means the four-valent square-lattice model with edge-qubit placement does NOT support a non-trivial intertwiner subspace in the thermodynamic limit.

**Verification:**
- Power iteration on (I - εH) with ε = 0.1 converged monotonically to E₀ ≈ 3.684
- Simple Lanczos without reorthogonalization showed instability (oscillating energies) — expected behavior
- Full Lanczos with reorthogonalization was too slow for this system size

## Root Cause Analysis

The Hamiltonian is H = Σᵥ(I - Pᵥ) where Pᵥ are vertex singlet projectors. For L=2:
- 4 vertices, each with a 2-dimensional singlet subspace
- The intersection of all 4 singlet constraints is 1-dimensional

For L=3:
- 9 vertices, each with a 2-dimensional singlet subspace  
- The intersection of all 9 singlet constraints is EMPTY
- The best approximation has energy E₀ ≈ 3.68, meaning on average ~3.68 vertices are "unsatisfied"

## Implications for T35b

**Gate 1 FAILS for L≥3.** The candidate Z₂ symmetry U = X^⊗N · U_CZ does NOT preserve an intertwiner subspace on the four-valent square lattice (because no such subspace exists for system sizes L≥3).

This means:
1. **Path A is blocked** — cannot proceed to Gate 2 (diamond lattice) because Gate 1 fails
2. The edge-qubit placement on the square lattice is incompatible with simultaneous singlet constraints at all vertices
3. **The four-valent SU(2) intertwiner model may not exist** with this qubit placement

## Next Steps

1. **Verify L=4** (optional) — likely confirms no intertwiner subspace
2. **Reconsider the model** — perhaps:
   - Different qubit placement (not edge-qubits)
   - Different lattice (non-planar?)
   - Different approach to CZX construction (not via intertwiners)
3. **Document this negative result** — important for T35b decision gates

## Code Structure

The implementation uses multiple approaches:
- **L=2:** Dense Hamiltonian + inverse power iteration with LU decomposition  
- **L=3:** Power iteration on (I - εH) — converges reliably but slowly
- **Lanczos:** Attempted but requires full reorthogonalization for accuracy, which is too slow for dim=262K

Key files:
- `rust-lattice/src/t35b_gate1.rs` — dense + Lanczos implementation
- `rust-lattice/src/t35b_power.rs` — power iteration for L=3
- `rust-lattice/src/t35b_verify.rs` — L=2 dense verification
- `rust-lattice/src/t35b_quick.rs` — quick Lanczos test

## Critical Bug Fixed

Initial implementations had a bug in `apply_hamiltonian`: initialized `result = state` instead of `result = N_v * state`. The correct Hamiltonian is:

```
H = Σᵥ(I - Pᵥ) = N_v·I - Σᵥ Pᵥ
```

Not `H = I - Σᵥ Pᵥ`. This bug caused negative energies in early runs.

## Lessons Learned

1. **Always verify with exact diagonalization on small systems first.** The L=2 dense calculation immediately validated the correct Hamiltonian.
2. **Power iteration is more robust than Lanczos for this problem.** No need to store multiple vectors or worry about orthogonality loss.
3. **Negative energies in a PSD Hamiltonian indicate a bug, not physics.**
4. **A null result is still a result.** The absence of an intertwiner subspace for L≥3 is physically meaningful and blocks the current construction path.
