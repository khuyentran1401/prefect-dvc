from pathlib import Path

from hydra import compose, initialize
from prefect import task


@task
def load_config():
    """Load configurations from the file `main.yaml` under the `config` directory"""
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config


def create_parent_directory(path: str):
    parent_dir = Path(path).parent
    parent_dir.mkdir(exist_ok=True)
