"""E2E carousel tests — testimonial navigation + wraparound."""

import pytest


@pytest.mark.e2e
class TestCarousel:
    def test_carousel_advances_to_next(self, page):
        """Clicking next should show a different testimonial."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_selector('.testimonial.active')
        initial_text = page.locator('.testimonial.active').first.inner_text()
        page.click('#nextRec')
        page.wait_for_timeout(400)
        new_text = page.locator('.testimonial.active').first.inner_text()
        assert new_text != initial_text, 'Next button should advance to next testimonial'

    def test_carousel_wraps_from_last_to_first(self, page):
        """After the last testimonial, next should wrap back to the first."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_selector('.testimonial.active')
        first_text = page.locator('.testimonial').first.inner_text()
        # 7 testimonials, 1 at a time: 6 clicks reach last, 7th click wraps to first
        for _ in range(7):
            page.click('#nextRec')
            page.wait_for_timeout(200)
        active_text = page.locator('.testimonial.active').first.inner_text()
        assert active_text == first_text, 'Carousel should wrap back to first testimonial'

    def test_counter_shows_position(self, page):
        """Counter should display current position in x / y format."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_selector('.testimonial-counter')
        text = page.locator('.testimonial-counter').inner_text()
        assert '/' in text, f'Counter should show "x / y" format, got: {text}'
        assert text.strip().startswith('1'), f'Counter should start at 1, got: {text}'

    def test_counter_updates_on_next(self, page):
        """Counter should update when navigating to next testimonial."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_selector('.testimonial-counter')
        page.click('#nextRec')
        page.wait_for_timeout(400)
        text = page.locator('.testimonial-counter').inner_text()
        assert text.strip().startswith('2'), f'Counter should show "2 / ..." after next click, got: {text}'

    def test_dot_click_navigates(self, page):
        """Clicking a dot should navigate to that testimonial."""
        page.set_viewport_size({'width': 400, 'height': 800})
        page.reload()
        page.wait_for_selector('.dot')
        page.locator('.dot').nth(1).click()
        page.wait_for_timeout(400)
        text = page.locator('.testimonial-counter').inner_text()
        assert text.strip().startswith('2'), f'Counter should show "2 / ..." after clicking 2nd dot, got: {text}'
