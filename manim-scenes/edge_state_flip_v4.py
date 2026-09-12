"""Manim v4 prototype for the proposed binary edge-state explanation.

Render from the repository root with:

    manim -pqh manim-scenes/edge_state_flip_v4.py EdgeStateFlipV4

The scene is intentionally deterministic.  The staggered flip order is chosen
to make the independent-link idea easy to review frame by frame.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import *


PROJECT_ROOT = Path(__file__).resolve().parents[1]
config.background_color = "#07111F"
config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080
config.media_dir = str(PROJECT_ROOT / "manim-scenes" / "media")


BACKGROUND = "#07111F"
LINK = "#7890A8"
NODE = "#F4B942"
UP_COLOR = "#27B6FF"
DOWN_COLOR = "#FF4F9A"
PULSE = "#FFE082"
TEXT = "#EEF6FF"
MUTED = "#A9BDD1"
LOOP = "#7CF2D3"


def edge_marker(point: np.ndarray, state: int) -> VGroup:
    """Return a vertical, screen-space arrow marker for a binary edge state."""

    point = np.array(point, dtype=float)
    color = UP_COLOR if state > 0 else DOWN_COLOR
    start = point + (DOWN if state > 0 else UP) * 0.23
    end = point + (UP if state > 0 else DOWN) * 0.23

    # The dark pill keeps the state glyph legible even when an edge is vertical.
    backplate = RoundedRectangle(
        width=0.34,
        height=0.78,
        corner_radius=0.11,
        stroke_width=0,
        fill_color=BACKGROUND,
        fill_opacity=1,
    ).move_to(point)
    arrow = Arrow(
        start,
        end,
        buff=0,
        stroke_width=6,
        color=color,
        max_tip_length_to_length_ratio=0.48,
    )
    return VGroup(backplate, arrow)


class EdgeStateFlipV4(Scene):
    """Show independent binary link flips, followed by a plaquette check."""

    def construct(self) -> None:
        title = Text(
            "A proposed Z₂ edge-state picture",
            font_size=40,
            color=TEXT,
        ).to_edge(UP, buff=0.28)
        subtitle = Text(
            "Binary orientation states live on links — not only at vertices",
            font_size=24,
            color=MUTED,
        ).next_to(title, DOWN, buff=0.14)

        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(subtitle, shift=DOWN * 0.1))

        # A compact square lattice makes both links and plaquettes immediately
        # recognizable while leaving room for the explanatory legend.
        positions = {
            (column, row): np.array((-3.3 + 2.2 * column, -1.35 + 1.55 * row, 0.0))
            for row in range(3)
            for column in range(3)
        }
        edge_specs = [
            ((column, row), (column + 1, row))
            for row in range(3)
            for column in range(2)
        ] + [
            ((column, row), (column, row + 1))
            for row in range(2)
            for column in range(3)
        ]

        links = [
            Line(positions[start], positions[end]).set_stroke(LINK, width=3, opacity=0.9)
            for start, end in edge_specs
        ]
        nodes = [
            Circle(
                radius=0.14,
                stroke_color=TEXT,
                stroke_width=2,
                fill_color=NODE,
                fill_opacity=1,
            ).move_to(position)
            for position in positions.values()
        ]

        # Fixed states and flip order keep review renders reproducible.
        initial_states = [1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1]
        flip_order = [3, 8, 0, 10, 5, 7]
        markers = [
            edge_marker((positions[start] + positions[end]) / 2, state)
            for (start, end), state in zip(edge_specs, initial_states)
        ]

        self.play(
            LaggedStart(*[Create(link) for link in links], lag_ratio=0.04, run_time=1.2),
            LaggedStart(*[FadeIn(node, scale=0.6) for node in nodes], lag_ratio=0.04, run_time=1.0),
            LaggedStart(*[FadeIn(marker, scale=0.7) for marker in markers], lag_ratio=0.04, run_time=1.25),
        )

        legend_title = Text("LINK STATES", font_size=22, color=TEXT)
        legend_title.move_to([5.25, 1.95, 0])
        legend_up = edge_marker(np.array([4.7, 1.25, 0]), 1).scale(0.72)
        legend_down = edge_marker(np.array([5.8, 1.25, 0]), -1).scale(0.72)
        up_label = Text("up", font_size=20, color=UP_COLOR).next_to(legend_up, DOWN, buff=0.08)
        down_label = Text("down", font_size=20, color=DOWN_COLOR).next_to(legend_down, DOWN, buff=0.08)
        legend = VGroup(legend_title, legend_up, legend_down, up_label, down_label)

        node_key = VGroup(
            Dot(radius=0.11, color=NODE),
            Text("node", font_size=20, color=MUTED),
        ).arrange(RIGHT, buff=0.12).move_to([5.25, 0.45, 0])
        link_key = VGroup(
            Line(ORIGIN, RIGHT * 0.48).set_stroke(LINK, width=3),
            Text("neutral link", font_size=20, color=MUTED),
        ).arrange(RIGHT, buff=0.12).move_to([5.25, -0.05, 0])
        self.play(FadeIn(legend), FadeIn(node_key), FadeIn(link_key))

        flip_caption = Text(
            "Each flip is local and independently timed",
            font_size=25,
            color=TEXT,
        ).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(flip_caption, shift=UP * 0.12))
        self.wait(0.6)

        for index in flip_order:
            start, end = edge_specs[index]
            midpoint = (positions[start] + positions[end]) / 2
            new_state = -initial_states[index]
            target = edge_marker(midpoint, new_state)
            self.play(
                Flash(
                    midpoint,
                    color=PULSE,
                    line_length=0.18,
                    num_lines=8,
                    flash_radius=0.34,
                ),
                Transform(markers[index], target),
                run_time=0.72,
            )

        self.wait(0.7)

        plaquette_points = [
            positions[(0, 1)],
            positions[(1, 1)],
            positions[(1, 2)],
            positions[(0, 2)],
        ]
        plaquette = Polygon(
            *plaquette_points,
            stroke_color=LOOP,
            stroke_width=5,
            fill_color=LOOP,
            fill_opacity=0.08,
        )
        plaquette_label = Text("example plaquette", font_size=24, color=LOOP).next_to(
            plaquette, UP, buff=0.12
        )
        loop_formula = MathTex(
            r"\sigma_{\rm loop}=\sigma_1\sigma_2\sigma_3\sigma_4=+1",
            font_size=28,
            color=TEXT,
        ).scale_to_fit_width(4.25).move_to([4.9, -1.0, 0])
        loop_note = Text(
            "a proposed gauge-invariant loop check",
            font_size=19,
            color=MUTED,
        ).scale_to_fit_width(4.3).next_to(loop_formula, DOWN, buff=0.18)

        self.play(Create(plaquette), FadeIn(plaquette_label, shift=UP * 0.1))
        self.play(FadeIn(loop_formula, shift=LEFT * 0.15), FadeIn(loop_note, shift=LEFT * 0.15))
        self.wait(1.5)


if __name__ == "__main__":
    # Manim discovers the Scene class when invoked from the command line.
    pass
