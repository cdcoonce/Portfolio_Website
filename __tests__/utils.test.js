import { getItemsToShow, isDesktop, formatProjectDate } from '../WebContent/js/utils.js';

describe('getItemsToShow', () => {
  test('returns desktop count when viewport exceeds breakpoint', () => {
    expect(getItemsToShow(1400, 1200, 2, 1)).toBe(2);
  });

  test('returns desktop count at exactly the breakpoint', () => {
    expect(getItemsToShow(1200, 1200, 2, 1)).toBe(2);
  });

  test('returns mobile count below breakpoint', () => {
    expect(getItemsToShow(1199, 1200, 2, 1)).toBe(1);
  });
});

describe('isDesktop', () => {
  test('returns true at breakpoint', () => {
    expect(isDesktop(1200, 1200)).toBe(true);
  });

  test('returns false below breakpoint', () => {
    expect(isDesktop(1199, 1200)).toBe(false);
  });

  test('returns true above breakpoint', () => {
    expect(isDesktop(1400, 1200)).toBe(true);
  });
});

describe('formatProjectDate', () => {
  test('formats YYYY-MM to abbreviated month and year', () => {
    expect(formatProjectDate('2024-09')).toBe('Sep 2024');
  });

  test('formats January correctly', () => {
    expect(formatProjectDate('2025-01')).toBe('Jan 2025');
  });

  test('formats December correctly', () => {
    expect(formatProjectDate('2024-12')).toBe('Dec 2024');
  });

  test('returns empty string for undefined input', () => {
    expect(formatProjectDate(undefined)).toBe('');
  });

  test('returns empty string for empty string input', () => {
    expect(formatProjectDate('')).toBe('');
  });
});
