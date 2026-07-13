from evaluation.evaluator import Evaluator
from evaluation.comparer import Comparer


class Trainer:
    def __init__(self, models):
        self.models = models
        self.results = {}
        self.predictions = {}

    def train_and_evaluate(self,
                           X_train, X_test, y_train, y_test
                           ):

        for model in self.models:

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)
            self.predictions[model.get_name()] = predictions

            metrics = Evaluator.evaluate(y_test, predictions)

            self.results[model.get_name()] = metrics

        comparison = Comparer.compare(self.results)

        print("\nModel Comparison")
        print(comparison)

        return comparison

    def get_best_model(self):

        best_model = max(
            self.results,
            key=lambda model: self.results[model]["R2"]
        )
        return best_model, self.results[best_model]


