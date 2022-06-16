import os
import pickle
from typing import Tuple

import click
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression


def load_data(load_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    return (
        pd.read_csv(os.path.join(load_path, "data_train.csv")),
        pd.read_csv(os.path.join(load_path, "target_train.csv"), squeeze=True, dtype=int),
    )


def save_model(model: BaseEstimator, model_path: str) -> None:
    os.makedirs(model_path, exist_ok=True)
    with open(os.path.join(model_path, "model.pkl"), "wb") as f:
        pickle.dump(model, f)


@click.command()
@click.option("--data_path", "-d", required=True)
@click.option("--model_path", "-m", required=True)
def train(data_path: str, model_path: str):
    data_train, target_train = load_data(data_path)
    model = LinearRegression().fit(data_train, target_train)
    save_model(model, model_path)


if __name__ == "__main__":
    train()
