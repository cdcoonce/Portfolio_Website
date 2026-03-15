# Phase 5: E2E Tests & Knowledge Base Rebuild

## Goal

Add E2E tests for date display and sorting, add integration tests for the knowledge base, and rebuild the knowledge base JSON.

## Files

- `tests/test_gallery.py` — add date-related E2E tests
- `tests/test_build_knowledge_base.py` — add integration tests
- `lambda/knowledge_base.json` — rebuilt by script

## E2E Tests to Add

In `TestProjectsPage` (tests/test_gallery.py):

- `test_cards_display_date` — every visible `.project-card .project-date` element has non-empty text content
- `test_cards_sorted_newest_first` — collect `data-date` attributes from all visible cards, assert they are in descending order

## Integration Tests to Add

In `TestLoadAllProjects` (tests/test_build_knowledge_base.py):

- `test_all_projects_have_date` — every project from `load_all_projects()` has a non-empty `date` field
- `test_projects_sorted_newest_first` — for each consecutive pair, assert `projects[i]["date_sort"] >= projects[i+1]["date_sort"]`

## Rebuild Knowledge Base

```bash
uv run python scripts/build_knowledge_base.py
```

Inspect output to confirm project dates are present and projects are sorted newest-first.

## Final Verification

```bash
uv run pytest && npm test
```

All tests green confirms the feature is complete end-to-end.
