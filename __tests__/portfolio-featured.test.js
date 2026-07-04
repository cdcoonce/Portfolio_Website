'use strict';

import { projects } from '../src/data/portfolio.js';
import { featuredProjects } from '../src/lib/featured.js';

describe('featuredProjects', () => {
  test('returns only projects flagged featured', () => {
    const result = featuredProjects(projects);
    expect(result.length).toBeGreaterThan(1);
    expect(result.every((p) => p.featured)).toBe(true);
  });

  test('keeps AFK as the first (default) slide', () => {
    expect(featuredProjects(projects)[0].title).toMatch(/^AFK/);
  });

  test('filters strictly on the featured flag', () => {
    const sample = [{ featured: false }, { featured: true }, {}];
    expect(featuredProjects(sample)).toEqual([{ featured: true }]);
  });
});
