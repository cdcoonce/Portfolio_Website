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

### Housing Affordability

- **Miami and Los Angeles are the least affordable metros**, both exceeding or approaching the 30% rent-burdened threshold on average (31.0% and 28.3% respectively).
- **Low-income residents exceed the 30% burden threshold in every metro**, ranging from 25.9% of income (Seattle) to 35.7% (Miami).
- **Memphis has the widest affordability gap** between income segments (17.1 percentage points), indicating extreme income-based inequality despite a moderate overall average.
- **Chicago is the most affordable on average** (21.1%) but still shows a 10.1-point gap between income groups.

### RQ1 — Housing-Commute Trade-Off

- **Commute time is statistically significant in only 4 of 9 metros** (Memphis, Seattle, Denver, DFW). In the other five, other factors dominate.
- **Renter share is the most consistently significant predictor**, reaching p < 0.01 in 7 of 9 metros.
- **Memphis has the strongest model fit** (R² = 0.73), likely because its simpler spatial structure follows a predictable center-periphery gradient.
- **The concave relationship** in Denver, DFW, Memphis, and Miami indicates a "drive until you qualify" effect with diminishing returns — rent burden drops with longer commutes up to a point, then plateaus.

### RQ2 — Equity Analysis

- **All 9 metros show statistically significant income-based rent burden differences** (p < 0.0001 in all cases) — the single most robust finding in the entire analysis.
- **8 of 9 metros show significant racial differences in rent burden.** Majority-white ZCTAs consistently have lower rent burdens.
- **Seattle is the sole exception** — no significant racial differences (F = 0.11, p = 0.90). Seattle's affordability dynamics are income-driven but not race-stratified.
- In **8 of 9 metros**, the commute-rent tradeoff operates similarly regardless of income level. **Seattle is again the exception** (p = 0.014): low-income residents there benefit more from the "drive until you qualify" tradeoff.
- Every metro produced a distinct "extreme pressure" K-Means cluster. Atlanta had the highest single-cluster burden (0.527). Chicago's worst cluster combines the highest rent burden (0.333) with the longest commute (39.9 min) — a "double-burdened" zone.

### RQ3 — Affordability-Commute Index (ACI)

- **Transit access has contradictory effects depending on metro structure:**
  - In **Chicago and Miami**, transit-rich areas have *higher* combined ACI pressure because they are desirable, expensive locations.
  - In **Dallas-Fort Worth**, transit access has a significant *negative* relationship with ACI — the only metro where more transit = less combined pressure.
  - In 6 other metros, transit has no measurable effect on ACI.
- **Phoenix is essentially unexplainable** by this model (R² = 0.017). Its dynamics operate through mechanisms not captured by these variables.
- **The Memphis paradox:** Best-fitting RQ1 model (R² = 0.73) but worst-fitting ACI model (R² = 0.17) — commute time alone powerfully predicts rent burden in Memphis, but adding transit collapses the model because Memphis has virtually no transit infrastructure.

### Cross-Cutting Themes

1. **Affordability is an income problem, not a commute problem.** Commute time predicts rent burden in only 4 of 9 metros. Policy interventions targeting commute reduction alone will not meaningfully address affordability.
2. **Racial inequality in housing is pervasive but not universal.** 8 of 9 metros show significant racial rent burden disparities; Seattle is the exception.
3. **Transit is a double-edged sword.** In dense cities it signals expensive, high-demand areas; in sprawling metros it genuinely serves affordability. Transit investment must be paired with affordability protections.
4. **"Drive until you qualify" has limits.** The concave relationships show a spatial boundary where further driving no longer buys proportionally more affordability.
5. **Metro structure matters more than metro size.** Explanatory power tracks with how consistently the metro follows an expected center-periphery gradient, not with observation count.

### Policy Implications

1. **Income-targeted interventions** (rental assistance, inclusionary zoning, wage policy) are more likely to reduce rent burden than commute-oriented strategies alone.
2. **Transit investment requires affordability protections.** In Chicago and Miami, transit-rich areas already price out lower-income residents.
3. **DFW's transit model is worth studying** — it is the only metro where transit access correlates with lower combined pressure.
4. **Racial equity in housing** remains a challenge in 8 of 9 metros. Place-based policies must account for racial disparities in cost burden.

### Notable Outliers

- **Seattle:** No racial rent disparities, but significant commute × income interaction — a unique equity profile among the nine metros.
- **Phoenix:** Neither model explains its affordability dynamics; rapid growth, seasonal migration, and land use patterns are candidate factors.
- **Atlanta:** Contains a 2-ZCTA cluster with rent burden of 0.527, the highest single-cluster burden observed.
- **Memphis:** Widest income gap (17.1pp), best RQ1 fit (R² = 0.73), worst ACI fit (R² = 0.17).

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
