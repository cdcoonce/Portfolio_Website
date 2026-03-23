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

### Model Performance

- **The Neural Network achieved the best overall performance** (RMSE ≈ $26,940), narrowly outperforming kNN ($27,025) and Linear Regression ($28,152) — a gap of roughly $1,200 between best and worst, reflecting meaningful but not dramatic differences across model classes.
- Cross-validation confirmed the ranking: the Neural Network generalized best, kNN consistently outperformed Linear Regression, and all three models benefited substantially from feature engineering.

### Bias-Variance Tradeoff (kNN Analysis)

- **The kNN RMSE-vs-k plot clearly demonstrated the bias-variance tradeoff**: at k=1, the model memorized training data (near-zero training error, high test error); as k increased toward 40, performance plateaued into underfitting. Optimal performance emerged around k=5.
- This visual illustration of the tradeoff — overfit at low k, underfit at high k — made kNN the most pedagogically valuable model in the comparison, even though it finished second overall.

### Feature Engineering Impact

- **TotalSF (combined square footage across all floors and basement) was the single most impactful engineered feature**, contributing more predictive signal than any raw feature in the dataset.
- TotalBath (combined full and half bath count), AgeAtSale, and RemodelAge further grounded the model in the property's lifecycle, capturing depreciation effects that raw year-built columns underrepresent.

### Analytical Takeaway

- **Model flexibility is valuable only when paired with proper architecture.** The Neural Network's advantage came from its ability to model interactions without overfitting — not just from adding layers.
- The performance gap between the three models was modest, but feature engineering moved all three significantly — validating that a well-engineered feature set often matters more than model choice.

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
