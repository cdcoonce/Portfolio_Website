# Phase 1: Filter Logic Extensions

**Files:** `WebContent/js/filter.js`, `WebContent/js/main.js`

## Overview

Extend the filter module with three new pure functions and refactor `initFilter` to accept a configuration object. The existing API contract (calling `initFilter()` with no arguments) must produce identical behavior to today.

## New Pure Functions

### 1.1 `applyMaxVisible(visibility, max)`

Caps the number of visible cards to `max`. Returns a new `boolean[]` with at most `max` true values (preserving order — first N visible cards win).

```javascript
/**
 * Caps visible cards to a maximum count.
 * @param {boolean[]} visibility - Array of visibility flags
 * @param {number|null} max - Maximum visible cards, or null for unlimited
 * @returns {boolean[]} New array with at most max true values
 */
export const applyMaxVisible = (visibility, max) => {
  if (max == null) return visibility;
  let count = 0;
  return visibility.map((v) => {
    if (v && count < max) {
      count++;
      return true;
    }
    return false;
  });
};
```

**Behavior:**

- `max === null` → returns input unchanged (unlimited mode, used on `projects.html`)
- `max === 4` → returns at most 4 `true` values, preserving original order
- `max === 0` → all cards hidden

### 1.2 `getFeaturedVisibility(featuredFlags)`

Returns visibility array based on whether each card has the `featured` class.

```javascript
/**
 * Returns visibility based on featured status.
 * @param {boolean[]} featuredFlags - Array of booleans (true if card has featured class)
 * @returns {boolean[]}
 */
export const getFeaturedVisibility = (featuredFlags) => {
  return featuredFlags.map((f) => f);
};
```

### 1.3 `getFilterFromURL()`

Reads the `filter` query parameter from the current URL.

```javascript
/**
 * Reads the filter query parameter from the current URL.
 * @returns {string|null} The filter value, or null if not present
 */
export const getFilterFromURL = () => {
  const params = new URLSearchParams(window.location.search);
  return params.get('filter') || null;
};
```

**Security note:** The returned value is only compared via `===` against existing `data-filter` attributes. It is never injected into the DOM as HTML, so no XSS risk.

## Refactor `initFilter(config)`

### Config Schema

```javascript
/**
 * @param {Object} [config]
 * @param {number|null} [config.maxVisible=null] - Max cards to show (null = unlimited)
 * @param {string} [config.defaultFilter='all'] - Default filter: 'all' or 'featured'
 * @param {string|null} [config.initialFilter=null] - Pre-selected filter from URL param
 */
```

### Changes to `render()`

```javascript
function render() {
  let visibility;
  if (activeFilters.size === 0 && defaultFilter === 'featured') {
    // Home page default: show only featured projects
    visibility = getFeaturedVisibility(featuredFlags);
  } else if (activeFilters.size === 0) {
    // All-projects page default: show everything
    visibility = cardTagSets.map(() => true);
  } else {
    // Filter active: use standard OR-logic filter
    visibility = getFilteredVisibility(cardTagSets, activeFilters);
  }
  // Apply max-visible cap (only affects home page; projects page passes null)
  visibility = applyMaxVisible(visibility, maxVisible);
  cards.forEach((card, i) => {
    card.style.display = visibility[i] ? 'flex' : 'none';
  });

  // Update "View All" link with current filter
  updateViewAllLink();
}
```

### New internal function: `updateViewAllLink()`

```javascript
function updateViewAllLink() {
  const viewAllLink = document.querySelector('.view-all-link');
  if (!viewAllLink) return;
  if (activeFilters.size === 1) {
    const filter = Array.from(activeFilters)[0];
    viewAllLink.href = `./projects.html?filter=${encodeURIComponent(filter)}`;
  } else {
    viewAllLink.href = './projects.html';
  }
}
```

Only passes a single filter to the URL (first active filter) for simplicity. When multiple filters are active, links to the unfiltered all-projects page.

### Rename `showAll` → `showDefault`

The reset button now clears filters and calls `render()`, which respects `defaultFilter` to either show all cards or just featured cards.

### Handle `initialFilter`

At the end of `initFilter`, after all event listeners are wired:

```javascript
if (initialFilter) {
  const matchingTag = Array.from(skillTags).find(
    (t) => t.getAttribute('data-filter') === initialFilter
  );
  if (matchingTag) {
    matchingTag.click(); // Programmatically trigger the click handler
  }
}
```

### Backward Compatibility

Calling `initFilter()` with no arguments produces:

- `maxVisible: null` → all cards visible (no cap)
- `defaultFilter: 'all'` → reset shows everything
- `initialFilter: null` → no pre-selected filter

This is identical to current behavior. Existing tests pass without modification.

## Update `main.js`

```javascript
import { initFilter, getFilterFromURL } from './filter.js';
import { initCarousel } from './carousel.js';

document.addEventListener('DOMContentLoaded', () => {
  // ... existing nav, back-to-top, scroll-down code (unchanged) ...

  // Page-aware initialization
  const page = document.body.dataset.page;

  if (page === 'projects') {
    initFilter({
      maxVisible: null,
      defaultFilter: 'all',
      initialFilter: getFilterFromURL(),
    });
    // No carousel on projects page
  } else {
    initFilter({
      maxVisible: 4,
      defaultFilter: 'featured',
    });
    initCarousel();
  }
});
```

## Implementation Order (TDD)

1. Write unit tests for `applyMaxVisible` → run Jest → fail
2. Implement `applyMaxVisible` → run Jest → pass
3. Write unit tests for `getFeaturedVisibility` → fail → implement → pass
4. Write unit tests for `getFilterFromURL` → fail → implement → pass
5. Refactor `initFilter` with config parameter → verify all existing tests pass
6. Update `main.js` → verify page loads correctly
