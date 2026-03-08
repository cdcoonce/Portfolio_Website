# NYC Collision Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

An Excel-based analysis of NYC vehicular collision data identifying seasonal patterns, high-risk time periods, and contributing factors. Charles used pivot tables, heatmaps with conditional formatting, and custom calculated columns to produce actionable insights for road safety improvement.

## Business Problem

New York City experiences thousands of vehicular collisions annually, but not all times, locations, and causes carry equal risk. Traffic safety planners need to understand when collisions peak (by month, day, and hour), what the most dangerous contributing factors are, and which of those factors are most likely to result in injury or death — so they can allocate enforcement and infrastructure resources effectively.

## Approach

Charles prepared the data by extracting weekday and hour values from the date and time columns using WEEKDAY and HOUR functions. He created a calculated column to enable percentage computations for contributing factor analysis. He then built three analytical views: a time-series line chart comparing monthly collision trends across 2021, 2022, and 2023; a heatmap using conditional formatting to visualize collision density by day of week and hour; and a contributing factors analysis using pivot tables and data bars to rank the most dangerous causes.

## Key Results & Insights

- Notable increases in collisions occurred in warmer months, particularly between February and June, with a general downward trend from June through December.
- Rush hours (2 PM – 6 PM) on weekdays showed the highest collision density, while late night and early morning hours had the lowest.
- Weekends between 12 AM and 1 AM showed elevated collision numbers compared to the same hours on weekdays.
- The top 3 contributing factors were driver inattention/distraction, unspecified causes, and failure to yield right-of-way.
- More than 60% of "failure to yield" collisions resulted in injury or death, making it the most dangerous specific factor.
- Nearly 30% of top contributing factors were classified as "unspecified," suggesting a data quality issue that limits more precise analysis.

## Technologies Used

- **Excel:** Pivot tables, WEEKDAY function, HOUR function, conditional formatting (heatmaps), calculated columns, data bars, line charts

## Links

- **GitHub:** https://github.com/cdcoonce/NYC_Collision_Analysis

## Skills Demonstrated

Spreadsheet & Business Analysis, Data Visualization & Dashboards
