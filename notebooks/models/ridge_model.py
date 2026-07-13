from sklearn.linear_model import Ridge
from .base_model import BaseModel

class RidgeRegressionModel(BaseModel):
    def __init__(self, alpha=1.0):
        super().__init__(Ridge(alpha=alpha))

