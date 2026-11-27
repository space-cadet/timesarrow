# Intertwiner-chain gluing and a candidate spin-one excitation

Recorded 27 November 2026. The [full dialogue](<transcripts/Intertwiner chain and triplet joining — transcript.md>) preserves the discussion, including the author's notation requests and final figure feedback.

## Two neighboring nodes

We continued the previous one-node calculation with two four-valent spin-one-half intertwiners. Their physical orientation states are $|s\rangle=(|\Phi_1\rangle+i s|\Phi_2\rangle)/\sqrt2$, with $s=\pm1$. Physical labels $s,t$ are distinct from magnetic indices $a,b,c,m,n,d,e,f=0,1$. Both shared legs are outgoing, ordered left then right. Six outer magnetic legs remain open.

Define $I^s_{abcm}=\langle a,b,c,m|s\rangle$ and $I^t_{ndef}=\langle n,d,e,f|t\rangle$. The normalized singlet pairing is $\epsilon_{01}=1/\sqrt2$, $\epsilon_{10}=-1/\sqrt2$, with other components zero. Reversing its ordering reverses its sign.

$$
G^{st}_{abcdef}=2\sum_{m,n=0}^{1}I^s_{abcm}\epsilon_{mn}I^t_{ndef}.
$$

The factor two normalizes this two-node contraction: each shared leg has reduced density matrix $I/2$, and the normalized singlet contraction has squared norm $1/4$. The four resulting orientation-labeled states are orthonormal. Direct numerical checks gave maximum Gram error $3.3\times10^{-16}$. The real-basis example gives $2\langle\epsilon|_{mn}(\Phi_{1,A}\otimes\Phi_{1,B})=-|\epsilon\rangle_{ab}|\epsilon\rangle_{cd}|\epsilon\rangle_{ef}$, checked to $5.6\times10^{-17}$. Spin time reversal exchanges both orientation signs after singlet gluing, with zero residual in the explicit check.

## The state expression and pedagogical choices

The author requested explanation of coefficient indices, then preferred writing the pairing itself as $\epsilon_{mn}$. Independent sums and the difference between retained physical labels and contracted magnetic labels were made explicit.

Write $|A_m^s\rangle=\sum_{a,b,c}I^s_{abcm}|a,b,c\rangle$ and $|B_n^t\rangle=\sum_{d,e,f}I^t_{ndef}|d,e,f\rangle$. These conditional three-leg states are unnormalized, with inner products $\delta_{mn}/2$. Then

$$
|G_{st}\rangle=\sqrt2\left(|A_0^s\rangle|B_1^t\rangle-|A_1^s\rangle|B_0^t\rangle\right).
$$

Normalizing each conditional vector makes the Bell-singlet form explicit. This entanglement is between the remaining three-leg systems for fixed chosen intertwiners; it is distinct from entanglement between the physical orientation labels themselves.

The author remembered this construction correctly. The thermal-intertwiners transcript *Coherent dipoles and cosmology*, 18 November, messages 13–14 and 19–20, already identified two chosen FL coherent intertwiners joined by a shared-leg Bell singlet. Its physical note, lines 113–129, gives the general spin-$j$ contraction. Today's chosen node states are orientation eigenstates rather than FL coherent states. Local earlier references are `memory-bank/implementation/t35b-encoded-tetrahedral-czx-spec.md`, section 2.3, and the Bell-state figure at `timesarrow.tex:1019`. The former uses an unnormalized epsilon tensor. The link operation agrees; this does not identify every node-state choice with an entire Bell-network state.

## Arbitrary pairings and the triplet

An arbitrary normalized pure two-spin state $|\chi\rangle=\sum c_{mn}|m,n\rangle$ supplies the bra tensor $E_{mn}=c_{mn}^{*}$. The joined state is $2\sum E_{mn}|A_m^s\rangle|B_n^t\rangle$. The same two-node normalization holds. The singlet is singled out by invariance under common SU(2) rotations.

The triplet states are $|T_+\rangle=|00\rangle$, $|T_0\rangle=(|01\rangle+|10\rangle)/\sqrt2$, and $|T_-\rangle=|11\rangle$. Their pairing matrices are respectively $\mathrm{diag}(1,0)$, $\frac1{\sqrt2}\begin{pmatrix}0&1\\1&0\end{pmatrix}$, and $\mathrm{diag}(0,1)$. The middle triplet yields the plus-sign Bell combination of conditional states; the extremal triplets yield products. A triplet projection leaves total spin one on the six outer legs. Under the outgoing convention, projection onto shared-leg magnetic component $M$ leaves outer component $-M$; a dual-basis identification converts to a conventional spin-one basis.

## The author's particle proposal

Deepak proposed interpreting the three triplet joining states as the states of a spin-one particle. Their representation content is exact: $\frac12\otimes\frac12=0\oplus1$ and the triplet Casimir is two in units $\hbar=1$. Selecting singlet links as a reference and replacing one edge $e$ by a triplet gives candidate localized states $|e,M\rangle$. This is a model proposal. No hopping operator, energy spectrum, stable vacuum, continuum spacetime spin identification, or particle propagation was derived. A retained spin-one index must be balanced by appropriate geometry, boundaries, or other excitations in an invariant complete state. The discussion cited Mansuroglu–Sahlmann, [arXiv:2011.13848](https://arxiv.org/abs/2011.13848), as related arbitrary-spin matter kinematics, without claiming that paper derives this proposal.

Next physics step: specify a transfer operator and determine whether a triplet insertion propagates along the physical intertwiner chain. Norms and independence for a longer chain require their own calculation.

## Figure drafts and explicit next-session direction

Created `figures/intertwiner-chain/`: three TikZ drawings with shared style, individual wrappers, reproducible build script, individual vector PDFs, 300 dpi PNGs, combined three-page PDF, and notation README. They show the two-node joining, reference chain versus one triplet insertion, and the three triplet pairings. The blocks sit directly on the connecting edges. Dashed violet legs distinguish physical labels from solid magnetic legs. The chain diagram retains $M$ as an extra leg of $E_{mnM}$.

All three renders were visually inspected. Final LaTeX compilation reported no warnings or overflowing boxes; fonts were embedded, PNG resolution verified at 300 dpi, and margins checked. The displayed four pairing matrices were checked for orthonormality and Casimirs zero/two. No manuscript build, release, commit or push occurred in this session.

The author accepted the direction but requested paper figures without the mathematical insets and a prettier tensor-network layout. Those revisions are explicitly deferred to a new session. These are explanatory drafts, not final approved paper figures. Resume with that redesign before further figure polishing; preserve the editable sources and distinguish a fixed two-leg triplet block from the family with its retained third index.
