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

    def test_all_project_cards_have_descriptions(self, soup):
        cards = soup.find_all('div', class_='project-card')
        assert len(cards) == 17, f'Expected 17 project cards, found {len(cards)}'
        for card in cards:
            content = card.find('div', class_='card-content')
            desc = content.find('p') if content else None
            title = card.find('h3')
            title_text = title.get_text(strip=True) if title else 'unknown'
            assert desc and desc.get_text(strip=True), f'Missing description in card: {title_text}'

    def test_featured_cards_exist(self, soup):
        cards = soup.find_all('div', class_='project-card')
        featured = [c for c in cards if 'featured' in c.get('class', [])]
        assert len(featured) >= 3, f'Expected at least 3 featured cards, found {len(featured)}'
