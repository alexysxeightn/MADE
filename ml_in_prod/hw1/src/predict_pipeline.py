"""
Script for inference model
"""
import logging
from typing import Union

import csv
import hydra
import numpy as np
import pandas as pd
import pickle
from omegaconf import DictConfig

from .data import load_data
from .models import SklearnClassifierModel, predict
from .predict_pipeline_params import get_predict_pipeline_params, PredictPipelineParams
from .preprocessing import CustomTransformerClass
from .utils import init_hydra, create_directory


logger = logging.getLogger(__name__)


def load_model(pipeline_params: PredictPipelineParams) -> SklearnClassifierModel:
    with open(pipeline_params.model_path, "rb") as f:
        model = pickle.load(f)

    logger.info(f"Loaded model: {model.__str__()}")

    return model


def load_transformer(pipeline_params: PredictPipelineParams) -> CustomTransformerClass:
    with open(pipeline_params.transformer_path, "rb") as f:
        transformer = pickle.load(f)

    return transformer


def save_inference_data(
    inference_data: Union[pd.Series, np.ndarray],
    pipeline_params: PredictPipelineParams
) -> None:
    create_directory(pipeline_params.output_inference_data_path)
    with open(pipeline_params.output_inference_data_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        for label in inference_data:
            csv_writer.writerow([label])


@hydra.main(config_path="../configs", config_name="default_predict_pipeline.yaml")
def run_predict(cfg: Union[DictConfig, PredictPipelineParams]) -> dict:
    init_hydra()
    
    logger.info("Started predict pipeline.")
    
    logger.info("Parse the config.")
    if isinstance(cfg, PredictPipelineParams):
        pipeline_params = cfg
    else:
        pipeline_params = get_predict_pipeline_params(dict(cfg))
    
    logger.info("Load data.")
    features = load_data(
        pipeline_params.input_data_path, pipeline_params.features, False
    )

    logger.info("Loading model.")
    model = load_model(pipeline_params)
    logger.info(f"Model: {model.__str__()}")

    logger.info("Loading transformer")
    transformer = load_transformer(pipeline_params)
    logger.info(f"Transformer: {transformer.__str__()}")

    features = transformer.transform(features)

    logger.info("Predicting.")
    inference_data = predict(model, features)

    if pipeline_params.save_output:
        logger.info("Saving results.")
        save_inference_data(inference_data, pipeline_params)


if __name__ == "__main__":
    run_predict()
