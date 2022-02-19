import dagshub
import hydra
from omegaconf import DictConfig, OmegaConf

from process_data import process_data
from segment import segment


@hydra.main(
    config_path="../config",
    config_name="main",
)
def main(config: DictConfig):

    with dagshub.dagshub_logger() as logger:

        if config.flow == "all":
            process_data(config, logger)
            segment(config, logger)

        elif config.flow == "process_data":
            process_data(config, logger)

        elif config.flow == "segment":
            segment(config, logger)

        else:
            print("flow not found")


if __name__ == "__main__":
    main()
