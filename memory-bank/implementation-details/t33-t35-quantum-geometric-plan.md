# Quantum-Geometric Numerics Plan: T33–T35

*Created: 2026-07-16*
*Last Updated: 2026-07-16*

## Summary

This document records the detailed plan for numerical work to bolster the quantum-geometric aspects of the Time's Arrow project. The plan was developed through a multi-round discussion between Sage (local OpenClaw agent), GPT 5.6 Luna (external review agent), and Deepak Vaid (author). The back-and-forth is preserved here to document how the final plan emerged from critique and revision.

---

## Original Question (2026-07-16)

> "Now what further numerical work can we do to bolster the quantum geometric aspects of the picture? Can you think of any CZX code related simulations which would be useful?"

> "The CZX code construction I use in the paper works only on a 4-valent graph. For the numerics involving the 3d behaviour, we have used six-valent graphs. Can the CZX construction be extended to the 6-valent case, or would it be better to use a 4-valent graph with a 3d topology to study the 3d case?"

---

## Round 1: Sage's Initial Proposal

Sage proposed five simulation directions:

1. **Diamond lattice Polyakov scan** — Quick control run
2. **Plaquette stabilizer correlation ⟨B_p B_{p'}⟩** — CZX topological order
3. **Defect cluster analysis** — Visual quantum geometry
4. **"Code fidelity" from ⟨B_p⟩** — One-number measure
5. **Intertwiner correlation on gauge-fixed configs** — Spin-network structure

Sage also answered the graph valence question: recommend diamond lattice (4-valent, 3D) over extending CZX to 6-valent.

---

## Round 2: Luna's Review (GPT 5.6)

Luna identified significant errors:

### Corrections Accepted

| Issue | Original | Corrected |
|-------|----------|-----------|
| Intertwiner uniqueness | "Unique" (sloppy but directionally right) | "Unique up to basis" (singlet space dim = 2 for 4-valent) |
| T33 scope | One lattice-constructor function | General cell-complex API with boundary operators |
| T33 β_c | Preselected 0.65–0.75 | Cheap coarse pilot first |
| T34 data | "Use existing T20/T31 data" | Existing data lacks link configs; need new snapshot mode |
| T34 phases | Wrong way around | Confined = winding loops; deconfined = small loops |
| T35 Hamiltonian | Naive perturbed toric code | Proper microscopic construction audit |
| T35 ED | Proposed L=4 diamond ED | Infeasible; replaced with analytic/tensor-network audit |

### Corrections Rejected (or Partially Accepted)

Luna's framing was sometimes overly pedantic. For example:
- The 4-valent singlet space being "not unique" was technically true (dim=2) but missed the point: it's still the *minimal* case, which is what matters for CZX.
- Some proposed observables were dismissed as "not CZX diagnostics" when they were never claimed to be — they were geometric characterizations.

Deepak's verdict: "I don't deduct marks for sloppiness. If I did I would have to fail myself first!"

---

## Round 3: Sage's Revised Plan (with Luna's Corrections)

The plan was reorganized into:

- **T33a:** General 4-valent cell-complex API (infrastructure)
- **T33b:** Diamond lattice Polyakov scan (control physics)
- **T34a:** Snapshot output mode (data infrastructure)
- **T34b:** Flux loop analysis (geometric characterization)
- **T35a:** Microscopic construction audit (genuinely quantum step)

---

## Round 4: Luna's Final Polish

Three remaining technical corrections:

1. **T33a must accept a valid oriented 3D cell complex, not merely "an arbitrary 4-valent graph."** Valence alone does not determine plaquettes or 3-cells. Use incidence/boundary matrices over ℤ₂ as ground truth: ∂₁∂₂ = 0, ∂₂∂₃ = 0. For periodic 3-torus, verify homology ranks (H₀=1, H₁=3).

2. **T33b Polyakov loop:** "Non-contractible" is not enough — must designate a compact Euclidean-time cycle/foliation, or measure named winding Wilson loops.

3. **T35a corrected order:**
   1. Start from four vertex qubits, write CZX-inspired local symmetry with controlled-Z structure
   2. Define candidate state on chosen 4-valent complex
   3. Apply intended SU(2)/intertwiner projection, test nonzero and symmetry-preserving
   4. Derive candidate local parent terms from the state
   5. Then decide whether SPT diagnostic exists

Plus snapshot metadata refinements: include action convention, thermalization/separation interval, cell-complex hash, format version. Save statistically separated configurations.

---

## Final Endorsed Plan

### Execution Order

| Step | Task | Effort | Parallel |
|------|------|--------|----------|
| 1 | T33a: Cell-complex API | 3–4 days | Yes |
| 2 | T34a: Snapshot output | 1 day | With T33a |
| 3 | T34b pilot: Small cubic | 1 day | After T34a |
| 4 | T33b: Diamond Polyakov | 2–3 days | After T33a |
| 5 | T34b full: Flux loops | 2 days | After T34b pilot |
| 6 | T35a: Microscopic audit | 1–2 weeks | After T33a |

### Key Principle

> "Gauge-transition numerics are control physics; an explicit microscopic CZX realization is the actual unresolved claim."

This distinction is essential. The cubic-lattice Polyakov scans (T31) are already sufficient control physics. The real open problem is a new gauge-invariant quantum-geometric observable or an explicit microscopic construction.

---

## Files

- `memory-bank/tasks/T33a.md`
- `memory-bank/tasks/T33b.md`
- `memory-bank/tasks/T34a.md`
- `memory-bank/tasks/T34b.md`
- `memory-bank/tasks/T35a.md`
