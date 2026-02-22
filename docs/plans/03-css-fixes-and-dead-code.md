# Plan 3: CSS Fixes and Dead Code Removal

**Priority:** High — do after Plan 1 (can be parallel with Plan 2)
**Complexity:** Medium
**Files touched:** `WebContent/css/style.css`, `WebContent/css/mediaqueries.css` (post-rename from Plan 1)

---

## Issues Addressed

| #   | Issue                                                            | Severity |
| --- | ---------------------------------------------------------------- | -------- |
| 7   | `padding-top: 2vh` overridden by `padding` shorthand             | High     |
| 8   | Redundant `box-sizing: border-box` on `section` (already global) | High     |
| 16  | Font family switches to Arial in testimonials container          | Medium   |
| 21  | Unused `@keyframes fadeIn` animation                             | Low      |
| 22  | Unused `.p` CSS class                                            | Low      |
| 23  | Redundant CSS in media queries                                   | Low      |
| 27  | `transition: all 300ms ease` is overly broad                     | Low      |
| 28  | `justify-content: right` is non-standard                         | Low      |

---

## Step-by-Step Changes

### Step 1: Fix `padding` override on `section` (Issue #7)

**File:** `style.css` lines 99-107

**Before:**

```css
section {
  padding-top: 2vh;
  padding: 0 2rem;
  box-sizing: border-box;
  min-height: fit-content;
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
}
```

**After:**

```css
section {
  padding: 2vh 2rem 0;
  min-height: fit-content;
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
}
```

This combines the `padding-top` with the shorthand so it's no longer silently overridden, and removes the redundant `box-sizing` (Issue #8) since `* { box-sizing: border-box; }` already covers all elements.

---

### Step 2: Narrow `transition: all` to specific properties (Issue #27)

**File:** `style.css` lines 25-29

**Before:**

```css
a,
img,
.btn {
  transition: all 300ms ease;
}
```

**After:**

```css
a,
img,
.btn {
  transition:
    color 300ms ease,
    background-color 300ms ease,
    transform 300ms ease,
    box-shadow 300ms ease,
    opacity 300ms ease;
}
```

This prevents unintended animations on layout properties (width, height, padding, etc.) while covering the properties actually animated in this site.

---

### Step 3: Remove `font-family` override from testimonials (Issue #16)

**File:** `style.css` line 299

**Before:**

```css
.testimonials-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
  width: 90%;
  max-width: 1200px;
  margin: auto;
  font-family: Arial, sans-serif;
  overflow: hidden;
  justify-content: space-evenly;
}
```

**After:**

```css
.testimonials-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
  width: 90%;
  max-width: 1200px;
  margin: auto;
  overflow: hidden;
  justify-content: space-evenly;
}
```

**File:** `mediaqueries.css` lines 71-80 (1250px breakpoint)

Remove `font-family: Arial, sans-serif;` from the `.testimonials-container` rule.

**File:** `mediaqueries.css` lines 111-121 (700px breakpoint)

Remove `font-family: Arial, sans-serif;` from the `.testimonials-container` rule.

---

### Step 4: Delete unused `.p` class (Issue #22)

**File:** `style.css` lines 324-326

**Remove entirely:**

```css
.p {
  display: flex;
}
```

This class is never referenced in the HTML.

---

### Step 5: Fix `justify-content: right` to `flex-end` (Issue #28)

**File:** `style.css` — three rules

**Line 339 (`.author`):**

```css
/* Before */
justify-content: right;
/* After */
justify-content: flex-end;
```

**Line 348 (`.job`):**

```css
/* Before */
justify-content: right;
/* After */
justify-content: flex-end;
```

**Line 357 (`.company`):**

```css
/* Before */
justify-content: right;
/* After */
justify-content: flex-end;
```

---

### Step 6: Remove unused `@keyframes fadeIn` (Issue #21)

**File:** `style.css` lines 389-396

**Remove entirely:**

```css
@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
```

This animation is defined but never referenced by any CSS rule or JavaScript.

---

### Step 7: Clean up redundant media query properties (Issue #23)

**File:** `mediaqueries.css`

In the `@media (max-width: 1250px)` block, the `.testimonial` rule (lines 92-101) redeclares nearly every property from the base rule in `style.css`. Only properties that **differ** from the base should be present.

**Before (1250px `.testimonial`):**

```css
.testimonial {
  display: none;
  max-width: 100%;
  padding: 20px;
  text-align: left;
  background-color: #ebf1f866;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 10px;
}
```

Compare to base `style.css` `.testimonial`:

```css
.testimonial {
  display: none;
  max-width: 100%;
  padding: 20px;
  text-align: left;
  background-color: rgba(235, 241, 248, 0.4);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 10px;
}
```

The only difference is `background-color`. Reduce to:

**After:**

```css
.testimonial {
  background-color: #ebf1f866;
}
```

Similarly, review the `.testimonials-container` and `.testimonials` rules at both breakpoints and remove any properties that are identical to the base styles. Keep only the overrides.

---

## Verification

1. Open `index.html` in browser — confirm no visual regressions
2. Inspect testimonials section — text should now render in Poppins font (not Arial)
3. Resize browser through breakpoints (>1250px, 700-1250px, <700px) — layout should remain responsive
4. Hover over buttons and project cards — transitions should animate smoothly on color/transform/shadow only
5. Check DevTools > Elements for any CSS warnings
6. Right-click testimonial author names — text should right-align correctly via `flex-end`
