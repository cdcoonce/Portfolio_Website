# Phase 5: Accessibility & Polish

**Suggestions addressed:** #13 (Keyboard/Focus Accessibility)
**Impact:** Low-Medium — improves usability for keyboard and assistive technology users

---

## Overview

This final phase addresses accessibility gaps and applies finishing touches. These changes are small in scope but important for inclusive design and overall professionalism.

---

## Tasks

### 5.1 Add `:focus-visible` styles

**File:** `WebContent/css/style.css`

Currently, there are no visible focus indicators for interactive elements. Keyboard users cannot tell which element is focused.

**Add global focus styles:**
```css
a:focus-visible,
button:focus-visible,
.filter:focus-visible {
  outline: 2px solid #353535;
  outline-offset: 2px;
}
```

This uses `:focus-visible` (not `:focus`) so the outline only appears during keyboard navigation, not on mouse clicks.

### 5.2 Make filter tags keyboard-accessible

**Files:** `index.html`, `WebContent/js/script.js`

The filter `<span>` elements are not keyboard-focusable by default. Add `tabindex="0"` and `role="button"` to each filter span, and handle `keydown` events for Enter/Space activation.

**HTML change (each filter span):**
```html
<span class="filter active" data-filter="all" tabindex="0" role="button">All</span>
```

**JS addition in the filter logic:**
```javascript
filter.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    filter.click();
  }
});
```

### 5.3 Add ARIA labels to carousel controls

**File:** `index.html`

The prev/next buttons use HTML entities (`&#10094;`, `&#10095;`) which aren't descriptive for screen readers.

**Current:**
```html
<button id="prevRec" class="btn btn-color-2">&#10094;</button>
<button id="nextRec" class="btn btn-color-2">&#10095;</button>
```

**Proposed:**
```html
<button id="prevRec" class="btn btn-color-2" aria-label="Previous testimonial">&#10094;</button>
<button id="nextRec" class="btn btn-color-2" aria-label="Next testimonial">&#10095;</button>
```

Also add `aria-live="polite"` to the testimonials container so screen readers announce when content changes:

```html
<div class="testimonials" aria-live="polite">
```

### 5.4 Verify color contrast ratios

**File:** `WebContent/css/style.css`

Review these color combinations against WCAG AA standards (minimum 4.5:1 for normal text):

| Element | Foreground | Background | Ratio | Status |
|---------|-----------|------------|-------|--------|
| Body text (`p`) | `rgb(85,85,85)` | `#fff` | ~5.9:1 | Pass |
| Inactive dots | `#b0b4b9` | `#fff` | ~2.8:1 | Fail (decorative, acceptable) |
| Filter tags (inactive) | inherit | `#fff` | Check | Verify |
| `.btn-color-2` text | `#353535` border on white | `#fff` | ~10:1 | Pass |

If any interactive element fails contrast, adjust colors accordingly.

### 5.5 Add `alt` text audit

**File:** `index.html`

All images currently have `alt` attributes (good). Audit them for descriptiveness:

- Project images: Ensure alt text describes what the image shows, not just the project name
- Icon images: `mailicon.png` and `linkedinicon.png` have alt text — verify it's meaningful
- Decorative images: If any images are purely decorative, use `alt=""`

### 5.6 Ensure semantic HTML

**File:** `index.html`

Minor semantic improvements:
- The testimonials `<p class="section_text__p1">Testimonials</p>` should be an `<h2>` for proper heading hierarchy
- The projects section is missing a heading — add a visually hidden `<h2>` or a visible one for screen readers

```html
<!-- Testimonials heading -->
<h2 class="section_text__p1">Testimonials</h2>

<!-- Projects section (add heading) -->
<section id="projects">
  <h2 class="sr-only">Projects</h2>
  ...
</section>
```

If using a visually hidden heading:
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

---

## Testing Checklist

- [ ] Tab key navigates through all interactive elements in logical order
- [ ] Focus indicator is visible on all focusable elements during keyboard navigation
- [ ] Focus indicator does not appear on mouse click
- [ ] Filter tags can be activated with Enter and Space keys
- [ ] Screen reader announces testimonial changes (test with VoiceOver on macOS)
- [ ] All images have meaningful alt text
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skipped levels)
- [ ] Color contrast passes WCAG AA for all text content

---

## Dependencies

- All previous phases should be completed first
- Testing requires keyboard-only navigation and ideally a screen reader (VoiceOver: Cmd+F5 on macOS)
