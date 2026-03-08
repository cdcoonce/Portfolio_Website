# Energy Analytics Pipeline with Dagster

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Jun 2025

## Summary

A modern energy analytics pipeline built with Dagster's software-defined assets, dbt transformations, and DuckDB. The pipeline ingests power trend data, performs analytical transformations, and includes a custom Dagster sensor that sends automated email notifications when key assets are materialized — demonstrating event-driven data architecture.

## Business Problem

Energy companies need reliable, automated pipelines that not only transform data but also notify stakeholders when critical datasets are refreshed. Manual monitoring of pipeline runs is error-prone and doesn't scale. This project demonstrates how to build an observable, event-driven pipeline where data updates automatically trigger downstream actions like notifications.

## Approach

Charles built the pipeline using Dagster's software-defined asset paradigm, where each dbt model is wrapped as a Dagster asset. Power trend data starts as a CSV, gets transformed through dbt models within DuckDB, and is orchestrated through Dagster's job system. He implemented a custom AssetSensorDefinition that listens for the materialization of the `power_trends_by_day` asset and triggers an email notification using a utility function backed by SMTP. Polars is used for data verification and analysis.

## Key Results & Insights

- The pipeline successfully demonstrates the software-defined asset paradigm — dependencies are inferred from asset relationships rather than hard-coded as a DAG.
- The asset sensor reliably triggers email notifications when the daily power trends asset is materialized, showcasing event-driven monitoring.
- The architecture is modular and extensible, with clear separation between asset definitions, jobs, sensors, and utilities.

## Technologies Used

- **Orchestration:** Dagster (software-defined assets, sensors, jobs)
- **Transformation:** dbt
- **Storage:** DuckDB
- **Data processing:** Polars
- **Notifications:** Python SMTP email utility

## Links

- **GitHub:** https://github.com/cdcoonce/Energy_Analytics_Pipeline

## Skills Demonstrated

Data Engineering & Pipelines, SQL & Database Analytics
