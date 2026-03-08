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

MONTH_MAP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


def parse_date_to_sort_key(date_str: str) -> str:
    """Convert a 'Mon YYYY' date string to a sortable 'YYYY-MM' key.

    Parameters
    ----------
    date_str : str
        Date string like "Jan 2025" or "Dec 2024".

    Returns
    -------
    str
        Sortable key like "2025-01", or "" if input is empty.
    """
    date_str = date_str.strip()
    if not date_str:
        return ""
    match = re.match(r"([A-Z][a-z]{2})\s+(\d{4})", date_str)
    if not match:
        return ""
    month_abbr, year = match.group(1), match.group(2)
    month_num = MONTH_MAP.get(month_abbr, "")
    if not month_num:
        return ""
    return f"{year}-{month_num}"


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
        Keys: type, status, featured, date, date_sort.
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
        date_match = re.match(r".*\*\*Date:\*\*\s*(.+)", line)
        if date_match:
            date_val = date_match.group(1).strip()
            result["date"] = date_val
            result["date_sort"] = parse_date_to_sort_key(date_val)
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
        "date": classification.get("date", ""),
        "date_sort": classification.get("date_sort", ""),
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
    """Load all project files, sorted newest-first by date."""
    projects = []
    for md_file in sorted(CONTEXT_DIR.glob("*.md")):
        if md_file.name in NON_PROJECT_FILES:
            continue
        projects.append(load_project(md_file))
    projects.sort(key=lambda p: (p.get("date_sort", ""), p["title"]), reverse=True)
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
    print(
        f"  Projects: {len(kb['projects'])} total, {featured} featured, "
        f"{in_progress} in-progress"
    )
    print(f"  Testimonials: {len(kb['testimonials'])}")


if __name__ == "__main__":
    main()
