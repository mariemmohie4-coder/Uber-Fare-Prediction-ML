from sklearn.ensemble import RandomForestRegressor
from .base_model import BaseModel

class RandomForestModel(BaseModel):
    def __init__(self, n_estimators=100, random_state=42, n_jobs=-1):
        super().__init__(RandomForestRegressor(n_estimators=n_estimators, random_state=random_state, n_jobs=n_jobs))