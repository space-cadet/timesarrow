# T25 — Volume Operator Extension

## Deployment

- **URL**: https://space-cadet.github.io/projects/timesarrow/numerics/tasks/t25-volume-operator.html
- **Main numerics page**: https://space-cadet.github.io/projects/timesarrow/numerics/
- **Project redirect**: https://space-cadet.github.io/projects/timesarrow/
- **Deployed**: 2026-06-24
- **Repo**: space-cadet.github.io (projects/timesarrow/ directory)

## Structure

Matches qhe-bhe project layout:
```
projects/timesarrow/
├── index.html              → redirect to numerics/
└── numerics/
    ├── index.html          → main numerics overview with task table
    ├── index_files/        → Quarto support files
    └── tasks/
        └── t25-volume-operator.html  → task detail page
```

## Code Changes

### ts-quantum Library
- **index.ts**: Exported intertwiner module (`export * from './intertwiner'`)
- **volumeOperator.ts**: Fixed `checkZ2Structure()` to handle zero eigenvalues properly
  - Old: Paired by sorted absolute value (broke on zeros)
  - New: Groups by absolute value, checks equal numbers of +q and -q
- **nValent.ts**: Added parity check in `constructNValentBasis()`
  - Odd number of half-integer spins → returns dimension 0 (can't couple to J=0)

### timesarrow-numerics
- **t25-volume-operator.test.ts**: Tests for 4,5,6 valent cases
- **generate-t25-data.ts**: Data generation script (stubbed for 6-valent)
- **t25-volume-operator.qmd**: Quarto documentation page

## Results

| Valence | j | Dimension | Eigenvalues | Z₂ Structure | Status |
|---------|---|-----------|-------------|--------------|--------|
| 4 | 1/2 | 2 | ±8√3/9 ≈ ±1.5396 | ✅ Confirmed | Complete |
| 5 | 1/2 | 0 | N/A | N/A | Excluded by parity |
| 6 | 1/2 | 5 | [pending] | [pending] | Framework ready |
