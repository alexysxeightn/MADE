"""
Functions for creating transformers
"""
import logging
from typing import Union, List, Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from .preprocessing_params import PreprocessingParams


logger = logging.getLogger(__name__)


class IdentityTransformer(BaseEstimator, TransformerMixin):
    def fit(self, features: Any):
        return self

    def transform(self, features) -> Any:
        return features


class OneHotTransformer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        numerical_features: List[str],
        categorical_features: List[str],
        scale: bool,
    ):
        self.categorical_features = categorical_features
        self.numerical_features = numerical_features
        self.one_hot_encoder: Union[OneHotEncoder, None] = None
        self.standard_scaler: Union[StandardScaler, None] = None

        self._was_fit = False
        self.scale = scale

    def fit(self, features: pd.DataFrame):
        self._was_fit = True
        self.one_hot_encoder = OneHotEncoder(handle_unknown="ignore").fit(
            features[self.categorical_features]
        )
        if self.scale:
            self.standard_scaler = StandardScaler().fit(
                features[self.numerical_features]
            )

        return self

    def transform(self, features: pd.DataFrame) -> pd.DataFrame:
        if not self._was_fit:
            logger.warning("The transformer hasn't been fit.")

        # StandardScaler drops column names, so they have to be recovered
        transformed_cat_features = pd.DataFrame(
            self.one_hot_encoder.transform(
                features[self.categorical_features]
            ).toarray(),
            columns=self.one_hot_encoder.get_feature_names_out(),
        )
        if self.scale:
            transformed_num_features = pd.DataFrame(
                self.standard_scaler.transform(features[self.numerical_features]),
                columns=self.numerical_features,
            )
        else:
            transformed_num_features = features[self.numerical_features]
        return pd.concat([transformed_cat_features, transformed_num_features], axis=1)


CustomTransformerClass = Union[IdentityTransformer, OneHotTransformer]


def create_transformer(
    params: PreprocessingParams,
    categorical_features: List[str],
    numerical_features: List[str],
    scale: bool = True,
) -> CustomTransformerClass:
    if params.transformer_type == "IdentityTransformer":
        return IdentityTransformer()
    elif params.transformer_type == "OneHotTransformer":
        return OneHotTransformer(numerical_features, categorical_features, scale)
    else:
        error_message = f"Unknown transformer type: {params.transformer_type}."
        logger.error(error_message)
        raise ValueError(error_message)
