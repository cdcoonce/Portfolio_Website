"""Generator for wiki/Knowledge-Base.md — context file inventory."""

from __future__ import annotations

import re
from pathlib import Path


def _count_words(text: str) -> int:
    """Count words in a string.

    Parameters
    ----------
    text : str
        Input text.

    Returns
    -------
    int
        Number of whitespace-separated tokens.
    """
    return len(text.split())


def _infer_topic(filename: str, text: str) -> str:
    """Infer a topic label from the filename and/or first heading.

    Parameters
    ----------
    filename : str
        The .md filename without path, e.g. 'bio.md'.
    text : str
        File contents.

    Returns
    -------
    str
        Short topic description.
    """
    # Try first H1/H2 heading
    heading_match = re.search(r"^#{1,2}\s+(.+)$", text, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    # Fall back to filename (strip .md, replace hyphens/underscores with spaces, title-case)
    stem = Path(filename).stem
    return stem.replace("-", " ").replace("_", " ").title()


def generate(repo_root: Path) -> str:
    """Generate Knowledge-Base.md content block for the wiki.

    Reads all *.md files in WebContent/context/ and produces an inventory
    table with filename, word count, and inferred topic.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    context_dir = repo_root / "WebContent" / "context"
    lines: list[str] = []

    lines.append("## Knowledge Base Files\n")
    lines.append("These Markdown files are loaded into the Lambda chat agent's context window.\n")

    if not context_dir.exists():
        lines.append("_No context files found (WebContent/context/ does not exist)._")
        return "\n".join(lines)

    md_files = sorted(context_dir.glob("*.md"))

    if not md_files:
        lines.append("_No .md files found in WebContent/context/._")
        return "\n".join(lines)

    lines.append("| File | Word Count | Topic |")
    lines.append("|---|---|---|")

    total_words = 0
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        wc = _count_words(text)
        total_words += wc
        topic = _infer_topic(md_file.name, text)
        lines.append(f"| `{md_file.name}` | {wc:,} | {topic} |")

    lines.append("")
    lines.append(f"**Total:** {len(md_files)} files · {total_words:,} words\n")

    return "\n".join(lines)
