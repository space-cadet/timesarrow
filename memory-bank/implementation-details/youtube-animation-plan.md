# Implementation Detail: YouTube Animation Plan
*Created: 2026-09-11 16:44:01 IST*
*Last Updated: 2026-09-12 12:22:58 IST*

## Purpose
Translate the paper's proposed mechanism into a clear visual story for a broad audience without presenting speculative links as completed derivations.

## Work Completed
- Connected to Blender and created project-local scripts, scenes, renders, and frame captures.
- Built the simple v1 geometry prototype.
- Built and reviewed the v2 sequence: smooth grid, graph, spin network, tetrahedral cells, discrete area, and four-valent node.
- Built and reviewed the v3 link-flip prototype.
- Corrected v3 disappearing outer links, overlapping arrow geometry, camera framing, plaquette reveal, and final invariant label.

## Visual Diagnosis
The current v3 is technically cleaner but still suggests a simultaneous operation around one central node. The intended picture is a network whose individual edges carry binary orientation states that can fluctuate independently.

The current Manim and Blender-to-Manim outputs are rough drafts. They demonstrate the intended direction, but they are not yet visually approved for production.

## Tool Division
- Blender: smooth spacetime, tetrahedra, 3D spin networks, and camera moves.
- Manim: graph layouts, labels, vertical state arrows, independent flips, pulses, and plaquette explanations.

## Manim v4 Design
- Use thin neutral links and clearly separated node styling.
- Place a small vertical arrow glyph at each edge midpoint, kept vertical in screen space.
- Use two contrasting states, such as blue/up and orange or magenta/down.
- Flip one edge at a time with staggered timing and a brief local pulse.
- Show several independent flips before zooming into a plaquette.
- Present any loop-product result as a separate explanatory step.

## Scientific Guardrails
The video should describe the construction as a proposed mechanism. It should not state that the work has already derived ordinary thermodynamic time's arrow, semiclassical spacetime, or fermionic matter.

## Remaining Work
1. Refine the Manim composition, arrow/link styling, spacing, contrast, timing, and labels.
2. Re-render milestone captures and a production candidate after each meaningful visual revision.
3. Review the complete candidate for conceptual clarity, especially independent edge behavior versus vertex-centered operations.
4. Reassess the Blender-to-Manim transition and approve or revise the exploratory combined render.
5. Add narration and audio only as a separate production pass within the proposal-only scientific boundaries.
