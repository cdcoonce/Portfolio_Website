# Phase 4: Testing

**Files:** `__tests__/filter.test.js`, `tests/test_validation.py`, `tests/test_gallery.py`, `tests/conftest.py`

## Overview

All new logic is tested following TDD: write the test first, watch it fail, then implement the minimum code to pass. Tests are organized into three tiers: unit tests (Jest), validation tests (pytest + BeautifulSoup), and E2E tests (pytest + Playwright).

## 4.1 Unit Tests — `__tests__/filter.test.js`

### New test suite: `applyMaxVisible`

```javascript
describe('applyMaxVisible', () => {
  test('returns same array when max is null', () => {
    const vis = [true, false, true, true];
    expect(applyMaxVisible(vis, null)).toEqual([true, false, true, true]);
  });

  test('caps visible cards to max count', () => {
    const vis = [true, true, true, true, true];
    expect(applyMaxVisible(vis, 4)).toEqual([true, true, true, true, false]);
  });

  test('returns unchanged when fewer visible than max', () => {
    const vis = [true, false, true];
    expect(applyMaxVisible(vis, 4)).toEqual([true, false, true]);
  });

  test('handles max of 0', () => {
    const vis = [true, true, true];
    expect(applyMaxVisible(vis, 0)).toEqual([false, false, false]);
  });

  test('preserves order — first N visible win', () => {
    const vis = [false, true, false, true, true, true];
    expect(applyMaxVisible(vis, 2)).toEqual([false, true, false, true, false, false]);
  });
});
```

### New test suite: `getFeaturedVisibility`

```javascript
describe('getFeaturedVisibility', () => {
  test('returns true only for featured flags', () => {
    expect(getFeaturedVisibility([true, false, true, false])).toEqual([true, false, true, false]);
  });

  test('returns all false when no featured cards', () => {
    expect(getFeaturedVisibility([false, false, false])).toEqual([false, false, false]);
  });
});
```

### New test suite: `getFilterFromURL`

```javascript
describe('getFilterFromURL', () => {
  const originalLocation = window.location;

  afterEach(() => {
    // Reset location mock
    delete window.location;
    window.location = originalLocation;
  });

  test('returns null when no filter param', () => {
    delete window.location;
    window.location = { search: '' };
    expect(getFilterFromURL()).toBeNull();
  });

  test('returns filter value from URL', () => {
    delete window.location;
    window.location = { search: '?filter=python' };
    expect(getFilterFromURL()).toBe('python');
  });

  test('returns null for empty filter param', () => {
    delete window.location;
    window.location = { search: '?filter=' };
    expect(getFilterFromURL()).toBeNull();
  });
});
```

### Existing tests

All existing `getFilteredVisibility` tests must continue to pass unchanged. No modifications to existing test cases.

## 4.2 Validation Tests — `tests/test_validation.py`

### Update existing assertions

- **`test_featured_cards_exist`:** Change assertion from `>= 3` to `== 4`

### New tests for `index.html`

```python
def test_view_all_link_exists(index_soup):
    """View All Projects link must point to projects.html."""
    link = index_soup.find('a', class_='view-all-link')
    assert link is not None, "View All Projects link not found"
    assert 'projects.html' in link['href']

def test_index_has_data_page_attribute(index_soup):
    """index.html body must have data-page='home'."""
    body = index_soup.find('body')
    assert body.get('data-page') == 'home'

def test_index_still_has_17_cards_in_dom(index_soup):
    """All 17 cards remain in DOM even though only 4 are visible."""
    cards = index_soup.find_all(class_='project-card')
    assert len(cards) == 17
```

### New tests for `projects.html`

```python
def test_projects_page_exists():
    """projects.html must exist at project root."""
    assert Path('projects.html').is_file()

def test_projects_page_has_all_17_cards(projects_soup):
    """All 17 project cards must be present on the projects page."""
    cards = projects_soup.find_all(class_='project-card')
    assert len(cards) == 17

def test_projects_page_has_filter_buttons(projects_soup):
    """Projects page must have skill filter buttons."""
    tags = projects_soup.find_all('button', class_='skill-tag')
    assert len(tags) > 0

def test_projects_page_has_data_page_attribute(projects_soup):
    """projects.html body must have data-page='projects'."""
    body = projects_soup.find('body')
    assert body.get('data-page') == 'projects'

def test_projects_page_has_featured_filter(projects_soup):
    """Projects page must have a Featured filter button."""
    featured = projects_soup.find('button', attrs={'data-filter': 'featured'})
    assert featured is not None
```

### New fixture

```python
@pytest.fixture
def projects_soup():
    """Parse projects.html with BeautifulSoup."""
    html = Path('projects.html').read_text(encoding='utf-8')
    return BeautifulSoup(html, 'html.parser')
```

## 4.3 E2E Tests — `tests/test_gallery.py`

### Update existing tests

- **`test_all_filter_shows_every_card`:** Rename to `test_featured_reset_shows_four_cards`. After clicking reset on `index.html`, exactly 4 cards should be visible, all with the `featured` class.
- **`test_filter_shows_only_matching_cards`:** After clicking a filter on `index.html`, at most 4 cards should be visible.

### New tests for `index.html`

```python
def test_default_shows_four_featured_cards(page):
    """On initial load, exactly 4 cards visible, all featured."""
    visible = page.locator('.project-card:visible')
    expect(visible).to_have_count(4)
    for i in range(4):
        expect(visible.nth(i)).to_have_class(re.compile(r'featured'))

def test_view_all_link_navigates(page):
    """Clicking View All Projects navigates to projects.html."""
    page.click('.view-all-link')
    expect(page).to_have_url(re.compile(r'projects\.html'))
```

### New test class: `TestProjectsPage`

```python
class TestProjectsPage:
    """E2E tests for the all-projects page."""

    def test_all_cards_visible_by_default(self, projects_page):
        """All 17 cards visible on initial load."""
        visible = projects_page.locator('.project-card:visible')
        expect(visible).to_have_count(17)

    def test_filter_works(self, projects_page):
        """Clicking a filter shows only matching cards."""
        projects_page.click('[data-filter="python"]')
        visible = projects_page.locator('.project-card:visible')
        count = visible.count()
        assert count > 0
        assert count <= 17

    def test_url_param_preselects_filter(self, browser, server):
        """Navigating with ?filter=python pre-selects the filter."""
        page = browser.new_page()
        page.goto(f'{server}/projects.html?filter=python')
        python_tag = page.locator('[data-filter="python"]')
        expect(python_tag).to_have_class(re.compile(r'active'))
        visible = page.locator('.project-card:visible')
        assert visible.count() > 0
        page.close()

    def test_featured_filter(self, projects_page):
        """Clicking Featured filter shows only featured cards."""
        projects_page.click('[data-filter="featured"]')
        visible = projects_page.locator('.project-card:visible')
        expect(visible).to_have_count(4)

    def test_reset_shows_all(self, projects_page):
        """Clicking reset after filtering shows all 17 cards."""
        projects_page.click('[data-filter="python"]')
        projects_page.click('.skill-filter-reset')
        visible = projects_page.locator('.project-card:visible')
        expect(visible).to_have_count(17)
```

### New fixture in `conftest.py`

```python
@pytest.fixture
def projects_page(browser, server):
    """Provide a fresh Playwright page loaded with projects.html."""
    page = browser.new_page()
    page.goto(f'{server}/projects.html')
    yield page
    page.close()
```

## 4.4 TDD Implementation Order

Tests are written **before** the corresponding implementation code. The order follows the dependency chain:

| Step | Test first                         | Then implement                                                  |
| ---- | ---------------------------------- | --------------------------------------------------------------- |
| 1    | `applyMaxVisible` unit tests       | `applyMaxVisible` function                                      |
| 2    | `getFeaturedVisibility` unit tests | `getFeaturedVisibility` function                                |
| 3    | `getFilterFromURL` unit tests      | `getFilterFromURL` function                                     |
| 4    | —                                  | Refactor `initFilter` (existing tests validate backward compat) |
| 5    | `index.html` validation tests      | Update `index.html`                                             |
| 6    | `projects.html` validation tests   | Create `projects.html`                                          |
| 7    | E2E tests for home page            | Wire everything together                                        |
| 8    | E2E tests for projects page        | Final integration                                               |

## 4.5 Running Tests

```bash
# Unit tests
npx jest

# Validation tests only
uv run pytest -m validation

# E2E tests only
uv run pytest -m e2e

# All tests with coverage
uv run pytest --cov=src --cov-report=term-missing
npx jest --coverage
```
