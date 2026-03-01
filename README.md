# Charles Coonce — Data Analytics Portfolio

Personal portfolio site showcasing data science, analytics engineering, and software development projects.

**Live site:** [charleslikesdata.com](https://charleslikesdata.com)

---

## Table of Contents

- [Charles Coonce — Data Analytics Portfolio](#charles-coonce--data-analytics-portfolio)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Local Development](#local-development)
  - [Available Scripts](#available-scripts)
  - [Code Standards](#code-standards)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript](#javascript)
  - [Branching \& Deployment](#branching--deployment)
    - [Branch naming](#branch-naming)
    - [Commit messages (Conventional Commits)](#commit-messages-conventional-commits)
    - [Deploying](#deploying)
  - [CI / CD Pipeline](#ci--cd-pipeline)
  - [Featured Projects](#featured-projects)
  - [Contact](#contact)
  - [License](#license)

---

## Overview

A single-page static site built with vanilla HTML5, CSS3, and JavaScript — no frameworks, no build tools. Hosted on GitHub Pages with a custom domain.

The site includes:

- Filterable project gallery with category tags
- Testimonials carousel
- Responsive layout across mobile, tablet, and desktop
- Contact links (GitHub, LinkedIn, Email)

---

## Tech Stack

| Area          | Technology                    |
| ------------- | ----------------------------- |
| Markup        | HTML5 (semantic elements)     |
| Styling       | CSS3 (custom properties, BEM) |
| Interactivity | Vanilla JavaScript (ES6+)     |
| Formatting    | Prettier                      |
| Hosting       | GitHub Pages                  |
| Domain        | Custom domain via `CNAME`     |

---

## Project Structure

```
Portfolio_Website/
├── index.html              # Single-page site (nav, profile, gallery, testimonials, footer)
├── 404.html                # Custom 404 page
├── CNAME                   # GitHub Pages custom domain
├── package.json            # Metadata and npm scripts
├── package-lock.json
├── .editorconfig           # Editor formatting rules
├── .prettierrc             # Prettier configuration
├── WebContent/
│   ├── assets/             # Images and icons (per-project subfolders)
│   ├── css/
│   │   ├── style.css       # Global styles and CSS custom properties
│   │   └── mediaqueries.css # Responsive breakpoints
│   └── js/
│       └── script.js       # Gallery filtering and carousel logic
├── docs/                   # Planning documents and site reviews
└── README.md
```

---

## Local Development

**Prerequisites:** Git, a modern browser, and Python 3 (for the dev server).

1. Clone the repository:

   ```bash
   git clone https://github.com/cdcoonce/Portfolio_Website.git
   cd Portfolio_Website
   ```

2. Install dev dependencies (Prettier):

   ```bash
   npm install
   ```

3. Start a local dev server:

   ```bash
   npm run serve
   # or directly: python3 -m http.server 8000
   ```

4. Open [http://localhost:8000](http://localhost:8000) in your browser.

> The site is a static file — you can also open `index.html` directly in a browser without a server.

---

## Available Scripts

| Command                | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `npm run serve`        | Start local dev server at `http://localhost:8000` |
| `npm run format`       | Auto-format all HTML, CSS, JS, MD, and JSON files |
| `npm run format:check` | Check formatting without writing changes          |

---

## Code Standards

Formatting is enforced via `.editorconfig` and `.prettierrc`:

- **Indentation:** 2 spaces
- **Line width:** 100 characters
- **Quotes:** Single quotes (JS)
- **Semicolons:** Required
- **Line endings:** LF
- **Encoding:** UTF-8
- **Final newline:** Required

### HTML

- Semantic elements throughout (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Descriptive `alt` text on all images
- `<button>` for interactive controls — not styled `<div>`s
- No inline styles or inline JavaScript

### CSS

- BEM naming convention (`.block__element--modifier`)
- CSS custom properties in `:root` for colors, fonts, and spacing
- Mobile-first approach — base styles for mobile, `min-width` media queries for larger screens

### JavaScript

- `'use strict';` at the top of every file
- `const` by default, `let` when reassignment is needed, never `var`
- Pure logic separated from DOM manipulation for readability and testability

---

## Branching & Deployment

This project uses a two-branch model:

| Branch     | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| `master`   | Development — all feature branches merge here        |
| `gh-pages` | Production — merging `master` here triggers a deploy |

### Branch naming

```
feature/add-tableau-project
fix/broken-resume-link
chore/update-dependencies
docs/update-readme
```

### Commit messages (Conventional Commits)

```
feat(gallery): add Manufacturing Downtime Analysis project card
fix(carousel): correct wraparound past last testimonial
docs(readme): update local development instructions
```

### Deploying

Deployment is **automated via GitHub Actions** (see [CI / CD Pipeline](#ci--cd-pipeline) below).

Every merge into `master` automatically triggers a merge from `master` → `gh-pages`,
which GitHub Pages then serves as the live site. No manual steps are needed.

---

## CI / CD Pipeline

A single GitHub Actions workflow (`.github/workflows/ci-cd.yml`) handles both
continuous integration and deployment.

| Trigger                         | Jobs that run                  |
| ------------------------------- | ------------------------------ |
| Pull request targeting `master` | `lint` — Prettier format check |
| Push to `master` (merged PR)    | `lint` → `deploy`              |

**`lint` job** — runs on every PR and every push to `master`:

- Installs Node.js 20 and project dependencies (`npm ci`)
- Runs `npm run format:check` (Prettier) across all HTML, CSS, JS, MD, and JSON files
- Fails the workflow if any file is not correctly formatted

**`deploy` job** — runs only on push to `master`, and only after `lint` passes:

- Checks out the full Git history
- Checks out `gh-pages` locally
- Merges `origin/master` into `gh-pages`
- Pushes the updated `gh-pages` branch to GitHub, triggering the live site update

The pipeline uses the built-in `GITHUB_TOKEN` with `contents: write` permission —
no external secrets or personal access tokens are required.

---

## Featured Projects

| Project                                   | Tools                      |
| ----------------------------------------- | -------------------------- |
| National Parks Dashboard                  | Tableau, Python            |
| Wine Quality Analysis                     | Python, Pandas, Matplotlib |
| Manufacturing Downtime Analysis           | SQL, Power BI              |
| NYC Collision Analysis                    | Python, Folium             |
| Global CO2 Emissions                      | Tableau                    |
| Spaceship Titanic Classification          | Python, scikit-learn       |
| Housing Affordability & Commute Tradeoffs | Python, GeoPandas          |
| AirBnB Listing Analysis                   | SQL, Python                |
| World Happiness Dashboard                 | Tableau                    |
| Sleep Deprivation Analysis                | R, ggplot2                 |

Full project details, descriptions, and links are on the [live site](https://charleslikesdata.com).

---

## Contact

**Charles Coonce**

- Email: [charles.coonce@gmail.com](mailto:charles.coonce@gmail.com)
- LinkedIn: [linkedin.com/in/charlescoonce](https://www.linkedin.com/in/charlescoonce/)
- GitHub: [github.com/cdcoonce](https://github.com/cdcoonce)

---

## License

All rights reserved. © 2026 Charles Coonce.

This repository is for a personal portfolio site. The code may be referenced for learning purposes, but may not be copied or repurposed for commercial use without permission.
