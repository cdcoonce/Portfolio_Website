# Projects Section Redesign — Implementation Plan

**Date:** 2026-03-03
**Branch:** `feat/projects-redesign`

## Problem

The main page currently renders all 17 project cards in a single grid. This creates a long, overwhelming scroll and buries the most impactful work. Users have no way to see a curated highlight without scrolling through everything.

## Goal

Redesign the projects section into two tiers:

1. **Main page (index.html):** Show a maximum of 4 project cards at a time. Default view displays "Featured" projects. Skill/tool filter buttons change which 4 projects are visible — any project can appear, not just featured ones.
2. **All-projects page (projects.html):** New standalone page showing the full 17-card gallery with its own filter controls, including a "Featured" filter option.

## Current Architecture

| Component | File | Description |
|-----------|------|-------------|
| HTML structure | `index.html` | Single-page site, 17 `<a class="project-card">` elements with `data-tags` attributes |
| Filter logic | `WebContent/js/filter.js` | Pure function `getFilteredVisibility()` + DOM-wiring `initFilter()` |
| Entry point | `WebContent/js/main.js` | Imports and initializes filter + carousel modules |
| Styles | `WebContent/css/style.css` | `.projects-grid` (CSS Grid), `.project-card`, `.skill-tag` |
| Responsive | `WebContent/css/mediaqueries.css` | Breakpoints at 1250px and 700px |
| Unit tests | `__tests__/filter.test.js` | Jest tests for `getFilteredVisibility` |
| E2E tests | `tests/test_gallery.py` | Playwright tests for filter UI behavior |
| Validation | `tests/test_validation.py` | HTML structure assertions (card count, featured count) |

**Key details:**
- 4 cards already have the `featured` class (lines 157, 181, 230, 551 of `index.html`)
- Filter uses OR logic: if any active filter matches any card tag, the card is visible
- Cards are shown/hidden via `display: flex | none` — no DOM insertion/removal
- No routing, no build tools, no frameworks — vanilla HTML/CSS/JS

## Phase Breakdown

| Phase | Document | Summary |
|-------|----------|---------|
| Phase 1 | [01-filter-logic.md](01-filter-logic.md) | Extend `filter.js` with new pure functions and config-driven `initFilter` |
| Phase 2 | [02-html-changes.md](02-html-changes.md) | Update `index.html` and create `projects.html` |
| Phase 3 | [03-css-changes.md](03-css-changes.md) | Add styles for projects footer and all-projects page |
| Phase 4 | [04-testing.md](04-testing.md) | Unit tests, validation tests, and E2E tests (TDD) |

## Files to Modify

| File | Action | Phase |
|------|--------|-------|
| `WebContent/js/filter.js` | Extend | 1 |
| `WebContent/js/main.js` | Modify | 1 |
| `index.html` | Modify | 2 |
| `projects.html` | **Create** | 2 |
| `WebContent/css/style.css` | Extend | 3 |
| `__tests__/filter.test.js` | Extend | 4 |
| `tests/test_validation.py` | Extend | 4 |
| `tests/test_gallery.py` | Modify + extend | 4 |
| `tests/conftest.py` | Extend | 4 |

## Verification Checklist

- [ ] `npx jest` — all unit tests pass
- [ ] `uv run pytest -m validation` — HTML structure tests pass
- [ ] `uv run pytest -m e2e` — Playwright E2E tests pass
- [ ] Manual: `index.html` loads with 4 featured cards visible
- [ ] Manual: clicking a skill filter shows up to 4 matching cards
- [ ] Manual: "View All Projects" link navigates to `projects.html`
- [ ] Manual: `projects.html` shows all 17 cards with working filters
- [ ] Manual: `projects.html?filter=python` pre-selects the python filter
