from typing import List

from dataclasses import dataclass
from marshmallow_dataclass import class_schema

from .data import FeatureParams, SplittingParams
from .preprocessing import PreprocessingParams
from .models import ModelParams


@dataclass()
class TrainingPipelineParams:
    input_data_path: str
    output_model_path: str
    output_transformer_path: str
    metric_path: str
    features: FeatureParams
    model: ModelParams
    metric: List[str]
    preprocessing: PreprocessingParams
    split: SplittingParams
    save_output: bool
    report_path: str


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def get_training_pipeline_params(dict_config: dict) -> TrainingPipelineParams:
    return TrainingPipelineParamsSchema().load(dict_config)
