# Portfolio Website

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Aug 2024

## Summary

A multi-page static portfolio website built from scratch with vanilla HTML5, CSS3, and ES module JavaScript — no frameworks, no bundlers, no build step. The site showcases Charles's projects with filterable galleries, a testimonial carousel, responsive design, and WCAG 2.1 AA accessibility compliance. It is maintained with professional-grade tooling including CI/CD, automated testing, and semantic versioning.

## Business Problem

A data professional's portfolio needs to be more than a list of projects — it needs to demonstrate technical ability, attention to detail, and professionalism. Charles built his portfolio site to serve as both a showcase of his project work and a standalone demonstration of web development skills, code quality practices, and DevOps discipline.

## Approach

Charles designed and built the site as a multi-page static application. The homepage features a hero profile section, four featured project cards with skill-tag filtering, a testimonial carousel with auto-scroll and dot pagination, and contact links. A dedicated gallery page displays all 17 projects with URL-driven filtering (e.g., `projects.html?filter=python`). The JavaScript is organized as ES modules with pure functions for business logic and thin DOM wrappers for rendering, making the codebase testable.

The site is tested with a two-layer strategy: Jest with jsdom for JavaScript unit tests (filter logic, carousel state, utilities) and pytest with Playwright for integration tests (HTML validation, accessibility, E2E browser tests, link checking). Linting is enforced with ESLint, Stylelint, and Prettier. A GitHub Actions CI/CD pipeline runs all checks on every PR and automatically deploys passing changes from master to gh-pages.

## Key Results & Insights

### Site Functionality

- **17 project cards** span two pages — a homepage (4 featured) and a full gallery — with single-select skill-tag filtering and URL-driven deep links that preserve filter state across navigation (e.g., `projects.html?filter=python` bookmarks a filtered view).
- The testimonial carousel displays **7 professional recommendations** with responsive layout (2 visible on desktop, 1 on mobile), auto-scroll at 20-second intervals, manual navigation arrows, and dot pagination — all keyboard-navigable and ARIA-attributed.
- Responsive breakpoints at **1250px and 700px** ensure correct layout across desktop, tablet, and mobile viewports, with a hamburger menu replacing the navigation bar on smaller screens.

### Code Quality & Engineering Standards

- **JavaScript organized as ES modules** with pure filtering functions decoupled from DOM manipulation — enabling Jest unit testing of business logic without launching a browser or mocking the DOM extensively.
- **WCAG 2.1 AA compliance** is continuously verified through automated axe-core accessibility tests in every CI run — compliance is a measurable pass/fail metric, not a one-time manual audit that drifts over time.
- Semantic HTML5 with ARIA attributes throughout: all interactive elements are keyboard-navigable, all images have descriptive alt text, and the page structure is screen-reader-compatible.

### DevOps & CI/CD

- **GitHub Actions pipeline runs Prettier, Stylelint, ESLint, Jest, and pytest** (including Playwright E2E tests) on every pull request — code reaches master only when all checks pass, with no manual gate-keeping required.
- Automatic deployment from master to gh-pages means every merged PR goes live at **charleslikesdata.com** within minutes with no manual deployment step — a production-grade delivery pattern applied to a personal project.
- Semantic versioning in `package.json` and a maintained `CHANGELOG.md` demonstrate release discipline: every significant change is documented with type, scope, and rationale rather than accumulating undifferentiated commits.

## Technologies Used

- **Frontend:** HTML5 (semantic elements, ARIA attributes), CSS3 (custom properties, media queries), JavaScript (ES modules, strict mode)
- **Testing:** Jest + jsdom (JS unit tests), pytest + Playwright (E2E, accessibility, validation), axe-core (WCAG compliance)
- **Linting & formatting:** ESLint, Stylelint, Prettier, EditorConfig
- **CI/CD:** GitHub Actions (lint → test → deploy pipeline)
- **Hosting:** GitHub Pages with custom domain (CNAME)

## Challenges & Solutions

Building the project filtering system required careful coordination between the HTML data attributes (data-tags on each card), the JavaScript filter logic, and the URL parameter support for deep linking. Charles kept the filtering logic as pure functions that could be unit tested with Jest, while the DOM manipulation layer stayed thin. Another challenge was making the testimonial carousel accessible — it needed keyboard navigation, proper ARIA attributes, and responsive behavior that changed the number of visible cards based on viewport width.

## Links

- **Live Site:** https://charleslikesdata.com
- **GitHub:** https://github.com/cdcoonce/Portfolio_Website

## Skills Demonstrated

Web Development, DevOps & Tooling
