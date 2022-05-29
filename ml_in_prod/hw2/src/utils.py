import os

from hydra.core.hydra_config import HydraConfig
from hydra.utils import get_original_cwd
from omegaconf import DictConfig


def create_directory(file_path: str) -> None:
    """
    Creates a directory for a file_path if directory doesn't exist.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.mkdir(directory)


def init_hydra() -> None:
    """
    The function is needed to use relative paths in configs
    (because hydra changes the working directory)
    """
    if HydraConfig.initialized():
        os.chdir(get_original_cwd())
