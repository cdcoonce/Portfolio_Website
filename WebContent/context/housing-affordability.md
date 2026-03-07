# Housing Affordability & Commute Trade-Off Analysis

## Classification

- **Type:** Capstone Project — Arizona State University
- **Status:** Complete
- **Featured:** Yes

## Summary

A data engineering and statistical analysis pipeline that quantifies the relationship between housing costs, commute time, and public transit accessibility across nine U.S. metropolitan areas. Charles built the entire project end-to-end — from data ingestion to regression analysis — to answer real research questions about where housing affordability and commute burdens intersect.

## Business Problem

Housing affordability is one of the most pressing issues facing American metro areas, but it is rarely analyzed in isolation. Where people can afford to live often determines how far they commute, and transit access plays a critical role in that equation. Policymakers, urban planners, and researchers need data-driven tools to identify which ZIP codes are most burdened by the combination of high rent and long commutes — and whether those burdens fall disproportionately on lower-income or minority communities.

## Approach

Charles designed a reproducible two-stage pipeline. The first stage is a data engineering pipeline that ingests data from four sources: Census ACS (commute patterns, rent, income, demographics), Zillow (observed rent index), OpenStreetMap (transit stop density), and Census TIGER/Line (geographic boundaries). The pipeline fetches CBSA boundaries, maps census tracts to ZCTAs (ZIP Code Tabulation Areas), performs spatial joins, and aggregates everything into a clean, analysis-ready dataset for each metro area.

The second stage applies statistical analysis to answer three research questions. RQ1 uses OLS regression with robust standard errors to model how commute time influences rent-to-income ratio, comparing linear and quadratic specifications and selecting the best model via AIC. RQ2 examines equity by testing how housing and commute burdens vary by income segment and race, using interaction models, ANOVA, and K-Means clustering. RQ3 constructs a composite Affordability-Commute Index (ACI) and models it with both OLS and quantile regression to identify the most burdened areas.

## Key Results & Insights

- The pipeline produces a clean ZCTA-level dataset with approximately 30 columns spanning housing, commute, transit, demographic, and vehicle access metrics for each of the nine metro areas.
- RQ1 confirmed a statistically significant relationship between commute time and rent burden across multiple metros, with model selection via AIC identifying quadratic specifications as the better fit in several cases.
- RQ2 revealed measurable disparities in housing and commute burdens across income segments and racial groups, with K-Means clustering identifying distinct "burden profiles" within metro areas.
- RQ3's Affordability-Commute Index successfully ranked ZCTAs by combined burden, with quantile regression revealing that the predictors of burden differ at the extremes compared to the median.
- The entire pipeline is reproducible — any of the nine metros can be re-run with a single command.

## Technologies Used

- **Data pipeline:** Python, GeoPandas, Polars, Census ACS API, Zillow ZORI, OpenStreetMap Overpass API, Census TIGER/Line shapefiles
- **Statistical analysis:** statsmodels (OLS, quantile regression), scikit-learn (K-Means, cross-validation), scipy (ANOVA)
- **Visualization:** Matplotlib (diagnostic plots, choropleth maps)
- **Testing & CI:** pytest, GitHub Actions, Ruff
- **Environment management:** uv

## Challenges & Solutions

One of the biggest challenges was mapping census tract-level data to ZCTA boundaries, since the two geographies don't align neatly. Charles implemented spatial joins using GeoPandas to handle the tract-to-ZCTA crosswalk, weighting aggregations by population overlap. Another challenge was handling the OpenStreetMap Overpass API, which has strict rate limits — the pipeline includes caching and retry logic to handle this gracefully. Finally, ensuring the analysis was truly reproducible across all nine metros required careful parameterization of both the pipeline and analysis stages.

## Links

- **GitHub:** https://github.com/cdcoonce/housing-commute-analysis

## Skills Demonstrated

Data Engineering & Pipelines, Statistical Analysis & Modeling, Machine Learning, Data Wrangling & ETL, Data Visualization & Dashboards, DevOps & Tooling
