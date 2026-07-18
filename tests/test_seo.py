"""Static-HTML SEO checks for the built Astro SPA.

These parse the served ``dist/index.html`` directly (no browser, no hydration)
to assert the document head is search/social ready: title, meta description,
Open Graph + Twitter cards, canonical link, and an SVG favicon. Open Graph is
now emitted by Base.astro, so those assertions must pass (no xfail).
"""

import pytest
import requests
from bs4 import BeautifulSoup

pytestmark = pytest.mark.validation


@pytest.fixture(scope="module")
def soup(base_url):
    """Parse the raw served homepage HTML (pre-hydration)."""
    html = requests.get(base_url, timeout=10).text
    return BeautifulSoup(html, "html.parser")


def test_has_title_tag(soup):
    title = soup.find("title")
    assert title is not None, "Missing <title> tag"
    assert len(title.get_text(strip=True)) > 0, "Title tag is empty"


def test_has_meta_description(soup):
    meta = soup.find("meta", attrs={"name": "description"})
    assert meta is not None, "Missing meta description"
    content = meta.get("content", "")
    assert len(content) >= 50, f"Meta description too short ({len(content)} chars)"


def test_has_open_graph_tags(soup):
    for prop in ("og:title", "og:description", "og:image", "og:type", "og:url"):
        tag = soup.find("meta", attrs={"property": prop})
        assert tag is not None, f"Missing {prop}"
        assert tag.get("content", "").strip(), f"Empty content for {prop}"


def test_has_twitter_card(soup):
    tag = soup.find("meta", attrs={"name": "twitter:card"})
    assert tag is not None, "Missing meta twitter:card"
    assert tag.get("content", "").strip(), "Empty twitter:card content"


def test_has_canonical_link(soup):
    canonical = soup.find("link", attrs={"rel": "canonical"})
    assert canonical is not None, "Missing <link rel=\"canonical\">"
    assert canonical.get("href", "").strip(), "Canonical link has no href"


def test_favicon_is_svg(soup):
    icon = soup.find("link", attrs={"rel": "icon"})
    assert icon is not None, "Missing <link rel=\"icon\">"
    href = icon.get("href", "")
    assert href.endswith(".svg"), f"Favicon is not an SVG: {href}"
