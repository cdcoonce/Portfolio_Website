# Phase 8: CI/CD Pipeline Updates

## Goal

Confirm the existing GitHub Actions CI/CD pipeline automatically picks up the new tests without changes, and make any minor adjustments needed.

## Prerequisites

- Phase 7 complete (all tests pass locally)

## Current CI/CD Pipeline

**File:** `.github/workflows/ci-cd.yml`

The pipeline has two jobs:

### Check Job (runs on every PR and push to master)

1. Prettier format check
2. Stylelint CSS linting
3. ESLint JS linting
4. Jest unit tests (`npm test`)
5. pytest integration tests (`uv run pytest -m "not slow"`)

### Deploy Job (runs only on push to master, after check passes)

1. Merge `origin/master` into `gh-pages`
2. Push to origin (triggers GitHub Pages deployment)

## What Happens Automatically

**No CI/CD changes are needed.** Here's why:

### Jest Tests

The `npm test` command runs Jest, which discovers test files matching the pattern `__tests__/**/*.test.js`. The new `__tests__/chat.test.js` file is automatically included.

### pytest Tests

The `uv run pytest -m "not slow"` command discovers all test files in the `tests/` directory. The new `tests/test_chat.py` file and the new `TestChatSectionValidation` class in `tests/test_validation.py` are automatically included.

### Prettier

The new `WebContent/js/chat.js` file matches the `WebContent/js/**/*.js` pattern. The `lambda/` directory is excluded via `.prettierignore` (Phase 6 Step 3).

### ESLint

The new `WebContent/js/chat.js` file matches the `WebContent/js/**/*.js` pattern in `eslint.config.mjs`. The `fetch` and `localStorage` globals were added in Phase 6 Step 2.

### Stylelint

CSS changes are in existing files (`style.css`, `mediaqueries.css`) that are already linted.

## Optional: Lambda CI (Future Enhancement)

The Lambda function tests in `lambda/tests/` are NOT run by the current CI pipeline. They are a separate Python project in the `lambda/` directory. If you want to add Lambda testing to CI in the future, you could add a step:

```yaml
- name: Lambda unit tests
  run: |
    cd lambda
    pip install -r requirements.txt pytest pytest-mock
    python -m pytest tests/ -v
```

This is optional and not needed for the initial implementation. The Lambda code is deployed separately from the static site.

## Verification

After pushing the feature branch and opening a PR:

1. The Check job should run automatically
2. All existing tests should continue to pass
3. New tests (chat.test.js, test_chat.py, TestChatSectionValidation) should appear in the test output
4. If all checks pass, the PR is ready for merge

```bash
# Verify locally before pushing
npm run format -- --check
npm run lint:js
npm run lint:css
npm test
uv run pytest -m "not slow" -v
```

## Deploy Flow

After merging to `master`:

1. CI Check job runs and passes
2. Deploy job merges `master` into `gh-pages`
3. GitHub Pages serves the updated site with the chat section
4. The chat section is visible but non-functional until the Lambda is deployed (Phase 3)
5. After Lambda deployment, update the `LAMBDA_URL` in `chat.js`, push again, and the chat becomes fully functional

## Output

After this phase:

- CI/CD pipeline runs without modifications
- All new tests are automatically discovered and executed
- The feature is ready for merge and deployment
- Lambda deployment is a separate manual process (Phase 3 guide)
