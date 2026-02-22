# Code Review: Portfolio Website

**Date:** 2026-02-21
**Repository:** PortfolioWebsite
**Reviewer:** Claude (automated)
**Site:** charleslikesdata.com

---

## Summary

This is a single-page portfolio website built with vanilla HTML, CSS, and JavaScript, hosted on GitHub Pages. It features a profile hero section, a filterable project grid (17 projects), a testimonial carousel, and a footer. The codebase is clean and well-organized overall, with good use of Prettier for formatting. Below are findings organized by severity.

---

## Critical Issues

### 1. ~~Duplicate `class` attribute on LinkedIn icon (`index.html:49-54`)~~ RESOLVED (Plan 2)

```html
<img
  class="icon"
  src="./WebContent/assets/linkedinicon.png"
  alt="My LinkedIn profile"
  class="icon"
  onclick="window.open('https://www.linkedin.com/in/charlesdcoonce/', '_blank')"
/>
```

The `<img>` tag has `class="icon"` declared **twice** (lines 49 and 52). Per the HTML spec, duplicate attributes are invalid — the second one is silently ignored by most browsers. While it works in this case (both values are the same), it signals a copy-paste error and will fail HTML validation.

**Fix:** Remove the duplicate `class="icon"` on line 52.

---

### 2. Inline `onclick` handlers call functions scoped inside `DOMContentLoaded` (`index.html:233,280` / `script.js:156,171`)

```html
<button id="prevRec" class="btn btn-color-2" onclick="prevTestimonial()">&#10094</button>
<button id="nextRec" class="btn btn-color-2" onclick="nextTestimonial()">&#10095</button>
```

The `prevTestimonial()` and `nextTestimonial()` functions are defined inside a `DOMContentLoaded` callback in `script.js`, making them **local to that closure**. Inline `onclick` attributes can only call globally-scoped functions. This means the inline `onclick` handlers will throw a `ReferenceError` at runtime.

The code works anyway because the JS also attaches `addEventListener('click', ...)` on lines 184-185, which properly reference the closure-scoped functions. The inline `onclick` attributes are dead code that produce console errors when clicked (the `addEventListener` fires first, but the inline handler still attempts to resolve the function name globally).

**Fix:** Remove the `onclick` attributes from both buttons entirely since the `addEventListener` calls in `script.js` already handle the click events correctly.

---

### 3. ~~`style_backup.css` checked into the repository~~ RESOLVED (Plan 1)

The file `WebContent/css/style_backup.css` is a stale backup of the main stylesheet from a previous iteration (contains the old carousel-based project layout). Backup files should not be tracked in version control — that's what git history is for. It adds 421 lines of dead code to the repo and could cause confusion about which file is authoritative.

**Fix:** Delete `style_backup.css` and rely on git history for previous versions.

---

## High-Priority Issues

### 4. ~~Incorrect `alt` text on multiple project images (`index.html:112,164,172,180,188`)~~ RESOLVED (Plan 2)

Five project card images all share the alt text `"Dangerous Collision Factors"`, which was clearly copy-pasted from the NYC Collisions card:

| Line | Project                    | Alt Text                                                   |
| ---- | -------------------------- | ---------------------------------------------------------- |
| 112  | Manufacturing Downtime     | `"Electricity Consumption"` (wrong, copied from Project 3) |
| 164  | Global CO2 Emissions       | `"Dangerous Collision Factors"`                            |
| 172  | AirBnB Listing Analysis    | `"Dangerous Collision Factors"`                            |
| 180  | Sleep Deprivation Analysis | `"Dangerous Collision Factors"`                            |
| 188  | Restaurant Order Analysis  | `"Dangerous Collision Factors"`                            |

This hurts accessibility (screen readers announce wrong content) and SEO.

**Fix:** Update each `alt` attribute to accurately describe the project image.

---

### 5. ~~Mail icon has wrong `alt` text (`index.html:46`)~~ RESOLVED (Plan 2)

```html
<a class="icon" href="mailto:CharlesCoonce@Gmail.com">
  <img src="./WebContent/assets/mailicon.png" alt="My Github profile" />
</a>
```

The email icon's alt text says `"My Github profile"` instead of something like `"Email me"`. This is misleading for screen reader users.

**Fix:** Change to `alt="Email Charles Coonce"` or similar.

---

### 6. ~~LinkedIn icon uses `<img onclick>` instead of `<a>` tag (`index.html:49-54`)~~ RESOLVED (Plan 2)

The LinkedIn icon is an `<img>` with an inline `onclick` to open a URL. Unlike the email icon (which correctly uses an `<a>` tag), this element:

- Is not keyboard-accessible (no focus or Enter-key activation)
- Has no `role="link"` or `tabindex`
- Won't be announced as a link by screen readers

**Fix:** Wrap the `<img>` in an `<a>` tag like the email icon:

```html
<a
  class="icon"
  href="https://www.linkedin.com/in/charlesdcoonce/"
  target="_blank"
  rel="noopener noreferrer"
>
  <img src="./WebContent/assets/linkedinicon.png" alt="LinkedIn profile" />
</a>
```

---

### 7. `padding-top` overridden immediately by `padding` shorthand (`style.css:100-101`)

```css
section {
  padding-top: 2vh;
  padding: 0 2rem;     /* This resets padding-top to 0 */
  ...
}
```

The `padding` shorthand on line 101 resets all four sides, overwriting the `padding-top: 2vh` declared on line 100. The `padding-top` has no effect.

**Fix:** Either use longhand properties (`padding-left`, `padding-right`) or combine into a single shorthand: `padding: 2vh 2rem 0 2rem;`.

---

### 8. `box-sizing: border-box` declared on `section` but already set globally (`style.css:5-9, 103`)

The universal selector `*` already sets `box-sizing: border-box`. The redundant declaration on `section` is harmless but unnecessary.

**Fix:** Remove `box-sizing: border-box` from the `section` rule.

---

## Medium-Priority Issues

### 9. Testimonial section uses `id="contacts"` (`index.html:229`)

The testimonials section has `id="contacts"` but contains no contact information — it only has testimonials. The CSS targets `#contacts` accordingly. This is a semantic naming issue that makes the code harder to understand.

**Fix:** Rename to `id="testimonials"` and update CSS references.

---

### 10. ~~Missing `rel="noopener noreferrer"` on external links~~ RESOLVED (Plan 2)

All external `<a>` tags with `target="_blank"` (project links on lines 89, 98, 107, etc.) are missing `rel="noopener noreferrer"`. While modern browsers mitigate the old `window.opener` vulnerability, it's still a best practice.

**Fix:** Add `rel="noopener noreferrer"` to all `<a target="_blank">` links.

---

### 11. ~~Buttons use `onclick="window.open(...)"` instead of `<a>` tags (`index.html:32-41`)~~ RESOLVED (Plan 2)

The GitHub and Resume buttons are `<button>` elements with inline `onclick` handlers calling `window.open()`. This pattern:

- Is not accessible (screen readers don't announce them as links)
- Doesn't support right-click > open in new tab
- Doesn't show the URL on hover in the browser status bar

**Fix:** Replace with `<a>` elements styled as buttons.

---

### 12. ~~Filename typo: `mediaquerires.css`~~ RESOLVED (Plan 1)

The file is named `mediaquerires.css` (extra "r" — should be `mediaqueries.css`). This typo exists in the filename and the `<link>` reference on `index.html:17`.

**Fix:** Rename file to `mediaqueries.css` and update the HTML reference.

---

### 13. Copyright year is hardcoded to 2024 (`index.html:286`)

```html
<p>Copyright &#169; 2024 Charles Coonce. All Rights Reserved.</p>
```

The copyright year is static. The README says 2025. Neither matches the current year of 2026.

**Fix:** Either update manually to the current year, or use JavaScript to set it dynamically:

```js
document.querySelector('footer p').innerHTML =
  `Copyright &copy; ${new Date().getFullYear()} Charles Coonce. All Rights Reserved.`;
```

---

### 14. ~~Missing `<meta name="description">` tag (`index.html`)~~ RESOLVED (Plan 2)

The `<head>` section has no meta description, which is important for SEO. Search engines use this to generate snippet text in results.

**Fix:** Add a meta description:

```html
<meta
  name="description"
  content="Charles Coonce - Data analyst portfolio showcasing projects in Python, SQL, R, Tableau, and more."
/>
```

---

### 15. ~~No favicon defined~~ RESOLVED (Plan 2)

The site has no `<link rel="icon">` in the `<head>`. Browsers will request `/favicon.ico` by default and receive a 404.

**Fix:** Add a favicon link in the `<head>`.

---

### 16. Font family inconsistency in testimonials section (`style.css:299`)

The `.testimonials-container` explicitly sets `font-family: Arial, sans-serif`, overriding the global `Poppins` font from the `body` rule. This also appears in the media queries (`mediaquerires.css:78, 119`). The testimonials section will render in a different font than the rest of the page.

**Fix:** Remove the `font-family` override from `.testimonials-container` (and its media query duplicates) to inherit Poppins consistently.

---

### 17. Auto-scroll `setInterval` never clears on page visibility change (`script.js:188-195`)

The testimonial carousel auto-scrolls every 20 seconds via `setInterval`. This timer runs indefinitely even when the tab is in the background, which:

- Wastes CPU cycles
- Can cause the carousel to jump multiple positions when the user returns

**Fix:** Use `document.addEventListener('visibilitychange', ...)` to pause/resume the interval, or switch to `setTimeout` with recursive calls.

---

### 18. Filter matching uses `String.includes()` which can produce false positives (`script.js:50`)

```js
const matches = Array.from(activeFilters).some((filter) => tags.includes(filter));
```

If a tag value is a substring of another (e.g., `"r"` is contained in `"machine-learning"`), clicking the "R" filter could incorrectly match cards tagged with `machine-learning`. Currently this happens to work because the `data-tags` values are comma-separated, but only by luck — `"r"` matches in strings like `"r,shiny"` as a substring, which is correct, but would break if a tag like `"r-studio"` were added.

**Fix:** Split `data-tags` by comma and use `Set`-based or array `.includes()` instead of string matching:

```js
const tagSet = new Set(card.getAttribute('data-tags').split(','));
const matches = Array.from(activeFilters).some((f) => tagSet.has(f));
```

---

### 19. ~~Portfolio Website card has empty `data-tags` (`index.html:129`)~~ RESOLVED (Plan 2)

```html
<div class="project-card" data-tags=""></div>
```

Project 6 (Portfolio Website) has `data-tags=""`. When any filter other than "All" is selected, this card will always be hidden. This may be intentional, but it's inconsistent — the card is visible with "All" but vanishes with any filter.

**Fix:** Add relevant tags (e.g., `"html,css,javascript"`) or add a dedicated "Web Development" filter.

---

## Low-Priority / Style Issues

### 20. ~~Inconsistent indentation in HTML~~ RESOLVED (Plan 1)

The HTML file mixes tabs and spaces for indentation, and nesting levels are inconsistent. For example, Projects 14-15 have an extra level of indentation compared to other cards, and Projects 16-17 are dedented differently.

**Fix:** Run Prettier (`npm run format`) to normalize formatting.

---

### 21. Unused CSS animation `fadeIn` (`style.css:389-396`)

The `@keyframes fadeIn` animation is defined but never referenced anywhere in the stylesheets.

**Fix:** Remove the unused animation, or apply it to testimonial transitions.

---

### 22. Unused CSS class `.p` (`style.css:324-326`)

```css
.p {
  display: flex;
}
```

This class is never used in the HTML.

**Fix:** Remove it.

---

### 23. Redundant CSS in media queries

The `@media (max-width: 1250px)` and `@media (max-width: 700px)` blocks in `mediaquerires.css` redeclare many properties that are identical to the base styles (e.g., `.testimonial` has the same `display: none`, `padding: 20px`, etc.). Only override what actually changes at each breakpoint.

**Fix:** Remove redundant property declarations from media queries.

---

### 24. ~~`package.json` main field points to non-existent file~~ RESOLVED (Plan 1)

```json
"main": "index.js"
```

There is no `index.js` in the project. This is a default value from `npm init` and is unused for a static site.

**Fix:** Remove the `main` field or change it to `"index.html"`.

---

### 25. ~~Missing opening quotation mark in testimonial (`index.html:249`)~~ RESOLVED (Plan 2)

```html
He <strong>collaborated and communicated</strong> well...
```

This testimonial (Katie Marks) is missing the opening `"` but has a closing `"`. The other testimonials are properly quoted.

**Fix:** Add the opening quotation mark.

---

### 26. ~~`<title>` is generic (`index.html:15`)~~ RESOLVED (Plan 2)

```html
<title>My Portfolio</title>
```

A more specific title like `"Charles Coonce | Data Analytics Portfolio"` would be better for SEO, bookmarks, and browser tabs.

---

### 27. `transition: all 300ms ease` is overly broad (`style.css:26-29`)

Applying `transition: all` to `a`, `img`, and `.btn` globally means every CSS property change (including layout properties) will animate. This can cause unexpected visual glitches and minor performance overhead.

**Fix:** Target specific properties: `transition: color 300ms ease, background-color 300ms ease, transform 300ms ease, box-shadow 300ms ease;`

---

### 28. `justify-content: right` is non-standard (`style.css:339,348,357`)

```css
.author {
  justify-content: right;
}
.job {
  justify-content: right;
}
.company {
  justify-content: right;
}
```

The value `right` is not standard for `justify-content` in flexbox. The correct value is `flex-end`. Some browsers may handle this gracefully, but it's not spec-compliant.

**Fix:** Change to `justify-content: flex-end;`.

---

## Security Considerations

### 29. Google Analytics ID exposed in source

The GA tracking ID `G-C3MKQC8F23` is visible in the HTML source. This is normal and expected for client-side analytics — not a vulnerability, but worth noting that anyone can send spoofed events to this ID. GA filtering should be configured server-side.

### 30. Email address in plain text (`index.html:43`)

The `mailto:` link exposes the email address to scrapers. Consider obfuscating it via JavaScript or using a contact form service if spam becomes an issue.

---

## Performance Notes

### 31. ~~No image optimization strategy~~ PARTIALLY RESOLVED (Plan 2 — added `loading="lazy"` to all project images)

Project card images are served as full-resolution PNGs/JPEGs without:

- Explicit `width`/`height` attributes (causes layout shift)
- `loading="lazy"` for below-the-fold images
- WebP/AVIF format alternatives
- Responsive `srcset` for different viewports

**Fix:** At minimum, add `loading="lazy"` to all project images and explicit `width`/`height` attributes.

### 32. Google Fonts loaded via `@import` in CSS (`style.css:3`)

Using `@import` in CSS is render-blocking — the browser must download the CSS, parse it, discover the `@import`, then fetch the font. Moving the Google Fonts `<link>` to the HTML `<head>` (with `rel="preconnect"`) would load faster.

**Fix:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
  rel="stylesheet"
/>
```

---

## Architecture & Maintainability

### 33. Single HTML file for 17 projects limits scalability

All 17 project cards are hardcoded in `index.html`. Adding or reordering projects requires editing HTML directly. For a site of this size it's manageable, but as the project count grows, consider:

- A JSON data file with project metadata rendered by JS
- A static site generator (e.g., 11ty, Hugo)

### 34. No error page (404)

GitHub Pages serves a default 404 page. A custom `404.html` would maintain branding if visitors hit a broken link.

---

## What's Done Well

- **Clean vanilla stack** — no unnecessary frameworks for what's fundamentally a static site
- **Well-structured JS** — guard clauses, configuration constants (`CAROUSEL_CONFIG`), and JSDoc comments
- **Good filter UX** — multi-select with OR logic and "All" reset is intuitive
- **Consistent code formatting** — Prettier + EditorConfig keep the codebase tidy
- **Responsive design** — three breakpoints handle desktop/tablet/mobile
- **Project diversity** — the portfolio demonstrates range across Python, SQL, R, Tableau, Excel, and Shiny

---

## Recommended Priority Order

1. Fix the inline `onclick` / scoped function conflict (issue #2)
2. Fix incorrect `alt` text across images (issues #4, #5)
3. Make LinkedIn icon keyboard-accessible (issue #6)
4. Fix the filter substring matching bug (issue #18)
5. Fix the overridden `padding-top` (issue #7)
6. Add `loading="lazy"` to images (issue #31)
7. Move Google Fonts to `<head>` (issue #32)
8. Clean up naming/typos (issues #9, #12, #13, #25, #26)
9. Remove dead code (issues #3, #21, #22)
10. Add meta description and favicon (issues #14, #15)
