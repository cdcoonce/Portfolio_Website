# Phase 2: CSS Cleanup & Custom Properties

**Priority:** Second — no dependencies on Phase 1 but keeps CSS changes isolated
**Complexity:** Medium
**Review items addressed:** #5, #12, #14, #15, #20
**Files touched:** `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`

---

## Issues Addressed

| #   | Issue                                                          | Severity |
| --- | -------------------------------------------------------------- | -------- |
| 5   | No CSS custom properties — colors hard-coded throughout        | Medium   |
| 12  | Dead CSS rules referencing removed classes                     | Low      |
| 14  | No-op CSS declarations (`.rec`, `.author`, `.job`, `.company`) | Low      |
| 15  | Inconsistent `@media screen and` vs `@media` syntax            | Low      |
| 20  | `0rem` with unnecessary unit                                   | Low      |

**Not in scope:** Full mobile-first rewrite (#6), BEM rename (#7), `px` → `rem` conversion (#7). These are deferred as aspirational per user decision.

---

## Step-by-Step Changes

### Step 1: Add CSS custom properties to `:root` (Issue #5)

**File:** `WebContent/css/style.css` — add at the very top, before the `* { ... }` reset

Extract all repeated color values into custom properties. This creates a single source of truth for the design palette without renaming any classes or restructuring selectors.

```css
:root {
  --color-text-primary: #353535;
  --color-text-secondary: rgb(85, 85, 85);
  --color-bg-white: #fff;
  --color-bg-light: #f9f9f9;
  --color-bg-card-highlight: rgba(235, 241, 248, 0.4);
  --color-accent-dark: rgb(53, 53, 53);
  --color-accent-black: rgb(0, 0, 0);
  --color-border: rgb(53, 53, 53);
  --color-shadow: rgba(0, 0, 0, 0.1);
  --color-dot-inactive: #ccc;
  --color-counter: #666;
  --color-quote: rgba(53, 53, 53, 0.2);
}
```

Then replace all hard-coded color values with the corresponding custom property. Key replacements:

| Hard-coded value                 | Replace with                    | Occurrences |
| -------------------------------- | ------------------------------- | ----------- |
| `#353535`                        | `var(--color-text-primary)`     | ~12         |
| `rgb(85, 85, 85)`               | `var(--color-text-secondary)`   | 1           |
| `#fff` / `white`                 | `var(--color-bg-white)`         | ~8          |
| `#f9f9f9`                        | `var(--color-bg-light)`         | 2           |
| `rgb(53, 53, 53)`               | `var(--color-accent-dark)`      | ~6          |
| `rgb(0, 0, 0)`                  | `var(--color-accent-black)`     | 2           |
| `rgba(0, 0, 0, 0.1)`            | `var(--color-shadow)`           | 2           |
| `rgba(0, 0, 0, 0.08)`           | Keep as-is (unique, nav only)   | 1           |
| `rgba(0, 0, 0, 0.15)`           | Keep as-is (unique, hover only) | 1           |
| `rgba(235, 241, 248, 0.4)`      | `var(--color-bg-card-highlight)`| 1           |
| `rgba(53, 53, 53, 0.2)`         | `var(--color-quote)`            | 1           |
| `#ccc`                           | `var(--color-dot-inactive)`     | 1           |
| `#666`                           | `var(--color-counter)`          | 1           |
| `#555`                           | `var(--color-text-secondary)`   | 3           |

**Note:** `#555` and `rgb(85, 85, 85)` are the same color. Consolidate to `var(--color-text-secondary)`.

Also update `mediaqueries.css` line 97 where `#ebf1f866` is used — this is `rgba(235, 241, 248, 0.4)` in hex notation. Replace with `var(--color-bg-card-highlight)`.

---

### Step 2: Remove dead CSS rules (Issue #12)

**File:** `WebContent/css/mediaqueries.css` lines 24–27, 67–75

Delete these rules that reference classes no longer in the HTML:

**Delete** (lines 24–27):

```css
.project__pic-container {
  width: 22.25rem;
  height: 20rem;
}
```

**Delete** (lines 67–75):

```css
.projects-filter {
  gap: 0.5rem; /* Reduce gap if needed */
}

.projects-filter .filter {
  flex: 1 1 100px;
  font-size: 0.9rem;
  text-align: center;
}
```

---

### Step 3: Fix no-op CSS declarations (Issue #14)

**File:** `WebContent/css/style.css`

**3a.** Replace `.rec { justify-self: left; }` (line 496–498) with `text-align: left` which actually works on block-level elements inside a flex column:

**Before:**

```css
.rec {
  justify-self: left;
}
```

**After:**

```css
.rec {
  text-align: left;
}
```

**3b.** Simplify `.author`, `.job`, `.company` (lines 500–526). These are `<p>` elements containing only text. Remove the unnecessary `display: flex; flex-direction: row;` and use `text-align: right` instead of `justify-content: flex-end`:

**Before:**

```css
.author {
  display: flex;
  flex-direction: row;
  margin-top: 10px;
  font-weight: bold;
  font-size: 14px;
  color: #555;
  justify-content: flex-end;
}

.job {
  display: flex;
  flex-direction: row;
  margin-top: 1px;
  font-size: 14px;
  color: #555;
  justify-content: flex-end;
}

.company {
  display: flex;
  flex-direction: row;
  margin-top: 1px;
  font-size: 14px;
  color: #555;
  justify-content: flex-end;
}
```

**After:**

```css
.author {
  margin-top: 10px;
  font-weight: bold;
  font-size: 14px;
  color: var(--color-text-secondary);
  text-align: right;
}

.job {
  margin-top: 1px;
  font-size: 14px;
  color: var(--color-text-secondary);
  text-align: right;
}

.company {
  margin-top: 1px;
  font-size: 14px;
  color: var(--color-text-secondary);
  text-align: right;
}
```

---

### Step 4: Normalize media query syntax (Issue #15)

**File:** `WebContent/css/mediaqueries.css` line 1

Remove the `screen and` keyword from the first breakpoint so both breakpoints use the same syntax.

**Before:**

```css
@media screen and (max-width: 1250px) {
```

**After:**

```css
@media (max-width: 1250px) {
```

---

### Step 5: Remove unit from zero value (Issue #20)

**File:** `WebContent/css/mediaqueries.css` line 48

**Before:**

```css
.section_text__p1 {
  padding-left: 0rem;
}
```

**After:**

```css
.section_text__p1 {
  padding-left: 0;
}
```

---

## Verification

1. Open `index.html` in browser — confirm no visual changes (colors should be identical)
2. Inspect with DevTools — confirm CSS custom properties are visible in `:root`
3. Search both CSS files for any remaining hard-coded `#353535` or `rgb(53, 53, 53)` — should be zero (except within `:root` definitions)
4. Run `npm run lint:css` — Stylelint passes
5. Run `npm run format:check` — Prettier passes
6. Run `uv run pytest -m e2e` — E2E tests pass (carousel, gallery unaffected)
