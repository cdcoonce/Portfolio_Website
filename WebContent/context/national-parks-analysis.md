# National Parks Visitation Analysis

## Classification

- **Type:** Independent
- **Status:** Complete
- **Featured:** No
- **Date:** Aug 2024

## Summary

An R-based analysis of U.S. National Parks visitation data from 1904 to 2016, combining exploratory visualization with clustering and route optimization. Charles analyzed visitation trends across regions, identified the most popular parks, grouped parks into geographic clusters, and applied the Traveling Salesman Problem (TSP) to create efficient multi-park visit itineraries.

## Business Problem

Planning a trip to visit multiple national parks is a logistical challenge — parks are spread across vast distances, and visitors want to maximize the number of parks they see while minimizing travel time. Beyond trip planning, understanding long-term visitation trends helps the National Park Service with resource allocation, capacity planning, and identifying parks that may be underserved relative to demand.

## Approach

Charles started with data exploration and cleaning, addressing missing values and inconsistent formats in the historical dataset. He then created visualizations of visitation trends over time — both nationally and by region — using line plots and faceted views. A state-level heatmap showed total visitation by geography, and a bubble plot highlighted the most visited parks. He then applied hierarchical clustering to group parks by geographic proximity and used the TSP algorithm to compute the most efficient driving routes within each cluster, mapping the results with spatial libraries.

## Key Results & Insights

- Overall national park visitation has increased steadily since 1904, with the Pacific West and Intermountain regions seeing the steepest growth.
- California, Wyoming, and Washington had the highest total visitation at the state level.
- Hierarchical clustering produced five main geographic clusters of parks, each suitable for a multi-park road trip.
- TSP optimization provided efficient routes within each cluster, offering practical itineraries for park visitors.

## Technologies Used

- **Data processing:** R (dplyr, tidyr, stringr, readr)
- **Visualization:** ggplot2, gridExtra, usmap, sf, scales, gganimate
- **Clustering:** hierarchical clustering (cluster package)
- **Route optimization:** TSP package
- **Spatial analysis:** sf, geosphere, httr, jsonlite

## Challenges & Solutions

The main challenge was integrating the clustering output with the TSP solver and then mapping the optimized routes geographically. Charles used the geosphere package for distance calculations between park coordinates, fed those into the TSP solver, and then plotted the resulting routes using sf and ggplot2. Handling the coordinate systems and ensuring the route visualization aligned with the cluster map required careful coordination between packages.

## Links

- **GitHub:** https://github.com/cdcoonce/National_Parks_Project

## Skills Demonstrated

Data Visualization & Dashboards, Statistical Analysis & Modeling, Data Wrangling & ETL
