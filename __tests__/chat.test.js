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
    localStorage.setItem(
      RATE_LIMIT_CONFIG.STORAGE_KEY,
      JSON.stringify([expired]),
    );
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
