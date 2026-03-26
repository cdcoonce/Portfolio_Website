"""Visual regression tests — full-page screenshots at key breakpoints."""

from pathlib import Path

import pytest


SNAPSHOTS_DIR = Path(__file__).parent / 'snapshots'

BREAKPOINTS = [
    ('mobile', 320, 568),
    ('tablet', 768, 1024),
    ('desktop', 1024, 768),
    ('wide', 1440, 900),
]


@pytest.mark.slow
@pytest.mark.parametrize('name,width,height', BREAKPOINTS)
def test_full_page_screenshot_at_breakpoint(browser, server, name, width, height):
    """Capture a full-page screenshot at each breakpoint and save to tests/snapshots/."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    page = browser.new_page(viewport={'width': width, 'height': height})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    snapshot_path = SNAPSHOTS_DIR / f'{name}.png'
    screenshot = page.screenshot(full_page=True)
    snapshot_path.write_bytes(screenshot)

    page.close()

    assert snapshot_path.exists(), f'Screenshot not saved: {snapshot_path}'
    assert snapshot_path.stat().st_size > 0, f'Screenshot file is empty: {snapshot_path}'


@pytest.mark.slow
@pytest.mark.parametrize('name,width,height', BREAKPOINTS)
def test_nav_visible_at_breakpoint(browser, server, name, width, height):
    """Navigation should be present at every breakpoint."""
    page = browser.new_page(viewport={'width': width, 'height': height})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    assert page.locator('#main-nav').is_visible(), (
        f'Nav should be visible at {name} ({width}x{height})'
    )
    page.close()


@pytest.mark.slow
@pytest.mark.parametrize('name,width,height', BREAKPOINTS)
def test_hero_section_visible_at_breakpoint(browser, server, name, width, height):
    """Hero/profile section should be visible at every breakpoint."""
    page = browser.new_page(viewport={'width': width, 'height': height})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    assert page.locator('#profile').is_visible(), (
        f'#profile section should be visible at {name} ({width}x{height})'
    )
    page.close()


@pytest.mark.slow
@pytest.mark.parametrize('name,width,height', BREAKPOINTS)
def test_footer_visible_at_breakpoint(browser, server, name, width, height):
    """Footer should be visible at every breakpoint."""
    page = browser.new_page(viewport={'width': width, 'height': height})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    page.locator('footer').scroll_into_view_if_needed()
    assert page.locator('footer').is_visible(), (
        f'Footer should be visible at {name} ({width}x{height})'
    )
    page.close()


@pytest.mark.slow
def test_hamburger_hidden_on_desktop(browser, server):
    """Hamburger toggle button should not be visible on a wide desktop viewport."""
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    toggle = page.locator('.nav-toggle')
    is_visible = toggle.is_visible()
    page.close()

    assert not is_visible, 'Hamburger button should be hidden on desktop (1440px wide)'


@pytest.mark.slow
def test_hamburger_visible_on_mobile(browser, server):
    """Hamburger toggle button should be visible on a narrow mobile viewport."""
    page = browser.new_page(viewport={'width': 320, 'height': 568})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    toggle = page.locator('.nav-toggle')
    is_visible = toggle.is_visible()
    page.close()

    assert is_visible, 'Hamburger button should be visible on mobile (320px wide)'


@pytest.mark.slow
def test_project_cards_visible_on_mobile(browser, server):
    """Project cards should be visible and not overflow on mobile."""
    page = browser.new_page(viewport={'width': 320, 'height': 568})
    page.goto(server)
    page.wait_for_load_state('networkidle')

    # Wait for JS to apply default filter
    page.wait_for_function(
        'document.querySelectorAll(".project-card:not([style*=\'none\'])").length > 0'
    )
    visible_cards = page.locator('.project-card:visible')
    count = visible_cards.count()
    page.close()

    assert count > 0, 'At least one project card should be visible on mobile'
