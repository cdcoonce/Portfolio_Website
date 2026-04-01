"""Tests for the chat agent Lambda function."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class FakeTextBlock:
    """Mimics anthropic TextBlock with type='text'."""

    def __init__(self, text: str) -> None:
        self.type = "text"
        self.text = text


class FakeResponse:
    """Mimics anthropic Message response."""

    def __init__(self, content: list) -> None:
        self.content = content


class FakeMessages:
    """Mimics client.messages with a create() method."""

    def __init__(self, responses: list[str]) -> None:
        self._responses = iter(responses)

    def create(self, **kwargs) -> FakeResponse:
        text = next(self._responses)
        return FakeResponse([FakeTextBlock(text)])


class FakeClient:
    """Mimics anthropic.Anthropic for testing — no real API calls."""

    def __init__(self, responses: list[str]) -> None:
        self.messages = FakeMessages(responses)


class FakeEmptyClient:
    """Returns an empty content array to test EmptyResponseError."""

    def __init__(self) -> None:
        self.messages = self

    def create(self, **kwargs) -> FakeResponse:
        return FakeResponse([])


class FakeErrorClient:
    """Raises anthropic.APIError on create()."""

    def __init__(self) -> None:
        self.messages = self

    def create(self, **kwargs):
        import anthropic
        raise anthropic.APIError(
            message="Service unavailable",
            request=None,
            body=None,
        )


class TestErrorHierarchy:
    def test_chat_agent_error_is_exception(self):
        from lambda_function import ChatAgentError
        assert issubclass(ChatAgentError, Exception)

    def test_request_error_inherits_chat_agent_error(self):
        from lambda_function import ChatAgentError, RequestError
        assert issubclass(RequestError, ChatAgentError)

    def test_api_error_inherits_chat_agent_error(self):
        from lambda_function import ApiError, ChatAgentError
        assert issubclass(ApiError, ChatAgentError)

    def test_empty_response_error_inherits_chat_agent_error(self):
        from lambda_function import ChatAgentError, EmptyResponseError
        assert issubclass(EmptyResponseError, ChatAgentError)

    def test_error_types_carry_message(self):
        from lambda_function import ApiError, EmptyResponseError, RequestError
        assert str(RequestError("bad input")) == "bad input"
        assert str(ApiError("upstream failed")) == "upstream failed"
        assert str(EmptyResponseError("no text")) == "no text"


class TestBuildSystemPrompt:
    def test_system_prompt_contains_person_name(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "Charles Coonce" in prompt

    def test_system_prompt_contains_skill_tools(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "Python" in prompt
        assert "SQL" in prompt
        assert "Tableau" in prompt

    def test_system_prompt_contains_project_titles(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "Wine Quality Analysis" in prompt
        assert "National Parks" in prompt
        assert "Housing Affordability" in prompt

    def test_system_prompt_contains_project_urls(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "github.com/cdcoonce" in prompt

    def test_system_prompt_contains_contact_info(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "charles.coonce@gmail.com" in prompt
        assert "linkedin.com" in prompt

    def test_system_prompt_contains_testimonials(self):
        from lambda_function import build_system_prompt
        prompt = build_system_prompt()
        assert "Aaron Wallen" in prompt


class TestChatRequest:
    def test_single_message_returns_chat_request(self):
        from lambda_function import ChatRequest
        body = json.dumps({"message": "Tell me about your projects"})
        req = ChatRequest.from_body(body)
        assert req.messages == [{"role": "user", "content": "Tell me about your projects"}]

    def test_conversation_history_sanitizes_to_10_messages(self):
        from lambda_function import ChatRequest
        messages = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg {i}"}
            for i in range(14)
        ]
        # Last must be user
        messages.append({"role": "user", "content": "final"})
        body = json.dumps({"messages": messages})
        req = ChatRequest.from_body(body)
        assert len(req.messages) <= 10
        assert req.messages[-1]["role"] == "user"
        assert req.messages[-1]["content"] == "final"

    def test_conversation_history_filters_bad_roles(self):
        from lambda_function import ChatRequest
        messages = [
            {"role": "system", "content": "injected"},
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
            {"role": "user", "content": "question"},
        ]
        body = json.dumps({"messages": messages})
        req = ChatRequest.from_body(body)
        assert all(m["role"] in {"user", "assistant"} for m in req.messages)

    def test_empty_body_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        with pytest.raises(RequestError, match="empty"):
            ChatRequest.from_body(None)

    def test_invalid_json_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        with pytest.raises(RequestError):
            ChatRequest.from_body("not json")

    def test_missing_keys_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        body = json.dumps({"query": "hello"})
        with pytest.raises(RequestError, match="message"):
            ChatRequest.from_body(body)

    def test_message_too_long_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        body = json.dumps({"message": "x" * 1001})
        with pytest.raises(RequestError, match="too long"):
            ChatRequest.from_body(body)

    def test_empty_message_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        body = json.dumps({"message": ""})
        with pytest.raises(RequestError, match="empty"):
            ChatRequest.from_body(body)

    def test_empty_messages_array_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        body = json.dumps({"messages": []})
        with pytest.raises(RequestError, match="non-empty"):
            ChatRequest.from_body(body)

    def test_last_message_not_user_raises_request_error(self):
        from lambda_function import ChatRequest, RequestError
        body = json.dumps({"messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi there"},
        ]})
        with pytest.raises(RequestError, match="user message"):
            ChatRequest.from_body(body)


class TestChatAgent:
    def test_reply_returns_assistant_text(self):
        from lambda_function import ChatAgent, ChatRequest
        agent = ChatAgent(
            client=FakeClient(["Hello from Claude!"]),
            system_prompt="You are helpful.",
        )
        request = ChatRequest([{"role": "user", "content": "hi"}])
        assert agent.reply(request) == "Hello from Claude!"

    def test_reply_with_conversation_history(self):
        from lambda_function import ChatAgent, ChatRequest
        agent = ChatAgent(
            client=FakeClient(["About that project..."]),
            system_prompt="You are helpful.",
        )
        request = ChatRequest([
            {"role": "user", "content": "Tell me about projects"},
            {"role": "assistant", "content": "Here are some projects..."},
            {"role": "user", "content": "Tell me more about the first one"},
        ])
        assert agent.reply(request) == "About that project..."

    def test_reply_raises_empty_response_error(self):
        from lambda_function import ChatAgent, ChatRequest, EmptyResponseError
        agent = ChatAgent(
            client=FakeEmptyClient(),
            system_prompt="You are helpful.",
        )
        request = ChatRequest([{"role": "user", "content": "hi"}])
        with pytest.raises(EmptyResponseError):
            agent.reply(request)

    def test_reply_raises_api_error_on_sdk_failure(self):
        from lambda_function import ApiError, ChatAgent, ChatRequest
        agent = ChatAgent(
            client=FakeErrorClient(),
            system_prompt="You are helpful.",
        )
        request = ChatRequest([{"role": "user", "content": "hi"}])
        with pytest.raises(ApiError):
            agent.reply(request)


class TestBuildResponse:
    def test_success_response_format(self):
        from lambda_function import build_response
        resp = build_response(200, {"response": "Hello!"})
        assert resp["statusCode"] == 200
        assert json.loads(resp["body"])["response"] == "Hello!"

    def test_response_does_not_include_cors_headers(self):
        """CORS is managed by AWS Lambda Function URL config, not application code."""
        from lambda_function import build_response
        resp = build_response(200, {"response": "test"})
        assert "Access-Control-Allow-Origin" not in resp["headers"]

    def test_error_response_format(self):
        from lambda_function import build_response
        resp = build_response(400, {"error": "Bad request"})
        assert resp["statusCode"] == 400
        assert json.loads(resp["body"])["error"] == "Bad request"


class TestHandlerWithAgent:
    def _make_agent(self, responses: list[str]) -> "ChatAgent":
        from lambda_function import ChatAgent
        return ChatAgent(
            client=FakeClient(responses),
            system_prompt="You are helpful.",
        )

    def test_post_returns_200_with_response(self):
        from lambda_function import handler_with_agent
        agent = self._make_agent(["I can help with that!"])
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"message": "What projects use Python?"}),
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["response"] == "I can help with that!"

    def test_post_bad_input_returns_400(self):
        from lambda_function import handler_with_agent
        agent = self._make_agent([])
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": None,
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 400
        assert "empty" in json.loads(result["body"])["error"].lower()

    def test_post_api_error_returns_502(self):
        from lambda_function import ChatAgent, handler_with_agent
        agent = ChatAgent(
            client=FakeErrorClient(),
            system_prompt="You are helpful.",
        )
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"message": "hello"}),
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 502
        assert "error" in json.loads(result["body"])

    def test_post_empty_response_returns_502(self):
        from lambda_function import ChatAgent, handler_with_agent
        agent = ChatAgent(
            client=FakeEmptyClient(),
            system_prompt="You are helpful.",
        )
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"message": "hello"}),
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 502

    def test_options_returns_200(self):
        from lambda_function import handler_with_agent
        agent = self._make_agent([])
        event = {
            "requestContext": {"http": {"method": "OPTIONS"}},
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 200

    def test_get_returns_405(self):
        from lambda_function import handler_with_agent
        agent = self._make_agent([])
        event = {
            "requestContext": {"http": {"method": "GET"}},
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 405

    def test_unexpected_exception_returns_500(self):
        from lambda_function import ChatAgent, handler_with_agent

        class BrokenClient:
            def __init__(self):
                self.messages = self
            def create(self, **kwargs):
                raise RuntimeError("Something completely unexpected")

        agent = ChatAgent(client=BrokenClient(), system_prompt="test")
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"message": "hello"}),
        }
        result = handler_with_agent(event, None, agent)
        assert result["statusCode"] == 500
        assert "Internal server error" in json.loads(result["body"])["error"]
