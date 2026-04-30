import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

print("Loading data...")
df = pd.read_excel("hourlyLoadDataIndia.xlsx")

# Rename columns
df = df.rename(columns={
    "datetime": "datetime",
    "National Hourly Demand": "national_load",
    "Northen Region Hourly Demand": "north",
    "Western Region Hourly Demand": "west",
    "Eastern Region Hourly Demand": "east",
    "Southern Region Hourly Demand": "south",
    "North-Eastern Region Hourly Demand": "north_east"
})

print("Engineering features...")
df["datetime"] = pd.to_datetime(df["datetime"])
df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month
df["day_of_week"] = df["datetime"].dt.dayofweek

# Create prev_load feature
df["prev_load"] = df["national_load"].shift(1)

# Drop rows with NaN values (due to shift)
df = df.dropna()

# Target
y = df["national_load"]

# Features
features = [
    "north", "west", "east", "south", "north_east",
    "hour", "day", "month", "day_of_week", "prev_load"
]
X = df[features]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

def evaluate(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return mae, rmse, r2, mape

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
    "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, n_jobs=-1)
}

results = []

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae, rmse, r2, mape = evaluate(y_test, y_pred)
    
    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape
    })
    
    joblib.dump(model, f"{name.replace(' ', '_')}.pkl", compress=3)

results_df = pd.DataFrame(results)
results_df.to_csv("model_results.csv", index=False)

print("\n✅ Training Complete!")
print(results_df)
