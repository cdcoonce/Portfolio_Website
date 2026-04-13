"""Tests for Phase 4: CI sync workflow — .github/workflows/wiki-sync.yml.

These tests parse the YAML file and assert structural properties without
actually running the workflow.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "wiki-sync.yml"


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Parse wiki-sync.yml and return as a dict."""
    assert WORKFLOW_PATH.exists(), (
        f"Workflow file not found: {WORKFLOW_PATH}"
    )
    return yaml.safe_load(WORKFLOW_PATH.read_text())


@pytest.fixture(scope="module")
def workflow_text() -> str:
    """Return the raw text of wiki-sync.yml."""
    assert WORKFLOW_PATH.exists(), (
        f"Workflow file not found: {WORKFLOW_PATH}"
    )
    return WORKFLOW_PATH.read_text()


# ---------------------------------------------------------------------------
# Trigger tests
# ---------------------------------------------------------------------------


def _get_push_trigger(workflow: dict) -> dict:
    """Return the push trigger dict, handling PyYAML's `on` -> True coercion."""
    # PyYAML parses the unquoted `on:` key as Python bool True.
    trigger_block = workflow.get(True) or workflow.get("on") or {}
    return trigger_block.get("push", {})


class TestTrigger:
    """Tests for the on.push trigger configuration."""

    def test_workflow_has_push_trigger(self, workflow: dict):
        """Workflow triggers on push to master."""
        push = _get_push_trigger(workflow)
        branches = push.get("branches", [])
        assert "master" in branches, (
            f"Expected 'master' in on.push.branches, got: {branches}"
        )

    def test_workflow_has_path_filters(self, workflow: dict):
        """All 8 watched path patterns are present in on.push.paths."""
        push = _get_push_trigger(workflow)
        paths = push.get("paths", [])
        expected = [
            "WebContent/js/**",
            "WebContent/css/**",
            "WebContent/context/**",
            "lambda/**",
            "__tests__/**",
            "tests/**",
            ".github/workflows/**",
            "scripts/wiki/**",
        ]
        for pattern in expected:
            assert pattern in paths, (
                f"Expected path pattern '{pattern}' not found in on.push.paths: {paths}"
            )

    def test_workflow_has_scripts_wiki_path_trigger(self, workflow: dict):
        """scripts/wiki/** is in on.push.paths so generator changes trigger CI."""
        push = _get_push_trigger(workflow)
        paths = push.get("paths", [])
        assert "scripts/wiki/**" in paths, (
            f"'scripts/wiki/**' must be in on.push.paths so that generator "
            f"changes trigger the wiki sync workflow; got: {paths}"
        )

    def test_workflow_readme_not_in_paths(self, workflow: dict):
        """README.md is NOT in path triggers (doc-only pushes must not fire)."""
        push = _get_push_trigger(workflow)
        paths = push.get("paths", [])
        assert "README.md" not in paths, (
            "README.md must NOT be a path trigger"
        )

    def test_workflow_docs_not_in_paths(self, workflow: dict):
        """docs/ is NOT in path triggers (doc-only pushes must not fire)."""
        push = _get_push_trigger(workflow)
        paths = push.get("paths", [])
        docs_patterns = [p for p in paths if p.startswith("docs")]
        assert len(docs_patterns) == 0, (
            f"docs/ patterns must NOT be in path triggers, found: {docs_patterns}"
        )


# ---------------------------------------------------------------------------
# Permissions tests
# ---------------------------------------------------------------------------


class TestPermissions:
    """Tests for workflow-level permissions."""

    def test_workflow_has_contents_write_permission(self, workflow: dict):
        """sync-wiki job declares permissions.contents == 'write'."""
        jobs = workflow["jobs"]
        sync_job = jobs["sync-wiki"]
        assert sync_job["permissions"]["contents"] == "write", (
            f"Expected sync-wiki job permissions.contents == 'write', "
            f"got: {sync_job.get('permissions', {}).get('contents')}"
        )


# ---------------------------------------------------------------------------
# Steps tests
# ---------------------------------------------------------------------------


class TestSteps:
    """Tests for required workflow steps."""

    def test_workflow_uses_github_token(self, workflow_text: str):
        """secrets.GITHUB_TOKEN appears in the workflow (used for wiki push auth)."""
        assert "secrets.GITHUB_TOKEN" in workflow_text, (
            "secrets.GITHUB_TOKEN must appear in the workflow for authentication"
        )

    def test_workflow_has_fetch_depth_zero(self, workflow_text: str):
        """fetch-depth: 0 is set to enable full git history for changelog."""
        assert "fetch-depth: 0" in workflow_text, (
            "fetch-depth: 0 must be set so git log works for changelog generation"
        )

    def test_workflow_has_orchestrator_step(self, workflow_text: str):
        """scripts/wiki/orchestrate.py appears in the workflow."""
        assert "scripts/wiki/orchestrate.py" in workflow_text, (
            "Orchestrator step must run scripts/wiki/orchestrate.py"
        )

    def test_workflow_has_wiki_clone_step(self, workflow_text: str):
        """Wiki git clone step is present."""
        assert ".wiki.git" in workflow_text, (
            "Workflow must clone the wiki repo (*.wiki.git)"
        )

    def test_workflow_has_commit_push_step(self, workflow_text: str):
        """Commit message contains 'chore(wiki): regenerate'."""
        assert "chore(wiki): regenerate" in workflow_text, (
            "Commit step must use message starting with 'chore(wiki): regenerate'"
        )

    def test_workflow_commit_references_sha(self, workflow_text: str):
        """github.sha appears in the workflow (commit message interpolates the SHA)."""
        assert "github.sha" in workflow_text, (
            "Commit message must interpolate github.sha for traceability"
        )
