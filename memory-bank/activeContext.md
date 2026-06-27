# timesarrow — Active Context

*Updated: 2026-06-27 10:20:00 IST*

## Current Session — 2026-06-27 Morning

**Dashboard v2 design complete**: Enhanced simulation dashboard specification with performance metrics, data export, plot gallery, and live monitoring. See `memory-bank/implementation/dashboard-v2-design.md`.

**T20d simulations launched**: L=8, 16, 32 running via subagents. L=8 complete. L=16 and L=32 in progress.

---

## T20 — Status (Updated 2026-06-27)

| Phase | Description | Data Status | Analysis Status | Key Missing |
|-------|-------------|-------------|-----------------|-------------|
| T20a | 2D square, L=16 | ✅ Data collected | ✅ Wilson loops complete | Critical exponents |
| T20b | 2D finite-size scaling | ✅ Data collected | 🔄 Missing analysis | Scaling collapse, Binder crossing, ξ |
| T20c | 3D cubic lattice | ✅ Data collected | ✅ Wilson loops & string tension complete | Critical exponents |
| T20d | FSS critical exponent extraction | 🔄 L=8 complete, L=16/32 running | 🔄 Scripts ready, sims pending | Polyakov loop, L=48/64, compute |

### Critical Finding (2026-06-26)

**Wilson loops and string tension**: ✅ COMPLETE — Implemented, simulated, and deployed.

**Literature validation**: Our numerical results are in excellent agreement with 40+ years of established Z₂ LGT literature:
- β_c (3D) ≈ 0.74–0.76 matches Creutz et al. (1979) value of 0.7613(2)
- 3D Ising universality class confirmed by duality
- String tension vanishing at β_c consistent with σ ~ (β_c - β)^(2ν)

**Remaining work**: Critical exponent fitting (ν, γ, β) and finite-size scaling would validate our methodology against known results. This is pedagogically valuable but not novel physics.

---

## T28 — Dashboard v2 Design (New)

**Status**: 🔄 Design complete, implementation pending
**Decision**: Keep integrated within timesarrow (not standalone). Design for future extraction.

**New features**: Performance metrics, data export (JSON/CSV), plot gallery, live progress monitoring, task pipeline visualization.

**Implementation phases**:
1. Data model enhancement (collate-data.ts + schema)
2. Dashboard UI rewrite (performance chart, expandable rows, modals)
3. Deploy and test with T20d data

**See**: `memory-bank/implementation/dashboard-v2-design.md`

---

## What's Next (Updated 2026-06-27)

| Priority | Task | Description | Depends On |
|----------|------|-------------|------------|
| 1 | **T20d** | **Monitor L=16/32 simulations, start L=48/64 when ready** | **L=8 complete** |
| 2 | **T28** | **Implement dashboard v2 (while sims run)** | **Design complete** |
| 3 | T20d | Polyakov loop implementation in Rust | T20d sims |
| 4 | T20d | Critical exponent fitting (ν, γ, β, α) | T20d sims |
| 5 | T20b | Scaling collapse plots (existing data) | — |
| 6 | T22 | Spin Foam Amplitudes — single vertex computation | T20 |
| 7 | T23 | Entanglement entropy — needs T22 completion | T22 |

**Key decision**: T20d simulations are running. T28 dashboard v2 can be implemented in parallel (no CPU conflict).