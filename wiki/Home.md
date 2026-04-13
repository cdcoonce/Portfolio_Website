# Home

<!-- generated:start -->
## portfoliowebsite v1.5.0

### Tech Stack

| Language / Tool | Version / Notes |
|---|---|
| Node.js | see `.nvmrc` or system Node |
| Python | `>=3.11` |
| Jest (JS test runner) | `30.2.0` |
| ESLint | `10.0.2` |
| Prettier | `3.6.2` |
| uv (Python package manager) | see `pyproject.toml` |
| Python dev deps | `anthropic`, `pytest`, `pytest-playwright`, `axe-playwright-python`, `requests`, `beautifulsoup4`, `pyyaml` |

### Test Commands

| Command | Description |
|---|---|
| `npm test` | Run JavaScript test suite (Jest) |
| `npm run test:coverage` | JS tests with coverage report |
| `uv run pytest` | Run Python test suite |
| `uv run pytest --cov=src --cov-report=term-missing` | Python tests with coverage |

### npm Scripts

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

### Wiki Pages

- [Home](Home) — this page
- [Architecture](Architecture)
- [Frontend Modules](Frontend-Modules)
- [Lambda Chat Agent](Lambda-Chat-Agent)
- [Testing](Testing)
- [CSS Design System](CSS-Design-System)
- [Knowledge Base](Knowledge-Base)
- [Contributing](Contributing)
- [CI/CD Pipeline](CI-CD-Pipeline)
- [Changelog](Changelog)
- [Architecture Decision Log](Architecture-Decision-Log)
<!-- generated:end -->
