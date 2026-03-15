# Manufacturing Downtime Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

An Excel-based analysis of production line downtime for a soft drink bottling operation. Charles calculated line efficiency, identified the top downtime factors using Pareto analysis, and built an operator-by-factor matrix to pinpoint where targeted training would have the most impact.

## Business Problem

A production manager inherited a bottling line with no visibility into what was causing downtime or how efficiently operators were running. Without data-driven insight, the team couldn't prioritize training or maintenance investments.

## Approach

Charles started by calculating batch-level efficiency — comparing actual production time to the standard minimum for each product using VLOOKUP to pull benchmark times from a products reference table. He then aggregated downtime logs by factor and applied a Pareto analysis to find the 20% of factors causing 80% of lost time. Finally, he cross-referenced downtime by operator and factor to create a heat map showing where each operator was losing the most time, using SUMIFS for the aggregation and conditional formatting for visual emphasis.

## Key Results & Insights

- Overall line efficiency was approximately 64%.
- The lowest-performing operator (Mac) ran at 61% efficiency — a clear candidate for targeted coaching.
- The top 5 downtime factors accounted for roughly 80% of total downtime, consistent with the Pareto principle.
- Three of those top 5 factors were operator errors, pointing to training as the highest-leverage intervention.
- Recommendations included standardized machine adjustment training, batch change coaching for specific operators, and a preventative maintenance schedule.

## Technologies Used

- **Excel:** Pivot tables, VLOOKUP, SUMIFS, conditional formatting, combo charts (Pareto), and bar charts for efficiency comparison.

## Challenges & Solutions

The main challenge was structuring the raw downtime logs so they could be cross-referenced with both the productivity data and the operator assignments. Charles used VLOOKUP to map each downtime entry back to its operator, then SUMIFS to build the operator-by-factor matrix — a practical exercise in joining data across related tables without a database.

## Links

- **GitHub:** https://github.com/cdcoonce/Manufacturing_Downtime_Analysis

## Skills Demonstrated

Spreadsheet & Business Analysis, Data Visualization & Dashboards
