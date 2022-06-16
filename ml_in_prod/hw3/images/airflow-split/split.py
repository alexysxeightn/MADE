import os
from typing import Tuple

import click
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(load_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    return (
        pd.read_csv(os.path.join(load_path, "data.csv")),
        pd.read_csv(os.path.join(load_path, "target.csv"), squeeze=True, dtype=int),
    )


def save_data(
    save_path: str,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> None:
    os.makedirs(save_path, exist_ok=True)
    for name, dataset in {
        "data_train": X_train,
        "data_test": X_test,
        "target_train": y_train,
        "target_test": y_test
    }.items():
        dataset.to_csv(os.path.join(save_path, f"{name}.csv"), index=False)


@click.command()
@click.option("--load_path", "-l", required=True)
@click.option("--save_path", "-s", required=True)
@click.option("--train_size", "-t", default=0.8)
@click.option("--random_state", "-r", default=42)
def split_data(load_path: str, save_path: str, train_size: float, random_state: int):
    
    X, y = load_data(load_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size, random_state=random_state
    )

    save_data(save_path, X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    split_data()
