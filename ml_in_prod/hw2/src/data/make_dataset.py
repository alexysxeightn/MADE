"""
Functions to loading and split dataset, and generate synthetic data
"""
import logging
from typing import Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .features_params import (
    FeatureParams,
    NumericalFeatureParams,
    CategoricalFeatureParams,
)
from .split_params import SplittingParams


logger = logging.getLogger(__name__)


def load_data(
    data_path: str,
    feature_params: FeatureParams,
    return_target=False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.Series]]:
    """
    Loading data from `data_path` (csv)

    Args:
        data_path: path to a csv file
        feature_params: describes all features and target to be included
        return_target: if True add target to output

    Returns: (features, target) or features.
    """
    df = pd.read_csv(data_path)
  
    if return_target:
        return df[feature_params.all_features], df[feature_params.target.name]
    
    return df[feature_params.all_features]


def split_data(
    features: Union[pd.DataFrame, np.ndarray],
    target: Union[pd.Series, np.ndarray],
    split_params: SplittingParams,
) -> Tuple[
    Union[pd.DataFrame, np.ndarray],
    Union[pd.DataFrame, np.ndarray],
    Union[pd.Series, np.ndarray],
    Union[pd.Series, np.ndarray],
]:
    """
    Splits features and target on train and test dataset.

    Returns: (features_train, features_test, target_train, target_test)
    """
    features_train, features_test, target_train, target_test = train_test_split(
        features,
        target,
        test_size=split_params.test_size,
        random_state=split_params.random_state,
    )
    logger.info(f"Split data. Test size: {split_params.test_size}")
    return features_train, features_test, target_train, target_test


def generate_numerical_samples(
    num_samples: int,
    feature_params: NumericalFeatureParams
) -> np.ndarray:
    """
    Generate synthetic numerical features
    
    Args:
        num_samples: number of samples to generate
        feature_params: feature description
        
    Returns: features
    """
    if feature_params.type == "discrete":
        return np.random.choice(
            range(int(feature_params.min), int(feature_params.max) + 1), num_samples
        )
    elif feature_params.type == "continuous":
        return np.random.random(num_samples) * (feature_params.max - feature_params.min)
    else:
        error_message = f"Unknown number type {feature_params.type}."
        logger.error(error_message)
        raise ValueError(error_message)


def generate_categorical_samples(
    num_samples: int,
    feature_params: CategoricalFeatureParams
) -> np.ndarray:
    """
    Generate synthetic categorical features
    
    Args:
        num_samples: number of samples to generate
        feature_params: feature description
        
    Returns: features
    """
    return np.random.choice(feature_params.categories, num_samples)


def generate_train_data(
    num_samples: int,
    feature_params: FeatureParams,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic features and target
    
    Args:
        num_samples: number of samples to generate
        feature_params: Feature description
        
    Returns: (features, target)
    """
    feature_name_to_samples = dict()
    for num_feature_params in feature_params.numerical_features:
        feature_name_to_samples[num_feature_params.name] = generate_numerical_samples(
            num_samples, num_feature_params
        )

    for cat_feature_params in feature_params.categorical_features:
        feature_name_to_samples[cat_feature_params.name] = generate_categorical_samples(
            num_samples, cat_feature_params
        )

    features = pd.DataFrame(
        {name: feature_name_to_samples[name] for name in feature_params.all_features}
    )
    targets = pd.Series(np.random.choice(feature_params.target.categories, num_samples))
    return features, targets
