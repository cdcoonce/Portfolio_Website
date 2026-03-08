# Phase 3: HTML Cards — Date Display & data-date Attribute

## Goal

Add a visible date and a sortable `data-date` attribute to all 17 project cards in both HTML files (34 card edits total).

## Files

- `WebContent/css/style.css` — add `.project-date` rule
- `index.html` — update 17 cards
- `projects.html` — update 17 cards

## CSS Addition

Add after the `.card-content p` rule (~line 466 in style.css):

```css
.project-date {
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.25rem;
}
```

## HTML Change Per Card

Before:

```html
<a href="..." class="project-card featured" data-tags="python,etl">
  <img ... />
  <div class="card-content">
    <h3>Project Title</h3>
    <p>Description.</p>
  </div>
</a>
```

After:

```html
<a href="..." class="project-card featured" data-tags="python,etl" data-date="2025-12">
  <img ... />
  <div class="card-content">
    <h3>Project Title</h3>
    <span class="project-date">Dec 2025</span>
    <p>Description.</p>
  </div>
</a>
```

## Card-to-Date Mapping

Only 17 of 21 context files have HTML cards. The 4 context-only projects (national-parks-analysis, energy-analytics-pipeline, renewable-asset-pipeline, synthetic-signal-observatory) receive dates in Phase 2 only for the knowledge base.

| Card Title | data-date | Display |
| --- | --- | --- |
| National Parks Dashboard | 2024-09 | Sep 2024 |
| Wine Quality Analysis | 2024-11 | Nov 2024 |
| Electricity Consumption | 2025-02 | Feb 2025 |
| Manufacturing Downtime Analysis | 2025-02 | Feb 2025 |
| Portfolio Website | 2024-08 | Aug 2024 |
| World Happiness Dashboard | 2024-09 | Sep 2024 |
| Data Archive | 2024-12 | Dec 2024 |
| NYC Collision Analysis | 2025-02 | Feb 2025 |
| Global CO2 Emissions | 2025-02 | Feb 2025 |
| AirBnB Listing Analysis | 2025-02 | Feb 2025 |
| Sleep Deprivation Analysis | 2025-02 | Feb 2025 |
| Restaurant Order Analysis | 2025-03 | Mar 2025 |
| Motor Vehicle Thefts | 2025-03 | Mar 2025 |
| Baby Names Analysis | 2025-03 | Mar 2025 |
| Spaceship Titanic Classification | 2025-05 | May 2025 |
| Ames Housing Price Prediction | 2025-10 | Oct 2025 |
| Housing Affordability & Commute Tradeoffs | 2025-12 | Dec 2025 |

## Verify

- Visual inspection in browser
- Existing E2E tests still pass: `uv run pytest tests/test_gallery.py`
