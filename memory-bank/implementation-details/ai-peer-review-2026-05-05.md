# AI Peer Review: Final Manuscript Pass (2026-05-05)

*Type*: Pre-submission peer review  
*Reviewer*: Kimi Code CLI (Kimi K2.6 based agent)  
*Author*: Deepak Vaid  
*Manuscript*: "Gauging Time Reversal Symmetry in Quantum Gravity: Arrow of Time from a Confinement–Deconfinement Transition"  
*Date*: 2026-05-05  

---

## Instructions

The author requested a final, brutally honest pass over the manuscript before arXiv submission, scanning for physical, mathematical, and conceptual errors. This document records the full dialog: the reviewer's initial claims, the author's responses, the reviewer's follow-up observations (including admitted errors), and the final resolutions.

---

## Round 1: Reviewer's Initial Report

> **Reviewer**: I have read every line of the manuscript and the supplementary calculations. Here is my brutally honest assessment.

### 🔴 Critical — Must Fix Before arXiv

**Issue #1 — Singlet states in `eqn:vol-states` are mathematically wrong**

The reviewer claimed the manuscript's basis states
```
|Φ₁⟩ = 1/√3(|0101⟩ + |1010⟩ − ½(|1001⟩ + |0110⟩ + |0011⟩ + |1100⟩))
|Φ₂⟩ = ½(|1001⟩ + |0110⟩ − |0011⟩ − |1100⟩)
```
were **not** SU(2) singlets. The reviewer computed that while $S^+_{\text{tot}}|Φ_i⟩ = 0$, the lowering operator gave $S^-_{\text{tot}}|Φ_i⟩ ≠ 0$, placing them in the $j_{\text{tot}} = 1$ sector. The reviewer further noted that Appendix F performed calculations using the *supplementary* basis while claiming to use the manuscript basis, creating an internal inconsistency.

**Impact assessment**: "This error infects the entire paper. The volume-operator discussion, the LQG–CZX correspondence, and the claim that $U_{CZX}$ acts as Pauli-X on the intertwiner subspace all rest on these states."

**Issue #2 — $Z_2$ vs SU(2) confusion at line 1437**

The reviewer flagged the sentence:
> "Since each $\tau_v$ generator at vertex $v$ squares to unity, $\tau_v^2 = 1$, the state remains invariant under local transformations."

as nonsensical in the SU(2) Gauss-constraint context, because SU(2) generators do not square to unity ($J_i^2 = \frac{3}{4}\mathbb{1}$ for $j=1/2$). The reviewer interpreted this as conflating the $Z_2$ gauge parameter $\tau_v$ with SU(2) gauge transformations.

### 🟠 Major — Strongly Recommended to Fix

**Issue #3** — Area minimum missing factor of $\pi$: $A_{\min} = 4\sqrt{3}\,\gamma\,l_p^2$ should be $4\sqrt{3}\,\pi\,\gamma\,l_p^2$.

**Issue #4** — Universality class claim suspicious: "3d $Z_2$ gauge theory is in the same universality class as the 3d Ising model." The reviewer argued 3D $Z_2$ gauge theory is dual to 2D Ising, not 3D Ising.

**Issue #5** — Introduction claim (iv) overstates literal $U_{CZX}$ action: "We provide an explicit computation showing that $U_{CZX}$ acts as a Pauli-X gate on the intertwiner subspace." The reviewer noted Appendix F proves $U_{CZX}$ does **not** preserve the SU(2) singlet subspace.

**Issue #6** — Dimensional mismatch between 2D CZX and 3D spin networks is hand-wavy; needs tighter justification.

### 🟡 Moderate

**Issue #7** — Thermal suppression argument dimensionally inconsistent: $\beta E_j$ with $E_j = \kappa\sqrt{j(j+1)}$ and $\kappa = 8\pi\gamma l_p^2$ has unit confusion unless working in Planck units.

**Issue #8** — MPS universality statement misleading about required bond dimension.

**Issue #9** — Hyphen/en-dash inconsistency between title and abstract.

**Bottom line**: "**Do not submit to arXiv until Issue #1 is fixed.** The singlet-basis error is not a typo — it invalidates the central mathematical pillar of the paper."

---

## Round 2: Author's Responses

> **Author**: Let me address the points you have raised.

### On Issue #1 (singlet basis)

> **Author**: The states are correct only calculated in a different basis from the one you are using. This confusion had arisen earlier with Claude also. There might be some mention of this in the memory bank.

The author asserted that the manuscript states are valid orthonormal singlets, merely expressed in a different basis from the supplementary calculations. The author noted this same confusion had occurred with a prior AI assistant.

### On Issue #2 ($Z_2$ reduction)

> **Author**: $Z_2$ comes about because that is what SU(2) reduces to. At least in the context of a discrete gauge theory arising from the underlying SU(2) gauge theory.

The author clarified that the $Z_2$ is the *effective discrete remnant* of SU(2) when restricted to the $j=1/2$ intertwiner qubit.

### On Issue #3 ($A_{\min}$)

> **Author**: Ok. Sure.

Approved fix.

### On Issue #4 (universality class)

> **Author**: What do you suggest?

Requested recommendation.

### On Issue #5 ($U_{CZX}$ claim)

> **Author**: Right. $U_{CZX}$ preserves the volume eigenstates. That's also where the $Z_2$ symmetry comes from btw. And this is the crux of the argument about the emergence of an arrow of time from the local breaking of the $Z_2$ symmetry. Again, check memory bank.

The author emphasized that the relevant $Z_2$ action is the sign-flip of the volume operator $\hat{Q}$ on the LQG side, structurally identified with $U_{CZX}$ on the CZX code subspace — not a literal operator equality on the full 16D Hilbert space.

### On Issue #6 (2D vs 3D)

> **Author**: We are not working with arbitrary graphs. We are working with a representative class of graphs. You are correct. I do not know how, or if, one could extend this to ALL graphs. Likely, not. Instead there should be some argument, similar to the $j=1/2$ dominance argument, for [why] regular graphs (lattices) will dominate the partition function of the model.

The author endorsed adding a "regular-lattice dominance" paragraph analogous to the thermal argument.

### On Issues #7–9

> **Author**: Please fix. / Please add. / Please fix.

All approved.

---

## Round 3: Reviewer's Re-evaluation and Retractions

> **Reviewer**: You are right on #1, and I apologize. I made a computational error mixing up $S^+$ and $S^-$ actions in my earlier verification.

### Retraction on Issue #1

The reviewer recomputed $S^-_{\text{tot}}|Φ_1⟩$ and $S^-_{\text{tot}}|Φ_2⟩$ **correctly** and found both vanish:

```
S^-|1001⟩ = |1101⟩ + |1011⟩
S^-|0110⟩ = |1110⟩ + |0111⟩
S^-|0011⟩ = |1011⟩ + |0111⟩
S^-|1100⟩ = |1110⟩ + |1101⟩

S^-|Φ₂⟩ = ½[(|1101⟩+|1011⟩) + (|1110⟩+|0111⟩) − (|1011⟩+|0111⟩) − (|1110⟩+|1101⟩)] = 0
```

The reviewer had previously **incorrectly** assigned $S^-|0110⟩ = |0010⟩ + |0100⟩$, which is actually the result for $S^+$, not $S^-$. This single sign-flip error cascaded into a false conclusion that the states were not singlets.

**Verdict**: The manuscript's $|Φ_1⟩$, $|Φ_2⟩$ **are** valid orthonormal singlets. They are a different basis from the supplementary calculations (related by a basis rotation in the 2D singlet space). The reviewer's initial claim was **wrong**.

However, the reviewer maintained that Appendix F has a **genuine inconsistency**: it claims to use the manuscript basis from `eqn:vol-states` but computes $U_{CZ}|Φ_1⟩ = ½(|0101⟩+|0110⟩+|1001⟩+|1010⟩)$, which has no $|0011⟩$ or $|1100⟩$ terms — a result that only holds for the supplementary basis. This was fixed.

### Response to Issue #2

The reviewer accepted the author's physics but noted the sentence was **in the wrong place**: it appeared in the SU(2) Gauss-constraint appendix (Appendix E) without context, making $\tau_v$ look like an SU(2) generator. The fix added an explicit bridge: "the continuous SU(2) symmetry reduces to an effective discrete $Z_2$ symmetry ... whose generator satisfies $\tau_v^2 = 1$."

### Response to Issue #4

The reviewer recommended a footnote hedge: clarify that the claim refers to the **$T=0$ quantum transition in $3+1$D** (dual to 3D quantum Ising), while noting that a purely classical 3D treatment maps to 2D classical Ising exponents.

### Response to Issue #5

The reviewer agreed with the author's framing: the relevant $Z_2$ on the LQG side is the **$\hat{Q}$-sign flip** (a unitary automorphism of the singlet subspace), structurally identified with $U_{CZX}$ on the CZX code subspace. The introduction was updated to match the structural-correspondence language already present in Section 6.4.

---

## Final Resolutions

| Issue | Severity | Initial Claim | Author Response | Final Resolution |
|-------|----------|---------------|-----------------|------------------|
| 1 | 🔴 Critical | States not singlets; appendix inconsistent | States are correct, different basis | **Retracted** — states are valid singlets; appendix inconsistency fixed |
| 2 | 🔴 Critical | $\tau_v^2=1$ conflates SU(2) and $Z_2$ | $Z_2$ is what SU(2) reduces to | Rewritten to clarify reduction to effective $Z_2$ on intertwiner qubit |
| 3 | 🟠 Major | $A_{\min}$ missing $\pi$ | Approved fix | Added $\pi$ |
| 4 | 🟠 Major | Universality class likely wrong | Asked for suggestion | Footnote added hedging quantum ($3+1$D → 3D Ising) vs classical (3D → 2D Ising) |
| 5 | 🟠 Major | Intro overstates literal $U_{CZX}$ action | $U_{CZX}$ preserves volume eigenstates | Intro reframed as structural $Z_2$ qubit correspondence |
| 6 | 🟠 Major | 2D/3D mismatch under-justified | Regular graphs dominate, like $j=1/2$ | Paragraph added arguing regular-lattice dominance |
| 7 | 🟡 Moderate | Dimensional inconsistency | Approved fix | Explicit Planck-units framing added; dimensions restored for $T_c$ |
| 8 | 🟡 Moderate | MPS statement misleading | Approved fix | Added bond-dimension caveat |
| 9 | 🟡 Moderate | Hyphen/en-dash inconsistency | Approved fix | En-dash applied consistently |

---

## Lessons Learned

1. **Basis rotation confusion**: The manuscript uses one orthonormal singlet basis; the supplementary calculations use another. Both are correct, but cross-referencing between them without explicit conversion led to an apparent inconsistency in Appendix F. Future revisions should explicitly state when a different basis is used.

2. **Reviewer's computational error**: The reviewer falsely rejected valid mathematics due to a single sign error ($S^+$ vs $S^-$). This is a cautionary tale about the fragility of AI-assisted verification — even rigorous-looking calculations can contain subtle mistakes.

3. **Effective symmetry reduction**: The author's physical intuition — that SU(2) "reduces to" $Z_2$ on the $j=1/2$ intertwiner qubit — is correct but was poorly explained in the text. The fix makes this reduction explicit rather than dropping $\tau_v$ into the SU(2) appendix without context.

4. **Structural vs literal correspondence**: The core of the paper is a *structural* identification of two $Z_2$-invariant qubits (LQG intertwiner ↔ CZX code), not a literal operator identity on the full 16D Hilbert space. Both the reviewer and author converged on this framing, but the introduction lagged behind the main text.

---

## Files Modified

- `timesarrow.tex` — 9 edits applied
- `arxiv_submission_v1/timesarrow.tex` — synchronized with root

## Build Verification

- `pdflatex` + `biber` + `pdflatex` × 2: clean, 42 pages, stable output
