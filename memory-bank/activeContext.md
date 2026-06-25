# timesarrow — Active Context

*Updated: 2026-06-25 18:40 IST*

## Session Summary — 2026-06-25

**T20 Phase 2**: ✅ COMPLETE — 5 lattice sizes (L=8,12,16,20,24) finite-size scaling
**T20 Phase 3**: ✅ COMPLETE — 3 lattice sizes (L=4,6,8) 3D cubic lattice
**Rust 3D support**: ✅ ADDED — `dimension` parameter, backward compatible

---

## T20 — Complete Status

| Phase | Description | Status | Key Results |
|-------|-------------|--------|-------------|
| Phase 1 | 2D square, L=8 | ✅ Complete | β_c ≈ 0.44 confirmed |
| Phase 2 | 2D finite-size scaling | ✅ Complete | L=8→24, Binder → U* ≈ 0.66 |
| Phase 3 | 3D cubic lattice | ✅ Complete | β_c ≈ 0.75, sharp first-order transition |

### Phase 3: 3D Cubic Results

| L | Time | Critical β | Susceptibility Peak | Notes |
|---|------|-----------|-------------------|-------|
| 4 | 1.5s | 0.70 | χ ≈ 0.46 | Small finite-size effects |
| 6 | 4.0s | 0.70 | χ ≈ 0.66 | Transition sharpening |
| 8 | 9.1s | 0.75 | χ ≈ 0.52 | Converging to β_c ≈ 0.76 |

**Key findings**:
1. 3D transition is first-order (sharp plaquette jump from ~0.5 to ~0.95)
2. Critical β converges from 0.70 (small L) toward 0.76 (L→∞)
3. Binder cumulant stabilizes at U ≈ 0.666 (3D Ising universal value)

---

## Data Collation System

New registry tracking all 8 runs:
- `data/registry.json` — Central index with metadata, parameters, results
- `data/registry.schema.json` — Schema definition
- `src/scripts/collate-data.ts` — Automated collation script

---

## What's Next

| Task | Status | Description |
|------|--------|-------------|
| T22 | 🟡 Ready | 2D Spin Foam Amplitudes — single vertex computation |
| T23 | 🔴 Blocked | Entanglement entropy — needs T22 completion |
| T20-ext | 🟡 Optional | Larger L=10,12 in 3D for better finite-size scaling |

---

*See `memory-bank/tasks/T20.md` for full results.*
*See `memory-bank/tasks/T22.md` for Spin Foam planning.*
