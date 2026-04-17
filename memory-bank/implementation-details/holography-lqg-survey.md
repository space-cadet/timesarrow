---
title: Holography in LQG and Tensor Networks — Survey of Recent Work
created: 2026-04-18 02:30:00 IST
last_updated: 2026-04-18 02:30:00 IST
related_tasks: T12
author: Claude Sonnet 4.6
guide: Deepak Vaid
---

# Holography in LQG and Tensor Networks: Survey (2015–2026)

## Overview

Three overlapping programs connect loop quantum gravity / group field theory (GFT)
to holography via tensor networks. They share a common architecture: spin-network
states (bulk) are identified with tensor network states; the boundary emerges from a
bulk-to-boundary map; the Ryu-Takayanagi (RT) formula for entanglement entropy is
derived or approximated. They differ in their starting point (GFT vs. LQG kinematics
vs. random tensor networks) and the rigor of their results.

---

## I. Chirco–Colafranceschi–Oriti Program (GFT → TN → Holography)

The most systematic LQG-specific body of work. All papers use GFT/spin-network
states as the bulk input and derive holographic properties as outputs.

### Chirco, Oriti, Zhang (2017) — Foundational paper
- **arXiv**: 1701.01383 | **Journal**: Class. Quantum Grav. 35, 115011 (2018)
- Establishes dictionary between GFT states and generalized random tensor networks.
  Recovers RT formula in two approximation schemes. This is the starting point of the
  whole GFT–random-TN program.
- Relevance: RT formula derived from GFT partition function; Rényi entropy is the
  central quantity.

### Chirco, Goeßmann, Oriti, Zhang (2019) — Dynamical corrections to RT
- **arXiv**: 1903.07344 | **Journal**: Class. Quantum Grav. 37, 095011 (2020)
- Feynman networks from interacting GFT are a generalization of random tensor networks
  with dynamics. Proves RT formula is dynamically stable: linear corrections from
  polynomial perturbations to the Gaussian measure are negligible for a broad class
  of networks.
- Relevance: RT formula survives LQG dynamics, not just kinematics.

### Colafranceschi, Oriti (2020) — Second-quantized PEPS
- **arXiv**: 2012.12622 | **Journal**: JHEP 07 (2021) 052
- Proves GFT states are second-quantized PEPS. "Label independence" of the network
  is a discrete analog of diffeomorphism invariance. Distinguishability of space quanta
  recovered only relationally in semi-classical limit.
- Relevance: Most rigorous TN formulation of spin-network / GFT states.

### Colafranceschi, Chirco, Oriti (2021) — Holographic maps from spin networks
- **arXiv**: 2105.06454 | **Journal**: Phys. Rev. D 105, 066005 (2022)
- **Key result (proven)**: Classifies exactly which entanglement structures of
  GFT/spin-network states make the bulk-to-boundary map isometric (holographic in
  the QI sense). Isometry condition is purely an entanglement condition on the bulk state.
- Relevance: **Must-cite for this manuscript** — directly frames spin-network states
  as holographic codes.

### Chirco, Colafranceschi, Oriti (2021) — Bulk area law + horizon-like regions
- **arXiv**: 2110.15166 | **Journal**: Phys. Rev. D 105, 046018 (2022)
- **Key result (proven)**: RT formula recovered for spin-network boundary entanglement,
  with corrections from bulk entanglement. When bulk entanglement exceeds a threshold,
  RT minimal surface cannot penetrate the region — horizon-like behavior emerges.
- Relevance: Derives RT + bulk corrections from spin-network geometry explicitly.

### Colafranceschi, Adesso (2022) — Focused review
- **arXiv**: 2202.05116 | **Journal**: AVS Quantum Science 4, 025901 (2022)
- Comprehensive review of the holographic entanglement program for spin networks.
  Best entry point for a reader coming from quantum information.
- Relevance: **Must-cite** as the review covering the field this manuscript enters.

### Colafranceschi, Langenscheidt, Oriti (2022/2024) — Superposed geometries
- **arXiv**: 2207.07625 | Status: Preprint v3 (February 2024), not yet published
- Extends holographic analysis to quantum superpositions of discrete geometric data.
  Main results (typicality): bulk regions isometrically map onto boundary only when
  total area is fixed; area operator and fixed-area condition emerge from quantum
  channel analysis.
- Relevance: **Must-cite** — generalization to quantum superpositions directly
  relevant to superposed spin-network states in LQG cosmology.

---

## II. Muxin Han and Collaborators

### Han, Hung (2016) — LQG exact holographic mapping
- **arXiv**: 1610.02134 | **Journal**: Phys. Rev. D 95, 024011 (2017)
- Proves LQG spin-network states in a space with boundary implement an exact
  holographic mapping in the sense of Qi (2013). RT formula recovered in semi-classical
  limit with entropy proportional to minimal area surface.
- Relevance: **Must-cite** — the direct LQG realization of Qi's exact holographic map;
  already cited in manuscript as Han2016Loop.

### Han, Huang (2017) — Discrete gravity and holographic Rényi entropy
- **arXiv**: 1705.01964 | **Journal**: JHEP 11 (2017) 148
- Applies Regge calculus 3d Euclidean gravity to random tensor network framework.
  Boundary Rényi entropy equals on-shell Einstein action on branched cover;
  matches CFT₂ ground-state Rényi entropy precisely.
- Relevance: Bridges LQG (Regge gravity) and holographic entropy in random TN.

### Han (2025) — Spinfoam path integral and area-law entanglement
- **arXiv**: 2510.26925 | Status: Preprint (October 2025)
- Computes entanglement entropy from 4d Lorentzian LQG spinfoam path integral.
  Area law S ≈ βA proven in semi-classical approximation; Bekenstein-Hawking formula
  reproduced for Barbero-Immirzi parameter in range 0–0.5.
- Relevance: Most recent Han result; extends the program to 4d Lorentzian LQG.

---

## III. Qi Exact Holographic Mapping (Precursor)

### Qi (2013) — Exact holographic mapping
- **arXiv**: 1309.6282 | Status: Unpublished preprint (never journal-submitted)
- Proposes unitary map from d-dimensional boundary lattice to (d+1)-dimensional bulk,
  with bulk metric determined by boundary two-point correlations. Explicit construction
  for (1+1)d Dirac fermions. Entangled pairs map to wormhole geometry.
- Relevance: Foundational; cited by Han–Hung and others as the framework for "exact
  holographic mapping." Already cited as Qi2013Exact.

---

## IV. Swingle MERA / AdS-CFT

### Swingle (2009/2012) — Entanglement renormalization and holography
- **arXiv**: 0905.1317 | **Journal**: Phys. Rev. D 86, 065007 (2012)
- Identifies MERA with discrete AdS geometry; bulk direction = renormalization scale.
  Correlation functions in MERA reproduce AdS correlators. Black-hole-like objects
  for finite-temperature states.
- Relevance: Paradigmatic TN for discrete AdS holography; background for TN–LQG work.
  Already cited as Swingle2009Entanglement.

---

## V. Random Tensor Networks (Hayden et al.)

### Hayden, Nezami, Qi, Thomas, Walter, Yang (2016)
- **arXiv**: 1601.01694 | **Journal**: JHEP 11 (2016) 009
- **Key result (proven)**: For random tensors with large bond dimension, boundary
  entanglement entropy obeys RT formula exactly (from min-cut/Ising domain-wall
  calculation). Entanglement wedge reconstruction also proven. Topology transitions
  from increased bulk entanglement.
- Relevance: Standard benchmark; the Chirco–Colafranceschi–Oriti program is compared
  against these results.

---

## VI. HaPPY Holographic Error-Correcting Codes

### Pastawski, Yoshida, Harlow, Preskill (2015)
- **arXiv**: 1503.06237 | **Journal**: JHEP 06 (2015) 149
- Perfect-tensor quantum error-correcting codes on hyperbolic tilings. Proven:
  RT formula exactly satisfied; bulk operator reconstruction on disjoint boundary
  regions; negative tripartite information matching AdS/CFT.
- Relevance: Most explicit TN proof of RT + operator reconstruction; standard
  reference for QECC in quantum gravity.

### Tobin (2025) — LQG and quantum error correction
- **arXiv**: 2510.26911 | Status: Preprint (October 2025)
- Adapts QECC to LQG gauge-invariant Hilbert space (which does not factorize;
  requires von Neumann algebra formulation). Proves RT formula at LQG kinematic level;
  Bekenstein-Hawking entropy reproduced from area-constrained canonical ensemble.
- Relevance: Direct LQG implementation of HaPPY-type QECC logic.

---

## VII. Spin Networks from Gauged MERA (Singh et al.)

### Singh, McMahon, Brennen (2017)
- **arXiv**: 1702.00392 | **Journal**: Phys. Rev. D 97, 026013 (2018)
- Shows lifting MERA representation of 1d system with global G-symmetry to 2d bulk
  naturally produces G-gauged spin-network states. Provides concrete realization of
  boundary-global-symmetry ↔ bulk-gauge-symmetry dictionary.
- Relevance: **Particularly relevant to this manuscript** — gauging a global symmetry
  (time-reversal Z₂) on the boundary produces a gauge structure in the bulk, directly
  analogous to the manuscript's program.

### Singh (2017)
- **arXiv**: 1701.04778 | **Journal**: Phys. Rev. D 97, 026012 (2018)
- Any TN represents two quantum many-body states (bulk and boundary). CFT properties
  extractable from bulk; boundary operators map to extended bulk operators.

---

## VIII. Additional Notable Work

### Czelusta, Mielczarek (2024)
- **arXiv**: 2410.18812 | **Journal**: Phys. Rev. D 111, 066012 (2025)
- Direct TN representations of SU(2) spin-network states; qubit efficiency over
  quantum-circuit methods; explicit holographic bulk-boundary implementation.
- Relevance: Most recent direct TN construction of LQG spin-network states.

### Akers, Penington (2021)
- **arXiv**: 2109.14618 | **Journal**: SciPost Phys. 12, 157 (2022)
- Proves state-specific reconstruction ↔ quantum minimal surface formula.
  Generalizes HaPPY/Harlow without fixed entanglement wedge.
- Relevance: Modern QECC result; pair with Dennis et al. in QECC discussion.

### Donnelly, Freidel (2016)
- **arXiv**: 1601.04744 | **Journal**: JHEP 09 (2016) 102
- Edge modes and entanglement in gauge theories and gravity. Boundary degrees of
  freedom needed to define local subsystems in LQG.
- Relevance: Edge modes are the boundary degrees of freedom in the holographic picture;
  connects to manuscript's edge-modes conjecture (Sec 6.4 / T12/M10).

---

## Synthesis and Citation Guidance for the Manuscript

| Section | Recommended additions |
|---------|----------------------|
| Introduction / Sec 4 | Colafranceschi-Adesso review (2202.05116); Jahn-Eisert review (2102.02619) |
| Sec 4 (spin networks as TN) | Colafranceschi-Chirco-Oriti (2105.06454); Singh-McMahon-Brennen (1702.00392) |
| Sec 5 (SPT-LQG mapping) | Chirco-Colafranceschi-Oriti (2110.15166); Czelusta-Mielczarek (2410.18812) |
| Discussion (QECC) | Akers-Penington (2109.14618); Tobin (2510.26911) |
| Discussion (edge modes) | Donnelly-Freidel (1601.04744) |

The Singh–McMahon result is the most directly relevant to the manuscript's specific
program (gauging a global symmetry → spin-network gauge structure), and has not been
cited. It should be added.
