import { getFilteredVisibility } from '../WebContent/js/filter.js';

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
