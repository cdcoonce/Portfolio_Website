# Electricity Consumption Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

An exploratory data analysis of seasonal electricity consumption patterns for Morocco's National Power Co. Charles analyzed hourly power data across three zones to identify peak load periods by hour and day, producing visualizations that could inform strategic infrastructure investments to prevent outages.

## Business Problem

Electricity grids need to anticipate demand surges to prevent outages. Morocco's National Power Co. needed to understand when consumption peaks occur — by hour, day of week, and season — so they could make informed decisions about capacity investments and demand management strategies. Without clear visibility into these patterns, the utility risked underinvesting in infrastructure during critical periods.

## Approach

Charles worked with a CSV dataset containing timestamped power consumption readings for three zones. He derived additional features — total consumption, hour of day, and day of week — from the raw timestamps. He then resampled the data to hourly frequency to create a stacked area chart showing consumption by zone over January 2017, and built a heatmap of average total consumption by day of week and hour of day to visually identify peak periods.

## Key Results & Insights

- Consumption fluctuates significantly over the course of the day, with identifiable peak periods visible in the hourly area charts.
- The heatmap revealed specific days and hours with consistently higher average consumption, suggesting targeted windows for investment in capacity or demand management.
- Zone-level breakdowns showed how each zone contributes to overall load at different times, providing more granular insight for operational planning.

## Technologies Used

- **Data processing:** Python, Pandas
- **Visualization:** Seaborn (heatmaps), Matplotlib (area charts)
- **Environment:** Jupyter Notebook, uv

## Links

- **GitHub:** https://github.com/cdcoonce/Electricity_Consumption_Analysis

## Skills Demonstrated

Data Wrangling & ETL, Data Visualization & Dashboards
