"""Tests for scripts/wiki/ Phase 2: table/list generators and changelog."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the wiki package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from wiki.orchestrate import run
from wiki import (
    generate_testing,
    generate_css,
    generate_knowledge_base,
    generate_contributing,
    generate_frontend_modules,
    generate_changelog,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# generate_testing
# ---------------------------------------------------------------------------


class TestGenerateTesting:
    """Tests for generate_testing.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_testing.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_has_table_headers(self):
        """Output contains Markdown table headers for file inventory."""
        output = generate_testing.generate(REPO_ROOT)
        assert "|" in output, "Expected Markdown table"

    def test_lists_js_test_files(self):
        """Output includes at least one .test.js file from __tests__/."""
        output = generate_testing.generate(REPO_ROOT)
        assert ".test.js" in output

    def test_lists_py_test_files(self):
        """Output includes at least one test_*.py file from tests/."""
        output = generate_testing.generate(REPO_ROOT)
        assert "test_" in output and ".py" in output

    def test_has_jest_config_info(self):
        """Output includes Jest testEnvironment from jest.config.js."""
        output = generate_testing.generate(REPO_ROOT)
        assert "jsdom" in output or "jest" in output.lower()

    def test_has_pytest_markers(self):
        """Output includes pytest markers from pyproject.toml."""
        output = generate_testing.generate(REPO_ROOT)
        # pyproject.toml has slow, a11y, e2e, validation markers
        assert "slow" in output or "a11y" in output or "e2e" in output

    def test_lists_lib_test_files(self):
        """Output references the src/lib unit-test files (carousel, chat)."""
        output = generate_testing.generate(REPO_ROOT)
        assert "portfolio-carousel" in output or "portfolio-chat" in output


# ---------------------------------------------------------------------------
# generate_css
# ---------------------------------------------------------------------------


class TestGenerateCSS:
    """Tests for generate_css.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_css.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_extracts_custom_properties(self):
        """Output contains at least one CSS custom property (-- variable)."""
        output = generate_css.generate(REPO_ROOT)
        assert "--" in output, "Expected CSS custom property with -- prefix"

    def test_has_token_table_header(self):
        """Output contains a table with token columns."""
        output = generate_css.generate(REPO_ROOT)
        assert "Token" in output or "Value" in output

    def test_extracts_known_property(self):
        """Output contains a known design token from src/styles/tokens.css."""
        output = generate_css.generate(REPO_ROOT)
        assert "--text-primary" in output or "--accent-blue" in output

    def test_has_media_queries_section(self):
        """Output contains a media query breakpoints section."""
        output = generate_css.generate(REPO_ROOT)
        assert "media" in output.lower() or "breakpoint" in output.lower()

    def test_has_known_breakpoint(self):
        """Output contains a known breakpoint from src/styles/global.css (mobile-first)."""
        output = generate_css.generate(REPO_ROOT)
        assert "700" in output or "800" in output

    def test_missing_css_files(self, tmp_path):
        """generate() does not crash when CSS files are absent."""
        output = generate_css.generate(tmp_path)
        assert isinstance(output, str)


# ---------------------------------------------------------------------------
# generate_knowledge_base
# ---------------------------------------------------------------------------


class TestGenerateKnowledgeBase:
    """Tests for generate_knowledge_base.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_has_table_headers(self):
        """Output contains a Markdown table."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert "|" in output

    def test_lists_context_files(self):
        """Output includes files from WebContent/context/."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        # Known files in context/
        assert ".md" in output

    def test_has_word_count_column(self):
        """Output contains word count data with digits between table pipe characters."""
        import re
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert re.search(r"\|\s*\d[\d,]*\s*\|", output), "Expected word count column with digits between pipes"

    def test_has_bio_file(self):
        """Output contains bio.md (known context file)."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert "bio" in output

    def test_has_skills_file(self):
        """Output contains skills.md (known context file)."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert "skills" in output

    def test_has_topic_column(self):
        """Output table has a Topic or File column header."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert "File" in output or "Topic" in output


# ---------------------------------------------------------------------------
# generate_contributing
# ---------------------------------------------------------------------------


class TestGenerateContributing:
    """Tests for generate_contributing.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_contributing.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_has_setup_steps(self):
        """Output contains local setup steps."""
        output = generate_contributing.generate(REPO_ROOT)
        assert "setup" in output.lower() or "install" in output.lower() or "clone" in output.lower()

    def test_has_make_targets(self):
        """Output references make targets (test, lint, etc.)."""
        output = generate_contributing.generate(REPO_ROOT)
        assert "make" in output.lower() or "test" in output.lower()

    def test_has_npm_targets(self):
        """Output references npm scripts."""
        output = generate_contributing.generate(REPO_ROOT)
        assert "npm" in output

    def test_has_commit_conventions(self):
        """Output mentions commit conventions (conventional commits)."""
        output = generate_contributing.generate(REPO_ROOT)
        assert "feat" in output or "fix" in output or "commit" in output.lower()

    def test_has_table(self):
        """Output contains a Markdown table."""
        output = generate_contributing.generate(REPO_ROOT)
        assert "|" in output


class TestContributingPageProseBlock:
    """Tests that Contributing.md gets a claude:prose block on first run."""

    def test_contributing_page_has_prose_block(self, tmp_path):
        """On first run, Contributing.md is created with a claude:prose block."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        contributing = tmp_path / "Contributing.md"
        assert contributing.exists(), "Contributing.md should be created on first run"
        content = contributing.read_text()
        assert "<!-- claude:prose -->" in content, "Contributing.md must have claude:prose block"
        assert "<!-- claude:prose:end -->" in content

    def test_contributing_page_has_generated_block(self, tmp_path):
        """Contributing.md also has the generated markers."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Contributing.md").read_text()
        assert "<!-- generated:start -->" in content
        assert "<!-- generated:end -->" in content

    def test_other_phase2_pages_no_prose_block(self, tmp_path):
        """Non-Contributing Phase 2 pages do NOT have claude:prose blocks."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        no_prose_pages = [
            "Testing.md",
            "CSS-Design-System.md",
            "Knowledge-Base.md",
            "Frontend-Modules.md",
            "Changelog.md",
        ]
        for page in no_prose_pages:
            path = tmp_path / page
            assert path.exists(), f"{page} should be created on first run"
            content = path.read_text()
            assert "<!-- claude:prose -->" not in content, (
                f"{page} must NOT have claude:prose block (only Contributing gets one)"
            )


# ---------------------------------------------------------------------------
# generate_frontend_modules
# ---------------------------------------------------------------------------


class TestGenerateFrontendModules:
    """Tests for generate_frontend_modules.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_has_table_headers(self):
        """Output contains a Markdown table."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "|" in output

    def test_lists_source_files(self):
        """Output references src/ source files (components and lib modules)."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert ".jsx" in output and ".js" in output

    def test_has_portfolio_island(self):
        """Output contains the root Portfolio island."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "Portfolio" in output

    def test_has_chat_module(self):
        """Output contains the src/lib/chat.js module."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "chat" in output

    def test_has_exports(self):
        """Output contains at least one real export reference from src/lib or src/data."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        # Known exports: sendMessage/isRateLimited (chat), nextIndex (carousel), navItems (data).
        assert any(
            name in output
            for name in ["sendMessage", "isRateLimited", "nextIndex", "navItems"]
        )

    def test_has_component_tree(self):
        """Output contains the React component tree diagram (graph TD)."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "graph TD" in output, "Component tree diagram should be present"

    def test_missing_src_dir(self, tmp_path):
        """generate() does not crash when src/ is absent."""
        output = generate_frontend_modules.generate(tmp_path)
        assert isinstance(output, str)


# ---------------------------------------------------------------------------
# generate_changelog
# ---------------------------------------------------------------------------


class TestGenerateChangelog:
    """Tests for generate_changelog.generate()."""

    def test_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_changelog.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_has_commit_type_header(self):
        """Output contains at least one conventional commit type H3 header."""
        output = generate_changelog.generate(REPO_ROOT)
        # Repo has feat, fix, chore, docs, refactor, style commits
        h3_labels = [
            "### Features",
            "### Bug Fixes",
            "### Chores",
            "### Documentation",
            "### Refactoring",
            "### Style",
        ]
        assert any(label in output for label in h3_labels), (
            f"Expected at least one H3 commit type header, got: {output[:200]}"
        )

    def test_has_feat_commits(self):
        """A feat commit is rendered under the Features section.

        Drives the generator with a synthetic commit list so the grouping
        logic is asserted deterministically, independent of the live 50-commit
        git window (which may contain only chore/content commits).
        """
        commits = [
            {
                "sha": "abc12345",
                "subject": "feat(carousel): add keyboard navigation",
                "body": "add keyboard navigation",
                "author": "Test Author",
                "date": "2026-01-01",
                "type": "feat",
            }
        ]
        output = generate_changelog.generate(REPO_ROOT, commits=commits)
        assert "### Features" in output
        assert "add keyboard navigation" in output

    def test_has_fix_commits(self):
        """A fix commit is rendered under the Bug Fixes section.

        Drives the generator with a synthetic commit list so the grouping
        logic is asserted deterministically, independent of the live 50-commit
        git window (which may contain only chore/content commits).
        """
        commits = [
            {
                "sha": "def67890",
                "subject": "fix(chat): handle empty response payload",
                "body": "handle empty response payload",
                "author": "Test Author",
                "date": "2026-01-02",
                "type": "fix",
            }
        ]
        output = generate_changelog.generate(REPO_ROOT, commits=commits)
        assert "### Bug Fixes" in output
        assert "handle empty response payload" in output

    def test_has_dates(self):
        """Output contains ISO date strings."""
        output = generate_changelog.generate(REPO_ROOT)
        # Dates look like 2026-04-12
        import re
        assert re.search(r"\d{4}-\d{2}-\d{2}", output), "Expected ISO date in changelog"

    def test_grouped_by_type(self):
        """Output is grouped with ## headers for each commit type."""
        output = generate_changelog.generate(REPO_ROOT)
        assert output.count("##") >= 1, "Expected at least one ## section header"

    def test_shows_commit_subjects(self):
        """Output includes dated commit entries with SHA + subject text."""
        import re

        output = generate_changelog.generate(REPO_ROOT)
        # Each entry is rendered as: - **YYYY-MM-DD** `sha` — subject
        assert re.search(r"\*\*\d{4}-\d{2}-\d{2}\*\* `[0-9a-f]+` — \S", output), (
            "Expected at least one dated commit entry in the changelog"
        )
