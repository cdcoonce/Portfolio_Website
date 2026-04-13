# Wiki System Design

**Date:** 2026-04-11
**Status:** Approved

## Overview

A comprehensive, auto-updating wiki for the PortfolioWebsite repo. The wiki covers all aspects of the codebase — architecture, frontend modules, Lambda/chat agent, testing, CI/CD, CSS design system, knowledge base pipeline, architecture decisions, and contributing guide.

The wiki lives in `wiki/` at the repo root, is versioned with the code, and automatically syncs to the GitHub Wiki tab on each relevant push via GitHub Actions.

Content is split into two ownership tiers:

- **Script-generated** (`<!-- generated:start/end -->`): a Python generator per page reads source files and produces structured Markdown (tables, code blocks, Mermaid diagrams). Runs in CI on every qualifying push. Zero cost.
- **Claude prose** (`<!-- claude:prose -->` / `<!-- claude:prose:end -->`): narrative explanation, design rationale, and ADL entries. Refreshed manually by running `/update-wiki`. No CI cost.

---

## Audiences

- **Personal reference** — dev memory aid, quick lookup of module exports, test markers, CSS tokens
- **Future contributors / collaborators** — onboarding, contribution guide, architecture context
- **External visitors** — employers and clients who want to understand project depth

The README becomes a lean 60-second quickstart. All depth lives in the wiki.

---

## Repository Layout

### New directories and files

```text
wiki/                                   # Source of truth, versioned with code
  Home.md
  Architecture.md
  Frontend-Modules.md
  Lambda-Chat-Agent.md
  Testing.md
  CI-CD-Pipeline.md
  CSS-Design-System.md
  Knowledge-Base.md
  Architecture-Decision-Log.md          # Claude prose only — hand-seeded
  Contributing.md

scripts/wiki/                           # One generator per wiki page
  orchestrate.py                        # Entry point — runs all generators
  generate_home.py
  generate_architecture.py
  generate_frontend_modules.py
  generate_lambda.py
  generate_testing.py
  generate_cicd.py
  generate_css.py
  generate_knowledge_base.py
  generate_contributing.py

.github/workflows/wiki-sync.yml         # CI job: generate + sync to GitHub Wiki
.claude/skills/update-wiki/SKILL.md    # /update-wiki skill
```

---

## Wiki Pages

### 1. Home.md

- **Reads:** `package.json`, `pyproject.toml`, `CLAUDE.md`
- **Extracts:** tech stack table, test commands, npm/make scripts, project summary
- **Diagrams:** none
- **Prose section:** brief project narrative (Claude)

### 2. Architecture.md

- **Reads:** `WebContent/js/*.js`, `index.html`, `projects.html`, `lambda/`
- **Extracts:** component inventory, page→module map, import relationships
- **Diagrams:**
  - `graph TD` — system component diagram (browser → JS modules → Lambda → Claude API)
  - `graph TD` — data flow diagram (user interaction → filter/carousel/chat → Lambda → response)
- **Prose section:** narrative explanation of system design and key patterns (Claude)

### 3. Frontend-Modules.md

- **Reads:** `WebContent/js/*.js`
- **Extracts:** exports (regex), JSDoc comments, function signatures, init patterns
- **Diagrams:**
  - `graph LR` — module dependency graph (which modules import which)
- **Prose section:** none (structured output sufficient)

### 4. Lambda-Chat-Agent.md

- **Reads:** `lambda/lambda_function.py`, `lambda/requirements.txt`
- **Extracts:** classes, methods, handler entry point, dependencies, docstrings
- **Diagrams:**
  - `sequenceDiagram` — chat request lifecycle (browser → Lambda → Anthropic API → response)
  - `classDiagram` — ChatAgent and ChatRequest structure
- **Prose section:** description of agent behavior and design decisions (Claude)

### 5. Testing.md

- **Reads:** `__tests__/*.test.js`, `tests/test_*.py`, `jest.config.js`, `pyproject.toml`
- **Extracts:** test file inventory, Jest describe blocks, pytest markers and counts
- **Diagrams:**
  - Coverage matrix table (test suite × source module)
- **Prose section:** none

### 6. CI-CD-Pipeline.md

- **Reads:** `.github/workflows/ci-cd.yml`
- **Extracts:** jobs, steps, triggers, branch rules, environment variables
- **Diagrams:**
  - `flowchart TD` — pipeline stages (lint → test → build → deploy)
  - `gitGraph` — branch strategy (master → gh-pages)
- **Prose section:** none

### 7. CSS-Design-System.md

- **Reads:** `WebContent/css/style.css`, `WebContent/css/mediaqueries.css`
- **Extracts:** CSS custom properties (color tokens, spacing), breakpoints (700px, 1250px), font definitions
- **Diagrams:** none
- **Prose section:** none

### 8. Knowledge-Base.md

- **Reads:** `WebContent/context/*.md`, `scripts/build_knowledge_base.py`
- **Extracts:** context file inventory (name, word count, topic), compile script logic
- **Diagrams:**
  - `flowchart LR` — `context/*.md` → `build_knowledge_base.py` → `knowledge_base.json` → Lambda startup
- **Prose section:** none

### 9. Architecture-Decision-Log.md

- **Reads:** nothing (Claude prose only)
- **Extracts:** n/a
- **Diagrams:** none
- **Content:** ADL entries covering key decisions — no framework, no bundler, Lambda over Edge, ES modules, uv, mobile-first CSS. Each entry: Context → Decision → Consequences.
- **Note:** This page is seeded once manually; the `/update-wiki` skill appends new entries when design decisions are made.

### 10. Contributing.md

- **Reads:** `CLAUDE.md`, `package.json`, `pyproject.toml`, `Makefile`
- **Extracts:** local setup steps, make targets, commit convention rules, branch naming, how to add a project
- **Diagrams:** none
- **Prose section:** onboarding narrative (Claude)

---

## Marker Convention

Each generated wiki page uses HTML comments to partition ownership:

```markdown
<!-- generated:start -->

| Module    | Purpose                        | Key Exports                       |
| --------- | ------------------------------ | --------------------------------- |
| filter.js | Project filtering & visibility | getFilteredVisibility, initFilter |

<!-- generated:end -->

<!-- claude:prose -->

The filter module follows the pure-function + orchestrator pattern...

<!-- claude:prose:end -->
```

**Rules:**

- `orchestrate.py` rewrites only `generated` blocks. It never touches `claude:prose` blocks.
- The `/update-wiki` skill rewrites only `claude:prose` blocks. It never touches `generated` blocks.
- No collisions possible between CI runs and manual Claude updates.

---

## Generation Pipeline

### CI trigger (wiki-sync.yml)

```yaml
on:
  push:
    branches: [master]
    paths:
      - 'WebContent/js/**'
      - 'WebContent/css/**'
      - 'WebContent/context/**'
      - 'lambda/**'
      - '__tests__/**'
      - 'tests/**'
      - '.github/workflows/**'
```

### CI job steps

1. Checkout repo (full history)
2. Set up Python + uv
3. `uv run python scripts/wiki/orchestrate.py` — regenerates all `generated` blocks in `wiki/*.md`
4. Clone GitHub Wiki repo (`https://github.com/cdcoonce/PortfolioWebsite.wiki.git`)
5. Copy `wiki/*.md` into the wiki repo
6. Commit and push using `GITHUB_TOKEN` (no extra secret required)

### orchestrate.py contract

Each generator module exports a single function:

```python
def generate(repo_root: Path) -> str:
    """Return the full Markdown content for this wiki page."""
```

The orchestrator calls each generator, then splices the returned content into the appropriate `generated` block of the existing wiki file (preserving `claude:prose` blocks). On first run, it creates the file with populated `generated` blocks and empty `claude:prose` / `claude:prose:end` markers so the skill has a target to write into. Pages with no prose sections (e.g. `Frontend-Modules.md`) are created with no `claude:prose` markers. The ADL page has no `generated` blocks — the orchestrator skips it entirely.

---

## /update-wiki Skill

**Trigger:** user runs `/update-wiki` or asks to "refresh the wiki"

**Behavior:**

- Reads `wiki/*.md` and identifies `claude:prose` blocks
- Reads relevant source files for context
- Rewrites prose in-place without touching `generated` blocks
- Supports targeting a single page: `/update-wiki Architecture`
- Prompts user to commit and push when done

**Pages with prose sections:**

- `Architecture.md` — system design narrative
- `Lambda-Chat-Agent.md` — agent behavior and design rationale
- `Architecture-Decision-Log.md` — full ADL entries
- `Contributing.md` — onboarding narrative

**Pages without prose sections (script-only):**

- `Frontend-Modules.md`, `Testing.md`, `CI-CD-Pipeline.md`, `CSS-Design-System.md`, `Knowledge-Base.md`

---

## Mermaid Diagrams Reference

| Page              | Diagram Type      | Content                                                    |
| ----------------- | ----------------- | ---------------------------------------------------------- |
| Architecture      | `graph TD`        | System components: browser, JS modules, Lambda, Claude API |
| Architecture      | `graph TD`        | Data flow: user action → module → Lambda → response        |
| Frontend-Modules  | `graph LR`        | Module imports and dependencies                            |
| Lambda-Chat-Agent | `sequenceDiagram` | Chat request lifecycle                                     |
| Lambda-Chat-Agent | `classDiagram`    | ChatAgent, ChatRequest structure                           |
| Testing           | Table matrix      | Test suite coverage per source module                      |
| CI-CD-Pipeline    | `flowchart TD`    | Lint → test → build → deploy stages                        |
| CI-CD-Pipeline    | `gitGraph`        | Branch strategy: master → gh-pages                         |
| Knowledge-Base    | `flowchart LR`    | context/\*.md → JSON → Lambda                              |

---

## README Scope (post-wiki)

The README is trimmed manually (not automated) to a 60-second quickstart:

- One-line project description
- Local setup commands
- How to run tests
- Link to the wiki for everything else

All depth (architecture, modules, decisions, contributing) moves to the wiki. This is a one-time manual edit done after the wiki is populated.

---

## Out of Scope

- No LLM API calls in CI (zero cost constraint)
- No MkDocs, Docsify, or rendered site — GitHub Wiki tab is the UI
- No full AST parsing — regex + line-based extraction is sufficient for this codebase
- No wiki search beyond GitHub's built-in wiki search
