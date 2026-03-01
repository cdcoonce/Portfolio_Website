"""HTML validation tests — structure, alt text, no inline styles."""

import pytest
from bs4 import BeautifulSoup
from pathlib import Path


@pytest.fixture(scope='module')
def soup():
    html = Path('index.html').read_text()
    return BeautifulSoup(html, 'html.parser')


@pytest.mark.validation
class TestHTMLValidation:
    def test_all_images_have_alt_text(self, soup):
        for img in soup.find_all('img'):
            assert img.get('alt'), f'Missing alt text: {img}'

    def test_semantic_structure(self, soup):
        assert soup.find('nav'), 'Missing <nav>'
        assert soup.find('footer'), 'Missing <footer>'

    def test_no_inline_styles(self, soup):
        styled = soup.find_all(style=True)
        assert len(styled) == 0, f'{len(styled)} elements with inline styles'
