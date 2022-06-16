import json
import os
import pickle
from typing import Dict, Tuple

import click
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def load_data(load_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    return (
        pd.read_csv(os.path.join(load_path, "data_test.csv")),
        pd.read_csv(os.path.join(load_path, "target_test.csv"), squeeze=True, dtype=int),
    )


def load_model(model_path: str) -> LinearRegression:
    with open(os.path.join(model_path, "model.pkl"), "rb") as model_file:
        model = pickle.load(model_file)
    return model


def calculate_metrics(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
    return {
        'r2': r2_score(y_true, y_pred),
        'MAE': mean_absolute_error(y_true, y_pred),
        'MSE': mean_squared_error(y_true, y_pred)
    }


def save_results(metrics: Dict[str, float], model_path: str) -> None:
    with open(os.path.join(model_path, "metrics.json"), "w") as f:
        json.dump(metrics, f)


@click.command()
@click.option("--data_path", "-d", required=True)
@click.option("--model_path", "-m", required=True)
def validation(data_path: str, model_path: str):
    data_test, target_test = load_data(data_path)
    model = load_model(model_path)
    metrics = calculate_metrics(target_test, model.predict(data_test))
    save_results(metrics, model_path)


if __name__ == "__main__":
    validation()