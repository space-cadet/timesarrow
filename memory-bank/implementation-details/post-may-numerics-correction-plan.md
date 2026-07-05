# Post-May Numerics Correction Plan

*Created: 2026-07-05 22:24:10 IST*
*Last Updated: 2026-07-05 22:24:10 IST*
*Task: T32*

## Purpose

Preserve the useful simulation infrastructure and raw results produced after T18 while correcting claims that are unsupported, internally inconsistent, or gauge-dependent. No post-May numerical conclusion should enter the main manuscript until its workstream below is complete.

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
2. Describe $± q$ spectral pairing as an algebraic spectral symmetry, not by itself proof of a physical $Z_2$ time-orientation symmetry.
3. Specify an operator implementing the proposed transformation and test its action on the volume operator and eigenstates.

## Workstream 5: Reproducibility and Manuscript Gate

1. Make the TypeScript build pass in strict mode and ensure test dependencies install from the lockfile.
2. Declare a supported Rust toolchain compatible with the selected Cargo edition.
3. Provide one documented validation command covering builds, unit tests, and key analysis checks.
4. Review tracked generated files, checkpoints, databases, logs, and rendered output; keep only intentional release artifacts.
5. Keep `timesarrow.tex` unchanged by T20d/T22a/T31 claims until T32 acceptance criteria pass.

## Recommended Order

T20 correction → T22a correction → T31 redesign → T25 calibration → reproducibility cleanup → manuscript review.
