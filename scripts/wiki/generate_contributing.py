"""Generator for wiki/Contributing.md — setup steps, make/npm targets, commit conventions."""

from __future__ import annotations

import json
import re
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
    try:
        return json.loads(pkg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _read_makefile_targets(repo_root: Path) -> list[tuple[str, str]]:
    """Extract .PHONY targets and their recipe comments from Makefile.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    list[tuple[str, str]]
        List of (target_name, recipe_first_line) tuples.
    """
    makefile = repo_root / "Makefile"
    if not makefile.exists():
        return []

    text = makefile.read_text(encoding="utf-8")
    targets = []

    # Find .PHONY line to get declared targets
    phony_match = re.search(r"\.PHONY\s*:\s*(.+)", text)
    phony_targets: list[str] = []
    if phony_match:
        phony_targets = phony_match.group(1).split()

    # Parse target blocks: "target:\n\t<recipe>"
    target_pattern = re.compile(r"^(\w[\w-]*):\s*\n((?:\t[^\n]*\n?)+)", re.MULTILINE)
    recipe_map: dict[str, str] = {}
    for match in target_pattern.finditer(text):
        name = match.group(1)
        first_recipe_line = match.group(2).strip().split("\n")[0].strip()
        recipe_map[name] = first_recipe_line

    # Use phony order if available, fall back to recipe_map order
    seen: set[str] = set()
    for name in phony_targets:
        if name not in seen:
            recipe = recipe_map.get(name, "")
            targets.append((name, recipe))
            seen.add(name)

    for name, recipe in recipe_map.items():
        if name not in seen:
            targets.append((name, recipe))
            seen.add(name)

    return targets


def generate(repo_root: Path) -> str:
    """Generate Contributing.md content block for the wiki.

    Reads CLAUDE.md, package.json, pyproject.toml, and Makefile to produce
    local setup steps, a make/npm targets table, and commit convention rules.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    pkg = _read_package_json(repo_root)
    make_targets = _read_makefile_targets(repo_root)

    lines: list[str] = []

    # --- Local setup steps ---
    lines.append("## Local Setup\n")
    lines.append("1. **Clone the repository**")
    lines.append("   ```")
    lines.append("   git clone https://github.com/cdcoonce/Portfolio_Website.git")
    lines.append("   cd Portfolio_Website")
    lines.append("   ```")
    lines.append("")
    lines.append("2. **Install JavaScript dependencies**")
    lines.append("   ```")
    lines.append("   npm install")
    lines.append("   ```")
    lines.append("")
    lines.append("3. **Install Python dependencies** (requires [uv](https://github.com/astral-sh/uv))")
    lines.append("   ```")
    lines.append("   uv sync")
    lines.append("   ```")
    lines.append("")
    lines.append("4. **Run all tests**")
    lines.append("   ```")
    lines.append("   make test")
    lines.append("   ```")
    lines.append("")

    # --- Make targets table ---
    if make_targets:
        lines.append("## Make Targets\n")
        lines.append("| Target | Command / Description |")
        lines.append("|---|---|")
        for name, recipe in make_targets:
            recipe_str = f"`{recipe}`" if recipe else "—"
            lines.append(f"| `make {name}` | {recipe_str} |")
        lines.append("")

    # --- npm scripts table ---
    scripts = pkg.get("scripts", {})
    if scripts:
        lines.append("## npm Scripts\n")
        lines.append("| Script | Command |")
        lines.append("|---|---|")
        for name, cmd in scripts.items():
            lines.append(f"| `npm run {name}` | `{cmd}` |")
        lines.append("")

    # --- Commit conventions ---
    lines.append("## Commit Conventions\n")
    lines.append("This project follows [Conventional Commits](https://www.conventionalcommits.org/).\n")
    lines.append("Format: `<type>(<scope>): <subject>`\n")
    lines.append("| Type | Purpose |")
    lines.append("|---|---|")
    lines.append("| `feat` | New feature |")
    lines.append("| `fix` | Bug fix |")
    lines.append("| `refactor` | Code change that is neither a fix nor a feature |")
    lines.append("| `docs` | Documentation only |")
    lines.append("| `test` | Adding or updating tests |")
    lines.append("| `chore` | Build process, tooling, maintenance |")
    lines.append("| `style` | Formatting, whitespace — no logic change |")
    lines.append("| `perf` | Performance improvement |")
    lines.append("| `ci` | CI/CD pipeline changes |")
    lines.append("")
    lines.append("**Examples:**")
    lines.append("```")
    lines.append("feat(wiki): add changelog generator")
    lines.append("fix(chat): handle empty API response gracefully")
    lines.append("docs(contributing): update setup instructions")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)
