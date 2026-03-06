'use strict';

/** Rate limit configuration. */
export const RATE_LIMIT_CONFIG = {
  MAX_REQUESTS: 10,
  WINDOW_MS: 60 * 60 * 1000, // 1 hour
  STORAGE_KEY: 'chat_rate_limit',
};

/**
 * Lambda Function URL — replace with your actual URL after deployment.
 * See docs/plans/chat-agent/aws-setup.md Step 8.
 */
const LAMBDA_URL =
  'https://YOUR_FUNCTION_URL.lambda-url.us-east-1.on.aws/';

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
  localStorage.setItem(
    RATE_LIMIT_CONFIG.STORAGE_KEY,
    JSON.stringify(timestamps),
  );
};

/**
 * Returns the number of remaining requests in the current window.
 *
 * @returns {number} Remaining requests (0 or positive).
 */
export const getRemainingRequests = () => {
  return Math.max(
    0,
    RATE_LIMIT_CONFIG.MAX_REQUESTS - getValidTimestamps().length,
  );
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
      chatRateLimit.textContent =
        'Rate limit reached. Please try again later.';
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

      appendMessage(
        formatMessage(
          'Sorry, something went wrong. Please try again.',
          'assistant',
        ),
      );
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
