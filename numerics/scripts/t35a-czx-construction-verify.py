"""
T35a: CZX State Construction — Exact Numerical Verification
Date: 2026-07-18

Explicit construction of the CZX SPT state on:
1. Single plaquette (4 qubits)
2. 2×2 torus (16 qubits, 4 sites × 4 plaquettes)

Key finding: The GLOBAL operator ∏_s U_CZX,s is the symmetry.
A single-site U_CZX,s alone does NOT preserve the state.
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


def CZ(i, j, n=4):
    """
    Controlled-Z between qubits i and j (1-indexed) in an n-qubit system.
    Returns a 2^n × 2^n diagonal matrix.
    """
    M = np.eye(2**n, dtype=complex)
    for s in range(2**n):
        b = [(s >> (n - 1 - k)) & 1 for k in range(n)]
        if b[i - 1] and b[j - 1]:
            M[s, s] = -1
    return M


# ═══════════════════════════════════════════════════════════════════════════════
# 1. SINGLE PLAQUETTE (4 qubits)
# ═══════════════════════════════════════════════════════════════════════════════

def build_single_plaquette_czx():
    """Build U_CZX = X^{⊗4} · CZ_{12}CZ_{23}CZ_{34}CZ_{41} on 4 qubits."""
    UX = kron4(X, X, X, X)
    UCZ = CZ(1, 2, 4) @ CZ(2, 3, 4) @ CZ(3, 4, 4) @ CZ(4, 1, 4)
    return UX @ UCZ


def verify_single_plaquette():
    """Verify the single-plaquette CZX state."""
    U_CZX = build_single_plaquette_czx()

    # GHZ-like state
    psi = np.zeros(16, dtype=complex)
    psi[0] = psi[15] = 1.0 / np.sqrt(2)

    # Checks
    overlap = np.vdot(psi, U_CZX @ psi)
    diff_norm = np.linalg.norm(U_CZX @ psi - psi)
    hermitian = np.allclose(U_CZX, U_CZX.T.conj())
    squares_to_identity = np.allclose(U_CZX @ U_CZX, np.eye(16, dtype=complex))

    print("═" * 60)
    print("SINGLE PLAQUETTE (4 qubits)")
    print("═" * 60)
    print(f"⟨ψ|U_CZX|ψ⟩       = {overlap.real:.6f} (expected: 1)")
    print(f"‖U_CZX|ψ⟩ − |ψ⟩‖  = {diff_norm:.2e} (expected: 0)")
    print(f"U_CZX Hermitian?   = {hermitian}")
    print(f"U_CZX² = I?        = {squares_to_identity}")

    # Check individual components
    UX = kron4(X, X, X, X)
    UCZ = CZ(1, 2, 4) @ CZ(2, 3, 4) @ CZ(3, 4, 4) @ CZ(4, 1, 4)

    overlap_X = np.vdot(psi, UX @ psi)
    overlap_CZ = np.vdot(psi, UCZ @ psi)
    print(f"⟨ψ|U_X|ψ⟩          = {overlap_X.real:.6f}")
    print(f"⟨ψ|U_CZ|ψ⟩         = {overlap_CZ.real:.6f}")

    return {
        "overlap": overlap,
        "diff_norm": diff_norm,
        "hermitian": hermitian,
        "squares_to_identity": squares_to_identity,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 2. OPEN PLAQUETTE (3 edges, dangling ends)
# ═══════════════════════════════════════════════════════════════════════════════

def verify_open_plaquette():
    """
    Open plaquette: 3 edges, so the |1111⟩ component gets phase (−1)³ = −1
    while |0000⟩ gets (+1). The state is NOT invariant.
    """
    psi = np.zeros(16, dtype=complex)
    psi[0] = psi[15] = 1.0 / np.sqrt(2)

    # For open boundary, one CZ is missing. Simulate by applying only 3 CZs:
    UCZ_open = CZ(1, 2, 4) @ CZ(2, 3, 4) @ CZ(3, 4, 4)  # missing CZ(4,1)
    UX = kron4(X, X, X, X)
    U_open = UX @ UCZ_open

    psi_prime = U_open @ psi
    overlap = np.vdot(psi, psi_prime)
    diff_norm = np.linalg.norm(psi_prime - psi)

    print()
    print("═" * 60)
    print("OPEN PLAQUETTE (3 edges, dangling)")
    print("═" * 60)
    print(f"⟨ψ|U_open|ψ⟩       = {overlap.real:.6f} (expected: 0)")
    print(f"‖U_open|ψ⟩ − |ψ⟩‖  = {diff_norm:.6f} (expected: √2 ≈ 1.414)")
    print()
    print("The |1111⟩ component picks up (−1)³ = −1 relative to |0000⟩.")
    print("This is the boundary signature of the non-on-site MPUO.")

    return {"overlap": overlap, "diff_norm": diff_norm}


# ═══════════════════════════════════════════════════════════════════════════════
# 3. FOUR-SITE VERSION (2×2 torus, 16 qubits)
# ═══════════════════════════════════════════════════════════════════════════════

N = 16  # total qubits: 4 plaquettes × 4 spins each


def qidx(p, s):
    """Flat index for qubit (plaquette p, site s)."""
    return p * 4 + s


def bits_of(state):
    """Extract N bits from an integer state."""
    return np.array([(state >> (N - 1 - q)) & 1 for q in range(N)])


def build_4site_state():
    """
    Build the 2×2 torus state:
    |Ψ⟩ = ⊗_{p=0}³ (|0000⟩_p + |1111⟩_p) / √2
    """
    amp = {}
    for b in product([0, 1], repeat=4):
        st = 0
        for p in range(4):
            for s in range(4):
                st |= b[p] << (N - 1 - qidx(p, s))
        amp[st] = 1.0 / 4.0  # normalization: 4 components × (1/√2)² = 1
    return amp


def apply_global_U(state):
    """
    Apply the GLOBAL CZX operator:
    U = ∏_s [ X_s · ∏_p CZ_{p,p+1}(s) ]

    On the 2×2 torus, each site s has CZ between plaquettes p and (p+1)%4.
    """
    b = bits_of(state)
    phase = 1

    # CZ layer: for each site s, CZ across plaquette ring
    for s in range(4):
        n = sum(b[qidx(p, s)] * b[qidx((p + 1) % 4, s)] for p in range(4))
        if n % 2 == 1:
            phase *= -1

    # X layer: flip all 16 qubits
    new_state = state ^ ((1 << N) - 1)
    return phase, new_state


def apply_single_site_U(state, s_target):
    """
    Apply U_CZX to a SINGLE site s_target only.
    This should NOT preserve the state.
    """
    b = bits_of(state)
    phase = 1

    # CZ only on site s_target across plaquettes
    n = sum(b[qidx(p, s_target)] * b[qidx((p + 1) % 4, s_target)] for p in range(4))
    if n % 2 == 1:
        phase *= -1

    # X only on qubits belonging to site s_target
    new_state = state
    for p in range(4):
        new_state ^= 1 << (N - 1 - qidx(p, s_target))

    return phase, new_state


def verify_4site_torus():
    """Verify the 2×2 torus CZX state."""
    amp = build_4site_state()

    # Convert amplitude dict to dense vector
    psi = np.zeros(2**N, dtype=complex)
    for st, a in amp.items():
        psi[st] = a

    norm = np.linalg.norm(psi)
    print()
    print("═" * 60)
    print("FOUR-SITE VERSION (2×2 torus, 16 qubits)")
    print("═" * 60)
    print(f"‖ψ‖ = {norm:.6f} (expected: 1)")

    # ─── Global symmetry ───
    psi_global = np.zeros_like(psi)
    for st in range(2**N):
        if abs(psi[st]) > 1e-15:
            ph, new_st = apply_global_U(st)
            psi_global[new_st] += ph * psi[st]

    overlap_global = np.vdot(psi, psi_global)
    diff_global = np.linalg.norm(psi_global - psi)
    print(f"⟨ψ|U_global|ψ⟩     = {overlap_global.real:.6f} (expected: 1)")
    print(f"‖U_global|ψ⟩ − |ψ⟩‖ = {diff_global:.2e} (expected: 0)")

    # ─── Single-site symmetry (should fail) ───
    for s in range(4):
        psi_single = np.zeros_like(psi)
        for st in range(2**N):
            if abs(psi[st]) > 1e-15:
                ph, new_st = apply_single_site_U(st, s)
                psi_single[new_st] += ph * psi[st]

        overlap_single = np.vdot(psi, psi_single)
        diff_single = np.linalg.norm(psi_single - psi)
        print(f"⟨ψ|U_{{{s}}}|ψ⟩     = {overlap_single.real:.6f} (expected: 0)")
        print(f"‖U_{{{s}}}|ψ⟩ − |ψ⟩‖  = {diff_single:.6f} (expected: √2 ≈ 1.414)")

    # ─── Global U_X alone ───
    psi_X = np.zeros_like(psi)
    for st in range(2**N):
        if abs(psi[st]) > 1e-15:
            psi_X[st ^ ((1 << N) - 1)] = psi[st]
    overlap_X = np.vdot(psi, psi_X)
    print(f"⟨ψ|U_X^{{⊗16}}|ψ⟩    = {overlap_X.real:.6f} (expected: 1)")

    # ─── Global U_CZ alone ───
    psi_CZ = np.zeros_like(psi)
    for st in range(2**N):
        if abs(psi[st]) > 1e-15:
            b = bits_of(st)
            ph = 1
            for s in range(4):
                n = sum(b[qidx(p, s)] * b[qidx((p + 1) % 4, s)] for p in range(4))
                if n % 2 == 1:
                    ph *= -1
            psi_CZ[st] = ph * psi[st]
    overlap_CZ = np.vdot(psi, psi_CZ)
    print(f"⟨ψ|U_CZ^{{global}}|ψ⟩ = {overlap_CZ.real:.6f} (expected: 1)")

    return {
        "norm": norm,
        "overlap_global": overlap_global,
        "diff_global": diff_global,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    verify_single_plaquette()
    verify_open_plaquette()
    verify_4site_torus()
    print()
    print("═" * 60)
    print("All verifications complete.")
    print("═" * 60)
