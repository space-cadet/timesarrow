# Intertwiner-chain joining figures

Three editable TikZ figures, exported as vector PDF and PNG at 300 dpi. The combined three-page file is [intertwiner-chain-figures.pdf](intertwiner-chain-figures.pdf).

| Figure | Content | Files |
| --- | --- | --- |
| 01 | Two four-valent nodes joined by an edge tensor; singlet and middle-triplet matrices | [PDF](01-two-node-contraction.pdf), [PNG](01-two-node-contraction.png), [TikZ](01-two-node-contraction.tikz) |
| 02 | Five-node singlet reference chain and one triplet insertion, with its spin-one index retained | [PDF](02-chain-triplet-insertion.pdf), [PNG](02-chain-triplet-insertion.png), [TikZ](02-chain-triplet-insertion.tikz) |
| 03 | Three triplet channels, their states, and their pairing matrices | [PDF](03-triplet-multiplet.pdf), [PNG](03-triplet-multiplet.png), [TikZ](03-triplet-multiplet.tikz) |

Solid slate lines carry magnetic indices. Dashed violet lines carry physical intertwiner labels. Pale teal blocks denote the singlet pairing $\epsilon$; amber blocks denote triplet pairings $E^{(M)}$. Each node has four magnetic legs. The physical index is a separate index of the intertwiner tensor.

All magnetic legs have $j=1/2$. Bits mean $0=\uparrow$, $1=\downarrow$. Both legs at a joining are written as outgoing representations, with the left index preceding the right. The pairing tensor is a bra coefficient: $E_{mn}=\langle\chi|m,n\rangle=c_{mn}^{*}$ for $|\chi\rangle=\sum_{m,n}c_{mn}|m,n\rangle$. The displayed singlet and triplet coefficients are real. Every pairing has unit Frobenius norm.

For two normalized four-leg singlet intertwiners, contraction with a normalized two-spin bra has squared norm $1/4$. Figure 01 therefore includes the factor $2$ in the normalized boundary tensor. This is the two-node normalization; it is not a claim that an arbitrary chain is normalized by a factor $2$ per link.

In Figure 02, $E_{mnM}=E^{(M)}_{mn}$ retains the triplet component as an additional open index. Fixing $M$ recovers the two-leg block used in the other drawings. A spin-one index must be coupled to appropriate additional data when imposing invariance on a complete closed state. $M$ labels the projected shared-leg triplet: under the stated outgoing convention, its bra leaves the six external legs with opposite total magnetic component. A conventional dual-basis identification converts this to a standard spin-one basis.

The triplet insertion is a candidate localized spin-one excitation. No propagation law, energy spectrum, or particle dynamics is encoded in these static drawings. The singlet reference is a specified configuration, not a calculated ground state.

Run `./build.sh` from this folder (or invoke it by path) to regenerate all exports. It requires `pdflatex`, TikZ, `newtxmath`, `sourcesanspro`, `fix-cm`, Poppler's `pdfseparate` and `pdftoppm`, and `rg`. Compiler output is saved to a temporary log. Standalone `.tex` wrappers are included for individual editing; `figure-set.tex` builds the full set. Shared typography, colors, and drawing macros are in `style.tex`.
