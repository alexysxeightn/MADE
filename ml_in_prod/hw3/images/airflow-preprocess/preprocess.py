import os
from typing import Tuple

import click
import pandas as pd


def load_data(load_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    return (
        pd.read_csv(os.path.join(load_path, "data.csv")),
        pd.read_csv(os.path.join(load_path, "target.csv"), squeeze=True, dtype=int),
    )


def fill_missing(data: pd.DataFrame) -> pd.DataFrame:
    return data.fillna(data.mean())


def save_data(save_path: str, data: pd.DataFrame, target: pd.Series) -> None:
    os.makedirs(save_path, exist_ok=True)
    for name, dataset in {"data": data, "target": target}.items():
        dataset.to_csv(os.path.join(save_path, f"{name}.csv"), index=False)


@click.command()
@click.option("--load_path", "-l", required=True)
@click.option("--save_path", "-s", required=True)
def preprocess(load_path: str, save_path: str):
    
    X, y = load_data(load_path)
    
    X = fill_missing(X)

    save_data(save_path, X, y)


if __name__ == "__main__":
    preprocess()
