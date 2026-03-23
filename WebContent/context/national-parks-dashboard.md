# National Parks Visitation Dashboard

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** Yes
- **Date:** Sep 2024

## Summary

An interactive R Shiny dashboard that allows users to explore U.S. National Parks visitation data over time. Users can filter by park and year range, view dynamic time-series visualizations, and browse detailed data in a color-coded interactive table.

## Business Problem

The National Park Service collects visitation data across dozens of parks over many decades, but raw data tables are hard to explore and compare. Park administrators, researchers, and enthusiasts need an accessible way to filter, visualize, and compare visitation trends across parks and time periods without needing to write code or build their own charts.

## Approach

Charles built a Shiny web application with a sidebar panel for user controls and a main panel for outputs. The app reads a CSV dataset, cleans it by filtering out summary rows and converting data types, and then uses reactive expressions to dynamically filter the data based on user selections. A dropdown allows multi-park selection, and a slider controls the year range. The app renders a time-series line chart using ggplot2 and an interactive data table using the DT package, with custom color coding based on visitor counts.

## Key Results & Insights

### Deployed & Accessible

- **The dashboard is publicly deployed on shinyapps.io** and accessible to anyone without installation — demonstrating the ability to take an analysis from local development to a shareable, hosted web application.
- Reactive expressions ensure the filtering logic runs only when user inputs change, keeping the app responsive even as the underlying dataset spans many decades and parks.

### Analytical Insights Surfaced

- **Side-by-side multi-park comparison reveals that visitation trajectories diverge sharply** — some parks grew steadily decade over decade while others plateaued or fluctuated, patterns that would be invisible in a single-park view.
- The year-range slider enables users to isolate specific historical windows (e.g., pre- vs. post-WWII, or the decade around the National Park Centennial in 2016) and observe how visitation responded to cultural moments and infrastructure improvements.
- **The color-coded DT table provides immediate visual triage**: high-visitation years appear in warm colors and low-visitation years in cool colors, allowing users to identify anomalous years (e.g., post-9/11 dip, 2020 COVID closures) at a glance without reading every number.

### Engineering Decisions

- Filtering out summary rows and converting data types at load time (rather than at render time) keeps reactive computations fast — a design choice that scales better as the dataset grows.
- Displaying region and state context dynamically alongside the selected parks adds interpretive value without cluttering the UI, reinforcing that dashboard design should surface context rather than force users to look it up separately.

## Technologies Used

- **Dashboard framework:** R Shiny
- **Visualization:** ggplot2
- **Data tables:** DT package
- **Data processing:** R (dplyr, readr)

## Links

- **Live Demo:** https://iuq9gs-charles-coonce.shinyapps.io/visitation/
- **GitHub:** https://github.com/cdcoonce/National_Parks_Dashboard

## Skills Demonstrated

Data Visualization & Dashboards
