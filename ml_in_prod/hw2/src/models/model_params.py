from dataclasses import dataclass


@dataclass()
class ModelParams:
    model_type: str
    params: dict
