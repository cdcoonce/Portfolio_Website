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
 * Wires filter buttons and reset button to project card visibility.
 */
export function initFilter() {
  const skillTags = document.querySelectorAll('button.skill-tag[data-filter]');
  const resetButton = document.querySelector('button.skill-filter-reset');
  const cards = document.querySelectorAll('.project-card');
  const activeFilters = new Set();

  if (!skillTags.length || !cards.length) {
    console.warn('Skill filter buttons or project cards not found in DOM');
    return;
  }

  const cardTagSets = Array.from(cards).map((c) => c.getAttribute('data-tags') || '');

  function render() {
    const visibility = getFilteredVisibility(cardTagSets, activeFilters);
    cards.forEach((card, i) => {
      card.style.display = visibility[i] ? 'flex' : 'none';
    });
  }

  function showAll() {
    activeFilters.clear();
    skillTags.forEach((t) => t.classList.remove('active'));
    if (resetButton) resetButton.classList.add('active');
    render();
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
        showAll();
      } else {
        render();
      }
    });
  });

  if (resetButton) {
    resetButton.addEventListener('click', showAll);
  }
}
