import { projects, tags, TAG_LABELS, TAG_CATEGORIES } from '../WebContent/js/projects.js';

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

describe('tags derived registry', () => {
  test('tags is a sorted array', () => {
    expect(Array.isArray(tags)).toBe(true);
    const sorted = [...tags].sort();
    expect(tags).toEqual(sorted);
  });

  test('tags contains only unique values', () => {
    expect(new Set(tags).size).toBe(tags.length);
  });

  test('every project tag appears in the tags registry', () => {
    const allProjectTags = projects.flatMap((p) => p.tags);
    for (const tag of allProjectTags) {
      expect(tags).toContain(tag);
    }
  });

  test('tags contains no values absent from all projects', () => {
    const allProjectTags = new Set(projects.flatMap((p) => p.tags));
    for (const tag of tags) {
      expect(allProjectTags.has(tag)).toBe(true);
    }
  });
});

describe('TAG_LABELS', () => {
  test('is a plain object', () => {
    expect(typeof TAG_LABELS).toBe('object');
    expect(TAG_LABELS).not.toBeNull();
  });

  test('every key in TAG_LABELS exists in tags', () => {
    for (const key of Object.keys(TAG_LABELS)) {
      expect(tags).toContain(key);
    }
  });

  test('maps multi-word or abbreviated tags to readable labels', () => {
    expect(TAG_LABELS['etl']).toBe('ETL/ELT');
    expect(TAG_LABELS['machine-learning']).toBe('Machine Learning');
    expect(TAG_LABELS['r']).toBe('R');
    expect(TAG_LABELS['sql']).toBe('SQL');
    expect(TAG_LABELS['html']).toBe('HTML');
    expect(TAG_LABELS['css']).toBe('CSS');
  });
});

describe('TAG_CATEGORIES', () => {
  test('is a non-empty array of category objects', () => {
    expect(Array.isArray(TAG_CATEGORIES)).toBe(true);
    expect(TAG_CATEGORIES.length).toBeGreaterThan(0);
  });

  test('every category has a name and a non-empty tags array', () => {
    for (const category of TAG_CATEGORIES) {
      expect(typeof category.name).toBe('string');
      expect(category.name.length).toBeGreaterThan(0);
      expect(Array.isArray(category.tags)).toBe(true);
      expect(category.tags.length).toBeGreaterThan(0);
    }
  });

  test('every categorized tag exists in the derived tags registry', () => {
    const allCategorized = TAG_CATEGORIES.flatMap((c) => c.tags);
    for (const tag of allCategorized) {
      expect(tags).toContain(tag);
    }
  });

  test('no tag appears in multiple categories', () => {
    const seen = new Set();
    for (const category of TAG_CATEGORIES) {
      for (const tag of category.tags) {
        expect(seen.has(tag)).toBe(false);
        seen.add(tag);
      }
    }
  });

  test('warns when tags exist that are not in any category (catch-all coverage)', () => {
    const categorized = new Set(TAG_CATEGORIES.flatMap((c) => c.tags));
    const uncategorized = tags.filter((t) => !categorized.has(t));
    if (uncategorized.length > 0) {
      console.warn(
        `Uncategorized tags will appear in "Other": ${uncategorized.join(', ')}. ` +
          'Consider adding them to TAG_CATEGORIES.'
      );
    }
    // This test always passes — it's a dev-time nudge, not a gate.
    // The catch-all in renderFilterButtons ensures they're still filterable.
    expect(true).toBe(true);
  });
});
