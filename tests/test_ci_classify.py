"""Tests for the `classify` gate in `.github/workflows/ci-cd.yml`.

The gate decides whether a push gets the full lint/test/e2e suite or skips
straight to deploy. It exists because the afk-cockpit publisher pushes a
regenerated dashboard snapshot to `main` roughly every 31 minutes, and
validating a data refresh with a full Playwright install is pure waste.

The failure mode is silent and expensive: if the gate wrongly classifies a
real source change as "generated only", broken code deploys to production
with no validation at all. So the gate is tested rather than trusted, against
a hermetic throwaway repository built per-test.

The shell is extracted from the workflow itself, so these tests fail if
someone edits the workflow logic without updating them.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.ci

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci-cd.yml"

# The one file the afk-cockpit publisher rewrites. Kept in sync with the
# GENERATED constant inside the workflow's classify step.
GENERATED = "public/afk-cockpit/index.html"
ZERO_SHA = "0" * 40


@pytest.fixture(scope="session")
def base_url() -> str:
    """Shadow the browser suite's `base_url` fixture.

    `pytest-base-url` registers a session-scoped autouse fixture that requests
    `base_url`, and `tests/conftest.py` overrides `base_url` to build the Astro
    site and serve `dist/` over HTTP. That makes every test in this directory —
    including these, which never open a browser — depend on a completed build.
    Shadowing it at module scope keeps this file runnable on a clean checkout.
    """
    return "http://127.0.0.1:0"


def _classify_script() -> str:
    """Extract the classify step's shell body from the committed workflow."""
    workflow = yaml.safe_load(WORKFLOW.read_text())
    steps = workflow["jobs"]["classify"]["steps"]
    for step in steps:
        if step.get("id") == "classify":
            return step["run"]
    raise AssertionError("no step with id 'classify' in the classify job")


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _commit(repo: Path, path: str, body: str, message: str) -> str:
    """Write `path`, commit it, and return the resulting SHA."""
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    _git(repo, "add", "--", path)
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A throwaway git repo seeded with one generated file and one source file."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "test")
    _commit(repo, GENERATED, "<html>seed</html>\n", "seed: generated")
    _commit(repo, "src/data/portfolio.js", "export const x = 0;\n", "seed: source")
    return repo


def _run(repo: Path, tmp_path: Path, event: str, before: str, sha: str) -> str:
    """Run the extracted classify shell and return the emitted code_changed value."""
    output_file = tmp_path / "gh_output"
    output_file.write_text("")
    result = subprocess.run(
        ["bash", "-c", _classify_script()],
        cwd=repo,
        capture_output=True,
        text=True,
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "EVENT": event,
            "BEFORE": before,
            "SHA": sha,
            "GITHUB_OUTPUT": str(output_file),
        },
    )
    assert result.returncode == 0, f"classify exited {result.returncode}:\n{result.stderr}"
    emitted = [
        line.split("=", 1)[1]
        for line in output_file.read_text().splitlines()
        if line.startswith("code_changed=")
    ]
    assert len(emitted) == 1, f"expected exactly one code_changed, got {emitted}"
    return emitted[0]


class TestSkipsGeneratedOnlyPushes:
    """The ~48/day snapshot pushes must not pay for the full suite."""

    def test_single_generated_commit_skips_validation(self, repo, tmp_path):
        before = _git(repo, "rev-parse", "HEAD")
        sha = _commit(repo, GENERATED, "<html>refreshed</html>\n", "chore: refresh")
        assert _run(repo, tmp_path, "push", before, sha) == "false"

    def test_several_generated_commits_in_one_push_skip_validation(self, repo, tmp_path):
        before = _git(repo, "rev-parse", "HEAD")
        for n in range(3):
            sha = _commit(repo, GENERATED, f"<html>{n}</html>\n", "chore: refresh")
        assert _run(repo, tmp_path, "push", before, sha) == "false"


class TestValidatesRealChanges:
    """Anything touching source must run the full suite before deploying."""

    def test_source_change_runs_validation(self, repo, tmp_path):
        before = _git(repo, "rev-parse", "HEAD")
        sha = _commit(repo, "src/data/portfolio.js", "export const x = 1;\n", "feat: bump")
        assert _run(repo, tmp_path, "push", before, sha) == "true"

    def test_source_and_generated_together_runs_validation(self, repo, tmp_path):
        """A mixed push must not be waved through by the generated file."""
        before = _git(repo, "rev-parse", "HEAD")
        _commit(repo, GENERATED, "<html>refreshed</html>\n", "chore: refresh")
        sha = _commit(repo, "src/data/portfolio.js", "export const x = 2;\n", "feat: bump")
        assert _run(repo, tmp_path, "push", before, sha) == "true"

    def test_file_with_generated_as_prefix_runs_validation(self, repo, tmp_path):
        """Exact-match only: a sibling path must not be mistaken for the snapshot."""
        before = _git(repo, "rev-parse", "HEAD")
        sha = _commit(repo, f"{GENERATED}.bak", "<html>decoy</html>\n", "chore: decoy")
        assert _run(repo, tmp_path, "push", before, sha) == "true"


class TestFailsOpen:
    """An undiffable push must run everything. Never deploy unvalidated."""

    def test_pull_request_event_runs_validation(self, repo, tmp_path):
        before = _git(repo, "rev-parse", "HEAD~1")
        sha = _git(repo, "rev-parse", "HEAD")
        assert _run(repo, tmp_path, "pull_request", before, sha) == "true"

    def test_zero_before_sha_runs_validation(self, repo, tmp_path):
        sha = _git(repo, "rev-parse", "HEAD")
        assert _run(repo, tmp_path, "push", ZERO_SHA, sha) == "true"

    def test_empty_before_sha_runs_validation(self, repo, tmp_path):
        sha = _git(repo, "rev-parse", "HEAD")
        assert _run(repo, tmp_path, "push", "", sha) == "true"

    def test_unreachable_before_sha_runs_validation(self, repo, tmp_path):
        """After a force-push the before-SHA may no longer exist."""
        sha = _git(repo, "rev-parse", "HEAD")
        assert _run(repo, tmp_path, "push", "de" * 20, sha) == "true"

    def test_empty_diff_runs_validation(self, repo, tmp_path):
        sha = _git(repo, "rev-parse", "HEAD")
        assert _run(repo, tmp_path, "push", sha, sha) == "true"


class TestDeployGateWiring:
    """The `if:` expressions are the other half of the gate; assert their shape.

    `always()` is load-bearing (a skipped dependency would otherwise skip
    deploy) and simultaneously dangerous (it would deploy through a red suite
    unless every failure state is re-asserted). Pin both halves.
    """

    @pytest.fixture
    def jobs(self):
        return yaml.safe_load(WORKFLOW.read_text())["jobs"]

    def test_heavy_jobs_are_gated_on_the_classifier(self, jobs):
        for name in ("check", "e2e"):
            assert jobs[name]["needs"] == "classify"
            assert jobs[name]["if"] == "needs.classify.outputs.code_changed == 'true'"

    def test_deploy_survives_skipped_dependencies(self, jobs):
        assert "always()" in jobs["deploy"]["if"]

    def test_deploy_refuses_failed_or_cancelled_dependencies(self, jobs):
        condition = " ".join(jobs["deploy"]["if"].split())
        for job in ("check", "e2e"):
            for state in ("failure", "cancelled"):
                assert f"needs.{job}.result != '{state}'" in condition, (
                    f"deploy must not run when {job} is {state}"
                )
        assert "needs.classify.result == 'success'" in condition

    def test_this_file_is_actually_selected_by_ci(self, jobs):
        """Guard the wiring that runs these tests at all.

        pytest is only ever invoked with an explicit `-m` expression, so
        dropping `ci` from that selector would not fail anything -- this file
        would just quietly stop running, and the classifier would go back to
        being trusted rather than tested.
        """
        runs = [
            " ".join(step["run"].split())
            for step in jobs["e2e"]["steps"]
            if "pytest" in str(step.get("run", ""))
        ]
        assert runs, "the e2e job no longer invokes pytest at all"
        assert any(
            "or ci" in run or '-m "ci' in run for run in runs
        ), f"no pytest invocation selects the `ci` marker: {runs}"

    def test_deploy_only_publishes_from_main(self, jobs):
        condition = " ".join(jobs["deploy"]["if"].split())
        assert "github.event_name == 'push'" in condition
        assert "github.ref == 'refs/heads/main'" in condition

    def test_manual_dispatch_can_actually_deploy(self, jobs):
        """A dispatch trigger that cannot deploy is a trap, not an escape hatch.

        `workflow_dispatch` exists so `main` can be republished without an
        empty commit. If the deploy gate only admits `push`, a dispatch runs
        the full suite and then silently skips the deploy -- which looks like
        success and publishes nothing.
        """
        workflow = yaml.safe_load(WORKFLOW.read_text())
        assert "workflow_dispatch" in workflow[True], (
            "workflow_dispatch trigger missing"
        )
        condition = " ".join(jobs["deploy"]["if"].split())
        assert "github.event_name == 'workflow_dispatch'" in condition, (
            "deploy admits push but not workflow_dispatch: a manual run would "
            f"validate and then skip publishing. Condition: {condition}"
        )


def test_generated_path_matches_the_workflow():
    """This test file and the workflow must name the same generated file."""
    assert f"GENERATED='{GENERATED}'" in _classify_script()
