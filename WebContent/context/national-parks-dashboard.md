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

- The dashboard is deployed and publicly accessible, allowing anyone to explore park visitation trends interactively.
- Users can compare visitation patterns across multiple parks simultaneously, revealing trends like the steady growth in visitation at popular parks and seasonal patterns.
- The color-coded data table makes it easy to spot high-visitation and low-visitation years at a glance.
- Additional context — such as region and state information for selected parks — is displayed dynamically alongside the visualizations.

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
