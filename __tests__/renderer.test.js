import { createProjectCard, renderProjectCards } from '../WebContent/js/renderer.js';

const sampleProject = {
  id: 'test-project',
  href: 'https://example.com',
  title: 'Test Project',
  date: '2024-09',
  description: 'A test project description.',
  image: './assets/test.png',
  imageAlt: 'Test Image',
  tags: ['python', 'etl'],
};

const featuredProject = {
  ...sampleProject,
  id: 'featured-project',
  featured: true,
  imageContain: true,
};

describe('createProjectCard', () => {
  test('returns an <a> element', () => {
    const card = createProjectCard(sampleProject);
    expect(card.tagName).toBe('A');
  });

  test('has class project-card', () => {
    const card = createProjectCard(sampleProject);
    expect(card.classList.contains('project-card')).toBe(true);
  });

  test('featured project gets featured class', () => {
    const card = createProjectCard(featuredProject);
    expect(card.classList.contains('featured')).toBe(true);
  });

  test('non-featured project does not get featured class', () => {
    const card = createProjectCard(sampleProject);
    expect(card.classList.contains('featured')).toBe(false);
  });

  test('data-tags is comma-joined tags', () => {
    const card = createProjectCard(sampleProject);
    expect(card.dataset.tags).toBe('python,etl');
  });

  test('data-date matches project date', () => {
    const card = createProjectCard(sampleProject);
    expect(card.dataset.date).toBe('2024-09');
  });

  test('href, target, and rel are set correctly', () => {
    const card = createProjectCard(sampleProject);
    expect(card.href).toBe('https://example.com/');
    expect(card.target).toBe('_blank');
    expect(card.rel).toBe('noopener noreferrer');
  });

  test('image has correct src, alt, loading, width, and height', () => {
    const card = createProjectCard(sampleProject);
    const img = card.querySelector('img');
    expect(img.getAttribute('src')).toBe('./assets/test.png');
    expect(img.alt).toBe('Test Image');
    expect(img.loading).toBe('lazy');
    expect(img.width).toBe(300);
    expect(img.height).toBe(200);
  });

  test('image gets img--contain when imageContain is true', () => {
    const card = createProjectCard(featuredProject);
    const img = card.querySelector('img');
    expect(img.classList.contains('img--contain')).toBe(true);
  });

  test('image does not get img--contain when imageContain is absent', () => {
    const card = createProjectCard(sampleProject);
    const img = card.querySelector('img');
    expect(img.classList.contains('img--contain')).toBe(false);
  });

  test('card content has <h3> with title', () => {
    const card = createProjectCard(sampleProject);
    const h3 = card.querySelector('.card-content h3');
    expect(h3).not.toBeNull();
    expect(h3.textContent).toBe('Test Project');
  });

  test('card content has <span class="project-date"> with formatted date', () => {
    const card = createProjectCard(sampleProject);
    const span = card.querySelector('.card-content span.project-date');
    expect(span).not.toBeNull();
    expect(span.textContent).toBe('Sep 2024');
  });

  test('card content has <p> with description', () => {
    const card = createProjectCard(sampleProject);
    const p = card.querySelector('.card-content p');
    expect(p).not.toBeNull();
    expect(p.textContent).toBe('A test project description.');
  });
});

describe('renderProjectCards', () => {
  test('populates container with correct number of children', () => {
    const container = document.createElement('div');
    const projects = [sampleProject, featuredProject];
    renderProjectCards(container, projects);
    expect(container.children.length).toBe(2);
  });

  test('clears existing content before rendering', () => {
    const container = document.createElement('div');
    const existing = document.createElement('p');
    existing.textContent = 'Old content';
    container.appendChild(existing);

    renderProjectCards(container, [sampleProject]);
    expect(container.children.length).toBe(1);
    expect(container.children[0].tagName).toBe('A');
    expect(container.querySelector('a.project-card')).not.toBeNull();
  });
});
