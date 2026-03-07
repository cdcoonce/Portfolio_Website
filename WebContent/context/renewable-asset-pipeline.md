# Renewable Asset Performance Pipeline

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No

## Summary

A production-grade analytics engineering pipeline for weather-adjusted renewable energy asset performance analysis. Charles built this project to demonstrate the full modern data stack — Dagster orchestration, dlt ingestion, dbt transformations, and Polars processing — all feeding into a DuckDB analytical warehouse that computes capacity factors, weather-normalized metrics, and rolling correlations for wind and solar assets.

## Business Problem

Renewable energy operators need to understand how weather conditions affect the performance of their wind and solar assets. Raw generation data alone doesn't tell the full story — an asset producing less power on a cloudy day isn't underperforming, it's responding to conditions. Operators need weather-adjusted performance metrics, capacity factors, and correlation analysis to distinguish between weather effects and genuine asset issues that need attention.

## Approach

Charles designed and built a multi-stage pipeline. First, mock data generators create two years of realistic hourly weather and generation data for 10 assets (both wind and solar) as Parquet files. A dlt pipeline incrementally loads these into DuckDB. Then dbt models transform the data through staging, intermediate, and mart layers — applying data quality checks, computing daily aggregations, joining weather and generation data, and producing final analytical tables with KPIs. Dagster orchestrates the entire workflow, with a custom sensor that sends email notifications when key assets are materialized.

## Key Results & Insights

- The pipeline computes capacity factors, weather-adjusted expected generation, and rolling 7-day and 30-day Pearson correlations between weather variables and generation output.
- The mart layer produces two key analytical tables: daily asset performance summaries and weather-normalized performance scores (0–100 scale).
- The Dagster sensor demonstrates event-driven architecture by triggering automated notifications on asset materialization.
- The full pipeline is reproducible and follows modern analytics engineering best practices with clear separation of ingestion, transformation, and orchestration.

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
