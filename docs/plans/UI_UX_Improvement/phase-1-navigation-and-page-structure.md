# Phase 1: Navigation & Page Structure

**Suggestions addressed:** #1 (Sticky Nav), #10 (Logo Branding), #11 (Back to Top)
**Impact:** High — establishes site-wide navigation framework before other content changes

---

## Overview

This phase adds the structural navigation elements that the rest of the site depends on. A sticky nav bar, branded logo link, and back-to-top button together solve the core usability problem: users currently have no way to move between sections without manually scrolling.

---

## Tasks

### 1.1 Add a `<nav>` element with section links

**Files:** `index.html`, `WebContent/css/style.css`

- Insert a `<nav>` element above the `#profile` section in `index.html`
- Include anchor links: Home (`#profile`), Projects (`#projects`), Testimonials (`#testimonials`)
- Move the existing `.logo` div ("Charles Coonce") inside the `<nav>` as the site brand/home link
- Wrap the logo text in an `<a href="#profile">` so it scrolls to the top

```html
<nav id="main-nav">
  <a href="#profile" class="logo">Charles Coonce</a>
  <ul class="nav-links">
    <li><a href="#profile">Home</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#testimonials">Testimonials</a></li>
  </ul>
</nav>
```

### 1.2 Style the nav bar as sticky

**Files:** `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`

> **Note:** Base styles go in `style.css`. Responsive overrides (e.g., reduced padding, font-size adjustments at `max-width: 1250px` and `max-width: 700px`) go in `mediaqueries.css`.

- `position: sticky; top: 0; z-index: 100`
- Background color: `#fff` with a subtle `box-shadow` on scroll (or a permanent light shadow)
- Flex layout: logo left-aligned, nav links right-aligned
- Match existing Poppins font and dark grey (`#353535`) color scheme
- Add hover/active state underline or color shift for nav links

```css
#main-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #353535;
  font-weight: 500;
  transition: color 300ms ease;
}

.nav-links a:hover {
  color: #000;
}
```

### 1.3 Add responsive nav with hamburger menu

**Files:** `index.html`, `WebContent/css/mediaqueries.css`, `WebContent/js/script.js`

At `max-width: 700px`, the nav links collapse behind a hamburger toggle button.

**HTML — add toggle button inside `<nav>` (after logo, before `<ul>`):**

```html
<button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
  <span class="nav-toggle__bar"></span>
  <span class="nav-toggle__bar"></span>
  <span class="nav-toggle__bar"></span>
</button>
```

**CSS in `mediaqueries.css` (inside `@media (max-width: 700px)`):**

```css
.nav-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.nav-toggle__bar {
  display: block;
  width: 24px;
  height: 3px;
  background-color: #353535;
  border-radius: 2px;
  transition:
    transform 300ms ease,
    opacity 300ms ease;
}

.nav-links {
  display: none;
  flex-direction: column;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  gap: 1rem;
}

.nav-links.open {
  display: flex;
}
```

**CSS in `style.css` (base styles — hide toggle on desktop):**

```css
.nav-toggle {
  display: none;
}
```

**JS toggle logic (in `script.js`):**

```javascript
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });
}
```

**Additional responsive concerns:**

- Logo font size may need reduction on small screens (`font-size: 1rem` at 700px)
- Close the menu when a nav link is clicked (add click listeners on `.nav-links a`)

### 1.4 Add a "Back to Top" button

**Files:** `index.html`, `WebContent/css/style.css`, `WebContent/js/script.js`

- Add a fixed-position button in the bottom-right corner of the viewport
- Hidden by default, appears after scrolling past the hero section (~400px)
- Smooth-scrolls to `#profile` on click
- Style as a circular button with an up-arrow (`&#8593;` or an SVG icon)

```css
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #353535;
  color: #fff;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  opacity: 0;
  transition: opacity 300ms ease;
  z-index: 99;
}

.back-to-top.visible {
  opacity: 1;
}
```

```javascript
const backToTop = document.querySelector('.back-to-top');
window.addEventListener('scroll', () => {
  backToTop.classList.toggle('visible', window.scrollY > 400);
});
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
```

### 1.5 Update the logo styling

**File:** `WebContent/css/style.css`

- Remove the standalone `.logo` styles from the profile section
- Restyle as a nav-integrated brand element with slightly bolder weight (`font-weight: 600`) and larger size
- Ensure no underline on the anchor link

---

## Testing Checklist

- [ ] Nav is visible and sticky at all scroll positions
- [ ] All anchor links scroll smoothly to correct sections
- [ ] Logo click scrolls to top
- [ ] Back-to-top button appears/disappears based on scroll position
- [ ] Nav renders properly at desktop (>1250px), tablet (700-1250px), and mobile (<700px)
- [ ] Nav does not overlap or obscure content in the hero section
- [ ] Existing `scroll-behavior: smooth` on `html` works with nav anchor links

---

## Dependencies

- None — this phase can be implemented independently
- Subsequent phases will add new nav links (e.g., "Contact" in Phase 4) to this nav bar
