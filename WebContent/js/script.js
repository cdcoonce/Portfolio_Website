'use strict';

/* === Navigation — Hamburger Toggle === */

/**
 * Toggles mobile nav menu open/closed and syncs aria-expanded on the button.
 * Closes the menu when any nav link is clicked.
 */
document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
});

/* === Back to Top Button === */

/**
 * Shows the back-to-top button once the testimonials section scrolls into view.
 */
document.addEventListener('DOMContentLoaded', () => {
  const backToTop = document.querySelector('.back-to-top');
  const testimonials = document.querySelector('#testimonials');

  if (backToTop) {
    window.addEventListener('scroll', () => {
      const testimonialsTop = testimonials ? testimonials.getBoundingClientRect().top : Infinity;
      backToTop.classList.toggle('visible', testimonialsTop <= window.innerHeight);
    });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
});

/* === Scroll Down Button === */

/**
 * Hides the scroll-down arrow once the user has scrolled past the profile section.
 */
document.addEventListener('DOMContentLoaded', () => {
  const scrollDown = document.querySelector('.scroll-down');
  const profileSection = document.querySelector('#profile');

  if (scrollDown && profileSection) {
    window.addEventListener('scroll', () => {
      const profileBottom = profileSection.getBoundingClientRect().bottom;
      scrollDown.classList.toggle('hidden', profileBottom < 0);
    });

    scrollDown.addEventListener('click', () => {
      const skills = document.querySelector('#skills');
      const nav = document.querySelector('#main-nav');
      const navHeight = nav ? nav.offsetHeight : 0;
      window.scrollTo({ top: skills.offsetTop - navHeight, behavior: 'smooth' });
    });
  }
});

/* === Skills-as-Filter: Multi-Selectable Project Filter === */

/**
 * Wires the Skills & Tools section buttons as multi-select project filters.
 * Clicking a skill tag toggles that filter; "All Projects" resets to show all.
 * If all tags are deselected, reverts to showing all cards.
 */
document.addEventListener('DOMContentLoaded', () => {
  const skillTags = document.querySelectorAll('button.skill-tag[data-filter]');
  const resetButton = document.querySelector('button.skill-filter-reset');
  const cards = document.querySelectorAll('.project-card');
  const activeFilters = new Set();

  if (!skillTags.length || !cards.length) {
    console.warn('Skill filter buttons or project cards not found in DOM');
    return;
  }

  /**
   * Shows all project cards and marks the reset button as active.
   */
  function showAllCards() {
    activeFilters.clear();
    skillTags.forEach((t) => t.classList.remove('active'));
    if (resetButton) resetButton.classList.add('active');
    cards.forEach((card) => (card.style.display = 'block'));
  }

  /**
   * Filters project cards to those matching any active skill tag.
   */
  function applyFilters() {
    cards.forEach((card) => {
      const tags = card.getAttribute('data-tags') || '';
      const tagSet = new Set(
        tags
          .split(',')
          .map((t) => t.trim())
          .filter(Boolean)
      );
      const matches = Array.from(activeFilters).some((f) => tagSet.has(f));
      card.style.display = matches ? 'block' : 'none';
    });
  }

  skillTags.forEach((tag) => {
    tag.addEventListener('click', () => {
      const filterValue = tag.getAttribute('data-filter');

      if (resetButton) resetButton.classList.remove('active');

      if (tag.classList.contains('active')) {
        tag.classList.remove('active');
        activeFilters.delete(filterValue);
      } else {
        tag.classList.add('active');
        activeFilters.add(filterValue);
      }

      if (activeFilters.size === 0) {
        showAllCards();
      } else {
        applyFilters();
      }
    });
  });

  if (resetButton) {
    resetButton.addEventListener('click', showAllCards);
  }
});

/* === Testimonials Slider === */

// Configuration constants for testimonial carousel behavior
const CAROUSEL_CONFIG = {
  DESKTOP_BREAKPOINT: 1200, // px width where we show 2 testimonials instead of 1
  AUTO_SCROLL_INTERVAL_MS: 20000, // Auto-advance every 20 seconds
  TESTIMONIALS_DESKTOP: 2,
  TESTIMONIALS_MOBILE: 1,
};

/**
 * Initializes a responsive testimonial carousel with navigation controls.
 * On desktop (≥1200px), shows 2 testimonials; mobile shows 1.
 * Auto-scrolls every 20 seconds and provides prev/next buttons.
 */
document.addEventListener('DOMContentLoaded', () => {
  const testimonials = document.querySelectorAll('.testimonial');
  const prevButtonTestimonial = document.getElementById('prevRec');
  const nextButtonTestimonial = document.getElementById('nextRec');
  const dotsContainer = document.querySelector('.dots-container');

  // Guard: Ensure required DOM elements exist
  if (!testimonials.length || !prevButtonTestimonial || !nextButtonTestimonial || !dotsContainer) {
    console.warn('Testimonial carousel elements not found in DOM');
    return;
  }

  let carouselIndex = 0; // Current starting index for visible testimonials
  let testimonialsToShow = getTestimonialsToShow();

  /**
   * Determines how many testimonials to display based on viewport width.
   * @returns {number} Number of testimonials to show simultaneously
   */
  function getTestimonialsToShow() {
    return window.innerWidth >= CAROUSEL_CONFIG.DESKTOP_BREAKPOINT
      ? CAROUSEL_CONFIG.TESTIMONIALS_DESKTOP
      : CAROUSEL_CONFIG.TESTIMONIALS_MOBILE;
  }

  // Re-render carousel when viewport size changes
  window.addEventListener('resize', () => {
    testimonialsToShow = getTestimonialsToShow();
    showTestimonials(carouselIndex);
    createDots();
  });

  /**
   * Creates pagination dots representing carousel pages.
   * Desktop (2 per page): 1 dot per pair; Mobile: 1 dot per testimonial.
   */
  function createDots() {
    dotsContainer.innerHTML = '';
    const isDesktop = window.innerWidth > CAROUSEL_CONFIG.DESKTOP_BREAKPOINT;

    testimonials.forEach((_, index) => {
      // On desktop, only create dot for even indices (pairs); on mobile, all indices
      if (isDesktop && index % 2 !== 0) return;

      const dot = document.createElement('div');
      dot.classList.add('dot');
      if (index === 0) dot.classList.add('active');
      dotsContainer.appendChild(dot);
    });
  }

  /**
   * Updates dot active states to match current carousel position.
   */
  function updateDots() {
    const dots = document.querySelectorAll('.dot');
    const isDesktop = window.innerWidth > CAROUSEL_CONFIG.DESKTOP_BREAKPOINT;
    const activeDotIndex = isDesktop ? carouselIndex / 2 : carouselIndex;

    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === activeDotIndex);
    });
  }

  /**
   * Displays testimonials starting from the given index.
   * Activates opacity and 'active' class for visible testimonials only.
   * @param {number} startIndex - Starting index in testimonials array
   */
  function showTestimonials(startIndex) {
    testimonials.forEach((testimonial, i) => {
      const isVisible = i >= startIndex && i < startIndex + testimonialsToShow;
      testimonial.classList.toggle('active', isVisible);
      testimonial.style.opacity = isVisible ? '1' : '0';
    });
    updateDots();
  }

  /**
   * Advances carousel to next testimonial(s).
   * On desktop, advances by 2; on mobile, by 1. Wraps to start if at end.
   */
  function nextTestimonial() {
    const step = window.innerWidth > CAROUSEL_CONFIG.DESKTOP_BREAKPOINT ? 2 : 1;

    if (carouselIndex + testimonialsToShow < testimonials.length) {
      carouselIndex += step;
    } else {
      carouselIndex = 0; // Wrap to beginning
    }
    showTestimonials(carouselIndex);
  }

  /**
   * Moves carousel to previous testimonial(s).
   * On desktop, moves back by 2; on mobile, by 1. Wraps to end if at start.
   */
  function prevTestimonial() {
    const step = window.innerWidth > CAROUSEL_CONFIG.DESKTOP_BREAKPOINT ? 2 : 1;

    if (carouselIndex > 0) {
      carouselIndex -= step;
    } else {
      // Wrap to last visible set of testimonials
      carouselIndex = Math.max(0, testimonials.length - testimonialsToShow);
    }
    showTestimonials(carouselIndex);
  }

  // Attach event listeners to navigation buttons
  nextButtonTestimonial.addEventListener('click', nextTestimonial);
  prevButtonTestimonial.addEventListener('click', prevTestimonial);

  // Auto-scroll carousel, pausing when tab is not visible
  let autoScrollTimer = setInterval(autoScroll, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);

  function autoScroll() {
    if (carouselIndex + testimonialsToShow < testimonials.length) {
      nextTestimonial();
    } else {
      carouselIndex = 0;
      showTestimonials(carouselIndex);
    }
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      clearInterval(autoScrollTimer);
    } else {
      autoScrollTimer = setInterval(autoScroll, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);
    }
  });

  // Initialize carousel display
  showTestimonials(carouselIndex);
  createDots();
});
