"""Generator for wiki/Home.md — tech stack, test commands, npm scripts."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


def _read_package_json(repo_root: Path) -> dict:
    """Read and parse package.json.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    dict
        Parsed package.json contents, or empty dict on failure.
    """
    pkg_path = repo_root / "package.json"
    if not pkg_path.exists():
        return {}
    return json.loads(pkg_path.read_text(encoding="utf-8"))


def _read_pyproject(repo_root: Path) -> str:
    """Read pyproject.toml as raw text.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Raw file contents, or empty string on failure.
    """
    path = repo_root / "pyproject.toml"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_python_version(pyproject_text: str) -> str:
    """Extract requires-python version from pyproject.toml text.

    Parameters
    ----------
    pyproject_text : str
        Raw pyproject.toml contents.

    Returns
    -------
    str
        Version string like '>=3.11', or empty string if not found.
    """
    match = re.search(r'requires-python\s*=\s*"([^"]+)"', pyproject_text)
    return match.group(1) if match else ""


def _extract_python_deps(pyproject_text: str) -> list[str]:
    """Extract dev dependency names from pyproject.toml.

    Parameters
    ----------
    pyproject_text : str
        Raw pyproject.toml contents.

    Returns
    -------
    list[str]
        List of package names without version constraints.
    """
    # Find content of [dependency-groups] dev = [ ... ]
    match = re.search(r'\[dependency-groups\][^\[]*dev\s*=\s*\[([^\]]+)\]', pyproject_text, re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    # Extract quoted package names (strip version constraints)
    entries = re.findall(r'"([a-zA-Z0-9_-]+)', block)
    return entries


def generate(repo_root: Path) -> str:
    """Generate Home.md content block for the wiki.

    Reads package.json, pyproject.toml, and produces a tech stack table,
    test commands section, and npm scripts section as Markdown.

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
    pkg = _read_package_json(repo_root)
    pyproject = _read_pyproject(repo_root)

    project_name = pkg.get("name", "portfoliowebsite")
    project_version = pkg.get("version", "unknown")
    python_version = _extract_python_version(pyproject)
    python_deps = _extract_python_deps(pyproject)
    dev_deps = pkg.get("devDependencies", {})

    # --- Tech stack table ---
    node_version = dev_deps.get("jest", "").lstrip("^~") or "see package.json"
    jest_version = dev_deps.get("jest", "unknown").lstrip("^~")
    eslint_version = dev_deps.get("eslint", "unknown").lstrip("^~")
    prettier_version = dev_deps.get("prettier", "unknown").lstrip("^~")

    lines: list[str] = []
    lines.append(f"## {project_name} v{project_version}\n")
    lines.append("### Tech Stack\n")
    lines.append("| Language / Tool | Version / Notes |")
    lines.append("|---|---|")
    lines.append(f"| Node.js | see `.nvmrc` or system Node |")
    lines.append(f"| Python | `{python_version}` |")
    lines.append(f"| Jest (JS test runner) | `{jest_version}` |")
    lines.append(f"| ESLint | `{eslint_version}` |")
    lines.append(f"| Prettier | `{prettier_version}` |")
    lines.append(f"| uv (Python package manager) | see `pyproject.toml` |")

    if python_deps:
        deps_str = ", ".join(f"`{d}`" for d in python_deps)
        lines.append(f"| Python dev deps | {deps_str} |")

    lines.append("")

    # --- Test commands ---
    lines.append("### Test Commands\n")
    lines.append("| Command | Description |")
    lines.append("|---|---|")
    lines.append("| `npm test` | Run JavaScript test suite (Jest) |")
    lines.append("| `npm run test:coverage` | JS tests with coverage report |")
    lines.append("| `uv run pytest` | Run Python test suite |")
    lines.append("| `uv run pytest --cov=src --cov-report=term-missing` | Python tests with coverage |")
    lines.append("")

    # --- npm scripts ---
    scripts = pkg.get("scripts", {})
    if scripts:
        lines.append("### npm Scripts\n")
        lines.append("| Script | Command |")
        lines.append("|---|---|")
        for name, cmd in scripts.items():
            lines.append(f"| `npm run {name}` | `{cmd}` |")
        lines.append("")

    return "\n".join(lines)
