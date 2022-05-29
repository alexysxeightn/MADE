"""
Functions for inference model
"""
from typing import Union

import numpy as np
import pandas as pd

from .train_model import SklearnClassifierModel


def predict(
    model: SklearnClassifierModel,
    features: Union[pd.DataFrame, np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    return model.predict(features)
