"""Automated accessibility checks for the Astro tabbed SPA.

Runs axe-core (via axe-playwright-python) against the default Overview view and
against the lazily-mounted Work and Ask AI panels, and spot-checks keyboard focus
and the accessible names on the testimonials carousel arrows. The severity gate is
deliberately tolerant — only "serious"/"critical" violations fail the suite, so a
pre-existing minor/moderate issue does not block the build.
"""

import pytest
from axe_playwright_python.sync_playwright import Axe

from helpers import switch_tab

pytestmark = pytest.mark.a11y


def _serious_violations(results):
    """Return axe violations whose impact is serious or critical.

    ``Axe.run`` yields a results object whose ``.response`` dict holds the raw
    axe-core report; ``impact`` may be absent/None, so read it defensively.
    """
    violations = results.response.get("violations", [])
    return [v for v in violations if v.get("impact") in ("serious", "critical")]


def _assert_no_serious(results, where):
    serious = _serious_violations(results)
    assert not serious, (
        f"{len(serious)} serious/critical a11y violation(s) on {where}: "
        + ", ".join(v.get("id", "?") for v in serious)
    )


def test_overview_has_no_serious_axe_violations(page):
    results = Axe().run(page)
    _assert_no_serious(results, "the Overview view")


def test_work_panel_has_no_serious_axe_violations(page):
    switch_tab(page, "work")
    results = Axe().run(page)
    _assert_no_serious(results, "the Work panel")


def test_ai_panel_has_no_serious_axe_violations(page):
    switch_tab(page, "ai")
    results = Axe().run(page)
    _assert_no_serious(results, "the Ask AI panel")


def test_tab_key_moves_focus_off_body(page):
    page.keyboard.press("Tab")
    focused = page.evaluate("document.activeElement.tagName")
    assert focused != "BODY", "Tab key did not move focus away from <body>"


def test_testimonial_arrows_have_accessible_names(page):
    switch_tab(page, "testimonials")
    prev_arrow = page.locator('button.arrow-btn[aria-label="Previous testimonial"]')
    next_arrow = page.locator('button.arrow-btn[aria-label="Next testimonial"]')
    assert prev_arrow.count() == 1, "missing accessible Previous-testimonial arrow"
    assert next_arrow.count() == 1, "missing accessible Next-testimonial arrow"
