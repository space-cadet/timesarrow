# T35a: CZX Microscopic Construction Audit

*Created: 2026-07-18*
*Status: 🔄 Local operator checkpoint complete*

## Scope

This audit uses the local `ts-quantum` library to distinguish the literal CZX on-site symmetry from the structural correspondence between the CZX code qubit and the LQG intertwiner qubit. It does not claim a 3D CZX parent Hamiltonian.

## Local Hilbert Space and Symmetry

Each four-valent vertex uses four qubits, so its local Hilbert space has dimension $2^4=16$. The tested on-site CZX symmetry is

$$
U_{\mathrm{CZX}} = X_1 X_2 X_3 X_4\,CZ_{12}CZ_{23}CZ_{34}CZ_{41}.
$$

The implementation is in `/Users/deepak/code/ts-quantum/src/models/czx.ts`; the reusable two-qubit controlled-Z primitive is in `src/operators/gates.ts`.

## Verified Result

Focused Vitest checks verify that $U_{\mathrm{CZX}}^2=I$ on the full four-qubit Hilbert space. Applying it to the orthonormal basis returned by `getFourSpinHalfBasis()` produces nonzero norm outside the two-dimensional $SU(2)$ singlet subspace.

Therefore the literal CZX operator does not preserve the LQG intertwiner subspace. This is an expected negative result for the literal-operator claim, not a failure of the implementation. The defensible statement remains a structural identification of two effective $Z_2$ qubits.

## Next Gate

Before attempting any 3D construction, define a candidate many-vertex state on a minimal decorated complex and test, in order:

1. Global symmetry preservation.
2. Nonzero intertwiner projection.
3. Whether a local parent Hamiltonian can be derived from that state.

No toric-code gauge projector may be used as a substitute for this construction.
