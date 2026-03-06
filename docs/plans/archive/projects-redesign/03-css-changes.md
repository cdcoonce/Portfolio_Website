# Phase 3: CSS Changes

**Files:** `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`

## Overview

CSS changes are minimal. The existing `.projects-grid` and `.project-card` styles already handle variable numbers of cards via `auto-fit`. The primary addition is styling for the "View All Projects" footer link.

## 3.1 New Rules in `style.css`

### Projects footer

Add after the existing `.project-card` rules (around line 455):

```css
/* === Projects Footer === */
.projects-footer {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}
```

The `.view-all-link` inherits from the existing `.btn.btn-color-1` class (already defined in the codebase), so no additional button styles are needed.

## 3.2 Media Query Changes

### `mediaqueries.css`

No changes required. The grid already handles responsive behavior:

- **Desktop (> 1250px):** Up to 4 cards per row — with only 4 visible, this fills one row perfectly
- **Tablet (700px–1250px):** 2 columns — 4 cards display as 2 rows of 2
- **Mobile (< 700px):** 1 column — 4 cards stack vertically

The all-projects page (`projects.html`) shows all 17 cards and uses the same responsive grid, working identically to the current main page layout.

## 3.3 No Changes to Existing Rules

The following existing styles work as-is for both pages:

- `.projects-grid` — `auto-fit` grid adapts to any card count
- `.project-card` — 300px fixed width, min-height 430px
- `.project-card.featured` — 3px top border
- `.card-content` — flex column layout
- `.skill-tag` / `.skill-filter-reset` — filter button styles
- `.skills-grid` — 4-column responsive grid
