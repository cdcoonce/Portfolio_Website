"""External-link reachability for the Astro tabbed SPA.

Replaces the retired file-based checker (which parsed a now-deleted index.html).
Hrefs are harvested from the *rendered* SPA: the site is tab-gated and non-active
panels are unmounted, so we drive a page through the hero + Work + Testimonials +
Contact tabs and collect every outbound anchor. Only absolute http(s) URLs are
checked; mailto: and site-relative links (/assets/..., /afk-cockpit/) are skipped.

Some hosts block bots (LinkedIn's 999, GitHub rate-limit 403/429), so those
statuses are tolerated with a warning rather than failing the reachability check.
"""

import warnings

import pytest
import requests

from helpers import switch_tab, wait_hydrated

pytestmark = pytest.mark.slow

# Statuses returned by anti-bot / rate-limit layers, not by broken links.
ACCEPTABLE_STATUSES = {403, 429, 999}
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-e2e link checker)"}


def _collect_hrefs(pg) -> list[str]:
    """Walk the rendered SPA and return every anchor href we can reach."""
    hrefs: list[str] = []

    # Hero (Overview is active on load): GitHub/Resume buttons + email/LinkedIn.
    hero = pg.locator('[data-testid="profile"] a')
    hrefs += [hero.nth(i).get_attribute("href") for i in range(hero.count())]

    # Work: one outbound anchor per project card.
    switch_tab(pg, "work")
    cards = pg.locator('[data-testid="project-card"]')
    hrefs += [cards.nth(i).get_attribute("href") for i in range(cards.count())]

    # Testimonials: single-quote carousel — click each dot to reveal that
    # author's LinkedIn avatar link (dots are safe to click; avatars are not).
    switch_tab(pg, "testimonials")
    dots = pg.locator(".testimonial-card__dots button")
    for i in range(dots.count()):
        dots.nth(i).click()
        avatar = pg.locator("a.testimonial-card__avatar--link")
        if avatar.count():
            hrefs.append(avatar.first.get_attribute("href"))

    # Contact: the outbound card grid (email, LinkedIn, GitHub, resume).
    switch_tab(pg, "contact")
    contact_cards = pg.locator('[data-testid="contact-card"]')
    hrefs += [contact_cards.nth(i).get_attribute("href") for i in range(contact_cards.count())]

    return hrefs


@pytest.fixture(scope="module")
def external_urls(browser, base_url) -> list[str]:
    """Harvest, filter, and dedupe absolute http(s) URLs from the rendered SPA."""
    pg = browser.new_page()
    pg.goto(base_url)
    wait_hydrated(pg)
    try:
        raw = _collect_hrefs(pg)
    finally:
        pg.close()

    urls: list[str] = []
    for href in raw:
        # Keep only absolute http(s); drop mailto: and site-relative links.
        if href and href.startswith(("http://", "https://")) and href not in urls:
            urls.append(href)
    return urls


def test_external_urls_harvested(external_urls):
    assert external_urls, "no external http(s) links harvested from the rendered SPA"
    joined = " ".join(external_urls)
    # Sanity-check the harvest actually reached the known outbound hosts.
    assert "github.com" in joined
    assert "linkedin.com" in joined


def test_external_links_reachable(external_urls):
    for url in external_urls:
        resp = requests.head(url, allow_redirects=True, timeout=15, headers=HEADERS)
        if resp.status_code >= 400:
            resp = requests.get(
                url, allow_redirects=True, timeout=15, headers=HEADERS, stream=True
            )
            resp.close()
        status = resp.status_code
        if status in ACCEPTABLE_STATUSES:
            warnings.warn(f"{url} returned {status} (bot-block/rate-limit); tolerated")
            continue
        assert status < 400, f"{url} returned {status}"
