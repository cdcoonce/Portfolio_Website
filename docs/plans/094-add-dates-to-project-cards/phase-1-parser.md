# Phase 1: Knowledge Base Parser — Date Extraction (TDD)

## Goal

Extend the Python parser to extract date fields from project context files and sort projects by date.

## Files

- `tests/test_build_knowledge_base.py` — write failing tests first
- `scripts/build_knowledge_base.py` — implement

## Tests to Add

In `TestParseClassification`:

- `test_parses_date` — input `- **Date:** Jan 2025`, assert `result["date"] == "Jan 2025"` and `result["date_sort"] == "2025-01"`
- `test_missing_date_defaults_empty` — no Date line, assert `result.get("date", "") == ""` and `result.get("date_sort", "") == ""`

## Implementation

1. **Add `MONTH_MAP` dict** at module level:

   ```python
   MONTH_MAP = {
       "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
       "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
       "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
   }
   ```

2. **Add `parse_date_to_sort_key(date_str: str) -> str`** helper:
   - Parses `Mon YYYY` into `YYYY-MM` using `MONTH_MAP`
   - Returns `""` for empty/missing input

3. **Update `parse_classification()`** — add regex for `**Date:**` line, call `parse_date_to_sort_key()`, return both `date` and `date_sort` in result dict

4. **Update `load_project()`** — include `classification.get("date", "")` and `classification.get("date_sort", "")` in project dict

5. **Update `load_all_projects()`** — sort by `date_sort` descending (newest first), then alphabetical title as tiebreaker

## Verify

```bash
uv run pytest tests/test_build_knowledge_base.py
```
