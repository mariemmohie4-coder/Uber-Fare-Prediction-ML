
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, root_mean_squared_error

class Evaluator:

    @staticmethod
    def evaluate(y_true, y_pred):

        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = root_mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        return {
            "MAE": round(mae, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4),
        }

