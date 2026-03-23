# Global CO₂ Emissions Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

A Tableau dashboard analyzing global carbon emissions data from 1750 to 2022. Charles built interactive visualizations — including a choropleth map, bubble chart, and time-series line chart — with parameterized controls that let users explore how different countries have contributed to global CO₂ emissions over time.

## Business Problem

Understanding historical and current patterns of carbon emissions is critical for policymakers, researchers, and organizations working on climate strategy. With a 79-column dataset spanning centuries of emissions data, users need an interactive tool to filter, compare, and explore trends rather than sifting through raw data. Key questions include which countries have historically dominated emissions, how per capita emissions compare to absolute emissions, and how each country's share of global emissions has shifted over time.

## Approach

Charles began with data profiling, discovering that the dataset included aggregated regional groupings (like "Asia" and "European Union") that would distort country-level analysis. He filtered these out by removing rows without valid ISO country codes. He converted emissions columns to numeric types for proper aggregation and created an integer parameter to enable dynamic "Top N" filtering in Tableau. He then built three main visualizations: a choropleth map of per capita emissions, a bubble chart comparing emissions against population, and a line chart tracking each country's share of global emissions over time.

## Key Results & Insights

### Historical Emissions Patterns

- **Early industrial powers (the United Kingdom, United States, and select Western European nations) dominated global emissions from the mid-1800s through the mid-20th century**, reflecting coal-driven industrialization. Their share of global emissions declined sharply after mid-century as Asia industrialized.
- **China's share of global CO₂ emissions grew dramatically from the 1980s onward**, surpassing the United States in absolute terms by the 2000s — a trend made immediately visible in the line chart's share-of-global-emissions view.
- The United States held the largest cumulative historical emissions share through most of the 20th century, a distinction that persists when the time-series is aggregated over the full 1750–2022 span.

### Per Capita vs. Absolute Emissions

- **Per capita and absolute emissions rankings diverge significantly** — countries like Qatar, Kuwait, and several Gulf states rank among the highest per capita emitters despite negligible absolute totals, while China and India rank lower per capita despite massive absolute emissions.
- The choropleth map made this divergence visually compelling: large countries with enormous populations appear muted on a per capita basis despite dominating absolute rankings, while small high-income oil states are intensely colored.
- This per capita framing is critical for equity-based policy discussions — responsibility for historical emissions is distributed very differently depending on which metric is used.

### Dashboard Interactivity

- The dynamic "Top N" parameter allows users to focus on the most significant emitters at any point in time, reducing visual noise and enabling cleaner country-to-country comparison.
- Filtering out non-country aggregates (regional groupings without ISO codes) was essential — their inclusion would have made the top-emitter charts misleading by mixing country-level and supra-national totals.

## Technologies Used

- **Visualization:** Tableau (choropleth maps, bubble charts, line charts, parameters, filters, calculated fields)

## Links

- **GitHub:** https://github.com/cdcoonce/Global_CO2_Emissions
- **Live Demo:** https://public.tableau.com/views/Global_Emissions_17395769212090/GlobalCO2Emissions

## Skills Demonstrated

Data Visualization & Dashboards
