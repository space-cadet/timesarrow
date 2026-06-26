# Technical Context
*Last Updated: 2026-04-16 20:15:00 IST*

## Tech Stack
- **Document Preparation**: LaTeX
- **Journal Template**: SciPost (via `SciPost.cls`)
- **Bibliography Management**: BibLaTeX with Biber backend (`timesarrow.bib`)
- **Graphics**: 
  - `graphicx` for external figures.
  - TikZ (via `pytikz.py` script) for programmatic diagrams.
  - Draw.io (`tensor networks.drawio`) for conceptual diagrams.

## Core Concepts
- **Loop Quantum Gravity (LQG)**: Spin networks, volume operator, tetrad/connection formalism, ADM splitting.
- **Condensed Matter Theory (CMT)**: Topological Order (TO), Symmetry Protected Topological (SPT) phases, CZX model, Matrix Product States (MPS).
- **Quantum Information**: Tensor Network States (TNS), entanglement entropy, Ryu-Takayanagi formula.

## Development Workflow
- **Build Tool**: `/Volumes/Data/owncloud/root/research/articles/timesarrow/buildtex` (custom script).
- **Reference Management**: Biber is used to process citations from `timesarrow.bib`.
- **Note Taking**: `todonotes` package used for internal manuscript comments.

## Infrastructure
- **Base Paths**:
  - Figures: `/Volumes/Data/owncloud/root/research/articles/timesarrow/figures/`
  - References: `/Volumes/Data/owncloud/root/research/articles/timesarrow/bridgeman-chubbs/` (local reference PDFs).

## Numerics Documentation Workflow

*Added: 2026-06-26*

Every time `.qmd` files in `numerics/docs/` change, follow this exact workflow:

1. **Edit** `.qmd` files in `timesarrow/numerics/docs/`
2. **Update `date-modified`** timestamp in YAML frontmatter (both YAML and body text if present)
3. **Commit** to timesarrow repo
4. **Render** HTML: `quarto render file.qmd --to html` (individual file, not project render — hangs)
5. **Copy** rendered `.html` to `space-cadet.github.io/projects/timesarrow/numerics/` (preserve subdirectory structure)
6. **Commit and push** gh-pages repo (`space-cadet.github.io`)

**Critical**: Update timestamps on **EVERY** change. Forgetting requires amending commits on both repos.

**Live site**: https://space-cadet.github.io/projects/timesarrow/numerics/

## Simulation Script Requirements

*Added: 2026-06-26*

**ALL simulation scripts MUST be checkpointable and resumable.** This is non-negotiable.

### Why
- Subagents get killed after timeouts
- Context compaction kills long-running sessions
- System restarts happen
- Rust batch processes take 1-2 hours per L value

### Requirements

1. **Incremental writes**: Save results after EACH β value or batch, not just at the end
2. **`--resume` flag**: Check existing output file, skip completed β values, continue from where left off
3. **Atomic writes**: Write to `.tmp` file, then `mv` to final name — never leave corrupted JSON
4. **Progress logging**: Print status after each β so we can see progress without checking files
5. **Test the resume path**: Verify that running with `--resume` on partial data actually works

### Anti-Patterns (Don't Do This)

❌ Collect all results in memory, write one big JSON at the end
❌ Overwrite output file without checking what's already there
❌ Leave orphaned Rust processes when Python parent dies
❌ Assume the script will run to completion in one go

### Example Pattern (t20-sim-3d-fss-v2.py)

```python
# Load existing data
if resume and outfile.exists():
    existing = load_existing_results(outfile)
    completed_betas = {r["beta"] for r in existing["results"]}
    remaining_betas = [b for b in betas if b not in completed_betas]
else:
    remaining_betas = betas

# Run remaining
for beta in remaining_betas:
    result = run_single_beta(beta)
    all_results.append(result)
    save_results(outfile, {"results": all_results})  # Incremental write!
```

## Rust Checkpointing Pattern

*Added: 2026-06-26*

For Rust binaries, implement checkpointing via `--checkpoint <path>`:

1. **Read existing checkpoint** on startup → skip completed work
2. **Use mpsc channel** instead of `.collect()` for streaming results
3. **Main thread writes incrementally** — append after each result
4. **Atomic writes**: `.tmp` → `rename` to avoid corruption
5. **Python wrapper** passes checkpoint path, handles retry logic

See: `implementation-details/t20-rust-checkpointing.md`

## Data Collation Pattern

*Added: 2026-06-26*

All simulation outputs should be registered in `numerics/data/registry.json`:

1. **Filename convention**: `t{task}-p{phase}-L{size}-{date}.json`
2. **Run collation script** after batch: `npx ts-node --esm src/scripts/collate-data.ts`
3. **Copy snapshot** for dashboard: `cp data/registry.json docs/data-registry.json`
4. **Commit registry changes** with the data

See: `implementation-details/t20-data-collation.md`
