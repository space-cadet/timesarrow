# Markdown Pilot

This directory contains a non-destructive pilot for authoring part of the manuscript in Markdown while still generating LaTeX for the final build.

Current scope:

- `z2-action.md`: Markdown-first source for the `Z_2` section
- `generated/z2-action.tex`: generated LaTeX output from Pandoc
- `z2-pilot.tex`: thin wrapper used to compile the generated section
- `scripts/render-z2-pilot.sh`: render Markdown to LaTeX
- `scripts/build-z2-pilot.sh`: render and compile the pilot PDF

The pilot is intentionally hybrid rather than pure Markdown:

- section and subsection structure use Markdown headings
- lists use Markdown lists
- equations, labels, `\autoref`, `\eqref`, and some citations remain raw LaTeX

This keeps the source readable while preserving the parts of the manuscript that depend on LaTeX-native features.

## Usage

From the repository root:

```bash
./markdown-pilot/scripts/render-z2-pilot.sh
./markdown-pilot/scripts/build-z2-pilot.sh
```

Outputs:

- generated TeX: `markdown-pilot/generated/z2-action.tex`
- pilot PDF: `markdown-pilot/build/z2-pilot.pdf`

## Why This Pilot Exists

The main manuscript is built on a custom SciPost LaTeX setup with many labels, citations, equations, and macros. This pilot tests the smallest safe migration shape before considering any larger conversion.
