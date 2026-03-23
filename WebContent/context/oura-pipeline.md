# Oura Ring Health Data Pipeline

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** Yes
- **Date:** Mar 2026

## Summary

A personal ELT pipeline that extracts health and wellness data from an Oura Ring via the Oura API v2, loads it into Snowflake as semi-structured JSON, and transforms it through dbt staging and mart models into analysis-ready tables — all orchestrated by Dagster with daily partitions.

## Business Problem

Wearable health devices generate rich longitudinal data — sleep stages, heart rate, activity levels, readiness scores — but the data is locked behind vendor APIs with no built-in way to combine, transform, or analyze it at scale. Charles needed a reliable, automated pipeline to pull his own health data into a cloud warehouse where it could be modeled, joined across domains, and queried for personal wellness insights.

## Approach

Charles designed a three-stage ELT pipeline. The **extract** stage uses a custom Dagster resource (`OuraAPI`) that authenticates via OAuth2 and pulls data from 13 Oura API v2 endpoints — including sleep, activity, readiness, heart rate, SpO2, stress, resilience, workouts, sessions, and tags. The **load** stage converts JSON responses into Polars DataFrames and writes them to Snowflake's `OURA_RAW` schema as VARIANT columns using a delete-then-insert upsert pattern with temp table batching, making every run idempotent and backfill-safe. The **transform** stage uses dbt Core to read from raw sources, build staging models (`stg_sleep`, `stg_activity`, `stg_readiness`, `stg_heartrate`) that extract and type-cast fields from the VARIANT JSON, and join them into a `fact_daily_wellness` mart — a single daily row combining sleep duration, steps, calories, and readiness score.

Dagster orchestrates all three phases, including dbt runs via `DbtCliResource` with a custom translator that maps dbt models to Dagster asset keys and groups. Each of the 13 endpoints is a partitioned Dagster asset with daily partitions starting from 2024-01-01, enabling selective materialization and backfill through the Dagster UI.

## Key Results & Insights

### Pipeline Architecture

- **Successfully ingests data from 13 Oura API v2 endpoints** on a daily cadence with full idempotency — endpoints include sleep, activity, readiness, heart rate, SpO2, stress, resilience, workouts, sessions, and tags.
- **Four-schema Snowflake warehouse** provides clear separation of concerns: `OURA_RAW` (raw VARIANT JSON), `OURA_STAGING` (typed and renamed columns), `OURA_MARTS` (analysis-ready joined fact tables), and `CONFIG` (OAuth token storage) — a warehouse organization pattern directly applicable to production analytics engineering workflows.
- **Delete-then-insert upsert pattern with temp table batching** makes every pipeline run idempotent and backfill-safe — high-volume endpoints like heart rate required batched inserts rather than row-by-row inserts to avoid timeout failures on large historical loads.

### Data Modeling

- **The `fact_daily_wellness` mart** joins sleep, activity, and readiness data into a single daily row using FULL OUTER JOINs — a deliberate design choice to preserve days where only a subset of endpoints returned data, rather than silently dropping partial days from the mart.
- **dbt staging models** handle all VARIANT extraction using Snowflake's `raw_data:field::type` syntax, type-casting JSON fields into properly typed columns before they reach the mart layer — keeping raw data as an immutable historical record while marts stay clean and queryable.

### Security and Operations

- **OAuth2 tokens stored in Snowflake** (`CONFIG.OAUTH_TOKENS`) with automatic refresh, eliminating local file dependencies that would break the pipeline when run from a different environment.
- **RSA key-pair authentication** secures all Snowflake connections (both Dagster resources and dbt profiles), replacing password-based auth with a more secure and automation-friendly approach.
- **Daily partitions** in Dagster enable targeted backfills and selective materialization through the UI — if the API is unavailable for a day, exactly that partition can be re-run without reprocessing the full history.

### Engineering Challenges Solved

- **DuckDB → Snowflake migration** required rewriting all 13 dbt staging models to use VARIANT extraction syntax and redesigning the load strategy from direct inserts to temp table batching — a practical lesson in how warehouse choice propagates through every layer of the stack.
- The OAuth token management migration from local files to a Snowflake config table eliminated a class of environment-specific credential failures that would have made the pipeline fragile to run on any machine other than the original development box.

## Technologies Used

- **Orchestration:** Dagster (partitioned assets, resource management, scheduling)
- **Transformation:** dbt Core with Snowflake adapter (staging and mart layers)
- **Warehouse:** Snowflake (VARIANT columns, RSA key-pair auth)
- **Data processing:** Polars (DataFrame operations for API response handling)
- **API integration:** Oura API v2 (OAuth2 authentication, 13 endpoints)
- **Testing & CI:** pytest, GitHub Actions
- **Environment management:** uv

## Challenges & Solutions

One of the biggest challenges was migrating from a local DuckDB warehouse to Snowflake. All 13 dbt staging models had to be rewritten to use Snowflake's `raw_data:field::type` VARIANT extraction syntax instead of direct column references. The load strategy also changed — high-volume endpoints like heartrate required temp table batching instead of row-by-row inserts to avoid timeouts. Authentication was redesigned around RSA key-pair auth for Snowflake and OAuth token storage was moved from local files into a Snowflake config table for portability.

## Links

- **GitHub:** https://github.com/cdcoonce/Oura-Pipeline

## Skills Demonstrated

Data Engineering & Pipelines, Data Wrangling & ETL, Cloud Data Warehousing, DevOps & Tooling
