# CI-CD-Pipeline

<!-- generated:start -->
## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. Every push to `master` and every pull request targeting `master` triggers the Lint & Test job. On a successful push to `master`, the Deploy job merges the branch into `gh-pages` to publish the site.

### Pipeline Flowchart

```mermaid
flowchart TD
    Push["Push / PR to master"]
    Checkout["Checkout code"]
    NodeSetup["Set up Node.js 20\n+ npm ci"]
    PythonSetup["Set up Python 3.12\n(uv sync)"]
    Playwright["Install Playwright\nbrowsers"]
    Lint["Lint & Format\n(Prettier · Stylelint · ESLint)"]
    JSTests["JS unit tests\n(Jest)"]
    PyTests["Python tests\n(pytest -m not slow)"]
    Check{"All checks pass?"}
    Deploy["Deploy to gh-pages\n(merge master → gh-pages)"]
    Done["Site live on GitHub Pages"]
    Fail["Pipeline fails\n(PR blocked)"]

    Push --> Checkout
    Checkout --> NodeSetup
    Checkout --> PythonSetup
    NodeSetup --> Playwright
    PythonSetup --> Playwright
    Playwright --> Lint
    Lint --> JSTests
    JSTests --> PyTests
    PyTests --> Check
    Check -->|yes + push to master| Deploy
    Check -->|no| Fail
    Deploy --> Done
```

### Branch Strategy

```mermaid
gitGraph
    commit id: "initial"
    branch feature
    checkout feature
    commit id: "feat: work"
    commit id: "fix: review"
    checkout master
    merge feature id: "PR merge"
    commit id: "chore: follow-up"
```

## Trigger Matrix

| Event | Branch | Jobs Triggered |
|---|---|---|
| `push` | `master` | Lint & Test, Deploy |
| `pull_request` | `master` | Lint & Test only |

## Workflow Files

| File | Triggers |
|---|---|
| `.github/workflows/ci-cd.yml` | push, pull_request |
| `.github/workflows/wiki-sync.yml` | push, pull_request |
<!-- generated:end -->
