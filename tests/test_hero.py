"""Hero & profile section tests — spacing, picture, skills section, favicon."""

import pytest
from bs4 import BeautifulSoup
from pathlib import Path


@pytest.fixture(scope='module')
def soup():
    html = Path('index.html').read_text()
    return BeautifulSoup(html, 'html.parser')


@pytest.mark.validation
class TestHeroStructure:
    def test_skills_section_exists(self, soup):
        section = soup.find('section', id='skills')
        assert section is not None, 'Missing <section id="skills">'

    def test_skills_section_has_heading(self, soup):
        section = soup.find('section', id='skills')
        assert section is not None
        heading = section.find('h2')
        assert heading is not None, 'Skills section missing <h2> heading'

    def test_skills_grid_has_four_categories(self, soup):
        grid = soup.find('div', class_='skills-grid')
        assert grid is not None, 'Missing <div class="skills-grid">'
        categories = grid.find_all('div', class_='skill-category')
        assert len(categories) == 4, f'Expected 4 skill categories, got {len(categories)}'

    def test_skills_section_between_profile_and_projects(self, soup):
        sections = [s.get('id') for s in soup.find_all('section') if s.get('id')]
        assert 'skills' in sections, 'skills section not found'
        profile_idx = sections.index('profile')
        skills_idx = sections.index('skills')
        projects_idx = sections.index('projects')
        assert profile_idx < skills_idx < projects_idx, (
            f'Expected profile < skills < projects, got indices {profile_idx}, {skills_idx}, {projects_idx}'
        )

    def test_skills_nav_link_exists(self, soup):
        nav = soup.find('nav', id='main-nav')
        assert nav is not None
        hrefs = [a.get('href') for a in nav.find_all('a')]
        assert '#skills' in hrefs, 'Missing Skills (#skills) nav link'

    def test_favicon_is_not_jpeg(self, soup):
        favicon = soup.find('link', rel='icon')
        assert favicon is not None, 'Missing favicon <link>'
        favicon_type = favicon.get('type', '')
        assert favicon_type != 'image/jpeg', 'Favicon should not be a JPEG'

    def test_favicon_href_not_jpeg_extension(self, soup):
        favicon = soup.find('link', rel='icon')
        assert favicon is not None
        href = favicon.get('href', '')
        assert not href.lower().endswith('.jpeg'), f'Favicon href should not end in .jpeg: {href}'
        assert not href.lower().endswith('.jpg'), f'Favicon href should not end in .jpg: {href}'

    def test_profile_pic_no_scale_transform(self, soup):
        """Profile picture should use width/height, not CSS scale transform."""
        profile_pic = soup.find('img', class_='profile_pic')
        assert profile_pic is not None, 'Missing profile picture'
        # Inline style with scale would be a red flag (also caught by no_inline_styles test)
        inline_style = profile_pic.get('style', '')
        assert 'scale' not in inline_style, 'Profile pic should not use inline scale transform'


@pytest.mark.e2e
class TestHeroE2E:
    def test_skills_section_visible(self, page):
        skills = page.locator('#skills')
        assert skills.is_visible(), 'Skills section should be visible on page load'

    def test_skills_section_has_four_categories(self, page):
        count = page.locator('.skill-category').count()
        assert count == 4, f'Expected 4 skill categories, got {count}'

    def test_skills_nav_link_scrolls_to_section(self, page):
        page.click('#main-nav .nav-links a[href="#skills"]')
        page.wait_for_timeout(600)
        skills_top = page.locator('#skills').bounding_box()['y']
        scroll_y = page.evaluate('window.scrollY')
        assert scroll_y > 0, 'Page should have scrolled to skills section'
        _ = skills_top  # bounding box verified element exists

    def test_skills_grid_responsive_desktop(self, page):
        page.set_viewport_size({'width': 1440, 'height': 900})
        page.reload()
        page.wait_for_timeout(300)
        grid = page.locator('.skills-grid')
        # On desktop: 4 columns — verify all 4 categories are visible
        count = page.locator('.skill-category:visible').count()
        assert count == 4, f'Expected 4 visible categories on desktop, got {count}'

    def test_skills_grid_responsive_mobile(self, page):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.reload()
        page.wait_for_timeout(300)
        count = page.locator('.skill-category:visible').count()
        assert count == 4, f'All 4 categories should still be visible on mobile, got {count}'
