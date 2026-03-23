"""AWS Lambda handler for the portfolio chat agent.

Receives user messages via POST, sends them to Claude Haiku with
portfolio context, and returns the response.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import anthropic

MAX_MESSAGE_LENGTH = 1000
MODEL_ID = "claude-haiku-4-5-20251001"
MAX_TOKENS = 512
ALLOWED_ORIGIN = "https://charleslikesdata.com"

_knowledge_base: dict | None = None


def load_knowledge_base() -> dict:
    """Load the portfolio knowledge base from the bundled JSON file."""
    global _knowledge_base
    if _knowledge_base is None:
        kb_path = Path(__file__).parent / "knowledge_base.json"
        _knowledge_base = json.loads(kb_path.read_text())
    return _knowledge_base


def build_system_prompt() -> str:
    """Construct the system prompt from the knowledge base."""
    kb = load_knowledge_base()
    person = kb["person"]
    skills = kb["skills"]
    projects = kb["projects"]
    testimonials = kb["testimonials"]

    # Build skill summaries
    skill_lines = []
    for s in skills:
        tools = ", ".join(s.get("tools", []))
        skill_lines.append(f"- {s['category']}: {tools}")

    # Build project summaries
    project_lines = []
    for i, p in enumerate(projects, 1):
        featured = " [FEATURED]" if p.get("featured") else ""
        techs = "; ".join(p.get("technologies", []))
        date = f" ({p['date']})" if p.get("date") else ""
        key_results = p.get("key_results", "")
        key_results_block = (
            f"\n   Key Results:\n{chr(10).join('     ' + ln for ln in key_results.splitlines())}"
            if key_results
            else ""
        )
        entry = (
            f"{i}. {p['title']}{featured}{date}\n"
            f"   Type: {p.get('type', '')}\n"
            f"   Summary: {p.get('summary', '')}"
            f"{key_results_block}\n"
            f"   Technologies: {techs}\n"
            f"   URL: {p.get('url', '')}"
        )
        project_lines.append(entry)

    # Build testimonial summaries
    testimonial_lines = []
    for t in testimonials:
        testimonial_lines.append(
            f'- "{t["quote"]}" -- {t["author"]}, {t["title"]}, {t["company"]}'
        )

    return (
        f"You are a helpful assistant on the portfolio website of {person['name']}, "
        f"who is a {person['title']}. You answer questions about Charles, his projects, "
        f"skills, and experience in a friendly, professional, and concise tone.\n\n"
        f"## About {person['name']}\n"
        f"{person['bio']}\n\n"
        f"## Career Journey\n"
        f"{person.get('career_journey', '')}\n\n"
        f"## Education\n"
        f"{person.get('education', '')}\n\n"
        f"## What Sets Charles Apart\n"
        f"{person.get('what_sets_apart', '')}\n\n"
        f"## Contact\n"
        f"- Email: {person.get('email', '')}\n"
        f"- LinkedIn: {person.get('linkedin', '')}\n"
        f"- GitHub: {person.get('github', '')}\n"
        f"- Website: {person.get('website', '')}\n\n"
        f"## Skills ({len(skills)} categories)\n"
        + "\n".join(skill_lines)
        + "\n\n"
        f"## Projects ({len(projects)} total)\n"
        + "\n".join(project_lines)
        + "\n\n"
        f"## Testimonials from Colleagues\n"
        + "\n".join(testimonial_lines)
        + "\n\n"
        "## Instructions\n"
        "- CRITICAL: This is a multi-turn conversation. When the user says 'the last one', "
        "'that project', 'the first one', or any relative reference, ALWAYS resolve it from "
        "your previous messages in the conversation — never from the numbered project list above. "
        "The conversation history is the ground truth for what was 'mentioned' or 'listed'.\n"
        "- Answer questions about Charles's projects, skills, background, and experience.\n"
        "- When referencing a project, include its URL so the user can explore further.\n"
        "- If the user asks something outside the scope of this portfolio, politely redirect.\n"
        "- IMPORTANT: Keep responses concise — 2-3 sentences maximum unless the user explicitly asks for detail. Never list all skills or projects unprompted.\n"
        "- Be friendly and professional.\n"
        "- Do not make up information that is not in the knowledge base above.\n"
    )


def get_anthropic_client() -> anthropic.Anthropic:
    """Create an Anthropic client using the ANTHROPIC_API_KEY env var."""
    return anthropic.Anthropic()


def parse_request(body: str | None) -> list[dict[str, str]]:
    """Parse and validate the incoming request body.

    Parameters
    ----------
    body : str | None
        Raw JSON string from the request body.

    Returns
    -------
    list[dict[str, str]]
        Validated conversation messages for the Anthropic API.

    Raises
    ------
    ValueError
        If the body is missing, not valid JSON, or messages are invalid.
    """
    if not body:
        raise ValueError("Request body is empty")
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON in request body") from exc

    # Support both single message and conversation history
    if "messages" in data:
        messages = data["messages"]
        if not isinstance(messages, list) or not messages:
            raise ValueError("Messages must be a non-empty array")
        # Validate the latest user message
        last = messages[-1]
        if last.get("role") != "user" or not last.get("content", "").strip():
            raise ValueError("Last message must be a non-empty user message")
        if len(last["content"]) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message too long (max {MAX_MESSAGE_LENGTH} characters)")
        # Sanitize: only allow role and content keys, limit history length
        allowed_roles = {"user", "assistant"}
        clean = []
        for m in messages[-10:]:  # Keep last 10 messages (5 turns)
            if m.get("role") in allowed_roles and m.get("content"):
                clean.append({"role": m["role"], "content": m["content"]})
        return clean
    elif "message" in data:
        message = data["message"].strip()
        if not message:
            raise ValueError("Message is empty")
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message too long (max {MAX_MESSAGE_LENGTH} characters)")
        return [{"role": "user", "content": message}]
    else:
        raise ValueError("Missing 'message' or 'messages' key in request body")


def build_response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    """Build a Lambda Function URL response with CORS headers.

    Parameters
    ----------
    status_code : int
        HTTP status code.
    body : dict[str, Any]
        Response body to serialize as JSON.

    Returns
    -------
    dict[str, Any]
        Lambda Function URL response dict.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def handler(event: dict, context: Any) -> dict[str, Any]:
    """Lambda Function URL handler.

    Parameters
    ----------
    event : dict
        Lambda Function URL event.
    context : Any
        Lambda context object (unused).

    Returns
    -------
    dict[str, Any]
        Lambda Function URL response.
    """
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if method == "OPTIONS":
        return build_response(200, {})

    if method != "POST":
        return build_response(405, {"error": "Method not allowed"})

    try:
        messages = parse_request(event.get("body"))
    except ValueError as e:
        return build_response(400, {"error": str(e)})

    try:
        client = get_anthropic_client()
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=MAX_TOKENS,
            system=build_system_prompt(),
            messages=messages,
        )
        assistant_text = response.content[0].text
        return build_response(200, {"response": assistant_text})
    except Exception as e:
        logger.error("Anthropic API error: %s", e, exc_info=True)
        return build_response(500, {"error": "Internal server error"})
