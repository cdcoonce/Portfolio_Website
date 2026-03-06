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
        assert soup.find('header'), 'Missing <header>'
        assert soup.find('main'), 'Missing <main>'
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
        assert len(featured) == 4, f'Expected 4 featured cards, found {len(featured)}'

    def test_data_page_attribute(self, soup):
        body = soup.find('body')
        assert body.get('data-page') == 'home', 'index.html body must have data-page="home"'

    def test_view_all_link_exists(self, soup):
        link = soup.find('a', class_='view-all-link')
        assert link is not None, 'View All Projects link not found'
        assert 'projects.html' in link['href']

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

    def test_no_inline_scripts_in_body(self, soup):
        """Ensure no inline <script> tags exist in the body (external src scripts are allowed)."""
        body = soup.find('body')
        inline_scripts = [s for s in body.find_all('script') if not s.get('src')]
        assert len(inline_scripts) == 0, (
            f'{len(inline_scripts)} inline script(s) found in body'
        )


@pytest.fixture(scope='module')
def projects_soup():
    html = Path('projects.html').read_text()
    return BeautifulSoup(html, 'html.parser')


@pytest.mark.validation
class TestProjectsPageValidation:
    def test_projects_page_exists(self):
        assert Path('projects.html').is_file(), 'projects.html must exist at project root'

    def test_projects_page_has_all_17_cards(self, projects_soup):
        cards = projects_soup.find_all(class_='project-card')
        assert len(cards) == 17, f'Expected 17 project cards, found {len(cards)}'

    def test_projects_page_has_filter_buttons(self, projects_soup):
        tags = projects_soup.find_all('button', class_='skill-tag')
        assert len(tags) > 0, 'Projects page must have skill filter buttons'

    def test_projects_page_has_data_page_attribute(self, projects_soup):
        body = projects_soup.find('body')
        assert body.get('data-page') == 'projects', 'projects.html body must have data-page="projects"'

    def test_projects_page_has_featured_filter(self, projects_soup):
        featured = projects_soup.find('button', attrs={'data-filter': 'featured'})
        assert featured is not None, 'Projects page must have a Featured filter button'

    def test_projects_page_has_semantic_structure(self, projects_soup):
        assert projects_soup.find('header'), 'Missing <header>'
        assert projects_soup.find('main'), 'Missing <main>'
        assert projects_soup.find('nav'), 'Missing <nav>'
        assert projects_soup.find('footer'), 'Missing <footer>'


@pytest.mark.validation
class TestChatSectionValidation:
    """Validate the chat agent section HTML structure."""

    def test_chat_section_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None, 'Missing <section id="chat-agent">'

    def test_chat_section_has_heading(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        h2 = section.find('h2')
        assert h2 is not None, 'Chat section missing <h2> heading'

    def test_chat_section_between_projects_and_testimonials(self, soup):
        sections = [s.get('id') for s in soup.find_all('section') if s.get('id')]
        assert 'chat-agent' in sections, 'chat-agent section not found'
        projects_idx = sections.index('projects')
        chat_idx = sections.index('chat-agent')
        testimonials_idx = sections.index('testimonials')
        assert projects_idx < chat_idx < testimonials_idx, (
            f'Section order wrong: projects={projects_idx}, chat={chat_idx}, testimonials={testimonials_idx}'
        )

    def test_chat_input_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        input_el = section.find('input', id='chat-input')
        assert input_el is not None, 'Missing chat input field'

    def test_chat_send_button_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        btn = section.find('button', id='chat-send')
        assert btn is not None, 'Missing chat send button'

    def test_chat_messages_container_exists(self, soup):
        section = soup.find('section', id='chat-agent')
        assert section is not None
        messages = section.find('div', id='chat-messages')
        assert messages is not None, 'Missing chat messages container'

    def test_chat_input_has_aria_label(self, soup):
        input_el = soup.find('input', id='chat-input')
        assert input_el is not None
        assert input_el.get('aria-label'), 'Chat input missing aria-label'

    def test_chat_send_button_has_aria_label(self, soup):
        btn = soup.find('button', id='chat-send')
        assert btn is not None
        assert btn.get('aria-label'), 'Chat send button missing aria-label'
