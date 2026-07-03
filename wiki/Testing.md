# Testing

<!-- generated:start -->
## Test Strategy

The unit suite runs on **Jest** and covers the framework-free logic in `src/lib/*` — `carousel.js` (pure wrap-around index math + initials) and `chat.js` (rate limiting, assistant-markdown rendering, and the Lambda `sendMessage` client). These are the modules the React islands import, so testing them directly keeps the fast unit layer independent of the DOM. A Python/**Playwright** E2E suite under `tests/` targets the **retired vanilla DOM** and is **not run in CI** — porting it to the Astro + React UI is a tracked follow-up.

## JavaScript Tests (Jest)

| File | Type | Describe Blocks |
|---|---|---|
| `portfolio-carousel.test.js` | Jest | carousel index math, initials |
| `portfolio-chat.test.js` | Jest | rate limiting, renderAssistantMarkdown, sendMessage |

### Jest Configuration

| Setting | Value |
|---|---|
| `testEnvironment` | `jest-environment-jsdom` |

## Python Tests

Wiki-generator tests (`tests/test_wiki_phase*.py`) run in CI. The Playwright E2E tests (`tests/test_*.py` for the site DOM) target the retired vanilla markup and are **pending a port** to the Astro + React UI — they are not part of the CI gate.

| File | Location |
|---|---|
| `test_accessibility.py` | `tests` |
| `test_build_knowledge_base.py` | `tests` |
| `test_carousel.py` | `tests` |
| `test_chat.py` | `tests` |
| `test_gallery.py` | `tests` |
| `test_hero.py` | `tests` |
| `test_links.py` | `tests` |
| `test_nav.py` | `tests` |
| `test_responsive.py` | `tests` |
| `test_seo.py` | `tests` |
| `test_validation.py` | `tests` |
| `test_wiki_phase1.py` | `tests` |
| `test_wiki_phase2.py` | `tests` |
| `test_wiki_phase3.py` | `tests` |
| `test_wiki_phase4.py` | `tests` |
| `test_lambda.py` | `lambda/tests` |

## Pytest Markers

| Marker | Description | Run Command |
|---|---|---|
| `slow` | visual regression tests | `uv run pytest -m slow` |
| `a11y` | accessibility tests | `uv run pytest -m a11y` |
| `e2e` | end-to-end browser tests | `uv run pytest -m e2e` |
| `validation` | HTML/CSS validation tests | `uv run pytest -m validation` |
<!-- generated:end -->
