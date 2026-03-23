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

### Daily Consumption Patterns

- **Peak consumption occurs in the evening hours (roughly 6 PM – 10 PM)**, driven by residential demand as people return home — the stacked area chart made this pattern immediately visible across all three zones for January 2017.
- **A secondary morning peak (around 7 AM – 9 AM)** is also evident, consistent with morning routines and commercial activity ramping up simultaneously.
- Late night and early morning hours (midnight – 5 AM) show the lowest consumption across all zones, providing a clear off-peak window for maintenance or demand response programs.

### Day-of-Week Patterns

- **Weekdays show higher and more consistent peak loads** than weekends, reflecting commercial and industrial contributions to the grid during business hours.
- **Sunday shows the lowest average consumption** across the week, while midweek days (Tuesday–Thursday) tend to show the highest sustained loads — a pattern visible in the heatmap's color gradient.
- The day-of-week × hour heatmap identified specific high-risk combinations (e.g., weekday evenings) where infrastructure strain is most likely.

### Zone-Level Contributions

- **Zone 1 contributes the largest share of total consumption** at most hours, suggesting it serves the densest or most industrialized area of the network.
- Zone 3 shows the most pronounced evening spike relative to its baseline, suggesting a primarily residential load profile that would benefit most from evening demand management programs.
- The stacked area chart made zone contributions directly comparable over time, surfacing how the mix of zones shifts throughout the day and across different days of the month.

### Operational Implication

- The heatmap identified that **targeted capacity investment should prioritize weekday evenings**, where demand peaks are both highest and most consistent — a more actionable finding than seasonally averaged data alone would provide.

## Technologies Used

- **Data processing:** Python, Pandas
- **Visualization:** Seaborn (heatmaps), Matplotlib (area charts)
- **Environment:** Jupyter Notebook, uv

## Links

- **GitHub:** https://github.com/cdcoonce/Electricity_Consumption_Analysis

## Skills Demonstrated

Data Wrangling & ETL, Data Visualization & Dashboards
