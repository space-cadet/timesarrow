# Implementation Detail: YouTube Animation Plan
*Created: 2026-09-11 16:44:01 IST*
*Last Updated: 2026-09-11 16:44:01 IST*

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
1. Create the Manim v4 prototype under the project folder.
2. Render milestone frame captures and the complete animation.
3. Review the rendered output visually and adjust spacing, contrast, timing, and labels.
4. Decide whether the Manim shot should be integrated with the Blender sequence.
