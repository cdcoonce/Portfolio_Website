# Phase 0: Test Infrastructure Setup

**Impact:** Foundation — enables TDD workflow for all subsequent phases
**Prerequisites:** None — this phase must be completed first

---

## Overview

The TDD workflow defined in the project skill requires Jest (JS unit tests), pytest (HTML validation, accessibility, E2E, visual regression), linting tools, and supporting config files. None of this infrastructure currently exists. This phase sets it all up before any UI/UX work begins, so each subsequent phase can be validated with automated tests.

---

## Tasks

### 0.1 Install JavaScript testing and linting dependencies

**File:** `package.json`

Add devDependencies and scripts:

```bash
npm install --save-dev jest jest-environment-jsdom stylelint stylelint-config-standard eslint
```

**Updated scripts in `package.json`:**

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint:css": "stylelint 'WebContent/css/**/*.css'",
    "lint:js": "eslint 'WebContent/js/**/*.js'",
    "lint": "npm run lint:css && npm run lint:js",
    "serve": "python3 -m http.server 8000",
    "format": "prettier --write '**/*.{html,css,js,md,json}'",
    "format:check": "prettier --check '**/*.{html,css,js,md,json}'"
  }
}
```

### 0.2 Create Jest test stubs

**Directory:** `__tests__/`

Create stub test files that will be fleshed out as features are built:

**`__tests__/filter.test.js`:**

```javascript
'use strict';

describe('Gallery Filter Logic', () => {
  test.todo('filters projects by single category');
  test.todo('"All" resets to show every project');
  test.todo('multi-tag cards appear in multiple filter results');
  test.todo('deselecting all filters reverts to "All"');
});
```

**`__tests__/carousel.test.js`:**

```javascript
'use strict';

describe('Testimonial Carousel', () => {
  test.todo('advances to next testimonial');
  test.todo('goes to previous testimonial');
  test.todo('wraps from last to first');
  test.todo('wraps from first to last');
  test.todo('returns correct count for desktop vs mobile');
});
```

**`__tests__/utils.test.js`:**

```javascript
'use strict';

describe('Utility Functions', () => {
  test.todo('shared utilities work correctly');
});
```

### 0.3 Create pytest test directory and conftest

**Directory:** `tests/`

**`tests/conftest.py`:**

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

**Stub test files** (each with a placeholder test):

- `tests/test_validation.py` — HTML structure, alt text, no inline styles
- `tests/test_accessibility.py` — WCAG automated checks
- `tests/test_links.py` — Broken link detection
- `tests/test_gallery.py` — E2E: filter buttons toggle card visibility
- `tests/test_carousel.py` — E2E: testimonial navigation + wraparound
- `tests/test_responsive.py` — Screenshots at 320, 768, 1024, 1440px
- `tests/test_seo.py` — Meta tags, Open Graph, title

### 0.4 Create `pyproject.toml`

```toml
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

### 0.5 Create `Makefile`

```makefile
.PHONY: test test-js test-py test-a11y test-e2e test-visual lint check

test: test-js test-py

test-js:
	npm test

test-py:
	pytest -m "not slow"

test-a11y:
	pytest -m a11y

test-e2e:
	pytest -m e2e

test-visual:
	pytest -m slow

lint:
	npm run lint

check: lint test
	@echo "All checks passed."
```

### 0.6 Create `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2025-01-15

### Added

- Initial portfolio site launch
- Project gallery with filter system (17 project cards)
- Testimonial carousel with 7 testimonials
- Responsive layout with desktop and mobile breakpoints
- Profile section with hero, bio, and contact links
```

### 0.7 Confirm version baseline

**File:** `package.json`

Ensure `"version": "1.0.0"` is set as the baseline version.

---

## Testing Checklist

- [ ] `npm test` runs Jest and reports todo tests (no failures)
- [ ] `pytest --collect-only` discovers all test stubs
- [ ] `npm run lint:css` runs Stylelint on CSS files
- [ ] `npm run lint:js` runs ESLint on JS files
- [ ] `make check` runs the full lint + test pipeline
- [ ] `CHANGELOG.md` exists with correct format
- [ ] `package.json` version is `1.0.0`

---

## Dependencies

- Python 3 with pip (for pytest, playwright, beautifulsoup4, requests, axe-playwright-python)
- Node.js with npm (for Jest, Stylelint, ESLint)
- Playwright browsers: `python3 -m playwright install chromium`
