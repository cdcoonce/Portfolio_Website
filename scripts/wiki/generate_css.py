"""Generator for wiki/CSS-Design-System.md — design tokens and responsive breakpoints.

The styling layer lives in two files:

- ``src/styles/tokens.css`` — the design tokens (a small system ported from a Claude
  Design kit: Poppins type scale, a grayscale ramp + one pale-blue accent, pill
  geometry, spacing/radii/shadows). All are CSS custom properties on ``:root``.
- ``src/styles/global.css`` — every component style, BEM-ish and mobile-first, plus
  the ``@media`` breakpoints that scale the layout up.

This generator reads both files, groups the tokens by category, and lists the
breakpoints. It degrades gracefully if the files are missing.
"""

from __future__ import annotations

import re
from pathlib import Path


def _extract_custom_properties(css_text: str) -> list[tuple[str, str]]:
    """Extract ``--name: value;`` custom-property declarations, order-preserving."""
    pattern = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
    results = []
    seen: set[str] = set()
    for match in pattern.finditer(css_text):
        name = match.group(1).strip()
        value = match.group(2).strip()
        if name not in seen:
            seen.add(name)
            results.append((name, value))
    return results


def _extract_media_queries(css_text: str) -> list[tuple[str, str, str]]:
    """Extract ``@media`` breakpoints as (condition, value, raw) tuples.

    Deduplicated, order-preserving. ``raw`` is the full parenthesized query for
    features that aren't a simple ``property: value`` pair (e.g.
    ``prefers-reduced-motion: reduce``).
    """
    pattern = re.compile(r"@media\s*\(([^)]+)\)")
    results: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for match in pattern.finditer(css_text):
        query = match.group(1).strip()
        if query in seen:
            continue
        seen.add(query)
        parts = query.split(":", 1)
        if len(parts) == 2:
            results.append((parts[0].strip(), parts[1].strip(), query))
        else:
            results.append((query, "", query))
    return results


def _categorize_token(name: str) -> str:
    """Bucket a token into a design-system category by name prefix."""
    prefixes = [
        ("Color — grayscale", ("--white", "--gray", "--black")),
        ("Color — accent", ("--accent",)),
        ("Color — semantic", ("--text-", "--surface", "--border", "--quote")),
        ("Typography", ("--font", "--weight", "--text-", "--leading")),
        ("Spacing", ("--space",)),
        ("Radii", ("--radius",)),
        ("Shadow", ("--shadow",)),
        ("Motion", ("--transition",)),
        ("Layout", ("--container",)),
    ]
    # Typography reuses the --text- prefix for sizes; disambiguate size tokens
    # (values in rem / unitless) from semantic colors (values referencing colors).
    for label, keys in prefixes:
        for key in keys:
            if name.startswith(key):
                return label
    return "Other"


def _breakpoint_description(condition: str, value: str) -> str:
    """Human-readable description for a breakpoint, mobile-first aware."""
    val_match = re.search(r"\d+", value)
    val_int = int(val_match.group()) if val_match else 0

    if "prefers-reduced-motion" in condition:
        return "Accessibility — disable animations when motion is reduced"
    if "min-width" in condition:
        if val_int >= 800:
            return "Desktop — multi-column featured/experience layouts"
        if val_int >= 700:
            return "Tablet — centered tab bar, aligned profile"
        if val_int >= 600:
            return "Large mobile / small tablet — wider grids"
        return "Small screens and up"
    if "max-width" in condition:
        return "Down from this width"
    return "Custom breakpoint"


def generate(repo_root: Path) -> str:
    """Generate the CSS-Design-System.md content block for the wiki."""
    styles_dir = repo_root / "src" / "styles"
    tokens_path = styles_dir / "tokens.css"
    global_path = styles_dir / "global.css"

    tokens_text = tokens_path.read_text(encoding="utf-8") if tokens_path.exists() else ""
    global_text = global_path.read_text(encoding="utf-8") if global_path.exists() else ""

    lines: list[str] = []

    lines.append("## Design Tokens\n")
    lines.append(
        "The token layer (`src/styles/tokens.css`) is a small design system ported from a "
        "Claude Design kit: **Poppins** as the type family, a grayscale ramp plus a single "
        "pale-blue analytical accent, pill geometry, and consistent spacing / radii / shadow "
        "scales. Component styles in `src/styles/global.css` reference these variables rather "
        "than hard-coded values.\n"
    )

    tokens = _extract_custom_properties(tokens_text)
    if tokens:
        # Group by category, preserving first-seen category order.
        grouped: dict[str, list[tuple[str, str]]] = {}
        order: list[str] = []
        for name, value in tokens:
            cat = _categorize_token(name)
            if cat not in grouped:
                grouped[cat] = []
                order.append(cat)
            grouped[cat].append((name, value))

        for cat in order:
            lines.append(f"### {cat}\n")
            lines.append("| Token | Value |")
            lines.append("|---|---|")
            for name, value in grouped[cat]:
                lines.append(f"| `{name}` | `{value}` |")
            lines.append("")
    else:
        lines.append("_No design tokens found in `src/styles/tokens.css`._\n")

    # --- Breakpoints (from global.css, mobile-first) ---
    lines.append("## Breakpoints\n")
    lines.append(
        "`global.css` is **mobile-first**: base styles target small screens and `@media "
        "(min-width: …)` queries scale the layout up.\n"
    )
    breakpoints: list[tuple[str, str, str]] = []
    for text in (tokens_text, global_text):
        for bp in _extract_media_queries(text):
            if bp not in breakpoints:
                breakpoints.append(bp)

    if breakpoints:
        lines.append("| Condition | Value | Description |")
        lines.append("|---|---|---|")
        for condition, value, _raw in breakpoints:
            desc = _breakpoint_description(condition, value)
            value_str = f"`{value}`" if value else "—"
            lines.append(f"| `{condition}` | {value_str} | {desc} |")
        lines.append("")
    else:
        lines.append("_No `@media` breakpoints found._\n")

    return "\n".join(lines)
