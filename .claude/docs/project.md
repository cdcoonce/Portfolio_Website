# Portfolio Website — Project Context

Personal portfolio website for a Data Engineer, showcasing data analytics projects with an AI-powered chat agent. Static site hosted on GitHub Pages with a serverless Lambda backend.

## Tech Stack

- **HTML5 / CSS3 / JavaScript ES6+ Modules** — no framework, no bundler, no build step
- **AWS Lambda** + **Anthropic Claude Haiku** — serverless chat agent (`lambda/`)
- **Jest** + **jsdom** — JavaScript unit tests (`__tests__/`)
- **pytest** + **Playwright** + **axe-core** — E2E, validation, accessibility tests (`tests/`)
- **Prettier / ESLint / Stylelint** — frontend formatting and linting
- **ruff** — Python linting
- **uv** — Python package manager
- **npm** — Node.js package manager
- **GitHub Actions** — CI/CD pipeline (lint → test → deploy)

## Project Layout

```text
index.html                        # Home page (hero, 4 featured projects, carousel, chat)
projects.html                     # Full project gallery (filterable cards)
404.html                          # Custom error page
WebContent/
  assets/                         # Images, icons, resume PDF
  css/
    style.css                     # Global styles, custom properties
    mediaqueries.css              # Responsive breakpoints (1250px, 700px)
  js/
    main.js                       # Entry point, page detection, component init
    filter.js                     # Project filtering & visibility logic
    carousel.js                   # Testimonial carousel & pagination
    chat.js                       # Chat agent UI, rate limiting, Lambda calls
    utils.js                      # Viewport breakpoint helpers
  context/                        # Markdown files compiled into Lambda knowledge base
lambda/
  lambda_function.py              # AWS Lambda handler
  knowledge_base.json             # Compiled portfolio context (from context/ files)
  requirements.txt                # anthropic>=0.40.0
scripts/
  build_knowledge_base.py         # Compiles context/ markdown → knowledge_base.json
__tests__/                        # Jest unit tests (filter, carousel, chat, utils)
tests/                            # pytest E2E, validation, accessibility
  conftest.py                     # Fixtures (HTTP server, Playwright browser)
docs/
  plans/                          # Implementation plans (archive/ for completed)
  code_reviews/                   # Code review reports
.github/workflows/ci-cd.yml      # GitHub Actions pipeline
```

## Test Markers

- `uv run pytest` — run all tests (excludes slow by default via config)
- `uv run pytest -m validation` — HTML structure, semantics, alt text
- `uv run pytest -m a11y` — WCAG 2.1 AA accessibility (axe-core)
- `uv run pytest -m e2e` — Playwright browser tests
- `uv run pytest -m "not slow"` — skip visual regression tests
- `npx jest` — JavaScript unit tests
- `make test` — Jest + pytest combined
- `make check` — lint + all tests

## Key Architecture Patterns

- **Pure functions + orchestrators**: Business logic in pure, testable functions; `init*()` functions wire to DOM. Example: `filter.js` exports `getFilteredVisibility()`, `initFilter()` orchestrates.
- **Page-aware init**: `<body data-page="home|projects">` tells `main.js` which components to initialize.
- **ES modules (native)**: `type="module"` in HTML, `import/export` in JS, no bundler.
- **Knowledge base compilation**: Python script reads `WebContent/context/*.md` → `lambda/knowledge_base.json`. Lambda loads JSON at startup, builds system prompt dynamically.
- **Mobile-first CSS**: Custom properties for theming, breakpoints at 1250px and 700px.
- **Two-branch deployment**: `master` (dev) → `gh-pages` (production), auto-synced by CI.

## Git Conventions

- **Conventional commits**: `feat(scope)`, `fix(scope)`, `test(scope)`, `docs(scope)`, `chore`, `refactor`
- **Scopes**: `gallery`, `carousel`, `hero`, `nav`, `footer`, `a11y`, `ci`, `chat`, `lambda`
- **Branch naming**: `feat/description`, `fix/description`, `docs/description`
