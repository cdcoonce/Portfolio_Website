"""Tests for scripts/wiki/ Phase 1: orchestrator and generate_home."""

import sys
import tempfile
import datetime
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the wiki package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from wiki.orchestrate import splice_content, run
from wiki.generate_home import generate

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Splice logic
# ---------------------------------------------------------------------------


class TestSpliceContent:
    """Unit tests for the orchestrator's marker-splice function."""

    def test_splice_inserts_into_empty_generated_block(self):
        """Content is inserted between generated markers when block is empty."""
        original = (
            "# Page Title\n\n"
            "<!-- generated:start -->\n"
            "<!-- generated:end -->\n"
        )
        result = splice_content(original, "new content here")
        assert "new content here" in result
        assert "<!-- generated:start -->" in result
        assert "<!-- generated:end -->" in result

    def test_splice_replaces_existing_generated_content(self):
        """Re-running splice replaces the old generated content."""
        original = (
            "# Page\n\n"
            "<!-- generated:start -->\n"
            "old content\n"
            "<!-- generated:end -->\n"
        )
        result = splice_content(original, "new content")
        assert "new content" in result
        assert "old content" not in result

    def test_splice_preserves_claude_prose(self):
        """Claude prose block is left untouched after splice."""
        original = (
            "# Page\n\n"
            "<!-- generated:start -->\n"
            "old generated\n"
            "<!-- generated:end -->\n\n"
            "<!-- claude:prose -->\n"
            "Human-authored narrative here.\n"
            "<!-- claude:prose:end -->\n"
        )
        result = splice_content(original, "new generated")
        assert "Human-authored narrative here." in result
        assert "new generated" in result
        assert "old generated" not in result

    def test_splice_preserves_content_outside_markers(self):
        """Text before and after the generated block is preserved."""
        original = (
            "# Heading\n\n"
            "Intro paragraph.\n\n"
            "<!-- generated:start -->\n"
            "old\n"
            "<!-- generated:end -->\n\n"
            "Footer text.\n"
        )
        result = splice_content(original, "replaced")
        assert "Intro paragraph." in result
        assert "Footer text." in result

    def test_splice_raises_on_multiple_generated_blocks(self):
        """ValueError is raised when content has more than one generated block."""
        original = (
            "# Page\n\n"
            "<!-- generated:start -->\n"
            "block one\n"
            "<!-- generated:end -->\n\n"
            "<!-- generated:start -->\n"
            "block two\n"
            "<!-- generated:end -->\n"
        )
        with pytest.raises(ValueError, match="generated blocks"):
            splice_content(original, "new content")


# ---------------------------------------------------------------------------
# Orchestrator file creation
# ---------------------------------------------------------------------------


class TestOrchestratorRun:
    """Integration tests: orchestrator writes files correctly."""

    def test_splice_creates_file_if_missing(self, tmp_path):
        """On first run, the orchestrator creates Home.md with marker structure."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        home = tmp_path / "Home.md"
        assert home.exists(), "Home.md should be created on first run"
        content = home.read_text()
        assert "<!-- generated:start -->" in content
        assert "<!-- generated:end -->" in content

    def test_rerun_preserves_claude_prose_block(self, tmp_path):
        """Re-running the orchestrator does not overwrite claude:prose blocks."""
        # Pre-populate Home.md with a prose block
        home = tmp_path / "Home.md"
        home.write_text(
            "# Home\n\n"
            "<!-- generated:start -->\n"
            "old generated\n"
            "<!-- generated:end -->\n\n"
            "<!-- claude:prose -->\n"
            "Preserved narrative.\n"
            "<!-- claude:prose:end -->\n"
        )
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = home.read_text()
        assert "Preserved narrative." in content

    def test_sidebar_has_navigation_sections(self, tmp_path):
        """_Sidebar.md contains Reference, Architecture, and Dev Guide sections."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        sidebar = tmp_path / "_Sidebar.md"
        assert sidebar.exists(), "_Sidebar.md should be created"
        content = sidebar.read_text()
        assert "Reference" in content
        assert "Architecture" in content
        assert "Dev Guide" in content

    def test_sidebar_has_correct_lambda_and_cicd_links(self, tmp_path):
        """_Sidebar.md uses correct page names for Lambda and CI-CD links."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "_Sidebar.md").read_text()
        assert "[[Lambda-Chat-Agent]]" in content, (
            "Sidebar must link to [[Lambda-Chat-Agent]], not [[Lambda]]"
        )
        assert "[[CI-CD-Pipeline]]" in content, (
            "Sidebar must link to [[CI-CD-Pipeline]], not [[CI-CD]]"
        )
        # Regression guards: old broken links must not appear
        assert "[[Lambda]]" not in content, (
            "[[Lambda]] is a dead link — use [[Lambda-Chat-Agent]]"
        )
        assert "[[CI-CD]]" not in content, (
            "[[CI-CD]] is a dead link — use [[CI-CD-Pipeline]]"
        )

    def test_footer_has_date_and_sha(self, tmp_path):
        """_Footer.md contains 'Last regenerated:' with a date."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        footer = tmp_path / "_Footer.md"
        assert footer.exists(), "_Footer.md should be created"
        content = footer.read_text()
        assert "Last regenerated:" in content
        today = str(datetime.date.today())
        assert today in content

    def test_home_generated_block_has_content(self, tmp_path):
        """Home.md generated block contains 'Tech Stack' between the generated markers."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Home.md").read_text()
        # Extract the generated block
        start_marker = "<!-- generated:start -->"
        end_marker = "<!-- generated:end -->"
        start_idx = content.index(start_marker) + len(start_marker)
        end_idx = content.index(end_marker)
        generated_block = content[start_idx:end_idx]
        assert "Tech Stack" in generated_block, "Expected 'Tech Stack' inside the generated block"


# ---------------------------------------------------------------------------
# generate_home
# ---------------------------------------------------------------------------


class TestGenerateHome:
    """Unit tests for generate_home.generate()."""

    def test_generate_home_has_tech_stack_table(self):
        """Output contains a Markdown table row with Node or Python."""
        output = generate(REPO_ROOT)
        assert "|" in output, "Expected a Markdown table"
        assert "Node" in output or "Python" in output

    def test_generate_home_has_test_commands(self):
        """Output contains test command references."""
        output = generate(REPO_ROOT)
        assert "npm test" in output or "uv run pytest" in output

    def test_generate_home_has_npm_scripts(self):
        """Output contains npm scripts section."""
        output = generate(REPO_ROOT)
        assert "npm" in output

    def test_generate_home_returns_string(self):
        """generate() returns a plain string."""
        output = generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_generate_home_includes_version(self):
        """Output includes a version number from package.json."""
        output = generate(REPO_ROOT)
        # package.json has version 1.5.0
        assert "1.5.0" in output

    def test_generate_home_has_python_version(self):
        """Output references Python version requirement from pyproject.toml."""
        output = generate(REPO_ROOT)
        assert "3.11" in output or "Python" in output

    def test_generate_home_with_missing_files(self, tmp_path):
        """generate() does not crash when package.json and pyproject.toml are absent."""
        output = generate(tmp_path)
        assert isinstance(output, str)
        assert len(output) > 0
