"""
Script for generate EDA report
"""
import os

import hydra
import pandas as pd
from omegaconf import DictConfig
from pandas_profiling import ProfileReport
from src.train_pipeline_params import get_training_pipeline_params, TrainingPipelineParams
from src.utils import init_hydra

def make_report(params: TrainingPipelineParams):
    data = pd.read_csv(params.input_data_path)
    ProfileReport(data, title="EDA report").to_file(params.report_path)
    
    
@hydra.main(config_path="configs", config_name="default_train_pipeline")
def make_report_command(cfg: DictConfig):
    init_hydra()
    
    if isinstance(cfg, TrainingPipelineParams):
        params = cfg
    else:
        params = get_training_pipeline_params(dict(cfg))
        
    make_report(params)
    
    
if __name__ == "__main__":
    make_report_command()
