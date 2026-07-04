// @ts-check
/** Pure index math for wrap-around carousels (unit-tested). */

/**
 * @param {number} current
 * @param {number} length
 * @returns {number} next index, wrapping past the end back to 0.
 */
export const nextIndex = (current, length) => (current + 1) % length;

/**
 * @param {number} current
 * @param {number} length
 * @returns {number} previous index, wrapping before 0 to the end.
 */
export const prevIndex = (current, length) => (current - 1 + length) % length;

/**
 * Initials from a full name, max two letters.
 * @param {string} name
 * @returns {string}
 */
export const initials = (name) =>
  (name || '')
    .split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('');
