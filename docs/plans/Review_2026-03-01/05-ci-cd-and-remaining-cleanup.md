# Phase 5: CI/CD & Remaining Cleanup

**Priority:** Last — all code changes from Phases 1–4 should be merged first
**Complexity:** Small
**Review items addressed:** #3, #11, #13
**Files touched:** `.github/workflows/ci-cd.yml`, `tests/test_validation.py`

---

## Issues Addressed

| #   | Issue                                               | Severity |
| --- | --------------------------------------------------- | -------- |
| 3   | CI does not run tests — broken code won't block deploy | High  |
| 11  | CI missing Stylelint and ESLint lint steps           | Medium   |
| 13  | 404 page favicon mismatch (covered in Phase 1 Step 6) | Low   |

**Note:** Issue #13 is already handled in Phase 1 Step 6. It is listed here for traceability only.

---

## Step-by-Step Changes

### Step 1: Add lint and test jobs to CI workflow (Issues #3, #11)

**File:** `.github/workflows/ci-cd.yml`

Replace the single `lint` job (which only runs Prettier) with a comprehensive `check` job that mirrors the local `make check` target: Prettier, Stylelint, ESLint, Jest, and pytest.

**Before:**

```yaml
jobs:
  lint:
    name: Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Check formatting (Prettier)
        run: npm run format:check

  deploy:
    name: Deploy to gh-pages
    runs-on: ubuntu-latest
    needs: lint
    if: github.event_name == 'push' && github.ref == 'refs/heads/master'
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Merge master into gh-pages
        run: |
          git fetch origin
          git checkout -B gh-pages origin/gh-pages
          git merge origin/master --no-edit
          git push origin gh-pages
```

**After:**

```yaml
jobs:
  check:
    name: Lint & Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # --- Node.js setup ---
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Node dependencies
        run: npm ci

      # --- Python setup ---
      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.12

      - name: Install Python dependencies
        run: uv sync

      - name: Install Playwright browsers
        run: uv run playwright install --with-deps chromium

      # --- Linting ---
      - name: Check formatting (Prettier)
        run: npm run format:check

      - name: Lint CSS (Stylelint)
        run: npm run lint:css

      - name: Lint JS (ESLint)
        run: npm run lint:js

      # --- Tests ---
      - name: Run JS unit tests (Jest)
        run: npm test

      - name: Run Python tests (validation, a11y, e2e)
        run: uv run pytest -m "not slow"

  deploy:
    name: Deploy to gh-pages
    runs-on: ubuntu-latest
    needs: check
    if: github.event_name == 'push' && github.ref == 'refs/heads/master'
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Merge master into gh-pages
        run: |
          git fetch origin
          git checkout -B gh-pages origin/gh-pages
          git merge origin/master --no-edit
          git push origin gh-pages
```

**Key changes:**
- Renamed `lint` → `check` to reflect broader scope
- Added `uv` + Python + Playwright setup steps
- Added Stylelint and ESLint steps (Issue #11)
- Added Jest and pytest steps (Issue #3)
- Deploy job now depends on `check` instead of `lint`
- Excluded `slow` marker tests (visual regression, link checking) from CI to keep builds fast

---

### Step 2: Add a validation test for no inline scripts (Issue #8 — test coverage)

**File:** `tests/test_validation.py`

Add a test to ensure no inline `<script>` tags exist inside `<body>` (excluding the external `<script src="...">` tag). This prevents regression of the `document.write()` fix from Phase 1.

```python
def test_no_inline_scripts_in_body():
    """Ensure no inline <script> tags exist in the body (external src scripts are allowed)."""
    body = soup.find('body')
    inline_scripts = [s for s in body.find_all('script') if not s.get('src')]
    assert len(inline_scripts) == 0, (
        f'{len(inline_scripts)} inline script(s) found in body'
    )
```

**Note:** The Google Analytics scripts in `<head>` are intentionally excluded — they are in the `<head>`, not `<body>`, and are a standard third-party integration pattern.

---

## Verification

1. Push a test branch and open a PR to `master` — confirm the `check` job runs all steps:
   - Prettier format check
   - Stylelint
   - ESLint
   - Jest unit tests
   - pytest (validation, a11y, e2e)
2. Confirm the `deploy` job only runs on push to `master` (not on PRs)
3. Intentionally break a test locally and verify CI would catch it:
   ```bash
   make check  # Should mirror what CI runs
   ```
4. Run `uv run pytest tests/test_validation.py` — new `test_no_inline_scripts_in_body` passes
