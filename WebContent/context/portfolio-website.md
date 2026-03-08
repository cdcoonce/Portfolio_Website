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

- The site serves 17 project cards across a homepage (4 featured) and a full gallery page, with single-select skill-tag filtering and URL-driven deep links.
- The testimonial carousel displays 7 recommendations with responsive layout (2 on desktop, 1 on mobile), auto-scroll at 20-second intervals, and dot pagination.
- Responsive breakpoints at 1250px and 700px ensure the site works well on desktop, tablet, and mobile, with a hamburger menu for mobile navigation.
- WCAG 2.1 AA compliance is verified through automated axe-core accessibility testing.
- The CI/CD pipeline runs Prettier, Stylelint, ESLint, Jest, and pytest on every pull request, with automatic deployment on merge to master.
- The site is hosted on GitHub Pages with a custom domain at charleslikesdata.com.

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
