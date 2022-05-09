from dataclasses import dataclass
from typing import List, Optional


@dataclass()
class CategoricalFeatureParams:
    name: str
    categories: List[int]


@dataclass()
class NumericalFeatureParams:
    name: str
    type: str
    min: float
    max: float


@dataclass()
class FeatureParams:
    all_features: List[str]
    categorical_features: List[CategoricalFeatureParams]
    numerical_features: List[NumericalFeatureParams]
    target: Optional[CategoricalFeatureParams]
