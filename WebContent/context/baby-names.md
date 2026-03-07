# Baby Names Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No

## Summary

A SQL-driven analysis of U.S. baby name trends from 1980 to 2009, exploring name popularity, decade-over-decade shifts, regional differences, and unique naming patterns. Charles used window functions, CTEs, and set operations to rank names, track popularity changes, and answer stakeholder-driven questions.

## Business Problem

Understanding naming trends has applications in marketing, demographic research, and cultural analysis. This project simulates a scenario where a stakeholder wants to understand how baby name popularity has shifted over three decades, how trends differ across U.S. regions, and which names are uniquely popular or used across genders.

## Approach

Charles structured the analysis around four objectives. First, he tracked popularity changes over time — identifying the overall most popular names, plotting individual name rankings by year using ROW_NUMBER(), and finding the biggest rank jumps between 1980 and 2009. Second, he compared popularity across decades using RANK() with decade groupings. Third, he analyzed regional patterns by joining the names table with a regions reference table and computing top names within each region. Fourth, he explored unique names — finding the most popular androgynous names, the shortest and longest names, and answering a custom stakeholder question about the geographic distribution of a specific name.

## Key Results & Insights

- Michael and Jessica dominated the 1980s and 1990s as the top boy and girl names, respectively.
- By the 2000s, Jacob and Emily emerged at the top, reflecting cultural shifts in naming preferences.
- The South had the largest total number of births, influencing national trends.
- Names like Aidan and Skylar showed the biggest popularity jumps from 1980 to 2009.
- The most popular androgynous names (used for both genders) included some surprising entries like Michael and Jessica, which were occasionally used for the opposite gender.
- The shortest names (2 letters, e.g., Ty, Bo) and longest names (15 letters, e.g., Franciscojavier) had vastly different popularity levels.

## Technologies Used

- **SQL:** Window functions (RANK, ROW_NUMBER), CTEs, UNION, JOINs, GROUP BY, HAVING, subqueries, CASE expressions

## Links

- **GitHub:** https://github.com/cdcoonce/Baby_Names_Analysis

## Skills Demonstrated

SQL & Database Analytics
