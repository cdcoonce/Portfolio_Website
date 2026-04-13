"""Tests for scripts/wiki/ Phase 3: Mermaid diagram generators."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the wiki package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from wiki.orchestrate import run
from wiki import (
    generate_architecture,
    generate_frontend_modules,
    generate_knowledge_base,
    generate_lambda,
    generate_cicd,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MERMAID_OPEN = "```mermaid"
MERMAID_CLOSE = "```"


def count_mermaid_blocks(text: str) -> int:
    """Count the number of mermaid code blocks in the text."""
    return text.count(MERMAID_OPEN)


# ---------------------------------------------------------------------------
# generate_architecture
# ---------------------------------------------------------------------------


class TestGenerateArchitecture:
    """Tests for generate_architecture.generate()."""

    def test_generate_architecture_has_graph_td(self):
        """Output contains a mermaid block and graph TD diagram."""
        output = generate_architecture.generate(REPO_ROOT)
        assert MERMAID_OPEN in output, "Expected ```mermaid opening"
        assert "graph TD" in output, "Expected graph TD diagram type"

    def test_generate_architecture_has_dataflow_diagram(self):
        """Output contains at least 2 mermaid blocks (system + data flow)."""
        output = generate_architecture.generate(REPO_ROOT)
        assert count_mermaid_blocks(output) >= 2, (
            f"Expected at least 2 mermaid blocks, got {count_mermaid_blocks(output)}"
        )

    def test_architecture_mermaid_blocks_properly_closed(self):
        """Each mermaid open block has a corresponding close."""
        output = generate_architecture.generate(REPO_ROOT)
        opens = output.count(MERMAID_OPEN)
        # Count standalone ``` lines (close markers)
        closes = sum(
            1 for line in output.splitlines()
            if line.strip() == MERMAID_CLOSE
        )
        assert opens == closes, (
            f"Mermaid block mismatch: {opens} opens vs {closes} closes"
        )

    def test_architecture_mentions_lambda(self):
        """Architecture diagram references Lambda."""
        output = generate_architecture.generate(REPO_ROOT)
        assert "Lambda" in output or "lambda" in output.lower()

    def test_architecture_mentions_browser(self):
        """Architecture diagram references Browser."""
        output = generate_architecture.generate(REPO_ROOT)
        assert "Browser" in output or "browser" in output.lower()

    def test_architecture_mentions_anthropic(self):
        """Architecture diagram references Anthropic API."""
        output = generate_architecture.generate(REPO_ROOT)
        assert "Anthropic" in output or "anthropic" in output.lower()

    def test_architecture_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_architecture.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0


# ---------------------------------------------------------------------------
# generate_frontend_modules (Phase 3 addition: graph LR)
# ---------------------------------------------------------------------------


class TestGenerateFrontendModulesDiagram:
    """Tests for the Phase 3 module dependency graph in generate_frontend_modules."""

    def test_generate_frontend_modules_has_graph_lr(self):
        """Output contains a mermaid graph LR dependency diagram."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert MERMAID_OPEN in output, "Expected ```mermaid opening"
        assert "graph LR" in output, "Expected graph LR diagram type"

    def test_frontend_modules_mermaid_blocks_properly_closed(self):
        """Each mermaid open has a corresponding close."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        opens = output.count(MERMAID_OPEN)
        closes = sum(
            1 for line in output.splitlines()
            if line.strip() == MERMAID_CLOSE
        )
        assert opens == closes, (
            f"Mermaid block mismatch: {opens} opens vs {closes} closes"
        )

    def test_frontend_modules_diagram_references_main(self):
        """Dependency graph mentions main.js (known entry point)."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "main" in output.lower()

    def test_frontend_modules_no_phase3_placeholder(self):
        """Phase 3 placeholder comment is replaced by actual diagram."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "Phase 3: module dependency graph will be inserted here" not in output, (
            "Placeholder comment should be replaced by the actual diagram"
        )

    def test_frontend_modules_still_has_table(self):
        """Module inventory table is still present after Phase 3 changes."""
        output = generate_frontend_modules.generate(REPO_ROOT)
        assert "| Module |" in output or "Module Inventory" in output


# ---------------------------------------------------------------------------
# generate_knowledge_base
# ---------------------------------------------------------------------------


class TestGenerateKnowledgeBase:
    """Tests for generate_knowledge_base.generate()."""

    def test_knowledge_base_has_flowchart_lr(self):
        """Output contains a flowchart LR compile pipeline diagram."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert "flowchart LR" in output, "Expected flowchart LR diagram in Knowledge-Base output"

    def test_knowledge_base_mermaid_block_properly_closed(self):
        """The mermaid block opened for the pipeline diagram is properly closed."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        opens = output.count(MERMAID_OPEN)
        closes = sum(
            1 for line in output.splitlines()
            if line.strip() == MERMAID_CLOSE
        )
        assert opens == closes, (
            f"Mermaid block mismatch: {opens} opens vs {closes} closes"
        )

    def test_knowledge_base_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_knowledge_base.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0


# ---------------------------------------------------------------------------
# generate_lambda
# ---------------------------------------------------------------------------


class TestGenerateLambda:
    """Tests for generate_lambda.generate()."""

    def test_generate_lambda_has_sequence_diagram(self):
        """Output contains a sequenceDiagram mermaid block."""
        output = generate_lambda.generate(REPO_ROOT)
        assert MERMAID_OPEN in output, "Expected ```mermaid opening"
        assert "sequenceDiagram" in output, "Expected sequenceDiagram diagram type"

    def test_generate_lambda_has_class_diagram(self):
        """Output contains a classDiagram mermaid block."""
        output = generate_lambda.generate(REPO_ROOT)
        assert "classDiagram" in output, "Expected classDiagram diagram type"

    def test_lambda_mermaid_blocks_properly_closed(self):
        """Each mermaid open has a corresponding close."""
        output = generate_lambda.generate(REPO_ROOT)
        opens = output.count(MERMAID_OPEN)
        closes = sum(
            1 for line in output.splitlines()
            if line.strip() == MERMAID_CLOSE
        )
        assert opens == closes, (
            f"Mermaid block mismatch: {opens} opens vs {closes} closes"
        )

    def test_lambda_sequence_mentions_user(self):
        """Sequence diagram mentions User participant."""
        output = generate_lambda.generate(REPO_ROOT)
        assert "User" in output

    def test_lambda_sequence_mentions_anthropic(self):
        """Sequence diagram mentions Anthropic API."""
        output = generate_lambda.generate(REPO_ROOT)
        assert "Anthropic" in output or "anthropic" in output.lower()

    def test_lambda_class_mentions_chat_agent(self):
        """Class diagram mentions ChatAgent."""
        output = generate_lambda.generate(REPO_ROOT)
        assert "ChatAgent" in output

    def test_lambda_class_mentions_chat_request(self):
        """Class diagram mentions ChatRequest."""
        output = generate_lambda.generate(REPO_ROOT)
        assert "ChatRequest" in output

    def test_lambda_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_lambda.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_lambda_has_at_least_two_mermaid_blocks(self):
        """Output contains at least 2 mermaid blocks (sequence + class)."""
        output = generate_lambda.generate(REPO_ROOT)
        assert count_mermaid_blocks(output) >= 2, (
            f"Expected at least 2 mermaid blocks, got {count_mermaid_blocks(output)}"
        )


# ---------------------------------------------------------------------------
# generate_cicd
# ---------------------------------------------------------------------------


class TestGenerateCicd:
    """Tests for generate_cicd.generate()."""

    def test_generate_cicd_has_flowchart(self):
        """Output contains a flowchart TD mermaid block."""
        output = generate_cicd.generate(REPO_ROOT)
        assert MERMAID_OPEN in output, "Expected ```mermaid opening"
        assert "flowchart TD" in output, "Expected flowchart TD diagram type"

    def test_generate_cicd_has_gitgraph(self):
        """Output contains a gitGraph mermaid block."""
        output = generate_cicd.generate(REPO_ROOT)
        assert "gitGraph" in output, "Expected gitGraph diagram type"

    def test_cicd_mermaid_blocks_properly_closed(self):
        """Each mermaid open has a corresponding close."""
        output = generate_cicd.generate(REPO_ROOT)
        opens = output.count(MERMAID_OPEN)
        closes = sum(
            1 for line in output.splitlines()
            if line.strip() == MERMAID_CLOSE
        )
        assert opens == closes, (
            f"Mermaid block mismatch: {opens} opens vs {closes} closes"
        )

    def test_cicd_mentions_lint(self):
        """Flowchart references lint step from CI config."""
        output = generate_cicd.generate(REPO_ROOT)
        assert "lint" in output.lower() or "Lint" in output

    def test_cicd_mentions_test(self):
        """Flowchart references test step from CI config."""
        output = generate_cicd.generate(REPO_ROOT)
        assert "test" in output.lower() or "Test" in output

    def test_cicd_mentions_deploy(self):
        """Flowchart references deploy step."""
        output = generate_cicd.generate(REPO_ROOT)
        assert "deploy" in output.lower() or "Deploy" in output

    def test_cicd_returns_string(self):
        """generate() returns a non-empty string."""
        output = generate_cicd.generate(REPO_ROOT)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_cicd_has_at_least_two_mermaid_blocks(self):
        """Output contains at least 2 mermaid blocks (flowchart + gitGraph)."""
        output = generate_cicd.generate(REPO_ROOT)
        assert count_mermaid_blocks(output) >= 2, (
            f"Expected at least 2 mermaid blocks, got {count_mermaid_blocks(output)}"
        )


# ---------------------------------------------------------------------------
# Prose blocks — Architecture.md and Lambda-Chat-Agent.md
# ---------------------------------------------------------------------------


class TestArchitecturePageProseBlock:
    """Tests that Architecture.md gets a claude:prose block on first run."""

    def test_architecture_page_has_prose_block(self, tmp_path):
        """On first run, Architecture.md is created with a claude:prose block."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        page = tmp_path / "Architecture.md"
        assert page.exists(), "Architecture.md should be created on first run"
        content = page.read_text()
        assert "<!-- claude:prose -->" in content, "Architecture.md must have claude:prose block"
        assert "<!-- claude:prose:end -->" in content

    def test_architecture_page_has_generated_block(self, tmp_path):
        """Architecture.md also has the generated markers."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Architecture.md").read_text()
        assert "<!-- generated:start -->" in content
        assert "<!-- generated:end -->" in content

    def test_architecture_page_has_graph_td(self, tmp_path):
        """Architecture.md contains the graph TD diagram."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Architecture.md").read_text()
        assert "graph TD" in content


class TestLambdaPageProseBlock:
    """Tests that Lambda-Chat-Agent.md gets a claude:prose block on first run."""

    def test_lambda_page_has_prose_block(self, tmp_path):
        """On first run, Lambda-Chat-Agent.md is created with a claude:prose block."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        page = tmp_path / "Lambda-Chat-Agent.md"
        assert page.exists(), "Lambda-Chat-Agent.md should be created on first run"
        content = page.read_text()
        assert "<!-- claude:prose -->" in content, "Lambda-Chat-Agent.md must have claude:prose block"
        assert "<!-- claude:prose:end -->" in content

    def test_lambda_page_has_generated_block(self, tmp_path):
        """Lambda-Chat-Agent.md also has the generated markers."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Lambda-Chat-Agent.md").read_text()
        assert "<!-- generated:start -->" in content
        assert "<!-- generated:end -->" in content

    def test_lambda_page_has_sequence_diagram(self, tmp_path):
        """Lambda-Chat-Agent.md contains the sequence diagram."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "Lambda-Chat-Agent.md").read_text()
        assert "sequenceDiagram" in content


class TestCicdPageNoProseBlock:
    """Tests that CI-CD-Pipeline.md does NOT get a claude:prose block."""

    def test_cicd_page_no_prose_block(self, tmp_path):
        """On first run, CI-CD-Pipeline.md has no claude:prose block."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        page = tmp_path / "CI-CD-Pipeline.md"
        assert page.exists(), "CI-CD-Pipeline.md should be created on first run"
        content = page.read_text()
        assert "<!-- claude:prose -->" not in content, (
            "CI-CD-Pipeline.md must NOT have claude:prose block"
        )

    def test_cicd_page_has_generated_block(self, tmp_path):
        """CI-CD-Pipeline.md has generated markers."""
        run(repo_root=REPO_ROOT, wiki_dir=tmp_path)
        content = (tmp_path / "CI-CD-Pipeline.md").read_text()
        assert "<!-- generated:start -->" in content
        assert "<!-- generated:end -->" in content
