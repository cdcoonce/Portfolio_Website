"""Generator for wiki/Testing.md — test file inventory and pytest marker reference."""

from __future__ import annotations

import re
from pathlib import Path


def _read_jest_config(repo_root: Path) -> dict:
    """Parse key fields from jest.config.js.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    dict
        Dict with 'testEnvironment' and 'testMatch' keys (strings).
    """
    config_path = repo_root / "jest.config.js"
    if not config_path.exists():
        return {}
    text = config_path.read_text(encoding="utf-8")
    result: dict = {}
    env_match = re.search(r"testEnvironment\s*:\s*['\"]([^'\"]+)['\"]", text)
    if env_match:
        result["testEnvironment"] = env_match.group(1)
    match_match = re.search(r"testMatch\s*:\s*\[([^\]]+)\]", text)
    if match_match:
        patterns = re.findall(r"['\"]([^'\"]+)['\"]", match_match.group(1))
        result["testMatch"] = ", ".join(patterns)
    return result


def _read_pytest_markers(repo_root: Path) -> list[tuple[str, str]]:
    """Extract pytest markers from pyproject.toml.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    list[tuple[str, str]]
        List of (marker_name, description) tuples.
    """
    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.exists():
        return []
    text = pyproject_path.read_text(encoding="utf-8")

    # Step 1: extract the [tool.pytest.ini_options] section
    section_match = re.search(
        r'\[tool\.pytest\.ini_options\](.*?)(?=\n\[|\Z)',
        text,
        re.DOTALL,
    )
    if not section_match:
        return []

    section = section_match.group(1)

    # Step 2: find the markers = [ ... ] block within the section
    markers_match = re.search(r"markers\s*=\s*\[([^\]]+)\]", section, re.DOTALL)
    if not markers_match:
        return []

    block = markers_match.group(1)
    markers = []
    for line in re.findall(r'"([^"]+)"', block):
        # Format: "name: description"
        parts = line.split(":", 1)
        name = parts[0].strip()
        desc = parts[1].strip() if len(parts) > 1 else ""
        markers.append((name, desc))
    return markers


def _extract_describe_blocks(js_text: str) -> list[str]:
    """Extract top-level describe() block names from JS test content.

    Parameters
    ----------
    js_text : str
        Contents of a .test.js file.

    Returns
    -------
    list[str]
        List of describe block titles.
    """
    return re.findall(r"describe\(['\"]([^'\"]+)['\"]", js_text)


def generate(repo_root: Path) -> str:
    """Generate Testing.md content block for the wiki.

    Reads __tests__/*.test.js, tests/test_*.py, jest.config.js, and
    pyproject.toml to produce a test file inventory and pytest markers table.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    lines: list[str] = []

    # --- JS test files ---
    js_test_dir = repo_root / "__tests__"
    js_tests = sorted(js_test_dir.glob("*.test.js")) if js_test_dir.exists() else []

    lines.append("## JavaScript Tests\n")
    lines.append("| File | Type | Describe Blocks |")
    lines.append("|---|---|---|")
    for test_file in js_tests:
        text = test_file.read_text(encoding="utf-8")
        describes = _extract_describe_blocks(text)
        desc_str = ", ".join(describes[:3]) if describes else "—"
        if len(describes) > 3:
            desc_str += f", +{len(describes) - 3} more"
        lines.append(f"| `{test_file.name}` | Jest | {desc_str} |")
    if not js_tests:
        lines.append("| — | — | No .test.js files found |")
    lines.append("")

    # --- Jest config ---
    jest_config = _read_jest_config(repo_root)
    if jest_config:
        lines.append("### Jest Configuration\n")
        lines.append("| Setting | Value |")
        lines.append("|---|---|")
        for key, value in jest_config.items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.append("")

    # --- Python test files ---
    py_test_dir = repo_root / "tests"
    py_tests = sorted(py_test_dir.glob("test_*.py")) if py_test_dir.exists() else []
    lambda_test_dir = repo_root / "lambda" / "tests"
    if lambda_test_dir.exists():
        py_tests += sorted(lambda_test_dir.glob("test_*.py"))

    lines.append("## Python Tests\n")
    lines.append("| File | Location |")
    lines.append("|---|---|")
    for test_file in py_tests:
        try:
            rel = test_file.relative_to(repo_root)
        except ValueError:
            rel = test_file
        lines.append(f"| `{test_file.name}` | `{rel.parent}` |")
    if not py_tests:
        lines.append("| — | No test_*.py files found |")
    lines.append("")

    # --- pytest markers ---
    markers = _read_pytest_markers(repo_root)
    if markers:
        lines.append("## Pytest Markers\n")
        lines.append("| Marker | Description | Run Command |")
        lines.append("|---|---|---|")
        for name, desc in markers:
            lines.append(f"| `{name}` | {desc} | `uv run pytest -m {name}` |")
        lines.append("")

    return "\n".join(lines)
