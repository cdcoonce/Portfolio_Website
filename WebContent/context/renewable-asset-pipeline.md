# Renewable Asset Performance Pipeline

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Dec 2025

## Summary

A production-grade analytics engineering pipeline for weather-adjusted renewable energy asset performance analysis. Charles built this project to demonstrate the full modern data stack — Dagster orchestration, dlt ingestion, dbt transformations, and Polars processing — all feeding into a DuckDB analytical warehouse that computes capacity factors, weather-normalized metrics, and rolling correlations for wind and solar assets.

## Business Problem

Renewable energy operators need to understand how weather conditions affect the performance of their wind and solar assets. Raw generation data alone doesn't tell the full story — an asset producing less power on a cloudy day isn't underperforming, it's responding to conditions. Operators need weather-adjusted performance metrics, capacity factors, and correlation analysis to distinguish between weather effects and genuine asset issues that need attention.

## Approach

Charles designed and built a multi-stage pipeline. First, mock data generators create two years of realistic hourly weather and generation data for 10 assets (both wind and solar) as Parquet files. A dlt pipeline incrementally loads these into DuckDB. Then dbt models transform the data through staging, intermediate, and mart layers — applying data quality checks, computing daily aggregations, joining weather and generation data, and producing final analytical tables with KPIs. Dagster orchestrates the entire workflow, with a custom sensor that sends email notifications when key assets are materialized.

## Key Results & Insights

### Analytical Outputs

- **Capacity factor computation enables apples-to-apples comparison across assets**: by expressing actual generation as a percentage of theoretical maximum (nameplate × hours), the pipeline separates weather-driven underperformance from genuine asset issues — the core distinction operators need.
- **Rolling 7-day and 30-day Pearson correlations** between weather variables (wind speed, irradiance) and generation output quantify how tightly each asset tracks its expected weather-driven profile, flagging assets where the correlation drops below typical range as candidates for inspection.
- **Weather-normalized performance scores (0–100 scale)** distill complex multi-variable relationships into a single actionable KPI per asset per day — making performance monitoring accessible to non-technical stakeholders without sacrificing analytical rigor.
- The `fact_daily_asset_performance` mart joins weather and generation data to produce a single daily row per asset, enabling straight-forward dashboarding and SQL-based alerting without complex joins at query time.

### Architecture Validation

- **The dlt incremental loading pattern successfully handles two years of hourly data** for 10 assets — roughly 175,000 rows — without full refreshes, demonstrating that incremental ingestion scales cleanly for time-series data.
- **The staging → intermediate → mart dbt pattern enforces a clean separation of concerns**: staging models do nothing but type-cast and rename, intermediate models join and aggregate, and mart models expose final KPIs — making the transformation graph easy to audit and test.
- The end-to-end pipeline (generate → ingest → transform → orchestrate → notify) demonstrates all four layers of the modern data stack in a single, self-contained project.

### Event-Driven Monitoring

- The Dagster sensor fires on key asset materialization, proving that **operational awareness can be built into the pipeline itself** rather than bolted on as a separate monitoring tool — a design pattern directly applicable to production energy data environments.

## Technologies Used

- **Orchestration:** Dagster (software-defined assets, sensors, schedules)
- **Ingestion:** dlt (incremental loading from Parquet to DuckDB)
- **Transformation:** dbt (staging, intermediate, and mart models)
- **Processing:** Polars
- **Storage:** DuckDB
- **Code quality:** Ruff, mypy, pytest, pre-commit hooks

## Challenges & Solutions

Designing the dbt model layers required careful thought about where to place business logic. Charles followed the staging → intermediate → mart pattern, keeping staging models as thin transformations and pushing aggregation and KPI computation into the intermediate and mart layers. Integrating Dagster with dbt also required mapping dbt models to Dagster assets correctly so that the dependency graph and sensor triggers worked as expected.

## Links

- **GitHub:** https://github.com/cdcoonce/Weather_Adjusted_Generation_Analytics

## Skills Demonstrated

Data Engineering & Pipelines, SQL & Database Analytics, DevOps & Tooling
