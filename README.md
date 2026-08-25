# Gauging Time Reversal Symmetry in Quantum Gravity

> **Arrow of Time from a Confinement–Deconfinement Transition**

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Build](https://img.shields.io/badge/Build-Passing-brightgreen)]()

This repository contains the manuscript, figures, and supplementary materials for the paper **"Gauging Time Reversal Symmetry in Quantum Gravity: Arrow of Time from a Confinement–Deconfinement Transition"** by Deepak Vaid.

---

## Abstract

This paper proposes that coherent cosmological time orientation can emerge as a gauge phenomenon. Binary tensor-network structure and paired signs of the LQG signed-volume operator motivate an effective $Z_2$ orientation field in a restricted four-valent $j=1/2$ spin-network sector. Adopting the minimal Wilson action gives a concrete mechanism:

- **Confined phase** — relative orientation cannot be transported coherently over macroscopic distances.
- **Deconfined phase** — long-distance orientation transport is coherent, as diagnosed by non-local gauge observables.

This is an effective proposal, not a completed derivation of the link field, Wilson coupling, semiclassical geometry, or cosmological trajectory from spin-foam dynamics. CZX is used as a controlled tensor-network reference construction, not identified with the projected LQG state. The numerical results are bounded controls of the adopted gauge theory and include a negative result for a tested signed-volume diagnostic.

---

## What's in This Repository

| Path | Description |
|------|-------------|
| `timesarrow.tex` | Main LaTeX manuscript source (SciPost template) |
| `arxiv_submission_v1/` | Clean arXiv submission bundle (44 pages, 34 figures) |
| `arxiv-submission-v1.tar.gz` | Ready-to-upload tarball |
| `figures/` | TikZ source files and PNG diagrams |
| `supplementary-calculations.tex` | Detailed derivations for corrected arguments |
| `web-static/` | Static HTML web presentation of the paper |
| `memory-bank/` | Project memory bank (tasks, sessions, implementation docs) |
| `ai-assistance-statement.md` | Detailed statement of AI-assisted contributions |
| `cover-letter.md` | Submission cover letter for SciPost Physics |

---

## Building the Paper

Requires a standard LaTeX distribution with `biber` (tested on TeX Live 2024):

```bash
# Build the manuscript
pdflatex timesarrow.tex
biber timesarrow
pdflatex timesarrow.tex
pdflatex timesarrow.tex

# Or use the build script
./buildtex
```

> **Note for Apple Silicon users:** If `biber` fails with architecture mismatch, see `memory-bank/implementation-details/biber-infrastructure-fix.md`.

---

## Numerics & Simulation Code

This repository includes two numerical components for reproducing the paper's lattice gauge theory results:

### TypeScript (`numerics/`)
- **Purpose:** Spin-network utilities, intertwiner computations, Z₂ lattice gauge theory configuration tools
- **Requirements:** Node.js 18+ (tested on Node.js 22.x)
- **Build:**
  ```bash
  cd numerics
  npm ci
  npx tsc --strict --noEmit
  ```

### Rust (`rust-lattice/`)
- **Purpose:** High-performance Monte Carlo simulations of Z₂ lattice gauge theory (2D–4D)
- **Requirements:** Rust 1.92.0, pinned by `rust-toolchain.toml` (edition 2024)
- **Build & test:**
  ```bash
  cd rust-lattice
  cargo check
  cargo test
  ```

### Full validation
Run `./scripts/validate.sh` from the repository root to check the TypeScript build, Rust build, ordinary Rust tests, and Rust doctests. When local `cargo`/`rustc` proxy links are unavailable, the script resolves the pinned compiler tools directly through `rustup`. It exits with a non-zero status if any step fails.

---

## Key Results

1. **Effective orientation proposal:** a $Z_2$ link field motivated by binary bond data and paired signed-volume sectors in the restricted $j=1/2$ setting.
2. **Concrete mechanism:** confinement obstructs long-distance orientation comparison; deconfinement permits it, with Wilson and Polyakov observables providing gauge-invariant controls.
3. **Microscopic boundary:** an explicit operator calculation shows that the literal CZX unitary does not preserve the full $SU(2)$ singlet intertwiner subspace, so a new encoding map is required.
4. **Reproducible numerical controls:** canonical raw datasets and scripts locate the expected transition region; the tested signed-volume dressing is retained as a negative result.
5. **Falsifiable next step:** derive, modify, or rule out the effective field, action, and cosmological trajectory using microscopic spin-foam dynamics.

---

## Web Presentation

An interactive web presentation translating the paper's concepts for a broader audience is in development:

- **Static version**: [`web-static/`](web-static/) — deployed landing page
- **Planned**: Next.js interactive scrollytelling app with animated spin networks, vertex explorer, and tiered narrative (see `memory-bank/implementation-details/gemini-web-presentation-plan.md`)

---

## AI Assistance Statement

This manuscript originated as the author's independent work (2016–2018). During the April 2026 revision, Claude (Anthropic) was used as a writing assistant for formalization, LaTeX editing, bibliography management, and error correction. **All physical ideas, arguments, and conclusions are the author's own.**

A complete, commit-level account of AI-assisted contributions is available in:
- [`ai-assistance-statement.md`](ai-assistance-statement.md)
- The publicly auditable git history of this repository

---

## Citation

If you use this work, please cite:

```bibtex
@article{vaid2026gauging,
  title={Gauging Time Reversal Symmetry in Quantum Gravity: 
         Arrow of Time from a Confinement--Deconfinement Transition},
  author={Vaid, Deepak},
  journal={SciPost Physics},
  year={2026},
  url={https://github.com/space-cadet/timesarrow}
}
```

---

## Author

**Deepak Vaid** — Independent Researcher  
📧 dvaid79@gmail.com  
🌐 [GitHub: @space-cadet](https://github.com/space-cadet)

---

## License

The manuscript text and figures are © 2026 Deepak Vaid. Code and build scripts are released under the MIT License.
