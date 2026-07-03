# Home

<!-- generated:start -->
## portfoliowebsite v2.0.0

Charles Coonce's personal portfolio site — an **Astro** (static output) app with **React islands**, deployed to GitHub Pages (production) and Cloudflare Pages (staging). Live at [charleslikesdata.com](https://charleslikesdata.com).

### Tech Stack

| Language / Tool | Version / Notes |
|---|---|
| Astro (framework, static output) | `7.0.6` |
| React (islands via `@astrojs/react`) | `19.2.7` |
| Node.js | 22 (see CI workflows) |
| Jest (JS test runner) | `30.2.0` |
| ESLint | `10.0.2` |
| Prettier | `3.6.2` |
| Python | `>=3.11` (wiki tooling) |
| uv (Python package manager) | see `pyproject.toml` |
| Python dev deps | `anthropic`, `pytest`, `pytest-playwright`, `axe-playwright-python`, `requests`, `beautifulsoup4`, `pyyaml` |

### Dev & Test Commands

| Command | Description |
|---|---|
| `npm run dev` | Start the Astro dev server |
| `npm run build` | Build the static site to `dist/` |
| `npm run preview` | Preview the built site locally |
| `npm test` | Run the JS unit suite (Jest — `src/lib/*`) |
| `npm run test:coverage` | JS tests with coverage report |
| `npm run lint` | Stylelint (CSS) + ESLint (JS) |

### npm Scripts

| Script | Command |
|---|---|
| `npm run dev` | `astro dev` |
| `npm run start` | `astro dev` |
| `npm run build` | `astro build` |
| `npm run preview` | `astro preview` |
| `npm run astro` | `astro` |
| `npm run test` | `NODE_OPTIONS='--experimental-vm-modules' jest` |
| `npm run test:watch` | `NODE_OPTIONS='--experimental-vm-modules' jest --watch` |
| `npm run test:coverage` | `NODE_OPTIONS='--experimental-vm-modules' jest --coverage` |
| `npm run lint:css` | `stylelint 'src/**/*.css'` |
| `npm run lint:js` | `eslint 'src/**/*.js' '__tests__/**/*.js'` |
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
