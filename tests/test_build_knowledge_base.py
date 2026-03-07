"""Tests for scripts/build_knowledge_base.py."""

import json
import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from build_knowledge_base import (
    build,
    extract_sections,
    load_all_projects,
    load_bio,
    load_project,
    load_skills,
    load_testimonials,
    parse_classification,
    parse_links,
    parse_skills_demonstrated,
    parse_technologies,
)

CONTEXT_DIR = Path(__file__).resolve().parent.parent / "WebContent" / "context"


# --- Unit tests for pure parsing functions ---


class TestExtractSections:
    def test_splits_on_h2_headings(self):
        text = "# Title\n\nIntro\n\n## First\n\nBody one\n\n## Second\n\nBody two\n"
        sections = extract_sections(text)
        assert "first" in sections
        assert "second" in sections
        assert "Body one" in sections["first"]
        assert "Body two" in sections["second"]

    def test_empty_text_returns_empty_dict(self):
        assert extract_sections("") == {}

    def test_no_h2_headings_returns_empty_dict(self):
        assert extract_sections("# Only H1\n\nSome text") == {}

    def test_multiline_section_body(self):
        text = "## Section\n\nLine 1\nLine 2\nLine 3\n"
        sections = extract_sections(text)
        assert "Line 1" in sections["section"]
        assert "Line 3" in sections["section"]


class TestParseClassification:
    def test_parses_all_fields(self):
        text = (
            "- **Type:** Independent\n"
            "- **Status:** Complete\n"
            "- **Featured:** Yes\n"
        )
        result = parse_classification(text)
        assert result["type"] == "Independent"
        assert result["status"] == "Complete"
        assert result["featured"] is True

    def test_featured_no(self):
        text = "- **Featured:** No\n"
        result = parse_classification(text)
        assert result["featured"] is False

    def test_empty_text(self):
        assert parse_classification("") == {}


class TestParseLinks:
    def test_extracts_github_url(self):
        text = "- **GitHub:** https://github.com/cdcoonce/repo-name\n"
        assert parse_links(text) == "https://github.com/cdcoonce/repo-name"

    def test_no_url_returns_empty(self):
        assert parse_links("No links here") == ""


class TestParseTechnologies:
    def test_extracts_list_items(self):
        text = (
            "- **Data pipeline:** Python, GeoPandas\n"
            "- **Visualization:** Matplotlib\n"
        )
        result = parse_technologies(text)
        assert len(result) == 2
        assert "**Data pipeline:** Python, GeoPandas" in result[0]

    def test_empty_text(self):
        assert parse_technologies("") == []


class TestParseSkillsDemonstrated:
    def test_comma_separated(self):
        text = "Data Engineering & Pipelines, Machine Learning, DevOps & Tooling"
        result = parse_skills_demonstrated(text)
        assert len(result) == 3
        assert result[0] == "Data Engineering & Pipelines"

    def test_empty_text(self):
        assert parse_skills_demonstrated("") == []


# --- Integration tests against real context files ---


class TestLoadBio:
    def test_loads_person_name(self):
        person = load_bio()
        assert person["name"] == "Charles Coonce"

    def test_has_bio_text(self):
        person = load_bio()
        assert "Data Engineer" in person["bio"]

    def test_has_contact_info(self):
        person = load_bio()
        assert "charleslikesdata.com" in person.get("website", "")
        assert "charles.coonce@gmail.com" in person.get("email", "")
        assert "linkedin" in person.get("linkedin", "").lower()
        assert "github" in person.get("github", "").lower()

    def test_has_career_journey(self):
        person = load_bio()
        assert len(person["career_journey"]) > 0

    def test_has_education(self):
        person = load_bio()
        assert len(person["education"]) > 0


class TestLoadSkills:
    def test_returns_9_categories(self):
        skills = load_skills()
        assert len(skills) == 9

    def test_each_category_has_name_and_narrative(self):
        skills = load_skills()
        for skill in skills:
            assert "category" in skill
            assert "narrative" in skill
            assert len(skill["narrative"]) > 0

    def test_categories_have_tools(self):
        skills = load_skills()
        with_tools = [s for s in skills if "tools" in s]
        assert len(with_tools) >= 8  # Most categories have tools


class TestLoadProject:
    def test_featured_project(self):
        filepath = CONTEXT_DIR / "housing-affordability.md"
        project = load_project(filepath)
        assert project["title"] == "Housing Affordability & Commute Trade-Off Analysis"
        assert project["type"] == "Capstone Project — Arizona State University"
        assert project["status"] == "Complete"
        assert project["featured"] is True
        assert len(project["summary"]) > 0
        assert len(project["technologies"]) > 0
        assert "github.com" in project["url"]
        assert len(project["skills_demonstrated"]) > 0

    def test_in_progress_project(self):
        filepath = CONTEXT_DIR / "synthetic-signal-observatory.md"
        project = load_project(filepath)
        assert project["status"] == "In Progress"
        assert project["featured"] is False

    def test_project_without_challenges(self):
        filepath = CONTEXT_DIR / "baby-names.md"
        project = load_project(filepath)
        assert "challenges" not in project

    def test_project_with_challenges(self):
        filepath = CONTEXT_DIR / "housing-affordability.md"
        project = load_project(filepath)
        assert "challenges" in project
        assert len(project["challenges"]) > 0


class TestLoadAllProjects:
    def test_returns_21_projects(self):
        projects = load_all_projects()
        assert len(projects) == 21

    def test_4_featured_projects(self):
        projects = load_all_projects()
        featured = [p for p in projects if p["featured"]]
        assert len(featured) == 4

    def test_1_in_progress_project(self):
        projects = load_all_projects()
        in_progress = [p for p in projects if p["status"] == "In Progress"]
        assert len(in_progress) == 1


class TestLoadTestimonials:
    def test_returns_7_testimonials(self):
        testimonials = load_testimonials()
        assert len(testimonials) == 7

    def test_each_testimonial_has_required_fields(self):
        testimonials = load_testimonials()
        for t in testimonials:
            assert "author" in t
            assert "title" in t
            assert "company" in t
            assert "quote" in t
            assert len(t["quote"]) > 0

    def test_first_testimonial_is_aaron_wallen(self):
        testimonials = load_testimonials()
        assert testimonials[0]["author"] == "Aaron Wallen"
        assert testimonials[0]["company"] == "One America Financial"


class TestBuild:
    def test_full_build_structure(self):
        kb = build()
        assert "person" in kb
        assert "skills" in kb
        assert "projects" in kb
        assert "testimonials" in kb

    def test_full_build_counts(self):
        kb = build()
        assert kb["person"]["name"] == "Charles Coonce"
        assert len(kb["skills"]) == 9
        assert len(kb["projects"]) == 21
        assert isinstance(kb["testimonials"], list)

    def test_full_build_is_json_serializable(self):
        kb = build()
        # Should not raise
        json.dumps(kb, ensure_ascii=False)
