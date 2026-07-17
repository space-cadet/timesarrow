# Session: T33a/T35a Foundation and Local CZX Audit

*Date: 2026-07-18 00:35 IST*

## Scope

- Validate and document the corrected T33a cell-complex 2-skeleton foundation.
- Use `ts-quantum` for a narrow T35a audit of the literal on-site four-qubit CZX candidate.

## Results

- The corrected cell-complex implementation passes its Rust test suite.
- The CZX candidate satisfies $U_{\mathrm{CZX}}^2=I$ on the full 16-dimensional qubit Hilbert space.
- Its action has nonzero leakage from the four-spin-half SU(2) singlet/intertwiner subspace.

## Interpretation and Next Step

This rules out treating the literal local operator as a complete microscopic realization on that constrained local space. It does not resolve the many-vertex construction. T35a next needs a minimal candidate state and an explicit symmetry-action check.

## Verification

- `rustup run 1.92.0-aarch64-apple-darwin cargo test` in `rust-lattice`: passed, 45 tests.
- `pnpm test` and `pnpm build` in `ts-quantum`: passed, 492 tests and production build.
