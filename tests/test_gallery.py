"""E2E gallery tests — filter buttons toggle card visibility."""

import re
import pytest


@pytest.mark.e2e
class TestGallery:
    def test_default_shows_four_featured_cards(self, page):
        # Wait for JS to apply featured filter on load
        page.wait_for_function(
            'document.querySelectorAll(".project-card[style*=\\"none\\"]").length > 0'
        )
        visible = page.locator('.project-card:visible')
        assert visible.count() == 4, f'Expected 4 visible cards on load, got {visible.count()}'
        for i in range(4):
            classes = visible.nth(i).get_attribute('class')
            assert 'featured' in classes, f'Visible card {i} is not featured'

    def test_filter_shows_only_matching_cards(self, page):
        page.click('[data-filter="python"]')
        all_cards = page.locator('.project-card')
        total = all_cards.count()
        assert total > 0, 'No project cards found in DOM'
        visible_count = 0
        for i in range(total):
            card = all_cards.nth(i)
            tags = (card.get_attribute('data-tags') or '').split(',')
            if card.is_visible():
                visible_count += 1
                assert 'python' in tags, f'Non-python card is visible: tags={tags}'
        assert visible_count <= 4, f'Expected at most 4 visible cards, got {visible_count}'

    def test_featured_reset_shows_four_cards(self, page):
        page.click('[data-filter="python"]')
        page.click('.skill-filter-reset')
        visible = page.locator('.project-card:visible')
        assert visible.count() == 4, f'Expected 4 visible cards after reset, got {visible.count()}'

    def test_featured_cards_remain_filterable(self, page):
        """Featured cards with matching tags should appear when filtered (subject to max-visible cap)."""
        page.wait_for_function(
            'document.querySelectorAll(".project-card[style*=\\"none\\"]").length > 0'
        )
        page.click('[data-filter="python"]')
        visible = page.locator('.project-card:visible')
        visible_count = visible.count()
        assert visible_count > 0, 'No cards visible after python filter'
        assert visible_count <= 4, f'Expected at most 4 visible cards, got {visible_count}'
        # All visible cards must have the python tag
        for i in range(visible_count):
            tags = (visible.nth(i).get_attribute('data-tags') or '').split(',')
            assert 'python' in tags, f'Non-python card is visible: tags={tags}'

    def test_view_all_link_navigates(self, page):
        page.click('.view-all-link')
        page.wait_for_url(re.compile(r'projects\.html'))


@pytest.mark.e2e
class TestProjectsPage:
    def test_all_cards_visible_by_default(self, projects_page):
        visible = projects_page.locator('.project-card:visible')
        assert visible.count() == 18, f'Expected 17 visible cards, got {visible.count()}'

    def test_filter_works(self, projects_page):
        projects_page.click('[data-filter="python"]')
        visible = projects_page.locator('.project-card:visible')
        count = visible.count()
        assert count > 0, 'No cards visible after filtering'
        assert count <= 18

    def test_url_param_preselects_filter(self, browser, server):
        page = browser.new_page()
        page.goto(f'{server}/projects.html?filter=python')
        python_tag = page.locator('[data-filter="python"]')
        assert 'active' in python_tag.get_attribute('class')
        visible = page.locator('.project-card:visible')
        assert visible.count() > 0
        page.close()

    def test_featured_filter(self, projects_page):
        projects_page.click('[data-filter="featured"]')
        visible = projects_page.locator('.project-card:visible')
        assert visible.count() == 4, f'Expected 4 featured cards, got {visible.count()}'

    def test_reset_shows_all(self, projects_page):
        projects_page.click('[data-filter="python"]')
        projects_page.click('.skill-filter-reset')
        visible = projects_page.locator('.project-card:visible')
        assert visible.count() == 18, f'Expected 17 visible after reset, got {visible.count()}'

    def test_cards_display_date(self, projects_page):
        dates = projects_page.locator('.project-card:visible .project-date')
        count = dates.count()
        assert count == 18, f'Expected 17 date elements, got {count}'
        for i in range(count):
            text = dates.nth(i).text_content().strip()
            assert text, f'Date element {i} is empty'

    def test_cards_sorted_newest_first(self, projects_page):
        cards = projects_page.locator('.project-card:visible')
        count = cards.count()
        dates = []
        for i in range(count):
            date_val = cards.nth(i).get_attribute('data-date') or ''
            dates.append(date_val)
        for i in range(len(dates) - 1):
            assert dates[i] >= dates[i + 1], (
                f'Card {i} ({dates[i]}) should sort before card {i + 1} ({dates[i + 1]})'
            )
