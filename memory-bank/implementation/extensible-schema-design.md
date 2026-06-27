# Extensible Numerics Schema Design

*Created: 2026-06-27*
*Status: Design Proposal | Pending Review*
*Related: T29 — Extensible Numerics Schema Design*

## Problem

Current `registry.schema.json` is tightly coupled to lattice gauge theory:
- Hardcoded fields: `latticeSize`, `betaValues`, `gaugeGroup`
- Observable names are free-text strings
- Figure references are just filename lists
- No data lineage — can't trace which runs produced which plot
- No separation between "what the dashboard must know" and "what it can know"

This works for T20 (Z₂ LGT) but breaks for DMRG, tensor networks, or any other numerics.

## Design Principle: Open/Closed Base Schema

The base schema is small, stable, and physics-agnostic. Everything specific lives in **extension namespaces**.

### Base Schema (never changes across physics domains)

```json
{
  "registryVersion": "1.0.0",
  "runs": [{
    "runId": "t20-p3b-L8-3D",
    "task": "T20",
    "status": "complete",
    "timestamp": "...",
    "description": "3D Z₂ LGT finite-size scaling, L=8",
    "extensions": {
      "lgt": {
        "dimension": 3,
        "latticeSize": 8,
        "betaValues": [0.70, 0.705, ...],
        "gaugeGroup": "Z2",
        "thermalizationSweeps": 500000,
        "measurementSweeps": 1000000
      }
    },
    "outputs": {
      "dataFiles": [{
        "path": "output/t20-p3b-L8.json",
        "format": "json",
        "schema": {
          "columns": ["beta", "plaquette", "plaquette_err", "susceptibility"],
          "shape": [25, 4],
          "indexColumn": "beta"
        }
      }],
      "figures": [{
        "id": "t20-p3-fss-plaquette",
        "path": "figures/t20-p3-fss-plaquette.png",
        "type": "FSS",
        "title": "Plaquette vs β (FSS)",
        "sourceRuns": ["t20-p3b-L8", "t20-p3b-L16", "t20-p3-L24", "t20-p3-L32"]
      }]
    }
  }]
}
```

**Why this works:** The dashboard can display run lists, task breakdowns, and figure galleries without understanding `lgt`. It only needs `lgt` when rendering LGT-specific visualizations or filtering by `dimension`/`latticeSize`.

### Extension Registry (global, versioned)

```json
{
  "extensions": {
    "lgt": {
      "version": "1.0.0",
      "parameters": {
        "dimension": { "type": "integer", "min": 1, "max": 4 },
        "latticeSize": { "type": "integer" },
        "betaValues": { "type": "array", "items": "number" },
        "gaugeGroup": { "type": "string", "enum": ["Z2", "U1", "SU2"] }
      }
    },
    "dmrg": {
      "version": "0.1.0",
      "parameters": {
        "chainLength": { "type": "integer" },
        "bondDimension": { "type": "integer" },
        "model": { "type": "string", "enum": ["Heisenberg", "Hubbard"] }
      }
    }
  }
}
```

New physics domain? Add one entry. Existing dashboards keep working.

### Observable Definitions (global, reusable)

```json
{
  "observables": {
    "plaquette": {
      "name": "Plaquette",
      "formula": "⟨∏_{□} σ⟩",
      "units": "dimensionless",
      "category": "gauge",
      "applicableTo": ["lgt"],
      "visualization": {
        "type": "line",
        "xAxis": "beta",
        "yAxis": "value",
        "yErr": "error"
      }
    },
    "binder_cumulant": {
      "name": "Binder Cumulant",
      "formula": "U_L = 1 - ⟨m⁴⟩/3⟨m²⟩²",
      "units": "dimensionless",
      "category": "critical",
      "applicableTo": ["lgt", "ising"],
      "visualization": { "type": "line", "xAxis": "beta", "yAxis": "value" }
    }
  }
}
```

New observable? Add one entry. No schema migration.

### Analysis Recipes (declarative, reproducible)

```json
{
  "analyses": [{
    "id": "t20-p3-fss-binder",
    "type": "finite_size_scaling",
    "inputs": {
      "observable": "binder_cumulant",
      "runs": ["t20-p3b-L8", "t20-p3b-L16", "t20-p3-L24", "t20-p3-L32"]
    },
    "parameters": {
      "criticalExponentNu": 0.63,
      "method": "binder_crossing"
    },
    "outputs": {
      "figure": "figures/t20-p3-fss-binder.png",
      "criticalBeta": 0.761,
      "criticalBetaErr": 0.002
    }
  }]
}
```

The dashboard can: "Show me all FSS analyses for 3D Z₂ LGT" without hardcoding T20 knowledge.

## Benefits

| Capability | Before | After |
|-----------|--------|-------|
| New physics domain | Fork + rewrite schema | Add extension namespace |
| New observable | Free-text guess | Register with formula + viz |
| Figure provenance | "t20-p3-fss.png" | Links to source runs + analysis recipe |
| Data discovery | Open file, inspect manually | Schema descriptor says columns + shape |
| Dashboard filter | Hardcoded LGT fields | Generic: "extension=lgt, dimension=3" |

## Migration Path

1. **Phase 1** (T29): Design + prototype schema v2.0
   - Write new schema JSON
   - Convert existing registry to new format
   - Validate: old dashboard still works with new schema

2. **Phase 2**: Update collation scripts
   - `collate-data.ts` outputs v2.0 format
   - Extension data extracted from simulation parameters

3. **Phase 3**: Dashboard v2 uses new schema
   - Generic filtering by extensions
   - Observable-aware plotting
   - Analysis recipe display

## Files

| File | Purpose | Status |
|------|---------|--------|
| `numerics/data/registry.schema.json` | Current schema (v1.0) | 🔄 Needs v2.0 |
| `numerics/schemas/base-registry.schema.json` | Base schema (physics-agnostic) | ⬜ Create |
| `numerics/schemas/extensions/lgt.schema.json` | LGT extension | ⬜ Create |
| `numerics/schemas/observables.schema.json` | Observable definitions | ⬜ Create |
| `numerics/src/scripts/migrate-registry.ts` | v1.0 → v2.0 converter | ⬜ Create |
| `memory-bank/implementation/extensible-schema-design.md` | This document | ✅ Created |
