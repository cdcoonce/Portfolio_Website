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
        cards = soup.find_all(class_='project-card')
        assert len(cards) == 17, f'Expected 17 project cards, found {len(cards)}'
        for card in cards:
            content = card.find('div', class_='card-content')
            desc = content.find('p') if content else None
            title = card.find('h3')
            title_text = title.get_text(strip=True) if title else 'unknown'
            assert desc and desc.get_text(strip=True), f'Missing description in card: {title_text}'

    def test_featured_cards_exist(self, soup):
        cards = soup.find_all(class_='project-card')
        featured = [c for c in cards if 'featured' in c.get('class', [])]
        assert len(featured) >= 3, f'Expected at least 3 featured cards, found {len(featured)}'

    def test_project_cards_are_anchor_elements(self, soup):
        cards = soup.find_all(class_='project-card')
        assert len(cards) == 17, f'Expected 17 project cards, found {len(cards)}'
        for card in cards:
            title = card.find('h3')
            title_text = title.get_text(strip=True) if title else 'unknown'
            assert card.name == 'a', f'Card is <{card.name}>, expected <a>: {title_text}'
            assert card.get('href'), f'Card link missing href: {title_text}'

    def test_no_learn_more_buttons_in_cards(self, soup):
        for card in soup.find_all(class_='project-card'):
            btn = card.find(class_='btn')
            title = card.find('h3')
            title_text = title.get_text(strip=True) if title else 'unknown'
            assert btn is None, f'Unexpected .btn found in card: {title_text}'
