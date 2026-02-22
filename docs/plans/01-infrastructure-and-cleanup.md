# Plan 1: Infrastructure and Cleanup — COMPLETED

**Status:** Implemented 2026-02-21
**Priority:** Do this FIRST (changes filenames referenced by other plans)
**Complexity:** Small
**Files touched:** `mediaquerires.css`, `style_backup.css`, `index.html`, `package.json`

---

## Issues Addressed

| #   | Issue                                                            | Severity |
| --- | ---------------------------------------------------------------- | -------- |
| 3   | `style_backup.css` is dead code checked into repo                | Critical |
| 12  | Filename typo `mediaquerires.css` (should be `mediaqueries.css`) | Medium   |
| 20  | Inconsistent HTML indentation (tabs vs spaces)                   | Low      |
| 24  | `package.json` main field points to non-existent `index.js`      | Low      |

---

## Step-by-Step Changes

### Step 1: Delete `style_backup.css` (Issue #3)

**File:** `WebContent/css/style_backup.css`

Delete this file entirely. It is a 421-line stale backup of the main stylesheet from a previous iteration (old carousel-based project layout). Git history preserves all previous versions.

```bash
git rm WebContent/css/style_backup.css
```

Verify it is not referenced anywhere:

- Not linked in `index.html`
- Not imported by any other CSS file

---

### Step 2: Rename `mediaquerires.css` to `mediaqueries.css` (Issue #12)

**File:** `WebContent/css/mediaquerires.css` -> `WebContent/css/mediaqueries.css`

```bash
git mv WebContent/css/mediaquerires.css WebContent/css/mediaqueries.css
```

Then update the reference in `index.html` line 17:

**Before:**

```html
<link rel="stylesheet" href="./WebContent/css/mediaquerires.css" />
```

**After:**

```html
<link rel="stylesheet" href="./WebContent/css/mediaqueries.css" />
```

---

### Step 3: Fix `package.json` main field (Issue #24)

**File:** `package.json` line 4

**Before:**

```json
"main": "index.js",
```

**After:**

```json
"main": "index.html",
```

---

### Step 4: Normalize formatting with Prettier (Issue #20)

Run Prettier to fix inconsistent indentation across all files:

```bash
npm run format
```

This normalizes tabs vs spaces, nesting levels, and trailing whitespace according to the existing `.prettierrc` and `.editorconfig` configuration.

---

## Verification

1. Open `index.html` in browser — confirm styles load correctly (no 404 for CSS files)
2. Inspect DevTools Network tab — confirm `mediaqueries.css` loads (not `mediaquerires.css`)
3. Confirm `style_backup.css` no longer exists in the working tree
4. Run `npm run format:check` — should pass with no issues
5. `git status` should show the rename, deletion, and any formatting changes
