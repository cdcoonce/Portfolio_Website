# Testing

<!-- generated:start -->
## JavaScript Tests

| File | Type | Describe Blocks |
|---|---|---|
| `carousel.test.js` | Jest | CAROUSEL_CONFIG, getNextIndex, getPrevIndex, +3 more |
| `chat.test.js` | Jest | Rate Limiting, Rate Limiting with injected storage, escapeHtml, +2 more |
| `filter.test.js` | Jest | getFilteredVisibility, applyMaxVisible, getFeaturedVisibility, +3 more |
| `projects.test.js` | Jest | projects data, tags derived registry, TAG_LABELS, +1 more |
| `renderer.test.js` | Jest | createProjectCard, renderProjectCards, renderFilterButtons |
| `utils.test.js` | Jest | getItemsToShow, isDesktop, formatProjectDate |

### Jest Configuration

| Setting | Value |
|---|---|
| `testEnvironment` | `jest-environment-jsdom` |

## Python Tests

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
