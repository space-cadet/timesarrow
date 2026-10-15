# T13 — Website visual explainers

*Created: 2026-10-16 03:29:19 IST*
*Status: Published and browser-verified; updated 2026-10-16 03:41:55 IST*

## Authorization and scope

The author authorized the proposed additions and discretionary improvements on 2026-10-16, and explicitly requested that plans and progress be recorded in the Memory Bank. These explanations address the public website audience; the author is the scientist directing the project.

## Delivered baseline, 2026-10-15–16

The static landing page is hosted at https://quantumofgravity.com/projects/timesarrow/ from the separate `space-cadet/website` repository. Current worktree: `/private/tmp/website-timesarrow-landing`; original website checkout remains on an unrelated vocabulary branch. Main-site commits through `e7414c0` include a light editorial page, arXiv link near the top, inline mathematical detail, SVG illustrations, an interactive four-link loop, project/AI history, and the existing T37 draft video. Mobile video intrinsic-size overflow was reproduced and fixed with grid-child `min-width: 0`, media width constraints, and stylesheet versioning.

TimesArrow commits `e75b332` and `6c9429a` correct the README arXiv citation and add a linked animation poster. The MP4 is already tracked at `manim-scenes/renders/t37_quantum_geometry_v4_plus_edge_state_v5.mp4`.

## Implementation plan

1. Extend the shared four-link example with local-label badges, a guided story, animated highlights, play/pause, step, and reset. Show one-link physical change separately from a two-link convention change. A negative loop is permitted; link variables are not assumed globally factorable into vertex labels.
2. Replace static area/perimeter pictures with scalable lattice diagrams and a shared loop-size control. Count enclosed cells and boundary segments exactly; retain the distinction between geometric counts and statistical Wilson-loop expectations. Use schematic labels and no invented simulation data.
3. Add a pair of illustrations: shared clock orientation and progressive mixing of two colors. State that coherence of orientation and the thermodynamic arrow are different questions. Mixing animation is illustrative and its reset is an interface operation.
4. Refine the existing video presentation with explicit geometry-to-link-diagram explanation, chapter buttons, WebVTT captions, and a text description. Preserve the MP4 and its draft status. New code-native scenes use square/mobile-friendly layouts. Recorded narration remains optional separate production work.
5. Verify keyboard controls, exact loop invariance, area/perimeter counts, motion pause/reduced-motion behavior, captions, and desktop/mobile layout. Publish through the website main-branch deploy workflow and verify the live page.

## Scientific and implementation decisions

- Keep model equations and assumptions in expandable detail.
- No independent-flip animation is presented as a sample from a confined/deconfined equilibrium ensemble.
- No gauge-variant alignment count is used as a physical time-orientation order parameter.
- Inline SVG/DOM is preferred to extra video downloads for responsive, accessible teaching animations.
- Scripts and styles extend the existing static page; no new framework or build dependency.

## Progress

- Plan recorded before implementation. Existing sources, tracked media, prior publication commits, and mobile fix inspected.

- Implemented guided four-step loop states, exact shared-grid counts, deterministic mixing illustration, video chapters and English WebVTT context captions. Browser checks are next. The original MP4 is unchanged.

- Author steering: remove demoralizing disclaimers throughout the public text. Teaching captions now explain the visual directly; assumptions and research directions are collected in one compact section. Preserve precise models and schematic labels without repeating defensive prose.

## Delivered architecture and evidence

Published website commit: `406e6d8`; successful deploy run: `38815185321`.
Canonical web code is `projects/timesarrow/index.html`, `landing.css`, and
`landing.js` in `space-cadet/website`. The source article repository retains
`manim-scenes/captions/t37-combined-walkthrough-en.vtt`; the website serves
an identical caption file under `media/timesarrow-walkthrough-en.vtt`.

- Four explicit story states keep private convention labels separate from
  independent link changes. Compass arrows remain fixed on relabeling.
- The shared grid uses integer side length 2–8; area is n² and perimeter 4n.
  Grid cells and boundary segments align on the same fixed lattice.
- Mixing dots use deterministic interpolation from separated to distributed
  colors. The clock panel depicts a shared future convention.
- Every animation is explicitly started and pausable. Timers stop when the
  document is hidden. Reduced-motion preference disables automatic playback;
  step buttons and sliders remain usable. Highlights are transient.
- Video chapter jumps are 0/10/19 seconds. Five English caption cues accompany
  the original silent MP4. Chapter testing needs an HTTP server supporting byte
  ranges; the initial Python preview server did not, while the range-capable
  preview and production server both passed.
- Public prose explains the illustrations directly. Scientific scope and next
  research steps are collected in a single compact section, per author request.

Local and live browser checks passed: all 64 vertex-relabeling cases, guided
loop products, counts (2,4,8)/(4,16,16)/(8,64,32), mixing/reset, play/pause,
reduced motion, five cues, 19-second seek, and zero page script errors.
Widths 320/375/768/1440 have no horizontal page overflow; video widths are
280/335/728/about 578 pixels respectively. Representative phone/desktop
screenshots were visually inspected. Node syntax and whitespace checks passed.

## Remaining work ownership

T13’s authorized website pass is complete. T37 retains recorded narration,
final video refinement, and author production approval. T36 retains manuscript
and scientific publication decisions. New public web scenes are available at
`#explore`, `#mechanism`, and `#two-arrows` on the landing page.
