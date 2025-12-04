/* === Multi-Selectable Projects Keyword Filter with "All" Logic === */

/**
 * Initializes project filter UI allowing multi-select tag filtering.
 * Selecting "All" clears other filters; selecting none reverts to "All".
 * Cards are shown/hidden based on whether their data-tags match any active filter.
 */
document.addEventListener('DOMContentLoaded', () => {
  const filters = document.querySelectorAll('.projects-filter .filter');
  const cards = document.querySelectorAll('.project-card');
  const activeFilters = new Set();

  // Guard: Ensure DOM elements exist before proceeding
  if (!filters.length || !cards.length) {
    console.warn('Project filters or cards not found in DOM');
    return;
  }

  filters.forEach((filter) => {
    filter.addEventListener('click', () => {
      const filterValue = filter.getAttribute('data-filter');

      if (filterValue === 'all') {
        // "All" selected: clear other filters and show all cards
        activeFilters.clear();
        filters.forEach((f) => f.classList.remove('active'));
        filter.classList.add('active');
        cards.forEach((card) => (card.style.display = 'block'));
      } else {
        const allFilter = document.querySelector('[data-filter="all"]');
        if (allFilter) allFilter.classList.remove('active');

        // Toggle the clicked filter's active state
        if (filter.classList.contains('active')) {
          filter.classList.remove('active');
          activeFilters.delete(filterValue);
        } else {
          filter.classList.add('active');
          activeFilters.add(filterValue);
        }

        // If no filters remain active, revert to showing all
        if (activeFilters.size === 0) {
          if (allFilter) allFilter.classList.add('active');
          cards.forEach((card) => (card.style.display = 'block'));
        } else {
          // Show only cards matching at least one active filter (OR logic)
          cards.forEach((card) => {
            const tags = card.getAttribute('data-tags') || '';
            const matches = Array.from(activeFilters).some((filter) => tags.includes(filter));
            card.style.display = matches ? 'block' : 'none';
          });
        }
      }
    });
  });
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

  // Auto-scroll carousel at configured interval
  setInterval(() => {
    if (carouselIndex + testimonialsToShow < testimonials.length) {
      nextTestimonial();
    } else {
      carouselIndex = 0;
      showTestimonials(carouselIndex);
    }
  }, CAROUSEL_CONFIG.AUTO_SCROLL_INTERVAL_MS);

  // Initialize carousel display
  showTestimonials(carouselIndex);
  createDots();
});
