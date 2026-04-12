# Architecture Decision Log

This file records significant architectural decisions made during the development of the
portfolio website. It is maintained by Claude — there are no generated blocks here.
New entries are appended at the bottom; existing entries are never modified.

---

## ADL-001: No Framework or Bundler — Vanilla HTML/CSS/JS

**Date:** 2024-01-15
**Status:** Accepted

### Context

When starting the portfolio, the options were a framework-based SPA (React, Vue, Svelte)
with a bundler (Vite, Webpack) versus hand-written HTML/CSS/ES modules served directly by
GitHub Pages. A personal portfolio has no dynamic routing needs, no shared component state,
and a fixed content set. Build tooling adds dependency surface area, CI complexity, and a
learning tax for future contributors.

### Decision

Use vanilla HTML5, CSS3, and native ES modules with no framework and no bundler. Each page
is a standalone `.html` file. JavaScript is split into focused modules (`main.js`,
`filter.js`, `carousel.js`, `utils.js`) imported via `<script type="module">`.

### Consequences

- **Positive:** Zero build step — `git push` deploys immediately. No framework version
  drift. Any browser that supports ES2022 renders the site correctly.
- **Positive:** The entire frontend is readable source; no compiled artifact to debug.
- **Negative:** No hot-module replacement during development (`npm run serve` restarts the
  static server instead).
- **Negative:** No tree-shaking — unused exports in a module remain in the bundle. Mitigated
  by keeping modules small and focused.

---

## ADL-002: AWS Lambda for the Chat Agent (Not Edge Functions)

**Date:** 2024-06-10
**Status:** Accepted

### Context

The portfolio needed a conversational chat widget backed by an LLM. Deployment options
included Cloudflare Workers/Edge Functions (closer to the user, low cold-start), Vercel
Serverless, and AWS Lambda. The site is already hosted on GitHub Pages (static), so any
backend is a separate deployment target. The chat agent needs to load a knowledge-base
context file (~10 KB) and call the Anthropic API — both require secrets management.

### Decision

Deploy the chat agent as an AWS Lambda function (Python 3.12, `lambda_function.py`) behind
an API Gateway HTTP endpoint. Secrets (Anthropic API key) are stored in Lambda environment
variables. The knowledge-base context is bundled with the deployment package.

### Consequences

- **Positive:** AWS Secrets Manager / env vars are a well-understood pattern. The Lambda
  runtime handles concurrency automatically.
- **Positive:** `uv` can build a hermetic deployment zip with pinned dependencies — no
  runtime dependency resolution.
- **Negative:** Cold-start latency (~300–800 ms) is noticeable on first chat message after
  idle. Mitigated by keeping the function warm via scheduled pings if needed.
- **Negative:** AWS account overhead (IAM roles, API Gateway config) compared to a
  one-click edge deployment.

---

## ADL-003: Native ES Modules — No Transpiler

**Date:** 2024-01-15
**Status:** Accepted

### Context

ES modules (`import`/`export`) became baseline across all modern browsers in 2020.
Transpiling with Babel or TypeScript adds a build step, output artifacts, and source-map
complexity. The target audience for the portfolio (hiring managers, developers) uses modern
browsers. IE11 support is explicitly out of scope.

### Decision

Write all JavaScript as native ES2022 modules. Use `type="module"` on all `<script>` tags.
No Babel, no TypeScript compilation step. ESLint enforces `eqeqeq`, `no-var`, and
`prefer-const` at lint time.

### Consequences

- **Positive:** Source files are the deployed files — no source maps needed.
- **Positive:** Strict mode is automatic inside ES modules; accidental globals are a syntax
  error.
- **Negative:** Dynamic `import()` in tests requires Jest to be configured with the
  `--experimental-vm-modules` flag and `jest.config.js` to use `"transform": {}`.
- **Negative:** No TypeScript means type errors surface at runtime or in tests rather than
  at compile time.

---

## ADL-004: uv as the Python Package Manager

**Date:** 2024-07-01
**Status:** Accepted

### Context

The pytest test suite (validation, accessibility, E2E via Playwright) requires several
Python packages. Options were `pip` + `requirements.txt`, `pip` + `pyproject.toml`,
`poetry`, and `uv`. The project already used `pyproject.toml` for metadata. `uv` resolves
and installs the lockfile in under two seconds, is a single binary, and integrates cleanly
with `pyproject.toml`/`uv.lock`.

### Decision

Adopt `uv` as the sole Python toolchain: `uv sync` installs the virtual environment,
`uv run pytest` runs tests. The lockfile (`uv.lock`) is committed to the repository.
`pip` is not used directly anywhere in the project.

### Consequences

- **Positive:** `uv sync` is deterministic and fast — CI cold-start for Python deps dropped
  from ~45 s to ~6 s.
- **Positive:** Single command (`uv run pytest`) works without activating a virtual
  environment manually.
- **Negative:** Contributors must install `uv` (a one-time `curl | sh` step) before they
  can run Python tests. The README documents this.
- **Negative:** `uv` is younger than `pip`/`poetry` — edge cases in dependency resolution
  may surface on unusual platforms.

---

## ADL-005: Mobile-First CSS

**Date:** 2024-01-15
**Status:** Accepted

### Context

The portfolio is primarily browsed on desktop (a hiring manager's laptop), but must be
fully functional on mobile for initial discovery via LinkedIn or QR codes. Two approaches
were considered: desktop-first (override with `max-width` queries) and mobile-first (build
the base layout for small screens, enhance with `min-width` queries).

### Decision

Write all base styles for mobile viewports. Use `min-width` media queries in
`mediaqueries.css` to add layout complexity at 700 px (tablet/landscape phone) and 1250 px
(desktop). Custom CSS properties (variables) defined in `:root` are shared across all
breakpoints.

### Consequences

- **Positive:** The default render path (no media query match) is the simplest layout —
  single-column, full-width. This is also the fastest to paint on slow connections.
- **Positive:** Progressive enhancement means accessibility features (large tap targets,
  readable font sizes) are in the base layer, not overridden on mobile.
- **Negative:** Grid and flex layouts intended primarily for desktop require careful
  `min-width` layering to avoid unintended inheritance on tablet widths.
- **Negative:** The hamburger navigation (mobile) and the full nav bar (desktop) are
  implemented as the same element with visibility toggled by CSS — this requires discipline
  to keep the two states in sync when adding new nav items.
