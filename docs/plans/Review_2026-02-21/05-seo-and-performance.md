# Plan 5: SEO and Performance — COMPLETED

**Status:** Implemented 2026-02-21
**Priority:** Low — do last (cross-cutting but isolated line ranges)
**Complexity:** Small
**Files touched:** `index.html`, `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`

---

## Issues Addressed

| #   | Issue                                                      | Severity    |
| --- | ---------------------------------------------------------- | ----------- |
| 9   | Section `id="contacts"` should be `id="testimonials"`      | Medium      |
| 13  | Copyright year hardcoded to 2024                           | Medium      |
| 32  | Google Fonts loaded via `@import` in CSS (render-blocking) | Performance |

---

## Step-by-Step Changes

### Step 1: Move Google Fonts from CSS `@import` to HTML `<link>` (Issue #32)

Loading fonts via `@import` in CSS is render-blocking — the browser must download the CSS file, parse it, discover the `@import`, then make a second request for the font. Moving it to the HTML `<head>` with `preconnect` hints allows the browser to start fetching fonts earlier.

**File:** `style.css` line 3

**Remove:**

```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
```

**File:** `index.html` — insert in `<head>` section, before the stylesheet links

**Add (before the existing `<link rel="stylesheet">` tags):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
  rel="stylesheet"
/>
```

---

### Step 2: Rename `id="contacts"` to `id="testimonials"` (Issue #9)

The testimonials section is semantically named `id="contacts"` but contains no contact information. This rename improves code readability and maintainability.

**File:** `index.html` line 229

**Before:**

```html
<section id="contacts"></section>
```

**After:**

```html
<section id="testimonials"></section>
```

**File:** `style.css` line 281

**Before:**

```css
#contacts {
```

**After:**

```css
#testimonials {
```

**File:** `mediaqueries.css` — update both breakpoints

In the `@media (max-width: 1250px)` block (around line 69, the `/* === Contacts === */` comment):

- Update comment to `/* === Testimonials === */`
- No ID selector to change here (this block only targets classes)

In the `@media (max-width: 700px)` block (around line 110, the `/* === Contacts === */` comment):

- Update comment to `/* === Testimonials === */`
- No ID selector to change here either

> **Note:** Search the entire codebase for any other `#contacts` references (JS, other HTML pages). In the current codebase, only `style.css` and `index.html` reference this ID.

---

### Step 3: Make copyright year dynamic (Issue #13)

**File:** `index.html` line 286

**Before:**

```html
<footer>
  <p>Copyright &#169; 2024 Charles Coonce. All Rights Reserved.</p>
</footer>
```

**After:**

```html
<footer>
  <p>
    Copyright &#169;
    <script>
      document.write(new Date().getFullYear());
    </script>
    Charles Coonce. All Rights Reserved.
  </p>
</footer>
```

This is the simplest approach for a static site. The inline `document.write` runs synchronously during page parse and inserts the current year. Alternatively, you could use a `<span id="year">` and set it from `script.js`, but for a single value the inline approach is simpler.

---

## Verification

1. Open `index.html` in browser
2. **Font loading:** Open DevTools > Network tab, filter by "Font" — confirm Poppins loads. Check the waterfall: the font request should start earlier than before (not blocked behind CSS download)
3. **Section ID:** Inspect the testimonials section in Elements tab — confirm `id="testimonials"` (not `id="contacts"`)
4. **CSS still applies:** Testimonials section should look the same visually (background, margins, padding)
5. **Copyright year:** Footer should display "Copyright (c) 2026" (current year)
6. **No regressions:** Scroll through entire page, test carousel, test filters
7. Run Lighthouse > Performance — font loading should no longer be flagged as render-blocking
