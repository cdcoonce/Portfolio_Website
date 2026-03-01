# Portfolio Website — charleslikesdata.com

## Project

Personal data analytics portfolio for Charles Coonce. Static site hosted on GitHub Pages.

- **Live**: https://charleslikesdata.com
- **Repo**: https://github.com/cdcoonce/Portfolio_Website
- **Dev branch**: `master` (all feature work merges here)
- **Deploy branch**: `gh-pages` (merge `master` → `gh-pages` to deploy)
- **Stack**: Vanilla HTML5 + CSS3 + JavaScript — no frameworks, no build tools

## Structure

```
Portfolio_Website/
├── index.html              # Single-page site (nav, hero, gallery, testimonials, footer)
├── 404.html                # Custom 404
├── CNAME                   # GitHub Pages custom domain
├── package.json            # Metadata, npm scripts
├── Makefile                # Unified test/lint runner
├── requirements-test.txt   # Python test dependencies
├── .editorconfig           # Editor formatting
├── .prettierrc             # Prettier config
├── WebContent/
│   ├── assets/             # Images and icons (per-project subfolders)
│   ├── css/                # Stylesheets
│   └── js/                 # Scripts
├── __tests__/              # Jest (JS unit tests)
├── tests/                  # pytest (validation, a11y, e2e, visual)
└── .claude/
    └── skills/             # Claude Code skills
```

## Quick Commands

```bash
npm test                # JS unit tests (Jest)
pytest                  # Python tests (validation, a11y, e2e)
pytest -m a11y          # Accessibility only
pytest -m e2e           # Browser integration only
make check              # Full suite: lint + JS tests + Python tests
npm run serve           # Local dev server at localhost:8000
```

## Formatting

- 2 spaces, 100 char width, single quotes, semicolons, LF, UTF-8

## Skills

Before writing any code, creating branches, making commits, or running tests on this project,
read the relevant skill in `.claude/skills/`:

- **`.claude/skills/portfolio-website/SKILL.md`** — Read this before any development work.
  Covers the TDD workflow (what to test, how to structure tests, which tool for which layer),
  coding standards (HTML, CSS, JS, and Python conventions), and versioning rules (branching,
  commit messages, release process). Do not skip this step.
