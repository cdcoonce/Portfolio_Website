"""Generator for wiki/Frontend-Modules.md — Astro pages/layout + React island inventory.

The site is an Astro (static output) app with React islands. This generator reads
the real files under ``src/`` to enumerate:

- Astro pages (``src/pages/*.astro``) and layouts (``src/layouts/*.astro``)
- React components (``src/components/*.jsx``) and tab sections (``src/components/tabs/*.jsx``)
- Plain-JS logic/data modules (``src/lib/*.js`` and ``src/data/*.js``)

and produces a component tree (Mermaid ``graph TD``) plus inventory tables.
"""

from __future__ import annotations

import re
from pathlib import Path

# Matches ES module default export of a React component:
#   export default function Foo(...)
_DEFAULT_EXPORT_PATTERN = re.compile(
    r"^export\s+default\s+function\s+(\w+)",
    re.MULTILINE,
)

# Matches named ES module exports:
#   export function foo(...) / export const foo = / export class Foo
_NAMED_EXPORT_PATTERN = re.compile(
    r"^export\s+(?:async\s+)?(?:function\*?\s+|const\s+|class\s+|let\s+|var\s+)(\w+)",
    re.MULTILINE,
)

# Matches local component/module imports:
#   import Foo from './Foo.jsx'
#   import { bar } from '../lib/carousel.js'
_LOCAL_IMPORT_PATTERN = re.compile(
    r"^import\s+.*?\s+from\s+['\"](\.[^'\"]+\.(?:jsx?|js))['\"]",
    re.MULTILINE,
)

# React hooks referenced in a component.
_HOOKS = ("useState", "useEffect", "useRef", "useMemo", "useCallback", "useReducer")


def _extract_named_exports(text: str) -> list[str]:
    """Return named ES exports from a JS/JSX file, order-preserving and deduped."""
    names: list[str] = []
    seen: set[str] = set()
    for match in _NAMED_EXPORT_PATTERN.finditer(text):
        name = match.group(1)
        if name in {"function", "class", "const", "let", "var", "default"}:
            continue
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def _extract_default_export(text: str) -> str | None:
    """Return the default-exported component name, if any."""
    match = _DEFAULT_EXPORT_PATTERN.search(text)
    return match.group(1) if match else None


def _extract_local_imports(text: str) -> list[str]:
    """Return local import target stems (e.g. 'Button', 'carousel')."""
    stems: list[str] = []
    for spec in _LOCAL_IMPORT_PATTERN.findall(text):
        stems.append(Path(spec).stem)
    return stems


def _extract_hooks(text: str) -> list[str]:
    """Return the React hooks used in a component, in canonical order."""
    return [hook for hook in _HOOKS if re.search(rf"\b{hook}\b", text)]


def _rel(path: Path, repo_root: Path) -> str:
    """Return a POSIX-style path relative to the repo root."""
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.name


# One-line descriptions keyed by component/module stem. Falls back to a generic
# label so new files never crash the generator.
_DESCRIPTIONS = {
    # Root island + primitives
    "Portfolio": "Root island — profile header, sticky tab bar, tab routing, footer",
    "Button": "Pill button primitive — `primary`/`ghost` variants, renders `<a>` or `<button>`",
    "Tag": "Small pill tag used for skills and project technologies",
    "ProjectCard": "Project card — image, date, title, description, tag row; links out",
    # Tab sections
    "Overview": "Overview tab — at-a-glance metrics grid + featured project spotlight",
    "Work": "Work tab — responsive grid of project cards",
    "Experience": "Experience tab — role timeline + categorized skills/tools tags",
    "Testimonials": "Testimonials tab — single-quote carousel with dots and arrows",
    "AskAI": "Ask AI tab — chat panel wired to the live Lambda assistant (rate limited)",
    "Contact": "Contact tab — prompt text + Email/LinkedIn/GitHub action buttons",
    # Logic / data
    "carousel": "Pure index math for wrap-around carousels (unit-tested)",
    "chat": "Ask-AI Lambda client — rate limiting, markdown rendering, `sendMessage`",
    "portfolio": "Site data — projects, skills, metrics, experience, testimonials, navItems",
}


def _describe(stem: str) -> str:
    return _DESCRIPTIONS.get(stem, f"`{stem}` module")


def _component_tree(components: list[dict]) -> str:
    """Build a Mermaid ``graph TD`` of the React component/island tree.

    Parameters
    ----------
    components : list[dict]
        Each dict has keys 'name' (default export), 'stem', 'imports'
        (list of local import stems).
    """
    by_name = {c["name"]: c for c in components if c["name"]}
    if not by_name:
        return ""

    lines = ["```mermaid", "graph TD"]
    lines.append('    IndexAstro["src/pages/index.astro"]')
    lines.append('    Portfolio["Portfolio.jsx (client:load island)"]')
    lines.append("    IndexAstro -->|client:load| Portfolio")

    # Edges from each component to its imported local components.
    emitted: set[tuple[str, str]] = set()
    for comp in components:
        name = comp["name"]
        if not name:
            continue
        for imported_stem in comp["imports"]:
            target = by_name.get(_stem_to_component_name(imported_stem, by_name))
            if target and (name, target["name"]) not in emitted:
                lines.append(f"    {name} --> {target['name']}")
                emitted.add((name, target["name"]))
    lines.append("```")
    return "\n".join(lines)


def _stem_to_component_name(stem: str, by_name: dict) -> str:
    """Map an import stem to a known component name (stems usually match names)."""
    if stem in by_name:
        return stem
    # Import stems for components equal their default-export name in this codebase.
    for name in by_name:
        if name == stem:
            return name
    return stem


def _read_files(directory: Path, pattern: str) -> list[Path]:
    return sorted(directory.glob(pattern)) if directory.exists() else []


def generate(repo_root: Path) -> str:
    """Generate the Frontend-Modules.md content block for the wiki."""
    src = repo_root / "src"
    lines: list[str] = []

    if not src.exists():
        return "_No `src/` directory found._"

    # --- Collect React components (root + tabs) ---
    component_files = _read_files(src / "components", "*.jsx")
    tab_files = _read_files(src / "components" / "tabs", "*.jsx")

    components: list[dict] = []
    for path in [*component_files, *tab_files]:
        text = path.read_text(encoding="utf-8")
        components.append(
            {
                "path": path,
                "stem": path.stem,
                "name": _extract_default_export(text),
                "imports": _extract_local_imports(text),
                "hooks": _extract_hooks(text),
            }
        )

    # --- Hydration / islands overview ---
    lines.append("## Astro + React Islands\n")
    lines.append(
        "The site is an [Astro](https://astro.build) app with **static output**. Astro "
        "renders pages to plain HTML at build time; interactivity is delivered as **React "
        "islands** — components that ship JS only where they're used. The whole app is a "
        "single client-side island: `src/pages/index.astro` mounts `<Portfolio client:load />`, "
        "so the `Portfolio` component (and everything it renders) hydrates in the browser on "
        "load. `src/pages/404.astro` is fully static apart from a `<Button>` link.\n"
    )
    lines.append("| Directive | Meaning | Used by |")
    lines.append("|---|---|---|")
    lines.append("| `client:load` | Hydrate the island immediately on page load | `Portfolio` (root island) |")
    lines.append("")

    # --- Component tree ---
    lines.append("## Component Tree\n")
    tree = _component_tree(components)
    if tree:
        lines.append(tree)
    lines.append("")

    # --- Astro pages & layouts ---
    page_files = _read_files(src / "pages", "*.astro")
    layout_files = _read_files(src / "layouts", "*.astro")
    lines.append("## Astro Pages & Layouts\n")
    lines.append("| File | Role |")
    lines.append("|---|---|")
    for path in [*page_files, *layout_files]:
        rel = _rel(path, repo_root)
        if path.parent.name == "layouts":
            role = "Layout — `<head>`, SEO/Open Graph, Google Analytics, fonts, `<slot />`"
        elif path.stem == "index":
            role = "Home page — renders `<Portfolio client:load />` inside `Base`"
        elif path.stem == "404":
            role = "404 page — static not-found view with a back-home `<Button>`"
        else:
            role = "Astro page"
        lines.append(f"| `{rel}` | {role} |")
    lines.append("")

    # --- React component inventory ---
    lines.append("## React Components\n")
    lines.append("| Component | File | Imports | Hooks | Description |")
    lines.append("|---|---|---|---|---|")
    for comp in components:
        name = comp["name"] or "—"
        rel = _rel(comp["path"], repo_root)
        imports = ", ".join(f"`{s}`" for s in comp["imports"]) if comp["imports"] else "—"
        hooks = ", ".join(f"`{h}`" for h in comp["hooks"]) if comp["hooks"] else "—"
        desc = _describe(comp["stem"])
        lines.append(f"| `{name}` | `{rel}` | {imports} | {hooks} | {desc} |")
    lines.append("")

    # --- Logic & data modules (plain JS, unit-testable) ---
    lib_files = _read_files(src / "lib", "*.js")
    data_files = _read_files(src / "data", "*.js")
    lines.append("## Logic & Data Modules\n")
    lines.append(
        "Framework-free JavaScript under `src/lib/` and `src/data/`. The `lib` modules are "
        "pure enough to unit-test directly with Jest (see the Testing page).\n"
    )
    lines.append("| Module | Exports | Description |")
    lines.append("|---|---|---|")
    for path in [*lib_files, *data_files]:
        text = path.read_text(encoding="utf-8")
        exports = _extract_named_exports(text)
        exports_str = ", ".join(f"`{e}`" for e in exports) if exports else "—"
        rel = _rel(path, repo_root)
        lines.append(f"| `{rel}` | {exports_str} | {_describe(path.stem)} |")
    lines.append("")

    return "\n".join(lines)
