# World Happiness Dashboard

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Sep 2024

## Summary

An R-based analysis and interactive dashboard exploring the factors that drive happiness across countries worldwide. Charles cleaned and analyzed the World Happiness Report data, applied statistical modeling to understand the relationships between happiness and factors like GDP, social support, and life expectancy, and built visualizations and an optional Shiny dashboard for interactive exploration.

## Business Problem

The World Happiness Report ranks countries by wellbeing measures annually, but the raw rankings don't explain why some countries score higher than others. Policymakers, researchers, and NGOs benefit from understanding which factors — economic output, social support, health, freedom, generosity, or corruption — most strongly predict happiness, and how these relationships vary across regions and over time.

## Approach

Charles cleaned and preprocessed the raw datasets by handling missing values, standardizing variable names, and transforming the data for analysis. He conducted exploratory data analysis to investigate trends and patterns in happiness scores, then examined the relationships between happiness and its component factors using correlation studies and regression analysis. He created visualizations using ggplot2 and plotly to reveal key trends and regional comparisons, and built an optional Shiny-based dashboard for interactive data exploration.

## Key Results & Insights

### Top Predictors of National Happiness

- **GDP per capita and social support were the two most consistent predictors of happiness scores** across the countries in the dataset, together explaining the majority of the variance in national happiness rankings — confirming that both economic and relational factors are essential components of wellbeing.
- **Life expectancy (healthy years lived) was the third-strongest predictor**, reinforcing that health infrastructure and outcomes are tightly coupled with subjective national wellbeing.
- **Freedom to make life choices and generosity showed weaker but positive associations**, while perceptions of corruption showed a negative relationship — countries with high perceived corruption consistently scored lower on happiness, independent of income level.

### Regional Differences

- **Nordic and Western European countries (Finland, Denmark, Switzerland, Iceland) consistently ranked among the happiest**, driven by high scores across all six factors simultaneously — no single factor explains their top rankings in isolation.
- **Sub-Saharan African countries clustered at the lower end of happiness scores**, where GDP per capita gaps drove much of the ranking differential — economic development remains the primary lever in this region.
- **Latin American countries outperformed their GDP rankings** on happiness, suggesting that social support and cultural factors contribute positively to wellbeing beyond what income alone would predict — a finding sometimes called the "Latin American happiness paradox."
- Some East Asian countries with high GDP per capita scored lower on happiness than expected, suggesting that social support, freedom, and perceptions of corruption partially offset economic advantages.

### Longitudinal Insights

- Annual rankings show meaningful stability at the top and bottom over the years covered, but the middle tiers fluctuate — suggesting that happiness is relatively stable for very high- and very low-income countries, while middle-income nations are more sensitive to year-to-year economic and political changes.
- The interactive Shiny dashboard allows users to trace individual country trajectories over time, making it easy to identify countries that meaningfully improved or declined across reporting years.

## Technologies Used

- **Data processing:** R (dplyr, tidyr, readr)
- **Visualization:** ggplot2, plotly
- **Dashboard:** R Shiny (optional interactive component)
- **Statistical analysis:** R (regression analysis, correlation studies)

## Links

- **GitHub:** https://github.com/cdcoonce/World_Happiness_Report

## Skills Demonstrated

Data Visualization & Dashboards, Statistical Analysis & Modeling
