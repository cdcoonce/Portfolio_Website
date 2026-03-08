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

- The analysis showed a clear decrease in the number of new hosts entering the Paris market after the 2015 regulatory changes.
- Average price per night showed an upward trend across various neighbourhoods following the regulations.
- The dual-axis visualization effectively demonstrated the inverse relationship between host entry rates and pricing, suggesting the regulations constrained supply while demand-side pressure pushed prices higher.

## Technologies Used

- **Data processing:** Python, Pandas
- **Visualization:** Matplotlib (time-series plots, dual-axis charts)
- **Environment:** Jupyter Notebook, uv

## Links

- **GitHub:** https://github.com/cdcoonce/Airbnb_Listing_Analysis

## Skills Demonstrated

Data Wrangling & ETL, Data Visualization & Dashboards
