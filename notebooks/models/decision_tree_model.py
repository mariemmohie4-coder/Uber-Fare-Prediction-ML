from sklearn.tree import DecisionTreeRegressor
from .base_model import BaseModel

class DecisionTreeModel(BaseModel):
    def __init__(self, random_state=42):
        super().__init__(DecisionTreeRegressor(random_state=random_state))