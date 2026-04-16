# System Patterns
*Last Updated: 2026-04-16 23:15:00 IST*

## Theoretical Mappings
- **Spin Network ↔ Tensor Network**: Spin network edges (labeled by SU(2) spins) map to TNS bonds; vertices map to tensors (intertwiners).
- **Z2 Gauge Field ↔ Time Reversal**: A local Z2 field on the spin network edges encodes the local time-reversal symmetry. Gauging is via Chen-Vishwanath procedure (bond-index insertions on TNS), NOT Yang-Mills gauging.
- **Volume Sign ↔ Time Arrow**: The sign of the volume operator (related to the tetrad determinant) represents the local direction of time. Flipping an edge spin → volume sign flip.
- **SPT Edge States ↔ Fermionic Matter**: Gapless edge modes of the SPT phase are conjectured to correspond to Dirac fermions. Three supporting arguments: string-net analogy, Dirac equation boundary conditions, spin-statistics.
- **Confined Phase (K < K_c) ↔ Pre-geometric Foam**: Z2 flux disordered (area law for Wilson loops), no coherent spacetime or arrow of time.
- **Deconfined Phase (K > K_c) ↔ Semiclassical Spacetime**: Z2 flux ordered (perimeter law for Wilson loops), coherent arrow of time. This IS the CZX SPT phase.
- **Confinement-Deconfinement Transition ↔ Cosmological Phase Transition**: Emergence of arrow of time = transition from confined to deconfined Z2 gauge theory on primordial spin network.

## Key Technical Points (Post-Rewrite)
- **Elitzur's Theorem**: Local ⟨σ_v⟩ = 0 in both phases (theorem satisfied). Physical order parameter is Wilson loop W(γ) (non-local, gauge-invariant). Phase transition detected by area law → perimeter law scaling.
- **j=1/2 Dominance**: At Planck scale, j=1/2 sector dominates (amplitude suppression like lowest Landau level, entropy counting). Higher spins = fluctuations; don't change universality class of phase transition.
- **QECC Interpretation**: Deconfined phase ≡ Kitaev toric code ≡ quantum error correcting code. Local "errors" (reversed time orientation at isolated vertices) are corrected by topological order. Exponential suppression of pockets of reversed time.
- **Hopf Algebra Structure**: Z2 gauge theory = quantum double (Bais, Propitius). Connected to Deepak's separate project on Hopf algebras in spin network dynamics. Markopoulou (1997, 2000) anticipated this connection.
- **Chen-Vishwanath Gauging**: NOT Yang-Mills gauging. Localizes global Z2 time-reversal via TNS bond-index insertions. Sum over all domain-wall configurations = "gauged" theory. This is why Elitzur's theorem applies only to local observables.

## Structural Conventions (Updated)
- **Paper Structure**: Introduction → Topological Order → MPS/TNS → Spin Networks → Volume/Z2 → SPT/CZX → **SPT/LQG Mapping** → **Z2 Action & Phase Transition** → Discussion → Appendices
- **Notation**: 
  - $j$: Spin labels for edges.
  - $\Tr$: Trace over bond indices.
  - $A^v$ / $I^v$: Vertex tensors / Intertwiners.
  - $g^e$ / $D^e$: Edge tensors / Wigner matrices.
  - $\sigma_e \in \{+1, -1\}$: Z2 gauge field on edges.
  - $K$: Dimensionless coupling in Z2 gauge action.
  - $K_c$: Critical coupling for confinement-deconfinement transition.
  - $W(\gamma) = \expect{\prod_{e \in \gamma} \sigma_e}$: Wilson loop order parameter.

## Document Evolution (Post-Rewrite)
- **Title**: Changed to "...Confinement-Deconfinement Transition"
- **Abstract**: Fully rewritten for clarity and completeness
- **Sec 6 (spt-lqg-mapping.tex)**: Expanded from ~15 lines → ~2500 words, 4 subsections
- **Sec 7 (z2-action-derivation.tex)**: Expanded from ~18 lines → ~3500 words, 4 subsections
- **Discussion**: Added 3 new subsections (Elitzur, QECC, Hopf algebras/future work)
- **Bibliography**: +9 entries (Elitzur, Wegner, Fradkin-Shenker, Kogut, Wilson, Markopoulou x2, Perez, Dennis-Kitaev-Landahl-Preskill)

## Critical Insights (Resolved in Rewrite)
- The "spontaneous symmetry breaking" language was problematic → reframed as "confinement-deconfinement transition"
- Elitzur's theorem objection → resolved via non-local Wilson loop order parameter
- CZX-to-LQG mapping was purely structural → now connected via common Z2 gauge theory framework
- Edge modes/fermions claim was speculative → now properly softened as conjecture with supporting arguments
- Hopf algebraic structure mentioned in old memory but not in paper → now acknowledged and connected to future directions

## Ready for Cleanup Tasks
Paper is scientifically complete. Remaining work is editorial:
- Trim Sec 3 MPS pedagogy
- Shorten Appendix D
- Fix typos and remove commented code
- Minor polishing for clarity
