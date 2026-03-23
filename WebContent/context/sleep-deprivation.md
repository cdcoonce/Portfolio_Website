# Sleep Deprivation & Cognitive Performance Analysis

## Classification

- **Type:** Guided Coursework
- **Status:** Complete
- **Featured:** No
- **Date:** Feb 2025

## Summary

An exploratory and moderation analysis investigating how sleep factors relate to cognitive and emotional outcomes. Charles examined whether stress levels moderate the relationships between sleep metrics (quality and hours) and performance outcomes (reaction time and emotion regulation), finding statistically significant effects in both low-stress and high-stress subgroups.

## Business Problem

Workplace performance and employee wellbeing are directly affected by sleep quality. Understanding how sleep interacts with stress to influence cognitive performance and emotional regulation can inform targeted wellness interventions — for example, prioritizing sleep quality programs for low-stress employees and sleep duration programs for high-stress employees.

## Approach

Charles performed exploratory data analysis to understand variable distributions and relationships across measures including sleep hours, sleep quality, daytime sleepiness, reaction time, cognitive accuracy, and emotion regulation. He then split participants into stress-level subgroups and conducted moderation analyses using centered regression models. For the low-stress group, he modeled emotion regulation as a function of sleep quality. For the high-stress group, he modeled PVT reaction time as a function of sleep hours.

## Key Results & Insights

### Low-Stress Subgroup: Sleep Quality → Emotion Regulation

- **Sleep quality was a significant positive predictor of emotion regulation in the low-stress group** — each 1-unit increase in sleep quality above the mean was associated with approximately 1.20 points higher emotion regulation scores (p ≈ 0.036, R² = 0.148).
- The effect is specific to emotional outcomes: in low-stress conditions, _how well_ you sleep matters more for emotional functioning than _how long_ you sleep.

### High-Stress Subgroup: Sleep Duration → Cognitive Performance

- **Sleep hours significantly predicted faster PVT reaction times in the high-stress group** — each additional hour of sleep above the mean was associated with approximately 16.92 units faster reaction time (p ≈ 0.037, R² = 0.147).
- Under high stress, the relationship flips: _how long_ you sleep matters for cognitive speed, while sleep quality loses significance — suggesting that stress consumes the emotional regulation benefits of quality sleep, leaving only the restorative impact of duration.

### Moderation Effect

- **Stress level moderates which sleep dimension matters**: quality for emotional outcomes in low-stress individuals, duration for cognitive performance in high-stress individuals. This stress × sleep interaction is the study's central finding.
- Both models explain modest variance (R² ≈ 0.15), consistent with the complexity of psychological outcomes — but p-values confirm these are not noise, and effect sizes are large enough to be practically meaningful for intervention design.

### Applied Implications

- **Sleep interventions should be stress-stratified**: low-stress populations benefit most from programs that improve sleep quality (sleep environment, consistency, hygiene); high-stress populations benefit most from programs that protect sleep duration (workload management, scheduling norms).
- This finding argues against one-size-fits-all wellness sleep programs — the lever that matters most depends on the stress context of the target population.

## Technologies Used

- **Data analysis:** Python, Pandas, NumPy
- **Statistical modeling:** statsmodels (OLS regression with centering)
- **Visualization:** Matplotlib (scatter plots with regression lines)
- **Environment:** Jupyter Notebook

## Links

- **GitHub:** https://github.com/cdcoonce/Sleep_Deprivation_Analysis

## Skills Demonstrated

Statistical Analysis & Modeling, Data Visualization & Dashboards
