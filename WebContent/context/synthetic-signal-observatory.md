# Synthetic Signal Observatory

## Classification

- **Type:** Independent
- **Status:** In Progress
- **Featured:** No
- **Date:** Dec 2025

## Summary

A Python-native, deployable, interactive dashboard that continuously generates synthetic signals, persists them locally, runs a lightweight analytics step, and visualizes results with interactive controls. Built with Streamlit, the project demonstrates Charles's ability to create end-to-end data applications with clean architecture and test coverage.

## Business Problem

Data teams often need lightweight, self-contained tools for monitoring and analyzing streaming or continuously generated data. This project serves as a demonstration of how to build a deployable analytics dashboard that handles data generation, persistence, analysis, and visualization in a single application — the kind of internal tool that data teams frequently build for operational monitoring.

## Approach

Charles structured the project with a clear separation of concerns: business logic lives as pure functions in a dedicated package, service and visualization layers handle orchestration and rendering, and the Streamlit app serves as a thin entrypoint. The project includes its own agent rules (AGENTS.md), architecture documentation (ARCHITECTURE.md), and a learnings log to track environment-specific quirks and pitfalls.

## Key Results & Insights

- The dashboard generates, persists, and visualizes synthetic signals in real time with interactive user controls.
- The architecture enforces clean boundaries between business logic, service layer, and UI — making the codebase testable and maintainable.
- The project includes a full pytest suite and is designed for easy deployment.

## Technologies Used

- **Dashboard:** Streamlit
- **Data processing:** Python (pure functions)
- **Testing:** pytest
- **Environment management:** uv

## Links

- **GitHub:** https://github.com/cdcoonce/Synthetic_Signal_Observatory

## Skills Demonstrated

Data Visualization & Dashboards, Data Engineering & Pipelines, DevOps & Tooling
