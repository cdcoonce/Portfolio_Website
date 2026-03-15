import { projects } from '../WebContent/js/projects.js';

describe('projects data', () => {
  test('exports a non-empty array', () => {
    expect(Array.isArray(projects)).toBe(true);
    expect(projects.length).toBeGreaterThan(0);
  });

  const requiredFields = [
    ['id', 'string'],
    ['href', 'string'],
    ['title', 'string'],
    ['date', 'string'],
    ['description', 'string'],
    ['image', 'string'],
    ['imageAlt', 'string'],
  ];

  test.each(requiredFields)('every project has a %s field of type %s', (field, type) => {
    for (const project of projects) {
      expect(typeof project[field]).toBe(type);
    }
  });

  test('every project date matches YYYY-MM format', () => {
    for (const project of projects) {
      expect(project.date).toMatch(/^\d{4}-\d{2}$/);
    }
  });

  test('every project has a non-empty tags array of strings', () => {
    for (const project of projects) {
      expect(Array.isArray(project.tags)).toBe(true);
      expect(project.tags.length).toBeGreaterThan(0);
      for (const tag of project.tags) {
        expect(typeof tag).toBe('string');
      }
    }
  });

  test('no duplicate id values', () => {
    const ids = projects.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  test('featured, when present, is true', () => {
    for (const project of projects) {
      if ('featured' in project) {
        expect(project.featured).toBe(true);
      }
    }
  });

  test('imageContain, when present, is true', () => {
    for (const project of projects) {
      if ('imageContain' in project) {
        expect(project.imageContain).toBe(true);
      }
    }
  });
});
