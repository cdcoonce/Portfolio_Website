"""Static-HTML semantic/structure checks for the Astro tabbed SPA.

Replaces the retired test_validation.py. These run without a browser: they GET
the served homepage and parse the raw shell with BeautifulSoup, so they only see
the Overview tab's SSR markup plus the shared shell (header/nav/footer). Retired
assertions (data-page, no-inline-scripts, projects.html) are intentionally gone:
Astro injects hydration scripts and there is no per-page routing.
"""

import pytest
import requests
from bs4 import BeautifulSoup

pytestmark = pytest.mark.validation


@pytest.fixture(scope="module")
def soup(base_url):
    """Parse the served homepage shell once for the module."""
    html = requests.get(base_url, timeout=30).text
    return BeautifulSoup(html, "html.parser")


def test_exactly_one_main(soup):
    assert len(soup.find_all("main")) == 1


def test_profile_header_present(soup):
    header = soup.find("header", class_="profile") or soup.select_one(
        '[data-testid="profile"]'
    )
    assert header is not None


def test_nav_contains_tabbar(soup):
    nav = soup.find("nav")
    assert nav is not None
    tabbar = soup.select_one('[data-testid="tabbar"]')
    assert tabbar is not None
    # The tabbar is the (or lives inside the) nav landmark.
    assert tabbar.name == "nav" or tabbar.find_parent("nav") is not None


def test_footer_present(soup):
    footer = soup.find("footer")
    assert footer is not None
    assert soup.select_one('[data-testid="site-footer"]') is not None


def test_images_have_alt_attribute(soup):
    images = soup.find_all("img")
    assert images, "expected at least one <img> in the static shell"
    # Decorative icons legitimately use alt="" — require the attribute to EXIST
    # (empty string allowed), not that it be non-empty.
    for img in images:
        assert img.get("alt") is not None


def test_h1_is_charles_coonce(soup):
    h1 = soup.find("h1")
    assert h1 is not None
    assert "Charles Coonce" in h1.get_text(strip=True)
