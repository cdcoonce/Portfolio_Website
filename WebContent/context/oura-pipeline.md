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

- Successfully ingests data from **13 Oura API v2 endpoints** on a daily cadence with full idempotency
- Snowflake warehouse organized across four schemas: `OURA_RAW` (raw VARIANT tables), `OURA_STAGING` (typed columns), `OURA_MARTS` (joined fact tables), and `CONFIG` (OAuth token storage)
- The `fact_daily_wellness` mart joins sleep, activity, and readiness data into a single daily row using FULL OUTER JOINs to handle days with partial data
- OAuth2 tokens are stored in Snowflake (`CONFIG.OAUTH_TOKENS`) with automatic refresh, eliminating local file dependencies
- RSA key-pair authentication secures all Snowflake connections (both Dagster resources and dbt profiles)
- Daily partitions enable targeted backfills and selective materialization through the Dagster UI

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
