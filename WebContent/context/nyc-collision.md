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

### Seasonal Patterns

- **Collision rates increased significantly in warmer months**, particularly February through June, then declined from June through December — consistent with increased vehicle activity, cycling traffic, and pedestrian exposure in spring and early summer.
- Multi-year comparison across 2021, 2022, and 2023 showed consistent seasonal patterns, suggesting the February–June peak is a structural feature of NYC collision dynamics, not an outlier year.

### Time-of-Day and Day-of-Week Patterns

- **Rush hours (2 PM – 6 PM) on weekdays showed the highest collision density** — afternoon rush generates higher collision risk than morning rush, likely due to fatigue accumulation across the day combined with peak traffic volume.
- **Late night and early morning hours had the lowest weekday collision counts**, but weekend overnight hours (particularly 12 AM – 1 AM Saturday and Sunday) showed elevated collisions relative to the same hours on weekdays — consistent with alcohol-related driving patterns.

### Contributing Factors and Severity

- **Driver inattention/distraction was the leading cause of collisions**, followed by unspecified causes and failure to yield right-of-way — establishing that behavioral factors dominate over mechanical or infrastructure failures.
- **"Failure to yield" was the most dangerous specific factor**: more than 60% of collisions citing this cause resulted in injury or death, far exceeding the lethality rate of inattention collisions — a finding with direct implications for enforcement prioritization.
- **Nearly 30% of contributing factors were classified as "unspecified"**, indicating a systematic data quality problem in collision reporting that limits the precision of any intervention strategy and highlights an opportunity for improved data collection.

### Analytical Takeaway

- The most actionable finding is the severity differential: enforcement targeting "failure to yield" violations would address the highest-injury-per-incident factor even if it is not the most common cause.
- The seasonal and time-of-day patterns provide a foundation for targeted enforcement scheduling — concentrating resources in February–June afternoons and weekend overnights would address the two highest-risk windows simultaneously.

## Technologies Used

- **Excel:** Pivot tables, WEEKDAY function, HOUR function, conditional formatting (heatmaps), calculated columns, data bars, line charts

## Links

- **GitHub:** https://github.com/cdcoonce/NYC_Collision_Analysis

## Skills Demonstrated

Spreadsheet & Business Analysis, Data Visualization & Dashboards
