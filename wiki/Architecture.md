# Architecture

<!-- generated:start -->
## System Architecture

The portfolio is a static site served from GitHub Pages. Interactive features (filtering, carousel, chat) run in the browser via ES modules. The chat widget communicates with an AWS Lambda function that proxies requests to the Anthropic Claude API.

### System Components

```mermaid
graph TD
    Browser["Browser (GitHub Pages)"]
    JSModules["JS Modules\n(main · filter · chat · renderer · carousel · projects · utils)"]
    Lambda["AWS Lambda\n(lambda_function.py)"]
    AnthropicAPI["Anthropic API\n(Claude Haiku)"]
    KnowledgeBase["knowledge_base.json\n(portfolio context)"]

    Browser -->|loads| JSModules
    JSModules -->|POST /chat| Lambda
    Lambda -->|reads| KnowledgeBase
    Lambda -->|messages.create| AnthropicAPI
    AnthropicAPI -->|assistant text| Lambda
    Lambda -->|JSON response| JSModules
    JSModules -->|renders reply| Browser
```

### Chat Data Flow

```mermaid
graph TD
    UserInput["User types message"]
    RateCheck["Rate limit check\n(localStorage)"]
    ChatModule["chat.js\nsendMessage()"]
    LambdaHandler["Lambda handler()\nparse + validate body"]
    ChatAgent["ChatAgent.reply()\nbuild prompt + call API"]
    AnthropicResponse["Anthropic Claude\nHaiku response"]
    RenderReply["Render assistant reply\nto chat UI"]

    UserInput --> RateCheck
    RateCheck -->|within limit| ChatModule
    RateCheck -->|exceeded| RenderReply
    ChatModule -->|POST JSON| LambdaHandler
    LambdaHandler --> ChatAgent
    ChatAgent --> AnthropicResponse
    AnthropicResponse --> ChatAgent
    ChatAgent -->|response text| LambdaHandler
    LambdaHandler -->|200 JSON| ChatModule
    ChatModule --> RenderReply
```

## Key Files

| File | Role |
|---|---|
| `WebContent/js/main.js` | Application entry point — wires all modules |
| `WebContent/js/chat.js` | Chat widget — rate limiting, XSS protection, Lambda calls |
| `lambda/lambda_function.py` | AWS Lambda handler — ChatAgent, ChatRequest |
| `lambda/knowledge_base.json` | Portfolio context for the LLM system prompt |
| `index.html` | Main page — chat widget, projects, testimonials |
| `projects.html` | Full projects listing |
<!-- generated:end -->

<!-- claude:prose -->

<!-- claude:prose:end -->
