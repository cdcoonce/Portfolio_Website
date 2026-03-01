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

**Files:** `index.html`, `WebContent/css/style.css`

Insert a new section between `#profile` and `#projects` that gives visitors an immediate overview of the tech stack without needing to scroll to the project filters.

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
  </div>
</section>
```

**CSS styling:**
- Use a grid or flexbox layout with 3 columns on desktop, stacking on mobile
- Reuse the existing pill/tag styling from `.projects-filter .filter` for visual consistency
- Light background (same `#f9f9f9` as projects or white) to create section contrast
- Keep it compact — this should be a quick scan, not a deep dive

### 2.4 Replace the JPEG favicon

**File:** `index.html:17`

**Current:**
```html
<link rel="icon" type="image/jpeg" href="./WebContent/assets/Headshots/LinkedinProfile.jpeg" />
```

**Proposed:**
- Create a proper 32x32 and 64x64 `.png` favicon from the profile image (or a simple "CC" monogram)
- Save as `WebContent/assets/favicon.png`
- Update the link tag:

```html
<link rel="icon" type="image/png" href="./WebContent/assets/favicon.png" />
```

---

## Testing Checklist

- [ ] "Hello, I'm" text aligns naturally with the name and bio text
- [ ] Profile picture displays at correct size without dead space or overflow
- [ ] Profile picture remains circular and responsive across breakpoints
- [ ] Skills section displays between hero and projects
- [ ] Skills section is responsive (3 columns → stacked on mobile)
- [ ] Skill tags are visually consistent with the project filter tags
- [ ] Favicon displays correctly in browser tab and bookmarks
- [ ] Nav from Phase 1 still works (no layout conflicts with new section)

---

## Dependencies

- Phase 1 should be completed first (nav may need a "Skills" anchor link added)
- Favicon creation requires an image editing tool or CLI tool (e.g., ImageMagick)
