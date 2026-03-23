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

### Architectural Achievements

- **Pure-function business logic layer is fully unit-testable in isolation** — signal generation, analytics, and transformation logic live as standalone Python functions with no Streamlit dependencies, allowing pytest to validate behavior without launching the UI.
- **Clean three-layer separation** (business logic → service layer → Streamlit entrypoint) means any of the three layers can be swapped independently — the signal generator could be replaced with a real data source, or the Streamlit UI replaced with a REST API, without touching the analytics logic.
- The project ships with its own `AGENTS.md` and `ARCHITECTURE.md`, demonstrating that documentation and team onboarding are treated as first-class deliverables rather than afterthoughts.

### Application Capabilities

- **The dashboard continuously generates synthetic signals, persists them to local storage, runs analytics, and updates visualizations** — completing the full "generate → store → analyze → display" loop that mirrors production monitoring tool patterns.
- Interactive controls (signal type, frequency, amplitude parameters) let users explore how different signal characteristics affect the analytics output, making the app educational as well as functional.
- The learnings log captures environment-specific quirks and Streamlit gotchas encountered during development — a practice that shortens onboarding time for future contributors.

### Engineering Standards

- The full pytest suite validates the analytics logic at the function level, providing a safety net for refactoring and demonstrating that data application code can and should be tested even when the UI is built with a rapid prototyping framework like Streamlit.
- The project is structured for easy deployment (Streamlit Cloud or Docker) with `uv`-managed dependencies, meaning reproducibility is built in from the start rather than retrofitted later.

## Technologies Used

- **Dashboard:** Streamlit
- **Data processing:** Python (pure functions)
- **Testing:** pytest
- **Environment management:** uv

## Links

- **GitHub:** https://github.com/cdcoonce/Synthetic_Signal_Observatory

## Skills Demonstrated

Data Visualization & Dashboards, Data Engineering & Pipelines, DevOps & Tooling
