# Phase 4: Testimonials & Contact

**Suggestions addressed:** #4 (Contact Section), #7 (Testimonial Carousel Improvements)
**Impact:** Medium-High — improves social proof presentation and adds a persistent CTA

---

## Overview

The testimonials section needs visual refinements to make quotes more impactful, and the site is missing a contact section at the bottom of the page. These are grouped together because they both affect the bottom half of the page and the contact section will sit between testimonials and the footer.

---

## Tasks

### 4.1 Add decorative quotation marks to testimonials

**Files:** `WebContent/css/style.css`

Add a large typographic opening quote mark using a CSS `::before` pseudo-element on each `.testimonial`.

```css
.testimonial::before {
  content: "\201C"; /* Left double quotation mark */
  font-size: 3rem;
  color: rgba(53, 53, 53, 0.2);
  font-family: Georgia, serif;
  line-height: 1;
  display: block;
  margin-bottom: -0.5rem;
}
```

### 4.2 Improve dot indicators

**File:** `WebContent/css/style.css:370-383`

**Current:** 10px dots with low-contrast colors (`#b0b4b9ac` inactive, `#272829c1` active).

**Proposed:**
```css
.dot {
  width: 12px;
  height: 12px;
  margin: 0 6px;
  background-color: #ccc;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #353535;
}
```

Changes: slightly larger, full-opacity colors, added `cursor: pointer` for affordance.

**Optional enhancement:** Add click-to-navigate on dots. This requires a small JS addition in `WebContent/js/script.js` to the dot creation logic:

```javascript
dot.addEventListener('click', () => {
  carouselIndex = isDesktop ? index : index;
  showTestimonials(carouselIndex);
});
```

### 4.3 Fix testimonial section height constraint

**File:** `WebContent/css/style.css:281-290`

**Current:**
```css
#testimonials {
  height: 50vh;
  margin-top: 2rem;
}
```

**Proposed:**
```css
#testimonials {
  min-height: 40vh;
  padding: 2rem 0;
  margin-top: 2rem;
}
```

Replace `height` with `min-height` so longer testimonials (like Chris Allard's, which is 3 sentences) don't get clipped. Add vertical padding for consistent spacing.

### 4.4 Add a testimonial counter

**File:** `WebContent/css/style.css`, `WebContent/js/script.js`

Add a small "3 / 7" style counter below the dots to indicate position.

**HTML (added dynamically via JS):**
```html
<p class="testimonial-counter">1 / 7</p>
```

**JS update in `showTestimonials()`:**
```javascript
const counter = document.querySelector('.testimonial-counter');
if (counter) {
  const current = Math.floor(carouselIndex / testimonialsToShow) + 1;
  const total = Math.ceil(testimonials.length / testimonialsToShow);
  counter.textContent = `${current} / ${total}`;
}
```

### 4.5 Add a Contact section

**Files:** `index.html`, `WebContent/css/style.css`

Insert a new section between `#testimonials` and `<footer>` with contact links. This mirrors the hero section's contact icons but is always accessible at the bottom of the page.

**HTML:**
```html
<section id="contact">
  <h2>Get in Touch</h2>
  <p>Interested in working together or have a question? Reach out below.</p>
  <div class="contact-links">
    <a href="mailto:CharlesCoonce@Gmail.com" class="btn btn-color-1">Email Me</a>
    <a href="https://www.linkedin.com/in/charlesdcoonce/" target="_blank" rel="noopener noreferrer" class="btn btn-color-2">LinkedIn</a>
    <a href="https://github.com/cdcoonce" target="_blank" rel="noopener noreferrer" class="btn btn-color-2">GitHub</a>
  </div>
</section>
```

**CSS:**
```css
#contact {
  text-align: center;
  padding: 3rem 2rem;
  max-width: 600px;
  margin: 0 auto;
}

#contact h2 {
  margin-bottom: 0.5rem;
  font-size: 1.75rem;
}

#contact p {
  margin-bottom: 1.5rem;
}

.contact-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}
```

### 4.6 Update navigation

**File:** `index.html`

Add a "Contact" link to the sticky nav created in Phase 1:

```html
<li><a href="#contact">Contact</a></li>
```

---

## Testing Checklist

- [ ] Decorative quote marks display correctly and don't interfere with testimonial text
- [ ] Dots are visually distinct and clickable (if click-to-navigate is added)
- [ ] Longer testimonials are not clipped at any viewport size
- [ ] Counter updates correctly when navigating the carousel
- [ ] Contact section displays below testimonials with proper spacing
- [ ] Contact buttons link to correct destinations (email, LinkedIn, GitHub)
- [ ] "Contact" nav link scrolls to the new section
- [ ] Mobile layout: contact buttons stack or wrap gracefully

---

## Dependencies

- Phase 1 (nav bar) should be completed so the "Contact" nav link can be added
- The testimonial JS in `WebContent/js/script.js` will need updates for counter and dot-click features
