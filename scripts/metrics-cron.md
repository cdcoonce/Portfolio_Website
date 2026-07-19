# Auto-refreshing the featured-card KPIs

The four featured "cockpit" cards on the Overview tab render from
[`src/data/metrics.json`](../src/data/metrics.json). Every number in that file
is recomputed from its source repo by
[`scripts/collect-metrics.py`](./collect-metrics.py):

| Card            | Source                               | What's read                                                           |
| --------------- | ------------------------------------ | --------------------------------------------------------------------- |
| afk             | `./afk-cockpit/index.html`           | header stats, cost tile, per-repo attempts (scraped; repo is private) |
| claude-workflow | `~/Developer/GitHub/claude-workflow` | skills, presets, `def test_` count, commits, preset/persona lists     |
| oura            | `~/Developer/GitHub/oura-pipeline`   | API sources, dbt models, schedules, test modules, pipeline stages     |
| the-vault       | `~/Developer/GitHub/the-vault`       | notes, wikilinks, skills+hooks, domains, notes-by-domain              |

Run it by hand anytime:

```bash
python3 scripts/collect-metrics.py            # dry run — print the delta
python3 scripts/collect-metrics.py --write     # rewrite metrics.json
python3 scripts/collect-metrics.py --write --commit   # + git add/commit/push
```

It's **fail-soft per field**: if a source can't be read, that number keeps its
current value and logs a warning — it never writes garbage over good data.

## Weekly schedule (macOS launchd)

> **Activate only after this work is merged to `master`.** Production (GitHub
> Pages) builds from `master`, and the `--commit` step pushes the currently
> checked-out branch. Enabling it on a feature branch commits there and does not
> update the live site.

```bash
# 1. install the agent
cp scripts/com.charleslikesdata.portfolio-metrics.plist ~/Library/LaunchAgents/

# 2. load it (runs Sundays 09:00; RunAtLoad is off, so nothing fires now)
launchctl load ~/Library/LaunchAgents/com.charleslikesdata.portfolio-metrics.plist

# run once now to confirm it works end-to-end:
launchctl start com.charleslikesdata.portfolio-metrics
tail -n 40 /tmp/portfolio-metrics.log
```

Pause / remove:

```bash
launchctl unload ~/Library/LaunchAgents/com.charleslikesdata.portfolio-metrics.plist
rm ~/Library/LaunchAgents/com.charleslikesdata.portfolio-metrics.plist
```

The `--commit` step only ever stages `src/data/metrics.json`, so a scheduled run
is safe even if you have other uncommitted changes in the tree — it won't touch
them. It does push, so make sure `master` has an upstream set.
