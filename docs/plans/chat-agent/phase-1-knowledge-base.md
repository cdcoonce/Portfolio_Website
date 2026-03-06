# Phase 1: Build Knowledge Base from Context Files

## Goal

Build a Python script that reads the markdown files in `WebContent/context/` and compiles them into `lambda/knowledge_base.json` for the Lambda function's system prompt.

**Workflow for updates:** Edit markdown files in `WebContent/context/` → run the build script → regenerated JSON is ready for Lambda deployment.

## Prerequisites

- None — this is the first phase.
- The context files already exist in `WebContent/context/`.

## Context Directory (Already Created)

All files are flat in `WebContent/context/` — no subdirectories.

```text
WebContent/context/
  ├── bio.md                          Person bio, career, education, contact
  ├── skills.md                       Skills by category with narrative
  ├── airbnb-listing.md               Project (Guided Coursework)
  ├── ames-housing.md                 Project (Academic) — not on site yet
  ├── baby-names.md                   Project (Guided Coursework)
  ├── data-archive.md                 Project (Independent)
  ├── electricity-consumption.md      Project (Guided Coursework)
  ├── energy-analytics-pipeline.md    Project (Independent) — not on site yet
  ├── global-co2-emissions.md         Project (Guided Coursework)
  ├── housing-affordability.md        Project (Independent, Featured)
  ├── manufacturing-downtime.md       Project (Guided Coursework, Featured)
  ├── motor-vehicle-thefts.md         Project (Guided Coursework)
  ├── national-parks-analysis.md      Project (Independent)
  ├── national-parks-dashboard.md     Project (Independent, Featured)
  ├── nyc-collision.md                Project (Guided Coursework)
  ├── portfolio-website.md            Project (Independent)
  ├── renewable-asset-pipeline.md     Project (Independent) — not on site yet
  ├── restaurant-sales.md             Project (Guided Coursework)
  ├── sleep-deprivation.md            Project (Guided Coursework)
  ├── spaceship-titanic.md            Project (Academic)
  ├── synthetic-signal-observatory.md Project (Independent, In Progress) — not on site yet
  ├── wine-quality.md                 Project (Academic, Featured)
  └── world-happiness.md              Project (Independent)
```

**Total:** 2 non-project files (`bio.md`, `skills.md`) + 21 project files (4 featured, 1 in-progress).

Note: There is no `testimonials.md`. The build script handles this gracefully — testimonials can be added later.

---

## File Formats (As They Exist)

### bio.md

Pure markdown with headings — no YAML frontmatter.

```markdown
# Bio

## Who Is Charles Coonce?
<paragraph — used as primary bio>

## Career Journey
<paragraphs>

## Education
<paragraphs>

## Professional Experience
### Company — Role (dates)
<paragraphs>

## What Sets Charles Apart
<paragraph>

## Connect with Charles
- **Portfolio:** [url](url)
- **Email:** email
- **LinkedIn:** [url](url)
- **GitHub:** [url](url)
```

### skills.md

Narrative markdown with `##` category headings. Each category has a description paragraph, a `**Tools & Technologies:**` line, and a `**Demonstrated in:**` line, separated by `---` horizontal rules.

```markdown
# Skills Overview

## Data Engineering & Pipelines
<narrative paragraph>

**Tools & Technologies:** Dagster, dbt, Polars, Snowflake, ...

**Demonstrated in:** Housing Affordability, Energy Analytics Pipeline, ...

---

## Statistical Analysis & Modeling
...
```

**9 categories:** Data Engineering & Pipelines, Statistical Analysis & Modeling, Machine Learning, Data Visualization & Dashboards, SQL & Database Analytics, Spreadsheet & Business Analysis, Data Wrangling & ETL, Web Development, DevOps & Tooling.

### Project Files

All 21 project files use a `## Classification` section with markdown bold list items for metadata. The implementing agent may optionally convert these to YAML frontmatter for cleaner parsing — both formats should be supported by the build script.

**Current format (as written):**

```markdown
# Project Title

## Classification

- **Type:** Academic | Independent | Guided Coursework
- **Status:** Complete | In Progress
- **Featured:** Yes | No

## Summary
<paragraph>

## Business Problem
<paragraph>

## Approach
<paragraphs>

## Key Results & Insights
<bullet points>

## Technologies Used
- **Category:** tool1, tool2

## Challenges & Solutions        ← optional, ~9 files have this
<paragraphs>

## Links
- **GitHub:** https://github.com/cdcoonce/...

## Skills Demonstrated
Skill A, Skill B, Skill C
```

**Optional YAML frontmatter alternative (recommended if refactoring):**

If converting project files to use frontmatter, the structured metadata moves to the top and the `## Classification` and `## Links` sections are removed:

```markdown
---
title: Project Title
type: Academic
status: Complete
featured: true
url: https://github.com/cdcoonce/repo-name
skills_demonstrated:
  - Data Engineering & Pipelines
  - Statistical Analysis & Modeling
---

## Summary
<paragraph>

## Business Problem
<paragraph>

## Approach
...
```

The build script should support both formats: if frontmatter exists, use it; otherwise fall back to parsing `## Classification` and `## Links` sections.

---

## File to Create

### `scripts/build_knowledge_base.py`

This script reads all markdown files from `WebContent/context/`, parses them by `##` heading sections, and writes `lambda/knowledge_base.json`.

```python
"""Build lambda/knowledge_base.json from WebContent/context/ markdown files.

Usage:
    python scripts/build_knowledge_base.py

Reads markdown files from WebContent/context/ and compiles them into
a single JSON knowledge base for the Lambda function.
"""

import json
import re
from pathlib import Path


CONTEXT_DIR = Path("WebContent/context")
OUTPUT_FILE = Path("lambda/knowledge_base.json")

# These files are not projects — handle them separately
NON_PROJECT_FILES = {"bio.md", "skills.md", "testimonials.md"}


def extract_sections(text: str) -> dict[str, str]:
    """Split markdown into a dict keyed by ## heading.

    Parameters
    ----------
    text : str
        Full markdown file content.

    Returns
    -------
    dict[str, str]
        Mapping from heading text (lowercase) to section body.
    """
    sections = {}
    current_heading = None
    current_lines = []

    for line in text.split("\n"):
        heading_match = re.match(r"^##\s+(.+)$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip().lower()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def parse_classification(section_text: str) -> dict:
    """Parse the Classification section into structured fields.

    Parameters
    ----------
    section_text : str
        The body text under ## Classification.

    Returns
    -------
    dict
        Keys: type, status, featured.
    """
    result = {}
    for line in section_text.split("\n"):
        type_match = re.match(r".*\*\*Type:\*\*\s*(.+)", line)
        if type_match:
            result["type"] = type_match.group(1).strip()
        status_match = re.match(r".*\*\*Status:\*\*\s*(.+)", line)
        if status_match:
            result["status"] = status_match.group(1).strip()
        featured_match = re.match(r".*\*\*Featured:\*\*\s*(.+)", line)
        if featured_match:
            result["featured"] = featured_match.group(1).strip().lower() == "yes"
    return result


def parse_links(section_text: str) -> str:
    """Extract the GitHub URL from the Links section.

    Parameters
    ----------
    section_text : str
        The body text under ## Links.

    Returns
    -------
    str
        The URL, or empty string if not found.
    """
    match = re.search(r"https?://\S+", section_text)
    return match.group(0) if match else ""


def parse_technologies(section_text: str) -> list[str]:
    """Extract technology entries from the Technologies Used section.

    Parameters
    ----------
    section_text : str
        The body text under ## Technologies Used.

    Returns
    -------
    list[str]
        Each line item (e.g., "Data pipeline: Python, GeoPandas, Polars").
    """
    techs = []
    for line in section_text.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            techs.append(line[2:].strip())
    return techs


def parse_skills_demonstrated(section_text: str) -> list[str]:
    """Parse the Skills Demonstrated comma-separated list.

    Parameters
    ----------
    section_text : str
        The body text under ## Skills Demonstrated.

    Returns
    -------
    list[str]
        Skill category names.
    """
    text = section_text.strip()
    if not text:
        return []
    return [s.strip() for s in text.split(",")]


def load_bio() -> dict:
    """Load person info from bio.md.

    Parses ## headings into structured fields and extracts
    contact links from the Connect with Charles section.
    """
    text = (CONTEXT_DIR / "bio.md").read_text()
    sections = extract_sections(text)

    # Extract contact links
    contact = {}
    connect_text = sections.get("connect with charles", "")
    for line in connect_text.split("\n"):
        if "portfolio" in line.lower():
            match = re.search(r"\((.+?)\)", line)
            if match:
                contact["website"] = match.group(1)
        elif "email" in line.lower():
            match = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", line)
            if match:
                contact["email"] = match.group(0)
        elif "linkedin" in line.lower():
            match = re.search(r"\((.+?)\)", line)
            if match:
                contact["linkedin"] = match.group(1)
        elif "github" in line.lower():
            match = re.search(r"\((.+?)\)", line)
            if match:
                contact["github"] = match.group(1)

    return {
        "name": "Charles Coonce",
        "title": "Data Engineer I at Clearway Energy Group",
        "bio": sections.get("who is charles coonce?", ""),
        "career_journey": sections.get("career journey", ""),
        "education": sections.get("education", ""),
        "professional_experience": sections.get("professional experience", ""),
        "what_sets_apart": sections.get("what sets charles apart", ""),
        **contact,
    }


def load_skills() -> list[dict]:
    """Load skills from skills.md as a list of skill categories.

    Each category has a name, narrative description, tools list,
    and demonstrated_in list.
    """
    text = (CONTEXT_DIR / "skills.md").read_text()
    sections = extract_sections(text)

    categories = []
    for heading, body in sections.items():
        if not body.strip():
            continue

        tools_match = re.search(
            r"\*\*Tools & Technologies:\*\*\s*(.+)", body
        )
        demo_match = re.search(r"\*\*Demonstrated in:\*\*\s*(.+)", body)

        # Narrative is everything before the **Tools** line
        narrative = body
        if tools_match:
            narrative = body[: tools_match.start()].strip()

        category = {
            "category": heading.title(),
            "narrative": narrative,
        }
        if tools_match:
            category["tools"] = [
                t.strip() for t in tools_match.group(1).split(",")
            ]
        if demo_match:
            category["demonstrated_in"] = [
                d.strip() for d in demo_match.group(1).split(",")
            ]
        categories.append(category)

    return categories


def load_project(filepath: Path) -> dict:
    """Load a single project markdown file.

    Parameters
    ----------
    filepath : Path
        Path to the project .md file.

    Returns
    -------
    dict
        Structured project data with all available sections.
    """
    text = filepath.read_text()

    # Extract title from # heading
    title_match = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem

    sections = extract_sections(text)
    classification = parse_classification(
        sections.get("classification", "")
    )

    project = {
        "title": title,
        "type": classification.get("type", ""),
        "status": classification.get("status", "Complete"),
        "featured": classification.get("featured", False),
        "summary": sections.get("summary", ""),
        "business_problem": sections.get("business problem", ""),
        "approach": sections.get("approach", ""),
        "key_results": sections.get("key results & insights", ""),
        "technologies": parse_technologies(
            sections.get("technologies used", "")
        ),
        "url": parse_links(sections.get("links", "")),
        "skills_demonstrated": parse_skills_demonstrated(
            sections.get("skills demonstrated", "")
        ),
    }

    # Optional section
    challenges = sections.get("challenges & solutions", "")
    if challenges:
        project["challenges"] = challenges

    return project


def load_all_projects() -> list[dict]:
    """Load all project files (any .md not in NON_PROJECT_FILES)."""
    projects = []
    for md_file in sorted(CONTEXT_DIR.glob("*.md")):
        if md_file.name in NON_PROJECT_FILES:
            continue
        projects.append(load_project(md_file))
    return projects


def load_testimonials() -> list[dict]:
    """Load testimonials if testimonials.md exists, else return []."""
    testimonials_path = CONTEXT_DIR / "testimonials.md"
    if not testimonials_path.exists():
        return []

    text = testimonials_path.read_text()
    text = re.sub(r"^#\s+.*\n+", "", text)

    testimonials = []
    blocks = re.split(r"\n---\n", text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        header_match = re.match(
            r"\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\n\n?(.*)",
            block,
            re.DOTALL,
        )
        if header_match:
            testimonials.append(
                {
                    "author": header_match.group(1).strip(),
                    "title": header_match.group(2).strip(),
                    "company": header_match.group(3).strip(),
                    "quote": header_match.group(4).strip(),
                }
            )

    return testimonials


def build() -> dict:
    """Build the complete knowledge base.

    Returns
    -------
    dict
        The assembled knowledge base ready for JSON serialization.
    """
    return {
        "person": load_bio(),
        "skills": load_skills(),
        "projects": load_all_projects(),
        "testimonials": load_testimonials(),
    }


def main():
    """Build and write the knowledge base JSON file."""
    kb = build()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(kb, indent=2, ensure_ascii=False) + "\n"
    )

    featured = sum(1 for p in kb["projects"] if p["featured"])
    in_progress = sum(
        1 for p in kb["projects"] if p["status"] == "In Progress"
    )
    print(f"Knowledge base written to {OUTPUT_FILE}")
    print(f"  Person: {kb['person']['name']}")
    print(f"  Skills: {len(kb['skills'])} categories")
    print(f"  Projects: {len(kb['projects'])} total, {featured} featured, "
          f"{in_progress} in-progress")
    print(f"  Testimonials: {len(kb['testimonials'])}")


if __name__ == "__main__":
    main()
```

---

## Running the Build

```bash
mkdir -p lambda scripts
python scripts/build_knowledge_base.py
```

Expected output:

```text
Knowledge base written to lambda/knowledge_base.json
  Person: Charles Coonce
  Skills: 9 categories
  Projects: 21 total, 4 featured, 1 in-progress
  Testimonials: 0
```

## Validation

```bash
python3 -c "
import json
kb = json.load(open('lambda/knowledge_base.json'))
assert 'person' in kb, 'Missing person section'
assert 'skills' in kb, 'Missing skills section'
assert len(kb['projects']) == 21, f'Expected 21 projects, got {len(kb[\"projects\"])}'
assert sum(1 for p in kb['projects'] if p['featured']) == 4, (
    f'Expected 4 featured, got {sum(1 for p in kb[\"projects\"] if p[\"featured\"])}'
)
assert len(kb['skills']) == 9, f'Expected 9 skill categories, got {len(kb[\"skills\"])}'
assert kb['person']['name'] == 'Charles Coonce'
print('Knowledge base validation passed')
"
```

## Updating the Knowledge Base

1. **Add a new project:** Create a new `.md` file in `WebContent/context/` following the project template
2. **Enrich a project:** Add detail to any section in an existing file
3. **Update bio:** Edit `WebContent/context/bio.md`
4. **Add/remove skills:** Edit `WebContent/context/skills.md`
5. **Add testimonials:** Create `WebContent/context/testimonials.md` (format below)
6. **Regenerate:** Run `python scripts/build_knowledge_base.py`

### Testimonials Format (if added later)

```markdown
# Testimonials

**Author Name** | Job Title | Company

Quote text here.

---

**Next Author** | Title | Company

Next quote.
```

## JSON Output Schema

```json
{
  "person": {
    "name": "Charles Coonce",
    "title": "Data Engineer I at Clearway Energy Group",
    "bio": "paragraph from 'Who Is Charles Coonce?' section",
    "career_journey": "text from 'Career Journey' section",
    "education": "text from 'Education' section",
    "professional_experience": "text from 'Professional Experience' section",
    "what_sets_apart": "text from 'What Sets Charles Apart' section",
    "website": "url",
    "email": "email",
    "linkedin": "url",
    "github": "url"
  },
  "skills": [
    {
      "category": "Category Name",
      "narrative": "description paragraph",
      "tools": ["tool1", "tool2"],
      "demonstrated_in": ["Project A", "Project B"]
    }
  ],
  "projects": [
    {
      "title": "Project Title",
      "type": "Academic | Independent | Guided Coursework",
      "status": "Complete | In Progress",
      "featured": true,
      "summary": "paragraph",
      "business_problem": "paragraph",
      "approach": "paragraphs",
      "key_results": "bullet points as text",
      "technologies": ["**Category:** tool1, tool2"],
      "url": "github url",
      "skills_demonstrated": ["Skill A", "Skill B"],
      "challenges": "paragraphs (optional, only if section exists)"
    }
  ],
  "testimonials": []
}
```

## Output

After this phase is complete:

- `scripts/build_knowledge_base.py` exists and runs successfully
- `lambda/knowledge_base.json` is generated with 21 projects, 9 skill categories, and full bio data
- Ready for Phase 2 (Lambda function) and Phase 4 (HTML/CSS)
