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

    def test_projects_grid_container_exists(self, soup):
        grid = soup.find('div', class_='projects-grid')
        assert grid is not None, 'Missing .projects-grid container'

    def test_data_page_attribute(self, soup):
        body = soup.find('body')
        assert body.get('data-page') == 'home', 'index.html body must have data-page="home"'

    def test_view_all_link_exists(self, soup):
        link = soup.find('a', class_='view-all-link')
        assert link is not None, 'View All Projects link not found'
        assert 'projects.html' in link['href']

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

    def test_projects_page_has_grid_container(self, projects_soup):
        grid = projects_soup.find('div', class_='projects-grid')
        assert grid is not None, 'Projects page must have .projects-grid container'

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
    """Validate the chat agent HTML structure (embedded in profile/hero section)."""

    def test_chat_agent_exists(self, soup):
        chat = soup.find(id='chat-agent')
        assert chat is not None, 'Missing element with id="chat-agent"'

    def test_chat_agent_inside_profile(self, soup):
        profile = soup.find('section', id='profile')
        assert profile is not None, 'Missing <section id="profile">'
        chat = profile.find(id='chat-agent')
        assert chat is not None, 'chat-agent must be inside the profile section'

    def test_chat_has_heading(self, soup):
        chat = soup.find(id='chat-agent')
        assert chat is not None
        h2 = chat.find('h2')
        assert h2 is not None, 'Chat section missing <h2> heading'

    def test_chat_input_exists(self, soup):
        chat = soup.find(id='chat-agent')
        assert chat is not None
        input_el = chat.find('input', id='chat-input')
        assert input_el is not None, 'Missing chat input field'

    def test_chat_send_button_exists(self, soup):
        chat = soup.find(id='chat-agent')
        assert chat is not None
        btn = chat.find('button', id='chat-send')
        assert btn is not None, 'Missing chat send button'

    def test_chat_messages_container_exists(self, soup):
        chat = soup.find(id='chat-agent')
        assert chat is not None
        messages = chat.find('div', id='chat-messages')
        assert messages is not None, 'Missing chat messages container'

    def test_chat_input_has_aria_label(self, soup):
        input_el = soup.find('input', id='chat-input')
        assert input_el is not None
        assert input_el.get('aria-label'), 'Chat input missing aria-label'

    def test_chat_send_button_has_aria_label(self, soup):
        btn = soup.find('button', id='chat-send')
        assert btn is not None
        assert btn.get('aria-label'), 'Chat send button missing aria-label'
