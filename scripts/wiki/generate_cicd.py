"""Generator for wiki/CI-CD-Pipeline.md — hybrid deploy pipeline and branch model.

Two workflows drive delivery:

- ``.github/workflows/ci-cd.yml`` — on push/PR to ``main``: lint + Jest + Astro build;
  on push to ``main`` it publishes ``dist/`` to the ``gh-pages`` branch (production
  GitHub Pages → charleslikesdata.com).
- ``.github/workflows/deploy-staging.yml`` — on push to ``dev``: build + deploy ``dist/``
  to the Cloudflare Pages project ``charleslikesdata-portfolio`` (staging).

So ``dev`` is live staging and ``main`` is production, with a ``dev → main`` promotion.
"""

from __future__ import annotations

from pathlib import Path


def _workflow_exists(repo_root: Path, name: str) -> bool:
    return (repo_root / ".github" / "workflows" / name).exists()


def generate(repo_root: Path) -> str:
    """Generate the CI-CD-Pipeline.md content block for the wiki."""
    lines: list[str] = []

    lines.append("## CI/CD Pipeline\n")
    lines.append(
        "Delivery runs on GitHub Actions across **two branches, two hosts**. `dev` is **live "
        "staging** (Cloudflare Pages); `main` is **production** (GitHub Pages). Both build the "
        "Astro site (`npm run build` → `dist/`) and publish that output — the only difference "
        "is the host and the quality gate in front of it.\n"
    )

    # --- Production pipeline flowchart (ci-cd.yml) ---
    lines.append("### Production Pipeline (`main` → GitHub Pages)\n")
    lines.append(
        "`ci-cd.yml` runs on every push and pull request targeting `main`. The **check** job "
        "must pass before the **deploy** job publishes to the `gh-pages` branch (including "
        "`CNAME`), which GitHub Pages serves.\n"
    )
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append('    Push["Push / PR to main"]')
    lines.append('    Checkout["Checkout code"]')
    lines.append('    NodeSetup["Set up Node.js 22\\n+ npm ci"]')
    lines.append('    Prettier["Check formatting\\n(Prettier)"]')
    lines.append('    LintCSS["Lint CSS\\n(Stylelint)"]')
    lines.append('    LintJS["Lint JS\\n(ESLint)"]')
    lines.append('    JSTests["JS unit tests\\n(Jest)"]')
    lines.append('    Build["Build site\\n(astro build → dist/)"]')
    lines.append('    Check{"push to main?"}')
    lines.append('    Deploy["Publish dist/ → gh-pages\\n(peaceiris/actions-gh-pages)"]')
    lines.append('    Done["Live on GitHub Pages\\n(charleslikesdata.com)"]')
    lines.append('    PR["PR: checks only, no deploy"]')
    lines.append("")
    lines.append("    Push --> Checkout --> NodeSetup --> Prettier --> LintCSS --> LintJS --> JSTests --> Build --> Check")
    lines.append("    Check -->|yes| Deploy --> Done")
    lines.append("    Check -->|pull_request| PR")
    lines.append("```\n")

    # --- Staging pipeline (deploy-staging.yml) ---
    lines.append("### Staging Pipeline (`dev` → Cloudflare Pages)\n")
    lines.append(
        "`deploy-staging.yml` runs on every push to `dev`. It builds the Astro site and "
        "deploys `dist/` to the Cloudflare Pages project `charleslikesdata-portfolio` via "
        "`wrangler`. The deploy self-skips until the `CLOUDFLARE_API_TOKEN` and "
        "`CLOUDFLARE_ACCOUNT_ID` repo secrets are set, so early pushes don't fail red.\n"
    )
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append('    DevPush["Push to dev"]')
    lines.append('    DevBuild["npm ci + astro build"]')
    lines.append('    SecretCheck{"Cloudflare secrets set?"}')
    lines.append('    Wrangler["wrangler pages deploy dist\\n--project charleslikesdata-portfolio"]')
    lines.append('    Staging["Live staging\\n(charleslikesdata-portfolio.pages.dev)"]')
    lines.append('    Skip["Skip deploy (log + exit 0)"]')
    lines.append("")
    lines.append("    DevPush --> DevBuild --> SecretCheck")
    lines.append("    SecretCheck -->|yes| Wrangler --> Staging")
    lines.append("    SecretCheck -->|no| Skip")
    lines.append("```\n")

    # --- Branch / promotion model ---
    lines.append("### Branch & Promotion Model\n")
    lines.append(
        "Feature work lands on `dev`, which auto-deploys to staging. Once verified, `dev` "
        "merges to `main`, which runs the full gate and promotes to production.\n"
    )
    lines.append("```mermaid")
    lines.append("gitGraph")
    lines.append('    commit id: "init"')
    lines.append("    branch dev")
    lines.append("    checkout dev")
    lines.append('    commit id: "feat: work (→ staging)"')
    lines.append('    commit id: "fix: review (→ staging)"')
    lines.append("    checkout main")
    lines.append('    merge dev id: "promote (→ production)"')
    lines.append("```\n")

    # --- Trigger matrix ---
    lines.append("## Trigger Matrix\n")
    lines.append("| Event | Branch | Workflow | Result |")
    lines.append("|---|---|---|---|")
    lines.append("| `push` | `main` | `ci-cd.yml` | Lint + Test + Build, then deploy to GitHub Pages |")
    lines.append("| `pull_request` | `main` | `ci-cd.yml` | Lint + Test + Build only (no deploy) |")
    lines.append("| `push` | `dev` | `deploy-staging.yml` | Build + deploy to Cloudflare Pages (staging) |")
    lines.append("")

    # --- Workflow files ---
    lines.append("## Workflow Files\n")
    lines.append("| File | Trigger | Purpose |")
    lines.append("|---|---|---|")
    if _workflow_exists(repo_root, "ci-cd.yml"):
        lines.append("| `.github/workflows/ci-cd.yml` | push / PR → `main` | Lint, test, build; deploy production to `gh-pages` |")
    if _workflow_exists(repo_root, "deploy-staging.yml"):
        lines.append("| `.github/workflows/deploy-staging.yml` | push → `dev` | Build + deploy staging to Cloudflare Pages |")
    if _workflow_exists(repo_root, "wiki-sync.yml"):
        lines.append("| `.github/workflows/wiki-sync.yml` | push → `main` (relevant paths) | Regenerate and sync this wiki |")
    lines.append("")

    return "\n".join(lines)
