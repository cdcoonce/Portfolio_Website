# Phase 2: Add Date Fields to Context Markdown Files

## Goal

Add `- **Date:** Mon YYYY` to the Classification section of all 21 project context files.

## Files

All 21 `.md` files in `WebContent/context/` (excluding bio.md, skills.md, testimonials.md).

## Change Pattern

Insert `- **Date:**` as the last line in each Classification section, after `- **Featured:**`:

```markdown
## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Jan 2025
```

All projects use a single `Mon YYYY` date sourced from the GitHub repo creation date. See the date reference table in [plan.md](plan.md) for each project's date.

## Verify

```bash
uv run pytest tests/test_build_knowledge_base.py
uv run python scripts/build_knowledge_base.py
```

Inspect the JSON output to confirm every project includes `date` and `date_sort` fields.
