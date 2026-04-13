# Charles Coonce — Portfolio

![HTML5](https://img.shields.io/badge/HTML5-Semantic-E34F26) ![CSS3](https://img.shields.io/badge/CSS3-Custom_Properties-1572B6) ![JavaScript](https://img.shields.io/badge/JavaScript-ES2022_Modules-F7DF1E) ![GitHub Pages](https://img.shields.io/badge/Hosting-GitHub_Pages-222222) ![Prettier](https://img.shields.io/badge/Formatting-Prettier-F7B93E) ![Jest](https://img.shields.io/badge/Tests-Jest_+_Playwright-C21325)

A multi-page static portfolio built with vanilla HTML5, CSS3, and ES module JavaScript — no frameworks, no bundlers, no build step.

**Live site:** [charleslikesdata.com](https://charleslikesdata.com)

---

## Local Setup

```bash
git clone https://github.com/cdcoonce/Portfolio_Website.git
cd Portfolio_Website
npm install
uv sync && uv run playwright install chromium
```

Start a local dev server:

```bash
npm run serve
# → http://localhost:8000
```

## Tests

```bash
npm test              # Jest unit tests (filter, carousel, utils)
uv run pytest         # Python suite (validation, accessibility, E2E)
make check            # Full suite — lint + JS tests + Python tests
```

---

Full documentation: [GitHub Wiki](../../wiki)
