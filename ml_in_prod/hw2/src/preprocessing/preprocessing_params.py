from dataclasses import dataclass, field


@dataclass()
class PreprocessingParams:
    transformer_type: str = field(default="OneHotTransformer")
