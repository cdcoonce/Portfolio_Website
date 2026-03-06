# Plan: Claude Chat Agent for Portfolio Website

## Context

Add an AI-powered chat section to charleslikesdata.com so visitors can ask questions about Charles's 17 portfolio projects, skills, and background. The site is static (vanilla HTML/CSS/JS on GitHub Pages), so a lightweight AWS Lambda backend proxies requests to the Claude API without exposing the API key.

**User decisions:**

- AWS Lambda (Python) with Lambda Function URL — no API Gateway
- Claude Haiku model for speed and cost
- Chat UI as a dedicated section between Projects and Testimonials on the homepage
- Scope: projects + about me (background, skills, experience)
- Client-side rate limiting (localStorage, 10 questions/hour)
- User needs to create an AWS account from scratch

## Architecture

```text
Browser (charleslikesdata.com)            AWS Lambda
┌──────────────────────────────┐    ┌───────────────────────────┐
│ index.html #chat-agent       │    │ lambda_function.py        │
│ chat.js                      │    │   anthropic SDK           │
│   - rate limit (localStorage)│    │   knowledge_base.json     │
│   - fetch() POST             │───>│   system prompt builder   │
│   - message display          │<───│   CORS headers            │
└──────────────────────────────┘    └───────────────────────────┘
```

Stateless: each request sends only the current question. The Lambda builds a system prompt from `knowledge_base.json` and calls Claude Haiku. Client manages conversation display in the DOM.

---

## Phase Index

Each phase has a detailed implementation document with full code, exact file paths, line numbers, and step-by-step instructions for agents.

| Phase | Document | Summary |
| ----- | -------- | ------- |
| 1 | [phase-1-knowledge-base.md](./phase-1-knowledge-base.md) | Markdown context files + build script to generate JSON |
| 2 | [phase-2-lambda-function.md](./phase-2-lambda-function.md) | Build Lambda handler with Anthropic SDK (TDD) |
| 3 | [phase-3-aws-setup.md](./phase-3-aws-setup.md) | AWS account creation + Lambda deployment guide |
| 4 | [phase-4-chat-ui.md](./phase-4-chat-ui.md) | HTML section + CSS styles (TDD) |
| 5 | [phase-5-chat-js.md](./phase-5-chat-js.md) | JavaScript chat module (TDD) |
| 6 | [phase-6-wiring.md](./phase-6-wiring.md) | Wire chat.js into main.js + config updates |
| 7 | [phase-7-verification.md](./phase-7-verification.md) | Full test suite verification |
| 8 | [phase-8-ci-cd.md](./phase-8-ci-cd.md) | CI/CD pipeline updates |

## Execution Order and Dependencies

```text
Phase 1 (knowledge base)
    │
    ├──> Phase 2 (Lambda) ──> Phase 3 (AWS setup)
    │
    └──> Phase 4 (HTML+CSS) ──> Phase 5 (chat.js) ──> Phase 6 (wiring)
                                                            │
                                                            v
                                                     Phase 7 (verification)
                                                            │
                                                            v
                                                     Phase 8 (CI/CD)
```

**Phases 2 and 4 are independent** and can be dispatched as parallel subagents after Phase 1 completes.

## Files Summary

| Action | File | Purpose |
| ------ | ---- | ------- |
| Create | `WebContent/context/about.md` | Person bio, contact, background |
| Create | `WebContent/context/skills.md` | Skills by category |
| Create | `WebContent/context/testimonials.md` | Colleague testimonials |
| Create | `WebContent/context/projects/*.md` | 17 project files (one per project) |
| Create | `scripts/build_knowledge_base.py` | Compiles context/ into JSON |
| Create | `lambda/knowledge_base.json` | Generated output (do not edit directly) |
| Create | `lambda/lambda_function.py` | Lambda handler |
| Create | `lambda/requirements.txt` | Python deps |
| Create | `lambda/tests/__init__.py` | Package marker |
| Create | `lambda/tests/test_lambda.py` | Lambda unit tests |
| Create | `WebContent/js/chat.js` | Chat UI module |
| Create | `__tests__/chat.test.js` | Jest tests for chat |
| Create | `tests/test_chat.py` | E2E tests for chat |
| Create | `docs/plans/chat-agent/aws-setup.md` | AWS setup guide |
| Modify | `index.html` | Add chat section + nav link |
| Modify | `WebContent/css/style.css` | Chat styles |
| Modify | `WebContent/css/mediaqueries.css` | Mobile chat styles |
| Modify | `WebContent/js/main.js` | Import + init chat |
| Modify | `tests/test_validation.py` | HTML validation tests |
| Modify | `eslint.config.mjs` | Add fetch/localStorage globals |
| Modify | `.prettierignore` | Exclude lambda/ |
