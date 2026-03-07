# Restaurant Sales Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No

## Summary

A SQL-based analysis of restaurant sales and menu item data. Charles explored the menu structure, pricing by category, and ordering trends to uncover insights that could help the restaurant optimize its menu and understand revenue drivers.

## Business Problem

Restaurant operators need to understand which menu categories drive the most revenue, which items are most and least popular, and how ordering patterns look over time. These insights inform decisions about menu pricing, item promotion, and inventory planning.

## Approach

Charles analyzed two related tables — menu items (with names, categories, and prices) and order details (with order IDs, timestamps, and item references). He used SQL aggregations to examine the menu composition, identify the most and least expensive items, calculate average prices by category, and determine the date range and volume of orders. He then joined the tables to find the most and least ordered items, identify the highest-spending orders, and break down those top orders by category.

## Key Results & Insights

- Italian cuisine had the highest average price per dish at $16.75, followed by Asian ($13.48), Mexican ($11.80), and American ($10.07).
- The order data spanned January 1 to March 31, 2023.
- The top 5 highest-spending orders were dominated by Italian dishes, reinforcing that Italian food contributes significantly to total revenue.
- The largest single order contained 14 items.
- These findings suggest Italian items are both high-value and frequently ordered in large quantities, making them the restaurant's strongest revenue category.

## Technologies Used

- **SQL:** Aggregations (COUNT, AVG, SUM, MIN, MAX), JOINs, UNION, subqueries, GROUP BY, ORDER BY, LIMIT

## Links

- **GitHub:** https://github.com/cdcoonce/Restaurant_Order_Analysis

## Skills Demonstrated

SQL & Database Analytics
