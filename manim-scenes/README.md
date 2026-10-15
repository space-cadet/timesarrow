# Manim edge-state animation

`edge_state_flip_v5.py` is the current production candidate for T37. It explains
binary link states with compact `+1`/`-1` badges, irregular independent flips,
link-local highlights, and a separate plaquette loop-product check. The v4
source and renders are retained as rough-draft history.

From the repository root, render a review-quality MP4 with:

```bash
manim -pqh manim-scenes/edge_state_flip_v5.py EdgeStateFlipV5
```

The scene is deterministic so milestone screenshots can be compared across
revisions. The wording is intentionally framed as a proposed mechanism and is
not a claim that the manuscript has derived the full microscopic construction.


## Web presentation (2026-10-16)

The existing combined Blender v4/Manim v5 MP4 is published as a draft on the
[project landing page](https://quantumofgravity.com/projects/timesarrow/).
Its source is `renders/t37_quantum_geometry_v4_plus_edge_state_v5.mp4`.
Context captions are retained in `captions/t37-combined-walkthrough-en.vtt`;
the website serves an identical copy. Chapter jumps are 0, 10, and 19 seconds.
The captions explain the 3D-to-flat-diagram change and distinguish independent
link changes from the separate web example of a local convention change.

The guided loop story, growing-loop comparison, and orientation/mixing pair
are responsive SVG/DOM scenes in the `website` repository’s
`projects/timesarrow/` page. They use explicit play/pause and manual controls,
and pause when the page is hidden. Device reduced-motion settings disable
automatic playback while retaining the manual controls.

The MP4 remains silent. Recorded narration and final YouTube production
approval remain part of T37; captioned web presentation is tracked in T13.
