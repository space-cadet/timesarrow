# Markdown-First Z2 Pilot
*Created: 2026-05-09 11:22:52 IST*
*Last Updated: 2026-05-09 12:03:05 IST*
*Related Task: T19*

## Purpose
Document the proof-of-concept workflow for authoring the manuscript's `Z_2` section in Markdown while generating LaTeX and preserving the current `timesarrow.tex` build path.

## Scope
- Pilot only the `Z_2` section currently in `timesarrow.tex:1013-1095`
- Keep the main manuscript source unchanged
- Validate a standalone build before any full-manuscript integration

## Artifacts
- `markdown-pilot/z2-action.md` — Markdown-first section source
- `markdown-pilot/generated/z2-action.tex` — Pandoc-generated LaTeX
- `markdown-pilot/z2-pilot.tex` — standalone wrapper
- `markdown-pilot/scripts/render-z2-pilot.sh` — render script
- `markdown-pilot/scripts/build-z2-pilot.sh` — build script
- `markdown-pilot/scripts/normalize_inline_math.py` — preprocessing helper
- `markdown-pilot/build/z2-pilot.pdf` — standalone verification artifact

## Workflow Decisions
- Use a hybrid model rather than pure Markdown: keep equations, labels, references, and citations in raw LaTeX.
- Normalize spaced inline math like `$ Z_2 $` before Pandoc render, since Pandoc treats that spacing as plain text.
- Replace LaTeX-style prose quotes in the Markdown source with plain quoted prose so Markdown parsing stays stable.
- Keep the standalone wrapper generic (`article` + `biblatex`) for the pilot; defer SciPost styling to the full-manuscript integration step.

## Verification
- Rendered `markdown-pilot/z2-action.md` to `markdown-pilot/generated/z2-action.tex`
- Built `markdown-pilot/build/z2-pilot.pdf` successfully
- Confirmed that equations, sectioning, lists, and bibliography render correctly in the standalone PDF
- Confirmed that unresolved `??` references are expected because the pilot wrapper excludes the rest of the manuscript

## Findings
- Markdown is viable for prose, headings, and list-heavy parts of the section.
- Raw LaTeX is still the right representation for equations and manuscript cross-references.
- The generated output is readable enough to support a Markdown-first authoring flow, but a full-manuscript test is required before broader migration.
- The main technical risk is not Markdown itself; it is preserving reference resolution and journal-specific formatting once the generated section is inserted back into the full manuscript.

## Recommended Next Step
Temporarily replace the handwritten `Z_2` section in `timesarrow.tex` with an `\input{markdown-pilot/generated/z2-action.tex}` path and build the full SciPost manuscript. That will test numbering, cross-reference resolution, bibliography behavior, and page-layout drift under the real document class.
