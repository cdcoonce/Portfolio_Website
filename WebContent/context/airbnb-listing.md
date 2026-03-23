# AirBnB Listing Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

An exploratory analysis of Paris AirBnB listings examining pricing trends and the impact of 2015 regulatory changes on the market. Charles cleaned and filtered the dataset, aggregated pricing by neighbourhood, and built time-series visualizations that revealed a decrease in new hosts and an increase in average prices following the introduction of regulations.

## Business Problem

AirBnB faces increasing regulatory pressure in major cities. Leadership at the company needed a visual summary of how Paris listings were affected by regulations introduced in 2015 — specifically whether the regulations reduced the number of new hosts entering the market and how pricing responded. Understanding these dynamics helps inform strategic decisions about market expansion and compliance.

## Approach

Charles started by exploring the dataset to understand its structure and identify quality issues, including missing host registration dates that he addressed through imputation. He filtered the data to Paris-only listings and selected relevant columns including host details, neighbourhood, accommodations, and price. After removing invalid entries (zero-priced listings), he grouped data by neighbourhood to calculate average pricing trends and created time-series visualizations comparing the number of new hosts against average price per night using dual-axis plots.

## Key Results & Insights

### Regulatory Impact on Host Supply

- **New host registrations declined noticeably after 2015**, with the time-series clearly showing a slowdown in host entry following the introduction of Paris short-term rental regulations — consistent with a supply-side chilling effect from increased compliance requirements.
- The pre-2015 period showed relatively consistent growth in new hosts; post-2015, that growth flattened or reversed depending on the neighbourhood, suggesting the regulations did not affect all areas uniformly.

### Pricing Response

- **Average nightly prices trended upward across Parisian neighbourhoods following the regulations**, consistent with a constrained supply environment — fewer new hosts entering the market reduced competition and put upward pressure on prices.
- The dual-axis visualization revealed an **inverse relationship between new host entry rates and average pricing**: as new host growth declined, average price per night increased — a pattern visible across the post-2015 window.
- Neighbourhoods with higher pre-regulation host density showed more pronounced price increases, suggesting the regulations had the sharpest effect in already-competitive areas.

### Analytical Takeaway

- The Paris case illustrates a classic supply-restriction dynamic: regulations designed to protect long-term housing availability reduced short-term supply, which in turn increased prices for remaining guests — a trade-off regulators and policymakers in other cities can learn from.
- Missing host registration dates required imputation, which is a common data quality challenge in marketplace datasets and a consideration when interpreting the exact timing of the post-regulation trend break.

## Technologies Used

- **Data processing:** Python, Pandas
- **Visualization:** Matplotlib (time-series plots, dual-axis charts)
- **Environment:** Jupyter Notebook, uv

## Links

- **GitHub:** https://github.com/cdcoonce/Airbnb_Listing_Analysis

## Skills Demonstrated

Data Wrangling & ETL, Data Visualization & Dashboards
