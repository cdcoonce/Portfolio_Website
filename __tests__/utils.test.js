import { getItemsToShow, isDesktop } from '../WebContent/js/utils.js';

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
