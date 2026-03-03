'use strict';

/**
 * Determines how many items to show based on viewport width and a breakpoint.
 * @param {number} viewportWidth - Current viewport width in pixels
 * @param {number} breakpoint - Width threshold for desktop layout
 * @param {number} desktopCount - Items to show on desktop
 * @param {number} mobileCount - Items to show on mobile
 * @returns {number}
 */
export const getItemsToShow = (viewportWidth, breakpoint, desktopCount, mobileCount) =>
  viewportWidth >= breakpoint ? desktopCount : mobileCount;

/**
 * Checks whether a viewport width qualifies as desktop.
 * @param {number} viewportWidth
 * @param {number} breakpoint
 * @returns {boolean}
 */
export const isDesktop = (viewportWidth, breakpoint) => viewportWidth >= breakpoint;
