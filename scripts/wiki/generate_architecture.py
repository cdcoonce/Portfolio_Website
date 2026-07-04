"""Generator for wiki/Architecture.md — Astro + React islands system overview."""

from __future__ import annotations

from pathlib import Path


def generate(repo_root: Path) -> str:
    """Generate the Architecture.md content block for the wiki.

    Describes the Astro (static output) + React islands architecture, the tabbed
    single-page experience, the ``src/`` layout, the Ask-AI → Lambda data flow,
    and the hybrid deploy (GitHub Pages production + Cloudflare Pages staging).

    Parameters
    ----------
    repo_root : Path
        Absolute path to the repository root.

    Returns
    -------
    str
        Markdown string suitable for insertion into the generated block.
        Does NOT include the marker comments — the orchestrator wraps it.
    """
    lines: list[str] = []

    lines.append("## System Architecture\n")
    lines.append(
        "The portfolio is an **Astro** app built with **static output** — every page is "
        "pre-rendered to plain HTML at build time (`npm run build` → `dist/`). Interactivity "
        "ships as **React islands** via `@astrojs/react`, so JavaScript is hydrated only where "
        "it's needed. The entire interactive UI is a single island: `src/pages/index.astro` "
        "mounts `<Portfolio client:load />`, a tabbed **single-page experience** that hydrates "
        "in the **browser** and swaps between the Overview, Work, Experience, Testimonials, Ask "
        "AI, and Contact sections with React state (no router, no page reloads). The **Ask AI** "
        "tab calls an AWS Lambda "
        "function that proxies to the Anthropic Claude API.\n"
    )

    # --- System component diagram ---
    lines.append("### System Components\n")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append('    Astro["Astro build\\n(static output → dist/)"]')
    lines.append('    Base["Base.astro layout\\n(head · SEO · GA · fonts)"]')
    lines.append('    IndexPage["index.astro\\n(<Portfolio client:load />)"]')
    lines.append('    Portfolio["Portfolio.jsx island\\n(profile · tab bar · routing)"]')
    lines.append('    Tabs["Tab sections\\n(Overview · Work · Experience · Testimonials · AskAI · Contact)"]')
    lines.append('    Lib["src/lib + src/data\\n(carousel · chat · portfolio)"]')
    lines.append('    Lambda["AWS Lambda\\n(lambda_function.py)"]')
    lines.append('    AnthropicAPI["Anthropic API\\n(Claude Haiku)"]')
    lines.append("")
    lines.append("    Astro -->|renders| Base")
    lines.append("    Base -->|slots| IndexPage")
    lines.append("    IndexPage -->|hydrates| Portfolio")
    lines.append("    Portfolio -->|routes to| Tabs")
    lines.append("    Tabs -->|import| Lib")
    lines.append("    Tabs -->|Ask AI: POST /chat| Lambda")
    lines.append("    Lambda -->|messages.create| AnthropicAPI")
    lines.append("    AnthropicAPI -->|assistant text| Lambda")
    lines.append("    Lambda -->|JSON response| Tabs")
    lines.append("```\n")

    # --- Ask-AI data flow diagram ---
    lines.append("### Ask AI Data Flow\n")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append('    UserInput["User types question"]')
    lines.append('    RateCheck["isRateLimited()\\n(localStorage, 25/hour)"]')
    lines.append('    ChatLib["src/lib/chat.js\\nsendMessage({messages})"]')
    lines.append('    LambdaHandler["Lambda handler()\\nparse + validate body"]')
    lines.append('    ChatAgent["ChatAgent.reply()\\nbuild prompt + call API"]')
    lines.append('    AnthropicResponse["Anthropic Claude\\nHaiku response"]')
    lines.append('    RenderReply["renderAssistantMarkdown()\\n→ chat panel"]')
    lines.append("")
    lines.append("    UserInput --> RateCheck")
    lines.append("    RateCheck -->|within limit| ChatLib")
    lines.append("    RateCheck -->|exceeded| RenderReply")
    lines.append("    ChatLib -->|POST JSON| LambdaHandler")
    lines.append("    LambdaHandler --> ChatAgent")
    lines.append("    ChatAgent --> AnthropicResponse")
    lines.append("    AnthropicResponse --> ChatAgent")
    lines.append("    ChatAgent -->|response text| LambdaHandler")
    lines.append("    LambdaHandler -->|200 JSON| ChatLib")
    lines.append("    ChatLib --> RenderReply")
    lines.append("```\n")

    # --- src/ layout ---
    lines.append("## Source Layout\n")
    lines.append("| Path | Contents |")
    lines.append("|---|---|")
    lines.append("| `src/pages/` | Astro pages — `index.astro` (home), `404.astro` |")
    lines.append("| `src/layouts/` | `Base.astro` — `<head>`, SEO/Open Graph, Google Analytics, fonts |")
    lines.append("| `src/components/` | React islands — `Portfolio.jsx`, `Button.jsx`, `Tag.jsx`, `ProjectCard.jsx` |")
    lines.append("| `src/components/tabs/` | Tab sections — `Overview`, `Work`, `Experience`, `Testimonials`, `AskAI`, `Contact` |")
    lines.append("| `src/lib/` | Framework-free logic — `carousel.js` (index math), `chat.js` (Lambda client + rate limiting) |")
    lines.append("| `src/data/` | `portfolio.js` — projects, skills, metrics, experience, testimonials, navItems |")
    lines.append("| `src/styles/` | `tokens.css` (design tokens) + `global.css` (component styles) |")
    lines.append("| `lambda/` | AWS Lambda chat backend (unchanged) |")
    lines.append("")

    # --- Deploy model ---
    lines.append("## Deploy Model\n")
    lines.append(
        "Two branches, two hosts. `dev` is **live staging**; `main` is **production**. Each "
        "push builds the Astro site and publishes the `dist/` output to a different host.\n"
    )
    lines.append("| Branch | Trigger | Host | URL |")
    lines.append("|---|---|---|---|")
    lines.append("| `main` | push (after lint + test + build) | GitHub Pages (`gh-pages` branch) | charleslikesdata.com |")
    lines.append("| `dev` | push | Cloudflare Pages (`charleslikesdata-portfolio`) | charleslikesdata-portfolio.pages.dev |")
    lines.append("")
    lines.append(
        "Promotion flows `dev → main`: work lands on `dev` (auto-deployed to staging), then "
        "merges to `main` for production. See the CI/CD Pipeline page for the workflow details.\n"
    )

    return "\n".join(lines)
