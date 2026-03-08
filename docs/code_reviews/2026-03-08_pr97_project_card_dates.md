# Code Review: PR #97 — feat: add dates to project cards for timeline visibility

**Date:** 2026-03-08
**Branch:** `feat/project-card-dates` -> `master`
**Files changed:** 37
**Additions:** 850 | **Deletions:** 246

## Status: PASSED (with minor suggestions)

## Summary

This PR adds date metadata to all 21 project context files, displays dates on project cards in the UI, sorts cards newest-first via JavaScript DOM reordering, and extends the knowledge base builder to extract and sort by date. Well-structured, phased implementation with good test coverage.

## Issues

### WARNING: JSDoc comment placement (filter.js:67)

The `initFilter` JSDoc block is orphaned — the `getSortedIndices` function and its own JSDoc were inserted between the `initFilter` JSDoc and the `initFilter` function declaration.

**File:** `WebContent/js/filter.js:67-81`

```js
// Line 67: This JSDoc belongs to initFilter but is now separated from it
/**
 * @param {Object} [config]
 * ...
 */
// Line 72: getSortedIndices JSDoc + function inserted here
/**
 * Returns indices that would sort dates newest-first...
 */
export const getSortedIndices = (dates) => { ... };

// Line 82: initFilter is now far from its JSDoc
export function initFilter(config = {}) {
```

**Fix:** Move `getSortedIndices` (lines 67-80) above the `initFilter` JSDoc block, or move the `initFilter` JSDoc to directly precede the function.

**Severity:** WARNING

---

### INFO: `getFeaturedVisibility` is an identity map (filter.js:48)

```js
export const getFeaturedVisibility = (featuredFlags) => {
  return featuredFlags.map((f) => f);
};
```

This creates a shallow copy via identity map. While not introduced by this PR, it's worth noting — `[...featuredFlags]` or `Array.from(featuredFlags)` would be clearer if the intent is copying, or just return the array directly if copying isn't needed.

**Severity:** INFO (pre-existing, not introduced by this PR)

---

### INFO: DOM reorder assumes single parent grid (filter.js:98-101)

```js
const grid = cards[0]?.parentElement;
if (grid) {
  sortedIndices.forEach((i) => grid.appendChild(cards[i]));
}
```

This assumes all `.project-card` elements share the same parent. This is true for the current HTML structure, but the assumption is implicit. A comment noting this assumption would add clarity.

**Severity:** INFO

---

### INFO: `parse_date_to_sort_key` silently returns empty string for invalid months (build_knowledge_base.py:48-50)

```python
month_num = MONTH_MAP.get(month_abbr, "")
if not month_num:
    return ""
```

If someone typos a month abbreviation (e.g., "Jab 2025"), it silently returns `""` and the project sorts to the end. This is safe behavior, but a `logging.warning()` call would help catch data entry mistakes during the build step.

**Severity:** INFO

---

### INFO: `load_all_projects` sort tiebreaker (build_knowledge_base.py:318)

```python
projects.sort(key=lambda p: (p.get("date_sort", ""), p["title"]), reverse=True)
```

With `reverse=True`, the title tiebreaker sorts Z-A for same-date projects. This is likely unintentional — typically alphabetical (A-Z) is preferred for tiebreaking. Consider a tuple key that reverses only the date:

```python
projects.sort(key=lambda p: (-ord_key(p["date_sort"]), p["title"]))
```

Or sort in two passes (stable sort):
```python
projects.sort(key=lambda p: p["title"])  # secondary: A-Z
projects.sort(key=lambda p: p.get("date_sort", ""), reverse=True)  # primary: newest
```

**Severity:** INFO

---

### INFO: Plan documents included in PR

Six plan files under `docs/plans/094-add-dates-to-project-cards/` are included. Per project conventions, fully implemented plans should be moved to `docs/plans/archive/`. Consider moving these before merge.

**Severity:** INFO

---

## Positives

- **Good TDD discipline** — Tests written for `parse_date_to_sort_key`, `parse_classification` with dates, `getSortedIndices`, and E2E date display/sort verification.
- **Clean separation** — `getSortedIndices` is a pure function extracted and independently testable.
- **Consistent data model** — Both `date` (human-readable "Mon YYYY") and `date_sort` (machine-sortable "YYYY-MM") stored, avoiding repeated parsing.
- **Stable sort** — JS sort handles tiebreaking by original index, preserving insertion order for same-date cards.
- **E2E coverage** — `test_cards_display_date` and `test_cards_sorted_newest_first` verify the full rendering pipeline.
- **All 94 tests pass** (40 Python + 54 JavaScript).

## Category Breakdown

| Category | Count |
|----------|-------|
| WARNING  | 1     |
| INFO     | 5     |
| ERROR    | 0     |

## Recommendation

**Approve with minor feedback.** The one WARNING (orphaned JSDoc) is a readability issue worth fixing. The INFO items are optional improvements. No bugs, no security issues, no architectural concerns.
