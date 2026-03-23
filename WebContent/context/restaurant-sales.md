# Restaurant Sales Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Mar 2025

## Summary

A SQL-based analysis of restaurant sales and menu item data. Charles explored the menu structure, pricing by category, and ordering trends to uncover insights that could help the restaurant optimize its menu and understand revenue drivers.

## Business Problem

Restaurant operators need to understand which menu categories drive the most revenue, which items are most and least popular, and how ordering patterns look over time. These insights inform decisions about menu pricing, item promotion, and inventory planning.

## Approach

Charles analyzed two related tables — menu items (with names, categories, and prices) and order details (with order IDs, timestamps, and item references). He used SQL aggregations to examine the menu composition, identify the most and least expensive items, calculate average prices by category, and determine the date range and volume of orders. He then joined the tables to find the most and least ordered items, identify the highest-spending orders, and break down those top orders by category.

## Key Results & Insights

### Menu Pricing by Category

- **Italian cuisine had the highest average price per dish at $16.75**, followed by Asian ($13.48), Mexican ($11.80), and American ($10.07) — a 66% price premium for Italian over American, which has significant revenue implications given order volumes.
- The price spread across categories reflects both ingredient costs and positioning decisions; Italian dishes command a premium that the ordering data confirms customers are willing to pay.

### Order Patterns and Revenue Drivers

- **The top 5 highest-spending orders were dominated by Italian dishes**, reinforcing that Italian is both the highest-priced and most revenue-generating category — a compounding effect where price premium and order frequency combine.
- **The largest single order contained 14 items**, suggesting group dining occasions drive significant single-order revenue — a finding relevant to staffing and kitchen capacity decisions for large-party management.
- Order data spanned January 1 to March 31, 2023, providing a full quarter of transactions for trend-stable conclusions.

### Strategic Implications

- **Italian is the restaurant's strongest revenue category on both dimensions** — highest average price and highest representation in the top spending orders. Menu strategy should protect and potentially expand the Italian category.
- **American cuisine underperforms on price** ($10.07 average) but may serve a high-volume, accessibility role; the analysis suggests investigating whether American dishes drive enough volume to compensate for lower per-dish margins.
- The data supports a focus on group dining experiences where Italian-heavy ordering naturally increases the average check size — an actionable revenue optimization target.

## Technologies Used

- **SQL:** Aggregations (COUNT, AVG, SUM, MIN, MAX), JOINs, UNION, subqueries, GROUP BY, ORDER BY, LIMIT

## Links

- **GitHub:** https://github.com/cdcoonce/Restaurant_Order_Analysis

## Skills Demonstrated

SQL & Database Analytics
