"""Generator for wiki/Lambda-Chat-Agent.md — sequence and class diagrams."""

from __future__ import annotations

import re
from pathlib import Path


def _extract_classes(lambda_text: str) -> list[tuple[str, list[str], list[str]]]:
    """Extract class names, attributes, and methods from lambda_function.py.

    Parameters
    ----------
    lambda_text : str
        Contents of lambda_function.py.

    Returns
    -------
    list[tuple[str, list[str], list[str]]]
        Each entry is (class_name, attributes, methods).
    """
    results = []
    # Find class definitions
    class_pattern = re.compile(r"^class (\w+)", re.MULTILINE)
    for match in class_pattern.finditer(lambda_text):
        class_name = match.group(1)
        # Find method definitions within the class (rough approximation)
        # Look for def statements indented with 4 spaces after this class
        start = match.start()
        # Find next class or end of text
        next_class = class_pattern.search(lambda_text, match.end())
        end = next_class.start() if next_class else len(lambda_text)
        class_body = lambda_text[start:end]

        methods = re.findall(r"    def (\w+)\(", class_body)
        # Extract instance variable assignments from __init__
        attrs = re.findall(r"self\.(\w+)\s*=", class_body)
        # Deduplicate preserving order
        seen_m: set[str] = set()
        unique_methods = [m for m in methods if not (m in seen_m or seen_m.add(m))]  # type: ignore[func-returns-value]
        seen_a: set[str] = set()
        unique_attrs = [a for a in attrs if not (a in seen_a or seen_a.add(a))]  # type: ignore[func-returns-value]

        results.append((class_name, unique_attrs, unique_methods))
    return results


def _extract_requirements(req_path: Path) -> list[str]:
    """Extract package names from requirements.txt.

    Parameters
    ----------
    req_path : Path
        Path to requirements.txt.

    Returns
    -------
    list[str]
        List of package names.
    """
    if not req_path.exists():
        return []
    lines = req_path.read_text(encoding="utf-8").splitlines()
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # Strip version specifiers
            name = re.split(r"[><=!;]", line)[0].strip()
            if name:
                packages.append(name)
    return packages


def generate(repo_root: Path) -> str:
    """Generate Lambda-Chat-Agent.md content block for the wiki.

    Reads lambda/lambda_function.py and lambda/requirements.txt, then
    produces a chat request sequence diagram and a class diagram showing
    ChatAgent and ChatRequest.

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
    lambda_path = repo_root / "lambda" / "lambda_function.py"
    req_path = repo_root / "lambda" / "requirements.txt"

    lambda_text = lambda_path.read_text(encoding="utf-8") if lambda_path.exists() else ""
    requirements = _extract_requirements(req_path)

    lines: list[str] = []

    lines.append("## Lambda Chat Agent\n")
    lines.append(
        "The portfolio chat widget is powered by an AWS Lambda function that "
        "receives POST requests from the browser, validates the message, builds a "
        "system prompt from the knowledge base, and proxies the conversation to the "
        "Anthropic Claude Haiku model.\n"
    )

    # --- Sequence diagram ---
    lines.append("### Chat Request Sequence\n")
    lines.append("```mermaid")
    lines.append("sequenceDiagram")
    lines.append("    participant User")
    lines.append("    participant Browser")
    lines.append("    participant Lambda")
    lines.append("    participant Anthropic")
    lines.append("")
    lines.append("    User->>Browser: types message")
    lines.append("    Browser->>Browser: rate limit check")
    lines.append("    Browser->>Lambda: POST {messages: [...]}")
    lines.append("    Lambda->>Lambda: ChatRequest.from_body()")
    lines.append("    Lambda->>Lambda: build_system_prompt()")
    lines.append("    Lambda->>Anthropic: messages.create(model, system, messages)")
    lines.append("    Anthropic-->>Lambda: assistant text block")
    lines.append("    Lambda-->>Browser: 200 {response: text}")
    lines.append("    Browser-->>User: renders assistant reply")
    lines.append("```\n")

    # --- Class diagram ---
    lines.append("### Class Diagram\n")
    lines.append("```mermaid")
    lines.append("classDiagram")

    if lambda_text:
        classes = _extract_classes(lambda_text)
        # Only include ChatAgent and ChatRequest for clarity
        target_classes = {"ChatAgent", "ChatRequest"}
        for class_name, attrs, methods in classes:
            if class_name not in target_classes:
                continue
            lines.append(f"    class {class_name} {{")
            for attr in attrs:
                lines.append(f"        +{attr}")
            for method in methods:
                lines.append(f"        +{method}()")
            lines.append("    }")
        # Add relationship
        lines.append("    ChatAgent ..> ChatRequest : uses")
    else:
        # Fallback static diagram
        lines.append("    class ChatAgent {")
        lines.append("        +client")
        lines.append("        +system_prompt")
        lines.append("        +model")
        lines.append("        +max_tokens")
        lines.append("        +reply()")
        lines.append("    }")
        lines.append("    class ChatRequest {")
        lines.append("        +messages")
        lines.append("        +from_body()")
        lines.append("    }")
        lines.append("    ChatAgent ..> ChatRequest : uses")

    lines.append("```\n")

    # --- Dependencies section ---
    lines.append("## Dependencies\n")
    lines.append("| Package | Source |")
    lines.append("|---|---|")
    if requirements:
        for pkg in requirements:
            lines.append(f"| `{pkg}` | `lambda/requirements.txt` |")
    else:
        lines.append("| _(none found)_ | — |")
    lines.append("")

    # --- Configuration ---
    lines.append("## Configuration\n")
    lines.append("| Constant | Value |")
    lines.append("|---|---|")

    if lambda_text:
        # Extract constants
        model_match = re.search(r'MODEL_ID\s*=\s*"([^"]+)"', lambda_text)
        max_tokens_match = re.search(r"MAX_TOKENS\s*=\s*(\d+)", lambda_text)
        max_msg_match = re.search(r"MAX_MESSAGE_LENGTH\s*=\s*(\d+)", lambda_text)

        model_id = model_match.group(1) if model_match else "unknown"
        max_tokens = max_tokens_match.group(1) if max_tokens_match else "unknown"
        max_msg = max_msg_match.group(1) if max_msg_match else "unknown"

        lines.append(f"| `MODEL_ID` | `{model_id}` |")
        lines.append(f"| `MAX_TOKENS` | `{max_tokens}` |")
        lines.append(f"| `MAX_MESSAGE_LENGTH` | `{max_msg}` |")
    else:
        lines.append("| _(lambda_function.py not found)_ | — |")

    lines.append("")

    return "\n".join(lines)
