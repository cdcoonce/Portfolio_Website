"""Responsive + visual smoke for the Astro tabbed SPA.

Resizes the hydrated page across four breakpoints and asserts the persistent
chrome (tab bar, profile hero, footer) survives every layout. Full-page
screenshots are written to tests/snapshots/ as baseline captures only — they are
NOT diffed against a golden image here; they exist for eyeballing regressions.
Replaces the retired vanilla-DOM version (#main-nav / .nav-toggle hamburger).
"""

from pathlib import Path

import pytest

from helpers import switch_tab

pytestmark = pytest.mark.slow

# (name, width, height) — name drives the snapshot filename.
BREAKPOINTS = [
    ("desktop", 1440, 900),
    ("laptop", 1024, 768),
    ("tablet", 768, 1024),
    ("mobile", 375, 812),
]

SNAPSHOTS = Path(__file__).parent / "snapshots"


@pytest.mark.parametrize("name,width,height", BREAKPOINTS)
def test_chrome_survives_breakpoint(page, name, width, height):
    page.set_viewport_size({"width": width, "height": height})
    assert page.locator('[data-testid="tabbar"]').is_visible()
    assert page.locator('[data-testid="profile"]').is_visible()
    assert page.locator('[data-testid="site-footer"]').is_visible()
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SNAPSHOTS / f"{name}-{width}x{height}.png"), full_page=True)


def test_work_grid_renders_on_mobile(page):
    page.set_viewport_size({"width": 375, "height": 812})
    switch_tab(page, "work")
    assert page.locator('[data-testid="project-card"]').first.is_visible()
