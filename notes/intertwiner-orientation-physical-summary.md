# Intertwiner orientation, the worldsheet proposal, and the next chain calculation

*Discussion: 26 November 2026 16:17:01–27 November 2026 01:30:50 IST.*

<< Sol 6.1 Medium Begin >>

This note records Deepak Vaid's research direction, the collaboratively checked single-node calculation, the approved manuscript changes, and the unfinished chain construction. The [complete chronological transcript](<transcripts/Intertwiner orientation — transcript.md>) preserves the original dialogue, including intermediate errors and corrections. This summary states the corrected account. It does not replace the manuscript derivation.

## 1. Why a two-dimensional lattice might be appropriate

Deepak proposed connecting timesarrow with the recent lqg-strings-p2 and hopf-lqg work. If the two-dimensional tensor network describes a string worldsheet, its dimension has a physical explanation: one direction runs along a string and the other describes its history. The surrounding geometry may have more spatial dimensions.

This is a promising interpretation, not a completed mapping. The original CZX model is a quantum system in two spatial dimensions, with a 2+1-dimensional spacetime description. A candidate string worldsheet has one spatial direction and one history direction. Reinterpreting a CZX ground-state contraction as a history requires an explicit transfer construction and identification of its state spaces, symmetry action, and observables. The original CZX phase classification does not follow from redrawing its lattice.

Two routes were distinguished: construct a 1+1-dimensional intertwiner-chain theory carrying the orientation variable, or investigate the 1+1-dimensional history of the boundary of a 2+1-dimensional CZX system. The first is closer to Part II's current chain-first proposal. Hopf/ribbon composition may help define joining and braiding, but supplies neither a selected local dynamics nor a demonstrated continuum worldsheet by itself.

Even a successful orientation-carrying string theory would leave the cosmological question: how do its strings and their interactions produce orientation coherence in the surrounding geometry? No answer was derived here.

## 2. One node: conventions and physical state space

All four legs are outgoing and carry spin one half. In leg order 1234,

$$
|0\rangle=|\uparrow\rangle,\qquad |1\rangle=|\downarrow\rangle,
\qquad J_e^a=\frac12\sigma_e^a,\qquad \hbar=1.
$$

Gauge invariance imposes closure:

$$
(\mathbf J_1+\mathbf J_2+\mathbf J_3+\mathbf J_4)|\psi\rangle=0.
$$

The invariant space has dimension two. Pairing legs 12 and 34 gives one singlet from the pair-spin sectors 0 tensor 0 and one from 1 tensor 1. The common orthonormal basis now used in the main text and supplement is

$$
|\Phi_1\rangle=\frac12
(|0101\rangle-|0110\rangle-|1001\rangle+|1010\rangle),
$$

$$
|\Phi_2\rangle=\frac1{\sqrt{12}}
(2|0011\rangle-|0101\rangle-|0110\rangle-|1001\rangle-|1010\rangle+2|1100\rangle).
$$

The first state combines two pair-singlets. The second combines two pair-triplets to total spin zero. These basis vectors are physical intertwiner states; their labels are distinct from the four magnetic leg indices. Here “physical” refers to satisfying the Gauss constraint, not to a demonstrated solution of every gravitational constraint.

The main text originally used a different valid real singlet basis. Deepak chose to unify the basis rather than maintain a conversion subsection. Pairing and phase conventions change matrices and state coefficients together; eigenvalues and predictions remain unchanged.

## 3. Constructing the basis by spinor-polynomial expansion

Deepak recalled the direct explanation in [Part II's spinor teaching note](/Volumes/Data/owncloud/root/research/articles/lqg-strings-p2/notes/dh-intertwiners-from-spinors.md). This became the preferred construction, followed by a short traditional coupling explanation.

For formal spinor variables $z_i=(\alpha_i,\beta_i)$, identify $\alpha_i$ with $|0\rangle_i$ and $\beta_i$ with $|1\rangle_i$. The common-rotation invariant

$$
F_{ij}=\alpha_i\beta_j-\beta_i\alpha_j
$$

represents an unnormalized pair-singlet. For four spin-one-half legs each spinor must occur once, leaving three pairings:

$$
A(z)=F_{12}F_{34},\qquad B(z)=F_{13}F_{24},\qquad C(z)=F_{14}F_{23}.
$$

Expanding $A$ produces the four coefficients of $\Phi_1$. The identity $A-B+C=0$ makes their linear dependence explicit. For individually normalized states represented by $A/2,B/2,C/2$,

$$
\langle A|B\rangle=\frac12,\qquad
|\Phi_1\rangle=|A\rangle,\qquad
|\Phi_2\rangle=\frac{2|B\rangle-|A\rangle}{\sqrt3}.
$$

These are formal representation variables. This fixed-spin construction does not inherit the entire all-spin Dittrich–Hnybida generating amplitude or its Ising correspondence merely by using the same invariant polynomials.

## 4. Correct singlet-constraint counting

For a general total-magnetic-number-zero state with coefficients $\alpha,\beta,\gamma,\delta,\epsilon,\zeta$ in the order 0011, 0101, 0110, 1001, 1010, 1100, the total raising operator yields four independent conditions:

$$
\alpha+\beta+\delta=0,\quad \alpha+\gamma+\epsilon=0,\quad
\beta+\gamma+\zeta=0,\quad \delta+\epsilon+\zeta=0.
$$

They imply $\delta=\gamma$, $\epsilon=\beta$, and $\alpha=\zeta=-\beta-\gamma$: two independent coefficients remain. The previous supplement incorrectly counted the rank as three and introduced a spurious spin-one component. Within total magnetic number zero, annihilation by the raising operator already implies a singlet, using

$$
\mathbf S_{\rm tot}^2=S^-_{\rm tot}S^+_{\rm tot}
+(S^z_{\rm tot})^2+S^z_{\rm tot}.
$$

## 5. The geometric triple product and volume normalization

The classical scalar triple product measures the oriented volume of a parallelepiped. In the tetrahedral interpretation the vectors are face-area vectors, so

$$
V_{\rm tet}^2=\frac29
\left|\mathbf E_1\cdot(\mathbf E_2\times\mathbf E_3)\right|.
$$

This explains the square root in the volume operator. Define the bare dimensionless Hermitian operator

$$
\hat q=\mathbf J_1\cdot(\mathbf J_2\times\mathbf J_3).
$$

It is separate from a chosen signed volume interior:

$$
\hat Q_v=c_v\hat q,\qquad
\hat V_v=\gamma^{3/2}\ell_P^3\sqrt{|\hat Q_v|}.
$$

The real coefficient $c_v$ includes normalization and, for AL, outgoing-edge tangent signs. With $\hat Q_v=C\sum_{I<J<K}\epsilon_v(I,J,K)\hat q_{IJK}$, closure gives

$$
c_v=C[\epsilon_v(1,2,3)-\epsilon_v(1,2,4)
+\epsilon_v(1,3,4)-\epsilon_v(2,3,4)].
$$

This treatment holds the embedding signs fixed under spin time reversal. If $c_v=0$, that volume operator vanishes; otherwise it has two opposite signed eigenvalues and one degenerate ordinary-volume value. No universal physical volume coefficient was established. RS places absolute values differently and was not identified with AL.

## 6. The explicit commutator and spin-exchange derivation

Define the pair-spin observables

$$
A=(\mathbf J_1+\mathbf J_2)^2,\qquad
B=(\mathbf J_2+\mathbf J_3)^2.
$$

Angular-momentum commutators give $[A,B]=-4i\hat q$, hence

$$
\hat q=\frac{i}{4}[A,B].
$$

This established identity appears in [Brunnemann–Thiemann, equation (8)](https://arxiv.org/pdf/gr-qc/0405060#page=4). In the common basis, $A$ is diagonal with entries 0 and 2.

For spin one half, use the exchange operator

$$
P_{23}=2\mathbf J_2\cdot\mathbf J_3+\frac12 I,\qquad B=I+P_{23},
$$

$$
P_{23}|m_1,m_2,m_3,m_4\rangle=|m_1,m_3,m_2,m_4\rangle.
$$

The identity follows because exchange has eigenvalues +1 on the triplet and -1 on the singlet, while the scalar product has eigenvalues $1/4$ and $-3/4$. The identity symbol is now $I$; its earlier blackboard variant failed to render in chat. An explicit overlap gives $\langle\Phi_2|P_{23}|\Phi_1\rangle=\sqrt3/2$, producing

$$
A=\begin{pmatrix}0&0\\0&2\end{pmatrix},\qquad
B=\begin{pmatrix}3/2&\sqrt3/2\\\sqrt3/2&1/2\end{pmatrix},
$$

$$
\boxed{\hat q=\frac{\sqrt3}{4}
\begin{pmatrix}0&-i\\i&0\end{pmatrix}.}
$$

The previous bare coefficient $1/(4\sqrt3)$ was too small by a factor of three. A basis change cannot repair an eigenvalue mismatch. The new derivation replaces an assertion of a “direct, lengthy” calculation with a short, inspectable computation.

## 7. Orientation eigenstates and antiunitary time reversal

The real singlet basis does not diagonalize the triple product. Its eigenstates are

$$
|\pm\rangle=\frac{|\Phi_1\rangle\pm i|\Phi_2\rangle}{\sqrt2},\qquad
\hat q|\pm\rangle=\pm\frac{\sqrt3}{4}|\pm\rangle.
$$

For one spin choose $\Theta_{1/2}=i\sigma_y\mathcal K$. On all four legs,

$$
\Theta=(i\sigma_y)^{\otimes4}\mathcal K,\qquad \Theta^2=I.
$$

Each real basis vector is fixed, but coefficients are conjugated. Consequently

$$
\Theta|+\rangle=|-\rangle,\qquad\Theta|-\rangle=|+\rangle,
\qquad \Theta=X\mathcal K
$$

in the orientation basis. Thus $\Theta\hat q\Theta^{-1}=-\hat q$, while the ordinary volume is invariant. Fixing two real basis vectors does not make an anti-linear transformation the linear identity on their complex span.

The labels + and - refer to the sign of the ordered triple product. Their correspondence with the signs of $Q_v$ reverses if $c_v<0$. Interpreting signed geometry as spacetime time orientation remains the paper's physical proposal; neither a thermodynamic arrow nor cosmological coherence follows from this one-node result.

## 8. CZX consistency after unifying the basis

The CZX code action is unitary $X$ on the basis 0000, 1111. Spin time reversal on the orientation qubit is antiunitary $X\mathcal K$. Matching exchanged sectors does not establish equivalent symmetry representations or many-body phases.

Updating the main-text appendix to the common basis gives, for $|w\rangle=|0001\rangle+|0010\rangle+|0100\rangle+|1000\rangle$,

$$
S^+_{\rm tot}U_{CZ}|\Phi_1\rangle=|w\rangle,\qquad
S^+_{\rm tot}U_{CZ}|\Phi_2\rangle=-\frac1{\sqrt3}|w\rangle.
$$

Both displayed vectors acquire nonsinglet components. The conclusion that the literal CZX unitary does not preserve the full intertwiner space survives the basis change. This does not claim that no particular singlet combination can remain a singlet.

## 9. Author review, implementation, and credit

Deepak required exact current passages followed by proposed replacements, displayed directly in chat one at a time. After an initially inadequate response format, that procedure was followed. He requested the spinor construction, a traditional explanation, one common basis, the full exchange explanation, and explicit credit to Sol 6.1 Medium. He approved implementation with “Go ahead!” and then requested the existing AI tagging convention.

Visible model-named `\GPTBegin` / `\GPTEnd` markers were adopted from lqg-strings-p2. The assistance statement distinguishes established mathematical identities from Sol 6.1 Medium's assembly of the worked presentation, independent algebraic checks, error identification, and drafting under the author's direction. Brunnemann–Thiemann receives the commutator citation; the standard exchange identity is supported by [C. C. Yu's lecture notes, equations (57)–(64)](https://webapps.ps.uci.edu/~cyu/p115A/LectureNotes/Lecture17/html_version/lecture17.html).

The first implementation left the complete derivation only in the separate supplement. Deepak inspected the manuscript and requested one location containing the calculation. The final implementation creates [four-valent-orientation-calculation.tex](../four-valent-orientation-calculation.tex), included once by each document. The manuscript now contains Appendix F, “Oriented geometry at a four-valent node,” pages 44–48 in the final 52-page build. The matrix/exchange calculation is on page 47; orientation states and time reversal are on page 48. The CZX appendix moves to Appendix G. Page numbers describe this build and may change.

Changed tracked files are `timesarrow.tex`, `timesarrow.bib`, `timesarrow.bbl`, `timesarrow.pdf`, `supplementary-calculations.tex`, and `ai-assistance-statement.md`. Relevant new files include the shared calculation, the historical passage-review draft, the supplement PDF, this note, and the transcript. The [review draft](../proposed-single-node-edits-2026-11-26.md) retains superseded proposals as a historical record; it is not the final implementation specification.

## 10. Verification and limits

During implementation, direct calculations on the sixteen spin states checked the bases, singlet constraints, triple-product matrices/eigenvectors, basis conversion, pair-Casimir commutator, four-edge reductions, time reversal and its square, and the updated CZX leakage formulas. Exact rational elimination checked constraint rank four. Verification scripts were temporary (`/tmp/check-timesarrow-node.py` and related commands); no permanent repository test suite was added or changed.

Both documents compiled. The final isolated build in `/tmp/timesarrow-consolidated` resolved the earlier bibliography/reference warnings; it produced the 52-page manuscript and 13-page supplement. Revised pages were rendered and visually inspected. Existing layout/font or bibliography-metadata warnings elsewhere were not comprehensively repaired. These builds are not clean-checkout submission or publication acceptance. No commit, push, release, or deployment was performed.

The broader CZX, gauge-theory, thermal-dominance, fermionic-matter, and cosmological claims were not comprehensively re-audited. The approved local rewrite does not authorize or complete the separate August Path A revision package.

## 11. Resume with two neighboring nodes

Deepak ended the research work after settling the one-node foundation. Start the next session with two four-valent spin-one-half intertwiners. Write each tensor with a physical intertwiner label and four magnetic leg indices. Glue one leg from each node using the appropriate invariant pairing, keeping both physical orientation labels visible. Specify orientation/dual conventions, normalization, and treatment of the uncontracted legs; do not silently identify a magnetic bond label with a physical orientation qubit.

Then determine the time-reversal action on the glued object. This supplies a first chain building block, not yet chain evolution. Part II's existing T3b owns chain/state-space choices and T3c owns transitions and sewing; T3e owns the eventual continuum interpretation. The timesarrow task registry has historical manuscript owners T11/T12 and current publication owner T36. No task statuses were changed in this recording pass.

For a later strip, the sought operator is $K_{\boldsymbol s',\boldsymbol s}$ between physical chain configurations. A row tensor acting on exposed magnetic boundary indices is a different map until a physical-state construction relates them. No two-node contraction, selected chain dynamics, scaling spectrum, continuum limit, or worldsheet identification was completed here.

## 12. Record source

The transcript was extracted from the main Codex session JSONL `rollout-2026-11-26T16-16-57-01a21777-325f-72f0-97bb-aec2b8140f78.jsonl`, identified by workspace metadata and matching dialogue. It contains 55 user/final-assistant messages in 15 chronological topics, through the request to save the records and run mem-scan. Injected setup, environment and skill messages, tools, progress commentary, and internal reasoning are omitted. Historical claims are retained in the transcript; mathematical delimiters and nested heading levels are normalized for Markdown. The detailed chat-summary reply is included.

<< Sol 6.1 Medium End >>
