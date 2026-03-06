# Phase 6: Wire chat.js into main.js + Config Updates

## Goal

Connect the chat module to the application entry point and update linting/formatting configs so the new code passes all checks.

## Prerequisites

- Phase 5 complete (`WebContent/js/chat.js` exists with `initChat()` export)
- Phase 4 complete (HTML elements exist in `index.html`)

## Critical Files to Modify

1. `WebContent/js/main.js` — Import and initialize chat module
2. `eslint.config.mjs` — Add browser globals used by chat.js
3. `.prettierignore` — Exclude the `lambda/` Python directory

---

## Step 1: Modify `WebContent/js/main.js`

### Current State (lines 1-82)

```javascript
'use strict';

import { initFilter, getFilterFromURL } from './filter.js';
import { initCarousel } from './carousel.js';

document.addEventListener('DOMContentLoaded', () => {
  // ... navigation, back-to-top, scroll-down setup ...

  const page = document.body.dataset.page;

  if (page === 'projects') {
    initFilter({
      maxVisible: null,
      defaultFilter: 'all',
      initialFilter: getFilterFromURL(),
    });
  } else {
    initFilter({
      maxVisible: 4,
      defaultFilter: 'featured',
    });
    initCarousel();
  }
});
```

### Changes

**Add import** — After line 3 (`import { initCarousel } from './carousel.js';`), add:

```javascript
import { initChat } from './chat.js';
```

**Add initialization** — After `initCarousel();` (line 80), add:

```javascript
initChat();
```

### Result (relevant lines)

```javascript
'use strict';

import { initFilter, getFilterFromURL } from './filter.js';
import { initCarousel } from './carousel.js';
import { initChat } from './chat.js';

// ... (DOMContentLoaded handler unchanged until the else branch) ...

  } else {
    initFilter({
      maxVisible: 4,
      defaultFilter: 'featured',
    });
    initCarousel();
    initChat();
  }
});
```

`initChat()` is called only on the homepage (`data-page="home"`) because it's in the `else` branch. The projects page (`data-page="projects"`) does not get the chat module, which is correct — chat only appears on the homepage.

---

## Step 2: Modify `eslint.config.mjs`

### Current State

```javascript
export default [
  {
    files: ['WebContent/js/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        document: 'readonly',
        window: 'readonly',
        console: 'readonly',
        setTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        clearTimeout: 'readonly',
        URLSearchParams: 'readonly',
      },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      'no-var': 'error',
      'prefer-const': 'warn',
      eqeqeq: 'error',
    },
  },
];
```

### Changes

Add `fetch` and `localStorage` to the `globals` object. These are browser APIs used by `chat.js` and would cause `no-undef` errors without being declared.

After `URLSearchParams: 'readonly',` add:

```javascript
        fetch: 'readonly',
        localStorage: 'readonly',
```

---

## Step 3: Modify `.prettierignore`

### Current State

```text
node_modules
.venv
package-lock.json
uv.lock
# Ignore project asset files (notebook exports, generated HTML, etc.)
WebContent/assets/

# Ignore node_modules (prettier already ignores these by default, but explicit is clearer)
node_modules/
```

### Changes

Add the `lambda/` directory at the end. This is a Python directory and should not be formatted by Prettier:

```text
# Ignore Lambda function (Python, not JS)
lambda/
```

---

## Step 4: Verify

Run all linting and formatting checks:

```bash
# ESLint — should pass with new globals
npm run lint:js

# Stylelint — should pass (no changes to CSS lint config)
npm run lint:css

# Prettier — should pass with lambda/ excluded
npm run format -- --check

# Jest — should pass all tests
npm test
```

If ESLint reports any new warnings or errors in `chat.js`, fix them before proceeding.

## Output

After this phase:

- `main.js` imports and initializes the chat module on the homepage
- ESLint config recognizes `fetch` and `localStorage` as valid globals
- Prettier ignores the `lambda/` Python directory
- All linting and formatting checks pass
- Ready for Phase 7 (full verification)
