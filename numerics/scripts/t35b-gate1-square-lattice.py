"""
T35b Gate 1: Four-Valent Square-Lattice Intertwiner Test
Date: 2026-07-21

Test whether a candidate Z_2 symmetry preserves the SU(2) intertwiner subspace
on a periodic L=2 square lattice (4 vertices, 8 edge-qubits).
"""

import numpy as np
from itertools import product

# ─── Pauli operators ───
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron_list(ops):
    """Kronecker product of a list of matrices."""
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result


def single_qubit_op(op, qubit_idx, n_qubits):
    """Apply single-qubit operator `op` to qubit `qubit_idx` in an n-qubit system."""
    ops = [I2] * n_qubits
    ops[qubit_idx] = op
    return kron_list(ops)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. FOUR-VALENT SINGLET PROJECTOR
# ═══════════════════════════════════════════════════════════════════════════════

def build_singlet_states():
    """
    Build the two orthogonal singlet states for four spin-1/2.
    Ordering: (e1, e2, e3, e4) in counterclockwise order.
    
    Uses the null-space method: find states with S^2 |psi> = 0.
    """
    # Build total spin operators for 4 qubits
    Sx = sum(single_qubit_op(X, i, 4) for i in range(4)) / 2
    Sy = sum(single_qubit_op(Y, i, 4) for i in range(4)) / 2
    Sz = sum(single_qubit_op(Z, i, 4) for i in range(4)) / 2
    S2 = Sx @ Sx + Sy @ Sy + Sz @ Sz
    
    # Find null space of S^2 (eigenvalue = 0)
    eigs, vecs = np.linalg.eigh(S2)
    singlet_indices = np.where(np.abs(eigs) < 1e-10)[0]
    
    assert len(singlet_indices) == 2, f"Expected 2 singlets, got {len(singlet_indices)}"
    
    s1 = vecs[:, singlet_indices[0]]
    s2 = vecs[:, singlet_indices[1]]
    
    # Ensure real and positive leading coefficient
    if np.abs(s1[0]) < 1e-10:
        # Find first nonzero component
        for i in range(16):
            if np.abs(s1[i]) > 1e-10:
                s1 = s1 / (s1[i] / np.abs(s1[i]))
                break
    else:
        s1 = s1 / (s1[0] / np.abs(s1[0]))
    
    if np.abs(s2[0]) < 1e-10:
        for i in range(16):
            if np.abs(s2[i]) > 1e-10:
                s2 = s2 / (s2[i] / np.abs(s2[i]))
                break
    else:
        s2 = s2 / (s2[0] / np.abs(s2[0]))
    
    # Make s2 orthogonal to s1
    overlap = np.vdot(s1, s2)
    s2 = s2 - overlap * s1
    s2 = s2 / np.linalg.norm(s2)
    
    # Verify
    assert np.isclose(np.vdot(s1, s1), 1.0)
    assert np.isclose(np.vdot(s2, s2), 1.0)
    assert np.isclose(np.vdot(s1, s2), 0.0)
    assert np.isclose(np.vdot(s1, S2 @ s1), 0.0, atol=1e-10)
    assert np.isclose(np.vdot(s2, S2 @ s2), 0.0, atol=1e-10)
    
    return s1, s2


def build_vertex_projector():
    """Build the 4-valent singlet projector P_v (16x16)."""
    s1, s2 = build_singlet_states()
    Pv = np.outer(s1, s1.conj()) + np.outer(s2, s2.conj())
    
    # Verify projector properties
    assert np.allclose(Pv @ Pv, Pv)
    assert np.allclose(Pv.T.conj(), Pv)
    assert np.isclose(np.trace(Pv), 2.0)  # 2-dimensional singlet subspace
    
    return Pv


# ═══════════════════════════════════════════════════════════════════════════════
# 2. L=2 PERIODIC SQUARE LATTICE: VERTEX-EDGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

# 4 vertices: (0,0), (1,0), (0,1), (1,1)
# 8 edges: 4 horizontal + 4 vertical
# Edge ordering: h00, h10, h01, h11, v00, v10, v01, v11

VERTEX_EDGES = {
    (0, 0): [0, 4, 1, 5],   # (+x=h00, +y=v00, -x=h10, -y=v10)
    (1, 0): [1, 6, 0, 7],   # (+x=h10, +y=v01, -x=h00, -y=v11)
    (0, 1): [2, 5, 3, 4],   # (+x=h01, +y=v10, -x=h11, -y=v00)
    (1, 1): [3, 7, 2, 6],   # (+x=h11, +y=v11, -x=h01, -y=v01)
}

N_VERTICES = 4
N_EDGES = 8


def build_global_projector(Pv):
    """
    Build the global intertwiner projector P_int.
    
    Each vertex projector P_v acts on 4 edge-qubits. Edge-qubits are shared
    between vertices, so the vertex projectors do NOT commute in general.
    
    The gauge-invariant subspace is the intersection of all vertex singlet
    subspaces. We compute the projector onto this intersection by finding
    the simultaneous +1 eigenspace of all vertex projectors.
    
    For L=2 with 8 edge-qubits, the full Hilbert space has dimension 256.
    """
    dim = 2 ** N_EDGES
    
    # Build each vertex projector as a 256x256 matrix
    P_list = []
    for v_idx, (vx, vy) in enumerate([(0,0), (1,0), (0,1), (1,1)]):
        edges = VERTEX_EDGES[(vx, vy)]
        
        # Pv acts on the 4 edge-qubits in `edges`
        # We need to embed Pv (16x16) into the full 256-dim space
        P_full = np.zeros((dim, dim), dtype=complex)
        
        # Iterate over all basis states of the 8 edge-qubits
        for state in range(dim):
            # Extract bits for the 4 edges of this vertex
            bits = [(state >> (N_EDGES - 1 - e)) & 1 for e in edges]
            local_idx = sum(b << (3 - i) for i, b in enumerate(bits))
            
            # Apply Pv to the local state
            for state2 in range(dim):
                bits2 = [(state2 >> (N_EDGES - 1 - e)) & 1 for e in edges]
                local_idx2 = sum(b << (3 - i) for i, b in enumerate(bits2))
                
                # Check if the other 4 edge-qubits match
                other_edges = [e for e in range(N_EDGES) if e not in edges]
                match = all(
                    ((state >> (N_EDGES - 1 - e)) & 1) == 
                    ((state2 >> (N_EDGES - 1 - e)) & 1)
                    for e in other_edges
                )
                
                if match:
                    P_full[state2, state] = Pv[local_idx2, local_idx]
        
        P_list.append(P_full)
    
    # Compute the intersection projector
    # Method: P_int = lim_{n->inf} (P1 P2 P3 P4)^n
    # Since P_i are projectors, iterating converges to the intersection projector
    P_int = np.eye(dim, dtype=complex)
    for P in P_list:
        P_int = P_int @ P
    
    # Iterate to convergence
    for _ in range(100):
        P_new = P_int.copy()
        for P in P_list:
            P_new = P_new @ P
        if np.allclose(P_new, P_int, atol=1e-12):
            break
        P_int = P_new
    
    # Symmetrize and project
    P_int = (P_int + P_int.T.conj()) / 2
    
    # Verify it's a projector
    assert np.allclose(P_int @ P_int, P_int, atol=1e-10)
    assert np.allclose(P_int.T.conj(), P_int, atol=1e-10)
    
    return P_int, P_list


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SYMMETRY OPERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def build_global_X():
    """Global X^{⊗8} operator."""
    dim = 2 ** N_EDGES
    U = np.zeros((dim, dim), dtype=complex)
    for state in range(dim):
        flipped = state ^ ((1 << N_EDGES) - 1)
        U[flipped, state] = 1.0
    return U


def build_plaquette_CZ():
    """
    CZ operators on plaquettes.
    For L=2, there are 4 plaquettes. Each plaquette is a square of 4 edges.
    CZ on a plaquette: apply CZ to pairs of opposite edges? Or adjacent?
    
    For the square lattice, a natural choice is CZ on the edges of each plaquette.
    But this needs careful definition since edges are shared.
    
    Let's define: for each plaquette, apply CZ to the 4 edges forming its boundary.
    This is analogous to the T35a plaquette CZ.
    """
    # Plaquettes (each is a square of 4 edges):
    # p00: h00, v00, h10, v10  (bottom-left)
    # p10: h10, v01, h00, v11  (bottom-right)
    # p01: h01, v10, h11, v00  (top-left)
    # p11: h11, v11, h01, v01  (top-right)
    
    # Actually, for L=2 periodic, the plaquettes are:
    plaquettes = [
        [0, 4, 1, 5],   # bottom-left (h00, v00, h10, v10)
        [1, 6, 0, 7],   # bottom-right (h10, v01, h00, v11)
        [2, 5, 3, 4],   # top-left (h01, v10, h11, v00)
        [3, 7, 2, 6],   # top-right (h11, v11, h01, v01)
    ]
    
    dim = 2 ** N_EDGES
    UCZ = np.eye(dim, dtype=complex)
    
    for p_edges in plaquettes:
        # Apply CZ to all pairs in the plaquette
        for i in range(4):
            for j in range(i+1, 4):
                e1, e2 = p_edges[i], p_edges[j]
                # CZ on edges e1, e2
                CZ_op = np.eye(dim, dtype=complex)
                for state in range(dim):
                    b1 = (state >> (N_EDGES - 1 - e1)) & 1
                    b2 = (state >> (N_EDGES - 1 - e2)) & 1
                    if b1 and b2:
                        CZ_op[state, state] = -1
                UCZ = UCZ @ CZ_op
    
    return UCZ


def build_candidate_U():
    """Build U = X^{⊗8} · UCZ (global)."""
    UX = build_global_X()
    UCZ = build_plaquette_CZ()
    return UX @ UCZ


# ═══════════════════════════════════════════════════════════════════════════════
# 4. GATE 1 TEST
# ═══════════════════════════════════════════════════════════════════════════════

def run_gate1_test():
    """Run the Gate 1 intertwiner test."""
    print("=" * 70)
    print("T35b Gate 1: Four-Valent Square-Lattice Intertwiner Test")
    print("=" * 70)
    print(f"Cluster: L=2 periodic square lattice")
    print(f"Vertices: {N_VERTICES}, Edges (qubits): {N_EDGES}")
    print(f"Hilbert space dimension: {2**N_EDGES}")
    print()
    
    # Build vertex projector
    print("Building 4-valent singlet projector P_v...")
    Pv = build_vertex_projector()
    print(f"  P_v dimension: 16x16")
    print(f"  P_v trace: {np.trace(Pv):.1f} (expected: 2.0)")
    print()
    
    # Build global projector
    print("Building global intertwiner projector P_int...")
    P_int, P_list = build_global_projector(Pv)
    dim_int = int(round(np.trace(P_int).real))
    print(f"  P_int trace: {np.trace(P_int):.1f}")
    print(f"  Intertwiner subspace dimension: {dim_int}")
    print()
    
    # Test individual vertex projectors
    print("Testing vertex projector commutators...")
    for i in range(N_VERTICES):
        for j in range(i+1, N_VERTICES):
            comm = P_list[i] @ P_list[j] - P_list[j] @ P_list[i]
            norm = np.linalg.norm(comm)
            print(f"  ||[P_{i}, P_{j}]|| = {norm:.6f}")
    print()
    
    # Build symmetry operator
    print("Building candidate symmetry U = X^{⊗8} · UCZ...")
    U = build_candidate_U()
    
    # Test U^2 = I
    U2 = U @ U
    print(f"  ||U^2 - I|| = {np.linalg.norm(U2 - np.eye(2**N_EDGES)):.6f}")
    print()
    
    # Test 1: Does U preserve the intertwiner subspace?
    print("Test 1: U acting on intertwiner subspace")
    M = P_int @ U @ P_int
    
    # Compute eigenvalues of M restricted to intertwiner subspace
    # Extract the dim_int x dim_int matrix
    idx = np.where(np.diag(P_int) > 0.5)[0]
    if len(idx) != dim_int:
        # Use SVD to find the range
        _, s, Vh = np.linalg.svd(P_int)
        idx = np.where(s > 0.5)[0]
        basis = Vh[idx, :].T.conj()
    else:
        basis = np.eye(2**N_EDGES, dtype=complex)[:, idx]
    
    M_restricted = basis.T.conj() @ M @ basis
    eigs = np.linalg.eigvalsh(M_restricted)
    
    print(f"  Eigenvalues of P_int U P_int (restricted):")
    for ev in sorted(eigs):
        print(f"    {ev:+.6f}")
    print()
    
    # Test 2: Leakage
    print("Test 2: Leakage out of intertwiner subspace")
    L = (np.eye(2**N_EDGES) - P_int) @ U @ P_int
    leakage_norm = np.linalg.norm(L)
    print(f"  ||(I - P_int) U P_int|| = {leakage_norm:.6f}")
    if leakage_norm < 1e-10:
        print("  → U PRESERVES the intertwiner subspace")
    else:
        print("  → U LEAKS out of the intertwiner subspace")
    print()
    
    # Test 3: Commutator
    print("Test 3: Commutator [U, P_int]")
    comm = U @ P_int - P_int @ U
    comm_norm = np.linalg.norm(comm)
    print(f"  ||[U, P_int]|| = {comm_norm:.6f}")
    if comm_norm < 1e-10:
        print("  → [U, P_int] = 0: U preserves intertwiner subspace exactly")
    else:
        print("  → [U, P_int] ≠ 0: U does not commute with intertwiner projector")
    print()
    
    # Test 4: Does U have +1 eigenvalue on intertwiner subspace?
    print("Test 4: U eigenvalues on intertwiner subspace")
    U_restricted = basis.T.conj() @ U @ basis
    eigs_U = np.linalg.eigvalsh(U_restricted)
    print(f"  Eigenvalues of U (restricted):")
    for ev in sorted(eigs_U):
        print(f"    {ev:+.6f}")
    
    plus1_count = sum(1 for ev in eigs_U if abs(ev - 1) < 1e-10)
    minus1_count = sum(1 for ev in eigs_U if abs(ev + 1) < 1e-10)
    print(f"  +1 eigenvalues: {plus1_count}")
    print(f"  -1 eigenvalues: {minus1_count}")
    print()
    
    # Test 5: Compare with U = X^{⊗8} alone (no CZ)
    print("Test 5: U_X = X^{⊗8} alone (no CZ)")
    UX = build_global_X()
    L_X = (np.eye(2**N_EDGES) - P_int) @ UX @ P_int
    comm_X = UX @ P_int - P_int @ UX
    print(f"  ||(I - P_int) U_X P_int|| = {np.linalg.norm(L_X):.6f}")
    print(f"  ||[U_X, P_int]|| = {np.linalg.norm(comm_X):.6f}")
    
    U_X_restricted = basis.T.conj() @ UX @ basis
    eigs_UX = np.linalg.eigvalsh(U_X_restricted)
    print(f"  U_X eigenvalue on intertwiner: {eigs_UX[0]:+.6f}")
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    if leakage_norm < 1e-10 and plus1_count > 0:
        print("PASS: U preserves intertwiner subspace and has +1 eigenvalue")
    elif leakage_norm < 1e-10:
        print("PARTIAL: U preserves intertwiner subspace but no +1 eigenvalue")
    else:
        print("OBSTRUCTION: U leaks from intertwiner subspace")
    print()
    
    return {
        "dim_int": dim_int,
        "leakage_norm": leakage_norm,
        "comm_norm": comm_norm,
        "plus1_count": plus1_count,
        "minus1_count": minus1_count,
    }


if __name__ == "__main__":
    result = run_gate1_test()
