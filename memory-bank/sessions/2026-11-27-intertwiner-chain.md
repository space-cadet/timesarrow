---
source_branch: main
source_commit: b705dd59c3da526420bc2abc9c38d020125386b1
---

# Session 2026-11-27 — Intertwiner chain and triplet joining

*Created: 2026-11-27 13:09:40 IST*
*Last Updated: 2026-11-27 13:09:40 IST*

## Work completed

- Continued from the checked one-node orientation calculation and joined two four-valent spin-one-half intertwiners along one shared magnetic leg.
- Kept physical orientation indices $s,t$ separate from magnetic indices; wrote the invariant pairing as $\epsilon_{mn}$ and explained the contraction in both index and state notation.
- Fixed the outgoing-leg convention and singlet normalization. The factor two gives an orthonormal family of four joined orientation states. An explicit real-basis example and the antiunitary time-reversal action were checked numerically.
- Located the matching one-link Bell-singlet construction in the 18 November thermal-intertwiners discussion. The shared-leg operation is the same; the node-state family here uses orientation intertwiners rather than FL coherent intertwiners.
- Generalized the joining tensor to an arbitrary two-spin bra. The triplet tensors form a spin-one representation; their $M=0$ channel gives an entangled Bell-type contraction, while $M=\pm1$ give product conditional states.
- Recorded the author's proposal to interpret a triplet insertion as a candidate localized spin-one excitation. Its status remains a proposal: no transfer dynamics or spectrum has been derived.
- Created three editable TikZ figures, their PDF and 300 dpi PNG exports, a combined three-page PDF, a build script, and notation guidance in `figures/intertwiner-chain/`. LaTeX compiled without warnings; all three figures were visually inspected.

## Records

- [Complete chronological transcript](../../notes/transcripts/Intertwiner chain and triplet joining — transcript.md)
- [Physical summary and calculation record](../../notes/intertwiner-chain-physical-summary.md)
- [Figure set and sources](../../figures/intertwiner-chain/README.md)

## Open work and author direction

The chain transition operator and propagation of the triplet insertion remain open. Part II task owners T3b and T3c cover state/model selection and transfer/sewing respectively. For the next figure session, remove the mathematical insets and refine the tensor-network layout for paper use. No manuscript figure integration or paper build was done. T12 remains paused; no task status changed. No commit or push was made.
