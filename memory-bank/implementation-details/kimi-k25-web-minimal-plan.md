# Implementation Detail: Minimal Static Web Presentation
*Created: 2026-04-18 02:55:00 IST*
*Last Updated: 2026-04-18 02:55:00 IST*

## Overview
A minimal static HTML presentation for "Gauging Time Reversal Symmetry in Quantum Gravity." This plan follows the KIRSS principle: minimal dependencies, no build tools, fast deployment, content-first approach.

---

## 1. Visual Layout (ASCII Diagrams)

### Full Page Structure
```
┌─────────────────────────────────────────────────────────────┐
│  NAV (sticky)                                               │
│  [Paper] [Supplementary] [arXiv] [GitHub]                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                                                     │  │
│  │     GAUGING TIME REVERSAL SYMMETRY                  │  │
│  │     IN QUANTUM GRAVITY                              │  │
│  │                                                     │  │
│  │     A mechanism for the cosmological                │  │
│  │     arrow of time from Z₂ gauge theory              │  │
│  │                                                     │  │
│  │     [Read the Paper] [View on arXiv]                │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ───────────────── SCROLL ───────────────────────────────── │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  SECTION: THE MYSTERY                             │  │
│  │                                                     │  │
│  │  Why does time move forward?                        │  │
│  │                                                     │  │
│  │  [Figure: Hourglass / Entropy gradient]           │  │
│  │                                                     │  │
│  │  Text: The laws of physics are time-reversible,   │  │
│  │  yet we experience a definite past-to-future flow. │  │
│  │  This asymmetry — the Arrow of Time — is usually  │  │
│  │  explained by entropy growth. Here, we propose    │  │
│  │  a different origin: symmetry breaking in the     │  │
│  │  quantum gravitational vacuum.                      │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ───────────────── SCROLL ───────────────────────────────── │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  SECTION: THE MECHANISM                             │  │
│  │                                                     │  │
│  │  Z₂ Gauging of Time Reversal                      │  │
│  │                                                     │  │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐        │  │
│  │  │ Before  │ → │ Gauge   │ → │ After   │        │  │
│  │  │         │    │         │    │         │        │  │
│  │  │  ⟷ ⟷   │    │  rule   │    │   →→    │        │  │
│  │  │  ⟷ ⟷   │    │  at each│    │   →→    │        │  │
│  │  │  point  │    │  point  │    │  point  │        │  │
│  │  │         │    │         │    │         │        │  │
│  │  │ Symmetric│    │         │    │ Broken  │        │  │
│  │  └─────────┘    └─────────┘    └─────────┘        │  │
│  │                                                     │  │
│  │  Text: By "gauging" time reversal — making it a   │  │
│  │  local rather than global symmetry — we force the │  │
│  │  quantum geometry to pick a preferred direction.  │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ───────────────── SCROLL ───────────────────────────────── │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  SECTION: THE MATH (Deep Dive)                    │  │
│  │                                                     │  │
│  │  Key Equations:                                     │  │
│  │                                                     │  │
│  │  $$ H = \sum_v \tau_v^2 $$  (Vertex term)         │  │
│  │                                                     │  │
│  │  $$ A_v \sim (-1)^{2j_v} $$  (Spin-foam amplitude) │  │
│  │                                                     │  │
│  │  [KaTeX rendered inline]                            │  │
│  │                                                     │  │
│  │  The transition from symmetric to broken phase      │  │
│  │  is a deconfinement transition in the Z₂ lattice    │  │
│  │  gauge theory.                                      │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ───────────────── SCROLL ───────────────────────────────── │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  SECTION: READ MORE                                 │  │
│  │                                                     │  │
│  │  • Full Paper (PDF)                                 │  │
│  │  • Supplementary Calculations                       │  │
│  │  • arXiv Preprint                                   │  │
│  │  • Code Repository                                  │  │
│  │                                                     │  │
│  │  Contact: [Author email]                          │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Mobile Layout (Simplified)
```
┌─────────────────┐
│  NAV (hamburger)│
├─────────────────┤
│                 │
│     TITLE       │
│     [Button]    │
│                 │
├─────────────────┤
│  THE MYSTERY    │
│  [Figure]       │
│  [Text...]      │
├─────────────────┤
│  THE MECHANISM  │
│  [Diagram]      │
│  [Text...]      │
├─────────────────┤
│  THE MATH       │
│  [Equation]     │
│  [Equation]     │
├─────────────────┤
│  READ MORE      │
│  [Links]        │
└─────────────────┘
```

---

## 2. Technical Architecture

### File Structure
```
/web-static/
├── index.html           (single page, semantic sections)
├── css/
│   ├── reset.css        (minimal reset)
│   ├── variables.css     (color/theme tokens)
│   ├── layout.css        (grid/flex utilities)
│   └── components.css    (section styling)
├── js/
│   └── katex-loader.js   (async KaTeX initialization)
├── figures/
│   ├── spin-network.svg  (exported from TikZ)
│   ├── z2-gauging.svg    (conceptual diagram)
│   └── phase-diagram.png (from paper figures/)
└── README.md             (deployment instructions)
```

### CSS Variables (Quantum Gravity Theme)
```css
:root {
  /* Colors */
  --bg-primary: #0a0c10;      /* Deep space black */
  --bg-secondary: #141820;    /* Lighter panel */
  --text-primary: #e8ecf1;    /* Off-white */
  --text-secondary: #8b9ab0;  /* Muted blue-gray */
  --accent: #00d4ff;          /* Cyan quantum */
  --accent-dim: #006680;      /* Darker cyan */
  --border: #1e2636;          /* Subtle borders */
  
  /* Typography */
  --font-body: system-ui, -apple-system, sans-serif;
  --font-mono: "SF Mono", Monaco, monospace;
  
  /* Spacing */
  --section-padding: 6rem;
  --content-max-width: 720px;
}
```

### KaTeX Integration (CDN)
```html
<link rel="stylesheet" 
      href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer 
        src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
        onload="renderMath()">
</script>
<script defer 
        src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js">
</script>
```

---

## 3. Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 640px | Single column, stacked nav, reduced padding |
| Tablet | 640-1024px | Two-column for mechanism section |
| Desktop | > 1024px | Max-width container, side margins |

---

## 4. Comparison with T13 (Next.js Approach)

| Aspect | T14 (This Plan) | T13 (Next.js) |
|--------|-----------------|---------------|
| Build tools | None | Next.js + React |
| Dependencies | KaTeX CDN only | npm packages (10+) |
| Interactivity | CSS only | Framer Motion, Three.js |
| Development time | 1-2 hours | 8-16 hours |
| Maintenance | Edit HTML directly | Build pipeline updates |
| Visual polish | Clean, minimal | High-fidelity animations |
| Math rendering | KaTeX (same) | KaTeX (same) |

---

## 5. Next Steps

1. **Create directory** `/web-static/` with file structure
2. **Write HTML**: Single semantic page with 4 sections
3. **Write CSS**: Dark theme with CSS variables
4. **Export figures**: Convert key TikZ diagrams to SVG
5. **Test locally**: Verify KaTeX renders, check mobile
6. **Deploy**: Use `deploy_web_app` tool with Netlify

---

## 6. Key Advantages of This Approach

- **Zero build time**: Open HTML file directly during development
- **No dependency drift**: No package.json to maintain
- **Fast iteration**: Edit → Refresh browser → Done
- **Reliable deployment**: Static files never have build failures
- **Accessible**: Screen readers handle semantic HTML well
- **Performance**: No JS bundle to download, instant first paint
