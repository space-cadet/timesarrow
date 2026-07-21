"""
T35a Thread 2: Parent Hamiltonian Construction (Stabilizer Version)
Date: 2026-07-21

Parent Hamiltonian for CZX state using stabilizer projectors.
For GHZ state on 4 qubits, stabilizers are: XXXX, ZZII, IZZI, IIZZ
H_p = (1/2) * Σ (I - S_i) for stabilizer generators S_i
"""

import numpy as np
from itertools import product

# ─── Pauli operators ───
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron4(a, b, c, d):
    """Kronecker product of four 2×2 matrices."""
    return np.kron(np.kron(a, b), np.kron(c, d))


N = 16  # total qubits for 2×2 torus


def qidx(p, s):
    """Flat index for qubit (plaquette p, site s)."""
    return p * 4 + s


def apply_pauli_string(state, paulis, qubits):
    """
    Apply a Pauli string to a state vector.
    paulis: list of 'X', 'Z', 'I'
    qubits: list of qubit indices
    """
    result = np.zeros_like(state)
    
    for idx in range(len(state)):
        if abs(state[idx]) < 1e-15:
            continue
        
        new_idx = idx
        phase = 1
        
        for p, q in zip(paulis, qubits):
            bit = (idx >> (N - 1 - q)) & 1
            if p == 'X':
                new_idx ^= (1 << (N - 1 - q))
            elif p == 'Z':
                if bit == 1:
                    phase *= -1
            # 'I' does nothing
        
        result[new_idx] += phase * state[idx]
    
    return result


def build_ghz_parent_hamiltonian_4qubit():
    """
    Parent Hamiltonian for 4-qubit GHZ state.
    H = (1/2) * [(I - XXXX) + (I - ZZII) + (I - IZZI) + (I - IIZZ)]
    """
    I16 = np.eye(16, dtype=complex)
    XXXX = kron4(X, X, X, X)
    ZZII = kron4(Z, Z, I2, I2)
    IZZI = kron4(I2, Z, Z, I2)
    IIZZ = kron4(I2, I2, Z, Z)
    
    H = 0.5 * (4 * I16 - XXXX - ZZII - IZZI - IIZZ)
    return H


def build_plaquette_hamiltonian(state, p):
    """
    Apply plaquette Hamiltonian h_p to a state vector.
    h_p = (1/2) * [(I - XXXX) + (I - ZZII) + (I - IZZI) + (I - IIZZ)]
    acting on qubits [qidx(p,0), qidx(p,1), qidx(p,2), qidx(p,3)]
    """
    qubits = [qidx(p, s) for s in range(4)]
    
    # h_p = 2I - (1/2)(XXXX + ZZII + IZZI + IIZZ)
    result = 2 * state.copy()
    
    for paulis in [['X', 'X', 'X', 'X'], ['Z', 'Z', 'I', 'I'], 
                   ['I', 'Z', 'Z', 'I'], ['I', 'I', 'Z', 'Z']]:
        result -= 0.5 * apply_pauli_string(state, paulis, qubits)
    
    return result


def apply_parent_hamiltonian(state):
    """Apply H = Σ_p h_p to a state vector."""
    result = np.zeros_like(state)
    for p in range(4):
        result += build_plaquette_hamiltonian(state, p)
    return result


def verify_parent_hamiltonian():
    """Verify properties of the parent Hamiltonian."""
    print("=" * 70)
    print("T35a Thread 2: Parent Hamiltonian (Stabilizer Version)")
    print("=" * 70)
    print(f"System: 2×2 torus, {N} qubits")
    print("H = Σ_p (1/2)[(I-XXXX) + (I-ZZII) + (I-IZZI) + (I-IIZZ)]_p")
    print()
    
    # Build the CZX ground state
    amp = {}
    for b in product([0, 1], repeat=4):
        st = 0
        for p in range(4):
            for s in range(4):
                st |= b[p] << (N - 1 - qidx(p, s))
        amp[st] = 1.0 / 4.0
    
    psi_0 = np.zeros(2**N, dtype=complex)
    for st, a in amp.items():
        psi_0[st] = a
    
    norm_psi = np.linalg.norm(psi_0)
    print(f"Ground state norm: {norm_psi:.6f}")
    print()
    
    # Check 1: H|psi_0⟩ = 0
    print("Check 1: CZX state is ground state?")
    H_psi = apply_parent_hamiltonian(psi_0)
    norm_H_psi = np.linalg.norm(H_psi)
    print(f"  ||H|ψ_0⟩|| = {norm_H_psi:.2e}")
    print(f"  Result: {'PASS' if norm_H_psi < 1e-10 else 'FAIL'}")
    print()
    
    # Check 2: Ground state energy = 0
    print("Check 2: Ground state energy?")
    E0 = np.vdot(psi_0, apply_parent_hamiltonian(psi_0)).real
    print(f"  ⟨ψ_0|H|ψ_0⟩ = {E0:.10f}")
    print(f"  Result: {'PASS (E_0 = 0)' if abs(E0) < 1e-10 else 'FAIL'}")
    print()
    
    # Check 3: Local terms commute?
    print("Check 3: Do local terms commute?")
    rng = np.random.default_rng(42)
    test_state = rng.random(2**N) + 1j * rng.random(2**N)
    test_state = test_state / np.linalg.norm(test_state)
    
    all_commute = True
    for i in range(4):
        for j in range(i+1, 4):
            h_i_h_j = build_plaquette_hamiltonian(
                build_plaquette_hamiltonian(test_state, j), i)
            h_j_h_i = build_plaquette_hamiltonian(
                build_plaquette_hamiltonian(test_state, i), j)
            diff = np.linalg.norm(h_i_h_j - h_j_h_i)
            if diff > 1e-10:
                print(f"  ||[h_{i}, h_{j}]|| = {diff:.6f} — DO NOT COMMUTE")
                all_commute = False
            else:
                print(f"  ||[h_{i}, h_{j}]|| = {diff:.2e} — commute")
    print(f"  Result: {'PASS' if all_commute else 'FAIL'}")
    print()
    
    # Check 4: H is positive semidefinite
    print("Check 4: H is positive semidefinite?")
    
    # Build full H matrix for verification
    print("  Building full H matrix (this may take a moment)...")
    H_full = np.zeros((2**N, 2**N), dtype=complex)
    for i in range(2**N):
        psi_i = np.zeros(2**N, dtype=complex)
        psi_i[i] = 1.0
        H_full[:, i] = apply_parent_hamiltonian(psi_i)
    
    eigs = np.linalg.eigvalsh(H_full)
    min_eig = np.min(eigs)
    print(f"  Minimum eigenvalue: {min_eig:.10f}")
    print(f"  Result: {'PASS' if min_eig > -1e-10 else 'FAIL'}")
    print()
    
    # Check 5: Unique ground state
    print("Check 5: Unique ground state?")
    zero_eigs = np.sum(np.abs(eigs) < 1e-10)
    print(f"  Number of zero eigenvalues: {zero_eigs}")
    print(f"  Result: {'PASS (unique)' if zero_eigs == 1 else 'FAIL (degenerate)'}")
    print()
    
    # Check 6: Gap
    print("Check 6: Spectral gap?")
    sorted_eigs = np.sort(eigs)
    if zero_eigs >= 1 and zero_eigs < len(sorted_eigs):
        gap = sorted_eigs[zero_eigs]
    else:
        gap = sorted_eigs[1] - sorted_eigs[0]
    print(f"  Gap to first excited state: {gap:.6f}")
    print(f"  Result: {'PASS (gapped)' if gap > 1e-10 else 'FAIL (gapless)'}")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    checks = [
        ("Ground state (H|ψ⟩ = 0)", norm_H_psi < 1e-10),
        ("Ground state energy = 0", abs(E0) < 1e-10),
        ("Terms commute", all_commute),
        ("Positive semidefinite", min_eig > -1e-10),
        ("Unique ground state", zero_eigs == 1),
        ("Gapped", gap > 1e-10),
    ]
    
    all_pass = all(passed for _, passed in checks)
    for name, passed in checks:
        print(f"  {name}: {'✓' if passed else '✗'}")
    print()
    print(f"Overall: {'PASS (valid parent Hamiltonian)' if all_pass else 'FAIL'}")
    
    return {
        "ground_state": norm_H_psi < 1e-10,
        "energy_zero": abs(E0) < 1e-10,
        "commute": all_commute,
        "positive": min_eig > -1e-10,
        "unique": zero_eigs == 1,
        "gapped": gap > 1e-10,
    }


if __name__ == "__main__":
    results = verify_parent_hamiltonian()
