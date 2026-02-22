# Plan 2: HTML Accessibility and Semantics — COMPLETED

**Status:** Implemented 2026-02-21
**Priority:** High — do after Plan 1
**Complexity:** Large (many edits, but all mechanical)
**Files touched:** `index.html` only

---

## Issues Addressed

| #   | Issue                                                          | Severity    |
| --- | -------------------------------------------------------------- | ----------- |
| 1   | Duplicate `class` attribute on LinkedIn `<img>`                | Critical    |
| 4   | Wrong/copy-pasted `alt` text on 5 project images               | High        |
| 5   | Mail icon `alt` says "My Github profile"                       | High        |
| 6   | LinkedIn icon is `<img onclick>` — not keyboard-accessible     | High        |
| 10  | Missing `rel="noopener noreferrer"` on `target="_blank"` links | Medium      |
| 11  | GitHub/Resume buttons use `onclick` instead of `<a>` tags      | Medium      |
| 14  | Missing `<meta name="description">` tag                        | Medium      |
| 15  | No favicon defined                                             | Medium      |
| 19  | Portfolio Website card has empty `data-tags`                   | Medium      |
| 25  | Missing opening quotation mark in testimonial                  | Low         |
| 26  | Generic `<title>` tag                                          | Low         |
| 31  | No `loading="lazy"` on project images                          | Performance |

---

## Step-by-Step Changes

### Step 1: Update `<title>` tag (Issue #26)

**Line 15**

**Before:**

```html
<title>My Portfolio</title>
```

**After:**

```html
<title>Charles Coonce | Data Analytics Portfolio</title>
```

---

### Step 2: Add `<meta name="description">` (Issue #14)

**Insert after line 14 (after the viewport meta tag):**

```html
<meta
  name="description"
  content="Charles Coonce — Data analyst portfolio showcasing projects in Python, SQL, R, Tableau, and more."
/>
```

---

### Step 3: Add favicon link (Issue #15)

**Insert in `<head>` section, near the other link tags:**

```html
<link rel="icon" type="image/png" href="./WebContent/assets/favicon.png" />
```

> **Note:** A favicon image file will need to be created or sourced. If no favicon asset is available, use a placeholder or generate one from the profile picture.

---

### Step 4: Replace GitHub button with `<a>` tag (Issue #11)

**Lines 32-35**

**Before:**

```html
<button class="btn btn-color-1" onclick="window.open('https://github.com/cdcoonce')">GitHub</button>
```

**After:**

```html
<a
  class="btn btn-color-1"
  href="https://github.com/cdcoonce"
  target="_blank"
  rel="noopener noreferrer"
>
  GitHub
</a>
```

---

### Step 5: Replace Resume button with `<a>` tag (Issue #11)

**Lines 37-41**

**Before:**

```html
<button
  class="btn btn-color-1"
  onclick="window.open('./WebContent/assets/CharlesCoonce_Resume.pdf')"
>
  Resume
</button>
```

**After:**

```html
<a
  class="btn btn-color-1"
  href="./WebContent/assets/CharlesCoonce_Resume.pdf"
  target="_blank"
  rel="noopener noreferrer"
>
  Resume
</a>
```

---

### Step 6: Fix mail icon `alt` text (Issue #5)

**Line 44-47**

**Before:**

```html
<img src="./WebContent/assets/mailicon.png" alt="My Github profile" />
```

**After:**

```html
<img src="./WebContent/assets/mailicon.png" alt="Email Charles Coonce" />
```

---

### Step 7: Fix LinkedIn icon — wrap in `<a>`, remove duplicate class (Issues #1, #6)

**Lines 49-54**

**Before:**

```html
<img
  class="icon"
  src="./WebContent/assets/linkedinicon.png"
  alt="My LinkedIn profile"
  class="icon"
  onclick="window.open('https://www.linkedin.com/in/charlesdcoonce/', '_blank')"
/>
```

**After:**

```html
<a
  class="icon"
  href="https://www.linkedin.com/in/charlesdcoonce/"
  target="_blank"
  rel="noopener noreferrer"
>
  <img src="./WebContent/assets/linkedinicon.png" alt="My LinkedIn profile" />
</a>
```

This fixes three problems at once:

- Removes the duplicate `class="icon"` attribute
- Makes the link keyboard-accessible (focusable, Enter-key activated)
- Screen readers will announce it as a link

---

### Step 8: Fix incorrect `alt` text on project images (Issue #4)

**Line 112 — Manufacturing Downtime:**

```html
<!-- Before -->
<img
  src="./WebContent/assets/Manufacturing_Downtime_Analysis/Dashboard.png"
  alt="Electricity Consumption"
/>
<!-- After -->
<img
  src="./WebContent/assets/Manufacturing_Downtime_Analysis/Dashboard.png"
  alt="Manufacturing Downtime Dashboard"
/>
```

**Line 164 — Global CO2 Emissions:**

```html
<!-- Before -->
<img
  src="./WebContent/assets/Global_CO2_Emissions/Dashboard.png"
  alt="Dangerous Collision Factors"
/>
<!-- After -->
<img
  src="./WebContent/assets/Global_CO2_Emissions/Dashboard.png"
  alt="Global CO2 Emissions Dashboard"
/>
```

**Line 172 — AirBnB Listing Analysis:**

```html
<!-- Before -->
<img
  src="./WebContent/assets/Airbnb_Listings_Analysis/Final_Viz.png"
  alt="Dangerous Collision Factors"
/>
<!-- After -->
<img
  src="./WebContent/assets/Airbnb_Listings_Analysis/Final_Viz.png"
  alt="AirBnB Listing Analysis Visualization"
/>
```

**Line 180 — Sleep Deprivation Analysis:**

```html
<!-- Before -->
<img
  src="./WebContent/assets/SleepDeprivation_HighStress_Reactions.png"
  alt="Dangerous Collision Factors"
/>
<!-- After -->
<img
  src="./WebContent/assets/SleepDeprivation_HighStress_Reactions.png"
  alt="Sleep Deprivation High Stress Reactions"
/>
```

**Line 188 — Restaurant Order Analysis:**

```html
<!-- Before -->
<img
  src="./WebContent/assets/Restaurant_Order_Analysis/Table_Joined_Analysis.png"
  alt="Dangerous Collision Factors"
/>
<!-- After -->
<img
  src="./WebContent/assets/Restaurant_Order_Analysis/Table_Joined_Analysis.png"
  alt="Restaurant Order Analysis SQL Join"
/>
```

---

### Step 9: Add `rel="noopener noreferrer"` to all external links (Issue #10)

Add `rel="noopener noreferrer"` to every `<a>` tag that has `target="_blank"`. These are the 17 "Learn More" project links:

- Line 89: National Parks Dashboard
- Line 98: Wine Quality
- Line 107: Electricity Consumption
- Line 116: Manufacturing Downtime
- Line 125: National Parks Analysis
- Line 134: Portfolio Website
- Line 143: World Happiness Dashboard
- Line 152: Data Archive
- Line 160: NYC Collision Analysis
- Line 168: Global CO2 Emissions
- Line 176: AirBnB Listing Analysis
- Line 184: Sleep Deprivation
- Line 192: Restaurant Order Analysis
- Line 200: Motor Vehicle Thefts
- Line 208: Baby Names Analysis
- Line 216: Spaceship Titanic
- Line 224: Housing Affordability

**Example (apply to all 17):**

```html
<!-- Before -->
<a href="https://..." target="_blank" class="btn">Learn More</a>
<!-- After -->
<a href="https://..." target="_blank" rel="noopener noreferrer" class="btn">Learn More</a>
```

---

### Step 10: Add tags to Portfolio Website card (Issue #19)

**Line 129**

**Before:**

```html
<div class="project-card" data-tags=""></div>
```

**After:**

```html
<div class="project-card" data-tags="html,css,javascript"></div>
```

> **Note:** If you don't want to add new filter buttons for HTML/CSS/JS, use existing tags or leave empty intentionally. Alternatively, add a "web-development" tag and corresponding filter button.

---

### Step 11: Fix missing opening quotation mark (Issue #25)

**Line 249**

**Before:**

```html
<p class="rec">He <strong>collaborated and communicated</strong> well...</p>
```

**After:**

```html
<p class="rec">"He <strong>collaborated and communicated</strong> well...</p>
```

---

### Step 12: Add `loading="lazy"` to all project images (Issue #31)

Add `loading="lazy"` to all 17 project card `<img>` tags. The first 2-3 images above the fold can optionally keep `loading="eager"` (the default), but all below-the-fold images should be lazy-loaded.

**Example (apply to all project images):**

```html
<!-- Before -->
<img src="./WebContent/assets/..." alt="..." />
<!-- After -->
<img src="./WebContent/assets/..." alt="..." loading="lazy" />
```

---

## Verification

1. Open `index.html` in browser — all images display correctly
2. Check browser tab title shows "Charles Coonce | Data Analytics Portfolio"
3. View page source — confirm no duplicate `class` attributes
4. Tab through all interactive elements — GitHub, Resume, Email, LinkedIn should all be focusable and activatable via Enter key
5. Right-click GitHub/Resume buttons — "Open in new tab" should appear in context menu
6. Run a screen reader or accessibility audit (Chrome DevTools > Lighthouse > Accessibility)
7. Inspect Network tab — confirm images below the fold load lazily on scroll
8. Validate HTML at validator.w3.org
