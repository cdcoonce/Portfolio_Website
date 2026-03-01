"""E2E gallery tests — filter buttons toggle card visibility."""

import pytest


@pytest.mark.e2e
class TestGallery:
    def test_filter_shows_only_matching_cards(self, page):
        page.click('[data-filter="python"]')
        all_cards = page.locator('.project-card')
        total = all_cards.count()
        assert total > 0, 'No project cards found in DOM'
        for i in range(total):
            card = all_cards.nth(i)
            tags = (card.get_attribute('data-tags') or '').split(',')
            if card.is_visible():
                assert 'python' in tags, f'Non-python card is visible: tags={tags}'

    def test_all_filter_shows_every_card(self, page):
        page.click('[data-filter="python"]')
        page.click('.skill-filter-reset')
        total = page.locator('.project-card').count()
        visible = page.locator('.project-card:visible').count()
        assert visible == total, f'Expected {total} visible cards after reset, got {visible}'

    def test_featured_cards_remain_filterable(self, page):
        featured = page.locator('.project-card.featured')
        assert featured.count() >= 3, 'Expected at least 3 featured cards'
        page.click('[data-filter="python"]')
        all_cards = page.locator('.project-card.featured')
        for i in range(all_cards.count()):
            card = all_cards.nth(i)
            tags = (card.get_attribute('data-tags') or '').split(',')
            is_visible = card.is_visible()
            has_python = 'python' in tags
            assert is_visible == has_python, (
                f'Featured card visibility mismatch: visible={is_visible}, has_python={has_python}, tags={tags}'
            )
