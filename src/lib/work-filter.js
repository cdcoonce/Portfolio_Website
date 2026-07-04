// @ts-check
/**
 * Pure work-gallery filtering: category definitions + tag/keyword matching.
 * Kept side-effect free so the Work tab's view layer stays a thin wrapper and
 * the logic is unit-testable in isolation.
 */

/** @typedef {import('../data/portfolio.js').Project} Project */

/**
 * Category rail for the Work tab. `tags` is the set of project tags that map to
 * the category; an empty set (the `all` bucket) matches everything.
 * @type {{ key: string, label: string, tags: string[] }[]}
 */
export const WORK_FILTERS = [
  { key: 'all', label: 'All', tags: [] },
  { key: 'python', label: 'Python', tags: ['Python'] },
  { key: 'sql-excel', label: 'SQL & Excel', tags: ['SQL', 'Excel'] },
  { key: 'r', label: 'R & Shiny', tags: ['R', 'Shiny'] },
  {
    key: 'dashboards',
    label: 'Dashboards & BI',
    tags: ['Analytics Dashboards', 'Tableau', 'Business Intelligence'],
  },
  { key: 'pipelines', label: 'Pipelines', tags: ['Data Pipelines', 'ETL/ELT'] },
  { key: 'ml', label: 'Machine Learning', tags: ['Machine Learning'] },
  { key: 'ai', label: 'AI Tooling', tags: ['AI Tooling'] },
];

/**
 * Whether a project belongs to a category. Unknown keys and `all` match all.
 * @param {Project} project
 * @param {string} filterKey
 * @returns {boolean}
 */
export const matchesFilter = (project, filterKey) => {
  const def = WORK_FILTERS.find((f) => f.key === filterKey) ?? WORK_FILTERS[0];
  if (def.tags.length === 0) return true;
  return project.tags.some((t) => def.tags.includes(t));
};

/**
 * Whether a project matches a free-text query across title, description, tags.
 * An empty/whitespace query matches everything.
 * @param {Project} project
 * @param {string} query
 * @returns {boolean}
 */
export const matchesQuery = (project, query) => {
  const q = (query || '').trim().toLowerCase();
  if (!q) return true;
  const haystack =
    `${project.title} ${project.description} ${project.tags.join(' ')}`.toLowerCase();
  return haystack.includes(q);
};

/**
 * Apply the active category and search query to the gallery.
 * @param {Project[]} gallery
 * @param {{ filter?: string, query?: string }} [state]
 * @returns {Project[]}
 */
export const filterProjects = (gallery, { filter = 'all', query = '' } = {}) =>
  gallery.filter((p) => matchesFilter(p, filter) && matchesQuery(p, query));

/**
 * Count of projects in a category (ignores the search query).
 * @param {Project[]} gallery
 * @param {string} filterKey
 * @returns {number}
 */
export const countFor = (gallery, filterKey) =>
  gallery.filter((p) => matchesFilter(p, filterKey)).length;
