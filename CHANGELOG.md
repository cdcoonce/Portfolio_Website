# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.1.0] - 2026-07-03

### Added

- Rotate the Overview "Featured project" spotlight through four projects
  (AFK, claude-workflow, Oura Ring pipeline, my-brain vault) via a manual
  carousel with dots + prev/next arrows (no auto-rotate); AFK is the default slide
- `claude-workflow` project card, promote the Oura Ring pipeline to featured, and
  add the `my-brain` second-brain vault as a featured-only card
- Cockpit-style SVG hero mockups for claude-workflow, the Oura pipeline, and the
  my-brain vault, with each project's real KPIs baked in (skills/presets/tests/
  commits; API-sources/models/schedules/test-modules; notes/wikilinks/skills/domains)
- `featuredProjects()` selector in `src/lib/featured.js` with unit tests
- `hideFromGallery` project flag so a project can be featured without appearing as
  a clickable Work-gallery card (used by my-brain, whose repo is private)

### Changed

- Bump the "Projects shipped" metric 7 → 8
- Replace the 176 KB `oura-pipeline.svg` raster asset with a 3.6 KB vector mockup
- Featured-card CTA now links to each project's repository/artifact (per-project
  `ctaLabel`: "View live cockpit", "View repository", "Use this template") instead
  of a generic in-card "See all work" button; external links open in a new tab
- Replace the decorative preset bars on the claude-workflow mockup with real,
  labeled chips for the 5 project presets and 5 personas
- Replace afk's raster hero (afk.png) with a vector cockpit mockup matching the
  other featured cards (merged PRs / cost-per-PR / attempts / repos + an
  attempts-by-repo chart); the interactive cockpit stays as the CTA destination

## [2.0.1] - 2026-07-03

### Fixed

- Correct Clearway Energy start date to May 2025 (from May 2024) in the bio,
  the Ask AI knowledge base, and the downloadable resume PDF
- Wire the professional-experience section into the Ask AI system prompt so the
  chat agent can answer employment-tenure questions (previously it had no dates)

## [2.0.0] - 2026-07-03

Full redesign: the single-scroll site is replaced by a tabbed single-page
portfolio built on **Astro + React islands**, implemented from the Claude
Design comp (`Charles Coonce Portfolio.dc.html`).

### Added

- Astro project (`src/`, `public/`) with React islands (`@astrojs/react`) for the interactive layer
- Design tokens ported from the design system into `src/styles/tokens.css` (Poppins, grayscale + one pale-blue accent, pill geometry)
- Tabbed layout with six sections: Overview, Work, Experience, Testimonials, Ask AI, Contact
- Reusable components: `Button`, `Tag`, `ProjectCard`, plus per-tab components
- Overview tab: at-a-glance metrics + featured-project spotlight
- Experience tab: role timeline + categorized skills
- Testimonials tab: single-quote carousel with segment dots and prev/next
- Ask AI tab: suggested-topic sidebar + chat wired to the existing Lambda assistant (`src/lib/chat.js`), with the previous 25-question/hour rate limiting preserved
- Jest unit tests for the new pure logic (`src/lib/carousel.js`, `src/lib/chat.js`)
- Open Graph / Twitter card meta and a canonical URL in the base layout

### Changed

- Deploy pipeline now builds the Astro site and publishes `dist/` (including `CNAME`) to `gh-pages`, replacing the previous `main` → `gh-pages` file mirror
- CI `check` job now runs lint + Jest + `astro build` (Node only)

### Notes

- The previous vanilla site files (`index.html`, `WebContent/css`, `WebContent/js`, `projects.html`) remain in the repo but are no longer the deployed site; they can be removed in a follow-up once this is confirmed.
- The Python/Playwright E2E suite (`tests/`) targeted the retired DOM and is not run in CI; porting it to the Astro site is a tracked follow-up.

## [1.5.0] - 2026-03-01

### Added

- `:focus-visible` outline styles on all `<a>` and `<button>` elements for keyboard navigation
- `.sr-only` utility class (visually hidden but screen-reader accessible) using `clip-path`
- Visually hidden `<h2 class="sr-only">Projects</h2>` in projects section for screen-reader heading hierarchy
- `aria-label="Previous testimonial"` and `aria-label="Next testimonial"` on carousel nav buttons
- `aria-live="polite"` on the `.testimonials` container so screen readers announce slide changes
- WCAG 2.1 AA automated compliance test (`test_wcag_compliance`) using axe-playwright
- E2E accessibility tests: focus navigation, carousel ARIA labels, `aria-live` region
- Validation tests: testimonials h2 heading, projects h2 heading, carousel ARIA labels, aria-live attribute

### Changed

- `<p class="section_text__p1">Testimonials</p>` promoted to `<h2>` for correct heading hierarchy
- `.testimonial-counter` color darkened from `#777` to `#666` (contrast ratio: 4.47 → 5.74:1) to pass WCAG AA

## [1.4.0] - 2026-03-01

### Added

- Decorative opening quotation mark on each testimonial card via CSS `::before` pseudo-element
- Testimonial position counter ("1 / 7") rendered dynamically below the dots
- Click-to-navigate on carousel dot indicators
- Contact section between testimonials and footer with Email, LinkedIn, and GitHub buttons
- "Contact" link in the sticky navigation bar
- E2E carousel tests: next navigation, wraparound, counter display, counter update, dot click

### Changed

- Testimonial section height from fixed `50vh` to `min-height: 40vh` with `padding: 2rem 0` to prevent clipping of longer testimonials
- Dot indicators: slightly larger (12px), full-opacity colors, `cursor: pointer` affordance

## [1.3.0] - 2026-03-01

### Added

- 1–2 sentence descriptions on all 17 project cards, highlighting key technique or insight
- Featured badge (dark top border) on 4 highlight projects: National Parks Dashboard, Wine Quality Analysis, Manufacturing Downtime Analysis, and Housing Affordability & Commute Tradeoffs
- E2E gallery filter tests (implemented stubs from Phase 3 plan): filter-by-tag, reset-to-all, featured-card filterability
- New validation tests: all cards have descriptions, featured cards exist
- `.img--contain` utility class for screenshot/dashboard thumbnails that should not be cropped

### Changed

- `.project-card` height from fixed `400px` to `min-height: 430px` to accommodate descriptions
- Project card image `object-fit` from `contain` to `cover` for uniform thumbnail appearance
- Fixed pre-existing CSS lint error: added blank line before `50%` keyframe in `@keyframes bounce`

## [1.2.0] - 2026-03-01

### Added

- Skills & Tools section between hero and projects (4 categories, responsive grid)
- Skills nav link in the sticky nav bar

### Changed

- Profile picture: replaced `scale: 0.7` with `width/height: 100%; object-fit: cover`
- Hero spacing: removed fragile `padding-left: 10rem` from "Hello, I'm" text

### Fixed

- Favicon: replaced JPEG profile photo with SVG "CC" monogram

## [1.1.0] - 2026-03-01

### Added

- Sticky navigation bar with Home, Projects, and Testimonials anchor links
- Logo branding link in nav that scrolls back to the profile section
- Responsive hamburger menu for mobile viewports (≤700px) with aria controls
- Back-to-top button (fixed, bottom-right) that appears after scrolling 400px
- Test infrastructure: pyproject.toml, Makefile, Jest stubs, pytest fixtures

## [1.0.0] - 2025-01-15

### Added

- Initial portfolio site launch
- Project gallery with filter system (17 project cards)
- Testimonial carousel with 7 testimonials
- Responsive layout with desktop and mobile breakpoints
- Profile section with hero, bio, and contact links
