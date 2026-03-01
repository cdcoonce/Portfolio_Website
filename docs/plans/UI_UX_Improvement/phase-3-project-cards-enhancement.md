# Phase 3: Project Cards Enhancement

**Suggestions addressed:** #2 (Project Descriptions), #6 (Image Standardization), #8 (Featured Projects)
**Impact:** High — project cards are the core content of the portfolio

---

## Overview

The projects section is the centerpiece of the portfolio but currently lacks context. Each card shows only a title and a "Learn More" link — visitors must click through to GitHub to understand what the project is about. This phase adds descriptions, standardizes the visual treatment, and highlights the best work.

---

## Tasks

### 3.1 Add descriptions to project cards

**File:** `index.html`

Add a `<p>` element inside each `.card-content` div with a 1-2 sentence description. The existing CSS already styles `.card-content p` with `color: #555` and `flex-grow: 1`.

**Example (Project 1):**

```html
<div class="card-content">
  <h3>National Parks Dashboard</h3>
  <p>
    Interactive Shiny dashboard exploring NPS visitation trends across parks, states, and time
    periods.
  </p>
</div>
```

**Descriptions needed for all 17 projects.** Each description should:

- Be 1-2 sentences max
- Highlight the key technique or insight, not just the topic
- Use active language ("Analyzes...", "Explores...", "Predicts...")

### 3.2 Adjust card height for descriptions

**File:** `WebContent/css/style.css:222-224`

The current fixed height of `400px` may need adjustment to accommodate descriptions without overflow.

**Current:**

```css
.project-card {
  height: 400px;
  width: 300px;
}
```

**Proposed:** Increase to `~430px` or use `min-height: 400px` to allow flexible expansion. Test with the longest description to ensure the "Learn More" button (positioned absolutely at `bottom: 1rem`) doesn't overlap text.

### 3.3 Standardize project card images

**File:** `WebContent/css/style.css:231-236`

**Current:**

```css
.project-card img {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background-color: #f0f0f0;
}
```

**Proposed:**

```css
.project-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background-color: #f0f0f0;
}
```

**Consideration:** `object-fit: cover` will crop some images. Review each project thumbnail to verify important content isn't clipped. For images that are charts or code screenshots, cropping may cut off key details. Options:

- Use `object-position` to control which part of the image is visible
- Create standardized 300x200 thumbnails for each project (ideal long-term)
- Use `cover` for most but override with `contain` on specific cards via a utility class

### 3.4 Add a "Featured" row for top projects

**Files:** `index.html`, `WebContent/css/style.css`

Add a visually distinct row of 3-4 featured projects above the main grid. This reduces choice paralysis by guiding visitors to the strongest work first.

**Option A — Visual badge on existing cards:**
Add a `.featured` class to select project cards and style with a subtle accent (e.g., a colored top border or a small "Featured" label).

```css
.project-card.featured {
  border-top: 3px solid #353535;
}
```

**Option B — Separate featured row:**
Create a distinct section above the filter/grid with larger cards or a different layout.

```html
<h3 class="projects-section-title">Featured Work</h3>
<div class="projects-grid featured-grid">
  <!-- 3-4 featured project cards -->
</div>
<h3 class="projects-section-title">All Projects</h3>
<div class="projects-filter">...</div>
<div class="projects-grid">...</div>
```

**Recommendation:** Option A is simpler and avoids duplicating cards. Option B gives more visual weight but requires deciding whether featured cards also appear in the main grid.

### 3.5 Update filter behavior for featured cards

**File:** `WebContent/js/script.js`

If using Option A (badge), ensure the filter logic still works normally — featured cards should be filtered like any other card. The `.featured` class is purely visual.

If using Option B (separate row), the featured row should remain visible regardless of filter state (it sits outside the filtered grid).

---

## Testing Checklist

- [ ] All 17 project cards have descriptions that fit within the card without overflow
- [ ] "Learn More" button doesn't overlap description text on any card
- [ ] Images look consistent across cards with the new `object-fit` value
- [ ] No critical image content is clipped by `object-fit: cover`
- [ ] Featured projects are visually distinguishable
- [ ] Filter system still works correctly with all changes
- [ ] Cards render properly in single-column mobile layout
- [ ] Card grid alignment is maintained (no orphaned cards creating uneven rows)

---

## Dependencies

- Phases 1 and 2 should be completed first
- Project descriptions need to be written (content task, not code)
- If creating standardized thumbnails (3.3), image assets need to be prepared
