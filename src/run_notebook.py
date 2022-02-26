from omegaconf import DictConfig
import papermill as pm
from omegaconf import DictConfig

def run_notebook(config: DictConfig):
    pm.execute_notebook(
        "notebook/analyze_data.ipynb",
        "notebook/analyze_data_out.ipynb",
        parameters=dict(columns=list(config.process.keep_columns)),
    )

