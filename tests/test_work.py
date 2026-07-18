"""Work tab: default gallery, category rail, search, empty state, card links.

The Work panel is tab-gated (unmounted until selected), so every test switches
to it first. Filtering/search matching itself is covered by Jest unit tests
against src/lib/work-filter.js; here we assert the DOM wiring — card counts, the
count label, and the external-link contract of each project card.
"""

import pytest

from helpers import GALLERY_COUNT, WORK_FILTER_COUNT, switch_tab

pytestmark = pytest.mark.e2e


def test_default_shows_full_gallery(page):
    switch_tab(page, "work")
    assert page.locator('[data-testid="project-card"]').count() == GALLERY_COUNT
    count_text = page.locator('[data-testid="work-count"]').inner_text()
    assert "all 22" in count_text


def test_rail_has_all_filter_buttons(page):
    switch_tab(page, "work")
    rails = page.locator('[data-testid^="rail-"]')
    assert rails.count() == WORK_FILTER_COUNT


def test_clicking_python_filters_gallery(page):
    switch_tab(page, "work")
    page.click('[data-testid="rail-python"]')
    page.wait_for_function(
        "() => document.querySelectorAll('[data-testid=\"project-card\"]').length === 12"
    )
    assert page.locator('[data-testid="project-card"]').count() == 12
    count_text = page.locator('[data-testid="work-count"]').inner_text()
    assert count_text == "Showing 12 of 22 projects"


def test_search_narrows_results(page):
    switch_tab(page, "work")
    page.fill('[data-testid="work-search"]', "wine")
    page.wait_for_function(
        "() => { const n = document.querySelectorAll('[data-testid=\"project-card\"]').length;"
        " return n >= 1 && n < 22; }"
    )
    count = page.locator('[data-testid="project-card"]').count()
    assert 1 <= count < GALLERY_COUNT


def test_no_match_shows_empty_state_and_clear_restores(page):
    switch_tab(page, "work")
    page.fill('[data-testid="work-search"]', "zzznotathing")
    page.wait_for_selector('[data-testid="work-empty"]')
    assert page.locator('[data-testid="work-empty"]').is_visible()
    assert page.locator('[data-testid="project-card"]').count() == 0

    page.click('[data-testid="work-clear"]')
    page.wait_for_function(
        "() => document.querySelectorAll('[data-testid=\"project-card\"]').length === 22"
    )
    assert page.locator('[data-testid="project-card"]').count() == GALLERY_COUNT


def test_project_cards_are_external_links(page):
    switch_tab(page, "work")
    cards = page.locator('[data-testid="project-card"]')
    total = cards.count()
    assert total == GALLERY_COUNT
    for i in range(total):
        card = cards.nth(i)
        assert card.get_attribute("target") == "_blank"
        aria_label = card.get_attribute("aria-label") or ""
        assert aria_label.endswith("opens in a new tab")
        href = card.get_attribute("href") or ""
        assert href != ""
