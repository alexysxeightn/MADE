import os

import click
from sklearn.datasets import load_diabetes


@click.command()
@click.option("--save_path", "-s", required=True)
def download(save_path: str):
    X, y = load_diabetes(return_X_y=True, as_frame=True)

    os.makedirs(save_path, exist_ok=True)
    X.to_csv(os.path.join(save_path, "data.csv"), index=False)
    y.to_csv(os.path.join(save_path, "target.csv"), index=False)


if __name__ == '__main__':
    download()
