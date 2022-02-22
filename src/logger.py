from dataclasses import dataclass

import mlflow
from dagshub import DAGsHubLogger


@dataclass
class BaseLogger:
    log_type: str = "mlflow"

    def __post_init__(self):
        if self.log_type == "dagshub":
            self.logger = DAGsHubLogger()

    def log_metrics(self, metrics: dict):
        if self.log_type == "mlflow":
            mlflow.log_metrics(metrics)
        elif self.log_type == "dagshub":
            self.logger.log_metrics(metrics)
        else:
            raise ValueError(f"log type {self.log_type} not found")

    def log_params(self, params: dict):
        if self.log_type == "mlflow":
            mlflow.log_params(params)
        elif self.log_type == "dagshub":
            self.logger.log_hyperparams(params)
        else:
            raise ValueError(f"log type {self.log_type} not found")
