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

### Visitation Trends

- **National park visitation increased dramatically over the century covered** (1904–2016), with the most pronounced acceleration occurring post-WWII as car ownership expanded and the Interstate Highway System made parks more accessible.
- **The Pacific West and Intermountain regions showed the steepest long-term growth**, driven by high-traffic parks like Grand Canyon, Yellowstone, Yosemite, and Olympic — parks that saw visitation grow from hundreds of thousands to millions annually.
- **California, Wyoming, and Washington led in total state-level visitation**, reflecting the concentration of iconic, marquee parks in those states rather than the number of parks alone.

### Geographic Clustering

- **Hierarchical clustering produced five geographically coherent clusters** of parks, aligning with natural regional groupings: the Pacific Northwest, California, the Intermountain Southwest, the Rocky Mountain corridor, and the Eastern parks.
- Cluster membership was driven by geographic proximity rather than visitation level, meaning each cluster contains a mix of high- and low-traffic parks — useful for itinerary planning because travelers aren't automatically routed only to the most crowded destinations.
- The bubble plot clearly distinguished the handful of "mega-parks" (by visitation) from the long tail of lesser-visited parks, highlighting that a small number of parks absorb a disproportionate share of total annual visits.

### Route Optimization

- **TSP optimization within each cluster produced efficient multi-park driving routes** that minimize total distance — a practical tool for trip planning that goes beyond simple "top parks" lists by accounting for travel logistics.
- The geosphere-based distance matrix correctly handled the spherical geometry of cross-continental distances, ensuring route calculations were accurate rather than relying on flat-plane approximations.
- The optimized routes surfaced non-obvious stopping sequences where visiting a less-famous park en route between two major parks adds minimal travel time — a finding not visible from ranked-popularity lists alone.

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
