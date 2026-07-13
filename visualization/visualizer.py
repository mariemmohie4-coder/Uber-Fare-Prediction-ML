import matplotlib.pyplot as plt


class Visualizer:

    @staticmethod
    def plot_predictions(y_true, y_pred, model_name):
        plt.figure(figsize=(7, 7))

        plt.scatter(y_true, y_pred, alpha=0.5)

        plt.plot(
            [y_true.min(), y_true.max()],
            [y_true.min(), y_true.max()],
            "r--",
            linewidth=2,
        )

        plt.xlabel("Actual Fare")
        plt.ylabel("Predicted Fare")
        plt.title(f"{model_name}\nActual vs Predicted")

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_residuals(y_true, y_pred, model_name):

        residuals = y_true - y_pred

        plt.figure(figsize=(8, 5))

        plt.scatter(y_pred, residuals, alpha=0.5)

        plt.axhline(y=0, color="red", linestyle="--")

        plt.xlabel("Predicted Fare")
        plt.ylabel("Residual")

        plt.title(f"{model_name}\nResidual Plot")

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_r2_scores(comparison_df):

        plt.figure(figsize=(8, 5))

        plt.bar(comparison_df.index, comparison_df["R2"])

        plt.ylabel("R² Score")
        plt.xlabel("Model")
        plt.title("Model Comparison (R²)")

        plt.xticks(rotation=45)

        plt.grid(axis="y")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_rmse(comparison_df):

        plt.figure(figsize=(8, 5))

        plt.bar(comparison_df.index, comparison_df["RMSE"])

        plt.ylabel("RMSE")
        plt.xlabel("Model")
        plt.title("Model Comparison (RMSE)")

        plt.xticks(rotation=45)

        plt.grid(axis="y")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_mae(comparison_df):

        plt.figure(figsize=(8, 5))

        plt.bar(comparison_df.index, comparison_df["MAE"])

        plt.ylabel("MAE")
        plt.xlabel("Model")
        plt.title("Model Comparison (MAE)")

        plt.xticks(rotation=45)

        plt.grid(axis="y")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_mse(comparison_df):

        plt.figure(figsize=(8, 5))

        plt.bar(comparison_df.index, comparison_df["MSE"])

        plt.ylabel("MSE")
        plt.xlabel("Model")
        plt.title("Model Comparison (MSE)")

        plt.xticks(rotation=45)

        plt.grid(axis="y")

        plt.tight_layout()
        plt.show()