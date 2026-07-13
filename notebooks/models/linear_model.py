from statistics import linear_regression

from sklearn.linear_model import LinearRegression
from .base_model import BaseModel

class LinearRegressionModel(BaseModel):
    def __init__(self):
        super().__init__(LinearRegression())
