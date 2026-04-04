'use strict';

/**
 * Determines which project cards should be visible given the active filter set.
 * @param {string[]} cardTagSets - Array of comma-separated tag strings (one per card)
 * @param {Set<string>} activeFilters - Currently active filter values
 * @returns {boolean[]} - Array of visibility flags, one per card
 */
export const getFilteredVisibility = (cardTagSets, activeFilters) => {
  if (activeFilters.size === 0) {
    return cardTagSets.map(() => true);
  }
  return cardTagSets.map((tags) => {
    const tagSet = new Set(
      tags
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean)
    );
    return Array.from(activeFilters).some((f) => tagSet.has(f));
  });
};

/**
 * Caps visible cards to a maximum count.
 * @param {boolean[]} visibility - Array of visibility flags
 * @param {number|null} max - Maximum visible cards, or null for unlimited
 * @returns {boolean[]} New array with at most max true values
 */
export const applyMaxVisible = (visibility, max) => {
  if (max === null || max === undefined) return visibility;
  let count = 0;
  return visibility.map((v) => {
    if (v && count < max) {
      count++;
      return true;
    }
    return false;
  });
};

/**
 * Returns visibility based on featured status.
 * @param {boolean[]} featuredFlags - Array of booleans (true if card has featured class)
 * @returns {boolean[]}
 */
export const getFeaturedVisibility = (featuredFlags) => {
  return featuredFlags.map((f) => f);
};

/**
 * Reads the filter query parameter from the current URL.
 * @returns {string|null} The filter value, or null if not present
 */
export const getFilterFromURL = () => {
  const params = new URLSearchParams(window.location.search);
  return params.get('filter') || null;
};

/**
 * Returns indices that would sort dates newest-first, with missing dates at the end.
 * @param {string[]} dates - Array of date strings (e.g. '2024-01')
 * @returns {number[]} Array of original indices in sorted order
 */
export const getSortedIndices = (dates) => {
  return dates
    .map((date, index) => ({ date: date || '0000-00', index }))
    .sort((a, b) => {
      const cmp = b.date.localeCompare(a.date);
      return cmp !== 0 ? cmp : a.index - b.index;
    })
    .map(({ index }) => index);
};

/**
 * Wires filter buttons and reset button to project card visibility.
 * @param {Object} [config]
 * @param {number|null} [config.maxVisible=null] - Max cards to show (null = unlimited)
 * @param {string} [config.defaultFilter='all'] - Default filter: 'all' or 'featured'
 * @param {string|null} [config.initialFilter=null] - Pre-selected filter from URL param
 * @param {Set<string>|null} [config.knownTags=null] - Known tag registry; warns if a filter button uses an unknown tag
 */
export function initFilter(config = {}) {
  const {
    maxVisible = null,
    defaultFilter = 'all',
    initialFilter = null,
    knownTags = null,
  } = config;

  const skillTags = document.querySelectorAll('button.skill-tag[data-filter]');
  const resetButton = document.querySelector('button.skill-filter-reset');
  let cards = document.querySelectorAll('.project-card');
  const activeFilters = new Set();

  if (!skillTags.length || !cards.length) {
    console.warn('Skill filter buttons or project cards not found in DOM');
    return;
  }

  // Warn about filter buttons whose data-filter value is not in the known tag registry
  if (knownTags) {
    for (const tag of skillTags) {
      const filterValue = tag.getAttribute('data-filter');
      if (!knownTags.has(filterValue)) {
        console.warn(
          `Filter button "${filterValue}" is not in knownTags — no project uses this tag`
        );
      }
    }
  }

  // Sort cards by date (newest first)
  const dates = Array.from(cards).map((c) => c.getAttribute('data-date') || '');
  const sortedIndices = getSortedIndices(dates);
  const grid = cards[0]?.parentElement;
  if (grid) {
    sortedIndices.forEach((i) => grid.appendChild(cards[i]));
  }
  // Re-query after reorder
  cards = document.querySelectorAll('.project-card');

  const cardTagSets = Array.from(cards).map((c) => {
    let tags = c.getAttribute('data-tags') || '';
    if (c.classList.contains('featured')) {
      tags = tags ? `${tags},featured` : 'featured';
    }
    return tags;
  });
  const featuredFlags = Array.from(cards).map((c) => c.classList.contains('featured'));

  function updateViewAllLink() {
    const viewAllLink = document.querySelector('.view-all-link');
    if (!viewAllLink) return;
    if (activeFilters.size === 1) {
      const filter = Array.from(activeFilters)[0];
      viewAllLink.href = `./projects.html?filter=${encodeURIComponent(filter)}`;
    } else {
      viewAllLink.href = './projects.html';
    }
  }

  function render() {
    let visibility;
    if (activeFilters.size === 0 && defaultFilter === 'featured') {
      visibility = getFeaturedVisibility(featuredFlags);
    } else if (activeFilters.size === 0) {
      visibility = cardTagSets.map(() => true);
    } else {
      visibility = getFilteredVisibility(cardTagSets, activeFilters);
    }
    visibility = applyMaxVisible(visibility, maxVisible);
    cards.forEach((card, i) => {
      card.style.display = visibility[i] ? 'flex' : 'none';
    });
    updateViewAllLink();
  }

  function showDefault() {
    activeFilters.clear();
    skillTags.forEach((t) => t.classList.remove('active'));
    if (resetButton) resetButton.classList.add('active');
    render();
  }

  skillTags.forEach((tag) => {
    tag.addEventListener('click', () => {
      const filterValue = tag.getAttribute('data-filter');
      const wasActive = tag.classList.contains('active');

      // Clear all active states (single-select)
      if (resetButton) resetButton.classList.remove('active');
      skillTags.forEach((t) => t.classList.remove('active'));
      activeFilters.clear();

      if (wasActive) {
        // Clicking the same filter again deselects it → return to default
        showDefault();
      } else {
        tag.classList.add('active');
        activeFilters.add(filterValue);
        render();
      }
    });
  });

  if (resetButton) {
    resetButton.addEventListener('click', showDefault);
  }

  if (initialFilter) {
    const matchingTag = Array.from(skillTags).find(
      (t) => t.getAttribute('data-filter') === initialFilter
    );
    if (matchingTag) {
      matchingTag.click();
    }
  } else {
    render();
  }
}
