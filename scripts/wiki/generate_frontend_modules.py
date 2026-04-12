"""Generator for wiki/Frontend-Modules.md — module inventory with exports."""

from __future__ import annotations

import re
from pathlib import Path


# Regex to match various ES module export forms:
#   export function foo(...)
#   export const foo = ...
#   export class Foo
#   export default function foo(...)
#   export default class Foo
_EXPORT_PATTERN = re.compile(
    r"^export\s+(?:default\s+)?(?:function\*?\s+|const\s+|class\s+|let\s+|var\s+)?(\w+)",
    re.MULTILINE,
)


def _extract_exports(js_text: str) -> list[str]:
    """Extract named exports from a JavaScript file.

    Handles: ``export function``, ``export const``, ``export class``,
    ``export default function/class``.

    Parameters
    ----------
    js_text : str
        Contents of a .js file.

    Returns
    -------
    list[str]
        List of exported names (deduplicated, preserving order).
    """
    names: list[str] = []
    seen: set[str] = set()
    for match in _EXPORT_PATTERN.finditer(js_text):
        name = match.group(1)
        # Skip keywords that can appear after 'export default'
        if name in {"function", "class", "const", "let", "var", "default"}:
            continue
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def _describe_module(filename: str, exports: list[str]) -> str:
    """Generate a short description for a module based on its name and exports.

    Parameters
    ----------
    filename : str
        The .js filename without path.
    exports : list[str]
        List of exported names.

    Returns
    -------
    str
        One-line description.
    """
    stem = Path(filename).stem.lower()
    descriptions = {
        "main": "Application entry point — wires up all modules on DOMContentLoaded",
        "filter": "Project card filtering logic and URL-based filter state",
        "chat": "Lambda-backed chat widget with rate limiting and XSS protection",
        "carousel": "Testimonials carousel with dot navigation and counter",
        "projects": "Project data array, tag registry, and tag label/category maps",
        "renderer": "DOM rendering for project cards and filter buttons",
        "utils": "Shared utility functions (viewport, date formatting, etc.)",
    }
    return descriptions.get(stem, f"{stem.title()} module")


def generate(repo_root: Path) -> str:
    """Generate Frontend-Modules.md content block for the wiki.

    Reads WebContent/js/*.js files, extracts exports, and produces a
    module inventory table. Includes a placeholder for the Phase 3 diagram.

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
    """
    js_dir = repo_root / "WebContent" / "js"
    lines: list[str] = []

    lines.append("<!-- Phase 3: module dependency graph will be inserted here -->\n")

    lines.append("## Module Inventory\n")

    if not js_dir.exists():
        lines.append("_No WebContent/js/ directory found._")
        return "\n".join(lines)

    js_files = sorted(js_dir.glob("*.js"))

    if not js_files:
        lines.append("_No .js files found in WebContent/js/._")
        return "\n".join(lines)

    lines.append("| Module | Exports | Description |")
    lines.append("|---|---|---|")

    for js_file in js_files:
        text = js_file.read_text(encoding="utf-8")
        exports = _extract_exports(text)
        exports_str = ", ".join(f"`{e}`" for e in exports) if exports else "—"
        desc = _describe_module(js_file.name, exports)
        lines.append(f"| `{js_file.name}` | {exports_str} | {desc} |")

    lines.append("")

    return "\n".join(lines)
