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

- The stacking ensemble (XGBoost + SVM + Logistic Regression) achieved approximately 81% accuracy on validation data and the best Kaggle leaderboard score.
- SHAP analysis revealed that CryoSleep was the strongest predictor of transportation, while higher spending (especially on VRDeck and Spa) correlated with not being transported.
- Passengers from Europa and those on the starboard side showed distinct transportation patterns.
- Low-spending cryo-sleepers were the most likely group to be transported — a finding that emerged from the interaction feature engineering.
- The SHAP dependence and interaction plots provided clear explanations of how features combined to influence predictions.

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
