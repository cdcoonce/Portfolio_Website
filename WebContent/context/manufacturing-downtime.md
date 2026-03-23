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

### Line Efficiency

- **Overall line efficiency was approximately 64%**, meaning the bottling operation lost 36% of available production time — a substantial gap from benchmark performance that quantifies the scale of the improvement opportunity.
- **Efficiency varied meaningfully across operators**, ranging from Mac's 61% (the lowest) to higher-performing peers — a spread that points to operator skill and training, not just equipment, as a key driver of production variability.

### Pareto Analysis — Downtime Factors

- **The top 5 downtime factors accounted for roughly 80% of total downtime**, consistent with the Pareto principle — confirming that a targeted intervention on a small set of root causes would address the majority of lost production time.
- **Three of the top 5 factors were operator errors** (not equipment failures or material issues), making targeted training the highest-leverage intervention available — maintenance investments alone would be insufficient.
- The remaining top-5 factors were equipment-related, supporting a two-track action plan: training for human factors, preventative maintenance scheduling for mechanical ones.

### Recommendations

- **Standardized machine adjustment training** for all operators, focused on the specific tasks most frequently coded as operator error in the downtime log.
- **Batch change coaching** for the lowest-performing operators, targeting the changeover procedures where variability was highest.
- **Preventative maintenance schedule** targeting the equipment-side downtime factors before they escalate into longer unplanned stoppages.

### Analytical Takeaway

- This project demonstrates how Excel can answer operational business questions that many organizations assume require specialized manufacturing software — VLOOKUP, SUMIFS, and conditional formatting are sufficient tools for a meaningful Pareto and operator analysis.
- The most important insight was not the efficiency number itself, but the breakdown of _why_ the line was inefficient — without that decomposition, a manager might invest in equipment when the real opportunity is training.

## Technologies Used

- **Excel:** Pivot tables, VLOOKUP, SUMIFS, conditional formatting, combo charts (Pareto), and bar charts for efficiency comparison.

## Challenges & Solutions

The main challenge was structuring the raw downtime logs so they could be cross-referenced with both the productivity data and the operator assignments. Charles used VLOOKUP to map each downtime entry back to its operator, then SUMIFS to build the operator-by-factor matrix — a practical exercise in joining data across related tables without a database.

## Links

- **GitHub:** https://github.com/cdcoonce/Manufacturing_Downtime_Analysis

## Skills Demonstrated

Spreadsheet & Business Analysis, Data Visualization & Dashboards
