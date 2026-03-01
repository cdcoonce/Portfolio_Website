---
name: portfolio-website
description: >
  TDD workflow, coding standards, and versioning conventions for charleslikesdata.com.
  Use this skill whenever working on the portfolio site — adding project cards, editing
  sections, writing tests, creating branches, making commits, or reviewing code. Trigger
  on any mention of the portfolio, website, charleslikesdata, project cards, testimonials,
  gallery filtering, or responsive styling.
---

# Portfolio Website — TDD, Standards & Versioning

## 1. Test-Driven Development (TDD)

All feature work and bug fixes follow **Red → Green → Refactor**.

### Testing Stack

| Layer | Tool | Language | Purpose |
|---|---|---|---|
| JS Unit | **Jest + jsdom** | JS | Pure JS logic: filtering, carousel state, utilities |
| HTML Validation | **pytest + BeautifulSoup** | Python | Semantic markup, alt text, no inline styles |
| Accessibility | **pytest + axe-playwright** | Python | WCAG 2.1 AA compliance |
| Link Checking | **pytest + requests** | Python | Verify all hrefs/srcs resolve |
| Integration / E2E | **pytest + playwright** | Python | Browser tests: filtering, carousel, nav |
| Visual Regression | **pytest + playwright** | Python | Screenshot comparison at breakpoints |
| CSS Linting | **Stylelint** (npm) | JS | CSS rule validation |

### Test File Layout

```
__tests__/                         # Jest (JS unit tests)
├── filter.test.js
├── carousel.test.js
└── utils.test.js

tests/                             # pytest (Python test suite)
├── conftest.py                    # Shared fixtures: browser, page, local server
├── test_validation.py             # HTML structure, alt text, no inline styles
├── test_accessibility.py          # WCAG automated checks
├── test_links.py                  # Broken link detection
├── test_gallery.py                # E2E: filter buttons toggle card visibility
├── test_carousel.py               # E2E: testimonial navigation + wraparound
├── test_responsive.py             # Screenshots at 320, 768, 1024, 1440px
└── test_seo.py                    # Meta tags, Open Graph, title
```

### Shared Fixtures (conftest.py)

```python
import pytest
import subprocess
import time
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='session')
def server():
    """Start a local HTTP server for the static site."""
    proc = subprocess.Popen(
        ['python3', '-m', 'http.server', '8000'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    yield 'http://localhost:8000'
    proc.terminate()

@pytest.fixture(scope='session')
def browser():
    """Provide a shared Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser, server):
    """Provide a fresh page loaded with the site for each test."""
    page = browser.new_page()
    page.goto(server)
    yield page
    page.close()
```

### pytest Configuration (pyproject.toml)

Python dependencies are managed with **uv**. The `pyproject.toml` serves as both the uv project manifest and the pytest config.

```toml
[project]
name = "portfolio-website-tests"
version = "0.1.0"
requires-python = ">=3.11"

[dependency-groups]
dev = [
  "pytest",
  "pytest-playwright",
  "axe-playwright-python",
  "requests",
  "beautifulsoup4",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "slow: visual regression tests",
    "a11y: accessibility tests",
    "e2e: end-to-end browser tests",
    "validation: HTML/CSS validation tests",
]
addopts = "-v --tb=short"
```

Install Python dependencies with:

```bash
uv sync
uv run playwright install chromium
```

### TDD Workflow

1. **Red** — Write a failing test (Jest for JS logic, pytest for everything else)
2. **Green** — Minimum code to pass
3. **Refactor** — Clean up, tests stay green
4. **Verify** — Full suite before committing:
   ```bash
   make check
   ```

### What to Test

| Area | Tool | Examples |
|---|---|---|
| Filter logic | Jest | Correct output per category; "All" resets; multi-tag cards |
| Carousel state | Jest | Next/prev index; wraparound; initial state |
| HTML validity | pytest | Semantic elements; no inline styles/JS; alt text on images |
| Accessibility | pytest | WCAG AA; focus order; color contrast |
| Links | pytest | External links resolve; mailto/social well-formed |
| Gallery E2E | pytest | Filter buttons toggle card visibility in real browser |
| Carousel E2E | pytest | Nav clicks advance slides; wraparound works |
| Responsive | pytest | Screenshots at 320px, 768px, 1024px, 1440px |
| SEO | pytest | Meta description; Open Graph tags; title tag |

### Example Tests

**HTML validation (test_validation.py)**:
```python
from bs4 import BeautifulSoup
from pathlib import Path

def test_all_images_have_alt_text():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        assert img.get('alt'), f'Missing alt text: {img}'

def test_semantic_structure():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find('header'), 'Missing <header>'
    assert soup.find('main'), 'Missing <main>'
    assert soup.find('footer'), 'Missing <footer>'
    assert soup.find('nav'), 'Missing <nav>'

def test_no_inline_styles():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    styled = soup.find_all(style=True)
    assert len(styled) == 0, f'{len(styled)} elements with inline styles'
```

**Accessibility (test_accessibility.py)**:
```python
import pytest
from axe_playwright_python.sync_playwright import Axe

@pytest.mark.a11y
def test_wcag_compliance(page):
    axe = Axe()
    results = axe.run(page)
    violations = results.response.get('violations', [])
    serious = [v for v in violations if v['impact'] in ('serious', 'critical')]
    assert len(serious) == 0, (
        f'{len(serious)} serious a11y violations: '
        + ', '.join(v["id"] for v in serious)
    )
```

**E2E gallery (test_gallery.py)**:
```python
import pytest

@pytest.mark.e2e
def test_filter_shows_only_matching_cards(page):
    page.click('button:has-text("Python")')
    visible = page.locator('.project-card:visible')
    for i in range(visible.count()):
        tags = visible.nth(i).get_attribute('data-tags')
        assert 'python' in tags.lower()

@pytest.mark.e2e
def test_all_filter_shows_every_card(page):
    page.click('button:has-text("All")')
    total = page.locator('.project-card').count()
    visible = page.locator('.project-card:visible').count()
    assert visible == total
```

**Link checking (test_links.py)**:
```python
import pytest
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def get_external_links():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)
            if a['href'].startswith('http')]

@pytest.mark.parametrize('url', get_external_links())
def test_external_link_resolves(url):
    resp = requests.head(url, allow_redirects=True, timeout=10)
    assert resp.status_code < 400, f'{url} returned {resp.status_code}'
```

### Runner Scripts

**package.json**:
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint:css": "stylelint 'WebContent/css/**/*.css'",
    "lint:js": "eslint 'WebContent/js/**/*.js'",
    "lint": "npm run lint:css && npm run lint:js",
    "serve": "python3 -m http.server 8000"
  }
}
```

**Makefile**:
```makefile
.PHONY: test test-js test-py test-a11y test-e2e test-visual lint check

test: test-js test-py

test-js:
	npm test

test-py:
	uv run pytest -m "not slow"

test-a11y:
	uv run pytest -m a11y

test-e2e:
	uv run pytest -m e2e

test-visual:
	uv run pytest -m slow

lint:
	npm run lint

check: lint test
	@echo "All checks passed."
```

---

## 2. Coding Standards

### Formatting

Enforced via `.editorconfig` and `.prettierrc`:
2 spaces, 100 char width, single quotes (JS), semicolons, LF, UTF-8, final newline.

### HTML

- Semantic elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Every `<img>` gets descriptive `alt` text
- `<button>` for interactive controls — not styled `<div>`s
- IDs for JS hooks; classes for styling
- Attribute order: `id`, `class`, `data-*`, `src/href`, `alt/title`, `aria-*`
- No inline styles or inline JS

### CSS

- **BEM naming**: `.block__element--modifier`
- **CSS custom properties** in `:root` for colors, fonts, spacing, breakpoints
- **Mobile-first**: base styles for mobile, `@media (min-width: ...)` for larger
- Media queries grouped at the bottom of each component section
- No `!important`; prefer `rem`/`em` over `px`

### JavaScript

- `'use strict';` at the top of every file
- `const` by default, `let` when needed, never `var`
- Descriptive names — no abbreviations
- Single responsibility functions; extract helpers aggressively
- Separate pure logic from DOM manipulation:
  ```js
  // Pure (testable)
  const getFilteredProjects = (projects, category) =>
    category === 'all'
      ? projects
      : projects.filter(p => p.tags.includes(category));

  // DOM (thin wrapper)
  const renderFilteredProjects = (category) => {
    const filtered = getFilteredProjects(allProjects, category);
    updateCardVisibility(filtered);
  };
  ```
- JSDoc on all public functions
- No magic numbers or strings — use named constants

### Python (test code)

- PEP 8 compliant
- Descriptive test names that read as specs:
  ```python
  def test_python_filter_shows_only_python_tagged_cards():
  def test_carousel_wraps_from_last_to_first_slide():
  ```
- Use `@pytest.mark` to categorize; fixtures for shared setup; `parametrize` for data-driven tests

### File Organization

```
WebContent/js/
├── main.js          # Entry point (DOMContentLoaded init)
├── filter.js        # Gallery filtering
├── carousel.js      # Testimonial carousel
└── utils.js         # Shared utilities

WebContent/css/
├── main.css         # Global styles + CSS custom properties
├── layout.css       # Page grid
├── components/
│   ├── nav.css
│   ├── hero.css
│   ├── gallery.css
│   ├── carousel.css
│   └── footer.css
└── utilities.css    # Reusable helpers
```

---

## 3. Professional Versioning

### Semantic Versioning

`MAJOR.MINOR.PATCH` tracked in `package.json`:

| Bump | When | Examples |
|---|---|---|
| MAJOR | Breaking redesign, restructured sections | Full site overhaul |
| MINOR | New feature/section (backward-compatible) | New project card, new filter category |
| PATCH | Bug fix, typo, style tweak, content update | Fix broken link, adjust spacing |

### Branching (GitHub Flow)

```
gh-pages (production — live on charleslikesdata.com)
  ↑ merge from master to deploy
master (development — all feature branches merge here)
  └── feature/add-tableau-project
  └── fix/broken-resume-link
  └── chore/update-dependencies
  └── refactor/extract-filter-logic
  └── docs/update-readme
```

- `gh-pages` is the deployment branch — merging `master` into `gh-pages` triggers GitHub Pages
- `master` is the integration branch — all feature work merges here first
- All work on feature branches: `{type}/{short-description}`

### Commits (Conventional Commits)

```
<type>(<scope>): <short description>
```

**Types**: `feat`, `fix`, `refactor`, `style`, `test`, `docs`, `chore`, `build`
**Scopes**: `gallery`, `carousel`, `hero`, `nav`, `footer`, `a11y`, `ci`, `deps`

Rules: imperative mood, ≤72 char subject, no trailing period, reference issues in footer.

**Examples**:
```
feat(gallery): add Manufacturing Downtime Analysis project card
fix(carousel): correct wraparound past last testimonial
test(gallery): add pytest E2E tests for multi-tag filtering
refactor(filter): extract pure logic from DOM manipulation
chore(deps): add pytest-playwright to test dependencies
```

### Release Workflow

1. Branch from `master`
2. Implement with TDD (red/green/refactor)
3. `make check` passes
4. Open PR to `master` with checklist:
   - [ ] All tests pass
   - [ ] No lint errors
   - [ ] HTML validates
   - [ ] Accessibility passes
   - [ ] Responsive tested at 320, 768, 1024, 1440px
   - [ ] Version bumped in `package.json`
   - [ ] CHANGELOG updated
5. Merge PR into `master`
6. Tag on `master`: `git tag -a v1.2.0 -m "feat: add new project cards"`
7. **Deploy**: merge `master` into `gh-pages` to push live
   ```bash
   git checkout gh-pages
   git merge master
   git push origin gh-pages
   git checkout master
   ```

### CHANGELOG (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]

## [1.1.0] - 2026-02-28
### Added
- Manufacturing Downtime Analysis project card

### Fixed
- Carousel wraparound bug

## [1.0.0] - 2025-01-15
### Added
- Initial launch
```

---

## Development Checklist

1. **Branch** — `{type}/{short-description}` from `master`
2. **Test first** — Failing test (Jest for JS, pytest for everything else)
3. **Implement** — Minimum to pass
4. **Refactor** — Clean up, tests green
5. **Verify** — `make check`
6. **Version** — Bump `package.json`
7. **Changelog** — Update `CHANGELOG.md`
8. **Commit** — Conventional Commit format
9. **PR** — Merge to `master`, checklist complete
10. **Tag** — Release tag on `master`
11. **Deploy** — Merge `master` → `gh-pages` to go live
