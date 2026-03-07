# Phase 5: Chat JavaScript Module (TDD)

## Goal

Create `WebContent/js/chat.js` — a JavaScript module that handles the chat UI interactions: sending messages to the Lambda, displaying responses, rate limiting, and loading states. Follow TDD: write Jest tests first, then implement.

## Prerequisites

- Phase 4 complete (HTML elements `#chat-input`, `#chat-send`, `#chat-messages`, `#chat-rate-limit` exist in `index.html`)
- Phase 3 complete (Lambda Function URL is known — needed for the `LAMBDA_URL` constant)

## Critical Files

- `WebContent/js/chat.js` — New module to create
- `__tests__/chat.test.js` — New Jest test file to create

## Existing Patterns to Follow

### Module Pattern (from `WebContent/js/filter.js`)

Each JS module exports pure functions for testability and an `init*()` function for DOM wiring:

```javascript
// Pure functions (testable without DOM)
export const getFilteredVisibility = (cardTags, activeFilters) => { ... };
export const applyMaxVisible = (visibility, max) => { ... };

// DOM orchestrator (called from main.js)
export function initFilter(config) { ... }
```

### Jest Test Pattern (from `__tests__/filter.test.js`)

Tests import pure functions directly and test them in isolation:

```javascript
import { getFilteredVisibility, applyMaxVisible } from '../WebContent/js/filter.js';

describe('getFilteredVisibility', () => {
  test('returns all true when no filters are active', () => {
    const result = getFilteredVisibility(cardTags, new Set());
    expect(result).toEqual([true, true, true, true]);
  });
});
```

### Jest Config (`jest.config.js`)

```javascript
export default {
  testEnvironment: 'jest-environment-jsdom',
  transform: {},
};
```

The `jsdom` environment provides `document`, `window`, `localStorage`, and other browser APIs for testing.

---

## Step 1: Write Jest Tests (RED)

**Create `__tests__/chat.test.js`**

```javascript
import {
  isRateLimited,
  recordRequest,
  getRemainingRequests,
  formatMessage,
  escapeHtml,
  RATE_LIMIT_CONFIG,
} from '../WebContent/js/chat.js';

describe('Rate Limiting', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('allows requests when no history exists', () => {
    expect(isRateLimited()).toBe(false);
  });

  test('allows requests under the limit', () => {
    for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_REQUESTS - 1; i++) {
      recordRequest();
    }
    expect(isRateLimited()).toBe(false);
  });

  test('blocks requests at the limit', () => {
    for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_REQUESTS; i++) {
      recordRequest();
    }
    expect(isRateLimited()).toBe(true);
  });

  test('returns correct remaining count', () => {
    expect(getRemainingRequests()).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS);
    recordRequest();
    expect(getRemainingRequests()).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS - 1);
  });

  test('expired requests are not counted', () => {
    const expired = Date.now() - RATE_LIMIT_CONFIG.WINDOW_MS - 1000;
    localStorage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify([expired]));
    expect(isRateLimited()).toBe(false);
    expect(getRemainingRequests()).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS);
  });
});

describe('escapeHtml', () => {
  test('escapes angle brackets', () => {
    expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
  });

  test('escapes ampersands', () => {
    expect(escapeHtml('a & b')).toBe('a &amp; b');
  });

  test('passes plain text through unchanged', () => {
    expect(escapeHtml('Hello world')).toBe('Hello world');
  });
});

describe('formatMessage', () => {
  test('creates user message HTML', () => {
    const html = formatMessage('Hello!', 'user');
    expect(html).toContain('chat-message');
    expect(html).toContain('user');
    expect(html).toContain('Hello!');
  });

  test('creates assistant message HTML', () => {
    const html = formatMessage('Hi there!', 'assistant');
    expect(html).toContain('chat-message');
    expect(html).toContain('assistant');
    expect(html).toContain('Hi there!');
  });

  test('escapes HTML in user messages to prevent XSS', () => {
    const html = formatMessage('<script>alert("xss")</script>', 'user');
    expect(html).not.toContain('<script>');
    expect(html).toContain('&lt;script&gt;');
  });

  test('does not escape assistant messages (trusted content)', () => {
    const html = formatMessage('Check <strong>this</strong> out', 'assistant');
    expect(html).toContain('<strong>this</strong>');
  });
});
```

**Run tests — they should all FAIL (RED):**

```bash
npm test
```

---

## Step 2: Implement chat.js (GREEN)

**Create `WebContent/js/chat.js`**

```javascript
'use strict';

/** Rate limit configuration. */
export const RATE_LIMIT_CONFIG = {
  MAX_REQUESTS: 10,
  WINDOW_MS: 60 * 60 * 1000, // 1 hour
  STORAGE_KEY: 'chat_rate_limit',
};

/**
 * Lambda Function URL — replace with your actual URL after deployment.
 * See docs/plans/chat-agent/phase-3-aws-setup.md Step 8.
 */
const LAMBDA_URL = 'https://YOUR_FUNCTION_URL.lambda-url.us-east-1.on.aws/';

// --- Pure Functions (exported for testing) ---

/**
 * Escapes HTML entities to prevent XSS in user-supplied text.
 *
 * @param {string} text - Raw text to escape.
 * @returns {string} HTML-safe text.
 */
export const escapeHtml = (text) => {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
};

/**
 * Gets non-expired request timestamps from localStorage.
 *
 * @returns {number[]} Timestamps within the current rate limit window.
 */
const getValidTimestamps = () => {
  try {
    const raw = localStorage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY);
    if (!raw) return [];
    const timestamps = JSON.parse(raw);
    const cutoff = Date.now() - RATE_LIMIT_CONFIG.WINDOW_MS;
    return timestamps.filter((t) => t > cutoff);
  } catch {
    return [];
  }
};

/**
 * Checks if the user has exceeded the rate limit.
 *
 * @returns {boolean} True if rate limited.
 */
export const isRateLimited = () => {
  return getValidTimestamps().length >= RATE_LIMIT_CONFIG.MAX_REQUESTS;
};

/**
 * Records a new request timestamp in localStorage.
 */
export const recordRequest = () => {
  const timestamps = getValidTimestamps();
  timestamps.push(Date.now());
  localStorage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify(timestamps));
};

/**
 * Returns the number of remaining requests in the current window.
 *
 * @returns {number} Remaining requests (0 or positive).
 */
export const getRemainingRequests = () => {
  return Math.max(0, RATE_LIMIT_CONFIG.MAX_REQUESTS - getValidTimestamps().length);
};

/**
 * Formats a chat message as an HTML string.
 *
 * User messages are escaped to prevent XSS. Assistant messages are
 * trusted (from the API) and rendered as-is.
 *
 * @param {string} text - Message text.
 * @param {'user'|'assistant'} role - Who sent the message.
 * @returns {string} HTML string for insertion into the DOM.
 */
export const formatMessage = (text, role) => {
  const content = role === 'user' ? escapeHtml(text) : text;
  return `<div class="chat-message ${role}"><p>${content}</p></div>`;
};

// --- Private Helpers ---

/**
 * Creates a loading indicator HTML string.
 *
 * @returns {string} HTML for the bouncing dots animation.
 */
const createLoadingHtml = () => {
  return `<div class="chat-message assistant chat-loading" id="chat-loading">
    <div class="chat-loading-dots">
      <span></span><span></span><span></span>
    </div>
  </div>`;
};

/**
 * Sends a message to the Lambda function.
 *
 * @param {string} message - User's question.
 * @returns {Promise<string>} The assistant's response text.
 * @throws {Error} If the request fails or returns a non-OK status.
 */
const sendMessage = async (message) => {
  const response = await fetch(LAMBDA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `Request failed (${response.status})`);
  }

  const data = await response.json();
  return data.response;
};

// --- DOM Orchestrator ---

/**
 * Initializes the chat agent UI and event handlers.
 *
 * Wires up the send button and Enter key to submit messages,
 * displays responses, and manages rate limiting UI.
 * Only runs when the required DOM elements exist.
 */
export function initChat() {
  const chatInput = document.getElementById('chat-input');
  const chatSend = document.getElementById('chat-send');
  const chatMessages = document.getElementById('chat-messages');
  const chatRateLimit = document.getElementById('chat-rate-limit');

  if (!chatInput || !chatSend || !chatMessages) {
    return;
  }

  let isProcessing = false;

  /** Appends HTML to the messages container and scrolls to bottom. */
  const appendMessage = (html) => {
    chatMessages.insertAdjacentHTML('beforeend', html);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  /** Updates the rate limit warning text and disables input at zero. */
  const updateRateLimitDisplay = () => {
    const remaining = getRemainingRequests();
    if (remaining <= 3 && remaining > 0) {
      chatRateLimit.textContent = `${remaining} question${remaining === 1 ? '' : 's'} remaining this hour`;
      chatRateLimit.hidden = false;
    } else if (remaining === 0) {
      chatRateLimit.textContent = 'Rate limit reached. Please try again later.';
      chatRateLimit.hidden = false;
      chatInput.disabled = true;
      chatSend.disabled = true;
    } else {
      chatRateLimit.hidden = true;
    }
  };

  /** Handles sending a message: validates, displays, calls API, shows response. */
  const handleSend = async () => {
    const message = chatInput.value.trim();
    if (!message || isProcessing) return;

    if (isRateLimited()) {
      updateRateLimitDisplay();
      return;
    }

    isProcessing = true;
    chatInput.value = '';
    chatSend.disabled = true;

    // Show user message
    appendMessage(formatMessage(message, 'user'));

    // Show loading indicator
    appendMessage(createLoadingHtml());

    try {
      recordRequest();
      const response = await sendMessage(message);

      // Remove loading indicator
      const loading = document.getElementById('chat-loading');
      if (loading) loading.remove();

      // Show assistant response
      appendMessage(formatMessage(response, 'assistant'));
    } catch {
      const loading = document.getElementById('chat-loading');
      if (loading) loading.remove();

      appendMessage(formatMessage('Sorry, something went wrong. Please try again.', 'assistant'));
    } finally {
      isProcessing = false;
      chatSend.disabled = false;
      chatInput.focus();
      updateRateLimitDisplay();
    }
  };

  // Wire event listeners
  chatSend.addEventListener('click', handleSend);

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  // Show initial rate limit state
  updateRateLimitDisplay();
}
```

## Step 3: Run Tests Again (GREEN)

```bash
npm test
```

All existing tests (filter, carousel, utils) plus all new chat tests should pass.

## Important: Update LAMBDA_URL

The `LAMBDA_URL` constant at the top of `chat.js` is a placeholder. After completing Phase 3 (AWS deployment), replace it with your actual Lambda Function URL:

```javascript
const LAMBDA_URL = 'https://abc123def456.lambda-url.us-east-1.on.aws/';
```

## Key Design Decisions

1. **Pure functions exported for testing:** `isRateLimited`, `recordRequest`, `getRemainingRequests`, `formatMessage`, and `escapeHtml` are all pure functions that can be tested without a DOM.

2. **XSS protection:** User input is escaped via `escapeHtml()` before rendering. Assistant responses from the API are trusted and rendered as-is (allowing the AI to return formatted text if needed).

3. **Rate limiting via localStorage:** Simple sliding window — stores an array of timestamps, filters out expired ones. Not tamper-proof (user can clear localStorage), but sufficient for a portfolio site.

4. **Loading state:** A bouncing dots animation (CSS from Phase 4) shows while waiting for the Lambda response. The loading element has `id="chat-loading"` so it can be removed when the response arrives.

5. **Error handling:** Network errors and non-OK responses show a generic "something went wrong" message. The rate limit counter still increments on errors to prevent retry abuse.

6. **No conversation history sent to API:** Each request is independent. The Lambda receives only the current question, not previous messages. This keeps the implementation simple and the token cost low.

## Output

After this phase:

- `WebContent/js/chat.js` exists with all exports
- `__tests__/chat.test.js` has 12+ passing tests
- `npm test` passes all tests (existing + new)
- Ready for Phase 6 (wire into main.js)
