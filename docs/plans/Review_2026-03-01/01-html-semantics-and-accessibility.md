# Phase 1: HTML Semantics & Accessibility

**Priority:** Do this FIRST (foundation for accessibility tests and screen readers)
**Complexity:** Small
**Review items addressed:** #1, #8, #9
**Files touched:** `index.html`, `404.html`, `tests/test_validation.py`

---

## Issues Addressed

| #   | Issue                                       | Severity |
| --- | ------------------------------------------- | -------- |
| 1   | Missing `<main>` and `<header>` landmarks   | High     |
| 8   | Inline `document.write()` in footer         | Medium   |
| 9   | `<meta charset>` not first in `<head>`      | Medium   |

---

## Step-by-Step Changes

### Step 1: Move `<meta charset>` before Google Analytics (Issue #9)

**File:** `index.html` lines 3–14

The HTML spec requires `<meta charset>` to appear within the first 1024 bytes of the document and before any content. Move it above the Google Analytics script tags.

**Before:**

```html
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-C3MKQC8F23"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag('js', new Date());
    gtag('config', 'G-C3MKQC8F23');
  </script>
  <meta charset="UTF-8" />
```

**After:**

```html
<head>
  <meta charset="UTF-8" />
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-C3MKQC8F23"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag('js', new Date());
    gtag('config', 'G-C3MKQC8F23');
  </script>
```

---

### Step 2: Wrap `<nav>` in `<header>` (Issue #1)

**File:** `index.html` lines 32–47

Wrap the existing `<nav id="main-nav">` element in a `<header>` element. This provides the ARIA `banner` landmark that screen readers expect.

**Before:**

```html
<body>
  <nav id="main-nav">
    ...
  </nav>
  <section id="profile">
```

**After:**

```html
<body>
  <header>
    <nav id="main-nav">
      ...
    </nav>
  </header>
  <main>
    <section id="profile">
```

---

### Step 3: Wrap all `<section>` elements in `<main>` (Issue #1)

**File:** `index.html`

Add `<main>` immediately after `</header>` and close it immediately before `<footer>`. This wraps `#profile`, `#skills`, `#projects`, `#testimonials`, and `#contact` in the main content landmark.

**Before:**

```html
  </section> <!-- end #contact -->
  <footer>
```

**After:**

```html
  </section> <!-- end #contact -->
  </main>
  <footer>
```

---

### Step 4: Replace inline `document.write()` with a `<span>` (Issue #8)

**File:** `index.html` lines 678–685

Remove the inline `<script>` tag and replace it with a `<span>` that JavaScript populates on load. This eliminates the last inline JS in the document.

**Before:**

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

**After:**

```html
<footer>
  <p>
    Copyright &#169; <span id="copyright-year"></span> Charles Coonce. All Rights Reserved.
  </p>
</footer>
```

Then add the following to the main JavaScript file (currently `WebContent/js/script.js`, will become `WebContent/js/main.js` in Phase 3) inside an existing `DOMContentLoaded` listener:

```js
const yearSpan = document.getElementById('copyright-year');
if (yearSpan) yearSpan.textContent = new Date().getFullYear();
```

---

### Step 5: Strengthen `test_semantic_structure` (Issue #1)

**File:** `tests/test_validation.py`

The current test only checks for `<nav>` and `<footer>`. Update it to also assert `<header>` and `<main>`, matching the SKILL.md example.

**Before:**

```python
def test_semantic_structure():
    assert soup.find('nav'), 'Missing <nav>'
    assert soup.find('footer'), 'Missing <footer>'
```

**After:**

```python
def test_semantic_structure():
    assert soup.find('header'), 'Missing <header>'
    assert soup.find('main'), 'Missing <main>'
    assert soup.find('nav'), 'Missing <nav>'
    assert soup.find('footer'), 'Missing <footer>'
```

---

### Step 6: Update 404 page favicon (Issue #13 — bonus, while editing HTML)

**File:** `404.html` line 7

Update the favicon to use the SVG icon, matching `index.html`.

**Before:**

```html
<link rel="icon" type="image/jpeg" href="./WebContent/assets/Headshots/LinkedinProfile.jpeg" />
```

**After:**

```html
<link rel="icon" type="image/svg+xml" href="./WebContent/assets/favicon.svg" />
```

---

## Verification

1. Open `index.html` in browser — confirm no visual changes
2. Inspect with browser accessibility tree — confirm `banner`, `main`, and `contentinfo` landmarks appear
3. Verify copyright year still renders in the footer
4. Run `uv run pytest tests/test_validation.py` — all tests pass including strengthened `test_semantic_structure`
5. Run `uv run pytest -m a11y` — accessibility tests pass
6. Run `npm run format:check` — Prettier passes
