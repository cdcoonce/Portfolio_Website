# Plan 4: JavaScript Behavior Fixes

**Priority:** Medium — do after Plans 2 and 3
**Complexity:** Medium
**Files touched:** `WebContent/js/script.js`, `index.html` (2 lines only)

---

## Issues Addressed

| #   | Issue                                                                                | Severity |
| --- | ------------------------------------------------------------------------------------ | -------- |
| 2   | Inline `onclick` handlers call closure-scoped functions (dead code + console errors) | Critical |
| 18  | Filter uses `String.includes()` which can false-match substrings                     | Medium   |
| 17  | Auto-scroll `setInterval` never pauses when tab is backgrounded                      | Medium   |

---

## Step-by-Step Changes

### Step 1: Remove inline `onclick` from testimonial buttons (Issue #2)

**File:** `index.html`

The `prevTestimonial()` and `nextTestimonial()` functions are defined inside a `DOMContentLoaded` closure in `script.js`, so the inline `onclick` attributes can't resolve them (they look for global scope). The `addEventListener` calls on `script.js:184-185` already handle click events correctly. The inline handlers are dead code that produce `ReferenceError` in the console.

**Line 233 — Previous button:**

**Before:**

```html
<button id="prevRec" class="btn btn-color-2" onclick="prevTestimonial()">&#10094</button>
```

**After:**

```html
<button id="prevRec" class="btn btn-color-2">&#10094;</button>
```

**Line 280 — Next button:**

**Before:**

```html
<button id="nextRec" class="btn btn-color-2" onclick="nextTestimonial()">&#10095</button>
```

**After:**

```html
<button id="nextRec" class="btn btn-color-2">&#10095;</button>
```

> **Note:** Also added the missing semicolons to the HTML entities (`&#10094;` and `&#10095;`). They work without them, but it's proper HTML.

No changes needed in `script.js` — the `addEventListener` calls on lines 184-185 already work correctly.

---

### Step 2: Fix filter substring matching (Issue #18)

**File:** `script.js` line 48-51

The current code uses `tags.includes(filter)` which does string substring matching on the comma-separated `data-tags` value. This can produce false positives — for example, filtering by `"r"` would match `"r,shiny"` correctly, but could also match a hypothetical tag like `"r-studio"` or `"orchestration"`.

**Before:**

```js
cards.forEach((card) => {
  const tags = card.getAttribute('data-tags') || '';
  const matches = Array.from(activeFilters).some((filter) => tags.includes(filter));
  card.style.display = matches ? 'block' : 'none';
});
```

**After:**

```js
cards.forEach((card) => {
  const tags = card.getAttribute('data-tags') || '';
  const tagSet = new Set(
    tags
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean)
  );
  const matches = Array.from(activeFilters).some((f) => tagSet.has(f));
  card.style.display = matches ? 'block' : 'none';
});
```

Changes:

- Split the comma-separated string into an array
- Trim whitespace from each tag (defensive)
- Filter out empty strings (handles `data-tags=""` case)
- Use `Set.has()` for exact matching instead of substring matching

---

### Step 3: Improve auto-scroll with visibility awareness (Issue #17)

**File:** `script.js` lines 187-195

The current `setInterval` runs continuously, even when the browser tab is inactive. This causes unnecessary CPU usage and can make the carousel jump unexpectedly when the user returns to the tab.

**Before:**

```js
// Auto-scroll carousel at configured interval
setInterval(() => {
  if (carouselIndex + testimonialsToShow < testimonials.length) {
    nextTestimonial();
  } else {
    carouselIndex = 0;
    showTestimonials(carouselIndex);
  }
}, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);
```

**After:**

```js
// Auto-scroll carousel, pausing when tab is not visible
let autoScrollTimer = setInterval(autoScroll, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);

function autoScroll() {
  if (carouselIndex + testimonialsToShow < testimonials.length) {
    nextTestimonial();
  } else {
    carouselIndex = 0;
    showTestimonials(carouselIndex);
  }
}

document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    clearInterval(autoScrollTimer);
  } else {
    autoScrollTimer = setInterval(autoScroll, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);
  }
});
```

Changes:

- Extract the auto-scroll logic into a named `autoScroll` function
- Store the interval ID in `autoScrollTimer`
- Add a `visibilitychange` listener that clears the interval when the tab is hidden and restarts it when visible again

---

## Verification

1. Open `index.html` in browser
2. Open DevTools Console — confirm **no** `ReferenceError` for `prevTestimonial` or `nextTestimonial`
3. Click the carousel prev/next buttons — testimonials should navigate correctly
4. Wait 20 seconds — carousel should auto-advance
5. Switch to another tab, wait 60+ seconds, switch back — carousel should be at the same position (not jumped ahead)
6. Test project filters:
   - Click "R" filter — should show only R-tagged projects (National Parks Dashboard, National Parks Analysis, World Happiness Dashboard)
   - Click "All" — all 17 projects should show
   - Click "Python" then "SQL" — should show projects tagged with either
   - Deselect all filters — should revert to showing all
7. Verify no console errors throughout all interactions
