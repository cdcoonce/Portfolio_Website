# Lambda-Chat-Agent

<!-- generated:start -->
## Lambda Chat Agent

The portfolio chat widget is powered by an AWS Lambda function that receives POST requests from the browser, validates the message, builds a system prompt from the knowledge base, and proxies the conversation to the Anthropic Claude Haiku model.

### Chat Request Sequence

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Lambda
    participant Anthropic

    User->>Browser: types message
    Browser->>Browser: rate limit check
    Browser->>Lambda: POST {messages: [...]}
    Lambda->>Lambda: ChatRequest.from_body()
    Lambda->>Lambda: build_system_prompt()
    Lambda->>Anthropic: messages.create(model, system, messages)
    Anthropic-->>Lambda: assistant text block
    Lambda-->>Browser: 200 {response: text}
    Browser-->>User: renders assistant reply
```

### Class Diagram

```mermaid
classDiagram
    class ChatRequest {
        +messages
        +from_body()
    }
    class ChatAgent {
        -_client
        -_system_prompt
        -_model
        -_max_tokens
        +reply()
    }
    ChatAgent ..> ChatRequest : uses
```

## Dependencies

| Package | Source |
|---|---|
| `anthropic` | `lambda/requirements.txt` |

## Configuration

| Constant | Value |
|---|---|
| `MODEL_ID` | `claude-haiku-4-5-20251001` |
| `MAX_TOKENS` | `512` |
| `MAX_MESSAGE_LENGTH` | `1000` |
<!-- generated:end -->

<!-- claude:prose -->

<!-- claude:prose:end -->
