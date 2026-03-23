# Spaceship Titanic Classification

## Classification

- **Type:** Academic
- **Status:** Complete
- **Featured:** No
- **Date:** May 2025

## Summary

A machine learning classification project for the Kaggle Spaceship Titanic competition. Charles predicted whether passengers were transported to another dimension using extensive feature engineering, multiple model comparison, SHAP-based interpretability analysis, and a final stacking ensemble that outperformed all individual models.

## Business Problem

The Spaceship Titanic competition is a Kaggle learning competition that challenges participants to build a binary classifier from passenger attributes. While the scenario is fictional, the techniques are directly applicable to real-world classification problems — customer churn prediction, fraud detection, medical diagnosis — where feature engineering, model selection, and interpretability all matter.

## Approach

Charles began with exploratory data analysis to understand class distributions and feature relationships. He then performed extensive feature engineering: parsing cabin codes into deck, number, and side components; extracting group structure from passenger IDs; and creating interaction features like a combined spending total and a CryoSleep × low-spend flag. After preprocessing (group-based imputation, one-hot encoding, standard scaling), he evaluated six models: Logistic Regression, SVM, KNN, Random Forest, XGBoost, and a Stacking Ensemble. He tuned hyperparameters using GridSearchCV and RandomizedSearchCV, and used SHAP for global feature importance, dependence plots, and individual prediction explanations.

## Key Results & Insights

### Model Performance

- **The stacking ensemble (XGBoost + SVM + Logistic Regression meta-learner) achieved approximately 81% accuracy** on validation data, outperforming all six individual models and earning the best Kaggle leaderboard position.
- Individual model accuracy ranged from Logistic Regression at ~77% to XGBoost at ~80% — the ensemble's lift over the best individual model reflects the value of combining classifiers with different error profiles.
- Hyperparameter tuning via GridSearchCV (XGBoost) and RandomizedSearchCV (SVM, Random Forest) provided measurable improvements over default configurations.

### SHAP Interpretability

- **CryoSleep was the strongest predictor of transportation** — passengers in cryo-sleep were far more likely to be transported, consistent with the narrative that unconscious passengers couldn't resist the anomaly.
- **Higher spending on VRDeck and Spa correlated strongly with NOT being transported** — active, spending passengers were "protected," and spending signals their engagement with the ship during the incident.
- **Passengers from Europa** showed distinct transportation patterns relative to Earth passengers, and **starboard-side cabin placement** showed significant differences from port side — spatial features that emerged as meaningful only after parsing cabin codes into deck, number, and side components.

### Feature Engineering Impact

- **Parsing the cabin code into deck, number, and side** transformed a single opaque string into three structured features with independent predictive signal — a common pattern in real-world datasets where IDs encode meaningful information.
- **The CryoSleep × low-spend interaction flag** emerged from SHAP analysis showing that the two features had a combined effect that neither captured alone — a reminder that initial SHAP results should guide a second round of feature engineering, not just explanation.
- Group structure extracted from passenger IDs improved imputation quality by using group-level statistics rather than global statistics for missing values.

### Analytical Takeaway

- This project demonstrates the full ML classification pipeline: EDA → feature engineering → model comparison → hyperparameter tuning → ensemble → interpretability — the exact sequence applicable to real classification problems like churn, fraud, and medical diagnosis.
- **The key lesson is that SHAP is a tool for iteration, not just explanation**: using feature importance results to build new interaction features, then re-evaluating, is what pushed the ensemble from ~79% to 81%.

## Technologies Used

- **Machine learning:** scikit-learn (Logistic Regression, SVM, KNN, Random Forest, Stacking), XGBoost
- **Interpretability:** SHAP (summary plots, dependence plots, interaction plots)
- **Preprocessing:** scikit-learn (Pipeline, StandardScaler, OneHotEncoder)
- **Tuning:** GridSearchCV, RandomizedSearchCV
- **Data processing:** Pandas, NumPy

## Challenges & Solutions

The biggest challenge was ensuring consistency between the training and test preprocessing — particularly with one-hot encoding, where the test set could have different category levels. Charles built a unified preprocessing pipeline that handled this gracefully. Feature engineering was also iterative; the CryoSleep × low-spend interaction flag only emerged after initial SHAP analysis suggested the two features had a combined effect that wasn't captured by either alone.

## Links

- **GitHub:** https://github.com/cdcoonce/Spaceship_Titanic

## Skills Demonstrated

Machine Learning, Statistical Analysis & Modeling, Data Wrangling & ETL
