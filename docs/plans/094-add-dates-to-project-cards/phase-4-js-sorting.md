# Phase 4: JavaScript Date Sorting

## Goal

Sort project cards by `data-date` (newest first) on page load.

## Files

- `__tests__/filter.test.js` — write failing tests first
- `WebContent/js/filter.js` — implement

## Tests to Add

```javascript
describe('getSortedIndices', () => {
  test('sorts newest first', () => {
    const result = getSortedIndices(['2024-01', '2025-06', '2024-12']);
    expect(result).toEqual([1, 2, 0]);
  });

  test('handles missing date — sorts to end', () => {
    const result = getSortedIndices(['2025-01', '', '2024-06']);
    expect(result).toEqual([0, 2, 1]);
  });

  test('stable sort for same date', () => {
    const result = getSortedIndices(['2025-01', '2025-01', '2024-06']);
    expect(result).toEqual([0, 1, 2]);
  });
});
```

## Implementation

1. **Export new pure function** `getSortedIndices(dates)` from `filter.js`:
    - Maps each date to `{ date, index }` pair
    - Replaces missing/empty dates with `"0000-00"` (sorts to end)
    - Sorts descending by date string (`b.date.localeCompare(a.date)`)
    - Returns array of original indices in sorted order

2. **In `initFilter()`**, before building `cardTagSets`:
    - Read `data-date` from all cards
    - Compute sorted indices via `getSortedIndices()`
    - Reorder DOM: `sortedIndices.forEach(i => container.appendChild(cards[i]))`
    - Re-query cards after reorder so subsequent filter logic uses the new order

## Verify

```bash
npm test
uv run pytest tests/test_gallery.py
```
