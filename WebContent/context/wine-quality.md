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

### Exploratory Findings

- **Alcohol content was the strongest quality predictor for both wine types** — correlation of 0.48 for reds and 0.44 for whites — suggesting that fermentation completeness and body are the most reliable chemical proxies for expert quality ratings.
- **Volatile acidity had the strongest negative impact on red wine quality** (correlation -0.39), reflecting the perceptible "vinegar" off-flavor that tasters penalize — a relationship that does not appear as strongly in white wines, which tolerate higher acidity differently.
- Red and white wines showed distinct chemical profiles requiring separate models: the features that predict quality in reds do not transfer directly to whites, making a combined model inappropriate.

### Model Performance

- **Full-feature gradient boosted models achieved test R² ≈ 0.54 (red) and 0.55 (white)**, with training R² of 0.93 for both — a large train/test gap indicating significant overfitting despite gradient boosting's built-in regularization.
- The gap between train and test R² (~0.38–0.39 points) signals that 11 physicochemical features capture meaningful but incomplete signal: subjective tasting is influenced by texture, finish, and contextual factors the chemical measurements don't fully quantify.

### Feature Selection and Multicollinearity

- **Removing highly correlated feature pairs** (density–residual sugar for whites; free sulfur dioxide–fixed acidity for reds; threshold > 0.65) produced leaner models with comparable test R² — demonstrating that correlated redundant features inflate apparent model complexity without improving generalization.
- **Feature importance plots consistently ranked alcohol, volatile acidity, and sulphates at the top** regardless of whether correlated features were included, validating these three as the core signal variables for quality prediction.

### Practical Implications

- The R² values around 0.54–0.55 suggest chemical properties alone cannot fully predict wine quality — a production use case would benefit from additional sensory descriptors beyond the 11 physicochemical measurements available in this dataset.
- For winemakers, the alcohol and volatile acidity findings translate directly to intervention points: managing fermentation conditions (alcohol) and controlling acetic acid bacteria (volatile acidity) are the two highest-leverage quality levers during production.

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
