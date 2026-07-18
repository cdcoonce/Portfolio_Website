"""Overview tab: featured-project spotlight carousel + see-all-work CTA.

The Overview panel is the active tab on load (no switch needed), rendered as
static HTML that Astro then hydrates. It leads with a rotating spotlight whose
current slide is either a Cockpit <svg> or an <img>, then a CTA into the Work
grid. Project titles are intentionally not hard-asserted — the data may reorder
— so these tests exercise structure, counts, and carousel wiring instead.
"""

import pytest

from helpers import FEATURED_COUNT, switch_tab

pytestmark = pytest.mark.e2e


def test_featured_spotlight_renders(page):
    featured = page.locator('[data-testid="featured"]')
    assert featured.is_visible()
    title = featured.locator(".featured__title")
    assert title.is_visible()
    assert (title.inner_text() or "").strip() != ""
    # Each slide shows a media element: a Cockpit <svg role="img"> or an <img>.
    media = page.locator(
        '[data-testid="featured"] svg[role="img"], [data-testid="featured"] img'
    )
    assert media.count() >= 1


def test_featured_has_one_dot_per_featured_project(page):
    dots = page.locator(".featured-nav__dots button")
    assert dots.count() == FEATURED_COUNT


def test_next_arrow_advances_spotlight(page):
    title = page.locator(".featured__title")
    before = (title.inner_text() or "").strip()
    page.locator('button.arrow-btn[aria-label="Next featured project"]').click()
    page.wait_for_function(
        "prev => { const el = document.querySelector('.featured__title');"
        " return el && el.textContent.trim() !== prev; }",
        arg=before,
    )
    assert (title.inner_text() or "").strip() != before


def test_clicking_dot_sets_aria_current(page):
    # Dot 1 is not the default (index 0) slide, so clicking it is a real change.
    dot = page.locator(".featured-nav__dots button").nth(1)
    dot.click()
    page.wait_for_function(
        "() => { const els = document.querySelectorAll('.featured-nav__dots button');"
        " return els[1] && els[1].getAttribute('aria-current') === 'true'; }"
    )
    assert dot.get_attribute("aria-current") == "true"


def test_returning_to_overview_still_renders(page):
    # Overview unmounts when another tab is active; switching back re-mounts it.
    switch_tab(page, "work")
    switch_tab(page, "overview")
    assert page.locator('[data-testid="featured"]').is_visible()


def test_see_all_work_cta_switches_to_work(page):
    # The Overview CTA is the promoted path into the full project grid.
    cta = page.locator('[data-testid="overview-see-work"]')
    assert cta.is_visible()
    cta.click()
    assert page.locator('[data-testid="work"]').is_visible()
    assert page.locator('[data-testid="overview"]').count() == 0
