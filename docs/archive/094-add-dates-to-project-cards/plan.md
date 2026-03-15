# Plan: Add Dates to Project Cards (Issue #94)

## Context

Project cards currently show no date information. Visitors can't tell which projects are recent vs. earlier work, making it harder to assess skill growth. This plan adds dates to context files, HTML cards, the knowledge base, and sorts projects newest-first.

## Design Decisions

- Date displayed **below the title**, above the description (small muted text)
- Dates sourced from **GitHub repo creation dates**
- `data-date="YYYY-MM"` attribute on cards for JS sorting
- All projects get a single `Mon YYYY` date — no ranges, no "Present"

## Project Date Reference

| Context File | Date | Sort Key |
|---|---|---|
| housing-affordability.md | Dec 2025 | 2025-12 |
| renewable-asset-pipeline.md | Dec 2025 | 2025-12 |
| synthetic-signal-observatory.md | Dec 2025 | 2025-12 |
| ames-housing.md | Oct 2025 | 2025-10 |
| energy-analytics-pipeline.md | Jun 2025 | 2025-06 |
| spaceship-titanic.md | May 2025 | 2025-05 |
| baby-names.md | Mar 2025 | 2025-03 |
| motor-vehicle-thefts.md | Mar 2025 | 2025-03 |
| restaurant-sales.md | Mar 2025 | 2025-03 |
| airbnb-listing.md | Feb 2025 | 2025-02 |
| electricity-consumption.md | Feb 2025 | 2025-02 |
| global-co2-emissions.md | Feb 2025 | 2025-02 |
| manufacturing-downtime.md | Feb 2025 | 2025-02 |
| nyc-collision.md | Feb 2025 | 2025-02 |
| sleep-deprivation.md | Feb 2025 | 2025-02 |
| data-archive.md | Dec 2024 | 2024-12 |
| wine-quality.md | Nov 2024 | 2024-11 |
| national-parks-dashboard.md | Sep 2024 | 2024-09 |
| world-happiness.md | Sep 2024 | 2024-09 |
| national-parks-analysis.md | Aug 2024 | 2024-08 |
| portfolio-website.md | Aug 2024 | 2024-08 |

## Phases

Phases are sequential: **1 → 2 → 3 → 4 → 5**

| Phase | Description | Details |
|---|---|---|
| 1 | Knowledge Base Parser — Date Extraction (TDD) | [phase-1-parser.md](phase-1-parser.md) |
| 2 | Add Date Fields to Context Markdown Files | [phase-2-context-files.md](phase-2-context-files.md) |
| 3 | HTML Cards — Date Display & data-date Attribute | [phase-3-html-cards.md](phase-3-html-cards.md) |
| 4 | JavaScript Date Sorting | [phase-4-js-sorting.md](phase-4-js-sorting.md) |
| 5 | E2E Tests & Knowledge Base Rebuild | [phase-5-e2e-tests.md](phase-5-e2e-tests.md) |

## Files Modified Summary

| File | Phase |
|---|---|
| `tests/test_build_knowledge_base.py` | 1, 5 |
| `scripts/build_knowledge_base.py` | 1 |
| `WebContent/context/*.md` (21 files) | 2 |
| `WebContent/css/style.css` | 3 |
| `index.html` | 3 |
| `projects.html` | 3 |
| `__tests__/filter.test.js` | 4 |
| `WebContent/js/filter.js` | 4 |
| `tests/test_gallery.py` | 5 |
| `lambda/knowledge_base.json` | 5 |

## Execution Strategy

Per subagent-driven development (CLAUDE.md), after Phase 2 completes, Phases 3 (HTML/CSS) and 4 (JS) can be dispatched as independent subagents since they touch different file types.
