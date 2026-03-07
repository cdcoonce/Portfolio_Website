# Global CO₂ Emissions Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No

## Summary

A Tableau dashboard analyzing global carbon emissions data from 1750 to 2022. Charles built interactive visualizations — including a choropleth map, bubble chart, and time-series line chart — with parameterized controls that let users explore how different countries have contributed to global CO₂ emissions over time.

## Business Problem

Understanding historical and current patterns of carbon emissions is critical for policymakers, researchers, and organizations working on climate strategy. With a 79-column dataset spanning centuries of emissions data, users need an interactive tool to filter, compare, and explore trends rather than sifting through raw data. Key questions include which countries have historically dominated emissions, how per capita emissions compare to absolute emissions, and how each country's share of global emissions has shifted over time.

## Approach

Charles began with data profiling, discovering that the dataset included aggregated regional groupings (like "Asia" and "European Union") that would distort country-level analysis. He filtered these out by removing rows without valid ISO country codes. He converted emissions columns to numeric types for proper aggregation and created an integer parameter to enable dynamic "Top N" filtering in Tableau. He then built three main visualizations: a choropleth map of per capita emissions, a bubble chart comparing emissions against population, and a line chart tracking each country's share of global emissions over time.

## Key Results & Insights

- Early industrial powers (certain European countries and the United States) dominated CO₂ emissions until the mid-20th century, after which countries like China and India increased their share significantly.
- Per capita analysis revealed a different story than absolute emissions — some countries with large total emissions have moderate per capita rates due to large populations, while smaller countries can have very high per capita emissions.
- The interactive dashboard allows users to dynamically select how many countries to display and compare specific countries side by side.

## Technologies Used

- **Visualization:** Tableau (choropleth maps, bubble charts, line charts, parameters, filters, calculated fields)

## Links

- **GitHub:** https://github.com/cdcoonce/Global_CO2_Emissions
- **Live Demo:** https://public.tableau.com/views/Global_Emissions_17395769212090/GlobalCO2Emissions

## Skills Demonstrated

Data Visualization & Dashboards
