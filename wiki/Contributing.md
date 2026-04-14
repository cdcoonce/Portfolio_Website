# Contributing

<!-- generated:start -->
## Local Setup

1. **Clone the repository**
   ```
   git clone https://github.com/cdcoonce/Portfolio_Website.git
   cd Portfolio_Website
   ```

2. **Install JavaScript dependencies**
   ```
   npm install
   ```

3. **Install Python dependencies** (requires [uv](https://github.com/astral-sh/uv))
   ```
   uv sync
   ```

4. **Run all tests**
   ```
   make test
   ```

## Make Targets

| Target | Command / Description |
|---|---|
| `make test` | Runs: test-js test-py |
| `make test-js` | `npm test` |
| `make test-py` | `uv run pytest -m "not slow"` |
| `make test-a11y` | `uv run pytest -m a11y` |
| `make test-e2e` | `uv run pytest -m e2e` |
| `make test-visual` | `uv run pytest -m slow` |
| `make lint` | `npm run lint` |
| `make check` | Runs: lint test |

## npm Scripts

| Script | Command |
|---|---|
| `npm run test` | `NODE_OPTIONS='--experimental-vm-modules' jest` |
| `npm run test:watch` | `NODE_OPTIONS='--experimental-vm-modules' jest --watch` |
| `npm run test:coverage` | `NODE_OPTIONS='--experimental-vm-modules' jest --coverage` |
| `npm run lint:css` | `stylelint 'WebContent/css/**/*.css'` |
| `npm run lint:js` | `eslint 'WebContent/js/**/*.js'` |
| `npm run lint` | `npm run lint:css && npm run lint:js` |
| `npm run serve` | `python3 -m http.server 8000` |
| `npm run format` | `prettier --write "**/*.{html,css,js,md,json}"` |
| `npm run format:check` | `prettier --check "**/*.{html,css,js,md,json}"` |

## Commit Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/).

Format: `<type>(<scope>): <subject>`

| Type | Purpose |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that is neither a fix nor a feature |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `chore` | Build process, tooling, maintenance |
| `style` | Formatting, whitespace — no logic change |
| `perf` | Performance improvement |
| `ci` | CI/CD pipeline changes |

**Examples:**
```
feat(wiki): add changelog generator
fix(chat): handle empty API response gracefully
docs(contributing): update setup instructions
```
<!-- generated:end -->

<!-- claude:prose -->
## Development Philosophy

### Test-First, Always

Every production code change in this project is preceded by a failing test. The red-green-refactor cycle isn't optional: write the test, watch it fail for the right reason, write the minimal code to pass, then clean up. This discipline exists because the portfolio has no staging environment — CI passing is the only gate before the live site. Tests that describe behavior before code is written prevent the common failure mode of tests that merely confirm the code you already wrote.

### Testing Pyramid

The test suite has four layers, each run with a different pytest marker:

| Layer | Marker | Command | What it covers |
| --- | --- | --- | --- |
| Unit / Integration | _(none)_ | `make test-py` | Pure logic, DOM structure, Lambda request/response |
| Accessibility | `a11y` | `make test-a11y` | WCAG compliance, ARIA labels, focus management |
| End-to-end | `e2e` | `make test-e2e` | User flows in a real browser via Playwright |
| Visual / slow | `slow` | `make test-visual` | Responsive screenshots, full-page visual checks |

`make test` (the CI gate) runs only the unmarked and `a11y` tests — E2E tests require the dev server to be running and are excluded from the default run to keep CI fast. Run `npm run serve` in one terminal, then `make test-e2e` in another if you need full E2E coverage locally.

### Jest and ES Modules

The JavaScript tests use Jest with native ES module support. Because Jest's module system predates the ES module spec, running ES module code in Jest requires the `--experimental-vm-modules` Node.js flag. This is set automatically via the `NODE_OPTIONS` environment variable in `npm run test`. The `jest.config.js` sets `"transform": {}` (no Babel transform) so Jest imports the source files directly without compilation. If you see `SyntaxError: Cannot use import statement outside a module` in a test, check that the test file is in `__tests__/` and that you haven't accidentally introduced a CommonJS `require()` call.

### CI Pipeline

Every push to `master` and every pull request runs the `check` job in `.github/workflows/ci-cd.yml` in this order:

1. **Prettier** (`npm run format:check`) — enforces consistent formatting across HTML, CSS, JS, Markdown, and JSON. Run `npm run format` to auto-fix before pushing.
2. **Stylelint** (`npm run lint:css`) — enforces CSS conventions in `WebContent/css/`.
3. **ESLint** (`npm run lint:js`) — enforces JS conventions in `WebContent/js/`. Key rules: `eqeqeq`, `no-var`, `prefer-const`.
4. **Jest** (`npm test`) — runs all JS unit tests.
5. **pytest** (`uv run pytest -m "not slow"`) — runs Python unit, validation, and accessibility tests. The checkout uses `fetch-depth: 0` so the changelog generator (which calls `git log`) has full history.

A push to `master` that passes CI also triggers the `deploy` job, which merges `master` into `gh-pages` for GitHub Pages hosting, and the `wiki-sync` job (in `wiki-sync.yml`) which regenerates and publishes all wiki pages.

### Knowledge Base and the Wiki

The Lambda chat agent's knowledge base is built from the Markdown context files in `WebContent/context/`. When you update a context file (bio, skills, a project entry), you need to redeploy the Lambda to pick up the changes — the knowledge base is bundled at deploy time, not read at request time. Use the `/deploy` skill in Claude Code to rebuild and redeploy automatically.

The wiki pages in `wiki/` are auto-generated from the source code by `scripts/wiki/orchestrate.py`. Generated sections (between `<!-- generated:start -->` and `<!-- generated:end -->`) are owned by the orchestrator and should never be edited manually — the next orchestrator run will overwrite them. Prose sections (between `<!-- claude:prose -->` and `<!-- claude:prose:end -->`) are maintained by the `/update-wiki` Claude Code skill.
<!-- claude:prose:end -->
