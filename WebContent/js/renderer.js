'use strict';

import { formatProjectDate } from './utils.js';

/**
 * Creates a project card DOM element from a project data object.
 *
 * @param {Object} project - Project data object
 * @param {string} project.id - Unique project identifier
 * @param {string} project.href - Link URL
 * @param {string} project.title - Project title
 * @param {string} project.date - Date in 'YYYY-MM' format
 * @param {string} project.description - Project description text
 * @param {string} project.image - Image source path
 * @param {string} project.imageAlt - Image alt text
 * @param {string[]} project.tags - Array of tag strings
 * @param {boolean} [project.featured] - Whether the project is featured
 * @param {boolean} [project.imageContain] - Whether the image uses contain sizing
 * @returns {HTMLAnchorElement} The constructed card element
 */
export function createProjectCard(project) {
  const card = document.createElement('a');
  card.href = project.href;
  card.target = '_blank';
  card.rel = 'noopener noreferrer';
  card.classList.add('project-card');

  if (project.featured === true) {
    card.classList.add('featured');
  }

  card.dataset.tags = project.tags.join(',');
  card.dataset.date = project.date;

  const img = document.createElement('img');
  img.src = project.image;
  img.alt = project.imageAlt;
  img.loading = 'lazy';
  img.width = 300;
  img.height = 200;

  if (project.imageContain === true) {
    img.classList.add('img--contain');
  }

  const content = document.createElement('div');
  content.classList.add('card-content');

  const heading = document.createElement('h3');
  heading.textContent = project.title;

  const dateSpan = document.createElement('span');
  dateSpan.classList.add('project-date');
  dateSpan.textContent = formatProjectDate(project.date);

  const desc = document.createElement('p');
  desc.textContent = project.description;

  content.appendChild(heading);
  content.appendChild(dateSpan);
  content.appendChild(desc);

  card.appendChild(img);
  card.appendChild(content);

  return card;
}

/**
 * Renders project cards into a container element.
 *
 * @param {HTMLElement} container - The DOM element to render cards into
 * @param {Object[]} projects - Array of project data objects
 */
export function renderProjectCards(container, projects) {
  container.innerHTML = '';

  for (const project of projects) {
    const card = createProjectCard(project);
    container.appendChild(card);
  }
}

/**
 * Converts a kebab-case tag to title case for display.
 *
 * @param {string} tag - Tag string (e.g. 'machine-learning')
 * @returns {string} Title-cased string (e.g. 'Machine Learning')
 */
function titleCase(tag) {
  return tag
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Creates a single filter button element.
 *
 * @param {string} tag - Tag identifier (e.g. 'python')
 * @param {Record<string, string>} labels - Tag-to-display-name mapping
 * @returns {HTMLButtonElement}
 */
function createFilterButton(tag, labels) {
  const button = document.createElement('button');
  button.classList.add('skill-tag');
  button.dataset.filter = tag;
  button.textContent = labels[tag] || titleCase(tag);
  return button;
}

/**
 * Renders a categorized filter grid into a container.
 *
 * Generates a `.skills-grid` with `.skill-category` groups, each containing
 * an h3 heading and `.skill-tags` wrapper with filter buttons. Tags present
 * in `allTags` but not assigned to any category are collected into an "Other"
 * catch-all group, ensuring every tag is filterable.
 *
 * @param {HTMLElement} container - The DOM element to render into
 * @param {string[]} allTags - Complete derived tag list (source of truth)
 * @param {Array<{name: string, tags: string[]}>} categories - Curated groupings
 * @param {Object} [options]
 * @param {Record<string, string>} [options.labels={}] - Tag-to-display-name mapping
 */
export function renderFilterButtons(container, allTags, categories, options = {}) {
  const { labels = {} } = options;
  container.innerHTML = '';

  const categorized = new Set(categories.flatMap((c) => c.tags));
  const uncategorized = allTags.filter((t) => !categorized.has(t));

  const allGroups =
    uncategorized.length > 0 ? [...categories, { name: 'Other', tags: uncategorized }] : categories;

  const grid = document.createElement('div');
  grid.classList.add('skills-grid');

  for (const category of allGroups) {
    const group = document.createElement('div');
    group.classList.add('skill-category');

    const heading = document.createElement('h3');
    heading.textContent = category.name;
    group.appendChild(heading);

    const tagsWrapper = document.createElement('div');
    tagsWrapper.classList.add('skill-tags');

    for (const tag of category.tags) {
      tagsWrapper.appendChild(createFilterButton(tag, labels));
    }

    group.appendChild(tagsWrapper);
    grid.appendChild(group);
  }

  container.appendChild(grid);
}
