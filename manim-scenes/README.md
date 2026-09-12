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
