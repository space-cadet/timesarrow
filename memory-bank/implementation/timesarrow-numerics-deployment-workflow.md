# Workflow: Rebuilding and Redeploying TimesArrow Numerics Pages

*Documented: 2026-06-26*

## Overview

The TimesArrow numerics documentation is built with Quarto and deployed to GitHub Pages via the `space-cadet.github.io` repository. This workflow documents the exact steps for rebuilding and redeploying.

## Prerequisites

- `quarto` CLI installed (`/usr/local/bin/quarto`)
- Write access to `space-cadet/space-cadet.github.io` (via HTTPS `gh` auth)
- Write access to `space-cadet/timesarrow` (source repo)

## Repository Layout

| Repo | Path | Purpose |
|------|------|---------|
| `timesarrow` | `numerics/docs/` | Quarto source (`.qmd` + assets) |
| `timesarrow` | `numerics/output/` | Raw JSON simulation data |
| `timesarrow` | `numerics/docs/assets/` | Generated plots (PNG/SVG) |
| `space-cadet.github.io` | `projects/timesarrow/numerics/` | Deployed HTML + assets |

## Workflow Steps

### 1. Generate New Data (if needed)

Run Rust simulations to produce raw JSON data:

```bash
cd timesarrow/rust-lattice
cargo build --release
./target/release/z2-lattice-gauge <L> <dim> <measure_sweeps> <thermal_sweeps> <workers> "<loop_sizes>" <beta_values...> \
  > ../numerics/output/<filename>.json
```

### 2. Generate Plots

Python scripts in `numerics/src/scripts/` process raw data into plots:

```bash
cd timesarrow/numerics
python3 src/scripts/t20-plot-phase3-fine-multi.py
# → creates docs/assets/t20-p3-*-multi.png/svg
```

### 3. Update Quarto Source + Timestamps

Edit the `.qmd` file to reference new figures. **Critical: Update timestamps.**

#### Timestamp Format (IST)

Use the exact format: `YYYY-MM-DD HH:MM IST` for inline text, **ISO 8601 with timezone offset** for YAML:

```yaml
---
date: "2026-06-25"
date-modified: "2026-06-26T02:47:00+05:30"
---
```

Also update the running text timestamp:

```markdown
*Last updated: 2026-06-26 02:47 IST*
```

**Why both?** The YAML `date-modified` is machine-readable (Quarto uses it for metadata, needs ISO 8601). The inline text is human-readable for readers checking currency. Keep them synchronized.

**⚠️ Quarto pitfall**: `date-modified: "2026-06-26 02:47 IST"` renders as **"Invalid Date"** because Quarto expects ISO 8601. Use `+05:30` offset instead.

#### Figure Management

- Use relative paths: `../assets/<filename>.png`
- Keep figure numbering sequential through document
- Include multi-lattice overlays when L-series data exists
- Add alt text / captions that describe what the reader should see

#### Checklist before rendering

- [ ] `date-modified` updated in YAML frontmatter
- [ ] Inline "Last updated" text matches
- [ ] New figures referenced with correct paths
- [ ] Figure captions describe the physics takeaway
- [ ] No broken figure references (check `../assets/` path)

### 4. Render HTML

```bash
cd timesarrow/numerics/docs
quarto render tasks/t20-z2-lgt.qmd --to html
# → creates tasks/t20-z2-lgt.html
```

### 5. Copy to space-cadet.github.io

```bash
# HTML
cp timesarrow/numerics/docs/tasks/t20-z2-lgt.html \
   space-cadet.github.io/projects/timesarrow/numerics/tasks/

# Assets
cp timesarrow/numerics/docs/assets/t20-p3-*-multi* \
   space-cadet.github.io/projects/timesarrow/numerics/assets/
```

### 6. Commit and Push Both Repos

```bash
# Source repo (timesarrow)
cd timesarrow
git add -A
git commit -m "docs: Description of changes"
git push

# Deploy repo (space-cadet.github.io)
cd space-cadet.github.io
git add -A
git commit -m "docs: Description of changes"
git push
```

### 7. Verify Deployment

GitHub Pages rebuilds automatically on push to `main`. Verify at:

```
https://space-cadet.github.io/projects/timesarrow/numerics/tasks/t20-z2-lgt.html
```

CDN caching may delay updates by 1–5 minutes. Force refresh with `Cmd+Shift+R` or `?nocache=1`.

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Single-lattice plots only | Always generate multi-lattice overlays when L-series data exists |
| Forgot to copy assets | Check `assets/` in both source and deploy repos |
| Quarto render fails | Check `date-modified` format is valid YAML |
| GitHub Pages stale | Wait 1–5 min, or force refresh browser |
| Figure numbering broken | Re-number sequentially after inserting new figures |
| **Stale timestamps** | **Update `date-modified` AND inline "Last updated" text** |
| Mismatched timestamps | YAML and inline text must match — readers notice |
| IST vs UTC confusion | User is IST (GMT+5:30); use IST for human text, ISO 8601 for machine |

## Timestamp Policy

All TimesArrow numerics pages use **IST timestamps** (user timezone) for human-readable dates, **ISO 8601** for machine-readable metadata:

```yaml
# YAML frontmatter (machine)
date-modified: "2026-06-26 02:47 IST"

# Inline text (human)
*Last updated: 2026-06-26 02:47 IST*
```

**Rule**: If you update content, you must update timestamps. The inline text is a promise to the reader that the page reflects current data.

## Related Files

- `timesarrow/numerics/docs/_quarto.yml` — Project config
- `timesarrow/numerics/docs/tasks/t20-z2-lgt.qmd` — Main task doc
- `timesarrow/numerics/src/scripts/t20-plot-*.py` — Plotting scripts
- `timesarrow/rust-lattice/src/main.rs` — Simulation CLI
