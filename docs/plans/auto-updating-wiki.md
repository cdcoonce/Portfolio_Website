# Plan: Auto-Updating Wiki System

> Source PRD: https://github.com/cdcoonce/Portfolio_Website/issues/115

## Architectural Decisions

Durable decisions that apply across all phases:

- **Generator contract**: each generator module exports `generate(repo_root: Path) -> str` returning the full Markdown content for its wiki page
- **Marker convention**: script owns `<!-- generated:start -->` … `<!-- generated:end -->` blocks; Claude skill owns `<!-- claude:prose -->` … `<!-- claude:prose:end -->` blocks; the two regions never overlap
- **Wiki location**: `wiki/` at repo root, versioned with code; synced to `{repo}.wiki.git` via CI
- **Generator location**: `scripts/wiki/` — one module per wiki page, plus `orchestrate.py` as entry point
- **ADL exception**: `Architecture-Decision-Log.md` has no `generated` blocks; the orchestrator skips it entirely
- **First-run behaviour**: orchestrator creates files with populated `generated` blocks and empty `claude:prose` markers for pages that have prose sections; pages without prose sections get no `claude:prose` markers
- **CI trigger**: path-filtered push to `master` (`WebContent/js/**`, `WebContent/css/**`, `WebContent/context/**`, `lambda/**`, `__tests__/**`, `tests/**`, `.github/workflows/**`)
- **Sync mechanism**: `wiki-sync.yml` clones `{repo}.wiki.git`, overwrites with `wiki/*.md`, pushes using `GITHUB_TOKEN`
- **Extraction strategy**: regex and line-based parsing — no AST; sufficient for this codebase
- **Special GitHub Wiki files**: `_Sidebar.md` (navigation panel) and `_Footer.md` (page footer) are written directly by the orchestrator, not by individual page generators
- **Changelog source**: `git log --format="%H|%s|%an|%ad" --date=short` parsed with conventional commit regex; no new dependencies (stdlib `subprocess` only)
- **GITHUB_TOKEN permissions**: `wiki-sync.yml` requires `permissions: contents: write` to push to the wiki repo

---

## Phase 1: Generator Foundation

**User stories**: 1, 20, 27

### What to build

Scaffold the `scripts/wiki/` package and implement `orchestrate.py` with the core marker-splice logic. Implement the first page generator, `generate_home.py`, which reads `package.json`, `pyproject.toml`, and `CLAUDE.md` to produce a tech stack table, test command reference, and npm/make script list.

The orchestrator also writes two special GitHub Wiki files on every run:

- **`_Sidebar.md`**: a structured navigation panel listing all wiki pages grouped by topic (Reference, Architecture, Dev Guide). Generated directly by the orchestrator �� not a page generator.
- **`_Footer.md`**: a footer line reading `Last regenerated: {date} · {sha}` that appears at the bottom of every wiki page. Also written by the orchestrator on every run.

Running `python scripts/wiki/orchestrate.py` from the repo root must create `wiki/Home.md`, `wiki/_Sidebar.md`, and `wiki/_Footer.md` with correct structure. The wiki page must be valid Markdown that renders cleanly on GitHub.

Tests cover the orchestrator's splice behaviour: it correctly inserts generated content into a `generated` block, and it leaves an existing `claude:prose` block untouched after a re-run.

### Acceptance criteria

- [ ] `scripts/wiki/__init__.py`, `orchestrate.py`, and `generate_home.py` exist
- [ ] `generate_home.py` produces a tech stack table (language/tool + version/notes), test commands section, and npm/make scripts section
- [ ] `orchestrate.py` splices generator output into `generated` blocks without touching `claude:prose` blocks
- [ ] On first run with no existing `wiki/Home.md`, the file is created with correct marker structure
- [ ] On re-run, a pre-existing `claude:prose` block in `wiki/Home.md` is preserved verbatim
- [ ] `wiki/_Sidebar.md` is created with a grouped navigation list (Reference, Architecture, Dev Guide sections)
- [ ] `wiki/_Footer.md` is created with a last-regenerated timestamp and git SHA
- [ ] `wiki/Home.md` includes links to all other wiki pages (placeholders are fine at this stage)
- [ ] Tests pass: orchestrator splice logic and `generate_home` output validated against real repo root

---

## Phase 2: Table and List Generators (No Diagrams)

**User stories**: 3, 7, 8, 11, 12, 16, 17

### What to build

Add five generators that extract structured content (tables and lists) without Mermaid diagrams:

- **`generate_testing.py`**: reads `__tests__/*.test.js`, `tests/test_*.py`, `jest.config.js`, and `pyproject.toml`; produces a test file inventory table and a pytest marker reference
- **`generate_css.py`**: reads `WebContent/css/style.css` and `mediaqueries.css`; produces a CSS custom properties table and breakpoint reference
- **`generate_knowledge_base.py`**: reads `WebContent/context/*.md`; produces a context file inventory table with name, word count, and inferred topic
- **`generate_contributing.py`**: reads `CLAUDE.md`, `package.json`, `pyproject.toml`, and `Makefile`; produces local setup steps, make targets, and commit convention rules; includes an empty `claude:prose` block for onboarding narrative
- **`generate_frontend_modules.py`** (table portion only — diagram deferred to Phase 3): reads `WebContent/js/*.js`; extracts exports via regex and produces a per-module table of exports and function signatures; Phase 3 will extend this generator to add the Mermaid dependency graph
- **`generate_changelog.py`**: calls `git log --format="%H|%s|%an|%ad" --date=short` via subprocess, parses conventional commit messages, groups entries by type (feat, fix, refactor, etc.), outputs the last 50 commits as a structured Markdown changelog

Orchestrator now produces 7 populated wiki pages plus the Changelog. Each page renders as valid, informative Markdown on GitHub.

### Acceptance criteria

- [ ] All six generators exist and are registered in `orchestrate.py`
- [ ] `Testing.md` contains a test file inventory table and lists all pytest markers from `pyproject.toml`
- [ ] `CSS-Design-System.md` lists all CSS custom properties and both breakpoints (700px, 1250px)
- [ ] `Knowledge-Base.md` lists all 24 context files with word counts
- [ ] `Contributing.md` contains setup steps derived from `CLAUDE.md` and `Makefile`, plus an empty `claude:prose` block
- [ ] `Frontend-Modules.md` contains a module inventory table with exports per module (no diagram yet — placeholder comment marks where Phase 3 will add it)
- [ ] `Changelog.md` groups the last 50 commits by conventional commit type with dates
- [ ] Running the orchestrator from a clean state produces all wiki files with correct marker structure
- [ ] Tests pass for each generator: output contains expected headings, tables, and at least one real data row derived from the repo

---

## Phase 3: Diagram Generators (Mermaid)

**User stories**: 2, 4, 5, 6, 9, 10, 13

### What to build

Add four generators that produce Mermaid diagram blocks alongside their structured content:

- **`generate_architecture.py`**: reads `WebContent/js/*.js`, `index.html`, `projects.html`, and `lambda/`; produces a system component diagram (`graph TD`: browser → JS modules → Lambda → Anthropic API) and a data flow diagram (`graph TD`: user interaction → module → Lambda → response); includes `claude:prose` block for system design narrative
- **`generate_frontend_modules.py`** (diagram portion — completes the generator): adds a module dependency graph (`graph LR`) derived from `import` statements in each JS file, replacing the placeholder comment left in Phase 2
- **`generate_lambda.py`**: reads `lambda/lambda_function.py` and `lambda/requirements.txt`; produces a chat request sequence diagram (`sequenceDiagram`) and a class diagram (`classDiagram`) for ChatAgent and ChatRequest; includes `claude:prose` block for agent design rationale
- **`generate_cicd.py`**: reads `.github/workflows/ci-cd.yml`; produces a pipeline flowchart (`flowchart TD`) and a branch strategy diagram (`gitGraph`)

All 10 wiki pages (excluding ADL) now generate. Every Mermaid block must use a valid diagram type and render on GitHub.

### Acceptance criteria

- [ ] `Architecture.md` contains two Mermaid blocks: system component `graph TD` and data flow `graph TD`
- [ ] `Frontend-Modules.md` now includes a `graph LR` module dependency diagram derived from actual import statements
- [ ] `Lambda-Chat-Agent.md` contains a `sequenceDiagram` and a `classDiagram`; class diagram reflects actual ChatAgent and ChatRequest structure
- [ ] `CI-CD-Pipeline.md` contains a `flowchart TD` pipeline diagram and a `gitGraph` branch diagram
- [ ] `Knowledge-Base.md` contains a `flowchart LR` compile pipeline diagram
- [ ] All Mermaid blocks open with ` ```mermaid ` and close with ` ``` `
- [ ] Running the orchestrator produces all 10 non-ADL wiki files
- [ ] Tests pass: each diagram generator's output contains at least one valid Mermaid code fence with the correct diagram type keyword

---

## Phase 4: CI Sync Workflow

**User stories**: 19, 21, 22

### What to build

Add `.github/workflows/wiki-sync.yml` — a GitHub Actions workflow that:

1. Triggers on push to `master` filtered to source paths (JS, CSS, context, Lambda, tests, workflows)
2. Checks out the repo with full history
3. Sets up Python and uv
4. Runs `uv run python scripts/wiki/orchestrate.py`
5. Clones the GitHub Wiki repo (`{repo}.wiki.git`)
6. Copies all files from `wiki/` into the wiki repo (including `_Sidebar.md`, `_Footer.md`, `Changelog.md`)
7. Commits and pushes using `GITHUB_TOKEN`

The workflow must declare `permissions: contents: write` — without this, `GITHUB_TOKEN` cannot push to the wiki repo and the job fails with a 403.

A push touching any watched path must result in the GitHub Wiki tab updating within the CI run. Doc-only pushes (e.g. touching only `docs/` or `README.md`) must not trigger the workflow.

### Acceptance criteria

- [ ] `wiki-sync.yml` exists with correct `on.push.paths` filter covering all 7 watched path patterns
- [ ] Workflow declares `permissions: contents: write`
- [ ] Workflow uses `GITHUB_TOKEN` — no additional repository secrets required
- [ ] A push that modifies a watched path triggers the workflow and updates the GitHub Wiki tab
- [ ] A push that modifies only `README.md` or `docs/` does not trigger the workflow
- [ ] The workflow commit step uses a consistent commit message (e.g. `chore(wiki): regenerate from {sha}`)
- [ ] Workflow completes without error on a clean push to master

---

## Phase 5: `/update-wiki` Skill, ADL Seed, and README Trim

**User stories**: 14, 15, 23, 24, 25, 26

### What to build

Three deliverables complete the system:

**`/update-wiki` skill** (`.claude/skills/update-wiki/SKILL.md`): Claude Code skill that reads `wiki/*.md`, identifies `claude:prose` blocks, reads relevant source files for context, and rewrites prose in-place without touching `generated` blocks. Supports single-page targeting via argument (`/update-wiki Architecture`). Prompts the user to commit and push on completion. Pages with prose sections: `Home.md`, `Architecture.md`, `Lambda-Chat-Agent.md`, `Contributing.md`, `Architecture-Decision-Log.md`.

**ADL seed** (`wiki/Architecture-Decision-Log.md`): hand-written initial file with ADL entries for the five key decisions — no framework/bundler, Lambda over Edge Functions, native ES modules, uv as Python package manager, mobile-first CSS. Each entry follows the Context → Decision → Consequences format.

**README trim** (manual one-time edit): reduce `README.md` to a 60-second quickstart covering one-line description, local setup, test commands, and a link to the wiki. All depth moves to the wiki.

### Acceptance criteria

- [ ] `.claude/skills/update-wiki/SKILL.md` exists with trigger conditions, behaviour description, and list of prose-bearing pages
- [ ] Running `/update-wiki` rewrites `claude:prose` blocks without modifying `generated` blocks
- [ ] Running `/update-wiki Architecture` updates only `Architecture.md`
- [ ] `wiki/Architecture-Decision-Log.md` exists with at least 5 ADL entries in Context → Decision → Consequences format
- [ ] The ADL file has no `generated` blocks; the orchestrator skips it on re-run
- [ ] `README.md` contains local setup instructions, test commands, and a link to the wiki; does not duplicate wiki content
- [ ] CLAUDE.md updated to include trigger condition for `/update-wiki`
