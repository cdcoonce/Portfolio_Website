# Motor Vehicle Thefts Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Mar 2025

## Summary

A SQL and Excel analysis of motor vehicle thefts in New Zealand, examining when, where, and which vehicles are most frequently stolen. Charles wrote analytical SQL queries to uncover patterns by time, location, vehicle type, and demographics, then created visualizations in Excel to communicate the findings.

## Business Problem

Law enforcement and public safety agencies need data-driven insights into vehicle theft patterns to allocate resources effectively. Understanding which vehicle types are targeted, when thefts peak, and which regions are most affected allows for more targeted patrols, public awareness campaigns, and prevention strategies.

## Approach

Charles structured the analysis around three objectives: when vehicles are stolen (by year, month, and day of week), which vehicles are stolen (by type, age, color, and luxury status), and where thefts occur (by region, population density). He wrote SQL queries using aggregations, joins, CASE expressions, CTEs, and UNION operations to extract insights from the relational dataset. He then visualized the results in Excel with charts showing theft trends by population density, regional distribution, vehicle characteristics, and day-of-week patterns.

## Key Results & Insights

### Geographic Patterns

- **Vehicle thefts were most prevalent in high-density regions, particularly Auckland** — the concentration of vehicles and population density creates both greater opportunity and greater anonymity for thieves, making urban centers disproportionately affected.
- **High-density and low-density regions showed meaningfully different vehicle type theft profiles**, suggesting different theft motivations: high-density thefts skew toward opportunistic theft of common vehicle types, while low-density patterns may reflect different target selection (e.g., utility vehicles, trucks).

### Temporal Patterns

- **Monday had the highest theft frequency, while Saturday had the lowest** — a counterintuitive finding, since one might expect weekend activity to create more opportunity. The weekday pattern likely reflects commuter parking and work-related vehicle exposure during the week.
- Seasonal patterns (by month) showed variation consistent with broader vehicle usage levels, with higher theft rates correlating with periods of higher overall vehicle activity.

### Vehicle Characteristics

- **Silver was the most commonly stolen vehicle color**, followed by white and black — a finding that reflects the overall prevalence of these colors in the vehicle fleet rather than targeted preference, since popular colors are simply more abundant targets.
- **Station wagons, saloons, and hatchbacks were the most stolen vehicle types**, which aligns with their dominance in the overall vehicle population. Thieves do not disproportionately target rare vehicle types.
- **Luxury vehicles accounted for only a small proportion of total thefts**, countering a common assumption — opportunistic theft dominates, and luxury vehicles are both less prevalent and often better secured.

### Law Enforcement Implications

- The concentration of thefts in Auckland by day of week and vehicle type provides actionable intelligence for patrol allocation — weekday hours in high-density urban zones represent the highest-risk window.
- The finding that theft profiles differ by population density suggests regional law enforcement strategies should be tailored, not uniform across the country.

## Technologies Used

- **SQL:** Aggregations, JOINs, CTEs, CASE expressions, UNION, subqueries
- **Excel:** Data visualization and formatting

## Links

- **GitHub:** https://github.com/cdcoonce/Motor_Vehicle_Thefts

## Skills Demonstrated

SQL & Database Analytics, Data Visualization & Dashboards
