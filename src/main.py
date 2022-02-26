import dagshub
import hydra
import mlflow
from omegaconf import DictConfig

from logger import BaseLogger
from process_data import process_data
from segment import segment


@hydra.main(
    config_path="../config",
    config_name="main",
)
def main(config: DictConfig):

    logger = BaseLogger()

    mlflow.set_tracking_uri(
        "https://dagshub.com/khuyentran1401/customer_segmentation_demo.mlflow"
    )
    with mlflow.start_run():

        logger.log_params(dict(config.process))
        logger.log_params({"num_columns": len(config.process.keep_columns)})

        if config.flow == "all":
            process_data(config)
            segment(config, logger)

        elif config.flow == "process_data":
            process_data(config)

        elif config.flow == "segment":
            segment(config, logger)

        else:
            print("flow not found")


if __name__ == "__main__":
    main()
