# Phase 2: Hero & Profile Polish

**Suggestions addressed:** #3 (Skills/About Section), #5 (Hero Spacing), #9 (Profile Picture), #12 (Favicon)
**Impact:** High — improves the first impression and above-the-fold experience

---

## Overview

The hero section is the first thing visitors see. This phase fixes layout quirks, optimizes the profile image rendering, adds a dedicated skills section for immediate tech stack visibility, and resolves the favicon issue. These changes all live in or near the top of the page and can be done together.

---

## Tasks

### 2.1 Fix the hero section spacing

**File:** `WebContent/css/style.css:153-157`

The `.section_text__p1` "Hello, I'm" text has `padding-left: 10rem`, creating a fragile offset.

**Current:**

```css
.section_text__p1 {
  text-align: left;
  font-size: 1.75rem;
  padding-left: 10rem;
}
```

**Proposed:** Remove the padding and let the text align naturally with the rest of `.section_text`. If a visual offset is desired, use a small `margin-left` or adjust within flexbox.

```css
.section_text__p1 {
  text-align: left;
  font-size: 1.75rem;
}
```

### 2.2 Fix profile picture rendering

**File:** `WebContent/css/style.css:138-141`

The `.profile_pic` uses `scale: 0.7` to shrink a large image via CSS transform. This wastes bandwidth and creates dead space around the image.

**Current:**

```css
.profile_pic {
  border-radius: 40rem;
  scale: 0.7;
}
```

**Proposed:** Replace `scale` with explicit dimensions. The container is already constrained to 400x400px, so set the image to fill it.

```css
.profile_pic {
  border-radius: 50%;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

Also consider creating a properly-sized version of `LinkedinProfile.jpeg` (400x400px) to reduce file size.

### 2.3 Add a Skills/About section

**Files:** `index.html`, `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`

Insert a new section between `#profile` and `#projects` that gives visitors an immediate overview of the tech stack without needing to scroll to the project filters.

> **Note:** Base grid styles go in `style.css`. The responsive column collapse (4 columns → 2 → 1) goes in `mediaqueries.css`.

The 4 categories below align exactly with the 13 existing filter tags used in the projects section:

**HTML structure:**

```html
<section id="skills">
  <h2>Skills & Tools</h2>
  <div class="skills-grid">
    <div class="skill-category">
      <h3>Languages</h3>
      <div class="skill-tags">
        <span class="skill-tag">Python</span>
        <span class="skill-tag">SQL</span>
        <span class="skill-tag">R</span>
      </div>
    </div>
    <div class="skill-category">
      <h3>Techniques</h3>
      <div class="skill-tags">
        <span class="skill-tag">ETL/ELT</span>
        <span class="skill-tag">Machine Learning</span>
        <span class="skill-tag">Statistical Analysis</span>
      </div>
    </div>
    <div class="skill-category">
      <h3>Tools & Platforms</h3>
      <div class="skill-tags">
        <span class="skill-tag">Tableau</span>
        <span class="skill-tag">Excel</span>
        <span class="skill-tag">Shiny</span>
      </div>
    </div>
    <div class="skill-category">
      <h3>Focus Areas</h3>
      <div class="skill-tags">
        <span class="skill-tag">Data Visualization</span>
        <span class="skill-tag">Analytics Dashboards</span>
        <span class="skill-tag">Data Pipelines</span>
        <span class="skill-tag">Business Intelligence</span>
      </div>
    </div>
  </div>
</section>
```

**CSS styling in `style.css`:**

```css
#skills {
  padding: 2rem;
  background-color: #f9f9f9;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.skill-category h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #353535;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  /* Reuse existing filter pill styling for visual consistency */
  padding: 0.4rem 0.8rem;
  border: 1px solid #353535;
  border-radius: 2rem;
  font-size: 0.85rem;
  color: #353535;
  background-color: #fff;
}
```

**Responsive overrides in `mediaqueries.css`:**

```css
/* At 1250px: 2 columns */
@media screen and (max-width: 1250px) {
  .skills-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* At 700px: single column */
@media (max-width: 700px) {
  .skills-grid {
    grid-template-columns: 1fr;
  }
}
```

Also add a "Skills" link to the nav from Phase 1:

```html
<li><a href="#skills">Skills</a></li>
```

### 2.4 Replace the JPEG favicon

**Files:** `index.html:17`, `WebContent/assets/favicon.png` (new)

**Current:**

```html
<link rel="icon" type="image/jpeg" href="./WebContent/assets/Headshots/LinkedinProfile.jpeg" />
```

**Design decision:** Use a "CC" monogram — dark grey (`#353535`) initials on a transparent background. This reads clearly at 32x32px and works at all sizes.

**Creating the favicon with ImageMagick:**

```bash
# Install ImageMagick if not present: brew install imagemagick
convert -size 64x64 xc:transparent \
  -font Helvetica-Bold -pointsize 32 \
  -fill '#353535' \
  -gravity Center -annotate 0 'CC' \
  WebContent/assets/favicon-64.png

convert WebContent/assets/favicon-64.png \
  -resize 32x32 \
  WebContent/assets/favicon.png
```

**Alternative — create via browser canvas (no CLI tools required):**

Open the browser console on any page and run:

```javascript
const canvas = document.createElement('canvas');
canvas.width = 64;
canvas.height = 64;
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#353535';
ctx.font = 'bold 28px Helvetica, Arial, sans-serif';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText('CC', 32, 34);
const a = document.createElement('a');
a.href = canvas.toDataURL('image/png');
a.download = 'favicon.png';
a.click();
```

Save the downloaded file to `WebContent/assets/favicon.png`.

**Update the link tag in `index.html`:**

```html
<link rel="icon" type="image/png" href="./WebContent/assets/favicon.png" />
```

---

## Testing Checklist

- [ ] "Hello, I'm" text aligns naturally with the name and bio text
- [ ] Profile picture displays at correct size without dead space or overflow
- [ ] Profile picture remains circular and responsive across breakpoints
- [ ] Skills section displays between hero and projects
- [ ] Skills section is responsive (4 columns → 2 columns → stacked on mobile)
- [ ] Skill tags are visually consistent with the project filter tags
- [ ] Favicon displays correctly in browser tab and bookmarks
- [ ] Nav from Phase 1 still works (no layout conflicts with new section)

---

## Dependencies

- Phase 1 must be completed first (the "Skills" nav link is added in task 2.3)
- Favicon creation: use either ImageMagick (`brew install imagemagick`) or the browser canvas method — no other tools required
