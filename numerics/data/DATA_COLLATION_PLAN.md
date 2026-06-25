# Data Collation System for TimesArrow Numerics

## Problem
As we perform more simulations, the data becomes scattered across:
- Individual JSON files in `output/`
- Embedded in Quarto documents
- Inconsistent naming conventions
- No central index of what's been run

## Solution: Structured Data Registry

### 1. Registry File (`data/registry.json`)
Central index of ALL simulation runs with:
- **Run metadata**: id, timestamp, task, phase, status
- **Parameters**: lattice size, β values, sweeps, etc.
- **Output files**: paths to raw data
- **Results summary**: key findings (collated from raw data)

### 2. Standardized Output Schema
Every simulation run produces:
```json
{
  "runId": "t20-p2-L16-20250625",
  "task": "T20",
  "phase": "phase2",
  "timestamp": "2025-06-25T10:00:00Z",
  "parameters": {
    "latticeSize": 16,
    "dimension": 2,
    "betaValues": [0.3, 0.35, ...],
    "thermalizationSweeps": 10000,
    "measurementSweeps": 100000
  },
  "results": {
    "criticalBeta": 0.44,
    "observables": {
      "plaquette": [...],
      "susceptibility": [...],
      "binderCumulant": [...]
    }
  },
  "outputFiles": [
    "output/t20-p2-L16-20250625.json"
  ]
}
```

### 3. Automated Collation Script
`scripts/collate-data.ts`:
- Scans `output/` for new JSON files
- Extracts metadata from filenames/headers
- Updates `registry.json`
- Generates summary tables for Quarto pages

### 4. Quarto Integration
Each task page (`tasks/t20-z2-lgt.qmd`) will:
- Read from `registry.json` for up-to-date status
- Include automatically-generated summary tables
- Link to raw data files
- Show run history with timestamps

## Implementation Steps

1. ✅ Create `data/registry.schema.json` (template)
2. 🔄 Create `scripts/collate-data.ts`
3. 🔄 Run Phase 2 simulations → populate registry
4. 🔄 Update T20 page with auto-generated tables
5. 🔄 Repeat for Phase 3 and other tasks
