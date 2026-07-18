# Theory Dashboard Deployment

**Date:** 2026-07-18
**Task:** T35a
**Deployed by:** Sage (local MacBook) via Cloudy's VPS

## Deployment Locations

### Source (GitHub-synced)
- Local: `~/.openclaw/workspace/code/timesarrow/theory/`
- VPS: `/home/cloudy/.openclaw/workspace/code/timesarrow/theory/`
- GitHub: `https://github.com/space-cadet/timesarrow/tree/main/theory`

### Deployed URLs
- **Main project page:** https://quantumofgravity.com/projects/timesarrow/
- **Theory dashboard:** https://quantumofgravity.com/projects/timesarrow/theory/
- **Numerics docs:** https://quantumofgravity.com/projects/timesarrow/numerics/

### VPS Filesystem Paths
```
/home/quantumofgravity/public_html/projects/timesarrow/
├── index.html          # Main landing page (hand-crafted)
├── numerics/           # Quarto-generated docs (deployed via GitHub Actions)
│   └── index.html
└── theory/             # Theory dashboard + docs (deployed manually)
    ├── index.html      # Dashboard (from pages/dashboard.html)
    ├── README.md
    ├── docs/
    │   ├── czx-intertwiner-analysis.md
    │   └── index.md
    └── pages/
        └── dashboard.html
```

## Deployment Procedure

1. **Pull latest changes** on VPS:
   ```bash
   cd /home/cloudy/.openclaw/workspace/code/timesarrow
   git pull origin main
   ```

2. **Copy to web directory**:
   ```bash
   sudo cp -r theory /home/quantumofgravity/public_html/projects/timesarrow/
   ```

3. **Fix permissions**:
   ```bash
   sudo chown -R quantumofgravity:quantumofgravity theory/
   sudo chmod -R 644 theory/*
   sudo chmod 755 theory/ theory/docs/ theory/pages/
   ```

4. **Update main page** (add "View Theory" button next to "View Numerics")

## Key Files

| File | Purpose | URL |
|------|---------|-----|
| `theory/index.html` | Dashboard | `/projects/timesarrow/theory/` |
| `theory/docs/czx-intertwiner-analysis.md` | T35a analysis | `/projects/timesarrow/theory/docs/czx-intertwiner-analysis.md` |
| `theory/docs/index.md` | Theory index | `/projects/timesarrow/theory/docs/index.md` |

## Notes

- The theory dashboard is vanilla HTML+JS with embedded JSON data
- Doc titles in dashboard link directly to markdown files
- Future: Consider converting markdown docs to HTML or adding a markdown renderer
- Numerics folder is deployed via GitHub Actions (separate workflow)
