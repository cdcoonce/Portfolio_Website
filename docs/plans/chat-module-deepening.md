# Refactor: Deepen Chat Module with Injectable Dependencies

## Problem

The chat module (`WebContent/js/chat.js`, 246 lines) mixes four concerns — rate limiting, message formatting, API communication, and DOM orchestration — with two of them fully untestable:

- **`LAMBDA_URL` is hardcoded** at line 14 as a module-level constant. To test `sendMessage()` or use a different endpoint (staging, local dev), you must edit source code. No environment variable, no injection point.
- **`sendMessage()` is private** and uses `fetch()` with the hardcoded URL. It's the only external dependency in the module, but there's no seam to intercept it for testing.
- **`initChat()` is a 100-line closure** that owns conversation history, DOM references, and the full send flow. Because `sendMessage` uses `fetch` with a hardcoded URL, the orchestrator can't be tested without mocking `fetch` globally or running a real server.
- **Zero E2E test coverage** for the chat widget. The Playwright suite covers carousel, filter, gallery, navigation, accessibility, and SEO — but not chat.
- **Rate-limit functions reference `localStorage` directly**, coupling tests to jsdom's localStorage implementation.

The pure functions (rate limiting, formatting) are well-tested. The architectural friction is entirely at the API boundary and the orchestrator.

**Dependency category:** True external (Mock) — the Lambda API is a third-party service from the frontend's perspective. The `fetch` call and `localStorage` are browser globals that should be injectable for testing.

## Proposed Interface

Design C: Caller-Optimized — trivial for main.js, zero global mocking for tests.

### Interface Change

The only export signature that changes is `initChat`:

```js
// Before
export function initChat()

// After
export function initChat({ apiUrl, fetchFn, storage } = {})
```

The options parameter accepts three injectable dependencies:

```js
/**
 * @typedef {Object} ChatDeps
 * @property {string}   [apiUrl]   - Lambda endpoint URL. Default: built-in LAMBDA_URL constant.
 * @property {function} [fetchFn]  - Replacement for window.fetch. Default: fetch.bind(window).
 * @property {object}   [storage]  - Replacement for localStorage. Default: window.localStorage.
 *                                   Must implement getItem(key), setItem(key, value), removeItem(key).
 */
```

Rate-limit functions gain an optional `storage` parameter (backward-compatible):

```js
export const isRateLimited = (storage = localStorage) => { ... }
export const recordRequest = (storage = localStorage) => { ... }
export const getRemainingRequests = (storage = localStorage) => { ... }
```

All existing call sites (main.js, existing tests) require zero changes.

### Usage — Production (main.js, zero changes)

```js
import { initChat } from './chat.js';
initChat(); // uses real Lambda URL, real fetch, real localStorage
```

### Usage — Tests (zero global mocking)

```js
import { initChat } from '../WebContent/js/chat.js';

test('sends user message and displays assistant response', async () => {
  document.body.innerHTML = `
    <div id="chat-messages"></div>
    <input id="chat-input" value="Hello" />
    <button id="chat-send"></button>
    <span id="chat-rate-limit" hidden></span>
  `;

  const fakeFetch = async (url, opts) => ({
    ok: true,
    json: async () => ({ response: 'I am a test response.' }),
  });

  const fakeStorage = new Map();
  const storage = {
    getItem: (k) => fakeStorage.get(k) ?? null,
    setItem: (k, v) => fakeStorage.set(k, v),
    removeItem: (k) => fakeStorage.delete(k),
  };

  initChat({ apiUrl: 'https://test.example.com/', fetchFn: fakeFetch, storage });

  document.getElementById('chat-send').click();
  await new Promise((r) => setTimeout(r, 0));

  const messages = document.getElementById('chat-messages').innerHTML;
  expect(messages).toContain('Hello');
  expect(messages).toContain('I am a test response.');
});
```

### What It Hides Internally

| Hidden inside                                                                     | Exposed to callers                          |
| --------------------------------------------------------------------------------- | ------------------------------------------- |
| `sendMessage` helper (now closes over `apiUrl`/`fetchFn` from `initChat` options) | `initChat({ apiUrl?, fetchFn?, storage? })` |
| Conversation history array (closure-scoped)                                       | Observed indirectly through DOM output      |
| Loading indicator lifecycle (create/insert/remove)                                | Never exposed                               |
| Event wiring (click, keydown handlers)                                            | Never exposed                               |
| Rate-limit display logic (`updateRateLimitDisplay`)                               | Never exposed                               |
| `isProcessing` flag and input state management                                    | Never exposed                               |

## Dependency Strategy

**All three external dependencies are injected via options bag with production defaults.**

| Dependency   | Production (default)            | Test (injected)                                |
| ------------ | ------------------------------- | ---------------------------------------------- |
| Lambda URL   | `LAMBDA_URL` constant (line 14) | Any string, e.g. `'https://test.example.com/'` |
| fetch        | `window.fetch`                  | Async function returning `{ ok, json() }`      |
| localStorage | `window.localStorage`           | Object with `getItem`/`setItem`/`removeItem`   |

The module-level `LAMBDA_URL` constant stays in the file as the default value. `sendMessage` moves from module scope into `initChat`'s closure, capturing `apiUrl` and `fetchFn` from the options destructuring.

## Testing Strategy

### New boundary tests to write

- `initChat` with fake fetch -> sends message, displays user message + assistant response
- `initChat` with failing fetch -> displays "Sorry, something went wrong" error message
- `initChat` with fake storage -> rate limiting works without touching real localStorage
- `initChat` rate limit at 0 -> disables input and send button
- `initChat` rate limit warning at <=3 remaining -> shows warning text
- `initChat` conversation history -> passes full history array to fetch body
- `initChat` Enter key submission -> triggers send flow
- `initChat` with missing DOM elements -> returns early without errors
- `isRateLimited(fakeStorage)` -> works with injected storage
- `recordRequest(fakeStorage)` -> writes to injected storage

### Existing tests that stay unchanged

- All `escapeHtml` tests (pure function, no dependencies)
- All `formatMessage` tests (pure function, no dependencies)
- All existing `isRateLimited`/`recordRequest`/`getRemainingRequests` tests (default parameter = localStorage, backward compatible)

### Test environment needs

- jsdom (already configured in jest.config.js)
- No `jest-localstorage-mock` or `jest.spyOn(global, 'fetch')` needed
- No real HTTP server needed

## Implementation Recommendations

### What the module should own

- Chat UI lifecycle (init, event wiring, input state management)
- Conversation history management (append user/assistant messages, pass to API)
- Rate limiting enforcement and display
- Message formatting (XSS escaping for user input, markdown rendering for assistant)
- Loading indicator lifecycle
- Error display on API failure

### What it should hide

- The `sendMessage` fetch call mechanics (URL, headers, JSON parsing)
- The `LAMBDA_URL` constant (implementation detail of the default transport)
- The loading indicator HTML template
- The `isProcessing` semaphore
- DOM element lookups (by ID)

### What it should expose

- `initChat({ apiUrl?, fetchFn?, storage? })` — the single entry point with injectable deps
- `escapeHtml(text)` — pure utility, unchanged
- `formatMessage(text, role)` — pure utility, unchanged
- `isRateLimited(storage?)` — pure function with optional storage injection
- `recordRequest(storage?)` — side-effecting function with optional storage injection
- `getRemainingRequests(storage?)` — pure function with optional storage injection
- `RATE_LIMIT_CONFIG` — constants, unchanged

### How callers should migrate

1. No migration needed for production callers — `initChat()` with no args is identical behavior
2. Existing rate-limit tests continue to work — default `storage` parameter is `localStorage`
3. New tests use `initChat({ fetchFn: fake, storage: fake })` for full isolation
4. If staging/dev URL is needed: `initChat({ apiUrl: 'http://localhost:3000' })`
5. The `sendMessage` function moves from module scope into `initChat` closure — this is an internal change with no external impact
