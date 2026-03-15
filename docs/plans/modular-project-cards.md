# Plan: Modular Project Cards

## Context

Project cards are currently hardcoded in both `index.html` and `projects.html` with identical markup. Adding or removing a project requires editing both files with the same content. The recent Oura pipeline addition (PR on this branch) demonstrates the pain — a single-purpose commit editing two files with duplicate card HTML. This plan introduces a single data source and a JS renderer so projects are defined once and rendered dynamically on both pages.

## Approach: JS Data Module + DOM Renderer

Use a JS module (not JSON) as the single source of truth. A renderer module builds card DOM elements. `filter.js` remains unchanged — it reads `data-tags`, `data-date`, and `.featured` from the DOM, which the renderer produces identically.

```
projects.js (data) → renderer.js (DOM) → main.js (orchestrates) → filter.js (reads DOM)
                          ↑                       ↑
                   uses formatProjectDate()   DOMContentLoaded
                   from utils.js
```

### New Files

1. **[`WebContent/js/projects.js`](WebContent/js/projects.js)** — Exported array of project objects:

   ```js
   export const projects = [
     {
       id: "national-parks-dashboard",
       href: "https://...",
       title: "National Parks Dashboard",
       date: "2024-09", // YYYY-MM format, sole source for dates
       description: "Interactive Shiny dashboard...",
       image: "./WebContent/assets/...",
       imageAlt: "National Parks Dashboard",
       imageContain: true, // ONLY present when true (omit for default cover behavior)
       tags: ["r", "shiny", "analytics-dashboard", "visualization"],
       featured: true, // ONLY present when true
     },
     // ... all projects (18 on this branch)
   ];
   ```

   **Design decisions:**
   - `dateDisplay` removed — derived by `formatProjectDate()` in utils.js (DRY)
   - `imageContain` and `featured` only specified when `true` — reduces boilerplate on ~14 of 18 projects
   - `tags` is an array (not comma string) — renderer joins for `data-tags` attribute

2. **[`WebContent/js/renderer.js`](WebContent/js/renderer.js)** — Two exported functions:
   - `createProjectCard(project)` → returns an `<a>` DOM element with exact current card structure
   - `renderProjectCards(container, projects)` → clears container, populates with cards

   **Security:** Must use `document.createElement()` + `textContent` — never `innerHTML` — to prevent XSS if HTML appears in data strings.

### Modified Files

3. **[`WebContent/js/utils.js`](WebContent/js/utils.js)** — Add `formatProjectDate(dateStr)`:

   ```js
   // '2024-09' → 'Sep 2024'
   export function formatProjectDate(dateStr) { ... }
   ```

4. **[`WebContent/js/main.js`](WebContent/js/main.js)** — Import projects + renderer, render cards before `initFilter()`:

   ```js
   import { projects } from "./projects.js";
   import { renderProjectCards } from "./renderer.js";
   // inside DOMContentLoaded:
   const grid = document.querySelector(".projects-grid");
   if (grid) {
     renderProjectCards(grid, projects);
   } else {
     console.warn("projects-grid container not found");
   }
   // then existing initFilter() calls — unchanged
   ```

5. **[`index.html`](index.html)** — Remove all hardcoded `<a class="project-card">` elements, keep empty `<div class="projects-grid"></div>`

6. **[`projects.html`](projects.html)** — Same: remove card markup, keep empty grid container

7. **[`tests/test_validation.py`](tests/test_validation.py)** — Remove card-specific assertions that parse static HTML (lines 30-68, 145-147). These are replaced by Jest tests on the data module + renderer.

8. **[`WebContent/js/filter.js`](WebContent/js/filter.js)** — No changes needed

### Anti-FOUC

Since cards don't exist in HTML until JS renders them, the grid starts empty (no flash). The existing CSS rule `[data-page='home'] .project-card:not(.featured) { display: none; }` still works as defense-in-depth once cards are injected. ES modules execute quickly and rendering is synchronous, so the empty state is imperceptible.

## Implementation Order (TDD)

| Step | Task                                                                | File(s)                      |
| ---- | ------------------------------------------------------------------- | ---------------------------- |
| 1    | Write `formatProjectDate` tests                                     | `__tests__/utils.test.js`    |
| 2    | Implement `formatProjectDate`                                       | `WebContent/js/utils.js`     |
| 3    | Write data validation tests                                         | `__tests__/projects.test.js` |
| 4    | Create projects data module (extract from HTML)                     | `WebContent/js/projects.js`  |
| 5    | Write renderer tests                                                | `__tests__/renderer.test.js` |
| 6    | Create renderer module                                              | `WebContent/js/renderer.js`  |
| 7    | Update main.js to import and render                                 | `WebContent/js/main.js`      |
| 8    | Strip cards from index.html                                         | `index.html`                 |
| 9    | Strip cards from projects.html                                      | `projects.html`              |
| 10   | Migrate card pytest assertions to Jest, clean up test_validation.py | `tests/test_validation.py`   |
| 11   | Full test suite + manual smoke test                                 | All                          |

Steps 1-2 can run first (utils dependency). Then 3-4 and 5-6 are independent and can run as parallel subagents.

## Testing

### New Jest Tests

- **`__tests__/utils.test.js`** (extend existing): `formatProjectDate` — '2024-09' → 'Sep 2024', edge cases (missing input, malformed)
- **`__tests__/projects.test.js`**: Validate each project has required fields (`id`, `href`, `title`, `date`, `description`, `image`, `imageAlt`, `tags`), correct types, `date` matches `YYYY-MM`, `tags` is non-empty array, no duplicate `id` values. No hardcoded count assertions — schema validation per project is sufficient.
- **`__tests__/renderer.test.js`**: `createProjectCard()` returns `<a>` with class `project-card`, `data-tags` (comma-joined), `data-date`, `href`/`target`/`rel` attributes. Featured projects get `.featured` class. Image has `src`/`alt`/`loading="lazy"`/`width`/`height`, gets `img--contain` when `imageContain: true`. `.card-content` has `<h3>` title, `<span class="project-date">` with formatted date, `<p>` description. `renderProjectCards()` clears then populates container.

### Modified Pytest Tests

- **`tests/test_validation.py`**: Remove `test_all_project_cards_have_descriptions`, `test_featured_cards_exist`, `test_project_cards_are_anchor_elements`, `test_no_learn_more_buttons_in_cards`, `test_projects_page_has_all_17_cards`. Keep all non-card tests (semantic structure, chat section, contact, testimonials, accessibility).

### Unchanged

- **`__tests__/filter.test.js`**: Pure functions, unaffected
- **`__tests__/carousel.test.js`**, **`__tests__/chat.test.js`**: Unrelated

## Verification

1. `npx jest` — all JS tests pass (new + existing)
2. `uv run pytest` — Python tests pass (card assertions removed, remaining tests pass)
3. Open `index.html` locally — featured cards display, filter buttons work, "View All" links correctly
4. Open `projects.html` locally — all cards display, filtering and sorting work, URL `?filter=python` works
5. Verify card HTML in browser DevTools matches current structure (classes, data attributes, image attributes)
