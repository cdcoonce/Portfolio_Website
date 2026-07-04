'use strict';

import { initials, nextIndex, prevIndex } from '../src/lib/carousel.js';

describe('carousel index math', () => {
  test('nextIndex advances and wraps past the end to 0', () => {
    expect(nextIndex(0, 4)).toBe(1);
    expect(nextIndex(2, 4)).toBe(3);
    expect(nextIndex(3, 4)).toBe(0);
  });

  test('prevIndex retreats and wraps before 0 to the end', () => {
    expect(prevIndex(3, 4)).toBe(2);
    expect(prevIndex(1, 4)).toBe(0);
    expect(prevIndex(0, 4)).toBe(3);
  });

  test('single-item carousel always stays on index 0', () => {
    expect(nextIndex(0, 1)).toBe(0);
    expect(prevIndex(0, 1)).toBe(0);
  });
});

describe('initials', () => {
  test('takes up to two leading initials', () => {
    expect(initials('Aaron Wallen')).toBe('AW');
    expect(initials('Katie Marks')).toBe('KM');
  });

  test('handles single names and empty input', () => {
    expect(initials('Cher')).toBe('C');
    expect(initials('')).toBe('');
  });
});
