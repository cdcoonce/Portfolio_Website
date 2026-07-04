import { WORK_FILTERS, matchesFilter, matchesQuery, filterProjects, countFor } from '../src/lib/work-filter.js';

const sample = [
  { title: 'Oura Pipeline', description: 'ELT into Snowflake', tags: ['Python', 'ETL/ELT', 'Data Pipelines'] },
  { title: 'Global CO2', description: 'Tableau dashboard', tags: ['Tableau', 'Analytics Dashboards'] },
  { title: 'Baby Names', description: 'SQL trends', tags: ['SQL', 'Statistical Analysis'] },
  { title: 'claude-workflow', description: 'plugin', tags: ['Python', 'AI Tooling'] },
];

describe('matchesFilter', () => {
  test('all bucket matches every project', () => {
    expect(sample.every((p) => matchesFilter(p, 'all'))).toBe(true);
  });

  test('unknown filter key falls back to all', () => {
    expect(matchesFilter(sample[0], 'nonexistent')).toBe(true);
  });

  test('category matches on any overlapping tag', () => {
    expect(matchesFilter(sample[0], 'pipelines')).toBe(true);
    expect(matchesFilter(sample[1], 'pipelines')).toBe(false);
  });

  test('dashboards category includes Tableau and BI', () => {
    expect(matchesFilter(sample[1], 'dashboards')).toBe(true);
  });
});

describe('matchesQuery', () => {
  test('empty query matches everything', () => {
    expect(matchesQuery(sample[0], '   ')).toBe(true);
  });

  test('matches against title, description, and tags', () => {
    expect(matchesQuery(sample[0], 'snowflake')).toBe(true); // description
    expect(matchesQuery(sample[2], 'baby')).toBe(true); // title
    expect(matchesQuery(sample[1], 'tableau')).toBe(true); // tag
    expect(matchesQuery(sample[1], 'python')).toBe(false);
  });
});

describe('filterProjects', () => {
  test('combines category and query (AND)', () => {
    const out = filterProjects(sample, { filter: 'python', query: 'plugin' });
    expect(out.map((p) => p.title)).toEqual(['claude-workflow']);
  });

  test('default state returns the full gallery', () => {
    expect(filterProjects(sample)).toHaveLength(sample.length);
  });
});

describe('countFor', () => {
  test('all counts the whole gallery', () => {
    expect(countFor(sample, 'all')).toBe(4);
  });

  test('python counts only python-tagged projects', () => {
    expect(countFor(sample, 'python')).toBe(2);
  });

  test('every rail category is countable', () => {
    for (const f of WORK_FILTERS) {
      expect(typeof countFor(sample, f.key)).toBe('number');
    }
  });
});
