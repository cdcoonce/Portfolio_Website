"""Tab bar + tab-switching behavior for the Astro tabbed SPA.

Replaces the retired test_nav.py (sticky nav / hamburger / back-to-top, all
removed). The nav is now a <nav class="tabbar"> of <button> tabs that swap a
single conditionally-rendered panel; non-active panels are unmounted.
"""

import pytest

from helpers import NAV_KEYS, NAV_LABELS, TAB_ROOT, switch_tab

pytestmark = pytest.mark.e2e


def test_tabbar_present(page):
    tabbar = page.locator('[data-testid="tabbar"]')
    assert tabbar.is_visible()
    assert tabbar.get_attribute("aria-label") == "Portfolio sections"


def test_all_six_tabs_present(page):
    labels = page.locator('[data-testid="tabbar"] button').all_inner_texts()
    assert labels == NAV_LABELS


def test_overview_active_by_default(page):
    overview_tab = page.locator('[data-testid="tab-overview"]')
    assert overview_tab.get_attribute("aria-current") == "page"
    assert "tabbar__tab--active" in (overview_tab.get_attribute("class") or "")
    assert page.locator('[data-testid="overview"]').is_visible()


def test_clicking_tab_switches_panel(page):
    switch_tab(page, "work")
    assert page.locator('[data-testid="work"]').is_visible()
    # Overview panel is unmounted once Work is active.
    assert page.locator('[data-testid="overview"]').count() == 0
    assert page.locator('[data-testid="tab-work"]').get_attribute("aria-current") == "page"
    assert page.locator('[data-testid="tab-overview"]').get_attribute("aria-current") is None


def test_only_active_panel_is_mounted(page):
    switch_tab(page, "contact")
    mounted = [k for k in NAV_KEYS if page.locator(f'[data-testid="{TAB_ROOT[k]}"]').count() > 0]
    assert mounted == ["contact"]


def test_every_tab_mounts_its_panel(page):
    for key in NAV_KEYS:
        switch_tab(page, key)
        assert page.locator(f'[data-testid="{TAB_ROOT[key]}"]').is_visible()


def test_tab_switch_does_not_change_url(page):
    start = page.url
    switch_tab(page, "experience")
    assert page.url == start


def test_tabbar_is_sticky(page):
    position = page.eval_on_selector(
        '[data-testid="tabbar"]', "el => getComputedStyle(el).position"
    )
    assert position == "sticky"
