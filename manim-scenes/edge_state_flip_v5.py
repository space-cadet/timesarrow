"""Production-candidate T37 link-state explanation."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[1]
config.background_color = "#07111F"
config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080
config.media_dir = str(ROOT / "manim-scenes" / "media")

BG = "#07111F"
LINK = "#71869D"
NODE = "#F3C35B"
PLUS = "#27B6FF"
MINUS = "#FF4F9A"
TEXT = "#EEF6FF"
MUTED = "#A9BDD1"
LOOP = "#72E6C1"


def state_glyph(point: np.ndarray, state: int, scale: float = 1.0) -> VGroup:
    """A compact screen-space state badge that does not erase its link."""
    color = PLUS if state > 0 else MINUS
    disk = Circle(radius=0.19 * scale, fill_color=BG, fill_opacity=0.92,
                  stroke_color=color, stroke_width=2.5 * scale).move_to(point)
    label = Text("+" if state > 0 else "−", font="Arial", weight=BOLD,
                 font_size=23 * scale, color=color).move_to(point)
    return VGroup(disk, label)


class EdgeStateFlipV5(Scene):
    def construct(self) -> None:
        title = Text("Binary states live on the links", font_size=42, color=TEXT)
        title.to_edge(UP, buff=0.35)
        qualifier = Text("A proposed Z₂ edge-state picture", font_size=22, color=MUTED)
        qualifier.next_to(title, DOWN, buff=0.12)

        positions = {(c, r): np.array((-3.75 + 2.5*c, -1.55 + 1.75*r, 0.0))
                     for r in range(3) for c in range(3)}
        specs = ([((c, r), (c+1, r)) for r in range(3) for c in range(2)] +
                 [((c, r), (c, r+1)) for r in range(2) for c in range(3)])
        links = VGroup(*[Line(positions[a], positions[b], color=LINK, stroke_width=4)
                         for a, b in specs])
        nodes = VGroup(*[Dot(p, radius=0.13, color=NODE).set_stroke(TEXT, 1.5)
                         for p in positions.values()])
        states = [1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1]
        markers = [state_glyph((positions[a]+positions[b])/2, s)
                   for (a, b), s in zip(specs, states)]

        legend = VGroup(
            Text("LINK STATE", font_size=20, color=MUTED),
            VGroup(state_glyph(ORIGIN, 1, .8), Text("+1", font_size=22, color=PLUS)).arrange(RIGHT, buff=.14),
            VGroup(state_glyph(ORIGIN, -1, .8), Text("−1", font_size=22, color=MINUS)).arrange(RIGHT, buff=.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.22).move_to([4.85, .8, 0])

        self.play(FadeIn(title, shift=DOWN*.12), FadeIn(qualifier, shift=DOWN*.08), run_time=.7)
        self.play(LaggedStart(*[Create(x) for x in links], lag_ratio=.025),
                  LaggedStart(*[FadeIn(x, scale=.7) for x in nodes], lag_ratio=.025),
                  run_time=1.0)
        self.play(LaggedStart(*[FadeIn(x, scale=.65) for x in markers], lag_ratio=.035),
                  FadeIn(legend), run_time=.9)

        caption = Text("Each link can change on its own", font_size=28, color=TEXT)
        caption.to_edge(DOWN, buff=.38)
        self.play(FadeIn(caption, shift=UP*.1), run_time=.45)

        # Irregular starts and one overlapping distant pair make independence visible.
        for indices, pause in [([3], .14), ([8], .42), ([0, 10], .18), ([5], .55), ([7], .0)]:
            animations = []
            for idx in indices:
                a, b = specs[idx]
                midpoint = (positions[a]+positions[b])/2
                states[idx] *= -1
                halo = Line(positions[a], positions[b], color=(PLUS if states[idx] > 0 else MINUS),
                            stroke_width=11).set_opacity(.65)
                animations.extend([ShowPassingFlash(halo, time_width=.65),
                                   Transform(markers[idx], state_glyph(midpoint, states[idx]))])
            self.play(*animations, run_time=.62)
            if pause > 0:
                self.wait(pause)

        self.wait(.45)
        self.play(FadeOut(caption), run_time=.3)

        # Top-left loop ends with two negative links: the +1 result is non-trivial.
        loop_indices = [2, 4, 9, 10]
        # Ensure exactly two negatives on the highlighted loop.
        desired = [1, -1, 1, -1]
        fixes = []
        for idx, target_state in zip(loop_indices, desired):
            if states[idx] != target_state:
                a, b = specs[idx]
                states[idx] = target_state
                fixes.append(Transform(markers[idx], state_glyph((positions[a]+positions[b])/2, target_state)))
        if fixes:
            self.play(*fixes, run_time=.45)

        corners = [positions[(0,1)], positions[(1,1)], positions[(1,2)], positions[(0,2)]]
        plaquette = Polygon(*corners, stroke_color=LOOP, stroke_width=7,
                            fill_color=LOOP, fill_opacity=.06)
        loop_title = Text("One closed loop", font_size=26, color=LOOP).next_to(plaquette, UP, buff=.14)
        self.play(Create(plaquette), FadeIn(loop_title), run_time=.75)

        factors = VGroup(*[Text(s, font_size=30, color=(PLUS if "+1" in s else MINUS))
                           for s in ["(+1)", "(−1)", "(+1)", "(−1)"]]).arrange(RIGHT, buff=.16)
        equals = Text("=  +1", font_size=32, color=TEXT)
        equation = VGroup(factors, equals).arrange(RIGHT, buff=.24).move_to([4.45, -.55, 0])
        note = Text("The four link states multiply to a loop value", font_size=20, color=MUTED)
        note.next_to(equation, DOWN, buff=.22)
        self.play(LaggedStart(*[FadeIn(x, shift=UP*.08) for x in factors], lag_ratio=.18), run_time=1.0)
        self.play(FadeIn(equals), FadeIn(note), run_time=.45)
        self.wait(1.5)
