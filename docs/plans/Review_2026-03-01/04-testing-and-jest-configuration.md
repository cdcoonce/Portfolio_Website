# Phase 4: Testing & Jest Configuration

**Priority:** Fourth — depends on Phase 3 (ES module exports must exist to import)
**Complexity:** Medium
**Review items addressed:** #2 (completion), #10, #18
**Files touched:** `package.json`, `__tests__/filter.test.js`, `__tests__/carousel.test.js`, `__tests__/utils.test.js`, `tests/test_links.py`, `tests/test_seo.py`

---

## Issues Addressed

| #   | Issue                                            | Severity |
| --- | ------------------------------------------------ | -------- |
| 2   | All Jest unit tests are stubs — zero JS coverage | High     |
| 10  | Missing Jest configuration for jsdom environment | Medium   |
| 18  | SEO & link tests are stubs                       | Low      |

---

## Step-by-Step Changes

### Step 1: Add Jest configuration to `package.json` (Issue #10)

**File:** `package.json`

Add a `"jest"` configuration block. Since `package.json` now uses `"type": "module"` (Phase 3), Jest needs ESM support via the `--experimental-vm-modules` flag.

Add the following to `package.json`:

```json
"jest": {
  "testEnvironment": "jsdom",
  "transform": {}
}
```

Update the test scripts to enable ESM support:

```json
"scripts": {
  "test": "NODE_OPTIONS='--experimental-vm-modules' jest",
  "test:watch": "NODE_OPTIONS='--experimental-vm-modules' jest --watch",
  "test:coverage": "NODE_OPTIONS='--experimental-vm-modules' jest --coverage"
}
```

---

### Step 2: Write `__tests__/utils.test.js` (Issue #2)

Replace the stub file with real tests for the pure utility functions.

```js
import { getItemsToShow, isDesktop } from '../WebContent/js/utils.js';

describe('getItemsToShow', () => {
  test('returns desktop count when viewport exceeds breakpoint', () => {
    expect(getItemsToShow(1400, 1200, 2, 1)).toBe(2);
  });

  test('returns desktop count at exactly the breakpoint', () => {
    expect(getItemsToShow(1200, 1200, 2, 1)).toBe(2);
  });

  test('returns mobile count below breakpoint', () => {
    expect(getItemsToShow(1199, 1200, 2, 1)).toBe(1);
  });
});

describe('isDesktop', () => {
  test('returns true at breakpoint', () => {
    expect(isDesktop(1200, 1200)).toBe(true);
  });

  test('returns false below breakpoint', () => {
    expect(isDesktop(1199, 1200)).toBe(false);
  });

  test('returns true above breakpoint', () => {
    expect(isDesktop(1400, 1200)).toBe(true);
  });
});
```

---

### Step 3: Write `__tests__/filter.test.js` (Issue #2)

Replace the stub with tests for `getFilteredVisibility`.

```js
import { getFilteredVisibility } from '../WebContent/js/filter.js';

describe('getFilteredVisibility', () => {
  const cardTags = [
    'python,etl,visualization',
    'r,shiny,analytics-dashboard',
    'sql,business-intelligence',
    'python,machine-learning',
  ];

  test('returns all true when no filters are active', () => {
    const result = getFilteredVisibility(cardTags, new Set());
    expect(result).toEqual([true, true, true, true]);
  });

  test('filters to cards matching a single tag', () => {
    const result = getFilteredVisibility(cardTags, new Set(['python']));
    expect(result).toEqual([true, false, false, true]);
  });

  test('filters with multiple active tags (OR logic)', () => {
    const result = getFilteredVisibility(cardTags, new Set(['python', 'sql']));
    expect(result).toEqual([true, false, true, true]);
  });

  test('returns all false when filter matches nothing', () => {
    const result = getFilteredVisibility(cardTags, new Set(['tableau']));
    expect(result).toEqual([false, false, false, false]);
  });

  test('handles empty tag strings gracefully', () => {
    const result = getFilteredVisibility(['', 'python'], new Set(['python']));
    expect(result).toEqual([false, true]);
  });

  test('trims whitespace in tag strings', () => {
    const result = getFilteredVisibility(['python , etl'], new Set(['etl']));
    expect(result).toEqual([true]);
  });
});
```

---

### Step 4: Write `__tests__/carousel.test.js` (Issue #2)

Replace the stub with tests for all exported pure carousel functions.

```js
import {
  getNextIndex,
  getPrevIndex,
  getDotCount,
  getActiveDotIndex,
  getCounterText,
} from '../WebContent/js/carousel.js';

describe('getNextIndex', () => {
  test('advances by step when not at end', () => {
    expect(getNextIndex(0, 1, 7, 1)).toBe(1);
  });

  test('advances by 2 on desktop', () => {
    expect(getNextIndex(0, 2, 7, 2)).toBe(2);
  });

  test('wraps to 0 when at end (mobile)', () => {
    expect(getNextIndex(6, 1, 7, 1)).toBe(0);
  });

  test('wraps to 0 when at end (desktop, 2-up)', () => {
    expect(getNextIndex(6, 2, 7, 2)).toBe(0);
  });

  test('advances when space remains for partial view', () => {
    expect(getNextIndex(4, 2, 7, 2)).toBe(6);
  });
});

describe('getPrevIndex', () => {
  test('goes back by step when not at start', () => {
    expect(getPrevIndex(3, 1, 7, 1)).toBe(2);
  });

  test('wraps to last set when at start (mobile)', () => {
    expect(getPrevIndex(0, 1, 7, 1)).toBe(6);
  });

  test('wraps to last set when at start (desktop)', () => {
    expect(getPrevIndex(0, 2, 7, 2)).toBe(5);
  });
});

describe('getDotCount', () => {
  test('returns total items on mobile', () => {
    expect(getDotCount(7, false)).toBe(7);
  });

  test('returns half (rounded up) on desktop', () => {
    expect(getDotCount(7, true)).toBe(4);
  });

  test('returns exact half for even count on desktop', () => {
    expect(getDotCount(6, true)).toBe(3);
  });
});

describe('getActiveDotIndex', () => {
  test('returns carousel index on mobile', () => {
    expect(getActiveDotIndex(3, false)).toBe(3);
  });

  test('returns halved index on desktop', () => {
    expect(getActiveDotIndex(4, true)).toBe(2);
  });

  test('returns 0 for first position on desktop', () => {
    expect(getActiveDotIndex(0, true)).toBe(0);
  });
});

describe('getCounterText', () => {
  test('returns "1 / 7" for first item mobile', () => {
    expect(getCounterText(0, 1, 7)).toBe('1 / 7');
  });

  test('returns "1 / 4" for first pair desktop', () => {
    expect(getCounterText(0, 2, 7)).toBe('1 / 4');
  });

  test('returns "4 / 4" for last pair desktop', () => {
    expect(getCounterText(6, 2, 7)).toBe('4 / 4');
  });
});
```

---

### Step 5: Implement `tests/test_seo.py` (Issue #18)

**File:** `tests/test_seo.py`

Replace skipped stubs with real tests. The meta description already exists in `index.html`; Open Graph tags are still missing and should remain as expected failures (marked `xfail`) to track as future work.

```python
from bs4 import BeautifulSoup
from pathlib import Path

import pytest

html = Path('index.html').read_text()
soup = BeautifulSoup(html, 'html.parser')


def test_has_title_tag():
    title = soup.find('title')
    assert title, 'Missing <title> tag'
    assert len(title.string.strip()) > 0, 'Title tag is empty'


def test_has_meta_description():
    meta = soup.find('meta', attrs={'name': 'description'})
    assert meta, 'Missing meta description'
    content = meta.get('content', '')
    assert len(content) >= 50, f'Meta description too short ({len(content)} chars)'


@pytest.mark.xfail(reason='Open Graph tags not yet implemented')
def test_has_open_graph_tags():
    assert soup.find('meta', property='og:title'), 'Missing og:title'
    assert soup.find('meta', property='og:description'), 'Missing og:description'
    assert soup.find('meta', property='og:image'), 'Missing og:image'
```

---

### Step 6: Implement `tests/test_links.py` (Issue #18)

**File:** `tests/test_links.py`

Replace the skipped stub with a real parametrized test. Mark as `slow` since it makes network requests.

```python
import pytest
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_external_links():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]


@pytest.mark.slow
@pytest.mark.parametrize('url', get_external_links())
def test_external_link_resolves(url):
    resp = requests.head(url, allow_redirects=True, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    assert resp.status_code < 400, f'{url} returned {resp.status_code}'
```

---

## Verification

1. Run `npm test` — all Jest tests pass (utils, filter, carousel)
2. Run `npm run test:coverage` — confirm meaningful coverage of pure logic
3. Run `uv run pytest tests/test_seo.py` — title and meta description pass; OG tags xfail
4. Run `uv run pytest tests/test_links.py -m slow` — all external links resolve
5. Run `make check` — full suite green
