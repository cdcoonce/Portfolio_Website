'use strict';

import { getItemsToShow, isDesktop } from './utils.js';

/** Configuration constants for testimonial carousel behavior */
export const CAROUSEL_CONFIG = {
  DESKTOP_BREAKPOINT: 1250, // Must match mediaqueries.css @media breakpoint
  AUTO_SCROLL_INTERVAL_MS: 20000,
  TESTIMONIALS_DESKTOP: 2,
  TESTIMONIALS_MOBILE: 1,
};

/**
 * Calculates the next carousel index with wraparound.
 * @param {number} currentIndex - Current starting index
 * @param {number} step - Number of items to advance
 * @param {number} totalItems - Total testimonial count
 * @param {number} itemsToShow - Items visible at once
 * @returns {number} New index
 */
export const getNextIndex = (currentIndex, step, totalItems, itemsToShow) => {
  if (currentIndex + itemsToShow < totalItems) {
    return currentIndex + step;
  }
  return 0;
};

/**
 * Calculates the previous carousel index with wraparound.
 * @param {number} currentIndex - Current starting index
 * @param {number} step - Number of items to go back
 * @param {number} totalItems - Total testimonial count
 * @param {number} itemsToShow - Items visible at once
 * @returns {number} New index
 */
export const getPrevIndex = (currentIndex, step, totalItems, itemsToShow) => {
  if (currentIndex > 0) {
    return currentIndex - step;
  }
  return Math.max(0, totalItems - itemsToShow);
};

/**
 * Calculates the number of pagination dots needed.
 * @param {number} totalItems - Total testimonial count
 * @param {boolean} desktop - Whether in desktop mode
 * @returns {number} Number of dots
 */
export const getDotCount = (totalItems, desktop) => {
  return desktop ? Math.ceil(totalItems / 2) : totalItems;
};

/**
 * Determines which dot index should be active.
 * @param {number} carouselIndex - Current carousel position
 * @param {boolean} desktop - Whether in desktop mode
 * @returns {number} Active dot index
 */
export const getActiveDotIndex = (carouselIndex, desktop) => {
  return desktop ? Math.floor(carouselIndex / 2) : carouselIndex;
};

/**
 * Returns the counter display string (e.g. "1 / 4").
 * @param {number} startIndex - Current starting index
 * @param {number} itemsToShow - Items visible at once
 * @param {number} totalItems - Total testimonial count
 * @returns {string}
 */
export const getCounterText = (startIndex, itemsToShow, totalItems) => {
  const current = Math.floor(startIndex / itemsToShow) + 1;
  const total = Math.ceil(totalItems / itemsToShow);
  return `${current} / ${total}`;
};

/**
 * Initializes the testimonial carousel with navigation, dots, and auto-scroll.
 */
export function initCarousel() {
  const testimonials = document.querySelectorAll('.testimonial');
  const prevButton = document.getElementById('prevRec');
  const nextButton = document.getElementById('nextRec');
  const dotsContainer = document.querySelector('.dots-container');

  if (!testimonials.length || !prevButton || !nextButton || !dotsContainer) {
    console.warn('Testimonial carousel elements not found in DOM');
    return;
  }

  const totalItems = testimonials.length;
  let carouselIndex = 0;

  function currentItemsToShow() {
    return getItemsToShow(
      window.innerWidth,
      CAROUSEL_CONFIG.DESKTOP_BREAKPOINT,
      CAROUSEL_CONFIG.TESTIMONIALS_DESKTOP,
      CAROUSEL_CONFIG.TESTIMONIALS_MOBILE
    );
  }

  function currentIsDesktop() {
    return isDesktop(window.innerWidth, CAROUSEL_CONFIG.DESKTOP_BREAKPOINT);
  }

  function showTestimonials(startIndex) {
    const itemsToShow = currentItemsToShow();
    testimonials.forEach((testimonial, i) => {
      const isVisible = i >= startIndex && i < startIndex + itemsToShow;
      testimonial.classList.toggle('active', isVisible);
      testimonial.style.opacity = isVisible ? '1' : '0';
    });
    updateDots();
    updateCounter(startIndex);
  }

  function createDots() {
    dotsContainer.innerHTML = '';
    const desktop = currentIsDesktop();
    const count = getDotCount(totalItems, desktop);

    for (let i = 0; i < count; i++) {
      const dot = document.createElement('div');
      dot.classList.add('dot');
      if (i === 0) dot.classList.add('active');
      const targetIndex = desktop ? i * 2 : i;
      dot.addEventListener('click', () => {
        carouselIndex = targetIndex;
        showTestimonials(carouselIndex);
      });
      dotsContainer.appendChild(dot);
    }
  }

  function updateDots() {
    const dots = document.querySelectorAll('.dot');
    const activeIndex = getActiveDotIndex(carouselIndex, currentIsDesktop());
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === activeIndex);
    });
  }

  function updateCounter(startIndex) {
    const counter = document.querySelector('.testimonial-counter');
    if (counter) {
      counter.textContent = getCounterText(startIndex, currentItemsToShow(), totalItems);
    }
  }

  function nextTestimonial() {
    const step = currentItemsToShow();
    carouselIndex = getNextIndex(carouselIndex, step, totalItems, currentItemsToShow());
    showTestimonials(carouselIndex);
  }

  function prevTestimonial() {
    const step = currentItemsToShow();
    carouselIndex = getPrevIndex(carouselIndex, step, totalItems, currentItemsToShow());
    showTestimonials(carouselIndex);
  }

  // Navigation buttons
  nextButton.addEventListener('click', nextTestimonial);
  prevButton.addEventListener('click', prevTestimonial);

  // Auto-scroll (Issue #16 — removed trivial autoScroll wrapper)
  let autoScrollTimer = setInterval(nextTestimonial, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      clearInterval(autoScrollTimer);
    } else {
      autoScrollTimer = setInterval(nextTestimonial, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);
    }
  });

  // Responsive resize
  window.addEventListener('resize', () => {
    showTestimonials(carouselIndex);
    createDots();
  });

  // Create counter element
  const counter = document.createElement('p');
  counter.classList.add('testimonial-counter');
  dotsContainer.insertAdjacentElement('afterend', counter);

  // Initial render
  createDots();
  showTestimonials(carouselIndex);
}
