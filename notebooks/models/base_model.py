class BaseModel:
    def __init__(self, model):
        self.model = model


    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)


    def predict(self, X_test):
        return self.model.predict(X_test)


    def get_model(self):
        return self.model

    def get_name(self):
        return self.model.__class__.__name__

