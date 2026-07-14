import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

data_path = os.path.join(os.path.dirname(__file__), '../Data/data_selection_uber.csv')
df = pd.read_csv(data_path)

X = df[['pickup_year', 'bearing', 'avg_distance_to_center', 'is_airport', 'manhattan_distance']]
y = df['fare_amount']

model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X, y)

save_path = os.path.join(os.path.dirname(__file__), 'best_model.joblib')
joblib.dump(model, save_path, compress=3)
