import os
import pickle

import click
import pandas as pd
from sklearn.linear_model import LinearRegression


def load_data(load_path: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(load_path, "data.csv"))


def load_model(model_path: str) -> LinearRegression:
    with open(os.path.join(model_path, "model.pkl"), "rb") as f:
        model = pickle.load(f)
    return model


def save_predictions(predictions: pd.Series, predictions_path: str) -> None:
    os.makedirs(predictions_path, exist_ok=True)
    predictions.to_csv(os.path.join(predictions_path, "predictions.csv"), index=False)


@click.command()
@click.option("--data_path", "-d", required=True)
@click.option("--model_path", "-m", required=True)
@click.option("--predictions_path", "-p", required=True)
def predict(data_path: str, model_path: str, predictions_path: str):
    dataset = load_data(data_path)
    model = load_model(model_path)
    predictions = pd.Series(model.predict(dataset))
    save_predictions(predictions, predictions_path)


if __name__ == "__main__":
    predict()