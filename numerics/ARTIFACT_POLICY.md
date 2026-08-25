# Numerical Artifact Policy

*Approved for T32: 2026-08-25 15:05:57 IST*
*Related Tasks: T20d, T22a, T25, T31, T32, T36*

## Purpose

This policy separates publication-canonical evidence from historical provenance, superseded interpretations, transient run state, and rendered mirrors. Keeping a file in the repository preserves audit history; it does not make that file eligible to support a manuscript claim.

`publication-artifacts.sha256` fixes the exact canonical source-data and analysis-script snapshot reviewed for T32.

## Authority Order

1. This policy and `publication-artifacts.sha256` define the publication evidence set.
2. The named raw datasets and analysis scripts are the canonical sources.
3. Summary JSON and figures are derived artifacts and are not canonical unless this policy names them explicitly.
4. `data/registry.json` and Quarto registries are discovery aids, not publication authority.
5. `docs/_site/` is a rendered release mirror, never a source of scientific truth.

## T20d Canonical Control Set

### Raw data

- `data/fss/t20-p3b-L8-3D-fine-20260710.json`
- `data/fss/t20-p3b-L16-3D-fine-20260714.json`
- `data/fss/t20d-L24-fine-20260629.json`
- `data/fss/t20-p3b-L32-3D-fine-20260714.json`

### Analysis

- `src/scripts/t20d-ising-reanalysis.py`

The analysis script must fail if one of the four canonical inputs is absent. It must not silently substitute an older run.

### Generated-figure decision

No existing T20d generated figure is publication-canonical. Visual inspection on 2026-08-25 found that the current line plots connect asynchronously ordered $\beta$ samples and therefore contain misleading backtracking segments. The analysis script now sorts each dataset by $\beta$, but regeneration remains blocked in the current shell because the scientific Python plotting stack is unavailable. T36 may use a bounded table derived from the canonical raw data, or regenerate and review figures in a declared environment before including them.

All existing `t20d-ising-*.png` files are retained as derived analysis artifacts but excluded from the paper until regenerated and visually approved. Independently of the plotting defect, precision extrapolation, Binder-crossing, collapse, and exponent-fit figures remain outside the Path A evidence boundary.

## T31 Canonical Control Set

### Raw data

- `data/t31-polyakov-L8-fine-20260715.json`
- `data/t31-polyakov-L10-fine-20260715.json`
- `data/t31-polyakov-L12-fine-20260715.json`
- `data/t31-polyakov-L16-fine-20260715.json`

### Analysis

- `src/scripts/t31-polyakov-exponent-analysis.py`

### Generated-figure decision

No existing T31 generated figure is publication-canonical. Visual inspection found the same unsorted-$\beta$ line-connection defect in the current Polyakov susceptibility plot. The analysis script now sorts its exact inputs before plotting. Until figures are regenerated and inspected in a declared scientific Python environment, T36 may use a bounded numerical table but must not include the existing susceptibility or log--log fit figures.

## T31 Signed-Volume Negative Result

The following cold-start and multiseed calibration files are canonical provenance for the bounded negative result:

- `data/signed-volume/t31-gi-L4-cold-calibration-20260714.json`
- `data/signed-volume/t31-gi-L6-cold-calibration-20260714.json`
- `data/signed-volume/t31-gi-L6-beta1-seed42-20260714.json`
- `data/signed-volume/t31-gi-L6-beta1-seed43-20260714.json`
- `data/signed-volume/t31-gi-L6-beta1-seed44-20260714.json`

They show that the tested implementation can return the expected cold-start value but does not yield a stable phase-discriminating dressed observable after thermalization. Raw `sv-L*.json` and `sv-L*.log` files remain gauge-dependent exploratory provenance and are not publication-positive evidence.

## Other Bounded Artifacts

- T22a corrected group-average data and figures are supplement-only analytic/code checks.
- T25 spectrum artifacts are algebraic background only; they do not establish a physical time-reversal operator or an ordered phase.
- T35a artifacts validate the reference CZX model only; they are not evidence of an LQG embedding.

## Superseded or Provenance-Only Material

The following material is quarantined logically and must not enter the manuscript evidence chain:

- filenames or figures labeled `first-order`, `latent-heat`, `double-peak`, or synthetic energy histograms;
- earlier T20 finite-size runs replaced by the four canonical datasets above;
- provisional critical-exponent fits and failed-collapse interpretations;
- raw signed-volume phase-scaling figures and Binder analyses;
- greedy gauge-alignment outputs;
- `.log`, `.bak`, `.checkpoint*`, `.monitor*`, and checkpoint directories;
- compiled `dist/` and `dist-cjs/` trees;
- rendered `docs/_site/` files except as a deployment snapshot; and
- stale registry descriptions that conflict with T31, T32, or this policy.

These files are retained for provenance unless a separate cleanup is approved. Retention does not authorize citation or reuse.

## Reproducibility Gate

Before a numerical artifact is used in `timesarrow.tex`:

1. Verify its checksum against `publication-artifacts.sha256`.
2. Run `./scripts/validate.sh` successfully with the pinned Rust toolchain.
3. Confirm that the claim stays within the Path A numerical evidence matrix.
4. Regenerate any chosen figure only from the exact canonical inputs above, then inspect it visually before inclusion.
5. Record any changed input, script, or figure by updating both this policy and the checksum manifest.
