"""Navigation tests — sticky nav, hamburger menu, back-to-top button."""

import pytest
from bs4 import BeautifulSoup
from pathlib import Path


@pytest.fixture(scope='module')
def soup():
    html = Path('index.html').read_text()
    return BeautifulSoup(html, 'html.parser')


@pytest.mark.validation
class TestNavStructure:
    def test_nav_element_exists(self, soup):
        nav = soup.find('nav', id='main-nav')
        assert nav is not None, 'Missing <nav id="main-nav">'

    def test_nav_contains_logo_link(self, soup):
        nav = soup.find('nav', id='main-nav')
        assert nav is not None
        logo = nav.find('a', class_='logo')
        assert logo is not None, 'Missing logo <a> inside nav'
        assert logo.get('href') == '#profile', 'Logo link should point to #profile'

    def test_nav_links_present(self, soup):
        nav = soup.find('nav', id='main-nav')
        assert nav is not None
        links = nav.find('ul', class_='nav-links')
        assert links is not None, 'Missing <ul class="nav-links">'
        hrefs = [a.get('href') for a in links.find_all('a')]
        assert '#profile' in hrefs, 'Missing Home (#profile) nav link'
        assert '#projects' in hrefs, 'Missing Projects (#projects) nav link'
        assert '#testimonials' in hrefs, 'Missing Testimonials (#testimonials) nav link'
        assert '#contact' in hrefs, 'Missing Contact (#contact) nav link'

    def test_hamburger_button_exists(self, soup):
        toggle = soup.find('button', class_='nav-toggle')
        assert toggle is not None, 'Missing hamburger <button class="nav-toggle">'

    def test_hamburger_has_aria_label(self, soup):
        toggle = soup.find('button', class_='nav-toggle')
        assert toggle is not None
        assert toggle.get('aria-label') == 'Toggle menu', 'Hamburger missing aria-label="Toggle menu"'

    def test_hamburger_has_aria_expanded(self, soup):
        toggle = soup.find('button', class_='nav-toggle')
        assert toggle is not None
        assert toggle.get('aria-expanded') is not None, 'Hamburger missing aria-expanded attribute'

    def test_back_to_top_button_exists(self, soup):
        btn = soup.find('button', class_='back-to-top')
        assert btn is not None, 'Missing <button class="back-to-top">'

    def test_back_to_top_has_aria_label(self, soup):
        btn = soup.find('button', class_='back-to-top')
        assert btn is not None
        assert btn.get('aria-label'), 'Back-to-top button missing aria-label'

    def test_logo_not_standalone_in_profile(self, soup):
        """Logo <div> should have moved to nav; profile section should not contain <div class="logo">."""
        profile = soup.find('section', id='profile')
        assert profile is not None
        standalone_logo = profile.find('div', class_='logo')
        assert standalone_logo is None, '.logo div should not exist inside #profile (moved to nav)'


@pytest.mark.e2e
class TestNavE2E:
    def test_nav_is_sticky(self, page):
        """Nav should remain visible after scrolling."""
        page.evaluate('window.scrollTo(0, 800)')
        nav = page.locator('#main-nav')
        assert nav.is_visible(), 'Nav should be visible after scrolling'

    def test_nav_home_link_scrolls_to_profile(self, page):
        """Clicking Home nav link should navigate to #profile."""
        page.click('#main-nav .nav-links a[href="#profile"]')
        page.wait_for_timeout(600)
        scroll_y = page.evaluate('window.scrollY')
        assert scroll_y < 100, f'Expected to scroll near top, got scrollY={scroll_y}'

    def test_back_to_top_hidden_at_page_top(self, page):
        """Back-to-top button should not be visible when at page top."""
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(400)
        btn = page.locator('.back-to-top')
        opacity = btn.evaluate('el => getComputedStyle(el).opacity')
        assert float(opacity) == 0, f'Back-to-top should be invisible at top, opacity={opacity}'

    def test_back_to_top_visible_after_scroll(self, page):
        """Back-to-top button should gain .visible class once the testimonials section is in view."""
        page.locator('#testimonials').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        btn = page.locator('.back-to-top')
        has_visible = btn.evaluate('el => el.classList.contains("visible")')
        assert has_visible, 'Back-to-top should have .visible class when testimonials section is in view'

    def test_back_to_top_click_scrolls_to_top(self, page):
        """Clicking back-to-top should scroll page back to top."""
        page.locator('#testimonials').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.click('.back-to-top')
        page.wait_for_timeout(1200)
        scroll_y = page.evaluate('window.scrollY')
        assert scroll_y < 100, f'Expected scrollY near 0 after back-to-top click, got {scroll_y}'

    def test_hamburger_toggles_nav_menu(self, page):
        """Hamburger button should show/hide nav links on mobile viewport."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_timeout(300)
        nav_links = page.locator('.nav-links')
        # Menu should be closed initially
        assert not nav_links.is_visible(), 'Nav links should be hidden on mobile initially'
        page.click('.nav-toggle')
        page.wait_for_timeout(300)
        assert nav_links.is_visible(), 'Nav links should be visible after hamburger click'
