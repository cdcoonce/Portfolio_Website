"""Orchestrator for the auto-updating wiki system.

Entry point: run() or invoke directly with ``python scripts/wiki/orchestrate.py``.

Marker convention
-----------------
- ``<!-- generated:start -->`` … ``<!-- generated:end -->`` — owned by this script.
  Content between these markers is replaced on every run.
- ``<!-- claude:prose -->`` … ``<!-- claude:prose:end -->`` — owned by the Claude skill.
  Content between these markers is NEVER touched by this script.

Usage
-----
From the repo root::

    python scripts/wiki/orchestrate.py
"""

from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path

# Ensure scripts/ is on sys.path when this file is run directly as a script,
# so that ``from wiki import ...`` resolves correctly.
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# ---------------------------------------------------------------------------
# Marker constants
# ---------------------------------------------------------------------------

GEN_START = "<!-- generated:start -->"
GEN_END = "<!-- generated:end -->"


# ---------------------------------------------------------------------------
# Splice logic
# ---------------------------------------------------------------------------


def splice_content(existing: str, new_content: str) -> str:
    """Replace content between generated markers, leaving everything else intact.

    Parameters
    ----------
    existing : str
        Current file contents (may already have markers, prose blocks, etc.)
    new_content : str
        The new generated content to insert between the markers.

    Returns
    -------
    str
        Updated file contents with generated block replaced.

    Raises
    ------
    ValueError
        If ``generated:start`` or ``generated:end`` markers are missing.
    """
    pattern = re.compile(
        r"(<!-- generated:start -->)(.*?)(<!-- generated:end -->)",
        re.DOTALL,
    )
    if not pattern.search(existing):
        raise ValueError("Generated markers not found in file content")

    matches = pattern.findall(existing)
    if len(matches) > 1:
        raise ValueError(
            f"File contains {len(matches)} generated blocks; named blocks not yet supported"
        )

    replacement = f"{GEN_START}\n{new_content.rstrip()}\n{GEN_END}"
    return pattern.sub(lambda _: replacement, existing)


def _build_fresh_home(generated_content: str) -> str:
    """Build a brand-new Home.md file content with correct marker structure.

    Home.md has no ``claude:prose`` block by design (spec: pages without
    prose sections get no prose markers on first run).

    Parameters
    ----------
    generated_content : str
        The output from the generate_home generator.

    Returns
    -------
    str
        Complete file contents for a new Home.md.
    """
    return (
        "# Home\n\n"
        f"{GEN_START}\n"
        f"{generated_content.rstrip()}\n"
        f"{GEN_END}\n"
    )


def _build_fresh_page(title: str, generated_content: str, *, prose: bool = False) -> str:
    """Build a brand-new wiki page with correct marker structure.

    Parameters
    ----------
    title : str
        Page heading (H1).
    generated_content : str
        The output from the page generator.
    prose : bool
        If True, append an empty ``claude:prose`` block for human narrative.

    Returns
    -------
    str
        Complete file contents for the new page.
    """
    parts = [
        f"# {title}\n\n",
        f"{GEN_START}\n",
        f"{generated_content.rstrip()}\n",
        f"{GEN_END}\n",
    ]
    if prose:
        parts += [
            "\n<!-- claude:prose -->\n",
            "\n<!-- claude:prose:end -->\n",
        ]
    return "".join(parts)


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _git_sha(repo_root: Path) -> str:
    """Return the short git SHA for the current HEAD commit.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Short SHA string, or 'unknown' if git is unavailable.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


# ---------------------------------------------------------------------------
# Special file writers
# ---------------------------------------------------------------------------


def _write_sidebar(wiki_dir: Path) -> None:
    """Write _Sidebar.md with grouped navigation sections.

    Parameters
    ----------
    wiki_dir : Path
        Directory where wiki files are written.
    """
    content = (
        "## Reference\n\n"
        "- [[Home]]\n"
        "- [[Changelog]]\n"
        "- [[Knowledge-Base]]\n\n"
        "## Architecture\n\n"
        "- [[Architecture]]\n"
        "- [[Frontend-Modules]]\n"
        "- [[Lambda]]\n"
        "- [[CI-CD]]\n\n"
        "## Dev Guide\n\n"
        "- [[Contributing]]\n"
        "- [[Testing]]\n"
        "- [[CSS-Design-System]]\n"
        "- [[Architecture-Decision-Log]]\n"
    )
    (wiki_dir / "_Sidebar.md").write_text(content, encoding="utf-8")


def _write_footer(wiki_dir: Path, repo_root: Path) -> None:
    """Write _Footer.md with last-regenerated timestamp and git SHA.

    Parameters
    ----------
    wiki_dir : Path
        Directory where wiki files are written.
    repo_root : Path
        Repository root (used to resolve git SHA).
    """
    today = datetime.date.today().isoformat()
    sha = _git_sha(repo_root)
    content = f"Last regenerated: {today} · {sha}\n"
    (wiki_dir / "_Footer.md").write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Generator registry
# ---------------------------------------------------------------------------


def _get_generators() -> list[tuple[str, object]]:
    """Return the list of registered (wiki_filename, generator_module) pairs.

    Returns
    -------
    list[tuple[str, object]]
        Each entry is (output filename without .md extension, module object).
    """
    # Import here to avoid circular issues; makes mocking easy in tests too.
    from wiki import generate_home  # noqa: PLC0415

    return [
        ("Home", generate_home),
    ]


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def run(repo_root: Path | None = None, wiki_dir: Path | None = None) -> None:
    """Run all registered generators and write wiki files.

    Parameters
    ----------
    repo_root : Path, optional
        Root of the repository. Defaults to ``Path.cwd()``.
    wiki_dir : Path, optional
        Directory to write wiki files into. Defaults to ``repo_root / 'wiki'``.
    """
    if repo_root is None:
        repo_root = Path.cwd()
    if wiki_dir is None:
        wiki_dir = repo_root / "wiki"

    wiki_dir.mkdir(parents=True, exist_ok=True)

    for page_name, generator_module in _get_generators():
        generated_content = generator_module.generate(repo_root)
        output_path = wiki_dir / f"{page_name}.md"

        if output_path.exists():
            existing = output_path.read_text(encoding="utf-8")
            if GEN_START in existing and GEN_END in existing:
                updated = splice_content(existing, generated_content)
            else:
                # File exists but has no generated markers — prepend block
                block = f"{GEN_START}\n{generated_content.rstrip()}\n{GEN_END}\n\n"
                updated = block + existing
        else:
            # First run: create file with correct marker structure
            if page_name == "Home":
                updated = _build_fresh_home(generated_content)
            else:
                updated = _build_fresh_page(page_name, generated_content, prose=True)

        output_path.write_text(updated, encoding="utf-8")

    _write_sidebar(wiki_dir)
    _write_footer(wiki_dir, repo_root)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    # Allow an optional repo_root argument from the CLI
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path.cwd()

    run(repo_root=root)
    print(f"Wiki generated in {root / 'wiki'}")
