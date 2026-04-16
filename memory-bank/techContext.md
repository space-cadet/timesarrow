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
