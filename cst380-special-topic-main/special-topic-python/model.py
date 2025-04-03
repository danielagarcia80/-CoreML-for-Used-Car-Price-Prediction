# @Author: Logan Powser
# @Date: 3/24/2024
# @Abstract: convert a trained regression model to a .mlmodel file for use in Swift!

import pandas as pd
import numpy as np
import coremltools as ct
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, root_mean_squared_error, make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline, make_pipeline

# Load dataset
df = pd.read_csv('./dataset/vehicles_processed0.csv')

# Variables of interest
predictors = ['odometer', 'condition', 'year', 'car_age']
target = 'price'

# Convert to numpy and split
X = df[predictors].values
y = df[target].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Scoring metrics
r2_scorer = make_scorer(r2_score)
mse_scorer = make_scorer(mean_squared_error)
rmse_scorer = make_scorer(root_mean_squared_error)

scorers = {
    'r2': r2_scorer,
    'mse': mse_scorer,
    'rmse': rmse_scorer
}

# Evaluation helper
def final_testing(pipeline: Pipeline, X_test, y_test, name: str):
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    print(f'\n-- {name} Prediction Metrics --')
    print(f"r2: {r2:.4g}")
    print(f"mse: {mse:.4g}")
    print(f"rmse: {rmse:.4g}\n")

# Grid search on decision tree
tree_grid = {
    'max_depth': range(1, 8, 2),
    'min_samples_leaf': range(2, 9, 2),
}

tree_grid_search = GridSearchCV(DecisionTreeRegressor(), tree_grid, cv=10, scoring=scorers, refit='r2')

tree_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('tree_search', tree_grid_search)
])

tree_pipeline.fit(X_train, y_train)
final_testing(tree_pipeline, X_test, y_test, 'Decision Tree Regression')

# Extract fitted scaler and best model (removing unsupported GridSearchCV)
fitted_scaler = tree_pipeline.named_steps['scaler']
best_model = tree_pipeline.named_steps['tree_search'].best_estimator_

# Create clean pipeline for CoreML
final_pipeline = make_pipeline(fitted_scaler, best_model)

# Convert and export
coreml_model = ct.converters.sklearn.convert(final_pipeline, predictors, target)
coreml_model.save('tree_model.mlmodel')
