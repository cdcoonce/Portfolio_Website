"""Tests for the chat agent Lambda function."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


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


class TestParseRequest:
    def test_parse_valid_message(self):
        from lambda_function import parse_request
        body = json.dumps({"message": "Tell me about your projects"})
        result = parse_request(body)
        assert result == "Tell me about your projects"

    def test_parse_empty_message_raises(self):
        from lambda_function import parse_request
        body = json.dumps({"message": ""})
        with pytest.raises(ValueError, match="empty"):
            parse_request(body)

    def test_parse_missing_message_key_raises(self):
        from lambda_function import parse_request
        body = json.dumps({"query": "hello"})
        with pytest.raises(ValueError, match="message"):
            parse_request(body)

    def test_parse_invalid_json_raises(self):
        from lambda_function import parse_request
        with pytest.raises(ValueError):
            parse_request("not json")

    def test_parse_message_too_long_raises(self):
        from lambda_function import parse_request
        body = json.dumps({"message": "x" * 1001})
        with pytest.raises(ValueError, match="too long"):
            parse_request(body)

    def test_parse_none_body_raises(self):
        from lambda_function import parse_request
        with pytest.raises(ValueError, match="empty"):
            parse_request(None)


class TestBuildResponse:
    def test_success_response_format(self):
        from lambda_function import build_response
        resp = build_response(200, {"response": "Hello!"})
        assert resp["statusCode"] == 200
        assert json.loads(resp["body"])["response"] == "Hello!"

    def test_response_includes_cors_headers(self):
        from lambda_function import build_response
        resp = build_response(200, {"response": "test"})
        headers = resp["headers"]
        assert headers["Access-Control-Allow-Origin"] == "https://charleslikesdata.com"
        assert "POST" in headers["Access-Control-Allow-Methods"]
        assert "Content-Type" in headers["Access-Control-Allow-Headers"]

    def test_error_response_format(self):
        from lambda_function import build_response
        resp = build_response(400, {"error": "Bad request"})
        assert resp["statusCode"] == 400
        assert json.loads(resp["body"])["error"] == "Bad request"


class TestHandler:
    def test_handler_returns_200_on_valid_post(self, mocker):
        from lambda_function import handler
        mock_client = mocker.patch("lambda_function.get_anthropic_client")
        mock_client.return_value.messages.create.return_value.content = [
            mocker.Mock(text="I can help with that!")
        ]
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"message": "What projects use Python?"}),
        }
        result = handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["response"] == "I can help with that!"

    def test_handler_returns_400_on_missing_body(self):
        from lambda_function import handler
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": None,
        }
        result = handler(event, None)
        assert result["statusCode"] == 400

    def test_handler_returns_cors_preflight_on_options(self):
        from lambda_function import handler
        event = {
            "requestContext": {"http": {"method": "OPTIONS"}},
        }
        result = handler(event, None)
        assert result["statusCode"] == 200
        assert "Access-Control-Allow-Origin" in result["headers"]

    def test_handler_returns_405_on_get(self):
        from lambda_function import handler
        event = {
            "requestContext": {"http": {"method": "GET"}},
        }
        result = handler(event, None)
        assert result["statusCode"] == 405
