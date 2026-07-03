# CI-CD-Pipeline

<!-- generated:start -->
## CI/CD Pipeline

Delivery runs on GitHub Actions across **two branches, two hosts**. `dev` is **live staging** (Cloudflare Pages); `main` is **production** (GitHub Pages). Both build the Astro site (`npm run build` → `dist/`) and publish that output — the only difference is the host and the quality gate in front of it.

### Production Pipeline (`main` → GitHub Pages)

`ci-cd.yml` runs on every push and pull request targeting `main`. The **check** job must pass before the **deploy** job publishes to the `gh-pages` branch (including `CNAME`), which GitHub Pages serves.

```mermaid
flowchart TD
    Push["Push / PR to main"]
    Checkout["Checkout code"]
    NodeSetup["Set up Node.js 22\n+ npm ci"]
    Prettier["Check formatting\n(Prettier)"]
    LintCSS["Lint CSS\n(Stylelint)"]
    LintJS["Lint JS\n(ESLint)"]
    JSTests["JS unit tests\n(Jest)"]
    Build["Build site\n(astro build → dist/)"]
    Check{"push to main?"}
    Deploy["Publish dist/ → gh-pages\n(peaceiris/actions-gh-pages)"]
    Done["Live on GitHub Pages\n(charleslikesdata.com)"]
    PR["PR: checks only, no deploy"]

    Push --> Checkout --> NodeSetup --> Prettier --> LintCSS --> LintJS --> JSTests --> Build --> Check
    Check -->|yes| Deploy --> Done
    Check -->|pull_request| PR
```

### Staging Pipeline (`dev` → Cloudflare Pages)

`deploy-staging.yml` runs on every push to `dev`. It builds the Astro site and deploys `dist/` to the Cloudflare Pages project `charleslikesdata-portfolio` via `wrangler`. The deploy self-skips until the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repo secrets are set, so early pushes don't fail red.

```mermaid
flowchart TD
    DevPush["Push to dev"]
    DevBuild["npm ci + astro build"]
    SecretCheck{"Cloudflare secrets set?"}
    Wrangler["wrangler pages deploy dist\n--project charleslikesdata-portfolio"]
    Staging["Live staging\n(charleslikesdata-portfolio.pages.dev)"]
    Skip["Skip deploy (log + exit 0)"]

    DevPush --> DevBuild --> SecretCheck
    SecretCheck -->|yes| Wrangler --> Staging
    SecretCheck -->|no| Skip
```

### Branch & Promotion Model

Feature work lands on `dev`, which auto-deploys to staging. Once verified, `dev` merges to `main`, which runs the full gate and promotes to production.

```mermaid
gitGraph
    commit id: "init"
    branch dev
    checkout dev
    commit id: "feat: work (→ staging)"
    commit id: "fix: review (→ staging)"
    checkout main
    merge dev id: "promote (→ production)"
```

## Trigger Matrix

| Event | Branch | Workflow | Result |
|---|---|---|---|
| `push` | `main` | `ci-cd.yml` | Lint + Test + Build, then deploy to GitHub Pages |
| `pull_request` | `main` | `ci-cd.yml` | Lint + Test + Build only (no deploy) |
| `push` | `dev` | `deploy-staging.yml` | Build + deploy to Cloudflare Pages (staging) |

## Workflow Files

| File | Trigger | Purpose |
|---|---|---|
| `.github/workflows/ci-cd.yml` | push / PR → `main` | Lint, test, build; deploy production to `gh-pages` |
| `.github/workflows/deploy-staging.yml` | push → `dev` | Build + deploy staging to Cloudflare Pages |
| `.github/workflows/wiki-sync.yml` | push → `main` (relevant paths) | Regenerate and sync this wiki |
<!-- generated:end -->
