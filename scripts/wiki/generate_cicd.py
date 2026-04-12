"""Generator for wiki/CI-CD-Pipeline.md — pipeline flowchart and branch strategy diagrams."""

from __future__ import annotations

from pathlib import Path


def _read_workflow(repo_root: Path) -> str:
    """Read the primary CI/CD workflow file.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Raw YAML content, or empty string if not found.
    """
    workflow_path = repo_root / ".github" / "workflows" / "ci-cd.yml"
    if not workflow_path.exists():
        return ""
    return workflow_path.read_text(encoding="utf-8")


def generate(repo_root: Path) -> str:
    """Generate CI-CD-Pipeline.md content block for the wiki.

    Reads .github/workflows/ci-cd.yml and produces a pipeline flowchart
    and a gitGraph branch strategy diagram.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
        Does NOT include the marker comments — the orchestrator wraps it.
    """
    workflow_text = _read_workflow(repo_root)

    lines: list[str] = []

    lines.append("## CI/CD Pipeline\n")
    lines.append(
        "The project uses GitHub Actions for continuous integration and deployment. "
        "Every push to `master` and every pull request targeting `master` triggers the "
        "Lint & Test job. On a successful push to `master`, the Deploy job merges the "
        "branch into `gh-pages` to publish the site.\n"
    )

    # --- Pipeline flowchart ---
    lines.append("### Pipeline Flowchart\n")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append('    Push["Push / PR to master"]')
    lines.append('    Checkout["Checkout code"]')
    lines.append('    NodeSetup["Set up Node.js 20\\n+ npm ci"]')
    lines.append('    PythonSetup["Set up Python 3.12\\n(uv sync)"]')
    lines.append('    Playwright["Install Playwright\\nbrowsers"]')
    lines.append('    Lint["Lint & Format\\n(Prettier · Stylelint · ESLint)"]')
    lines.append('    JSTests["JS unit tests\\n(Jest)"]')
    lines.append('    PyTests["Python tests\\n(pytest -m not slow)"]')
    lines.append('    Check{"All checks pass?"}')
    lines.append('    Deploy["Deploy to gh-pages\\n(merge master → gh-pages)"]')
    lines.append('    Done["Site live on GitHub Pages"]')
    lines.append('    Fail["Pipeline fails\\n(PR blocked)"]')
    lines.append("")
    lines.append("    Push --> Checkout")
    lines.append("    Checkout --> NodeSetup")
    lines.append("    Checkout --> PythonSetup")
    lines.append("    NodeSetup --> Playwright")
    lines.append("    PythonSetup --> Playwright")
    lines.append("    Playwright --> Lint")
    lines.append("    Lint --> JSTests")
    lines.append("    JSTests --> PyTests")
    lines.append("    PyTests --> Check")
    lines.append("    Check -->|yes + push to master| Deploy")
    lines.append("    Check -->|no| Fail")
    lines.append("    Deploy --> Done")
    lines.append("```\n")

    # --- Branch strategy ---
    lines.append("### Branch Strategy\n")
    lines.append("```mermaid")
    lines.append("gitGraph")
    lines.append("    commit id: \"initial\"")
    lines.append("    branch feature")
    lines.append("    checkout feature")
    lines.append("    commit id: \"feat: work\"")
    lines.append("    commit id: \"fix: review\"")
    lines.append("    checkout master")
    lines.append("    merge feature id: \"PR merge\"")
    lines.append("    commit id: \"chore: follow-up\"")
    lines.append("```\n")

    # --- Trigger matrix ---
    lines.append("## Trigger Matrix\n")
    lines.append("| Event | Branch | Jobs Triggered |")
    lines.append("|---|---|---|")
    lines.append("| `push` | `master` | Lint & Test, Deploy |")
    lines.append("| `pull_request` | `master` | Lint & Test only |")
    lines.append("")

    # --- Workflow file info ---
    workflow_files = list((repo_root / ".github" / "workflows").glob("*.yml")) if (
        repo_root / ".github" / "workflows"
    ).exists() else []

    lines.append("## Workflow Files\n")
    lines.append("| File | Triggers |")
    lines.append("|---|---|")
    if workflow_files:
        for wf_file in sorted(workflow_files):
            lines.append(f"| `.github/workflows/{wf_file.name}` | push, pull_request |")
    else:
        lines.append("| _(no workflow files found)_ | — |")
    lines.append("")

    return "\n".join(lines)
