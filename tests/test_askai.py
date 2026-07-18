"""Ask AI tab: chat panel wired to the live Lambda assistant.

The tab issues a real network call to the Lambda Function URL, so every test
stubs ``**/*.on.aws/**`` and clears (or seeds) localStorage BEFORE navigation.
That means building the page by hand from the ``browser`` + ``base_url``
fixtures rather than using the pre-navigated ``page`` fixture. Pure rate-limit /
markdown logic is covered by the Jest unit suite; here we assert DOM wiring:
greeting render, send-on-click, send-on-Enter, blank guard, the error bubble,
and the rate-limit lockout.
"""

import json

import pytest

from helpers import switch_tab, wait_hydrated

pytestmark = pytest.mark.e2e

STUB_REPLY = "Charles built several Python projects."
ERROR_TEXT = "Sorry, something went wrong. Please try again."


def _reply_ok(route):
    """Fulfill the Lambda call with a successful, stubbed assistant reply."""
    route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"response": STUB_REPLY}),
    )


def _reply_500(route):
    """Fulfill the Lambda call with a server error to exercise the catch path."""
    route.fulfill(
        status=500,
        content_type="application/json",
        body=json.dumps({"error": "boom"}),
    )


def _open_askai(browser, base_url, *, handler=_reply_ok, init_script="window.localStorage.clear();"):
    """Build a fresh, hydrated page on the Ask AI tab.

    Network stubbing and localStorage seeding are installed BEFORE ``goto`` so
    they are in place for the island's first render.
    """
    pg = browser.new_page()
    pg.route("**/*.on.aws/**", handler)  # set up BEFORE goto
    pg.add_init_script(init_script)
    pg.goto(base_url)
    wait_hydrated(pg)
    switch_tab(pg, "ai")
    return pg


def test_structure_and_greeting(browser, base_url):
    pg = _open_askai(browser, base_url)
    try:
        assert pg.locator('[data-testid="askai"]').is_visible()
        assert pg.locator('[data-testid="askai-input"]').count() == 1
        assert pg.locator('[data-testid="askai-send"]').count() == 1
        messages = pg.locator('[data-testid="askai-messages"]')
        assert messages.is_visible()
        assert messages.get_attribute("role") == "log"
        assert messages.get_attribute("aria-live") == "polite"

        # The conversation opens with exactly one assistant greeting bubble.
        greeting = pg.locator(".bubble--assistant")
        assert greeting.count() == 1
        assert "Charles" in greeting.first.inner_text()
        assert pg.locator('[data-testid="msg-user"]').count() == 0
    finally:
        pg.close()


def test_send_appends_user_and_assistant_bubbles(browser, base_url):
    pg = _open_askai(browser, base_url)
    try:
        question = "What has Charles built with Python?"
        pg.fill('[data-testid="askai-input"]', question)
        pg.click('[data-testid="askai-send"]')

        pg.wait_for_selector('[data-testid="msg-user"]')
        assert pg.locator('[data-testid="msg-user"]').count() == 1
        assert pg.locator(".bubble--user").inner_text() == question

        pg.wait_for_selector(f'.bubble--assistant:has-text("{STUB_REPLY}")')
    finally:
        pg.close()


def test_enter_key_sends(browser, base_url):
    pg = _open_askai(browser, base_url)
    try:
        question = "Tell me about Charles's dashboards."
        inp = pg.locator('[data-testid="askai-input"]')
        inp.fill(question)
        inp.press("Enter")

        pg.wait_for_selector('[data-testid="msg-user"]')
        assert pg.locator(".bubble--user").inner_text() == question
        pg.wait_for_selector(f'.bubble--assistant:has-text("{STUB_REPLY}")')
    finally:
        pg.close()


def test_blank_input_does_not_send(browser, base_url):
    pg = _open_askai(browser, base_url)
    try:
        pg.fill('[data-testid="askai-input"]', "   ")
        pg.click('[data-testid="askai-send"]')
        # Whitespace-only text is trimmed away and never reaches the transcript.
        assert pg.locator('[data-testid="msg-user"]').count() == 0
    finally:
        pg.close()


def test_error_shows_failure_bubble(browser, base_url):
    pg = _open_askai(browser, base_url, handler=_reply_500)
    try:
        pg.fill('[data-testid="askai-input"]', "This request will fail.")
        pg.click('[data-testid="askai-send"]')
        pg.wait_for_selector(f'.bubble--assistant:has-text("{ERROR_TEXT}")')
    finally:
        pg.close()


def test_rate_limit_locks_input(browser, base_url):
    # Seed the storage window full (25 recent timestamps) before the island
    # mounts, so its rate-limit effect locks the composer on first render.
    seed = (
        "const stamps = Array.from({ length: 25 }, () => Date.now());"
        "window.localStorage.setItem('chat_rate_limit', JSON.stringify(stamps));"
    )
    pg = _open_askai(browser, base_url, init_script=seed)
    try:
        pg.wait_for_function(
            "() => document.querySelector('[data-testid=\"askai-hint\"]')"
            "?.textContent.includes('Rate limit reached')"
        )
        assert pg.locator('[data-testid="askai-input"]').is_disabled()
        assert "Rate limit reached" in pg.locator('[data-testid="askai-hint"]').inner_text()
    finally:
        pg.close()
