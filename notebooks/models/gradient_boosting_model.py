from sklearn.ensemble import GradientBoostingRegressor
from .base_model import BaseModel

class GradientBoostingModel(BaseModel):
    def __init__(self, learning_rate=0.01, n_estimators=100, random_state=42):
        super().__init__(GradientBoostingRegressor(learning_rate=learning_rate, n_estimators=n_estimators, random_state=random_state))