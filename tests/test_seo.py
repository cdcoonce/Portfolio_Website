"""SEO tests — meta tags, Open Graph, title."""

from bs4 import BeautifulSoup
from pathlib import Path

import pytest

html = Path('index.html').read_text()
soup = BeautifulSoup(html, 'html.parser')


def test_has_title_tag():
    title = soup.find('title')
    assert title, 'Missing <title> tag'
    assert len(title.string.strip()) > 0, 'Title tag is empty'


def test_has_meta_description():
    meta = soup.find('meta', attrs={'name': 'description'})
    assert meta, 'Missing meta description'
    content = meta.get('content', '')
    assert len(content) >= 50, f'Meta description too short ({len(content)} chars)'


@pytest.mark.xfail(reason='Open Graph tags not yet implemented')
def test_has_open_graph_tags():
    assert soup.find('meta', property='og:title'), 'Missing og:title'
    assert soup.find('meta', property='og:description'), 'Missing og:description'
    assert soup.find('meta', property='og:image'), 'Missing og:image'
