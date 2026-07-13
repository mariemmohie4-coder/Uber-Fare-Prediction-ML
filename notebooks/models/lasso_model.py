from sklearn.linear_model import Lasso
from .base_model import BaseModel

class LassoRegressionModel(BaseModel):
    def __init__(self, alpha=0.1):
        super().__init__(Lasso(alpha=alpha))