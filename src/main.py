import hydra
from omegaconf import DictConfig

from process_data import process_data
from segment import segment
from run_notebook import run_notebook

@hydra.main(
    config_path="../config",
    config_name="main",
)
def main(config: DictConfig):

    process_data(config)
    segment(config)
    run_notebook(config)

if __name__ == "__main__":
    main()
