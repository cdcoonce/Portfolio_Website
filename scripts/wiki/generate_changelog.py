"""Generator for wiki/Changelog.md — grouped conventional commit changelog."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


# Ordered display sequence for commit types
_TYPE_ORDER = [
    "feat",
    "fix",
    "refactor",
    "perf",
    "test",
    "docs",
    "style",
    "chore",
    "ci",
    "other",
]

_TYPE_LABELS = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "refactor": "Refactoring",
    "perf": "Performance",
    "test": "Tests",
    "docs": "Documentation",
    "style": "Style",
    "chore": "Chores",
    "ci": "CI/CD",
    "other": "Other",
}

# Matches: feat(scope): subject  or  feat: subject
_CONVENTIONAL_PATTERN = re.compile(
    r"^(feat|fix|refactor|perf|test|docs|style|chore|ci)(?:\([^)]+\))?(?:!)?:\s*(.+)$",
    re.IGNORECASE,
)


def _fetch_git_log(repo_root: Path, max_commits: int = 50) -> list[dict]:
    """Run git log and parse into structured commit records.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.
    max_commits : int
        Maximum number of commits to retrieve.

    Returns
    -------
    list[dict]
        List of dicts with keys: sha, subject, author, date, type, scope, body.
    """
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                f"--max-count={max_commits}",
                "--format=%H|%s|%an|%ad",
                "--date=short",
            ],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    commits = []
    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        sha, subject, author, date = parts[0], parts[1], parts[2], parts[3]

        # Parse conventional commit type
        m = _CONVENTIONAL_PATTERN.match(subject)
        if m:
            commit_type = m.group(1).lower()
            body = m.group(2).strip()
        else:
            commit_type = "other"
            body = subject

        commits.append(
            {
                "sha": sha[:8],
                "subject": subject,
                "body": body,
                "author": author,
                "date": date,
                "type": commit_type,
            }
        )
    return commits


def generate(repo_root: Path) -> str:
    """Generate Changelog.md content block for the wiki.

    Calls git log, parses conventional commit messages, groups by type,
    and returns a Markdown changelog showing the last 50 commits.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    commits = _fetch_git_log(repo_root, max_commits=50)
    lines: list[str] = []

    if not commits:
        lines.append("_No git history found._")
        return "\n".join(lines)

    # Group commits by type
    groups: dict[str, list[dict]] = {t: [] for t in _TYPE_ORDER}
    for commit in commits:
        t = commit["type"]
        if t not in groups:
            t = "other"
        groups[t].append(commit)

    lines.append(f"_Last {len(commits)} commits — grouped by conventional commit type._\n")

    for commit_type in _TYPE_ORDER:
        type_commits = groups[commit_type]
        if not type_commits:
            continue
        label = _TYPE_LABELS.get(commit_type, commit_type.title())
        lines.append(f"## {commit_type}\n")
        lines.append(f"### {label}\n")
        for c in type_commits:
            lines.append(f"- **{c['date']}** `{c['sha']}` — {c['body']}")
        lines.append("")

    return "\n".join(lines)
