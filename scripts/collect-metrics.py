#!/usr/bin/env python3
"""Recompute the featured-card KPIs in src/data/metrics.json from source repos.

All four project sources live locally on this Mac (including the private ones),
so this is the only place every number is computable. The script rewrites the
numeric values and the preset/persona lists while preserving the hand-written
copy (eyebrows, headlines, subtitles, tile/bar labels) and the card structure.

Per-project isolation: if a source can't be read, that project keeps its
existing numbers and a loud warning is logged — the collector never writes
garbage over good data.

Usage:
    python scripts/collect-metrics.py            # dry run — print the deltas
    python scripts/collect-metrics.py --write     # rewrite metrics.json
    python scripts/collect-metrics.py --write --commit   # write + git commit/push
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
from pathlib import Path

log = logging.getLogger("collect-metrics")

GITHUB = Path.home() / "Developer" / "GitHub"
VAULT = GITHUB / "my-brain"
CW = GITHUB / "claude-workflow"
OURA = GITHUB / "oura-pipeline"
PORTFOLIO = GITHUB / "PortfolioWebsite"
AFK_HTML = PORTFOLIO / "public" / "afk-cockpit" / "index.html"
METRICS = PORTFOLIO / "src" / "data" / "metrics.json"

# Dirs excluded from the notes/wikilink counts — matches the reference `find`
# so the collector reproduces the established card numbers exactly.
NOTE_EXCLUDE_DIRS = frozenset(
    {".claude", ".obsidian", ".pytest_cache", ".brain", ".git", "templates", "node_modules"}
)
WIKILINK = re.compile(r"\[\[[^\]]*\]\]")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def sh(args: list[str], cwd: Path) -> str:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True).stdout


def iter_notes(base: Path, excludes: frozenset[str] = NOTE_EXCLUDE_DIRS):
    """Markdown files under base, skipping any dir named in `excludes`."""
    for path in base.rglob("*.md"):
        parts = path.relative_to(base).parts[:-1]
        if any(p in excludes for p in parts):
            continue
        yield path


def count_notes(base: Path, excludes: frozenset[str] = NOTE_EXCLUDE_DIRS) -> int:
    return sum(1 for _ in iter_notes(base, excludes))


def count_files(base: Path) -> int:
    return sum(1 for p in base.rglob("*") if p.is_file()) if base.exists() else 0


def fmt_k(n: int) -> str:
    """1660 -> '1.7K' style; below 1000 stays exact."""
    return f"{n / 1000:.1f}K" if n >= 1000 else str(n)


def fmt_comma(n: int) -> str:
    return f"{n:,}"


def set_tile(proj: dict, label: str, value, changes: list, name: str) -> None:
    for tile in proj["tiles"]:
        if tile["label"] == label:
            if str(tile["value"]) != str(value):
                changes.append((name, tile["value"], value))
            tile["value"] = value
            return
    log.warning("  tile label %r not found", label)


def block(proj: dict, kind: str, title: str | None) -> dict | None:
    for b in proj.get("blocks", []):
        if b.get("type") == kind and (title is None or b.get("title") == title):
            return b
    return None


def set_bar(blk: dict, label: str, value: int, changes: list, name: str) -> None:
    for item in blk["items"]:
        if item["label"] == label:
            if item["value"] != value:
                changes.append((name, item["value"], value))
            item["value"] = value
            return
    log.warning("  bar label %r not found", label)


# --------------------------------------------------------------------------- #
# per-project collectors — each mutates `proj` and appends (name, old, new)
# --------------------------------------------------------------------------- #
def collect_my_brain(proj: dict, changes: list) -> None:
    notes = count_notes(VAULT)
    wikilinks = sum(len(WIKILINK.findall(p.read_text(encoding="utf-8", errors="ignore")))
                    for p in iter_notes(VAULT))
    skills_hooks = sum(count_files(VAULT / ".claude" / d) for d in ("commands", "agents", "scripts"))
    domains = sum(1 for p in VAULT.iterdir() if p.is_dir() and not p.name.startswith("."))

    set_tile(proj, "Notes", str(notes), changes, "my-brain notes")
    set_tile(proj, "Wikilinks", fmt_k(wikilinks), changes, "my-brain wikilinks")
    set_tile(proj, "Skills & hooks", str(skills_hooks), changes, "my-brain skills&hooks")
    set_tile(proj, "Domains", str(domains), changes, "my-brain domains")

    bars = block(proj, "bars", "NOTES BY DOMAIN")
    if bars:
        for item in bars["items"]:
            d = VAULT / item["label"]
            if d.is_dir():
                set_bar(bars, item["label"], count_notes(d), changes, f"my-brain/{item['label']}")


def collect_claude_workflow(proj: dict, changes: list) -> None:
    skills = sum(1 for _ in (CW / "core" / "skills").iterdir())
    presets_dir = CW / "presets"
    preset_dirs = sorted(p.name for p in presets_dir.iterdir() if p.is_dir())
    presets = len(preset_dirs)
    tests = sum(len(re.findall(r"def test_", p.read_text(encoding="utf-8", errors="ignore")))
                for p in (CW / "tests").rglob("*.py"))
    commits = int(sh(["git", "rev-list", "--count", "HEAD"], CW).strip())

    set_tile(proj, "Skills", str(skills), changes, "claude-workflow skills")
    set_tile(proj, "Presets", str(presets), changes, "claude-workflow presets")
    set_tile(proj, "Tests", str(tests), changes, "claude-workflow tests")
    set_tile(proj, "Commits", str(commits), changes, "claude-workflow commits")

    base = [p for p in preset_dirs if not p.startswith("persona-")]
    personas = [p[len("persona-"):] for p in preset_dirs if p.startswith("persona-")]
    _set_chips(proj, "PROJECT PRESETS", base, changes, "claude-workflow presets-list")
    _set_chips(proj, "PERSONAS", personas, changes, "claude-workflow personas-list")


def collect_oura(proj: dict, changes: list) -> None:
    models_dir = OURA / "dbt_oura" / "models"
    sources_yml = (models_dir / "sources.yml").read_text(encoding="utf-8", errors="ignore")
    api_sources = len(re.findall(r"^\s{6}- name:", sources_yml, re.MULTILINE))
    dbt_models = sum(1 for _ in models_dir.rglob("*.sql"))
    staging = sum(1 for _ in (models_dir / "staging").rglob("*.sql"))
    marts = sum(1 for _ in (models_dir / "marts").rglob("*.sql"))
    sched = (OURA / "src" / "dagster_project" / "defs" / "schedules.py").read_text(encoding="utf-8", errors="ignore")
    schedules = len(re.findall(r"ScheduleDefinition|build_schedule_from_partitioned_job", sched))
    test_modules = sum(1 for _ in (OURA / "tests").rglob("test_*.py"))

    set_tile(proj, "API sources", str(api_sources), changes, "oura api-sources")
    set_tile(proj, "dbt models", str(dbt_models), changes, "oura dbt-models")
    set_tile(proj, "Schedules", str(schedules), changes, "oura schedules")
    set_tile(proj, "Test modules", str(test_modules), changes, "oura test-modules")

    bars = block(proj, "bars", "PIPELINE STAGES")
    if bars:
        set_bar(bars, "Extract · raw endpoints", api_sources, changes, "oura/extract")
        set_bar(bars, "Stage · dbt views", staging, changes, "oura/stage")
        set_bar(bars, "Marts · fact tables", marts, changes, "oura/marts")


def collect_afk(proj: dict, changes: list) -> None:
    html = AFK_HTML.read_text(encoding="utf-8", errors="ignore")

    # Post afk-cockpit#115 re-grain: header reads "N repos · N runs · N issues · N merged".
    # "issues" (distinct issues attempted) is the count the per-repo bars sum to,
    # so that's what maps to the card's "Attempts" tile — not the raw run count.
    header = re.search(
        r"([\d,]+)\s*repos.{0,20}?[\d,]+\s*runs.{0,20}?([\d,]+)\s*issues.{0,20}?([\d,]+)\s*merged",
        html, re.DOTALL,
    )
    if header:
        repos, issues, merged = (int(g.replace(",", "")) for g in header.groups())
        set_tile(proj, "Merged PRs", str(merged), changes, "afk merged")
        set_tile(proj, "Attempts", fmt_comma(issues), changes, "afk attempts")
        set_tile(proj, "Repos", str(repos), changes, "afk repos")
    else:
        log.warning("  afk header line not found — keeping merged/attempts/repos")

    cost_match = re.search(r'API-equiv \$ / merged PR.{0,80}?\$([\d.,]+)', html, re.DOTALL) or \
        re.search(r'<span class="kpi-value">(\$[\d.,]+)</span>\s*</div>\s*<div class="kpi-label">API-equiv \$ / merged PR', html)
    if not cost_match:
        cost_match = re.search(r'<span class="kpi-value">\$([\d.,]+)</span>[^%]{0,120}?API-equiv \$ / merged PR', html, re.DOTALL)
    if cost_match:
        val = cost_match.group(1)
        cost = val if val.startswith("$") else f"${val}"
        set_tile(proj, "Cost / PR", cost, changes, "afk cost")
    else:
        log.warning("  afk cost tile not found — keeping existing")

    # Per-repo bars: "By repository" rows — <div class="repo-label">NAME</div> ...
    # <div class="repo-total"><strong>NUM</strong> · PCT%</div>. NUM is the total
    # attempted-issues count for that repo (matches the header's "issues" grain).
    bars = block(proj, "bars", "ATTEMPTS BY REPO")
    if bars:
        row = re.compile(
            r'<div class="repo-label">([^<]+)</div>.*?<div class="repo-total"><strong>(\d+)</strong>',
            re.DOTALL,
        )
        found = {name: int(count) for name, count in row.findall(html)}
        for item in bars["items"]:
            if item["label"] in found:
                set_bar(bars, item["label"], found[item["label"]], changes, f"afk/{item['label']}")
            else:
                log.warning("  afk repo %r not matched — keeping existing", item["label"])


def _set_chips(proj: dict, title: str, items: list[str], changes: list, name: str) -> None:
    blk = block(proj, "chips", title)
    if blk is None:
        log.warning("  chips block %r not found", title)
        return
    if blk["items"] != items:
        changes.append((name, blk["items"], items))
    blk["items"] = items


COLLECTORS = {
    "afk": collect_afk,
    "claude-workflow": collect_claude_workflow,
    "oura": collect_oura,
    "my-brain": collect_my_brain,
}


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="rewrite metrics.json (default: dry run)")
    ap.add_argument("--commit", action="store_true", help="git add/commit/push after writing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    data = json.loads(METRICS.read_text(encoding="utf-8"))
    changes: list = []
    for slug, collect in COLLECTORS.items():
        proj = data.get(slug)
        if proj is None:
            log.warning("no metrics entry for %r — skipping", slug)
            continue
        try:
            collect(proj, changes)
        except Exception as exc:  # noqa: BLE001 — isolate per project, keep old data
            log.warning("!! %s collector failed (%s) — keeping existing numbers", slug, exc)

    if not changes:
        log.info("No changes — metrics.json already current.")
        return 0

    log.info("Deltas (%d):", len(changes))
    for name, old, new in changes:
        log.info("  %-28s %s -> %s", name, old, new)

    if args.write:
        METRICS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        log.info("Wrote %s", METRICS)
        if args.commit:
            sh(["git", "add", str(METRICS)], PORTFOLIO)
            sh(["git", "commit", "-m", "chore(metrics): refresh featured-card KPIs"], PORTFOLIO)
            sh(["git", "push"], PORTFOLIO)
            log.info("Committed + pushed.")
    else:
        log.info("(dry run — pass --write to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
