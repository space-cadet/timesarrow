# T20: Data Collation System

*Date: 2026-06-26*
*Applies to: numerics/data/registry.json, numerics/src/scripts/collate-data.ts*

## Purpose

Central registry of all simulation runs for the TimesArrow project. Enables tracking, reproducibility, and dashboard display.

## Registry Schema

```json
{
  "schemaVersion": "1.0.0",
  "project": "timesarrow",
  "lastUpdated": "ISO-8601 timestamp",
  "runs": [
    {
      "runId": "t20-p3-L16-3D-20250626",
      "task": "T20",
      "phase": "phase3",
      "status": "complete",
      "timestamp": "ISO-8601",
      "description": "Human-readable summary",
      "parameters": { "latticeSize": 16, "dimension": 3, "betaValues": [...] },
      "results": { "keyFinding": "...", "criticalBetaEstimate": 0.751 },
      "outputFiles": ["output/t20-p3-L16-3D-20250626.json"],
      "page": "tasks/t20-z2-lgt.qmd"
    }
  ],
  "tasks": {
    "T20": { "name": "...", "status": "in-progress", "phases": {...} }
  }
}
```

## Filename Conventions

| Pattern | Example | Meaning |
|---------|---------|---------|
| `t{task}-p{phase}-L{size}-{date}` | `t20-p2-L16-20250625` | Phase result |
| `t{task}-p{phase}-L{size}-3D-{detail}-{date}` | `t20-p3-L16-3D-wilson-fine-20250626` | 3D with detail |
| `t{task}-p{phase}b-L{size}-3D-{detail}-{date}` | `t20-p3b-L8-3D-fine-20260626` | Phase 3b (FSS) |

**Date format**: `YYYYMMDD` (no hyphens) for collation regex compatibility.

## Collation Script: `collate-data.ts`

### Usage

```bash
cd numerics
npx ts-node --esm src/scripts/collate-data.ts
```

### What it does

1. Scans `output/` directory for `.json` files matching run patterns
2. Extracts metadata from filenames (task, phase, L, date)
3. Reads JSON content for key results (if readable)
4. Updates `registry.json` with new runs
5. Sets `lastUpdated` timestamp

### Implementation Notes

- Uses `import` (ES modules) not `require`
- Regex: `/t(\d+)-p(\d+)([b]?)-L(\d+)-3D-(\w+)-(\d{8})/`
- Date parsing: `new Date(dateStr.slice(0,4) + '-' + ...)`

## Known Issues

1. **Plaintext in JSON files**: Some scripts (benchmarks) log to stdout which gets captured in the JSON file, corrupting it. Fix: redirect logs to stderr or separate log file.
2. **Date inconsistency**: Some files use `20260626` (wrong year) instead of `20250626`. These are legacy runs.
3. **Manual registry edits**: `registry.json` was hand-edited at one point, introducing syntax errors (missing commas). Always use the collation script.

## Status (2026-06-26)

- **Total runs registered**: 33
- **T20**: 26 runs (phases 1, 2, 3, 3b)
- **T27**: 5 runs (benchmarks)
- **T25**: 1 run (volume operator)
