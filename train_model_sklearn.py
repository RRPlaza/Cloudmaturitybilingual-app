# train_model_sklearn.py

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("training_data.csv")

# Features and targets
X = df.iloc[:, :14]
y = df[["madurez_general", "riesgo_general"]]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
xgb_model = MultiOutputRegressor(xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100))
xgb_model.fit(X_train, y_train)

# Predict
y_pred = xgb_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

# Save model
joblib.dump(xgb_model, "model_sklearn_xgb.pkl")
print("Model saved as 'model_sklearn_xgb.pkl'")