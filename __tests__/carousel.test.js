import {
  CAROUSEL_CONFIG,
  getNextIndex,
  getPrevIndex,
  getDotCount,
  getActiveDotIndex,
  getCounterText,
} from '../WebContent/js/carousel.js';

describe('CAROUSEL_CONFIG', () => {
  test('DESKTOP_BREAKPOINT matches CSS media query (1250px)', () => {
    expect(CAROUSEL_CONFIG.DESKTOP_BREAKPOINT).toBe(1250);
  });
});

describe('getNextIndex', () => {
  test('advances by step when not at end', () => {
    expect(getNextIndex(0, 1, 7, 1)).toBe(1);
  });

  test('advances by 2 on desktop', () => {
    expect(getNextIndex(0, 2, 7, 2)).toBe(2);
  });

  test('wraps to 0 when at end (mobile)', () => {
    expect(getNextIndex(6, 1, 7, 1)).toBe(0);
  });

  test('wraps to 0 when at end (desktop, 2-up)', () => {
    expect(getNextIndex(6, 2, 7, 2)).toBe(0);
  });

  test('advances when space remains for partial view', () => {
    expect(getNextIndex(4, 2, 7, 2)).toBe(6);
  });
});

describe('getPrevIndex', () => {
  test('goes back by step when not at start', () => {
    expect(getPrevIndex(3, 1, 7, 1)).toBe(2);
  });

  test('wraps to last set when at start (mobile)', () => {
    expect(getPrevIndex(0, 1, 7, 1)).toBe(6);
  });

  test('wraps to last set when at start (desktop)', () => {
    expect(getPrevIndex(0, 2, 7, 2)).toBe(5);
  });
});

describe('getDotCount', () => {
  test('returns total items on mobile', () => {
    expect(getDotCount(7, false)).toBe(7);
  });

  test('returns half (rounded up) on desktop', () => {
    expect(getDotCount(7, true)).toBe(4);
  });

  test('returns exact half for even count on desktop', () => {
    expect(getDotCount(6, true)).toBe(3);
  });
});

describe('getActiveDotIndex', () => {
  test('returns carousel index on mobile', () => {
    expect(getActiveDotIndex(3, false)).toBe(3);
  });

  test('returns halved index on desktop', () => {
    expect(getActiveDotIndex(4, true)).toBe(2);
  });

  test('returns 0 for first position on desktop', () => {
    expect(getActiveDotIndex(0, true)).toBe(0);
  });
});

describe('getCounterText', () => {
  test('returns "1 / 7" for first item mobile', () => {
    expect(getCounterText(0, 1, 7)).toBe('1 / 7');
  });

  test('returns "1 / 4" for first pair desktop', () => {
    expect(getCounterText(0, 2, 7)).toBe('1 / 4');
  });

  test('returns "4 / 4" for last pair desktop', () => {
    expect(getCounterText(6, 2, 7)).toBe('4 / 4');
  });
});
