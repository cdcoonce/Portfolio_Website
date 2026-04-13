"""Generator for wiki/CSS-Design-System.md — custom properties and breakpoints."""

from __future__ import annotations

import re
from pathlib import Path


def _extract_custom_properties(css_text: str) -> list[tuple[str, str]]:
    """Extract CSS custom property declarations from a CSS text block.

    Matches patterns like: ``--variable-name: value;``

    Parameters
    ----------
    css_text : str
        Raw CSS file contents.

    Returns
    -------
    list[tuple[str, str]]
        List of (property_name, value) tuples.
    """
    pattern = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
    results = []
    for match in pattern.finditer(css_text):
        name = match.group(1).strip()
        value = match.group(2).strip()
        results.append((name, value))
    return results


def _extract_media_queries(css_text: str) -> list[tuple[str, str]]:
    """Extract @media breakpoints from a CSS text block.

    Parameters
    ----------
    css_text : str
        Raw CSS file contents.

    Returns
    -------
    list[tuple[str, str]]
        List of (condition, raw_query_string) tuples.
        e.g. [('max-width', '1250px'), ...]
    """
    pattern = re.compile(r"@media\s*\(([^)]+)\)")
    results = []
    seen: set[str] = set()
    for match in pattern.finditer(css_text):
        query = match.group(1).strip()
        if query not in seen:
            seen.add(query)
            # Parse out property and value
            parts = query.split(":")
            if len(parts) == 2:
                prop = parts[0].strip()
                val = parts[1].strip()
                results.append((prop, val))
            else:
                results.append((query, ""))
    return results


def _infer_breakpoint_description(condition: str, value: str) -> str:
    """Infer a human-readable description for a breakpoint.

    Parameters
    ----------
    condition : str
        CSS media condition, e.g. 'max-width'.
    value : str
        Breakpoint value, e.g. '1250px'.

    Returns
    -------
    str
        Short description.
    """
    val_int = 0
    val_match = re.search(r"\d+", value)
    if val_match:
        val_int = int(val_match.group())

    if "max-width" in condition:
        if val_int >= 1200:
            return "Large desktop → tablet/desktop transition"
        elif val_int >= 900:
            return "Tablet landscape"
        elif val_int >= 700:
            return "Tablet portrait / large mobile"
        else:
            return "Mobile"
    elif "min-width" in condition:
        if val_int >= 1200:
            return "Large desktop"
        elif val_int >= 700:
            return "Tablet and up"
        else:
            return "Mobile and up"
    return "Custom breakpoint"


def generate(repo_root: Path) -> str:
    """Generate CSS-Design-System.md content block for the wiki.

    Reads WebContent/css/style.css and WebContent/css/mediaqueries.css to
    produce a custom properties table and a breakpoints reference table.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    css_dir = repo_root / "WebContent" / "css"
    style_path = css_dir / "style.css"
    media_path = css_dir / "mediaqueries.css"

    style_text = style_path.read_text(encoding="utf-8") if style_path.exists() else ""
    media_text = media_path.read_text(encoding="utf-8") if media_path.exists() else ""

    lines: list[str] = []

    # --- Custom properties ---
    custom_props = _extract_custom_properties(style_text)
    # Also check mediaqueries for any custom props
    media_props = _extract_custom_properties(media_text)
    all_props = custom_props + media_props

    lines.append("## CSS Custom Properties\n")
    if all_props:
        lines.append("| Property | Value |")
        lines.append("|---|---|")
        for name, value in all_props:
            lines.append(f"| `{name}` | `{value}` |")
    else:
        lines.append("_No CSS custom properties found._")
    lines.append("")

    # --- Media query breakpoints ---
    all_breakpoints: list[tuple[str, str]] = []
    # Check both files
    for text in [style_text, media_text]:
        bps = _extract_media_queries(text)
        for bp in bps:
            if bp not in all_breakpoints:
                all_breakpoints.append(bp)

    lines.append("## Breakpoints\n")
    if all_breakpoints:
        lines.append("| Condition | Value | Description |")
        lines.append("|---|---|---|")
        for condition, value in all_breakpoints:
            desc = _infer_breakpoint_description(condition, value)
            lines.append(f"| `{condition}` | `{value}` | {desc} |")
    else:
        lines.append("_No @media breakpoints found._")
    lines.append("")

    return "\n".join(lines)
