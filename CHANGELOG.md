# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
