# Single-node calculation: proposed edits for review

<< Sol 6.1 Medium Begin >>

Status: historical review draft. The author approved the passages in chat, with subsequent changes: spinor-polynomial construction, one shared basis, an explicit exchange-operator explanation, credit to Sol 6.1 Medium, and visible AI markers. Those approved changes were applied on 27 November 2026. The original pairs below are retained as the review record.

<< Sol 6.1 Medium End >>

This review pairs each exact existing passage with its proposed LaTeX replacement. Read the proposed passages in items 1–5 consecutively for the revised calculation. Items 6–9 are the corresponding corrections elsewhere. The two source files use different real singlet bases; each is retained, with their relation made explicit.

The checked bare operator is q = J1 · (J2 × J3), with dimensionless J = sigma/2. Its eigenvalue magnitude is sqrt(3)/4. The full signed volume interior is written Q_v = c_v q. No universal numerical volume is asserted before choosing its normalization and vertex embedding. The different signs of the displayed eigenvectors in the main text and supplement follow from their different bases.

The proposals are plain LaTeX snippets. AI assistance is already disclosed in the existing documents; this review does not introduce new disclosure macros.

## Review map

- Item 1: Begin with the geometry; construct the singlet basis — `supplementary-calculations.tex:68`.
- Item 2: Replace the obsolete comparison with the current manuscript basis — `supplementary-calculations.tex:213`.
- Item 3: Separate the bare triple product from volume conventions — `supplementary-calculations.tex:301`.
- Item 4: Calculate the matrix and show time reversal explicitly — `supplementary-calculations.tex:365`.
- Item 5: Update the local correction list — `supplementary-calculations.tex:483`.
- Item 6: Correct the main-text identification of orientation eigenstates — `timesarrow.tex:763`.
- Item 7: Correct the related effective-qubit comparison — `timesarrow.tex:930`.
- Item 8: Keep the later reference to the result consistent — `supplementary-calculations.tex:706`.
- Item 9: Replace obsolete single-node entries in the final correction summary — `supplementary-calculations.tex:1022`.

## Checks and references

Direct computation on all 16 spin states verifies both singlet bases, the matrix of q, the change of basis, time reversal, and the pair-Casimir commutator. The four raising constraints have rank four. Independent matrix calculations give q = (sqrt(3)/4) sigma_y in the supplement basis and its negative in the main-text basis.

For the face-normal geometry and V² = (2/9)|E1 · (E2 × E3)|, see [Bianchi, Quantum Geometry of Space in Spinfoam Gravity, section 2](https://www.actaphys.uj.edu.pl/fulltext?page=2447&series=Reg&vol=44). For volume-operator context and four-valent spectral methods, see [Brunnemann and Thiemann](https://arxiv.org/abs/gr-qc/0405060). The numerical coefficient in this review is calculated explicitly rather than inferred from a citation.

The CZX calculation and thermal-dominance section are not rewritten here. Their older summary contains other claims needing a separate audit. In particular, item M6a and the effective-qubit map in Calculation 2 should not be read as a completed operator or phase identification. The wider main-text volume discussion also requires a separate consistency pass; the present proposal repairs the single-node derivation and its immediate references.

## 1. Begin with the geometry; construct the singlet basis

Source: `supplementary-calculations.tex:68`.

Reason: Lead with the requested triple-product picture. Remove the unfinished pairing expression and incorrect constraint counting; retain the supplement basis used later.

### Current passage (verbatim)

```latex
\section{Calculation 1 (T11/C3): The two-dimensional singlet subspace and the
  volume operator}
\label{sec:calc1}
% =============================================================================

\subsection{The full Clebsch-Gordan decomposition}
\label{sub:cg}

The tensor product of four spin-$\tfrac{1}{2}$ representations decomposes as
\begin{equation}\label{eqn:cg-decomp}
  \underbrace{\tfrac{1}{2} \otimes \tfrac{1}{2}}_{\text{pair 12}}
  \otimes
  \underbrace{\tfrac{1}{2} \otimes \tfrac{1}{2}}_{\text{pair 34}}
  = (0 \oplus 1) \otimes (0 \oplus 1)
  = 0 \oplus 1 \oplus 1 \oplus (0 \oplus 1 \oplus 2).
\end{equation}
Collecting irreducibles: $0 \oplus 0 \oplus 1 \oplus 1 \oplus 1 \oplus 2$,
so the singlet ($j_{\rm tot}=0$) subspace is \emph{two-dimensional}, confirming
the statement in the manuscript.

\subsection{Explicit orthonormal singlet basis in the computational basis}
\label{sub:singlet-basis}

We label the four spin-$\tfrac{1}{2}$ Hilbert spaces $1,2,3,4$.
The unique (up to normalisation) singlet formed from pair $(12)$ is
\begin{equation}
  \ket{s_{12}} = \frac{1}{\sqrt{2}}\bigl(\ket{01}-\ket{10}\bigr)_{12},
\end{equation}
and similarly for pair $(34)$.  The first basis singlet is therefore
\begin{equation}\label{eqn:singlet-s}
  \ket{s}
  = \ket{s_{12}}\otimes\ket{s_{34}}
  = \frac{1}{2}\bigl(\ket{0101}-\ket{0110}-\ket{1001}+\ket{1010}\bigr).
\end{equation}

The second independent singlet is obtained by pairing $(13)$ and $(24)$, or
equivalently by pairing $(14)$ and $(23)$; both choices give the same
two-dimensional space.  A convenient orthonormal partner is obtained by
pairing $(14)$ and $(23)$:
\begin{equation}
  \ket{t}
  = \ket{s_{14}}\otimes\ket{s_{23}}
  = \frac{1}{2}\bigl(\ket{0110}-\ket{1001}-\ket{0110}+\cdots\bigr).
\end{equation}
However it is more useful to exhibit the orthonormal pair directly.
Working in the 16-dimensional computational basis $\{\ket{m_1 m_2 m_3 m_4}\}$
with $m_i\in\{0,1\}$, the $j_{\rm tot}=0$ subspace is spanned by the \emph{six}
basis vectors that have $\sum_i m_i = 2$ (i.e.\ total $M_z = 0$):
\begin{equation}\label{eqn:mz0-basis}
  \ket{0011},\;\ket{0101},\;\ket{0110},\;\ket{1001},\;\ket{1010},\;\ket{1100}.
\end{equation}
The two singlet conditions ($S^{(12+34)}_z = 0$ is automatic; we also need
$S^2_{\rm tot}=0$, i.e.\ $\hat{S}^+_{\rm tot}\ket{\Psi}=0$) give two linear
constraints on the six-dimensional $M_z=0$ subspace, leaving exactly a
two-dimensional solution space.

Solving these constraints explicitly (see below), the two orthonormal
singlets are:
\begin{align}
  \ket{\Phi_1}
  &= \frac{1}{2}\bigl(\ket{0101}-\ket{0110}-\ket{1001}+\ket{1010}\bigr),
  \label{eqn:Phi1}\\[4pt]
  \ket{\Phi_2}
  &= \frac{1}{\sqrt{12}}
     \bigl(2\ket{0011}-\ket{0101}-\ket{0110}-\ket{1001}-\ket{1010}+2\ket{1100}\bigr).
  \label{eqn:Phi2}
\end{align}

\begin{result}
  $\ket{\Phi_1}$ and $\ket{\Phi_2}$ defined in
  \eqref{eqn:Phi1}--\eqref{eqn:Phi2} form an orthonormal basis for the
  $SU(2)$-singlet subspace of $(\tfrac{1}{2})^{\otimes 4}$.
\end{result}

\paragraph{Derivation of the singlet constraint.}
The total raising operator is
$\hat{S}^+_{\rm tot} = \sum_{k=1}^{4}\hat{S}^+_k$, where
$\hat{S}^+_k\ket{0}_k=0$ and $\hat{S}^+_k\ket{1}_k=\ket{0}_k$.
Acting on a general $M_z=0$ state
$\ket{\Psi} = \alpha\ket{0011}+\beta\ket{0101}+\gamma\ket{0110}
              +\delta\ket{1001}+\eps\ket{1010}+\zeta\ket{1100}$
we need $\hat{S}^+_{\rm tot}\ket{\Psi}=0$.  The action on each basis vector is:

\noindent
$\hat{S}^+_{\rm tot}\ket{0011} = \ket{0001}+\ket{0010}$,\quad
$\hat{S}^+_{\rm tot}\ket{0101} = \ket{0001}+\ket{0100}$,\\
$\hat{S}^+_{\rm tot}\ket{0110} = \ket{0010}+\ket{0100}$,\quad
$\hat{S}^+_{\rm tot}\ket{1001} = \ket{0001}+\ket{1000}$,\\
$\hat{S}^+_{\rm tot}\ket{1010} = \ket{0010}+\ket{1000}$,\quad
$\hat{S}^+_{\rm tot}\ket{1100} = \ket{0100}+\ket{1000}$.

Setting $\hat{S}^+_{\rm tot}\ket{\Psi}=0$ gives four conditions (one per
$M_z=+1$ basis state):
\begin{align}
  [\ket{0001}]: &\quad \alpha+\beta+\delta = 0,\label{eqn:sing1}\\
  [\ket{0010}]: &\quad \alpha+\gamma+\eps  = 0,\label{eqn:sing2}\\
  [\ket{0100}]: &\quad \beta+\gamma+\zeta  = 0,\label{eqn:sing3}\\
  [\ket{1000}]: &\quad \delta+\eps+\zeta   = 0.\label{eqn:sing4}
\end{align}
The sum of all four equations gives $2(\alpha+\beta+\gamma+\delta+\eps+\zeta)=0$,
so the four constraints are not all independent; there are three independent
constraints on six coefficients, giving a solution space of dimension $6-3=3$.
However, this 3-dimensional space contains not just singlets but also
$j_{\rm tot}=1$, $m=0$ states (which satisfy $\hat{S}^+_{\rm tot}\ket{\psi}=0$
vacuously in the $M_z=0$ sector but are not annihilated by $\hat{S}^2_{\rm tot}$
acting into the $M_z=\pm 1$ sectors via the lowering operator).  The correct
procedure is to additionally impose $\hat{S}^-_{\rm tot}\ket{\Psi}=0$, which
gives four more conditions that are linearly dependent on
\eqref{eqn:sing1}--\eqref{eqn:sing4} by the symmetry $0\leftrightarrow 1$, so
no new constraints arise from lowering.  Instead, one must impose
$\hat{S}^2_{\rm tot}\ket{\Psi}=0(\cdot\ket{\Psi})$, which distinguishes singlets
from the $j_{\rm tot}=1$, $m=0$ component.  Working this out explicitly (or by
direct Clebsch-Gordan decomposition) one finds the singlet subspace is exactly
2-dimensional.

The explicit orthonormal singlet basis is:
\begin{align}
  \ket{\Phi_1}
  &= \frac{1}{2}\bigl(
     +\ket{0101} - \ket{0110} - \ket{1001} + \ket{1010}
     \bigr),
  \tag{\ref{eqn:Phi1}}\\[4pt]
  \ket{\Phi_2}
  &= \frac{1}{\sqrt{12}}\bigl(
     +2\ket{0011} - \ket{0101} - \ket{0110} - \ket{1001} - \ket{1010} + 2\ket{1100}
     \bigr).
  \tag{\ref{eqn:Phi2}}
\end{align}

\paragraph{Verification.}
$\braket{\Phi_1}{\Phi_1} = \tfrac{1}{4}(1+1+1+1)=1$. \checkmark \\
$\braket{\Phi_2}{\Phi_2} = \tfrac{1}{12}(4+1+1+1+1+4)=1$. \checkmark \\
$\braket{\Phi_1}{\Phi_2} = \tfrac{1}{2\sqrt{3}}(-1 \cdot(-1)+(-1)\cdot(-1)+(-1)\cdot(-1)+1\cdot(-1))$;
more carefully:
\begin{align*}
  \braket{\Phi_1}{\Phi_2}
  &= \frac{1}{2}\cdot\frac{1}{\sqrt{12}}
     \bigl[
       1\cdot(-1) + (-1)\cdot(-1) + (-1)\cdot(-1) + 1\cdot(-1)
     \bigr]\\
  &= \frac{1}{2\sqrt{12}}\bigl[-1+1+1-1\bigr] = 0.\checkmark
\end{align*}
Both states satisfy $\hat{S}^+_{\rm tot}\ket{\Phi_i}=0$ by construction
(verified term by term above).
```

### Proposed replacement

```latex
\section{Calculation 1: Oriented geometry at a four-valent node}
\label{sec:calc1}

\subsection{The triple product and its geometric meaning}

Consider three classical vectors. Their scalar triple product
\begin{equation}
 d=\mathbf a\cdot(\mathbf b\times\mathbf c)
\end{equation}
measures an oriented volume: $|d|$ is the volume of the parallelepiped,
while its sign distinguishes its two handed orientations. Reversing all
three vectors changes that sign.

At a spin-network node, the angular momenta describe oriented face-area
vectors of a quantum polyhedron. For a tetrahedron these are four vectors
$\mathbf E_e$ satisfying $\sum_{e=1}^4\mathbf E_e=0$. Their triple product
has dimensions of volume squared, and the classical tetrahedral volume is
\begin{equation}
 V_{\rm tet}^2=\frac{2}{9}
 \left|\mathbf E_1\cdot(\mathbf E_2\times\mathbf E_3)\right|.
\end{equation}
The face-area vectors are distinct from the edge-vectors used to construct
a parallelepiped. This explains why a square root enters the volume formula.

We first calculate the dimensionless quantum triple product
\begin{equation}\label{eqn:q-def}
 \hat q=\mathbf J_1\cdot(\mathbf J_2\times\mathbf J_3)
 =\sum_{a,b,c=1}^3\varepsilon_{abc}J_1^aJ_2^bJ_3^c,
 \qquad J_e^a=\frac12\sigma_e^a.
\end{equation}
Here $e$ labels a leg, while $a,b,c$ label Cartesian components. The three
factors in each term act on different legs and commute, so $\hat q$ is
Hermitian. The relation to a chosen LQG volume prescription is stated below.

\subsection{The two physical intertwiner states}
\label{sub:cg}\label{sub:singlet-basis}

Take all four legs to be outgoing and to carry spin $j=\tfrac12$.
Gauge invariance requires
\begin{equation}
 (\mathbf J_1+\mathbf J_2+\mathbf J_3+\mathbf J_4)|\psi\rangle=0.
\end{equation}
Pairing legs $(12)$ and $(34)$ gives
\begin{equation}\label{eqn:cg-decomp}
 (\tfrac12\otimes\tfrac12)\otimes(\tfrac12\otimes\tfrac12)
 =(0\oplus1)\otimes(0\oplus1).
\end{equation}
A total singlet occurs once from $0\otimes0$ and once from $1\otimes1$.
The physical intertwiner space is therefore two-dimensional.

For a pair of spins, write
\begin{equation}
 |s\rangle=\frac{|01\rangle-|10\rangle}{\sqrt2},\qquad
 |t_+\rangle=|00\rangle,\quad
 |t_0\rangle=\frac{|01\rangle+|10\rangle}{\sqrt2},\quad
 |t_-\rangle=|11\rangle.
\end{equation}
An orthonormal basis is
\begin{align}
 |\Phi_1\rangle&=|s\rangle_{12}|s\rangle_{34}\nonumber\\
 &=\frac12(|0101\rangle-|0110\rangle-|1001\rangle+|1010\rangle),
 \label{eqn:Phi1}\\
 |\Phi_2\rangle&=\frac1{\sqrt3}
 (|t_+\rangle_{12}|t_-\rangle_{34}
 -|t_0\rangle_{12}|t_0\rangle_{34}
 +|t_-\rangle_{12}|t_+\rangle_{34})\nonumber\\
 &=\frac1{\sqrt{12}}
 (2|0011\rangle-|0101\rangle-|0110\rangle-|1001\rangle
 -|1010\rangle+2|1100\rangle).
 \label{eqn:Phi2}
\end{align}
The pair-singlet and pair-triplet sectors are orthogonal, and the displayed
coefficients give unit norm. This basis is the one used in Calculation 2.

For a direct check, a general state with total magnetic number zero is
\begin{equation}
 |\psi\rangle=\alpha|0011\rangle+\beta|0101\rangle
 +\gamma|0110\rangle+\delta|1001\rangle
 +\epsilon|1010\rangle+\zeta|1100\rangle.
\end{equation}
The condition $S^+_{\rm tot}|\psi\rangle=0$ gives
\begin{equation}
 \alpha+\beta+\delta=0,\quad \alpha+\gamma+\epsilon=0,\quad
 \beta+\gamma+\zeta=0,\quad \delta+\epsilon+\zeta=0.
\end{equation}
These four equations are independent. Their solutions obey
$\delta=\gamma$, $\epsilon=\beta$, $\zeta=\alpha$, and
$\alpha+\beta+\gamma=0$, leaving two free coefficients.
Within the total-$M_z=0$ space, annihilation by $S^+_{\rm tot}$ is sufficient
for a singlet: the identity
$\mathbf S_{\rm tot}^2=S^-_{\rm tot}S^+_{\rm tot}
 +(S^z_{\rm tot})^2+S^z_{\rm tot}$ gives
$\mathbf S_{\rm tot}^2|\psi\rangle=0$.
```

## 2. Replace the obsolete comparison with the current manuscript basis

Source: `supplementary-calculations.tex:213`.

Reason: The old subsection discusses manuscript states that have already been replaced. Give the checked change of basis for the current files.

### Current passage (verbatim)

```latex
\subsection{Relation to the manuscript's states}
\label{sub:manuscript-states}

The manuscript (eqs.\ \texttt{eqn:vol-states}, \texttt{eqn:vol-states-2}) defines
\begin{align}
  \ket{\Psi_A} &= \ket{0101}+\ket{1010},\label{eqn:PsiA}\\
  \ket{\Psi_B} &= \ket{1001}+\ket{0110},\label{eqn:PsiB}\\
  \ket{\Psi_1} &= \ket{\Psi_A}+\ket{\Psi_B}
               = \ket{0101}+\ket{1010}+\ket{1001}+\ket{0110},\label{eqn:Psi1}\\
  \ket{\Psi_2} &= \ket{\Psi_A}-\ket{\Psi_B}
               = \ket{0101}+\ket{1010}-\ket{1001}-\ket{0110}.\label{eqn:Psi2}
\end{align}
\textbf{These are not normalised} (each has norm $2$) and more importantly we
must check whether they actually lie in the singlet subspace.

\paragraph{Singlet check for $\ket{\Psi_1}$.}
\begin{align*}
  \hat{S}^+_{\rm tot}\ket{\Psi_1}
  &= \hat{S}^+_{\rm tot}\ket{0101}+\hat{S}^+_{\rm tot}\ket{1010}
    +\hat{S}^+_{\rm tot}\ket{1001}+\hat{S}^+_{\rm tot}\ket{0110}\\
  &= (\ket{0001}+\ket{0100})
    +(\ket{0010}+\ket{1000})
    +(\ket{0001}+\ket{1000})
    +(\ket{0010}+\ket{0100})\\
  &= 2\ket{0001}+2\ket{0010}+2\ket{0100}+2\ket{1000} \;\neq\; 0.
\end{align*}
\textbf{$\ket{\Psi_1}$ as written in the manuscript is NOT a singlet.}

\paragraph{Singlet check for $\ket{\Psi_2}$.}
\begin{align*}
  \hat{S}^+_{\rm tot}\ket{\Psi_2}
  &= (\ket{0001}+\ket{0100})
    +(\ket{0010}+\ket{1000})
    -(\ket{0001}+\ket{1000})
    -(\ket{0010}+\ket{0100})\\
  &= 0. \checkmark
\end{align*}

So $\ket{\Psi_2}$ (normalised: $\ket{\Psi_2}/2$) \emph{is} a singlet.
After normalising,
\begin{equation}\label{eqn:psi2-normalised}
  \frac{\ket{\Psi_2}}{2}
  = \frac{1}{2}\bigl(\ket{0101}+\ket{1010}-\ket{1001}-\ket{0110}\bigr)
  = +\ket{\Phi_1},
\end{equation}
i.e.\ it equals $+\ket{\Phi_1}$ (the ordering of terms within the state does
not affect the vector).

The manuscript's $\ket{\Psi_1}$ lies \emph{outside} the singlet subspace.
The correct orthonormal singlet pair to use is \eqref{eqn:Phi1}--\eqref{eqn:Phi2}.

\begin{result}\label{res:correct-basis}
  The correct orthonormal singlet basis for the invariant subspace of
  $(\tfrac{1}{2})^{\otimes 4}$ is:
  \begin{align}
    \ket{\Psi_1^{\rm corr}}
    &= \frac{1}{2}\bigl(\ket{0101}-\ket{0110}-\ket{1001}+\ket{1010}\bigr),\\
    \ket{\Psi_2^{\rm corr}}
    &= \frac{1}{\sqrt{12}}\bigl(
       2\ket{0011}-\ket{0101}-\ket{0110}-\ket{1001}-\ket{1010}+2\ket{1100}
       \bigr).
  \end{align}
  The manuscript state $\ket{\Psi_2}/2 = +\ket{\Psi_1^{\rm corr}}$ is correct.
  The manuscript state $\ket{\Psi_1}$ is \textbf{not} a singlet; it must be
  corrected to $\ket{\Psi_2^{\rm corr}}$ above, or to the alternative partner
  \begin{equation}\label{eqn:alternative-partner}
    \ket{\tilde\Psi_2}
    = \frac{1}{2}\bigl(\ket{0011}-\ket{1100}\bigr)\sqrt{2}
      +\frac{1}{2\sqrt{2}}\bigl(-\ket{0101}-\ket{0110}-\ket{1001}-\ket{1010}\bigr),
  \end{equation}
  depending on which pairing convention is preferred.
\end{result}

\paragraph{Note on alternative singlet basis.}
An equally valid orthonormal basis is obtained by the $(14)(23)$ pairing:
\begin{align}
  \ket{\chi_1}
  &= \frac{1}{2}\bigl(\ket{0110}-\ket{0101}+\ket{1001}-\ket{1010}\bigr),
  \label{eqn:chi1}\\
  \ket{\chi_2}
  &= \frac{1}{\sqrt{12}}\bigl(
     2\ket{0011}+\ket{0101}+\ket{0110}+\ket{1001}+\ket{1010}+2\ket{1100}
     \bigr).
  \label{eqn:chi2}
\end{align}
Note $\ket{\chi_1} = -\ket{\Phi_1}$ and $\ket{\chi_2}$ differs from $\ket{\Phi_2}$
by signs.  All such pairs span the same 2-dimensional singlet subspace.
```

### Proposed replacement

```latex
\subsection{Relation to the manuscript's basis}
\label{sub:manuscript-states}

The main text uses another real orthonormal singlet basis. Denoting its
states by $|\Phi_1^{\rm main}\rangle,|\Phi_2^{\rm main}\rangle$ avoids
confusing them with the states in this supplement:
\begin{align}
 |\Phi_1^{\rm main}\rangle&=\frac{\sqrt3}{2}|\Phi_1\rangle
                         -\frac12|\Phi_2\rangle,\\
 |\Phi_2^{\rm main}\rangle&=-\frac12|\Phi_1\rangle
                         -\frac{\sqrt3}{2}|\Phi_2\rangle.
\end{align}
This real orthogonal change of basis preserves the singlet space. Neither
real basis diagonalizes $\hat q$. The opposite-orientation eigenstates
will be complex combinations of its two basis states.
```

## 3. Separate the bare triple product from volume conventions

Source: `supplementary-calculations.tex:301`.

Reason: The existing expressions mix edge and Cartesian indices, Hermitian and anti-Hermitian conventions, and numerical prefactors. State one explicit Hermitian convention without pretending to settle a universal physical volume coefficient.

### Current passage (verbatim)

```latex
\subsection{Volume operator in the singlet subspace}
\label{sub:volume}

\subsubsection{Definition and reduction to the interior operator}

The Rovelli-Smolin volume operator at a 4-valent vertex with all $j=\tfrac{1}{2}$
edges is (restoring the prefactor)
\begin{equation}\label{eqn:RS-volume}
  \hat{V} = \gamma^{3/2}\lp^3\,\left|
    \frac{iC_{\rm reg}}{8}\,
    \sum_{\{a,b,c\}\subset\{1,2,3,4\}}\eps^{abc}\,\hat{J}^{(a)}_x\hat{J}^{(b)}_y\hat{J}^{(c)}_z
  \right|^{1/2},
\end{equation}
where the sum is over the $\binom{4}{3}=4$ triples of edges.
The key object is the \emph{interior operator}:
\begin{equation}\label{eqn:Q-def}
  \hat{Q} \equiv \frac{iC_{\rm reg}}{8}
  \sum_{\{a,b,c\}\subset\{1,2,3,4\}}
  \eps^{abc}\,\hat{J}^{(a)}_x\hat{J}^{(b)}_y\hat{J}^{(c)}_z,
\end{equation}
so that $\hat{V} = \gamma^{3/2}\lp^3\,|\hat{Q}|^{1/2}$.

For $j=\tfrac{1}{2}$, $\hat{J}^{(k)}_a = \tfrac{1}{2}\sigma_a^{(k)}$, so
\begin{equation}
  \hat{Q} = \frac{iC_{\rm reg}}{8}
  \sum_{\{a,b,c\}\subset\{1,2,3,4\}}
  \eps^{abc}\,
  \frac{\sigma^{(a)}_x}{2}\,\frac{\sigma^{(b)}_y}{2}\,\frac{\sigma^{(c)}_z}{2}.
\end{equation}
The four triples from $\{1,2,3,4\}$ are $(1,2,3),(1,2,4),(1,3,4),(2,3,4)$.
Using $\eps^{xyz}=+1$ and antisymmetry:
\begin{equation}\label{eqn:Q-expanded}
  \hat{Q} = \frac{iC_{\rm reg}}{64}
  \Bigl[
    \sx^{(1)}\sy^{(2)}\sz^{(3)}\otimes\mathbbm{1}^{(4)}
  + \sx^{(1)}\sy^{(2)}\mathbbm{1}^{(3)}\otimes\sz^{(4)}
  + \sx^{(1)}\mathbbm{1}^{(2)}\sy^{(3)}\sz^{(4)}
  + \mathbbm{1}^{(1)}\sx^{(2)}\sy^{(3)}\sz^{(4)}
  + \text{permutations}
  \Bigr].
\end{equation}
In the full form with antisymmetry in $(a,b,c)$ and the three cyclic permutations
$(xyz),(yzx),(zxy)$ each contributing, the operator simplifies
(see Brunnemann-Thiemann \cite{Brunnemann2006Simplification}) to:
\begin{equation}\label{eqn:Q-compact}
  \hat{Q} = -\frac{C_{\rm reg}}{8}
  \bigl(
    \hat{\vec{J}}^{(1)}\cdot(\hat{\vec{J}}^{(2)}\times\hat{\vec{J}}^{(3)})
  + \text{3 cyclic permutations of } (1,2,3,4)
  \bigr).
\end{equation}
For a 4-valent vertex the Gauss constraint reads
$\hat{\vec{J}}^{(1)}+\hat{\vec{J}}^{(2)}+\hat{\vec{J}}^{(3)}+\hat{\vec{J}}^{(4)}=0$,
so we can eliminate $\hat{\vec{J}}^{(4)}$ and the four contributions are not
independent.  The standard result \cite{Brunnemann2006Simplification,Rovelli1994Discreteness}
is that on the singlet subspace:
\begin{equation}\label{eqn:Q-singlet}
  \hat{Q}\big|_{\rm singlet}
  = -\frac{C_{\rm reg}}{8}\,
  \hat{\vec{J}}^{(1)}\cdot(\hat{\vec{J}}^{(2)}\times\hat{\vec{J}}^{(3)}),
\end{equation}
up to an overall constant depending on the ordering convention (different authors
use different values of $C_{\rm reg}\in\{1,2,4\}$).
```

### Proposed replacement

```latex
\subsection{Volume and signed orientation}
\label{sub:volume}

The triple product $\hat q$ is the common algebraic object needed here.
To distinguish it from the signed interior of a particular volume
prescription, write, on the four-valent singlet space,
\begin{equation}\label{eqn:Q-singlet}
 \hat Q_v=c_v\hat q,\qquad
 \hat V_v=\gamma^{3/2}\ell_P^3\sqrt{|\hat Q_v|}.
\end{equation}
The real dimensionless coefficient $c_v$ includes the normalization.
For the AL operator it also includes the edge-tangent orientation factors.
We leave it explicit rather than assign a numerical volume before these
choices are fixed.

For example, write the signed Ashtekar--Lewandowski interior as
\begin{equation}
 \hat Q_v=C\sum_{1\leq I<J<K\leq4}\epsilon_v(I,J,K)\hat q_{IJK},
 \qquad \hat q_{IJK}=\mathbf J_I\cdot(\mathbf J_J\times\mathbf J_K).
\end{equation}
Here $C$ is the chosen real normalization and $\epsilon_v(I,J,K)$ is the
sign of the determinant of the three outgoing edge tangents, or zero if
those tangents are linearly dependent. On gauge-invariant states, closure
and the angular-momentum commutators give
\begin{equation}
 \hat q_{124}=-\hat q_{123},\qquad
 \hat q_{134}=\hat q_{123},\qquad
 \hat q_{234}=-\hat q_{123}.
\end{equation}
Consequently
\begin{equation}
 c_v=C\,[\epsilon_v(1,2,3)-\epsilon_v(1,2,4)
          +\epsilon_v(1,3,4)-\epsilon_v(2,3,4)].
\end{equation}
This is a fixed-embedding calculation: these tangent signs are held fixed
when time reversal acts on the spin labels. If $c_v=0$, this volume
operator vanishes at the vertex. If $c_v\ne0$, its two signed eigenvalues
have opposite sign and its ordinary volume is degenerate. The
Rovelli--Smolin prescription places absolute values differently and should
be treated separately; no equality of the two prescriptions is assumed here.
```

## 4. Calculate the matrix and show time reversal explicitly

Source: `supplementary-calculations.tex:365`.

Reason: Replace the skipped matrix calculation and erroneous bare coefficient 1/(4 sqrt(3)) with the explicit commutator derivation; distinguish antiunitary time reversal from a unitary bit flip.

### Current passage (verbatim)

```latex
\subsubsection{Matrix elements of $\hat{Q}$ in the singlet subspace}

We set $C_{\rm reg}=1$ and compute $\hat{q}\equiv \hat{\vec{J}}^{(1)}\cdot(\hat{\vec{J}}^{(2)}\times\hat{\vec{J}}^{(3)})$
in the singlet subspace spanned by $\{\ket{\Phi_1},\ket{\Phi_2}\}$.

Expanding:
\begin{align}
  \hat{q}
  &= \hat{J}^{(1)}_x(\hat{J}^{(2)}_y\hat{J}^{(3)}_z - \hat{J}^{(2)}_z\hat{J}^{(3)}_y)
  + \hat{J}^{(1)}_y(\hat{J}^{(2)}_z\hat{J}^{(3)}_x - \hat{J}^{(2)}_x\hat{J}^{(3)}_z)
  + \hat{J}^{(1)}_z(\hat{J}^{(2)}_x\hat{J}^{(3)}_y - \hat{J}^{(2)}_y\hat{J}^{(3)}_x).
\end{align}
With $\hat{J}^{(k)}_a = \tfrac{1}{2}\sigma_a^{(k)}$, each term is a product of three
$j=\tfrac{1}{2}$ Pauli matrices. The result is an operator on $(\mathbb{C}^2)^{\otimes 4}$
(identity on factor 4).

The $2\times 2$ matrix representation of $\hat{Q}$ restricted to the
singlet subspace is:
\begin{equation}\label{eqn:Q-matrix}
  Q_{ij} = \bra{\Phi_i}\hat{Q}\ket{\Phi_j},\quad i,j\in\{1,2\}.
\end{equation}

\paragraph{Computing $\hat{q}\ket{\Phi_1}$.}

The operator $\hat{q}$ contains terms like $\sx^{(1)}\sy^{(2)}\sz^{(3)}$.
In the computational basis $\ket{m_1 m_2 m_3 m_4}$:
\begin{align*}
  \sx^{(1)}\sy^{(2)}\sz^{(3)}\ket{m_1 m_2 m_3 m_4}
  &= \ket{\bar m_1}(-i)^{m_2}(-1)^{m_3+1/2}\cdots,
\end{align*}
where $\sx\ket{0}=\ket{1}$, $\sx\ket{1}=\ket{0}$;
$\sy\ket{0}=i\ket{1}$, $\sy\ket{1}=-i\ket{0}$;
$\sz\ket{0}=\ket{0}$, $\sz\ket{1}=-\ket{1}$.

Computing $\hat{q}\ket{\Phi_1}$ in full:
\begin{equation*}
  \ket{\Phi_1}=\tfrac{1}{2}(\ket{0101}-\ket{0110}-\ket{1001}+\ket{1010}).
\end{equation*}
A direct (lengthy but straightforward) evaluation in the full
16-dimensional space gives (citing the known result from Brunnemann-Thiemann
\cite{Brunnemann2006Simplification} and Borissenko \cite{Borissenko2021Volume}):

\begin{equation}\label{eqn:q-matrix-result}
  \boxed{
  [Q_{ij}]
  = \frac{i}{4\sqrt{3}}
  \begin{pmatrix}
    0 & -1 \\
    1 &  0
  \end{pmatrix},
  \qquad \text{i.e.}\quad
  \hat{Q}\big|_{\rm singlet}
  = \frac{1}{4\sqrt{3}}\begin{pmatrix}0 & -i\\ i & 0\end{pmatrix}.}
\end{equation}

This matrix is $\frac{1}{4\sqrt{3}}\sigma_y$ (up to an overall sign convention),
which is Hermitian with eigenvalues $\pm\frac{1}{4\sqrt{3}}$.

\paragraph{Derivation sketch for \eqref{eqn:q-matrix-result}.}
Using $J_a = \tfrac{1}{2}\sigma_a$ and the product rule for Paulis
($\sigma_a\sigma_b = \delta_{ab}\mathbbm{1}+i\eps_{abc}\sigma_c$):
\begin{align}
  \hat{J}^{(2)}_y\hat{J}^{(3)}_z
  &= \frac{1}{4}\sy^{(2)}\sz^{(3)},\qquad
  \hat{J}^{(2)}_z\hat{J}^{(3)}_y
  = \frac{1}{4}\sz^{(2)}\sy^{(3)}.
\end{align}
The matrix element $Q_{12}=\bra{\Phi_1}\hat{q}\ket{\Phi_2}$ picks up a
non-zero value from the cross-terms because $\ket{\Phi_1}$ involves
only pairs $\ket{01}$ and $\ket{10}$ (in positions 1,2 and 3,4), while
$\ket{\Phi_2}$ involves additionally $\ket{00}$ and $\ket{11}$ in positions
1,4.  The diagonal elements $Q_{11}$ and $Q_{22}$ vanish because
$\hat{q}$ is odd under the exchange $0\leftrightarrow 1$ (time reversal)
while $\ket{\Phi_1}$ and $\ket{\Phi_2}$ have definite parities under this
exchange.

The eigenvalues of $Q_{ij}$ are $\pm q_0$ where
\begin{equation}\label{eqn:q0}
  q_0 = \frac{1}{4\sqrt{3}}.
\end{equation}

\subsubsection{Eigenvalues of the volume operator in the singlet subspace}

The volume operator eigenvalues are $V = \gamma^{3/2}\lp^3|Q|^{1/2}$.
Since $Q$ has eigenvalues $\pm q_0$, the matrix $|Q|$ has eigenvalues
$+q_0$ (both eigenvalues of $Q$ have the same absolute value), and:
\begin{equation}\label{eqn:volume-eigenvalue}
  v_0 = \gamma^{3/2}\lp^3\,\sqrt{q_0}
  = \gamma^{3/2}\lp^3\,\frac{1}{\sqrt{4\sqrt{3}}}
  = \gamma^{3/2}\lp^3\cdot 3^{-1/4}/2.
\end{equation}

\begin{remark}
  Both eigenstates of $\hat{Q}$ have the \emph{same} volume eigenvalue $v_0$;
  they differ in the \emph{sign} of $Q$.  The volume operator
  $\hat{V}=\gamma^{3/2}\lp^3|Q|^{1/2}$ therefore has a degenerate eigenvalue
  $v_0$ on the entire singlet subspace.  The sign of $Q$ -- i.e.\ the
  eigenvalue of $Q$ itself, $\pm q_0$ -- is what distinguishes the two
  time orientations in the manuscript.  It is important that the manuscript
  frames this correctly: the two singlet states are eigenstates of the
  \emph{interior operator $\hat{Q}$} (not of $\hat{V}$) with eigenvalues
  $\pm q_0$.
\end{remark}

\begin{result}\label{res:volume}
  The eigenstates of $\hat{Q}|_{\rm singlet}$ are
  \begin{align}
    \ket{+} &= \frac{1}{\sqrt{2}}(\ket{\Phi_1}+i\ket{\Phi_2}),
    & \hat{Q}\ket{+} &= +q_0\ket{+},\\
    \ket{-} &= \frac{1}{\sqrt{2}}(\ket{\Phi_1}-i\ket{\Phi_2}),
    & \hat{Q}\ket{-} &= -q_0\ket{-},
  \end{align}
  with $q_0 = 1/(4\sqrt{3})$ (in units where $C_{\rm reg}=1$, $\hbar=1$).
  These are the states to identify with $\ket{\Psi_1}$ and $\ket{\Psi_2}$
  in the manuscript.  They represent the two time orientations: forward
  ($\hat{Q}>0$) and backward ($\hat{Q}<0$).
\end{result}
```

### Proposed replacement

```latex
\subsubsection{Matrix elements of the triple product}

There is a short way to evaluate $\hat q$ without expanding all sixteen
spin states. Define
\begin{equation}
 A=(\mathbf J_1+\mathbf J_2)^2,\qquad
 B=(\mathbf J_2+\mathbf J_3)^2.
\end{equation}
Since $[J_e^a,J_f^b]=i\delta_{ef}\sum_c\varepsilon_{abc}J_e^c$,
\begin{align}
 [A,B]&=4[\mathbf J_1\cdot\mathbf J_2,\mathbf J_2\cdot\mathbf J_3]
 \nonumber\\
 &=4i\sum_{a,b,c}\varepsilon_{abc}J_1^aJ_2^cJ_3^b
 =-4i\hat q.
\end{align}
Thus $\hat q=(i/4)[A,B]$.

In the basis $(\Phi_1,\Phi_2)$ the pair $(12)$ has spin zero or one, so
\begin{equation}
 A=\begin{pmatrix}0&0\\0&2\end{pmatrix}.
\end{equation}
For spin one-half, the swap operator $P_{23}$ satisfies
$P_{23}=2\mathbf J_2\cdot\mathbf J_3+\tfrac12\mathbbm1$, so
$B=\mathbbm1+P_{23}$. Swapping the middle two bits gives
\begin{equation}
 P_{23}|\Phi_1\rangle
 =\frac12(|0011\rangle-|0110\rangle-|1001\rangle+|1100\rangle).
\end{equation}
Taking its overlap with $\Phi_2$ gives
\begin{equation}
 \langle\Phi_2|P_{23}|\Phi_1\rangle
 =\frac{2+1+1+2}{2\sqrt{12}}=\frac{\sqrt3}{2}.
\end{equation}
The two diagonal overlaps are $1/2$ and $-1/2$, respectively. Hence
\begin{equation}
 B=\begin{pmatrix}3/2&\sqrt3/2\\\sqrt3/2&1/2\end{pmatrix},
 \qquad [A,B]=\begin{pmatrix}0&-\sqrt3\\\sqrt3&0\end{pmatrix},
\end{equation}
and therefore
\begin{equation}\label{eqn:q-matrix-result}
 \boxed{\hat q\big|_{\rm singlet}
 =\frac{\sqrt3}{4}\begin{pmatrix}0&-i\\i&0\end{pmatrix}.}
\end{equation}
The coefficient follows from $J^a=\sigma^a/2$ and the explicit definition
of $\hat q$; it contains no volume regularization constant.

\subsubsection{The two orientation states}

\begin{result}\label{res:volume}
 The states
 \begin{equation}
 |+\rangle=\frac{|\Phi_1\rangle+i|\Phi_2\rangle}{\sqrt2},\qquad
 |-\rangle=\frac{|\Phi_1\rangle-i|\Phi_2\rangle}{\sqrt2}
 \end{equation}
 satisfy $\hat q|\pm\rangle=\pm q_0|\pm\rangle$, where
 \begin{equation}\label{eqn:q0}
 q_0=\frac{\sqrt3}{4}.
 \end{equation}
 For $\hat Q_v=c_v\hat q$, their signed eigenvalues are $\pm c_vq_0$.
 Both have ordinary volume
 \begin{equation}\label{eqn:volume-eigenvalue}
 v_0=\gamma^{3/2}\ell_P^3\sqrt{|c_v|\,q_0}.
 \end{equation}
\end{result}
The labels $+$ and $-$ refer to the sign of the ordered triple product
$\hat q$. They agree with the signs of $\hat Q_v$ when $c_v>0$ and are
exchanged when $c_v<0$.

\subsubsection{Time reversal exchanges the orientations}

For one spin choose $\Theta_{1/2}=i\sigma_y\mathcal K$, with $\mathcal K$
complex conjugation in the computational basis. Then
$\Theta_{1/2}|0\rangle=-|1\rangle$ and
$\Theta_{1/2}|1\rangle=|0\rangle$. On four spins,
\begin{equation}
 \Theta=(i\sigma_y)^{\otimes4}\mathcal K,\qquad \Theta^2=1.
\end{equation}
Each displayed singlet is real and unchanged by this operation:
$\Theta|\Phi_1\rangle=|\Phi_1\rangle$ and
$\Theta|\Phi_2\rangle=|\Phi_2\rangle$.
Anti-linearity then gives
\begin{equation}
 \Theta|+\rangle=|-\rangle,\qquad\Theta|-\rangle=|+\rangle.
\end{equation}
Equivalently, in the orientation basis $\Theta=X\mathcal K$.
Since $\Theta\mathbf J_e\Theta^{-1}=-\mathbf J_e$,
\begin{equation}
 \Theta\hat q\Theta^{-1}=-\hat q,\qquad
 \Theta\hat V_v\Theta^{-1}=\hat V_v.
\end{equation}
Time reversal changes the sign of the oriented geometry while preserving
its ordinary volume. The further interpretation of this sign as a
spacetime time orientation is the physical proposal of the main text.
```

## 5. Update the local correction list

Source: `supplementary-calculations.tex:483`.

Reason: Remove instructions to replace a valid main-text basis and references to obsolete state labels.

### Current passage (verbatim)

```latex
\subsection{Recommended corrections to the manuscript}
\label{sub:corr1}

\begin{enumerate}
  \item Replace the manuscript states \texttt{eqn:vol-states-2} with the
    orthonormal pair \eqref{eqn:Phi1}--\eqref{eqn:Phi2}.
  \item Replace the claim that $\ket{\Psi_1}$ and $\ket{\Psi_2}$ are eigenstates
    of $\hat{V}$ with the statement that $\ket{+}$ and $\ket{-}$ (Result
    \ref{res:volume}) are eigenstates of the \emph{interior operator} $\hat{Q}$
    with eigenvalues $\pm q_0$, and both have the same volume eigenvalue $v_0$.
    Phrase as: ``the two time orientations are distinguished by the sign of
    $\hat{Q}$, the signed volume operator, rather than by the modulus $\hat{V}$.''
  \item Add the reference to Brunnemann-Thiemann \cite{Brunnemann2006Simplification}
    for the calculation of $\hat{Q}$ in the singlet subspace.
\end{enumerate}

% =============================================================================
```

### Proposed replacement

```latex
\subsection{Corresponding changes in the main text}
\label{sub:corr1}

The main text's real singlet basis is valid. Its signed-orientation
states are the complex combinations obtained by diagonalizing $\hat q$
in that basis. Numerical eigenvalues should distinguish the bare value
$q_0=\sqrt3/4$ from the convention-dependent factor in $\hat Q_v=c_v\hat q$.
The time-reversal action is antiunitary; its exchange of the two
orientation states should be stated with complex conjugation included.

% =============================================================================
```

## 6. Correct the main-text identification of orientation eigenstates

Source: `timesarrow.tex:763`.

Reason: Correct the actual main-text error while retaining its existing singlet basis.

### Current passage (verbatim)

```latex
where $ \{\ket{\Phi_1}, \ket{\Phi_2}\} $ form an orthonormal basis for the 2D singlet subspace. These states are eigenvectors of the signed interior operator $\hat{Q}$ with eigenvalues $\pm q$, corresponding to the two possible time orientations. Note that the standard volume operator $\hat{V} \propto \sqrt{|\hat{Q}|}$ is degenerate on this subspace, but the time-orientation is captured by the sign of $\hat{Q}$.
```

### Proposed replacement

```latex
where $\{\ket{\Phi_1},\ket{\Phi_2}\}$ form an orthonormal basis for the two-dimensional singlet subspace. These real basis states do not diagonalize the oriented triple product $\hat q=\hat{\mathbf J}_1\cdot(\hat{\mathbf J}_2\times\hat{\mathbf J}_3)$. With $J^a=\sigma^a/2$ and the displayed basis, its eigenstates are
\begin{equation}
 \ket{+}=\frac{\ket{\Phi_1}-i\ket{\Phi_2}}{\sqrt2},\qquad
 \ket{-}=\frac{\ket{\Phi_1}+i\ket{\Phi_2}}{\sqrt2},\qquad
 \hat q\ket{\pm}=\pm\frac{\sqrt3}{4}\ket{\pm}.
\end{equation}
The supplementary calculation derives this result and relates its basis to the one used here. For a fixed nondegenerate vertex and volume convention, write the signed interior as $\hat Q_v=c_v\hat q$. The ordinary volume $\hat V_v\propto\sqrt{|\hat Q_v|}$ is equal on the two states, while their signed eigenvalues are opposite. Spin time reversal exchanges $\ket{+}$ and $\ket{-}$ antiunitarily. The interpretation of these opposite geometric orientations as opposite time orientations is the physical proposal considered here.
```

## 7. Correct the related effective-qubit comparison

Source: `timesarrow.tex:930`.

Reason: The existing paragraph repeats the incorrect eigenbasis and treats unitary and antiunitary symmetries as interchangeable. This replacement corrects that specific comparison; it does not rewrite the rest of the CZX argument.

### Current passage (verbatim)

```latex
The on-site $ Z_2 $ symmetry of the CZX model acts as a Pauli-$ X $ gate on the two-dimensional code subspace $ \operatorname{span}\{\ket{0000}, \ket{1111}\} $, exchanging the two basis states \cite{Chen2010Local}. The intertwiner subspace at a 4-valent $ j = 1/2 $ spin-network vertex is likewise two-dimensional, spanned by $ \{\ket{\Phi_1}, \ket{\Phi_2}\} $, with the $ Z_2 $ time-reversal action realized by the sign flip of the signed volume operator: $ \hat{Q} \ket{\Phi_{1,2}} = \pm q_0 \ket{\Phi_{1,2}} $. The only delicate point is the precise basis identification between the LQG volume-qubit basis $ \{\ket{\Phi_1},\ket{\Phi_2}\} $ and the CZX code-space basis $ \{\ket{0000},\ket{1111}\} $. At the level of effective qubits, both subspaces carry a $Z_2$ automorphism exchanging their two orientation/code sectors. At the microscopic operator level, however, $U_{CZX}$ does not act literally on the full $SU(2)$ singlet intertwiner subspace; the explicit computation is given in \autoref{subsec:czx-intertwiner}. Thus the CZX correspondence is not merely an analogy: the four qubits, inter-site bond entanglement, shared edge variables, and local $Z_2$ gauge structure are present in the spin-network construction, while the volume-qubit/code-space basis map remains the point requiring the most care.
```

### Proposed replacement

```latex
The on-site $Z_2$ symmetry of the CZX model acts as a Pauli-$X$ gate on the code subspace $\operatorname{span}\{\ket{0000},\ket{1111}\}$, exchanging its basis states \cite{Chen2010Local}. The four-valent $j=1/2$ intertwiner space is also two-dimensional. In its orientation basis $\{\ket{+},\ket{-}\}$, spin time reversal acts as $X\mathcal K$, exchanging the signed-geometric sectors and conjugating their amplitudes. This gives a structural correspondence between the exchanged sectors, while retaining the distinction between unitary CZX symmetry and antiunitary time reversal. At the microscopic operator level, $U_{CZX}$ does not preserve the full $SU(2)$ singlet intertwiner subspace; the explicit calculation is given in \autoref{subsec:czx-intertwiner}. The two-dimensional state spaces alone therefore do not identify their symmetry representations or their many-body phases.
```

## 8. Keep the later reference to the result consistent

Source: `supplementary-calculations.tex:706`.

Reason: A necessary notation update in Calculation 2; its CZX operator calculations remain outside this review.

### Current passage (verbatim)

```latex
    The $\mathbb{Z}_2$ ``time-orientation'' degree of freedom corresponds to
    the eigenvalue $\pm q_0$ of the signed volume operator $\hat{Q}$
    (Result \ref{res:volume}).
```

### Proposed replacement

```latex
The two orientation states in Result \ref{res:volume} have eigenvalues
    $\pm q_0$ of the bare triple product $\hat q$ and $\pm c_vq_0$ of
    the signed volume interior $\hat Q_v$.
```

## 9. Replace obsolete single-node entries in the final correction summary

Source: `supplementary-calculations.tex:1022`.

Reason: Remove stale claims about earlier manuscript states; make the final single-node summary agree with the proposed calculation.

### Current passage (verbatim)

```latex
  \item[\textbf{C3a}] (Critical) The manuscript states $\ket{\Psi_1}$ and
    $\ket{\Psi_2}$ in \texttt{eqn:vol-states-2} are both $SU(2)$ singlets.
    Only $\ket{\Psi_2}/2 = +\ket{\Phi_1}$ \eqref{eqn:psi2-normalised} is
    a singlet.  $\ket{\Psi_1}$ as written is \textbf{not} a singlet
    ($\hat{S}^+_{\rm tot}\ket{\Psi_1}=2(\ket{0001}+\ket{0010}+\ket{0100}
    +\ket{1000})\neq 0$).
    \textbf{Action}: Replace with the correct orthonormal pair
    \eqref{eqn:Phi1}--\eqref{eqn:Phi2}.

  \item[\textbf{C3b}] (Critical) The manuscript implies the two singlet
    states are eigenstates of the volume operator $\hat{V}$ with
    \emph{opposite eigenvalues} (``positive and negative volume'').
    This is imprecise: $\hat{V}=\gamma^{3/2}\lp^3|\hat{Q}|^{1/2}$
    has a \emph{degenerate} eigenvalue $v_0$ on the entire singlet
    subspace, since $|\hat{Q}|$ has the same magnitude eigenvalue $q_0$
    for both eigenstates.  The sign of time orientation is encoded in
    the eigenvalue of the \emph{signed} interior operator $\hat{Q}$
    (eigenvalues $\pm q_0$), not of $\hat{V}$.
    \textbf{Action}: Replace ``eigenstates of $\hat{V}$ with opposite
    eigenvalues'' with ``eigenstates of $\hat{Q}$ with eigenvalues $\pm q_0$,
    where $\hat{Q}\equiv\hat{\vec{J}}^{(1)}\cdot(\hat{\vec{J}}^{(2)}\times
    \hat{\vec{J}}^{(3)})$ is the signed volume operator.''.
```

### Proposed replacement

```latex
\item[\textbf{C3a}] The main text's current real singlet basis is valid.
    Distinguish it from the complex combinations that diagonalize the
    oriented triple product. The explicit change of basis is given in
    Calculation 1.

  \item[\textbf{C3b}] With $J^a=\sigma^a/2$, the bare triple product has
    eigenvalues $\pm\sqrt3/4$. A volume convention introduces the factor
    $c_v$ in $\hat Q_v=c_v\hat q$. The ordinary volume is degenerate on
    the singlet space, and spin time reversal exchanges the opposite
    orientation states antiunitarily.
```

## Verification of the proposal

The algebra verification passed. A disposable full-supplement copy incorporating the proposed replacements compiled successfully. The remaining overfull boxes occur in the untouched later calculations; no overfull box was reported in the rewritten Calculation 1. Bibliography and cross-reference warnings in that temporary standalone build are not a clean submission check. Source checksums were verified unchanged after drafting.

## Source checksums at review creation

- `supplementary-calculations.tex`: `3404a87b4077b069ff5c2f5e46013957d63fb072fba6149e609740f9ed6709c2`
- `timesarrow.tex`: `02e6a78c6d2801d107305ad323143c331eb02994ef164cba63941f6898203c75`
