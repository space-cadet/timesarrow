# T35b Gate 1: Matrix-Free Intertwiner Subspace Iteration (Rust)

*Created: 2026-07-21 18:02 IST*
*Related: T35b Diamond-Lattice CZX Existence Test*

## Problem

Extend the four-valent square-lattice intertwiner test from L=2 to L=3 and L=4. The full Hilbert space dimensions are:

| L | Vertices | Edges (qubits) | Hilbert space dim |
|---|----------|----------------|-------------------|
| 2 | 4 | 8 | 256 |
| 3 | 9 | 18 | 262,144 |
| 4 | 16 | 32 | 4,294,967,296 |

Dense matrix approaches fail at L=3 and beyond. The L=2 Python script used dense `ndarray` (256×256), which is fine for L=2 but infeasible for L=3+.

## Solution: Matrix-Free Subspace Iteration

Following the same philosophy as `t35a_thread2.rs` (matrix-free Lanczos for 16-qubit parent Hamiltonian), we avoid storing dense matrices entirely.

### Key Insight

The intertwiner subspace is expected to be small (L=2: dim=1). We only need to *find* this subspace, not represent operators on the full space.

### Algorithm

```
1. Build the 4-valent singlet projector P_v (16×16 dense, once)
   - Find null space of S² = (Σᵢ Sᵢ)² for 4 qubits
   - Result: 2-dimensional subspace spanned by |s₁⟩, |s₂⟩
   - P_v = |s₁⟩⟨s₁| + |s₂⟩⟨s₂|

2. For a given L, construct the vertex-edge incidence map:
   - Each vertex v has 4 incident edges (qubits)
   - Edge ordering follows a fixed convention (e.g., +x, +y, -x, -y)

3. Subspace iteration to find the global intertwiner subspace:
   a. Start with k random state vectors (k = estimated subspace dim + buffer)
   b. For each vertex v:
      - Apply P_v to each vector: extract 4-qubit amplitudes, project, reconstruct
   c. Orthogonalize (modified Gram-Schmidt)
   d. Repeat until convergence (subspace dimension stabilizes)

4. Tests on the converged subspace basis {bᵢ}:
   a. Leakage: ||(I - P_int) U |bᵢ⟩|| for each basis vector
   b. Commutator: ||[U, P_int]|| (via action on basis)
   c. Eigenvalues: diagonalize U restricted to the intertwiner subspace
   d. Compare U = X^⊗N · U_CZ vs U_X = X^⊗N alone
```

### Matrix-Free Vertex Projector Application

For a state |ψ⟩ (full N-qubit space), applying P_v:

```
For each basis state |n⟩ in |ψ⟩:
    Extract bits for the 4 edges of vertex v
    Form local index i ∈ [0, 15] from these 4 bits
    The remaining N-4 bits form a "frozen" configuration c
    
    Collect all amplitudes ψ_{i,c} for fixed c, varying i
    Apply P_v to this 16-dim vector: ψ'_{i,c} = Σⱼ P_v[i,j] ψ_{j,c}
    Write back: new_state[config(i,c)] += ψ'_{i,c}
```

This is O(2^N · 16²) per vertex, but since we only apply it to k vectors (k ≈ few), and iterate ~10-20 times, it's feasible even for L=4 (32 qubits, ~4 billion configs) — though L=4 may need checkpointing or parallelization.

### Matrix-Free Symmetry Operators

**U_X = X^⊗N**: Bit-flip all edge qubits. Applied by `new_idx = idx ^ ((1<<N) - 1)`.

**U_CZ**: Phase (-1) on plaquettes where two edges are both |1⟩. Applied by checking bit patterns.

### Output

| Quantity | How computed |
|----------|-------------|
| Intertwiner dim | Final orthogonalized basis size |
| Leakage norm | Apply U to each bᵢ, project out of subspace, measure norm |
| Commutator norm | ||U P_int bᵢ - P_int U bᵢ|| averaged over basis |
| U eigenvalues on subspace | Small dense matrix: Mᵢⱼ = ⟨bᵢ|U|bⱼ⟩ |
| U_X vs U comparison | Same tests for both, compare eigenvalue spectra |

## Rust Implementation Plan

New binary: `t35b_gate1.rs`

Dependencies: existing `ndarray`, `rand`, `rayon` (for parallelization if needed)

Key functions:
- `build_singlet_projector() -> Array2<f64>` (16×16)
- `apply_vertex_projector(state: &mut [f64], edges: &[usize])` (matrix-free)
- `subspace_iteration(n_qubits, vertices, max_iter, tolerance) -> Vec<Vec<f64>>` (basis vectors)
- `apply_ux(state: &mut [f64], n_qubits)`
- `apply_ucz(state: &mut [f64], plaquettes: &[[usize; 4]])`
- `test_leakage(basis, u_operator) -> f64`
- `test_commutator(basis, u_operator) -> f64`
- `eigenvalues_on_subspace(basis, u_operator) -> Vec<f64>`

## Expected Results

| L | Expected intertwiner dim | Key question |
|---|--------------------------|--------------|
| 2 | 1 (confirmed) | Baseline |
| 3 | ? | Does it grow? |
| 4 | ? | Is CZ visible? |

If L=3 shows dim > 1 and U ≠ U_X on the subspace, proceed to Gate 2 (diamond cluster).
If intertwiner dim stays pathologically small, reconsider edge-qubit placement.

## References

- `t35a_thread2.rs`: Matrix-free Lanczos approach for 16-qubit system
- `t35b-gate1-square-lattice.py`: Python L=2 reference implementation
- `memory-bank/implementation/t35b-gate1-results.md`: L=2 results
