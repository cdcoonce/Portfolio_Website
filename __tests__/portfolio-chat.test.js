'use strict';

import { jest } from '@jest/globals';
import {
  RATE_LIMIT_CONFIG,
  getRemainingRequests,
  isRateLimited,
  recordRequest,
  renderAssistantMarkdown,
  sendMessage,
} from '../src/lib/chat.js';

/** Minimal in-memory Storage stand-in. */
const makeStorage = () => {
  const map = new Map();
  return {
    getItem: (k) => (map.has(k) ? map.get(k) : null),
    setItem: (k, v) => map.set(k, String(v)),
    removeItem: (k) => map.delete(k),
  };
};

describe('rate limiting', () => {
  test('starts with the full quota and decrements per request', () => {
    const storage = makeStorage();
    expect(getRemainingRequests(storage)).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS);
    recordRequest(storage);
    expect(getRemainingRequests(storage)).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS - 1);
    expect(isRateLimited(storage)).toBe(false);
  });

  test('blocks once the quota is exhausted', () => {
    const storage = makeStorage();
    for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_REQUESTS; i += 1) recordRequest(storage);
    expect(getRemainingRequests(storage)).toBe(0);
    expect(isRateLimited(storage)).toBe(true);
  });

  test('ignores timestamps older than the window', () => {
    const storage = makeStorage();
    const stale = Date.now() - RATE_LIMIT_CONFIG.WINDOW_MS - 1000;
    storage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify([stale, stale]));
    expect(getRemainingRequests(storage)).toBe(RATE_LIMIT_CONFIG.MAX_REQUESTS);
  });
});

describe('renderAssistantMarkdown', () => {
  test('escapes HTML then applies bold/italic', () => {
    expect(renderAssistantMarkdown('a <b> **x** *y*')).toBe(
      'a &lt;b&gt; <strong>x</strong> <em>y</em>'
    );
  });

  test('links markdown and bare URLs, and converts newlines', () => {
    expect(renderAssistantMarkdown('[site](https://x.com)')).toContain(
      '<a href="https://x.com" target="_blank" rel="noopener">site</a>'
    );
    expect(renderAssistantMarkdown('line1\nline2')).toBe('line1<br>line2');
  });
});

describe('sendMessage', () => {
  test('posts the conversation and returns the response text', async () => {
    const fetchFn = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ response: 'hi there' }),
    });
    const out = await sendMessage([{ role: 'user', content: 'hi' }], {
      apiUrl: 'https://api.test/',
      fetchFn,
    });
    expect(out).toBe('hi there');
    expect(fetchFn).toHaveBeenCalledWith(
      'https://api.test/',
      expect.objectContaining({ method: 'POST' })
    );
  });

  test('throws on a non-OK status', async () => {
    const fetchFn = jest.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ error: 'boom' }),
    });
    await expect(sendMessage([], { apiUrl: 'https://api.test/', fetchFn })).rejects.toThrow('boom');
  });
});
