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


# --- Error hierarchy with HTTP status semantics ---


class ChatAgentError(Exception):
    """Base error for chat agent operations."""


class RequestError(ChatAgentError):
    """Client input validation failure -> HTTP 400."""


class ApiError(ChatAgentError):
    """Upstream API failure -> HTTP 502."""


class EmptyResponseError(ChatAgentError):
    """API returned no text content -> HTTP 502."""


MODEL_ID = "claude-haiku-4-5-20251001"
MAX_TOKENS = 512
_knowledge_base: dict | None = None


def load_knowledge_base(path: Path | None = None) -> dict:
    """Load the portfolio knowledge base from a JSON file.

    Parameters
    ----------
    path : Path | None
        Path to the knowledge base JSON. If None, uses the bundled default.
    """
    global _knowledge_base
    if path is not None:
        return json.loads(path.read_text())
    if _knowledge_base is None:
        kb_path = Path(__file__).parent / "knowledge_base.json"
        _knowledge_base = json.loads(kb_path.read_text())
    return _knowledge_base


def build_system_prompt(kb: dict | None = None) -> str:
    """Construct the system prompt from the knowledge base.

    Parameters
    ----------
    kb : dict | None
        Knowledge base dict. If None, loads from bundled JSON file.
    """
    if kb is None:
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


class ChatRequest:
    """Validated conversation request — parse/validate/sanitize boundary.

    Parameters
    ----------
    messages : list[dict[str, str]]
        Sanitized conversation messages ready for the Anthropic API.
    """

    def __init__(self, messages: list[dict[str, str]]) -> None:
        self.messages = messages

    @staticmethod
    def from_body(body: str | None) -> "ChatRequest":
        """Parse raw JSON body into a validated ChatRequest.

        Parameters
        ----------
        body : str | None
            Raw JSON string from the request body.

        Returns
        -------
        ChatRequest
            Validated request with sanitized messages.

        Raises
        ------
        RequestError
            If the body is missing, not valid JSON, or messages are invalid.
        """
        if not body:
            raise RequestError("Request body is empty")
        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RequestError("Invalid JSON in request body") from exc

        if "messages" in data:
            messages = data["messages"]
            if not isinstance(messages, list) or not messages:
                raise RequestError("Messages must be a non-empty array")
            last = messages[-1]
            if last.get("role") != "user" or not last.get("content", "").strip():
                raise RequestError("Last message must be a non-empty user message")
            if len(last["content"]) > MAX_MESSAGE_LENGTH:
                raise RequestError(
                    f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"
                )
            allowed_roles = {"user", "assistant"}
            clean = []
            for m in messages[-10:]:
                if m.get("role") in allowed_roles and m.get("content"):
                    clean.append({"role": m["role"], "content": m["content"]})
            return ChatRequest(clean)
        elif "message" in data:
            message = data["message"].strip()
            if not message:
                raise RequestError("Message is empty")
            if len(message) > MAX_MESSAGE_LENGTH:
                raise RequestError(
                    f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"
                )
            return ChatRequest([{"role": "user", "content": message}])
        else:
            raise RequestError(
                "Missing 'message' or 'messages' key in request body"
            )


class ChatAgent:
    """Injectable LLM orchestrator — no patching needed in tests.

    Parameters
    ----------
    client : anthropic.Anthropic
        Anthropic API client (injected for testability).
    system_prompt : str
        System prompt for the conversation.
    model : str
        Model ID for the Anthropic API.
    max_tokens : int
        Maximum tokens in the response.
    """

    def __init__(
        self,
        *,
        client: anthropic.Anthropic,
        system_prompt: str,
        model: str = MODEL_ID,
        max_tokens: int = MAX_TOKENS,
    ) -> None:
        self._client = client
        self._system_prompt = system_prompt
        self._model = model
        self._max_tokens = max_tokens

    def reply(self, request: ChatRequest) -> str:
        """Send messages to Claude, return assistant text.

        Parameters
        ----------
        request : ChatRequest
            Validated conversation request.

        Returns
        -------
        str
            Assistant response text.

        Raises
        ------
        ApiError
            If the Anthropic API call fails.
        EmptyResponseError
            If the API returns no text content.
        """
        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=self._system_prompt,
                messages=request.messages,
            )
        except anthropic.APIError as exc:
            raise ApiError(str(exc)) from exc

        # Filter for TextBlock — future-proof against ToolUseBlock
        for block in response.content:
            if getattr(block, "type", None) == "text":
                return block.text

        raise EmptyResponseError("API returned no text content")


def create_default_agent() -> ChatAgent:
    """Wire up the production ChatAgent with real client and knowledge base."""
    return ChatAgent(
        client=anthropic.Anthropic(),
        system_prompt=build_system_prompt(),
    )


def build_response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    """Build a Lambda Function URL response.

    CORS is handled by the AWS Lambda Function URL configuration,
    not by application-level headers. See the AllowOrigins list in
    the Function URL CORS settings.

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


_default_agent: ChatAgent | None = None


def handler_with_agent(
    event: dict, context: Any, agent: ChatAgent
) -> dict[str, Any]:
    """Testable Lambda core — all dependencies injected.

    Parameters
    ----------
    event : dict
        Lambda Function URL event.
    context : Any
        Lambda context object (unused).
    agent : ChatAgent
        Injected chat agent for LLM calls.

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
        request = ChatRequest.from_body(event.get("body"))
        assistant_text = agent.reply(request)
        return build_response(200, {"response": assistant_text})
    except RequestError as e:
        return build_response(400, {"error": str(e)})
    except EmptyResponseError:
        logger.error("Empty response from AI")
        return build_response(502, {"error": "Empty response from AI"})
    except ApiError as e:
        logger.error("AI service error: %s", e, exc_info=True)
        return build_response(502, {"error": "AI service error"})
    except Exception as e:
        logger.exception("Unexpected %s: %s", type(e).__name__, e)
        return build_response(500, {"error": "Internal server error"})


def handler(event: dict, context: Any) -> dict[str, Any]:
    """Lambda Function URL entry point — delegates to handler_with_agent.

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
    global _default_agent
    if _default_agent is None:
        _default_agent = create_default_agent()
    return handler_with_agent(event, context, _default_agent)
