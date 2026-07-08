# Post-May Numerics Correction Plan

*Created: 2026-07-05 22:24:10 IST*
*Last Updated: 2026-07-08 17:42 IST*
*Task: T32*

## Purpose

Preserve the useful simulation infrastructure and raw results produced after T18 while correcting claims that are unsupported, internally inconsistent, or gauge-dependent. No post-May numerical conclusion should enter the main manuscript until its workstream below is complete.

## Identified Error Inventory

This section records the actual errors identified in the post-May numerical work. The workstreams below describe the correction path; this inventory is the forensic record of what was wrong and why it matters.

### Error 1: T20d Misclassified the 3D $Z_2$ Gauge Transition

**Affected artifacts:** `t20d-fss-analysis.tex`, `numerics/docs/tasks/t20-z2-lgt.qmd`, rendered T20 task pages, dashboard text, and generated FSS figures.

**What was wrong:**

1. The transition was described as first-order, even though the standard expectation for pure 3D $Z_2$ lattice gauge theory is a continuous transition in the 3D Ising universality class.
2. A plaquette Binder cumulant near $2/3$ was treated as evidence of first-order behavior. This is not valid: a narrowly distributed nonzero plaquette can approach $2/3$ generically.
3. Local plaquette behavior was rhetorically promoted toward an order-parameter role without clearly distinguishing it from Wilson-loop or dual-Ising diagnostics.
4. Schematic or synthetic double-peak histograms were included in the evidence chain as if they supported measured phase coexistence.
5. Visual finite-size-scaling collapse failures were overinterpreted as evidence against continuous 3D Ising scaling, without a controlled treatment of corrections to scaling, autocorrelation, or uncertainty.
6. Some text converted incomplete exploratory analysis into publication-strength conclusions.

**Why it matters:** This error directly changes the scientific conclusion of the T20d analysis. It could lead the manuscript to cite a false transition-order result and to overstate the evidential value of the retained simulations.

**Resolved so far:**

- The standalone annexure and canonical Quarto task page have been rewritten around continuous 3D Ising-universality scaling.
- First-order, latent-heat, synthetic-histogram, and failed-collapse claims have been withdrawn from the canonical T20 task text.
- The dashboard source now omits the superseded first-order figure entries rather than duplicating them under unmarked titles.

**Still remaining:**

- The underlying numerical reanalysis still needs autocorrelation-aware uncertainties, controlled finite-size scaling, and Wilson-loop diagnostics.
- Generated or deployed dashboard outputs need to be rebuilt and checked so `_site` no longer contains stale dashboard entries.
- Superseded figure files and old analysis scripts remain present for provenance and need an intentional artifact policy before final cleanup.

### Error 2: T22a Was Mislabeled as a Spin-Foam Vertex Calculation

**Affected artifacts:** `numerics/scripts/t22a-fk-vertex-estimate.py`, `memory-bank/implementation-details/spin-foam-amplitude-calculation.md`, T22a task records, and any text calling the result an FK/EPRL vertex amplitude.

**What was wrong:**

1. The calculation was described as an FK or EPRL spin-foam vertex estimate, but it only evaluates a normalized SU(2) four-leg group average.
2. The computed ratio near $0.45$ was squared again and relabeled as a stronger approximately $0.20$ suppression ratio, even though that extra squaring was not supported by the calculation being performed.
3. The result was used to suggest $j=1/2$ dominance more strongly than the calculation justifies.
4. Monte Carlo validation was treated as the primary result, while the relevant four-character group average has an analytic character-integral interpretation that should be stated explicitly.

**Why it matters:** This error overstates what the calculation establishes. It turns a useful toy normalization/code-check result into apparent evidence for a physical spin-foam amplitude hierarchy.

**Resolved so far:**

- T22a has been reclassified as a normalized SU(2) four-leg group average.
- New `su2-four-leg-group-average` scripts record the analytic character-integral result as primary and use Monte Carlo as validation.
- The unsupported extra squaring from approximately $0.45$ to approximately $0.20$ has been removed from the corrected source text.
- The canonical T22 task source states that the calculation is not a complete FK/EPRL vertex and does not establish $j=1/2$ dominance.

**Still remaining:**

- The deployed `_site` T22 page is stale and still contains older FK-vertex and $j=1/2$ dominance wording until the docs are rebuilt.
- Old `t22a-fk-vertex-*` scripts, output, and figures are preserved for provenance and should stay clearly marked as superseded.

### Error 3: T31 Used a Gauge-Dependent Signed-Volume Diagnostic

**Affected artifacts:** `rust-lattice/src/lib.rs`, T31 generated data and figures, `memory-bank/implementation-details/signed-volume-observable.md`, T31 task page, and dashboard references.

**What was wrong:**

1. The path-based signed-volume observable was treated as a phase diagnostic even though the construction is gauge-dependent.
2. The proposed greedy or iterative gauge alignment would not fix the problem; spanning-tree-style alignment can force $|Q| = N$ in any phase and would destroy the observable's diagnostic value.
3. Existing phase-scaling claims based on $|Q|/N$ were therefore not gauge-invariant results.
4. The local gauge-transformation test was incomplete because it did not transform every incident link needed for a valid local gauge check.
5. Production-style runs were made before a replacement observable had passed gauge-invariance tests.

**Why it matters:** A gauge-dependent quantity can reflect the chosen representative rather than physics. Claims about time orientation or phase structure based on this diagnostic cannot be promoted until a gauge-invariant replacement is specified and tested.

**Resolved so far:**

- Existing $|Q|/N$ runs are now marked as gauge-dependent exploratory data.
- Greedy/iterative gauge alignment has been withdrawn.
- `rust-lattice/src/lib.rs` includes a corrected local gauge transformation that flips all six incident 3D links.
- The Rust source now contains a candidate gauge-invariant dressed orientation correlator, `gauge_invariant_signed_volume_3d()`.
- Source-level tests cover plaquette gauge invariance, gauge dependence of the old signed volume, and gauge invariance of the candidate replacement under single and multiple local transformations.
- The canonical T31 task page now records the correction and no longer recommends greedy gauge fixing.

**Still remaining:**

- The Rust tests still need to be run with a Rust 2024-compatible toolchain; the local Cargo available during the audit was too old.
- The dressed correlator needs physical review and production-scale validation before it can replace the old observable in conclusions.
- New simulations and finite-size scaling remain blocked until that validation is complete.

### Error 4: T25 Overinterpreted Spectral Pairing

**Affected artifacts:** T25 task records, volume-operator interpretation notes, and any manuscript or dashboard language connecting paired spectra to physical time orientation.

**What was wrong:**

1. The higher-valence volume spectra showed $+q/-q$ pairing, but the interpretation moved too quickly from algebraic spectral symmetry to a physical $Z_2$ time-orientation symmetry.
2. No explicit operator was specified and tested as the physical transformation implementing that symmetry on the relevant states.
3. The result was therefore stronger as an algebraic observation than as a demonstrated dynamical or physical orientation mechanism.

**Why it matters:** The spectra remain useful, but they cannot by themselves carry the physical interpretation assigned to them. The manuscript needs the distinction between "paired eigenvalues exist" and "a physical time-orientation symmetry has been demonstrated."

**Resolved so far:**

- T25 source and rendered task text now describe the result as algebraic spectral reflection symmetry.
- The physical $Z_2$ time-orientation interpretation is explicitly deferred until an operator implementing the transformation is constructed and tested.

**Still remaining:**

- The physical-transformation test itself remains future work, likely T33 or later.

### Error 5: Reproducibility Was Not Established Before Claims Were Promoted

**Affected artifacts:** `numerics/package.json`, TypeScript test/build setup, Rust toolchain and tests, generated outputs, checkpoints, rendered artifacts, and memory-bank/database regeneration.

**What was wrong:**

1. The repository did not provide a single clean, documented validation path covering the relevant TypeScript, Rust, and analysis checks.
2. Build/test requirements were not fully pinned or verified from the recorded project state.
3. Some generated artifacts and rendered outputs were treated as evidence-bearing publication artifacts before the underlying correction checks were complete.
4. SQLite memory-bank regeneration was deferred because local database dependencies such as `sql.js` were not installed; Markdown remained canonical, but the limitation needed to be recorded.

**Why it matters:** Without a reproducible validation path, it is too easy for corrected text, raw data, rendered dashboards, and generated figures to drift out of sync.

**Resolved so far:**

- `README.md` documents the TypeScript and Rust requirements.
- `scripts/validate.sh` provides a single validation command for TypeScript build checking, Rust build checking, and Rust unit tests.
- Markdown remains the canonical memory-bank audit trail while SQLite regeneration dependencies are absent.

**Still remaining:**

- The validation path has not been verified in the current shell because the available Cargo cannot parse Rust edition 2024.
- The artifact policy for generated outputs, checkpoints, databases, logs, and rendered pages still needs a final pass.

### Error 6: Manuscript Gate Was Too Weak

**Affected artifacts:** `timesarrow.tex`, annexures, numerical task pages, dashboard pages, and any future manuscript integration notes.

**What was wrong:**

1. Several post-May numerical claims were close to manuscript-ready language before their interpretation and reproducibility had been verified.
2. Superseded conclusions were not initially separated clearly enough from retained raw data and infrastructure.
3. The memory bank needed an explicit gate preventing T20d, T22a, T31, and T25 claims from entering `timesarrow.tex` until T32 is complete.

**Why it matters:** The useful work should be preserved, but unsupported conclusions must not leak into the main paper as established results.

**Resolved so far:**

- The manuscript gate is recorded in T32, `activeContext.md`, and `progress.md`.
- `timesarrow.tex` inspection did not find the withdrawn T20d first-order result or the erroneous T22a $0.20$ claim.

**Still remaining:**

- The gate remains active until T20d reanalysis, T31 validation, reproducibility verification, and rendered-artifact synchronization are complete.

## Workstream 1: T20 Transition Interpretation

1. Treat the 3D pure $Z_2$ gauge transition as continuous and in the 3D Ising universality class unless new validated evidence establishes otherwise.
2. Withdraw the claim that a plaquette Binder cumulant approaching $2/3$ proves a first-order transition. A narrowly distributed nonzero plaquette approaches this value generically.
3. Do not call a single plaquette a Wilson-loop order parameter; distinguish local plaquette energy from area-law/perimeter-law measurements.
4. Remove schematic double-peak histograms from the evidence chain. Retain them only if explicitly labeled as illustrations, not measurements.
5. Reanalyse existing data with suitable nonlocal observables, dual-Ising quantities, autocorrelation treatment, and finite-size scaling.

## Workstream 2: T22a Reclassification

1. Rename the result as a normalized SU(2) four-leg group average.
2. Record the analytic character-integral result and use Monte Carlo only as a validation check.
3. Remove the extra squaring that converts the computed ratio near $0.45$ into an unsupported $0.20$ ratio.
4. State explicitly that the calculation is not a complete FK/EPRL vertex amplitude and does not establish $j=1/2$ dominance.

## Workstream 3: T31 Observable Redesign

1. Do not implement iterative gauge transformations that maximize $|Q|$; spanning-tree alignment can force $|Q|=N$ in any phase.
2. Mark current signed-volume runs as gauge-dependent exploratory data.
3. Replace the observable with a gauge-invariant dressed orientation correlator, a Wilson line with physical endpoint variables, or an appropriate Wilson/'t Hooft-loop diagnostic.
4. Correct the gauge-transformation unit test so every incident link is transformed.
5. Run new production simulations only after the observable passes gauge-invariance tests.

## Workstream 4: T25 Interpretation

1. Preserve the higher-valence signed-volume spectra.
2. Describe $+q/-q$ spectral pairing as an algebraic spectral symmetry, not by itself proof of a physical $Z_2$ time-orientation symmetry.
3. Specify an operator implementing the proposed transformation and test its action on the volume operator and eigenstates.

## Workstream 5: Reproducibility and Manuscript Gate

1. Make the TypeScript build pass in strict mode and ensure test dependencies install from the lockfile.
2. Declare a supported Rust toolchain compatible with the selected Cargo edition.
3. Provide one documented validation command covering builds, unit tests, and key analysis checks.
4. Review tracked generated files, checkpoints, databases, logs, and rendered output; keep only intentional release artifacts.
5. Keep `timesarrow.tex` unchanged by T20d/T22a/T31 claims until T32 acceptance criteria pass.

## Recommended Order

T20 correction → T22a correction → T31 redesign → T25 calibration → reproducibility cleanup → manuscript review.
