"""Generator for wiki/Architecture.md — system component and data flow diagrams."""

from __future__ import annotations

from pathlib import Path


def generate(repo_root: Path) -> str:
    """Generate Architecture.md content block for the wiki.

    Produces two Mermaid diagrams: a system component diagram showing the
    high-level architecture, and a data flow diagram showing a chat request
    lifecycle.

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
        "The portfolio is a static site served from GitHub Pages. "
        "Interactive features (filtering, carousel, chat) run in the browser via ES modules. "
        "The chat widget communicates with an AWS Lambda function that proxies requests to "
        "the Anthropic Claude API.\n"
    )

    # --- System component diagram ---
    lines.append("### System Components\n")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append('    Browser["Browser (GitHub Pages)"]')
    lines.append('    JSModules["JS Modules\\n(main · filter · chat · renderer · carousel · projects · utils)"]')
    lines.append('    Lambda["AWS Lambda\\n(lambda_function.py)"]')
    lines.append('    AnthropicAPI["Anthropic API\\n(Claude Haiku)"]')
    lines.append('    KnowledgeBase["knowledge_base.json\\n(portfolio context)"]')
    lines.append("")
    lines.append("    Browser -->|loads| JSModules")
    lines.append("    JSModules -->|POST /chat| Lambda")
    lines.append("    Lambda -->|reads| KnowledgeBase")
    lines.append("    Lambda -->|messages.create| AnthropicAPI")
    lines.append("    AnthropicAPI -->|assistant text| Lambda")
    lines.append("    Lambda -->|JSON response| JSModules")
    lines.append("    JSModules -->|renders reply| Browser")
    lines.append("```\n")

    # --- Data flow diagram ---
    lines.append("### Chat Data Flow\n")
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append('    UserInput["User types message"]')
    lines.append('    RateCheck["Rate limit check\\n(localStorage)"]')
    lines.append('    ChatModule["chat.js\\nsendMessage()"]')
    lines.append('    LambdaHandler["Lambda handler()\\nparse + validate body"]')
    lines.append('    ChatAgent["ChatAgent.reply()\\nbuild prompt + call API"]')
    lines.append('    AnthropicResponse["Anthropic Claude\\nHaiku response"]')
    lines.append('    RenderReply["Render assistant reply\\nto chat UI"]')
    lines.append("")
    lines.append("    UserInput --> RateCheck")
    lines.append("    RateCheck -->|within limit| ChatModule")
    lines.append("    RateCheck -->|exceeded| RenderReply")
    lines.append("    ChatModule -->|POST JSON| LambdaHandler")
    lines.append("    LambdaHandler --> ChatAgent")
    lines.append("    ChatAgent --> AnthropicResponse")
    lines.append("    AnthropicResponse --> ChatAgent")
    lines.append("    ChatAgent -->|response text| LambdaHandler")
    lines.append("    LambdaHandler -->|200 JSON| ChatModule")
    lines.append("    ChatModule --> RenderReply")
    lines.append("```\n")

    # --- Key files section ---
    lines.append("## Key Files\n")
    lines.append("| File | Role |")
    lines.append("|---|---|")
    lines.append("| `WebContent/js/main.js` | Application entry point — wires all modules |")
    lines.append("| `WebContent/js/chat.js` | Chat widget — rate limiting, XSS protection, Lambda calls |")
    lines.append("| `lambda/lambda_function.py` | AWS Lambda handler — ChatAgent, ChatRequest |")
    lines.append("| `lambda/knowledge_base.json` | Portfolio context for the LLM system prompt |")
    lines.append("| `index.html` | Main page — chat widget, projects, testimonials |")
    lines.append("| `projects.html` | Full projects listing |")
    lines.append("")

    return "\n".join(lines)
