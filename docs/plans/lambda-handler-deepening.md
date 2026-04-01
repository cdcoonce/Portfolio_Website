# Refactor: Deepen Lambda Handler with ChatAgent + ChatRequest Pattern

## Problem

The Lambda handler (`lambda/lambda_function.py`, ~242 lines) has several architectural friction points:

- **`parse_request()` mixes three concerns** — JSON parsing, input validation, and conversation history sanitization in one function. Its return type changed from `str` to `list[dict]` when multi-turn conversations were added, but tests weren't updated — resulting in a **broken test** on line 54.
- **`handler()` is a shallow orchestrator** with a single `except Exception` block that catches everything (IndexError, APIError, KeyError) and logs it all as "Anthropic API error." There's no way to distinguish client input errors (400) from upstream failures (502) from code bugs (500).
- **`response.content[0].text` is unsafe** — if the Anthropic API returns an empty content array, this crashes with an IndexError that gets swallowed by the broad exception handler.
- **No dependency injection** — `get_anthropic_client()` and `load_knowledge_base()` are called inside functions, forcing tests to use `mocker.patch()` to intercept them. This couples tests to import paths.
- **Zero test coverage** for the conversation history path (lines 146-162), which is already used by the frontend.

**Dependency category:** True external (Mock) — the Anthropic API is a third-party service. The deepened module should take the client as an injected dependency, with tests providing a fake implementation.

## Proposed Interface

Design C: Caller-Optimized — trivial for both the Lambda runtime and the test suite.

### Public API Surface

```python
# --- Value Object: parse-validate-sanitize boundary ---

class ChatRequest:
    messages: list[dict[str, str]]

    @staticmethod
    def from_body(body: str | None) -> "ChatRequest":
        """Parse raw JSON body -> validated ChatRequest.
        Raises RequestError on any validation failure."""

# --- Orchestrator: injectable, no patching needed ---

class ChatAgent:
    def __init__(
        self,
        *,
        client: anthropic.Anthropic,
        system_prompt: str,
        model: str = MODEL_ID,
        max_tokens: int = MAX_TOKENS,
    ) -> None: ...

    def reply(self, request: ChatRequest) -> str:
        """Send messages to Claude, return assistant text.
        Raises ApiError or EmptyResponseError."""

# --- Error hierarchy with HTTP status codes ---

class ChatAgentError(Exception): ...
class RequestError(ChatAgentError): ...       # -> 400
class ApiError(ChatAgentError): ...           # -> 502
class EmptyResponseError(ChatAgentError): ... # -> 502

# --- Lambda entry points ---

def handler_with_agent(event, context, agent: ChatAgent) -> dict:
    """Testable core."""

def handler(event, context) -> dict:
    """Lambda entry point. Delegates to handler_with_agent with cached default agent."""

# --- Pure helpers (unchanged) ---

def build_response(status_code: int, body: dict) -> dict: ...
def build_system_prompt(knowledge_base: dict) -> str: ...
def load_knowledge_base(path: Path | None = None) -> dict: ...
```

### Usage — Lambda Runtime (zero changes needed)

```python
_default_agent = create_default_agent()

def handler(event, context):
    return handler_with_agent(event, context, _default_agent)
```

### Usage — Tests (zero mocking needed)

```python
def test_reply_with_conversation_history():
    agent = ChatAgent(
        client=FakeClient(["About that project..."]),
        system_prompt="You are helpful.",
    )
    body = json.dumps({"messages": [
        {"role": "user", "content": "Tell me about projects"},
        {"role": "assistant", "content": "Here are some projects..."},
        {"role": "user", "content": "Tell me more about the first one"},
    ]})
    request = ChatRequest.from_body(body)
    assert agent.reply(request) == "About that project..."
```

### What It Hides Internally

| Hidden inside                                                                                                   | Exposed to callers                                                        |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| JSON parsing, format detection (`message` vs `messages`), length validation, role filtering, history truncation | `ChatRequest.from_body(body)` -> validated object or `RequestError`       |
| Anthropic SDK call mechanics, safe content extraction, empty-list guard                                         | `agent.reply(request)` -> `str` or raises `ApiError`/`EmptyResponseError` |
| Knowledge base file I/O, caching                                                                                | `load_knowledge_base(path)` — only called by `create_default_agent()`     |
| System prompt string assembly (80 lines)                                                                        | `build_system_prompt(kb)` — pure function, takes dict, returns string     |

## Dependency Strategy

**True external (Mock)** — the Anthropic API is injected via constructor.

| Concern        | Production                                          | Test                                                    |
| -------------- | --------------------------------------------------- | ------------------------------------------------------- |
| LLM client     | `anthropic.Anthropic()` passed to `ChatAgent`       | `FakeClient` with canned responses                      |
| Knowledge base | `load_knowledge_base()` reads bundled JSON          | Pass a minimal dict to `build_system_prompt()` directly |
| System prompt  | `build_system_prompt(kb)` called once at cold start | Pass a short string like `"You are helpful."`           |
| Wiring         | `create_default_agent()` composes everything        | `ChatAgent(client=fake, system_prompt="test")`          |

## Testing Strategy

### New boundary tests to write

- `ChatRequest.from_body()` with single message -> returns `ChatRequest` with one message
- `ChatRequest.from_body()` with conversation history -> sanitizes to 10 messages, filters roles
- `ChatRequest.from_body()` with invalid input -> raises `RequestError` (empty, too long, bad JSON, missing keys)
- `ChatAgent.reply()` with valid request -> returns assistant text
- `ChatAgent.reply()` with empty API response -> raises `EmptyResponseError`
- `ChatAgent.reply()` with API failure -> raises `ApiError`
- `handler_with_agent()` full POST flow -> 200 with response
- `handler_with_agent()` with bad input -> 400
- `handler_with_agent()` with API error -> 502
- `handler_with_agent()` OPTIONS/GET -> 200/405

### Old tests to update or replace

- `TestParseRequest.test_parse_valid_message` (line 54) — **currently broken**, replace with `ChatRequest.from_body()` tests
- `TestParseRequest` remaining tests — migrate to test `ChatRequest.from_body()` raising `RequestError`
- `TestHandler` tests — migrate to use `handler_with_agent()` with fake agent instead of `mocker.patch`
- `TestBuildSystemPrompt` — keep as-is, but `build_system_prompt` now takes a dict parameter

### Test environment needs

- A `FakeClient` class (or `SimpleNamespace` stand-in) that satisfies duck typing for `anthropic.Anthropic().messages.create()`
- No external services, no mocking libraries needed for core tests

## Implementation Recommendations

### What the module should own

- HTTP method routing (OPTIONS, POST, 405)
- Request parsing, validation, and sanitization (single responsibility: raw body -> validated `ChatRequest`)
- LLM conversation orchestration (system prompt + messages -> assistant text)
- Safe response extraction (guard against empty content arrays)
- Error classification (client error vs upstream failure vs code bug)
- Lambda response formatting

### What it should hide

- JSON parsing mechanics and format detection (`message` vs `messages`)
- Conversation history truncation logic (10 messages, role filtering)
- Anthropic SDK call details (`client.messages.create(...)`)
- Content array safety checks
- Knowledge base file I/O and caching

### What it should expose

- `ChatRequest.from_body(body)` — the parse/validate boundary
- `ChatAgent(client, system_prompt)` — the injectable orchestrator
- `ChatAgent.reply(request)` — the conversation boundary
- `handler_with_agent(event, context, agent)` — the testable Lambda core
- `handler(event, context)` — the production entry point
- `build_system_prompt(kb)` — pure function for prompt construction
- Three error types with HTTP status semantics

### How callers should migrate

1. Fix the broken test first (line 54) by updating to expect `ChatRequest` from `from_body()`
2. Replace `mocker.patch("lambda_function.get_anthropic_client")` with `ChatAgent(client=FakeClient(...))`
3. Replace `handler(event, None)` calls in tests with `handler_with_agent(event, None, agent)`
4. Add conversation history tests using `ChatRequest.from_body()` with `{"messages": [...]}`
5. Delete `get_anthropic_client()` — replaced by constructor injection

## CEO Review Decisions (2026-03-31, HOLD SCOPE)

| #   | Issue              | Decision                                                                                                                                               | Rationale                                                           |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| 1   | File layout        | **Single file** — all new classes stay in `lambda_function.py`                                                                                         | Under 350 lines total; minimal diff; simpler Lambda packaging       |
| 2   | Catch-all handler  | **Typed catch-all** in `handler_with_agent()`: `ChatAgentError` → mapped status, final `except Exception` → 500 + `logger.exception()` with class name | Prevents unhandled Lambda crashes; zero silent failures             |
| 3   | Content extraction | **Filter for TextBlock** explicitly in `reply()` — find first block with `type == "text"`, raise `EmptyResponseError` if none                          | Future-proofs against ToolUseBlock if tools are ever added          |
| 4   | Test migration     | **Atomic delete-and-replace** per test class — new tests + old test removal in same commit                                                             | Suite stays green at every commit; no xfail markers                 |
| 5   | Cold start         | **Lazy init** — `_default_agent = None` at module level, `create_default_agent()` on first `handler()` call                                            | Bad knowledge base fails one request with 500, not the whole Lambda |

### Updated handler error map

```
handler_with_agent():
  except RequestError        → 400 + error message
  except EmptyResponseError  → 502 + "Empty response from AI"
  except ApiError            → 502 + "AI service error"
  except Exception           → 500 + "Internal server error" + logger.exception(class name)
```

### Updated cold-start pattern

```python
_default_agent: ChatAgent | None = None

def handler(event, context):
    global _default_agent
    if _default_agent is None:
        _default_agent = create_default_agent()
    return handler_with_agent(event, context, _default_agent)
```
