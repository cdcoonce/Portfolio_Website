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

<!-- claude:prose:end -->
