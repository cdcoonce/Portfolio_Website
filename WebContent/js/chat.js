'use strict';

/** Rate limit configuration. */
export const RATE_LIMIT_CONFIG = {
  MAX_REQUESTS: 25,
  WINDOW_MS: 60 * 60 * 1000, // 1 hour
  STORAGE_KEY: 'chat_rate_limit',
};

/**
 * Lambda Function URL — replace with your actual URL after deployment.
 * See docs/plans/chat-agent/aws-setup.md Step 8.
 */
const LAMBDA_URL = 'https://a4qby7o6wqmq7rpb6rorezbc7u0tsyhc.lambda-url.us-west-1.on.aws/';

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
 * Gets non-expired request timestamps from storage.
 *
 * @param {Storage} storage - Storage backend (defaults to localStorage).
 * @returns {number[]} Timestamps within the current rate limit window.
 */
const getValidTimestamps = (storage = localStorage) => {
  try {
    const raw = storage.getItem(RATE_LIMIT_CONFIG.STORAGE_KEY);
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
 * @param {Storage} [storage=localStorage] - Storage backend for rate limit data.
 * @returns {boolean} True if rate limited.
 */
export const isRateLimited = (storage = localStorage) => {
  return getValidTimestamps(storage).length >= RATE_LIMIT_CONFIG.MAX_REQUESTS;
};

/**
 * Records a new request timestamp in storage.
 *
 * @param {Storage} [storage=localStorage] - Storage backend for rate limit data.
 */
export const recordRequest = (storage = localStorage) => {
  const timestamps = getValidTimestamps(storage);
  timestamps.push(Date.now());
  storage.setItem(RATE_LIMIT_CONFIG.STORAGE_KEY, JSON.stringify(timestamps));
};

/**
 * Returns the number of remaining requests in the current window.
 *
 * @param {Storage} [storage=localStorage] - Storage backend for rate limit data.
 * @returns {number} Remaining requests (0 or positive).
 */
export const getRemainingRequests = (storage = localStorage) => {
  return Math.max(0, RATE_LIMIT_CONFIG.MAX_REQUESTS - getValidTimestamps(storage).length);
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
  if (role === 'user') {
    return `<div class="chat-message ${role}"><p>${escapeHtml(text)}</p></div>`;
  }
  // Convert markdown to HTML for assistant messages
  const html = text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(
      /(^|[^"'>])(https?:\/\/[^\s<]+)/g,
      '$1<a href="$2" target="_blank" rel="noopener">$2</a>'
    )
    .replace(/\n/g, '<br>');
  return `<div class="chat-message ${role}"><p>${html}</p></div>`;
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
 * @param {Array<{role: string, content: string}>} messages - Conversation history.
 * @param {Object} options - Send options.
 * @param {string} options.apiUrl - API endpoint URL.
 * @param {Function} options.fetchFn - Fetch implementation.
 * @returns {Promise<string>} The assistant's response text.
 * @throws {Error} If the request fails or returns a non-OK status.
 */
const sendMessage = async (messages, { apiUrl, fetchFn }) => {
  const response = await fetchFn(apiUrl, {
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

// --- DOM Orchestrator ---

/**
 * Initializes the chat agent UI and event handlers.
 *
 * Wires up the send button and Enter key to submit messages,
 * displays responses, and manages rate limiting UI.
 * Only runs when the required DOM elements exist.
 *
 * @param {Object} [options] - Optional dependency overrides.
 * @param {string} [options.apiUrl] - API endpoint URL (defaults to LAMBDA_URL).
 * @param {Function} [options.fetchFn] - Fetch implementation (defaults to global fetch).
 * @param {Storage} [options.storage] - Storage backend (defaults to localStorage).
 */
export function initChat({ apiUrl = LAMBDA_URL, fetchFn, storage = localStorage } = {}) {
  const resolvedFetch = fetchFn || globalThis.fetch;
  const chatInput = document.getElementById('chat-input');
  const chatSend = document.getElementById('chat-send');
  const chatMessages = document.getElementById('chat-messages');
  const chatRateLimit = document.getElementById('chat-rate-limit');

  if (!chatInput || !chatSend || !chatMessages) {
    return;
  }

  let isProcessing = false;
  const conversationHistory = [
    {
      role: 'assistant',
      content: "Hi! I'm Charles's AI assistant. Ask me about his projects, skills, or experience.",
    },
  ];

  /** Appends HTML to the messages container and scrolls to bottom. */
  const appendMessage = (html) => {
    chatMessages.insertAdjacentHTML('beforeend', html);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  /** Updates the rate limit warning text and disables input at zero. */
  const updateRateLimitDisplay = () => {
    const remaining = getRemainingRequests(storage);
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

    if (isRateLimited(storage)) {
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
      recordRequest(storage);
      conversationHistory.push({ role: 'user', content: message });
      const response = await sendMessage(conversationHistory, { apiUrl, fetchFn: resolvedFetch });

      // Remove loading indicator
      const loading = document.getElementById('chat-loading');
      if (loading) loading.remove();

      conversationHistory.push({ role: 'assistant', content: response });

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
