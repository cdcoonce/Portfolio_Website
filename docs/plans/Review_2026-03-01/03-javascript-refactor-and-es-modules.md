# Phase 3: JavaScript Refactor & ES Modules

**Priority:** Third — must come before Phase 4 (testing depends on importable modules)
**Complexity:** Large
**Review items addressed:** #2, #4, #16, #17
**Files touched:** `WebContent/js/script.js` (deleted), `WebContent/js/main.js` (new), `WebContent/js/filter.js` (new), `WebContent/js/carousel.js` (new), `WebContent/js/utils.js` (new), `index.html`, `package.json`

---

## Issues Addressed

| #   | Issue                                             | Severity |
| --- | ------------------------------------------------- | -------- |
| 2   | Pure logic not separated from DOM — untestable    | High     |
| 4   | Carousel breakpoint `>=` vs `>` inconsistency     | High     |
| 16  | `autoScroll` is a trivial wrapper                 | Low      |
| 17  | Multiple `DOMContentLoaded` listeners             | Low      |

---

## Architecture

Split `script.js` into four ES modules per SKILL.md:

```
WebContent/js/
├── main.js       # Entry point — imports modules, single DOMContentLoaded
├── filter.js     # Pure filter logic (exported) + DOM wiring (exported init)
├── carousel.js   # Pure carousel logic (exported) + DOM wiring (exported init)
└── utils.js      # Shared utilities (exported)
```

Each module exports:
- **Pure functions** — no DOM access, fully testable by Jest
- **An `init()` function** — wires pure logic to the DOM, called by `main.js`

The browser loads only `main.js` via `<script type="module">`. Jest imports the pure functions directly.

---

## Step-by-Step Changes

### Step 1: Create `WebContent/js/utils.js`

Shared utility functions used by multiple modules.

```js
'use strict';

/**
 * Determines how many items to show based on viewport width and a breakpoint.
 * @param {number} viewportWidth - Current viewport width in pixels
 * @param {number} breakpoint - Width threshold for desktop layout
 * @param {number} desktopCount - Items to show on desktop
 * @param {number} mobileCount - Items to show on mobile
 * @returns {number}
 */
export const getItemsToShow = (viewportWidth, breakpoint, desktopCount, mobileCount) =>
  viewportWidth >= breakpoint ? desktopCount : mobileCount;

/**
 * Checks whether a viewport width qualifies as desktop.
 * @param {number} viewportWidth
 * @param {number} breakpoint
 * @returns {boolean}
 */
export const isDesktop = (viewportWidth, breakpoint) => viewportWidth >= breakpoint;
```

**Note:** Both functions use `>=` consistently, fixing Issue #4 at the source.

---

### Step 2: Create `WebContent/js/filter.js`

Extract filtering logic from the current `script.js` lines 80–143.

```js
'use strict';

/**
 * Determines which project cards should be visible given the active filter set.
 * @param {string[]} cardTagSets - Array of comma-separated tag strings (one per card)
 * @param {Set<string>} activeFilters - Currently active filter values
 * @returns {boolean[]} - Array of visibility flags, one per card
 */
export const getFilteredVisibility = (cardTagSets, activeFilters) => {
  if (activeFilters.size === 0) {
    return cardTagSets.map(() => true);
  }
  return cardTagSets.map((tags) => {
    const tagSet = new Set(
      tags
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean)
    );
    return Array.from(activeFilters).some((f) => tagSet.has(f));
  });
};

/**
 * Wires filter buttons and reset button to project card visibility.
 */
export function initFilter() {
  const skillTags = document.querySelectorAll('button.skill-tag[data-filter]');
  const resetButton = document.querySelector('button.skill-filter-reset');
  const cards = document.querySelectorAll('.project-card');
  const activeFilters = new Set();

  if (!skillTags.length || !cards.length) {
    console.warn('Skill filter buttons or project cards not found in DOM');
    return;
  }

  const cardTagSets = Array.from(cards).map((c) => c.getAttribute('data-tags') || '');

  function render() {
    const visibility = getFilteredVisibility(cardTagSets, activeFilters);
    cards.forEach((card, i) => {
      card.style.display = visibility[i] ? 'flex' : 'none';
    });
  }

  function showAll() {
    activeFilters.clear();
    skillTags.forEach((t) => t.classList.remove('active'));
    if (resetButton) resetButton.classList.add('active');
    render();
  }

  skillTags.forEach((tag) => {
    tag.addEventListener('click', () => {
      const filterValue = tag.getAttribute('data-filter');
      if (resetButton) resetButton.classList.remove('active');

      if (tag.classList.contains('active')) {
        tag.classList.remove('active');
        activeFilters.delete(filterValue);
      } else {
        tag.classList.add('active');
        activeFilters.add(filterValue);
      }

      if (activeFilters.size === 0) {
        showAll();
      } else {
        render();
      }
    });
  });

  if (resetButton) {
    resetButton.addEventListener('click', showAll);
  }
}
```

---

### Step 3: Create `WebContent/js/carousel.js`

Extract carousel logic from `script.js` lines 148–309. Separate pure index-calculation functions from DOM manipulation.

```js
'use strict';

import { getItemsToShow, isDesktop } from './utils.js';

/** Configuration constants for testimonial carousel behavior */
export const CAROUSEL_CONFIG = {
  DESKTOP_BREAKPOINT: 1200,
  AUTO_SCROLL_INTERVAL_MS: 20000,
  TESTIMONIALS_DESKTOP: 2,
  TESTIMONIALS_MOBILE: 1,
};

/**
 * Calculates the next carousel index with wraparound.
 * @param {number} currentIndex - Current starting index
 * @param {number} step - Number of items to advance
 * @param {number} totalItems - Total testimonial count
 * @param {number} itemsToShow - Items visible at once
 * @returns {number} New index
 */
export const getNextIndex = (currentIndex, step, totalItems, itemsToShow) => {
  if (currentIndex + itemsToShow < totalItems) {
    return currentIndex + step;
  }
  return 0;
};

/**
 * Calculates the previous carousel index with wraparound.
 * @param {number} currentIndex - Current starting index
 * @param {number} step - Number of items to go back
 * @param {number} totalItems - Total testimonial count
 * @param {number} itemsToShow - Items visible at once
 * @returns {number} New index
 */
export const getPrevIndex = (currentIndex, step, totalItems, itemsToShow) => {
  if (currentIndex > 0) {
    return currentIndex - step;
  }
  return Math.max(0, totalItems - itemsToShow);
};

/**
 * Calculates the number of pagination dots needed.
 * @param {number} totalItems - Total testimonial count
 * @param {boolean} desktop - Whether in desktop mode
 * @returns {number} Number of dots
 */
export const getDotCount = (totalItems, desktop) => {
  return desktop ? Math.ceil(totalItems / 2) : totalItems;
};

/**
 * Determines which dot index should be active.
 * @param {number} carouselIndex - Current carousel position
 * @param {boolean} desktop - Whether in desktop mode
 * @returns {number} Active dot index
 */
export const getActiveDotIndex = (carouselIndex, desktop) => {
  return desktop ? Math.floor(carouselIndex / 2) : carouselIndex;
};

/**
 * Returns the counter display string (e.g. "1 / 4").
 * @param {number} startIndex - Current starting index
 * @param {number} itemsToShow - Items visible at once
 * @param {number} totalItems - Total testimonial count
 * @returns {string}
 */
export const getCounterText = (startIndex, itemsToShow, totalItems) => {
  const current = Math.floor(startIndex / itemsToShow) + 1;
  const total = Math.ceil(totalItems / itemsToShow);
  return `${current} / ${total}`;
};

/**
 * Initializes the testimonial carousel with navigation, dots, and auto-scroll.
 */
export function initCarousel() {
  const testimonials = document.querySelectorAll('.testimonial');
  const prevButton = document.getElementById('prevRec');
  const nextButton = document.getElementById('nextRec');
  const dotsContainer = document.querySelector('.dots-container');

  if (!testimonials.length || !prevButton || !nextButton || !dotsContainer) {
    console.warn('Testimonial carousel elements not found in DOM');
    return;
  }

  const totalItems = testimonials.length;
  let carouselIndex = 0;

  function currentItemsToShow() {
    return getItemsToShow(
      window.innerWidth,
      CAROUSEL_CONFIG.DESKTOP_BREAKPOINT,
      CAROUSEL_CONFIG.TESTIMONIALS_DESKTOP,
      CAROUSEL_CONFIG.TESTIMONIALS_MOBILE
    );
  }

  function currentIsDesktop() {
    return isDesktop(window.innerWidth, CAROUSEL_CONFIG.DESKTOP_BREAKPOINT);
  }

  function showTestimonials(startIndex) {
    const itemsToShow = currentItemsToShow();
    testimonials.forEach((testimonial, i) => {
      const isVisible = i >= startIndex && i < startIndex + itemsToShow;
      testimonial.classList.toggle('active', isVisible);
      testimonial.style.opacity = isVisible ? '1' : '0';
    });
    updateDots();
    updateCounter(startIndex);
  }

  function createDots() {
    dotsContainer.innerHTML = '';
    const desktop = currentIsDesktop();
    const count = getDotCount(totalItems, desktop);

    for (let i = 0; i < count; i++) {
      const dot = document.createElement('div');
      dot.classList.add('dot');
      if (i === 0) dot.classList.add('active');
      const targetIndex = desktop ? i * 2 : i;
      dot.addEventListener('click', () => {
        carouselIndex = targetIndex;
        showTestimonials(carouselIndex);
      });
      dotsContainer.appendChild(dot);
    }
  }

  function updateDots() {
    const dots = document.querySelectorAll('.dot');
    const activeIndex = getActiveDotIndex(carouselIndex, currentIsDesktop());
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === activeIndex);
    });
  }

  function updateCounter(startIndex) {
    const counter = document.querySelector('.testimonial-counter');
    if (counter) {
      counter.textContent = getCounterText(startIndex, currentItemsToShow(), totalItems);
    }
  }

  function nextTestimonial() {
    const step = currentItemsToShow();
    carouselIndex = getNextIndex(carouselIndex, step, totalItems, currentItemsToShow());
    showTestimonials(carouselIndex);
  }

  function prevTestimonial() {
    const step = currentItemsToShow();
    carouselIndex = getPrevIndex(carouselIndex, step, totalItems, currentItemsToShow());
    showTestimonials(carouselIndex);
  }

  // Navigation buttons
  nextButton.addEventListener('click', nextTestimonial);
  prevButton.addEventListener('click', prevTestimonial);

  // Auto-scroll (Issue #16 — removed trivial autoScroll wrapper)
  let autoScrollTimer = setInterval(nextTestimonial, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      clearInterval(autoScrollTimer);
    } else {
      autoScrollTimer = setInterval(nextTestimonial, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);
    }
  });

  // Responsive resize
  window.addEventListener('resize', () => {
    showTestimonials(carouselIndex);
    createDots();
  });

  // Create counter element
  const counter = document.createElement('p');
  counter.classList.add('testimonial-counter');
  dotsContainer.insertAdjacentElement('afterend', counter);

  // Initial render
  createDots();
  showTestimonials(carouselIndex);
}
```

**Key fixes:**
- Issue #4: All breakpoint checks now use `isDesktop()` from `utils.js` which consistently uses `>=`
- Issue #16: `autoScroll` wrapper removed — `nextTestimonial` passed directly to `setInterval`

---

### Step 4: Create `WebContent/js/main.js`

Single entry point — one `DOMContentLoaded` listener (fixes Issue #17).

```js
'use strict';

import { initFilter } from './filter.js';
import { initCarousel } from './carousel.js';

/**
 * Application entry point.
 * Initializes all interactive components after DOM is ready.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Copyright year (moved from inline script — Phase 1 Step 4)
  const yearSpan = document.getElementById('copyright-year');
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  // Navigation — hamburger toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Back to top button
  const backToTop = document.querySelector('.back-to-top');
  const testimonials = document.querySelector('#testimonials');

  if (backToTop) {
    window.addEventListener('scroll', () => {
      const testimonialsTop = testimonials ? testimonials.getBoundingClientRect().top : Infinity;
      backToTop.classList.toggle('visible', testimonialsTop <= window.innerHeight);
    });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Scroll-down button
  const scrollDown = document.querySelector('.scroll-down');
  const profileSection = document.querySelector('#profile');

  if (scrollDown && profileSection) {
    window.addEventListener('scroll', () => {
      const profileBottom = profileSection.getBoundingClientRect().bottom;
      scrollDown.classList.toggle('hidden', profileBottom < 0);
    });

    scrollDown.addEventListener('click', () => {
      const skills = document.querySelector('#skills');
      const nav = document.querySelector('#main-nav');
      const navHeight = nav ? nav.offsetHeight : 0;
      window.scrollTo({ top: skills.offsetTop - navHeight, behavior: 'smooth' });
    });
  }

  // Initialize feature modules
  initFilter();
  initCarousel();
});
```

---

### Step 5: Update `index.html` script tag

**File:** `index.html` line 688

**Before:**

```html
<script src="./WebContent/js/script.js"></script>
```

**After:**

```html
<script type="module" src="./WebContent/js/main.js"></script>
```

---

### Step 6: Update `package.json` module type

**File:** `package.json` line 24

Change `"type": "commonjs"` to `"type": "module"` so Node/Jest treat `.js` files as ESM by default.

**Before:**

```json
"type": "commonjs",
```

**After:**

```json
"type": "module",
```

**Note:** This also requires updating `eslint.config.mjs` to `eslint.config.js` (since `.js` is now ESM) or keeping it as `.mjs`. Keeping it as `.mjs` is the simplest path — no change needed.

---

### Step 7: Delete `WebContent/js/script.js`

All logic has been migrated. Delete the old file.

```bash
git rm WebContent/js/script.js
```

---

## Verification

1. Open `index.html` in browser — confirm all features work:
   - Hamburger nav opens/closes on mobile
   - Back-to-top button appears at testimonials
   - Scroll-down button hides on scroll
   - Skill tag filtering works (multi-select + reset)
   - Carousel navigation (prev/next/dots/auto-scroll)
   - Copyright year renders in footer
2. Test at exactly 1200px viewport width — confirm carousel shows 2 testimonials and dots match (Issue #4 fixed)
3. Run `npm run lint:js` — ESLint passes
4. Run `npm run format:check` — Prettier passes
5. Run `uv run pytest -m e2e` — all E2E tests pass
6. Run `uv run pytest -m a11y` — accessibility tests pass
