"""Contact tab: heading, contact-card grid, and the expected outbound links.

The Contact panel renders a small grid of <a class="contact-card"> links (email,
LinkedIn, GitHub, resume). Cards navigate away / open new tabs, so we assert on
their hrefs and never click them.
"""

import pytest

from helpers import CONTACT_CARD_COUNT, switch_tab

pytestmark = pytest.mark.e2e


def test_contact_title(page):
    switch_tab(page, "contact")
    title = page.locator("h2.contact__title")
    assert title.is_visible()
    assert title.inner_text() == "Get in touch"


def test_contact_card_count(page):
    switch_tab(page, "contact")
    assert page.locator('[data-testid="contact-card"]').count() == CONTACT_CARD_COUNT


def test_contact_links_cover_expected_channels(page):
    switch_tab(page, "contact")
    cards = page.locator('[data-testid="contact-card"]')
    hrefs = [cards.nth(i).get_attribute("href") for i in range(cards.count())]
    assert any(h and h.startswith("mailto:") for h in hrefs)
    assert any(h and "linkedin.com" in h for h in hrefs)
    assert any(h and "github.com" in h for h in hrefs)
    assert any(h and h.lower().endswith(".pdf") for h in hrefs)
