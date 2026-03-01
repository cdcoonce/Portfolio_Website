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

    def test_contact_section_exists(self, soup):
        contact = soup.find('section', id='contact')
        assert contact is not None, 'Missing <section id="contact">'

    def test_contact_section_has_heading(self, soup):
        contact = soup.find('section', id='contact')
        assert contact is not None, 'Missing <section id="contact">'
        h2 = contact.find('h2')
        assert h2 is not None, 'Contact section missing <h2>'

    def test_contact_section_has_email_link(self, soup):
        contact = soup.find('section', id='contact')
        assert contact is not None, 'Missing <section id="contact">'
        email_link = contact.find('a', href=lambda h: h and h.startswith('mailto:'))
        assert email_link is not None, 'Contact section missing email link'

    def test_contact_section_has_linkedin_link(self, soup):
        contact = soup.find('section', id='contact')
        assert contact is not None, 'Missing <section id="contact">'
        linkedin = contact.find('a', href=lambda h: h and 'linkedin.com' in h)
        assert linkedin is not None, 'Contact section missing LinkedIn link'

    def test_contact_section_has_github_link(self, soup):
        contact = soup.find('section', id='contact')
        assert contact is not None, 'Missing <section id="contact">'
        github = contact.find('a', href=lambda h: h and 'github.com' in h)
        assert github is not None, 'Contact section missing GitHub link'

    def test_testimonials_section_has_h2_heading(self, soup):
        section = soup.find('section', id='testimonials')
        assert section is not None, 'Missing <section id="testimonials">'
        h2 = section.find('h2')
        assert h2 is not None, 'Testimonials section missing <h2> heading'

    def test_projects_section_has_heading(self, soup):
        section = soup.find('section', id='projects')
        assert section is not None, 'Missing <section id="projects">'
        h2 = section.find('h2')
        assert h2 is not None, 'Projects section missing <h2> heading'

    def test_carousel_prev_button_has_aria_label(self, soup):
        btn = soup.find('button', id='prevRec')
        assert btn is not None, 'Missing #prevRec button'
        assert btn.get('aria-label'), '#prevRec button missing aria-label'

    def test_carousel_next_button_has_aria_label(self, soup):
        btn = soup.find('button', id='nextRec')
        assert btn is not None, 'Missing #nextRec button'
        assert btn.get('aria-label'), '#nextRec button missing aria-label'

    def test_testimonials_container_has_aria_live(self, soup):
        container = soup.find('div', class_='testimonials')
        assert container is not None, 'Missing .testimonials div'
        assert container.get('aria-live'), '.testimonials div missing aria-live attribute'
