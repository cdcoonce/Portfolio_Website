# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
