# System Patterns
*Last Updated: 2026-04-16 20:15:00 IST*

## Theoretical Mappings
- **Spin Network $\leftrightarrow$ Tensor Network**: Spin network edges (labeled by SU(2) spins) map to TNS bonds; vertices map to tensors (intertwiners).
- **Z2 Gauge Field $\leftrightarrow$ Time Reversal**: A local Z2 field on the spin network edges encodes the local time-reversal symmetry.
- **Volume Sign $\leftrightarrow$ Time Arrow**: The sign of the volume operator (related to the tetrad determinant) represents the local direction of time.
- **SPT Edge States $\leftrightarrow$ Fermionic Matter**: Gapless excitations at the boundary of the SPT phase (like in the CZX model) are interpreted as Dirac fermions.

## Structural Conventions
- **Paper Structure**: Follows the SciPost Physics template (Introduction $\rightarrow$ Topological Order $\rightarrow$ MPS/TNS $\rightarrow$ Spin Networks $\rightarrow$ Volume/$Z_2$ $\rightarrow$ SPT/CZX $\rightarrow$ SPT/LQG $\rightarrow$ Discussion).
- **Notation**: 
  - $j$: Spin labels for edges.
  - $\Tr$: Trace over bond indices.
  - $A^v$: Vertex tensors.
  - $g^e$: Edge tensors.

## Document Evolution
- **Drafting Strategy**: Large sections of the paper are detailed, but the link between CZX and spontaneous symmetry breaking (`sec:spt-lqg` and `sec:z2-action`) is the current area of active development/refinement.
- **Reference Style**: Citations are managed via BibLaTeX and Biber for high precision.
