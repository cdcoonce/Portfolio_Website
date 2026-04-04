import { projects, tags, TAG_LABELS } from '../WebContent/js/projects.js';

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
