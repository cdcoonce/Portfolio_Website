# Ames Housing Price Prediction

## Classification

- **Type:** Academic
- **Status:** Complete
- **Featured:** No
- **Date:** Oct 2025

## Summary

A predictive modeling project comparing Linear Regression, k-Nearest Neighbors, and a Neural Network on the Ames Housing Dataset. Charles built this for an Applied Predictive Modeling course to demonstrate the bias-variance tradeoff and evaluate how model flexibility impacts performance on a real-world regression task.

## Business Problem

Accurately predicting home sale prices is valuable for real estate professionals, appraisers, and homebuyers. The Ames Housing Dataset, with 79 features describing 2,930 homes, provides a rich testbed for understanding which modeling approaches best capture the complex relationships between property characteristics and sale price.

## Approach

Charles started with data preparation — removing irrelevant columns, handling missing values, and engineering new features like total square footage (TotalSF), combined bathroom count (TotalBath), age at sale (AgeAtSale), and time since last remodel (RemodelAge). He built a preprocessing pipeline using scikit-learn's ColumnTransformer with imputation, standard scaling for numeric features, and one-hot encoding for categorical variables.

He then trained three models of increasing flexibility: Linear Regression as a high-bias baseline, k-Nearest Neighbors (testing k from 1 to 40 to demonstrate the bias-variance tradeoff), and a Neural Network with two hidden layers (128 and 64 neurons, ReLU activation) built in TensorFlow/Keras.

## Key Results & Insights

- The Neural Network achieved the best performance with an RMSE of approximately $26,940, followed by kNN at $27,025 and Linear Regression at $28,152.
- The kNN analysis clearly demonstrated the bias-variance tradeoff — very low k values overfit (high variance), while high k values underfit (high bias), with optimal performance around k=5.
- The Neural Network captured complex nonlinear relationships without significant overfitting, validating the benefit of increased model flexibility when paired with proper architecture.
- Cross-validation confirmed that kNN consistently outperformed Linear Regression, while the Neural Network showed the best generalization overall.
- Feature engineering (especially TotalSF) significantly improved results across all models.

## Technologies Used

- **Data processing:** Pandas, NumPy
- **Machine learning:** scikit-learn (Linear Regression, KNeighborsRegressor, Pipeline, ColumnTransformer)
- **Neural network:** TensorFlow, Keras
- **Validation:** KFold cross-validation, train/test split
- **Visualization:** Matplotlib (correlation heatmap, bias-variance plot, training curves, parity plot)

## Challenges & Solutions

The dataset has 79 features with a mix of numeric and categorical variables, many with missing values. Charles addressed this by building a robust preprocessing pipeline that handled imputation, scaling, and encoding in a single reproducible step. Selecting the right k value for kNN required systematic experimentation, which he visualized as an RMSE vs. k plot to clearly show the tradeoff.

## Links

- **GitHub:** https://github.com/cdcoonce/Ames_Housing_Model_Comparison

## Skills Demonstrated

Machine Learning, Statistical Analysis & Modeling, Data Wrangling & ETL, Data Visualization & Dashboards
