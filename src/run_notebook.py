from omegaconf import DictConfig
import papermill as pm
from omegaconf import DictConfig
import hydra 

@hydra.main(
    config_path="../config",
    config_name="main",
)
def run_notebook(config: DictConfig):
    pm.execute_notebook(
        "notebook/analyze_data.ipynb",
        "notebook/analyze_data_out.ipynb",
        parameters=dict(columns=list(config.process.keep_columns)),
    )

if __name__ == "__main__":
    run_notebook()

