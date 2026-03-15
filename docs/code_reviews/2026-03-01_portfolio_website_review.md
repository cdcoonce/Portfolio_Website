# Portfolio Website Code Review — 2026-03-01

## High Priority

### 1. Missing `<main>` landmark

`index.html` has no `<main>` element wrapping the page sections. Screen readers rely on `<main>` to skip directly to content (WCAG 2.4.1). Similarly, there's no `<header>` wrapper around the nav. The test in `tests/test_validation.py` was weakened to only assert `<nav>` and `<footer>`, masking this gap — SKILL.md's example tests check for both `<header>` and `<main>`.

### 2. All Jest unit tests are stubs

Every file in `__tests__/` contains only `test.todo(...)` — zero JS unit test coverage. The root cause: all logic in `WebContent/js/script.js` lives inside `DOMContentLoaded` closures with no exports, making it impossible for Jest to import and test pure functions. The SKILL.md pattern of separating pure logic from DOM manipulation hasn't been applied.

### 3. CI does not run tests

`.github/workflows/ci-cd.yml` only runs `npm run format:check` (Prettier). It does not run Jest, pytest, Stylelint, or ESLint. A broken test will not block a deploy to `gh-pages`.

### 4. Carousel breakpoint inconsistency

In `WebContent/js/script.js`, `getTestimonialsToShow()` uses `>=` for the 1200px breakpoint, but `createDots()` and the navigation functions use `>`. At exactly 1200px, the dot count won't match the testimonials-per-page count.

---

## Medium Priority

### 5. No CSS custom properties

`WebContent/css/style.css` hard-codes colors like `#353535` and `rgb(85,85,85)` throughout. SKILL.md requires a `:root` block with design tokens for colors, fonts, and spacing.

### 6. Desktop-first CSS (SKILL.md says mobile-first)

`WebContent/css/mediaqueries.css` uses `max-width` breakpoints (desktop-first). SKILL.md specifies mobile-first with `min-width` media queries.

### 7. `px` used extensively instead of `rem`/`em`

Both CSS files use pixel values for font sizes, padding, widths, etc. SKILL.md prefers relative units.

### 8. Inline `document.write()` in footer

`index.html` (~line 680) has `document.write(new Date().getFullYear())` inline in the footer, violating the "no inline JS" standard.

### 9. `<meta charset>` not first in `<head>`

The Google Analytics script tag appears before `<meta charset="UTF-8">`. The charset declaration should be the very first element in `<head>` per HTML spec.

### 10. Missing Jest configuration

`jest-environment-jsdom` is in `package.json` devDependencies but no Jest config points to it. Tests would run in the default Node environment, not jsdom.

### 11. CI missing lint steps

Stylelint and ESLint are configured but not run in CI — only Prettier format checking runs.

---

## Low Priority

### 12. Dead CSS rules

`WebContent/css/mediaqueries.css` references `.project__pic-container` and `.projects-filter .filter` — classes that no longer exist in the HTML.

### 13. 404 page favicon mismatch

`404.html` still uses `image/jpeg` favicon pointing to a headshot, while `index.html` uses the SVG favicon added in v1.2.0.

### 14. No-op CSS declarations

- `.rec { justify-self: left; }` — has no effect on flex children (only works in grid).
- `.author`, `.job`, `.company` set to `display: flex` unnecessarily — they're `<p>` elements with text only.

### 15. Inconsistent media query syntax

The 1250px breakpoint uses `@media screen and (max-width: 1250px)` while the 700px one uses `@media (max-width: 700px)` — the `screen` keyword is applied inconsistently.

### 16. `autoScroll` function is a trivial wrapper

It just calls `nextTestimonial()` with no additional logic — could be eliminated.

### 17. Multiple `DOMContentLoaded` listeners

`WebContent/js/script.js` has 4 separate `DOMContentLoaded` callbacks instead of a single entry point as recommended by SKILL.md.

### 18. SEO & link tests are stubs

`tests/test_seo.py` (Open Graph, meta description) and `tests/test_links.py` (external link checking) are skipped/stubbed.

---

## What's Working Well

- **Pytest suite is solid** — 13 validation tests, 4 a11y tests, 14 E2E tests across carousel, gallery, hero, and nav.
- **Accessibility effort** — `aria-expanded` on hamburger, `aria-label` on buttons, `aria-live` on carousel, `:focus-visible` styles, `.sr-only` class, contrast-checked counter color.
- **Clean JS** — JSDoc on functions, `const` by default, `'use strict'`, guard clauses for missing DOM elements.
- **Conventional Commits & CHANGELOG** — well-maintained version history following Keep a Changelog.
- **Makefile & npm scripts** — clean, match SKILL.md spec.
