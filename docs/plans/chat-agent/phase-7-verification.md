# Phase 7: Full Test Suite Verification

## Goal

Run every test, linter, and formatter to confirm the entire chat agent feature works end-to-end without breaking any existing functionality.

## Prerequisites

- All previous phases (1-6) complete

## Verification Steps

Run each check in order. All must pass before the feature is considered complete.

---

### 1. Prettier (Code Formatting)

```bash
npm run format -- --check
```

Expected: No formatting issues. If any files need formatting, run `npm run format` to fix them.

### 2. ESLint (JavaScript Linting)

```bash
npm run lint:js
```

Expected: No errors. Warnings for unused vars are acceptable but should be reviewed.

### 3. Stylelint (CSS Linting)

```bash
npm run lint:css
```

Expected: No errors. The new CSS in `style.css` and `mediaqueries.css` should conform to existing conventions.

### 4. Jest Unit Tests (JavaScript)

```bash
npm test
```

Expected output should include:

- `__tests__/filter.test.js` — all passing (existing)
- `__tests__/carousel.test.js` — all passing (existing)
- `__tests__/utils.test.js` — all passing (existing)
- `__tests__/chat.test.js` — all passing (NEW: ~12 tests)

### 5. pytest Validation Tests (HTML Structure)

```bash
uv run pytest tests/test_validation.py -v
```

Expected: All tests pass, including:

- `TestHTMLValidation` — all existing tests (17 project cards, featured cards, semantic structure, etc.)
- `TestProjectsPageValidation` — all existing tests
- `TestChatSectionValidation` — all 8 new tests (section exists, heading, position, input, button, messages, aria labels)

### 6. pytest E2E Tests (Browser)

```bash
uv run pytest tests/ -m "not slow" -v
```

Expected: All tests pass, including:

- `test_gallery.py` — project filtering (existing)
- `test_carousel.py` — testimonial carousel (existing)
- `test_nav.py` — navigation and hamburger menu (existing)
- `test_hero.py` — hero section and skills grid (existing)
- `test_accessibility.py` — WCAG 2.1 AA accessibility (existing)
- `test_seo.py` — meta tags and Open Graph (existing)
- `test_chat.py` — chat section visibility, input focus, messages area (NEW: 4 tests)

### 7. Lambda Tests (Python)

```bash
cd lambda && pip install -r requirements.txt pytest pytest-mock && python -m pytest tests/ -v
```

Expected: All 15 tests pass (system prompt, request parsing, response formatting, handler integration).

### 8. Visual Verification (Manual)

```bash
npm run serve
```

Open http://localhost:8000 and verify:

1. **Section placement:** Chat section appears between Projects and Testimonials
2. **Navigation:** "Ask AI" link appears in the nav bar and scrolls to the chat section
3. **Welcome message:** The default assistant message is visible in the chat area
4. **Input field:** Can type text, placeholder text reads "e.g., What projects use Python?"
5. **Send button:** Styled consistently with other `.btn-color-1` buttons on the site
6. **Keyboard:** Pressing Enter in the input field triggers send (same as clicking Send)
7. **Mobile (resize to < 700px):** Heading centered, message bubbles take ~95% width, hamburger menu includes "Ask AI"
8. **Tablet (resize to < 1250px):** Layout remains clean and centered

Note: The chat will NOT actually work in local testing unless the Lambda is deployed (Phase 3) and the `LAMBDA_URL` in `chat.js` points to a real endpoint. The UI interaction (typing, button states) can still be verified.

### 9. Accessibility Check

```bash
uv run pytest tests/test_accessibility.py -v
```

Verify that the new chat section does not introduce any WCAG 2.1 AA violations. The axe-core scan should pass. Key accessibility features:

- `aria-label` on input and send button
- `aria-live="polite"` on the messages container (announces new messages to screen readers)
- `role="log"` on the messages container (indicates a log of messages)
- Keyboard navigable (Tab to input, Enter to send)

---

## Troubleshooting

### Common Failures

| Symptom                                                    | Likely Cause                           | Fix                                                                       |
| ---------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------- |
| ESLint `no-undef` on `fetch` or `localStorage`             | Phase 6 Step 2 incomplete              | Add globals to `eslint.config.mjs`                                        |
| Prettier errors in `lambda/`                               | Phase 6 Step 3 incomplete              | Add `lambda/` to `.prettierignore`                                        |
| `TestChatSectionValidation` fails                          | Phase 4 HTML not inserted correctly    | Check `index.html` for `<section id="chat-agent">`                        |
| Section order test fails                                   | Chat section in wrong position         | Must be between `</section>` (projects) and `<section id="testimonials">` |
| Jest `Cannot find module chat.js`                          | Phase 5 file not created               | Create `WebContent/js/chat.js`                                            |
| Existing test count changes (e.g., 18 cards instead of 17) | HTML insertion broke existing elements | Check that the chat section doesn't contain `class="project-card"`        |
| axe-core violations                                        | Missing aria attributes                | Ensure `aria-label`, `aria-live`, and `role` are present                  |

## Output

After this phase:

- All linters pass (Prettier, ESLint, Stylelint)
- All Jest unit tests pass (filter, carousel, utils, chat)
- All pytest tests pass (validation, E2E, accessibility)
- All Lambda tests pass
- Visual verification confirms correct layout and interaction
- Ready for Phase 8 (CI/CD confirmation)
