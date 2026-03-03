# Phase 2: HTML Changes

**Files:** `index.html` (modify), `projects.html` (create)

## 2.1 Changes to `index.html`

### Add `data-page` attribute to `<body>`

```html
<body data-page="home"></body>
```

This allows `main.js` to determine which page config to use for `initFilter`.

### Change reset button text

Current (line ~126 area):

```html
<button class="skill-filter-reset active" data-filter="all">All Projects</button>
```

New:

```html
<button class="skill-filter-reset active" data-filter="featured">Featured</button>
```

The button now defaults to showing featured projects instead of all projects.

### Add "View All Projects" link

Insert immediately after the closing `</div>` of `.projects-grid`:

```html
<div class="projects-footer">
  <a href="./projects.html" class="btn btn-color-1 view-all-link">View All Projects</a>
</div>
```

### Keep all 17 cards in the DOM

All 17 project cards remain in `index.html`. JavaScript handles visibility — only 4 are shown at a time via `display: flex | none`. This preserves the filter logic's ability to search across all projects.

### Update section heading (optional)

Consider changing the projects `<h2>` from "Projects" to "Featured Projects" to better communicate the curated nature. The "View All Projects" link provides the path to the full gallery.

## 2.2 Create `projects.html`

### Structure

The new page is a standalone HTML file at the project root. It shares the same `<head>`, `<nav>`, and `<footer>` as `index.html` but contains only the skills filter and projects sections.

```
projects.html
├── <head> (same meta, same CSS links)
├── <body data-page="projects">
│   ├── <header>
│   │   └── <nav> (same structure, "Projects" link active)
│   ├── <main>
│   │   ├── <section id="skills">
│   │   │   ├── Section heading: "All Projects"
│   │   │   ├── Reset button: "All Projects" (data-filter="all")
│   │   │   ├── "Featured" as a skill-tag button (data-filter="featured")
│   │   │   └── Same 4 skill categories with all filter tags
│   │   └── <section id="projects">
│   │       └── <div class="projects-grid">
│   │           └── All 17 project cards (same HTML as index.html)
│   └── <footer> (same structure)
│   └── <script type="module" src="./WebContent/js/main.js">
```

### Navigation adjustments

On `projects.html`, the nav links need slight changes:

| Link         | `index.html` value | `projects.html` value           |
| ------------ | ------------------ | ------------------------------- |
| Home         | `#profile`         | `./index.html`                  |
| Skills       | `#skills`          | `#skills` (same page section)   |
| Projects     | `#projects`        | `#projects` (same page section) |
| Testimonials | `#testimonials`    | `./index.html#testimonials`     |
| Contact      | `#contact`         | `./index.html#contact`          |

### "Featured" as a filter tag

On `projects.html`, "Featured" appears as a regular skill tag button (not the reset button). It filters to only the 4 featured cards:

```html
<div class="skill-category">
  <h3>Filter</h3>
  <div class="skill-tags">
    <button class="skill-tag" data-filter="featured">Featured</button>
  </div>
</div>
```

The `getFilteredVisibility` function needs to handle `featured` as a special filter value. When the active filter set contains `"featured"`, cards with the `featured` CSS class are shown (not matched by `data-tags`).

**Implementation detail:** In `initFilter`, when building the tag sets, also inject `"featured"` into the tag set of cards that have the `featured` class. This keeps the pure function working without special cases:

```javascript
const cardTagSets = Array.from(cards).map((c) => {
  let tags = c.getAttribute('data-tags') || '';
  if (c.classList.contains('featured')) {
    tags = tags ? `${tags},featured` : 'featured';
  }
  return tags;
});
```

### Elements NOT included on `projects.html`

- Profile/hero section
- Testimonials carousel
- Contact form
- Scroll-down button
- Back-to-top button (could optionally include)

### Page title

```html
<title>All Projects | Charles Coonce</title>
```

## Data Duplication Note

The 17 project cards are duplicated between `index.html` and `projects.html`. This is acceptable for a vanilla HTML site with no templating engine. A future enhancement could extract project data into a JSON file and render cards dynamically, but that is out of scope for this plan.
