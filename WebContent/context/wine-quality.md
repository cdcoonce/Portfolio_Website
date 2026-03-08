# Wine Quality Analysis

## Classification

- **Type:** Academic
- **Status:** Complete
- **Featured:** Yes
- **Date:** Nov 2024

## Summary

A statistical and machine learning analysis of the Wine Quality Dataset from the UCI Machine Learning Repository. Charles explored the physicochemical properties of red and white Portuguese wines to identify the key features that influence quality ratings, then built predictive regression models to estimate wine quality scores.

## Business Problem

Wine quality assessment traditionally relies on expert tasters, which is subjective and difficult to scale. If measurable chemical properties — like acidity, alcohol content, and sulfur dioxide levels — can reliably predict quality, producers could use data to guide production decisions, optimize blending, and maintain consistency across vintages.

## Approach

Charles started with exploratory data analysis, examining feature distributions, pair plots, and a correlation matrix to understand how the 11 physicochemical attributes relate to quality ratings for both red and white wines separately. He identified that alcohol content was the strongest positive predictor of quality for both wine types, while volatile acidity negatively impacted quality, especially in reds.

He then built gradient boosted regression models using the full feature set and evaluated performance using RMSE and R² on train/test splits. To address multicollinearity, he identified highly correlated feature pairs (threshold > 0.65) — such as density and residual sugar in white wines — and removed redundant features to build leaner models.

## Key Results & Insights

- Alcohol content was the strongest quality predictor for both red wines (correlation 0.48) and white wines (correlation 0.44).
- Volatile acidity had the strongest negative impact on red wine quality (correlation -0.39).
- Full-feature models achieved test R² of approximately 0.54 (red) and 0.55 (white), with training R² of 0.93 for both — indicating some overfitting that could be addressed with regularization.
- Removing highly correlated features (free sulfur dioxide and fixed acidity for reds; density and residual sugar for whites) produced more interpretable models without significant loss in performance.
- Feature importance plots confirmed that alcohol, volatile acidity, and sulphates were the most influential variables.

## Technologies Used

- **Data analysis:** Python, Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn (distribution plots, pair plots, correlation heatmaps, feature importance charts)
- **Machine learning:** scikit-learn (gradient boosted regression, train/test split)

## Challenges & Solutions

The main challenge was handling multicollinearity between features. Several pairs of variables — like density and residual sugar, or total and free sulfur dioxide — were highly correlated, which can inflate variance in model coefficients. Charles addressed this by computing correlation matrices, setting a threshold of 0.65, and systematically removing the less predictive feature from each correlated pair.

## Links

- **GitHub:** https://github.com/cdcoonce/Wine_Quality_Analysis

## Skills Demonstrated

Statistical Analysis & Modeling, Machine Learning, Data Wrangling & ETL, Data Visualization & Dashboards
