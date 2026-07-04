// @ts-check
/**
 * Chat client for Charles's AI assistant.
 * Pure logic + network call ported verbatim from the previous vanilla site
 * (WebContent/js/chat.js) so the existing Lambda integration and its tests
 * carry over unchanged. The React <AskAI> island consumes these functions.
 */

'use strict';

/** Rate limit configuration. */
export const RATE_LIMIT_CONFIG = {
  MAX_REQUESTS: 25,
  WINDOW_MS: 60 * 60 * 1000, // 1 hour
  STORAGE_KEY: 'chat_rate_limit',
};

/** Lambda Function URL for the assistant backend. */
export const LAMBDA_URL = 'https://a4qby7o6wqmq7rpb6rorezbc7u0tsyhc.lambda-url.us-west-1.on.aws/';

/**
 * Gets non-expired request timestamps from storage.
 * @param {Storage} [storage=localStorage]
 * @returns {number[]}
 */
const getValidTimestamps = (storage = localStorage) => {
  try {
    const raw = storage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY);
    if (!raw) return [];
    const timestamps = JSON.parse(raw);
    const cutoff = Date.now() - RATE_LIMIT_CONFIG.WINDOW_MS;
    return timestamps.filter((/** @type {number} */ t) => t > cutoff);
  } catch {
    return [];
  }
};

/**
 * Checks if the user has exceeded the rate limit.
 * @param {Storage} [storage=localStorage]
 * @returns {boolean}
 */
export const isRateLimited = (storage = localStorage) =>
  getValidTimestamps(storage).length >= RATE_LIMIT_CONFIG.MAX_REQUESTS;

/**
 * Records a new request timestamp in storage.
 * @param {Storage} [storage=localStorage]
 */
export const recordRequest = (storage = localStorage) => {
  const timestamps = getValidTimestamps(storage);
  timestamps.push(Date.now());
  storage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify(timestamps));
};

/**
 * Returns the number of remaining requests in the current window.
 * @param {Storage} [storage=localStorage]
 * @returns {number}
 */
export const getRemainingRequests = (storage = localStorage) =>
  Math.max(0, RATE_LIMIT_CONFIG.MAX_REQUESTS - getValidTimestamps(storage).length);

/**
 * Converts a small subset of markdown to HTML for assistant messages.
 * User text is never passed here — React escapes it on render.
 * @param {string} text
 * @returns {string} HTML string (assistant content is trusted, from the API).
 */
export const renderAssistantMarkdown = (text) =>
  text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(
      /(^|[^"'>])(https?:\/\/[^\s<]+)/g,
      '$1<a href="$2" target="_blank" rel="noopener">$2</a>'
    )
    .replace(/\n/g, '<br>');

/**
 * Sends the conversation to the Lambda function and returns the reply text.
 * @param {Array<{role: string, content: string}>} messages - Conversation history.
 * @param {Object} [options]
 * @param {string} [options.apiUrl=LAMBDA_URL]
 * @param {typeof fetch} [options.fetchFn]
 * @returns {Promise<string>}
 * @throws {Error} On non-OK status or transport failure.
 */
export const sendMessage = async (messages, { apiUrl = LAMBDA_URL, fetchFn } = {}) => {
  const doFetch = fetchFn || globalThis.fetch;
  const response = await doFetch(apiUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `Request failed (${response.status})`);
  }

  const data = await response.json();
  return data.response;
};
