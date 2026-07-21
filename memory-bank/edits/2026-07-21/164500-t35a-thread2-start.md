#### 16:45 IST - T35a: Parent Hamiltonian thread started, ts-quantum sparse eigensolver added

**Actions:**
- Created `numerics/scripts/t35a-thread2-parent-hamiltonian.py` — numpy stabilizer-based parent Hamiltonian construction for 16-qubit 2×2 torus
- Created `numerics/scripts/t35a-thread2-verify.ts` — ts-quantum sparse Lanczos eigensolver verification script
- Updated `package.json` to use workspace ts-quantum (file: path) for access to new sparse eigensolver

**ts-quantum changes (committed):**
- Added `src/operators/sparseEigensolver.ts` — Lanczos algorithm for extreme eigenvalues of sparse Hermitian matrices
- Updated `SparseOperator.eigenDecompose()` to use sparse solver for large matrices
- Added `__tests__/sparseEigensolver.test.ts` with 6 tests (diagonal, real symmetric, complex Hermitian)
- All 498 tests pass

**Context:** Session ended prematurely due to second context compaction. Resuming in new session.

**Files modified:**
- `memory-bank/tasks/T35a.md` — Updated open threads, added files, updated timestamp
- `memory-bank/activeContext.md` — Added Thread 2 section, updated priorities
