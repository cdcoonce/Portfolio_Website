import {
  getFilteredVisibility,
  applyMaxVisible,
  getFeaturedVisibility,
  getFilterFromURL,
  getSortedIndices,
} from '../WebContent/js/filter.js';

describe('getFilteredVisibility', () => {
  const cardTags = [
    'python,etl,visualization',
    'r,shiny,analytics-dashboard',
    'sql,business-intelligence',
    'python,machine-learning',
  ];

  test('returns all true when no filters are active', () => {
    const result = getFilteredVisibility(cardTags, new Set());
    expect(result).toEqual([true, true, true, true]);
  });

  test('filters to cards matching a single tag', () => {
    const result = getFilteredVisibility(cardTags, new Set(['python']));
    expect(result).toEqual([true, false, false, true]);
  });

  test('filters with multiple active tags (OR logic)', () => {
    const result = getFilteredVisibility(cardTags, new Set(['python', 'sql']));
    expect(result).toEqual([true, false, true, true]);
  });

  test('returns all false when filter matches nothing', () => {
    const result = getFilteredVisibility(cardTags, new Set(['tableau']));
    expect(result).toEqual([false, false, false, false]);
  });

  test('handles empty tag strings gracefully', () => {
    const result = getFilteredVisibility(['', 'python'], new Set(['python']));
    expect(result).toEqual([false, true]);
  });

  test('trims whitespace in tag strings', () => {
    const result = getFilteredVisibility(['python , etl'], new Set(['etl']));
    expect(result).toEqual([true]);
  });
});

describe('applyMaxVisible', () => {
  test('returns same array when max is null', () => {
    const vis = [true, false, true, true];
    expect(applyMaxVisible(vis, null)).toEqual([true, false, true, true]);
  });

  test('caps visible cards to max count', () => {
    const vis = [true, true, true, true, true];
    expect(applyMaxVisible(vis, 4)).toEqual([true, true, true, true, false]);
  });

  test('returns unchanged when fewer visible than max', () => {
    const vis = [true, false, true];
    expect(applyMaxVisible(vis, 4)).toEqual([true, false, true]);
  });

  test('handles max of 0', () => {
    const vis = [true, true, true];
    expect(applyMaxVisible(vis, 0)).toEqual([false, false, false]);
  });

  test('preserves order — first N visible win', () => {
    const vis = [false, true, false, true, true, true];
    expect(applyMaxVisible(vis, 2)).toEqual([false, true, false, true, false, false]);
  });
});

describe('getFeaturedVisibility', () => {
  test('returns true only for featured flags', () => {
    expect(getFeaturedVisibility([true, false, true, false])).toEqual([true, false, true, false]);
  });

  test('returns all false when no featured cards', () => {
    expect(getFeaturedVisibility([false, false, false])).toEqual([false, false, false]);
  });
});

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

describe('getFilterFromURL', () => {
  let originalHref;

  beforeEach(() => {
    originalHref = window.location.href;
  });

  afterEach(() => {
    window.history.replaceState({}, '', originalHref);
  });

  test('returns null when no filter param', () => {
    window.history.replaceState({}, '', '/');
    expect(getFilterFromURL()).toBeNull();
  });

  test('returns filter value from URL', () => {
    window.history.replaceState({}, '', '/?filter=python');
    expect(getFilterFromURL()).toBe('python');
  });

  test('returns null for empty filter param', () => {
    window.history.replaceState({}, '', '/?filter=');
    expect(getFilterFromURL()).toBeNull();
  });
});
