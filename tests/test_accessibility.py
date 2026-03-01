"""Accessibility tests — WCAG automated checks."""

import pytest
from axe_playwright_python.sync_playwright import Axe


@pytest.mark.a11y
class TestAccessibility:
    def test_wcag_compliance(self, page):
        axe = Axe()
        results = axe.run(page)
        violations = results.response.get('violations', [])
        serious = [v for v in violations if v['impact'] in ('serious', 'critical')]
        assert len(serious) == 0, (
            f'{len(serious)} serious a11y violations: '
            + ', '.join(v['id'] for v in serious)
        )

    def test_focus_visible_interactive_elements(self, page):
        """Verify interactive elements receive a visible focus indicator on keyboard nav."""
        page.keyboard.press('Tab')
        focused = page.evaluate('() => document.activeElement.tagName')
        assert focused != 'BODY', 'Tab key did not move focus away from body'

    def test_carousel_buttons_have_accessible_names(self, page):
        prev_label = page.get_attribute('#prevRec', 'aria-label')
        next_label = page.get_attribute('#nextRec', 'aria-label')
        assert prev_label, '#prevRec button missing aria-label'
        assert next_label, '#nextRec button missing aria-label'

    def test_testimonials_aria_live_region(self, page):
        live = page.get_attribute('.testimonials', 'aria-live')
        assert live == 'polite', '.testimonials missing aria-live="polite"'
