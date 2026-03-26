"""E2E tests for the AI chat agent widget."""

import json
import pytest


LAMBDA_URL = 'https://a4qby7o6wqmq7rpb6rorezbc7u0tsyhc.lambda-url.us-west-1.on.aws/'
MOCK_RESPONSE = "I am Charles's AI assistant. Here is a test response."


def make_success_handler(response_text=MOCK_RESPONSE):
    """Return a Playwright route handler that fulfils with a successful JSON response."""

    def handler(route, request):
        route.fulfill(
            status=200,
            content_type='application/json',
            body=json.dumps({'response': response_text}),
        )

    return handler


def error_handler(route, request):
    """Playwright route handler that returns a 500 error."""
    route.fulfill(
        status=500,
        content_type='application/json',
        body=json.dumps({'error': 'Internal server error'}),
    )


@pytest.mark.e2e
class TestChatWidgetStructure:
    """Verify the chat widget DOM is present and correctly structured."""

    def test_chat_agent_container_is_visible(self, page):
        chat = page.locator('#chat-agent')
        assert chat.is_visible(), '#chat-agent container should be visible on page load'

    def test_chat_input_is_visible(self, page):
        assert page.locator('#chat-input').is_visible(), '#chat-input should be visible'

    def test_chat_send_button_is_visible(self, page):
        assert page.locator('#chat-send').is_visible(), '#chat-send button should be visible'

    def test_chat_messages_container_is_visible(self, page):
        assert page.locator('#chat-messages').is_visible(), '#chat-messages should be visible'

    def test_initial_assistant_greeting_is_present(self, page):
        """The assistant welcome message should appear on load without any user action."""
        messages = page.locator('#chat-messages .chat-message.assistant')
        assert messages.count() >= 1, 'At least one assistant message should exist on load'
        first = messages.first.inner_text()
        assert 'Charles' in first, f'Initial greeting should mention Charles, got: {first}'


@pytest.mark.e2e
class TestChatSend:
    """Verify sending a message triggers a request and displays the response."""

    def test_typing_and_clicking_send_shows_user_message(self, page):
        page.route(LAMBDA_URL, make_success_handler())
        page.fill('#chat-input', 'What projects has Charles worked on?')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        user_messages = page.locator('#chat-messages .chat-message.user')
        assert user_messages.count() >= 1, 'User message should appear after send'
        assert 'What projects' in user_messages.first.inner_text()

    def test_successful_response_appears_in_messages(self, page):
        reply = 'Charles has worked on data engineering pipelines.'
        page.route(LAMBDA_URL, make_success_handler(reply))
        page.fill('#chat-input', 'Tell me about Charles.')
        page.click('#chat-send')
        page.wait_for_selector(f'#chat-messages .chat-message.assistant >> text={reply[:30]}')
        assistant_msgs = page.locator('#chat-messages .chat-message.assistant')
        texts = [assistant_msgs.nth(i).inner_text() for i in range(assistant_msgs.count())]
        assert any(reply in t for t in texts), f'Expected reply not found. Messages: {texts}'

    def test_enter_key_sends_message(self, page):
        page.route(LAMBDA_URL, make_success_handler())
        page.fill('#chat-input', 'Hello via Enter key')
        page.keyboard.press('Enter')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        user_messages = page.locator('#chat-messages .chat-message.user')
        assert user_messages.count() >= 1, 'User message should appear after Enter key'

    def test_input_cleared_after_send(self, page):
        page.route(LAMBDA_URL, make_success_handler())
        page.fill('#chat-input', 'Clear me after send')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        value = page.input_value('#chat-input')
        assert value == '', f'Input should be empty after send, got: {value!r}'

    def test_empty_input_does_not_send_request(self, page):
        requests_made = []

        def capture_abort(route, request):
            requests_made.append(request.url)
            route.abort()

        page.route(LAMBDA_URL, capture_abort)
        page.fill('#chat-input', '')
        page.click('#chat-send')
        page.wait_for_timeout(300)
        assert len(requests_made) == 0, 'No request should be sent for an empty message'

    def test_whitespace_only_input_does_not_send_request(self, page):
        requests_made = []

        def capture_abort(route, request):
            requests_made.append(request.url)
            route.abort()

        page.route(LAMBDA_URL, capture_abort)
        page.fill('#chat-input', '   ')
        page.click('#chat-send')
        page.wait_for_timeout(300)
        assert len(requests_made) == 0, 'No request should be sent for whitespace-only input'


@pytest.mark.e2e
class TestChatLoadingIndicator:
    """Verify the loading indicator appears while waiting and disappears after response."""

    def test_loading_indicator_gone_after_response(self, page):
        page.route(LAMBDA_URL, make_success_handler())
        page.fill('#chat-input', 'Fast response test')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        assert page.locator('#chat-loading').count() == 0, (
            '#chat-loading element should not exist after response is received'
        )

    def test_send_button_disabled_while_processing(self, page):
        """Send button should be disabled while a request is in flight."""
        send_was_disabled = []

        def capture_disabled_state(route, request):
            disabled = page.get_attribute('#chat-send', 'disabled')
            send_was_disabled.append(disabled is not None)
            route.fulfill(
                status=200,
                content_type='application/json',
                body=json.dumps({'response': 'Reply.'}),
            )

        page.route(LAMBDA_URL, capture_disabled_state)
        page.fill('#chat-input', 'Are you disabled?')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        assert any(send_was_disabled), 'Send button should be disabled while request is in flight'


@pytest.mark.e2e
class TestChatErrorHandling:
    """Verify graceful degradation when the Lambda API returns an error."""

    def test_network_error_shows_error_message(self, page):
        page.route(LAMBDA_URL, lambda route, request: route.abort('failed'))
        page.fill('#chat-input', 'Trigger a network error')
        page.click('#chat-send')
        page.wait_for_timeout(2000)
        assistant_msgs = page.locator('#chat-messages .chat-message.assistant')
        texts = [assistant_msgs.nth(i).inner_text() for i in range(assistant_msgs.count())]
        error_shown = any('wrong' in t.lower() or 'error' in t.lower() for t in texts)
        assert error_shown, f'Error message should appear after network failure. Got: {texts}'

    def test_server_error_shows_error_message(self, page):
        page.route(LAMBDA_URL, error_handler)
        page.fill('#chat-input', 'Trigger a server error')
        page.click('#chat-send')
        page.wait_for_timeout(2000)
        assistant_msgs = page.locator('#chat-messages .chat-message.assistant')
        texts = [assistant_msgs.nth(i).inner_text() for i in range(assistant_msgs.count())]
        error_shown = any('wrong' in t.lower() or 'error' in t.lower() for t in texts)
        assert error_shown, f'Error message should appear after 500 response. Got: {texts}'

    def test_send_button_re_enabled_after_error(self, page):
        page.route(LAMBDA_URL, lambda route, request: route.abort('failed'))
        page.fill('#chat-input', 'Error recovery test')
        page.click('#chat-send')
        page.wait_for_timeout(2000)
        is_disabled = page.get_attribute('#chat-send', 'disabled')
        assert is_disabled is None, 'Send button should be re-enabled after error'

    def test_loading_indicator_gone_after_error(self, page):
        page.route(LAMBDA_URL, lambda route, request: route.abort('failed'))
        page.fill('#chat-input', 'Loading gone on error')
        page.click('#chat-send')
        page.wait_for_timeout(2000)
        assert page.locator('#chat-loading').count() == 0, (
            '#chat-loading should be removed even when request fails'
        )


@pytest.mark.e2e
class TestChatConversationHistory:
    """Verify multi-turn conversations display correctly and in order."""

    def test_multiple_messages_appear_in_order(self, page):
        replies = ['First reply.', 'Second reply.', 'Third reply.']
        call_count = [0]

        def sequential_response(route, request):
            idx = call_count[0]
            call_count[0] += 1
            text = replies[idx] if idx < len(replies) else 'Extra reply.'
            route.fulfill(
                status=200,
                content_type='application/json',
                body=json.dumps({'response': text}),
            )

        page.route(LAMBDA_URL, sequential_response)

        for question in ['Question one', 'Question two', 'Question three']:
            page.fill('#chat-input', question)
            page.click('#chat-send')
            page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
            page.wait_for_timeout(100)

        user_msgs = page.locator('#chat-messages .chat-message.user')
        assistant_msgs = page.locator('#chat-messages .chat-message.assistant')

        assert user_msgs.count() == 3, f'Expected 3 user messages, got {user_msgs.count()}'
        # 1 initial greeting + 3 replies
        assert assistant_msgs.count() == 4, (
            f'Expected 4 assistant messages (1 greeting + 3 replies), got {assistant_msgs.count()}'
        )

    def test_request_body_includes_conversation_history(self, page):
        """Each request should carry the full conversation history."""
        captured_bodies = []

        def capture_and_respond(route, request):
            body = json.loads(request.post_data)
            captured_bodies.append(body)
            route.fulfill(
                status=200,
                content_type='application/json',
                body=json.dumps({'response': 'Acknowledged.'}),
            )

        page.route(LAMBDA_URL, capture_and_respond)

        page.fill('#chat-input', 'First message')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)
        page.wait_for_timeout(100)

        page.fill('#chat-input', 'Second message')
        page.click('#chat-send')
        page.wait_for_selector('#chat-loading', state='detached', timeout=5000)

        assert len(captured_bodies) == 2, f'Expected 2 requests, got {len(captured_bodies)}'
        # Second request should have more messages than the first
        first_len = len(captured_bodies[0]['messages'])
        second_len = len(captured_bodies[1]['messages'])
        assert second_len > first_len, (
            f'Second request should carry more history than first ({second_len} > {first_len})'
        )


@pytest.mark.e2e
class TestChatRateLimit:
    """Verify rate limiting blocks requests and shows the correct warning."""

    def test_rate_limit_warning_visible_at_low_remaining(self, page):
        """When fewer than 4 requests remain, the rate limit warning should appear."""
        # Inject 23 timestamps (leaving 2 remaining of 25) into localStorage
        now_ms = int(page.evaluate('Date.now()'))
        timestamps = [now_ms - i * 1000 for i in range(23)]
        page.evaluate(
            f"localStorage.setItem('chat_rate_limit', JSON.stringify({timestamps}))"
        )
        page.reload()
        page.wait_for_timeout(300)
        rate_limit_el = page.locator('#chat-rate-limit')
        hidden_attr = rate_limit_el.get_attribute('hidden')
        assert hidden_attr is None, (
            '#chat-rate-limit should be visible when few requests remain'
        )
        text = rate_limit_el.inner_text()
        assert 'remaining' in text.lower(), (
            f'Rate limit text should mention "remaining", got: {text}'
        )

    def test_rate_limit_reached_disables_input(self, page):
        """Once limit is hit, the input and send button should be disabled."""
        now_ms = int(page.evaluate('Date.now()'))
        timestamps = [now_ms - i * 1000 for i in range(25)]
        page.evaluate(
            f"localStorage.setItem('chat_rate_limit', JSON.stringify({timestamps}))"
        )
        page.reload()
        page.wait_for_timeout(300)
        input_disabled = page.get_attribute('#chat-input', 'disabled')
        send_disabled = page.get_attribute('#chat-send', 'disabled')
        assert input_disabled is not None, '#chat-input should be disabled at rate limit'
        assert send_disabled is not None, '#chat-send should be disabled at rate limit'

    def test_rate_limit_message_says_try_again_later(self, page):
        now_ms = int(page.evaluate('Date.now()'))
        timestamps = [now_ms - i * 1000 for i in range(25)]
        page.evaluate(
            f"localStorage.setItem('chat_rate_limit', JSON.stringify({timestamps}))"
        )
        page.reload()
        page.wait_for_timeout(300)
        text = page.locator('#chat-rate-limit').inner_text()
        assert 'later' in text.lower() or 'limit' in text.lower(), (
            f'Rate limit message should mention limit/later, got: {text}'
        )

    def test_expired_timestamps_do_not_count_toward_limit(self, page):
        """Timestamps older than 1 hour should be ignored — user should not be rate limited."""
        now_ms = int(page.evaluate('Date.now()'))
        old_base = now_ms - 2 * 60 * 60 * 1000  # 2 hours ago
        timestamps = [old_base - i * 1000 for i in range(25)]
        page.evaluate(
            f"localStorage.setItem('chat_rate_limit', JSON.stringify({timestamps}))"
        )
        page.reload()
        page.wait_for_timeout(300)
        input_disabled = page.get_attribute('#chat-input', 'disabled')
        assert input_disabled is None, (
            '#chat-input should NOT be disabled when all timestamps are expired'
        )
