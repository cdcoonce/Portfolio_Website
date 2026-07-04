// @ts-check
/** Pure selection of featured projects for the Overview spotlight carousel. */

/**
 * Featured projects, in source order (the first entry is the default slide).
 * @param {import('../data/portfolio.js').Project[]} all
 * @returns {import('../data/portfolio.js').Project[]}
 */
export const featuredProjects = (all) => all.filter((p) => p.featured);
