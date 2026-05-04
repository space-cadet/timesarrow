# Gauging Time Reversal Symmetry in Quantum Gravity

> **Arrow of Time from a Confinement–Deconfinement Transition**

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Build](https://img.shields.io/badge/Build-Passing-brightgreen)]()

This repository contains the manuscript, figures, and supplementary materials for the paper **"Gauging Time Reversal Symmetry in Quantum Gravity: Arrow of Time from a Confinement–Deconfinement Transition"** by Deepak Vaid.

---

## Abstract

The question of the origin of time's arrow is a major outstanding problem in physics. Here we present a mechanism for the emergence of a cosmological arrow of time from a confinement–deconfinement transition in a $Z_2$ lattice gauge theory living on the spin-network states of Loop Quantum Gravity (LQG). Following Chen and Vishwanath, who showed that time-reversal symmetry can be gauged on tensor network states, and using the spin-network/tensor-network correspondence, we introduce a $Z_2$ gauge field on spin networks encoding a local time-reversal symmetry. The effective theory of this gauge field contains:

- **Confined phase** — a pre-geometric "quantum gravitational foam" with no coherent arrow of time.
- **Deconfined phase** — semiclassical spacetime with a uniform cosmological arrow, detected by the Wilson loop order parameter.

The deconfined phase is further shown to correspond to a symmetry-protected topological (SPT) phase of the CZX type, whose topological order provides additional stability of the coherent time orientation against local perturbations. We conjecture that the topologically protected surface excitations of this SPT phase give rise to fermionic matter degrees of freedom.

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

## Key Results

1. **Local $Z_2$ gauge field on spin networks** as the microscopic representation of time-reversal symmetry in LQG, with a derived $Z_2$ lattice gauge theory effective action.
2. **Cosmological arrow of time** identified with the confinement–deconfinement transition, with the Wilson loop as the order parameter (consistent with Elitzur's theorem).
3. **Structural correspondence** between 4-valent $j=1/2$ LQG intertwiners and the CZX model, verified by an explicit operator computation.
4. **SPT phase identification** of the deconfined phase, linked to the 3D bosonic SPT classification $H^4(Z_2^T, U(1)_\mathcal{T}) \cong \mathbb{Z}_2$.
5. **Conjecture** that surface excitations yield fermionic matter, supported by group cohomology, black-hole entropy arguments, and the all-fermion toric code.

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
