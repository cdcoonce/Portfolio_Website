# UI/UX Improvement Suggestions

**Date:** 2026-02-21
**Scope:** User experience and visual design improvements for charleslikesdata.com

---

## High Priority

### 1. Add a Sticky Navigation Bar

There is no persistent navigation. Once users scroll past the hero, there's no way to jump between sections or get back to the top without scrolling. Add a `<nav>` with anchor links (`#profile`, `#projects`, `#testimonials`) and make it `position: sticky; top: 0`. This is especially important with 17 project cards creating a long page.

### 2. Add Project Descriptions to Cards

Every card currently shows only a title and a "Learn More" button. A 1-2 sentence description would give context before requiring a click to an external GitHub page. This is critical for converting visitors — especially recruiters who are skimming.

### 3. Create a Dedicated Skills/About Section

Right now, skills only appear as filter tags in the Projects section. A visitor who doesn't scroll that far gets no tech stack overview. A small "About Me" or "Skills" section between the hero and projects would improve scanability significantly.

### 4. Add a Contact Section

The only contact options are icons in the hero section — once users scroll down, they're gone. Add a brief contact section in the footer area with email/LinkedIn/GitHub links so the CTA is always available at the end of the page.

---

## Medium Priority

### 5. Fix the Hero Section Spacing

**File:** `WebContent/css/style.css:156`

`.section_text__p1` has `padding-left: 10rem` on desktop, which is an awkward indent for a short line like "Hello, I'm". This only works because the text is visually offset relative to the heading, but it's a fragile layout. Use alignment or flexbox instead.

### 6. Standardize Project Card Images

**File:** `WebContent/css/style.css:234`

`object-fit: contain` with a `#f0f0f0` background means images render at inconsistent sizes with visible grey padding around smaller images. Switch to `object-fit: cover` for a uniform, polished card grid look.

### 7. Improve the Testimonial Carousel

- Add large decorative opening quotation marks for visual impact — the text quotes exist in HTML but a typographic treatment would improve readability.
- The dot indicators are tiny (10px) and low-contrast (`WebContent/css/style.css:376`). Make them slightly larger or add a count label like "3 / 7".
- `height: 50vh` on `#testimonials` can clip longer quotes on smaller screens. Use `min-height` instead.

### 8. Feature Your Best Projects

With 17 cards, visitors may suffer from choice paralysis. Consider a "Featured" or "Pinned" row of 3-4 top projects above the full grid, or add a visual badge to highlight your strongest work.

---

## Lower Priority / Polish

### 9. Profile Picture Rendering

**File:** `WebContent/css/style.css:141`

The `.profile_pic` uses `scale: 0.7` — this scales a full-size image down via CSS, which wastes bandwidth and leaves dead space. Set an explicit `width`/`height` instead, or size the image itself.

### 10. Logo is Underutilized

**File:** `index.html:26`

The `.logo` div with "Charles Coonce" is visually plain and positioned in the top-left but does nothing (no link, no brand treatment). Either make it a nav anchor link to `#profile` or give it a bit more typographic weight.

### 11. Add a "Back to Top" Button

A floating button that appears after scrolling down improves UX significantly on long single-page sites.

### 12. Favicon

**File:** `index.html:17`

Using a `.jpeg` as a favicon is non-standard. Browsers handle it, but a proper `.ico` or `.png` (32x32 or 64x64) is more reliable across platforms and bookmark displays.

### 13. Keyboard/Focus Accessibility

There are no visible focus styles for the filter buttons or carousel nav. Add a `:focus-visible` style so keyboard users can navigate clearly.

---

## Summary Priority Table

| Priority | Change | Impact |
|----------|--------|--------|
| 1 | Sticky navigation | High — improves navigation on a long page |
| 2 | Project card descriptions | High — gives context before external clicks |
| 3 | Skills/About section | High — immediate tech stack visibility |
| 4 | Contact section at bottom | High — persistent CTA for recruiters |
| 5 | Fix hero `padding-left: 10rem` | Medium — cleaner layout |
| 6 | `object-fit: cover` on project images | Medium — visual consistency |
| 7 | Testimonial carousel improvements | Medium — better usability and readability |
| 8 | Feature top projects | Medium — reduces choice paralysis |
| 9 | Profile picture sizing | Low — performance and layout fix |
| 10 | Logo link/branding | Low — minor UX polish |
| 11 | Back to top button | Low — convenience feature |
| 12 | Proper favicon format | Low — cross-browser reliability |
| 13 | Focus/accessibility styles | Low — keyboard navigation support |
