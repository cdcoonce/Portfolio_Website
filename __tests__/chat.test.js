import { jest } from '@jest/globals';
import {
  isRateLimited,
  recordRequest,
  getRemainingRequests,
  formatMessage,
  escapeHtml,
  initChat,
  RATE_LIMIT_CONFIG,
} from '../WebContent/js/chat.js';

// --- Helper: set up the chat DOM elements ---
const setupChatDom = () => {
  document.body.innerHTML = `
    <input id="chat-input" />
    <button id="chat-send">Send</button>
    <div id="chat-messages"></div>
    <div id="chat-rate-limit" hidden></div>
  `;
};

// --- Helper: create a fake storage object ---
const createFakeStorage = (initialData = {}) => {
  const store = { ...initialData };
  return {
    getItem: (key) => (key in store ? store[key] : null),
    setItem: (key, value) => {
      store[key] = String(value);
    },
    removeItem: (key) => {
      delete store[key];
    },
    clear: () => {
      for (const key of Object.keys(store)) delete store[key];
    },
    _store: store,
  };
};

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

describe('Rate Limiting with injected storage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('isRateLimited uses injected storage instead of localStorage', () => {
    const fakeStorage = createFakeStorage();
    expect(isRateLimited(fakeStorage)).toBe(false);

    // Fill up the storage to the limit
    const timestamps = [];
    for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_REQUESTS; i++) {
      timestamps.push(Date.now());
    }
    fakeStorage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify(timestamps));

    expect(isRateLimited(fakeStorage)).toBe(true);
    // localStorage should remain untouched
    expect(isRateLimited()).toBe(false);
  });

  test('recordRequest uses injected storage instead of localStorage', () => {
    const fakeStorage = createFakeStorage();
    recordRequest(fakeStorage);

    const stored = JSON.parse(fakeStorage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY));
    expect(stored).toHaveLength(1);
    // localStorage should remain untouched
    expect(localStorage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY)).toBeNull();
  });

  test('getRemainingRequests uses injected storage instead of localStorage', () => {
    const fakeStorage = createFakeStorage();
    expect(getRemainingRequests(fakeStorage)).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS);

    recordRequest(fakeStorage);
    expect(getRemainingRequests(fakeStorage)).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS - 1);
    // localStorage should still show full remaining
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

describe('initChat', () => {
  beforeEach(() => {
    localStorage.clear();
    document.body.innerHTML = '';
  });

  test('returns early when DOM elements are missing', () => {
    document.body.innerHTML = '<div>no chat elements</div>';
    // Should not throw
    expect(() => initChat()).not.toThrow();
  });

  test('sends message via fake fetch and displays response', async () => {
    setupChatDom();

    const fakeFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ response: 'Hello from the assistant!' }),
    });

    initChat({ fetchFn: fakeFetch, apiUrl: 'https://fake.api/chat' });

    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('chat-send');
    const messages = document.getElementById('chat-messages');

    input.value = 'Hi there';
    sendButton.click();

    // Wait for async fetch to resolve
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(fakeFetch).toHaveBeenCalledWith(
      'https://fake.api/chat',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
    );
    expect(messages.innerHTML).toContain('Hi there');
    expect(messages.innerHTML).toContain('Hello from the assistant!');
  });

  test('displays error message when fetch fails', async () => {
    setupChatDom();

    const fakeFetch = jest.fn().mockRejectedValue(new Error('Network error'));

    initChat({ fetchFn: fakeFetch, apiUrl: 'https://fake.api/chat' });

    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('chat-send');
    const messages = document.getElementById('chat-messages');

    input.value = 'Hi there';
    sendButton.click();

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(messages.innerHTML).toContain('Sorry, something went wrong');
  });

  test('uses injected storage for rate limiting', async () => {
    setupChatDom();

    const fakeStorage = createFakeStorage();
    const fakeFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ response: 'OK' }),
    });

    initChat({ fetchFn: fakeFetch, apiUrl: 'https://fake.api/chat', storage: fakeStorage });

    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('chat-send');

    input.value = 'test message';
    sendButton.click();

    await new Promise((resolve) => setTimeout(resolve, 0));

    // The fake storage should have a recorded request
    const stored = JSON.parse(fakeStorage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY));
    expect(stored).toHaveLength(1);
    // localStorage should remain untouched
    expect(localStorage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY)).toBeNull();
  });

  test('disables input when rate limit is at zero', () => {
    setupChatDom();

    // Pre-fill storage with max requests
    const timestamps = [];
    for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_REQUESTS; i++) {
      timestamps.push(Date.now());
    }
    const fakeStorage = createFakeStorage({
      [RATE_LIMIT_CONFIG.STORAGE_KEY]: JSON.stringify(timestamps),
    });

    initChat({ storage: fakeStorage, apiUrl: 'https://fake.api/chat', fetchFn: jest.fn() });

    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('chat-send');
    const rateLimit = document.getElementById('chat-rate-limit');

    expect(input.disabled).toBe(true);
    expect(sendButton.disabled).toBe(true);
    expect(rateLimit.hidden).toBe(false);
    expect(rateLimit.textContent).toContain('Rate limit reached');
  });

  test('passes full conversation history to fetch', async () => {
    setupChatDom();

    const fakeFetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'First response' }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'Second response' }),
      });

    initChat({ fetchFn: fakeFetch, apiUrl: 'https://fake.api/chat' });

    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('chat-send');

    // Send first message
    input.value = 'First question';
    sendButton.click();
    await new Promise((resolve) => setTimeout(resolve, 0));

    // Send second message
    input.value = 'Second question';
    sendButton.click();
    await new Promise((resolve) => setTimeout(resolve, 0));

    // Second call should include full history
    const secondCallBody = JSON.parse(fakeFetch.mock.calls[1][1].body);
    expect(secondCallBody.messages).toEqual([
      { role: 'assistant', content: expect.stringContaining('AI assistant') },
      { role: 'user', content: 'First question' },
      { role: 'assistant', content: 'First response' },
      { role: 'user', content: 'Second question' },
    ]);
  });

  test('Enter key triggers message send', async () => {
    setupChatDom();

    const fakeFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ response: 'Response' }),
    });

    initChat({ fetchFn: fakeFetch, apiUrl: 'https://fake.api/chat' });

    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');

    input.value = 'Enter key test';
    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(fakeFetch).toHaveBeenCalled();
    expect(messages.innerHTML).toContain('Enter key test');
  });
});
