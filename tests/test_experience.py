"""Experience tab: role timeline + categorized skill tags.

Two-column panel rendered by src/components/tabs/Experience.jsx: an "Experience"
timeline of roles and a "Skills & Tools" column of tag pills. The panel is
unmounted until the Experience tab is active, so every test switches first.
"""

import pytest

from helpers import EXPERIENCE_ROW_COUNT, SKILL_CATEGORY_COUNT, switch_tab

pytestmark = pytest.mark.e2e


def test_timeline_row_count(page):
    switch_tab(page, "experience")
    assert page.locator('[data-testid="timeline-row"]').count() == EXPERIENCE_ROW_COUNT


def test_skills_category_count(page):
    switch_tab(page, "experience")
    assert page.locator('[data-testid="skills-cat"]').count() == SKILL_CATEGORY_COUNT


def test_column_headings(page):
    switch_tab(page, "experience")
    headings = page.locator('[data-testid="experience"] h3.col-heading').all_inner_texts()
    assert headings == ["Experience", "Skills & Tools"]


def test_skills_column_has_tag_pills(page):
    switch_tab(page, "experience")
    assert page.locator('[data-testid="skills"] .tag').count() >= 1
