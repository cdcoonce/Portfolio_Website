"""Shared helpers and expected content counts for the E2E suite.

Counts are derived from src/data/portfolio.js and verified against the rendered
SPA. Keep them in sync with the data model, not with the retired vanilla DOM.
"""

# Tab key -> the data-testid of that tab panel's root element. Non-active tabs
# are unmounted (absent from the DOM), so a test must switch to a tab before
# querying inside it.
TAB_ROOT = {
    "overview": "overview",
    "work": "work",
    "experience": "experience",
    "testimonials": "testimonials",
    "ai": "askai",
    "contact": "contact",
}

NAV_KEYS = ["overview", "work", "experience", "testimonials", "ai", "contact"]
NAV_LABELS = ["Overview", "Work", "Experience", "Testimonials", "Ask AI", "Contact"]

# projects[] minus the single hideFromGallery entry (my-brain).
GALLERY_COUNT = 22
# WORK_FILTERS = "all" + 7 categories.
WORK_FILTER_COUNT = 8
SKILL_CATEGORY_COUNT = 4
EXPERIENCE_ROW_COUNT = 3
CONTACT_CARD_COUNT = 4
TESTIMONIAL_COUNT = 5
# projects[] with featured: true (spotlight carousel on the Overview tab).
FEATURED_COUNT = 6


def wait_hydrated(page) -> None:
    """Block until the Astro island has hydrated (interactive React attached).

    The built page ships the Overview tab as static HTML inside an
    ``<astro-island ssr>`` wrapper; Astro strips the ``ssr`` attribute once the
    island hydrates, which is our signal that tab switching / carousels work.
    """
    page.wait_for_selector('[data-testid="tabbar"]')
    page.wait_for_function(
        "() => { const el = document.querySelector('astro-island');"
        " return !el || !el.hasAttribute('ssr'); }"
    )


def switch_tab(page, key: str) -> None:
    """Click a tab and wait for its panel root to mount."""
    page.click(f'[data-testid="tab-{key}"]')
    page.wait_for_selector(f'[data-testid="{TAB_ROOT[key]}"]')
