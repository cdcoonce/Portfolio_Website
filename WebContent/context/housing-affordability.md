# Housing Affordability & Commute Trade-Off Analysis

## Classification

- **Type:** Independent Research — began as an Arizona State University capstone, substantially rebuilt and extended in 2026
- **Status:** Active
- **Featured:** Yes
- **Date:** Jul 2026

## Summary

A data engineering and econometrics project that quantifies the relationship between housing costs, commute time, transit access, and employment geography across nine U.S. metropolitan areas. Charles built the entire system end-to-end: a reproducible pipeline joining seven data sources into ZCTA-level datasets (1,503 ZIP-code areas cross-sectionally, plus a 102,773-row monthly rent panel spanning 138 months from 2015 through mid-2026), and a four-question statistical analysis that culminates in a panel fixed-effects study of whether COVID repriced the commute gradient. The headline result: where repricing happened, it favored the periphery — long-commute, low-job-access areas gained rent relative to job-rich cores — and it did not reverse in the return-to-office era.

## Business Problem

Housing affordability is one of the most pressing issues facing American metro areas, but it is rarely analyzed in isolation. Where people can afford to live often determines how far they commute, and transit access and employment geography play critical roles in that equation. Policymakers, urban planners, and researchers need data-driven tools to identify which ZIP codes are most burdened by the combination of high rent and long commutes — whether those burdens fall disproportionately on lower-income or minority communities — and whether the pandemic's remote-work shock permanently changed the price of proximity to jobs.

## Approach

Charles designed a reproducible two-stage system. The first stage is a data pipeline that ingests seven sources: Census ACS 5-year (commute patterns, rent, income, demographics, vehicle access), a separate pre-COVID ACS 2015–2019 vintage (for the panel study's fixed 2019 commute measures), Zillow ZORI (both the latest-month rent index and the full 2015-onward monthly panel, committed behind a revision gate that bounds Zillow's between-pull changes), OpenStreetMap (transit stop density), LEHD LODES employment data (job density, distance to CBD, and gravity-model job accessibility — both a 2021 cross-section and a 2015–2023 annual panel), and Census TIGER/Line (geographic boundaries). The pipeline maps census tracts to ZCTAs with GeoPandas spatial joins and emits schema-validated, manifest-tracked datasets per metro.

The second stage answers four research questions. RQ1 models how commute time influences rent-to-income ratio with OLS, comparing linear and quadratic specifications via AIC, and estimates a "drive until you qualify" threshold as the quadratic vertex with a delta-method confidence interval. RQ2 examines equity: income- and race-based burden differences via ANOVA, commute × income interaction models, and K-Means clustering. RQ3 constructs a composite Affordability-Commute Index (ACI) modeled with OLS and quantile regression. RQ4 — the 2026 extension — asks whether COVID repriced the commute gradient: per-metro two-way fixed-effects regressions on the monthly rent panel, interacting three pre-COVID gradient measures (2019-vintage commute time, distance to CBD, and job accessibility) with a two-phase structural break (pandemic disruption 2020–2021, partial return-to-office 2022 onward), backed by event-study pre-trend checks, wild cluster bootstrap inference at coarse spatial clusters, and renter-weighted and seasonal-adjustment robustness variants.

## Key Results & Insights

### RQ4 — COVID and the Commute Gradient (the headline)

- **Where repricing happened, it favored the periphery.** Across the nine metros, covered ZIP-code areas far from jobs gained rent relative to job-rich cores after March 2020: commute-gradient interactions are positive in Phoenix, Denver, Atlanta, and Chicago; job-accessibility interactions are negative in Phoenix, LA, DFW, Atlanta, and Chicago; Seattle's repricing runs through distance to CBD. No metro shows core-favoring repricing that survives the robustness checks.
- **The repricing did not reverse in the return-to-office era.** In no metro does a significant pandemic-phase effect return to zero in the 2022+ phase — in Atlanta, Denver, LA, and Chicago (commute) the later-phase coefficient exceeds the disruption-phase one. The one clean fade is Chicago's job-accessibility effect.
- **The honesty rails matter — and are part of the point.** Event-study pre-trend checks demote Atlanta, Seattle, and Miami to "trend + break" (their gradients were already steepening before COVID), and a wild cluster bootstrap at coarse spatial clusters sustains only a subset of the conventional significance (Seattle's distance effect, DFW's access effect, Denver's disruption-phase set, and the phase-1 distance effects in Phoenix and Atlanta). Memphis is flagged under-identified (only 12 ZIP-code areas observed on both sides of the break) and treated as an honest null. The strictly-clean-and-robust list is short; the directional consistency across nine metros is the stronger finding.
- **Estimand discipline:** results describe Zillow's covered rental submarket only, "repricing" means the listing index moved (price and composition together), and every estimate is a within-metro relative description — not a causal effect of COVID, since every area is treated and no control group exists.

### Housing Affordability

- **Miami and Los Angeles are the least affordable metros** (mean rent-to-income 31.0% and 28.3%).
- **Low-income residents exceed or approach the 30% burden threshold in every metro**, ranging from 25.9% of income (Seattle) to 35.7% (Miami).
- **Memphis has the widest affordability gap** between income segments (17.1 percentage points); **Chicago is the most affordable on average** (21.1%) but still shows a 10.1-point income gap.

### RQ1 — Housing-Commute Trade-Off

- **Commute time is statistically significant in 6 of 9 metros** (Atlanta, Chicago, Los Angeles, Denver, DFW, Miami). This was originally 4 of 9; adding employment-center variables in 2026 changed both the count and the membership — Memphis and Seattle dropped out while Atlanta, Chicago, LA, and Miami entered.
- **Renter share is the most consistently significant predictor** — significant in 8 of 9 metros. Areas with higher renter concentration have higher rent burdens nearly universally.
- **Memphis has the strongest model fit** (R² = 0.80), though commute itself is no longer significant there — renter share carries the model.
- **The "drive until you qualify" threshold is identified in exactly one metro: Denver, at a 36.5-minute commute** (95% CI [31.9, 41.0]). Beyond that, longer commutes no longer trade for improved affordability. The other eight metros are honest nulls — the apparent concavity originally seen in several metros was substantially proxying employment-center structure.

### RQ2 — Equity Analysis

- **All 9 metros show statistically significant income-based rent burden differences** (p < 0.0001 everywhere) — the single most robust finding in the analysis.
- **8 of 9 metros show significant racial differences in rent burden**, with majority-white areas consistently less burdened. **Seattle is the sole exception** (F = 0.11, p = 0.90) — its market stratifies by wealth rather than race, an open research question.
- **Commute × income interactions run in opposite directions where they exist:** in Seattle, low-income residents benefit more from trading commute for affordability (p = 0.022); in Chicago, rent burden rises faster with commute time in low-income areas (p = 0.020).
- **Job accessibility is income-stratified in 5 of 9 metros**, and every metro produced a distinct "extreme pressure" K-Means cluster — Atlanta's worst cluster averages 52.7% rent burden; Chicago's combines its highest burden with its longest commutes.

### RQ3 — Affordability-Commute Index (ACI)

- **Job accessibility is the most consistent ACI predictor** — significant and negative in 8 of 9 metros: better access to jobs means lower combined affordability-commute pressure.
- **Transit access signals expensive, high-demand areas** — significant and positive in Chicago, Miami, and Phoenix — and **no metro shows a significant affordability-serving transit effect** once employment structure is controlled. (An earlier version of this analysis found DFW as a counter-example; that result did not survive the employment controls and was retracted.)
- **Adding employment-center variables in 2026 transformed the models:** Phoenix went from essentially unexplainable (R² = 0.017) to R² = 0.335, and the "Memphis paradox" (best commute model, worst ACI model) resolved — its ACI fit rose from 0.17 to 0.69 with job accessibility supplying the spatial signal transit couldn't.

### Cross-Cutting Themes

1. **Affordability is an income problem, not a commute problem.** Renter share (8 of 9) and income segment (9 of 9) dominate everywhere; commute matters in 6 of 9 metros but never leads.
2. **Racial inequality in housing is pervasive but not universal** — 8 of 9 metros, with Seattle the exception.
3. **Transit is not serving affordability anywhere** once employment structure is controlled; in dense cities it marks expensive areas. Transit investment needs affordability protections.
4. **The COVID repricing stuck.** The pandemic-era relative gains of peripheral, low-access areas persisted or deepened through mid-2026.
5. **Metro structure matters more than metro size** — model fit tracks how cleanly a metro follows a center-periphery gradient, not how many areas it has.

## Technologies Used

- **Data pipeline:** Python, Polars, GeoPandas, Prefect (cached, retrying task orchestration), Census ACS API, Zillow ZORI, OpenStreetMap Overpass API, LEHD LODES, Census TIGER/Line
- **Statistical analysis:** statsmodels (OLS, quantile regression, two-way fixed-effects panel models with cluster-robust inference), custom wild cluster bootstrap (Webb weights), scikit-learn (K-Means, cross-validation), scipy (ANOVA)
- **Data integrity:** schema validation, dataset manifests, and a panel revision gate that bounds and reports Zillow's between-vintage data revisions
- **Visualization:** Matplotlib (108 committed figures: regression diagnostics, equity boxplots and clusters, ACI plots, and event studies)
- **Testing & CI:** pytest (288 tests), GitHub Actions, Ruff
- **Environment management:** uv

## Challenges & Solutions

Mapping census tract-level data to ZCTA boundaries required GeoPandas spatial joins with population-weighted aggregation, since the two geographies don't align. The OpenStreetMap Overpass API's strict rate limits demanded caching and retry logic. The 2026 panel extension added a harder class of problems: Zillow revises its published rent history between pulls, so the committed panel sits behind a revision gate that quantifies and bounds those changes; the panel regressions needed honest inference under spatially correlated errors (solved with wild cluster bootstrap at coarse spatial clusters, deliberately conservative degrees-of-freedom corrections, and event-study pre-trend checks that demote several headline results); and the analysis reports what it cannot claim — under-identified metros are flagged rather than dropped, and composition-vs-price ambiguity is stated up front.

## Links

- **GitHub:** https://github.com/cdcoonce/housing-commute-analysis
- **Full findings:** https://github.com/cdcoonce/housing-commute-analysis/blob/main/docs/findings.md

## Skills Demonstrated

Data Engineering & Pipelines, Panel Econometrics & Statistical Inference, Statistical Analysis & Modeling, Machine Learning, Data Wrangling & ETL, Data Visualization & Dashboards, DevOps & Tooling
