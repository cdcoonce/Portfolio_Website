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
