import pytest

from helpers import TESTIMONIAL_COUNT, switch_tab

pytestmark = pytest.mark.e2e

QUOTE = '[data-testid="testimonial-quote"]'
DOTS = ".testimonial-card__dots button"
PREV_ARROW = 'button.arrow-btn[aria-label="Previous testimonial"]'
NEXT_ARROW = 'button.arrow-btn[aria-label="Next testimonial"]'


def test_quote_visible_and_nonempty(page):
    switch_tab(page, "testimonials")
    quote = page.locator(QUOTE)
    assert quote.is_visible()
    assert quote.inner_text().strip()


def test_dot_count_matches_testimonials(page):
    switch_tab(page, "testimonials")
    assert page.locator(DOTS).count() == TESTIMONIAL_COUNT


def test_next_arrow_changes_quote(page):
    switch_tab(page, "testimonials")
    before = page.locator(QUOTE).inner_text().strip()
    page.locator(NEXT_ARROW).click()
    page.wait_for_function(
        "(prev) => {"
        " const el = document.querySelector('[data-testid=\"testimonial-quote\"]');"
        " return el && el.innerText.trim() !== prev; }",
        arg=before,
    )
    after = page.locator(QUOTE).inner_text().strip()
    assert after
    assert after != before


def test_dot_updates_aria_current(page):
    switch_tab(page, "testimonials")
    target = page.locator(DOTS).nth(TESTIMONIAL_COUNT - 1)
    target.click()
    page.wait_for_function(
        "(i) => {"
        " const dots = document.querySelectorAll('.testimonial-card__dots button');"
        " return dots[i] && dots[i].getAttribute('aria-current') === 'true'; }",
        arg=TESTIMONIAL_COUNT - 1,
    )
    assert target.get_attribute("aria-current") == "true"


def test_previous_from_first_wraps(page):
    switch_tab(page, "testimonials")
    first = page.locator(QUOTE).inner_text().strip()
    page.locator(PREV_ARROW).click()
    page.wait_for_function(
        "(prev) => {"
        " const el = document.querySelector('[data-testid=\"testimonial-quote\"]');"
        " return el && el.innerText.trim() !== prev; }",
        arg=first,
    )
    wrapped = page.locator(QUOTE).inner_text().strip()
    assert wrapped
    assert wrapped != first


def test_arrow_aria_labels(page):
    switch_tab(page, "testimonials")
    prev_arrow = page.locator(PREV_ARROW)
    next_arrow = page.locator(NEXT_ARROW)
    assert prev_arrow.count() == 1
    assert next_arrow.count() == 1
    assert prev_arrow.is_visible()
    assert next_arrow.is_visible()
