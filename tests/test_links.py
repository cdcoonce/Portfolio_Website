"""Link checking tests — broken link detection."""

import pytest
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_external_links():
    html = Path('index.html').read_text()
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]


@pytest.mark.slow
@pytest.mark.parametrize('url', get_external_links())
def test_external_link_resolves(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.head(url, allow_redirects=True, timeout=10, headers=headers)
    if resp.status_code == 405:
        resp = requests.get(url, allow_redirects=True, timeout=10, headers=headers, stream=True)
        resp.close()
    # LinkedIn returns 999 to block automated requests — not a broken link
    assert resp.status_code < 400 or resp.status_code == 999, f'{url} returned {resp.status_code}'
