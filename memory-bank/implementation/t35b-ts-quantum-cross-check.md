# T35b Cross-Check: ts-quantum CZX Implementation

*Date: 2026-07-21*
*Purpose: Compare ts-quantum CZX code with T35b Gate 1 results*

## ts-quantum Source Files

- `src/models/czx.ts` — CZX symmetry operator + intertwiner audit
- `__tests__/czx.test.ts` — Vitest unit tests
- `memory-bank/implementation-details/czx-intertwiner-audit.md` — Scope notes

## What ts-quantum Implements

### 1. `createCzxOnSiteSymmetry()`

Builds the 4-qubit on-site operator:
$$U_{\mathrm{CZX}} = X_1 X_2 X_3 X_4 \, CZ_{12} CZ_{23} CZ_{34} CZ_{41}$$

- Qubit 0 is the most significant bit
- Matrix is 16×16, unitary
- Verified: $U_{\mathrm{CZX}}^2 = I$ ✓

### 2. `auditCzxOnIntertwinerSubspace()`

Applies $U_{\mathrm{CZX}}$ to each basis vector of a 4-spin-½ SU(2) intertwiner space and measures:
- Projection norm back into intertwiner subspace
- Leakage norm (= 1 − projection²)

## Test Result

```typescript
const audit = auditCzxOnIntertwinerSubspace(getFourSpinHalfBasis());
expect(audit.subspaceDimension).toBe(2);
expect(audit.preservesIntertwinerSubspace).toBe(false);  // ← LEAKS
expect(audit.squaredLeakageNorms.some(norm => norm > 1e-10)).toBe(true);
```

**Result: The literal on-site 4-qubit CZX LEAKS from the intertwiner subspace.**

## Comparison with T35b Gate 1

| | ts-quantum (local) | T35b Gate 1 (global) |
|---|---|---|
| Qubit placement | Sites (4 qubits) | Edges (8 qubits) |
| Operator scope | Single 4-qubit $U_{\mathrm{CZX}}$ | Global $U = X^{\otimes 8} \cdot U_{CZ}$ |
| Intertwiner space | 2-dimensional singlet | 1-dimensional intersection |
| Leakage | **> 0** (FAILS) | **0** (PASSES) |
| Commutator $[U, P_{\mathrm{int}}]$ | Not tested | **0** ✓ |

## Interpretation

1. **ts-quantum confirms the T35a/T35b lesson**: The on-site 4-qubit $U_{\mathrm{CZX}}$ is not a valid symmetry of the intertwiner subspace. This matches the session notes finding: "a single-site $U_{CZX,s}$ alone does not preserve the state."

2. **The global/dressed operator works**: T35b Gate 1 shows that a global operator on edge-qubits preserves the intertwiner subspace. The dressing (CZ factors + global product structure) is essential.

3. **Different Hilbert spaces**: ts-quantum tests a single 4-qubit vertex. T35b tests 4 vertices with shared edge-qubits. The non-commuting vertex projectors in T35b create a more constrained (1-dimensional) intertwiner subspace.

4. **Scope limitation**: The ts-quantum audit is explicitly labeled as "not a claim that the full microscopic model has been constructed." It is a local sanity check, not a many-vertex construction.

## Conclusion

The cross-check is **consistent**:
- ts-quantum: Local on-site CZX leaks from intertwiner subspace ✗
- T35b: Global dressed operator preserves intertwiner subspace ✓

Both agree that the symmetry is **global, not on-site**. The CZX SPT mechanism requires the dressed product structure.

## Action Items

- [ ] ts-quantum could add a multi-vertex test (like T35b Gate 1) to verify global invariance
- [ ] T35b could test whether the intertwiner subspace grows for $L=3, 4$ to better probe the CZ structure
