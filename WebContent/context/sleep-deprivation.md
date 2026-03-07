# Sleep Deprivation & Cognitive Performance Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No

## Summary

An exploratory and moderation analysis investigating how sleep factors relate to cognitive and emotional outcomes. Charles examined whether stress levels moderate the relationships between sleep metrics (quality and hours) and performance outcomes (reaction time and emotion regulation), finding statistically significant effects in both low-stress and high-stress subgroups.

## Business Problem

Workplace performance and employee wellbeing are directly affected by sleep quality. Understanding how sleep interacts with stress to influence cognitive performance and emotional regulation can inform targeted wellness interventions — for example, prioritizing sleep quality programs for low-stress employees and sleep duration programs for high-stress employees.

## Approach

Charles performed exploratory data analysis to understand variable distributions and relationships across measures including sleep hours, sleep quality, daytime sleepiness, reaction time, cognitive accuracy, and emotion regulation. He then split participants into stress-level subgroups and conducted moderation analyses using centered regression models. For the low-stress group, he modeled emotion regulation as a function of sleep quality. For the high-stress group, he modeled PVT reaction time as a function of sleep hours.

## Key Results & Insights

- In the low-stress subgroup, sleep quality was a significant positive predictor of emotion regulation — each 1-unit increase in sleep quality above the mean was associated with approximately 1.20 points higher emotion regulation scores (p ≈ 0.036, R² = 0.148).
- In the high-stress subgroup, sleep hours significantly predicted faster reaction times — each additional hour of sleep was associated with approximately 16.92 units faster PVT reaction time (p ≈ 0.037, R² = 0.147).
- These findings suggest that stress plays a moderating role: in low-stress conditions, sleep quality matters most for emotional outcomes, while in high-stress conditions, sleep duration matters most for cognitive performance.
- While the models explain a modest portion of variance, they point to clear, actionable differences in how sleep interventions should be targeted based on stress levels.

## Technologies Used

- **Data analysis:** Python, Pandas, NumPy
- **Statistical modeling:** statsmodels (OLS regression with centering)
- **Visualization:** Matplotlib (scatter plots with regression lines)
- **Environment:** Jupyter Notebook

## Links

- **GitHub:** https://github.com/cdcoonce/Sleep_Deprivation_Analysis

## Skills Demonstrated

Statistical Analysis & Modeling, Data Visualization & Dashboards
