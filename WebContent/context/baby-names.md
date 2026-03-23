# Baby Names Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Mar 2025

## Summary

A SQL-driven analysis of U.S. baby name trends from 1980 to 2009, exploring name popularity, decade-over-decade shifts, regional differences, and unique naming patterns. Charles used window functions, CTEs, and set operations to rank names, track popularity changes, and answer stakeholder-driven questions.

## Business Problem

Understanding naming trends has applications in marketing, demographic research, and cultural analysis. This project simulates a scenario where a stakeholder wants to understand how baby name popularity has shifted over three decades, how trends differ across U.S. regions, and which names are uniquely popular or used across genders.

## Approach

Charles structured the analysis around four objectives. First, he tracked popularity changes over time — identifying the overall most popular names, plotting individual name rankings by year using ROW_NUMBER(), and finding the biggest rank jumps between 1980 and 2009. Second, he compared popularity across decades using RANK() with decade groupings. Third, he analyzed regional patterns by joining the names table with a regions reference table and computing top names within each region. Fourth, he explored unique names — finding the most popular androgynous names, the shortest and longest names, and answering a custom stakeholder question about the geographic distribution of a specific name.

## Key Results & Insights

### Decade-Over-Decade Trends

- **Michael and Jessica dominated the 1980s and 1990s** as the top boy and girl names respectively — a cultural consistency across two decades that reflects a generational peak before giving way to new patterns.
- **By the 2000s, Jacob and Emily had risen to the top**, marking a clear generational shift — syllable patterns, cultural influences, and pop culture references all drive decade-scale naming cycles in measurable ways.
- **Names like Aidan and Skylar showed the largest rank jumps from 1980 to 2009**, demonstrating how a name can go from obscurity to national prominence within a single generation — a pattern attributable to a confluence of pop culture moments and social network effects.

### Regional Analysis

- **The South had the largest total number of births** across the 1980–2009 window, giving it an outsized influence on national name rankings — names that trend first in high-birth regions propagate upward in overall rankings more quickly.
- Regional top-name lists revealed distinct preferences beyond just birth volume, pointing to cultural, religious, and demographic variation in naming conventions across U.S. regions.

### Unique Naming Patterns

- **The most popular androgynous names** (used for both genders in measurable quantities) included unexpected entries — names historically gendered one way that cross over in small but statistically visible proportions.
- **Name length varied widely**: the shortest tracked names (2 letters, e.g., Ty, Bo) clustered at low-to-moderate popularity, while the longest (15 letters, e.g., Franciscojavier) appeared in very small volumes — reflecting the trade-off between distinctiveness and ease of use.

### SQL Technique Takeaways

- Window functions (`ROW_NUMBER()`, `RANK()`) enabled per-year and per-decade ranking without subquery duplication — a key advantage over traditional aggregation for temporal analysis.
- CTEs and `UNION` operations allowed multi-step analytic questions to be answered in single, readable queries — a pattern directly applicable to business intelligence reporting workflows.

## Technologies Used

- **SQL:** Window functions (RANK, ROW_NUMBER), CTEs, UNION, JOINs, GROUP BY, HAVING, subqueries, CASE expressions

## Links

- **GitHub:** https://github.com/cdcoonce/Baby_Names_Analysis

## Skills Demonstrated

SQL & Database Analytics
