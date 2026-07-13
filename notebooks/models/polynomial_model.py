from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from .base_model import BaseModel



class PolynomialRegressionModel(BaseModel):

    def __init__(self):

        model = Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("linear", LinearRegression())
        ])

        super().__init__(model)