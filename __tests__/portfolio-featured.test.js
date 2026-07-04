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

describe('WAGA card links', () => {
  const waga = projects.find((p) => p.slug === 'waga');

  test('exposes both a Dashboard and a Repository link', () => {
    expect(waga).toBeDefined();
    expect(waga.links).toEqual([
      { label: 'View Dashboard', href: 'https://waga-dashboard.pages.dev' },
      {
        label: 'View Repository',
        href: 'https://github.com/cdcoonce/Weather-Adjusted-Generation-Analytics',
      },
    ]);
  });

  test('every link is an absolute URL', () => {
    for (const link of waga.links) {
      expect(link.href).toMatch(/^https?:\/\//);
    }
  });
});
