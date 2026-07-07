#### 02:55:00 IST - T32: Calibrate T25 spectral pairing interpretation

**Files Modified:**
- `memory-bank/tasks/T25.md`
- `memory-bank/implementation-details/volume-operator-extension.md`
- `memory-bank/implementation-details/T25-volume-operator-extension.md`
- `memory-bank/tasks/T32.md`
- `memory-bank/progress.md`
- `numerics/docs/tasks/t25-volume-operator.qmd`
- `numerics/docs/tasks/t25-volume-operator.html`
- `numerics/docs/_site/tasks/t25-volume-operator.qmd`
- `numerics/docs/_site/tasks/t25-volume-operator.html`

**Key Wording Changes (before → after):**
- "Z₂ structure" / "Z₂ sign-flip structure" → "algebraic spectral reflection symmetry"
- "time-orientation flip symmetry" → "operator's algebraic symmetry under sign reversal"
- "key numerical diagnostic for the paper's central claim about time-orientation symmetry" → "numerical diagnostic for algebraic spectral reflection symmetry of the volume operator. It does not, by itself, establish a physical dynamical Z₂ time-orientation symmetry"
- "Strong support for Z₂ time-orientation as fundamental" → "algebraic spectral reflection symmetry of the volume operator" + note that physical demonstration requires explicit symmetry generator
- "Tests whether Z₂ structure requires uniform j" → "Tests whether algebraic ± spectral reflection symmetry requires uniform j"
- Table column "Z₂ Structure" → "Algebraic Spectral Symmetry" with "Confirmed (spectral reflection)" status

**Physical-Transformation Test:**
- **Deferred** to future work (T33 or later).
- T25.md now explicitly states: "A physical Z₂ dynamical symmetry would require an explicit operator τ acting on the relevant states that (i) commutes with the Hamiltonian, (ii) satisfies τ² = 1, and (iii) maps +q eigenstates to -q eigenstates. Constructing and testing such an operator is deferred to future work (T33 or later)."
- Rationale: The algebraic pairing is established; demonstrating that a physical Z₂ operator commutes with the Hamiltonian and acts as q→-q on eigenstates requires constructing the explicit symmetry generator, which is beyond T25's scope.

**Raw Data Status:**
- All computed spectral data, eigenvalues, and test results remain intact and valid.
- Only the interpretation and surrounding language has been calibrated.

**T32 Acceptance Criterion:**
- T32 checkbox for T25 updated from `[ ]` to `[x]`.
