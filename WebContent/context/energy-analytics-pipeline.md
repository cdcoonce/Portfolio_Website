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

### Pipeline Architecture Outcomes

- **Demonstrated that Dagster's software-defined asset paradigm eliminates manual DAG wiring** — dependencies are declared through function inputs and outputs rather than explicit edges, making the pipeline self-documenting and easier to refactor.
- The `power_trends_by_day` asset is the materialization trigger for the downstream sensor, proving that **asset-centric orchestration enables clean separation between computation and reaction** — the sensor has no knowledge of how the asset is computed, only that it has been updated.
- **dbt + DuckDB + Dagster forms a cohesive local analytics stack**: dbt handles the SQL transformation layer, DuckDB provides fast in-process analytics without a server, and Dagster ties them together with observability and scheduling.

### Event-Driven Monitoring

- **The custom `AssetSensorDefinition` fires reliably** on each successful materialization of the daily asset — demonstrating that event-driven stakeholder notification can be implemented without a separate message queue or scheduler.
- The SMTP email notification utility is decoupled from both the sensor and the asset, making it independently testable and reusable — a design decision that reinforces single-responsibility principles in pipeline code.

### Extensibility Demonstration

- The modular structure (assets / jobs / sensors / utilities as separate concerns) means adding a new data source requires only a new asset definition — the sensor and job layers require no modification.
- Polars was used for data verification rather than Pandas, demonstrating comfort with the modern Python data ecosystem beyond the standard Pandas-centric workflow.

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
