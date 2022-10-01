import os
import warnings
from datetime import date

import pandas as pd
from dvc.api import DVCFileSystem
from omegaconf import DictConfig
from prefect import flow, task
from prefect.blocks.system import Secret
from sklearn.preprocessing import StandardScaler

from helper import load_config

warnings.simplefilter(action="ignore", category=UserWarning)


@task
def add_credentials():
    user = Secret.load("dagshub-user").get()
    password = Secret.load("dagshub-password").get()
    os.system(f"dvc remote modify --local origin user '{user}'")
    os.system(f"dvc remote modify --local origin password '{password}'")


@task
def download_data(git: DictConfig, raw_data: str) -> pd.DataFrame:
    fs = DVCFileSystem(git.url, rev=git.rev)
    fs.get_file(raw_data, raw_data)


@task
def read_data(raw_data: str) -> pd.DataFrame:
    return pd.read_csv(raw_data)


@task
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


@task
def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        age=df["Year_Birth"].apply(lambda row: date.today().year - row)
    )


@task
def get_total_children(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total_children=df["Kidhome"] + df["Teenhome"])


@task
def get_total_purchases(df: pd.DataFrame) -> pd.DataFrame:
    purchases_columns = df.filter(like="Purchases", axis=1).columns
    return df.assign(total_purchases=df[purchases_columns].sum(axis=1))


@task
def get_enrollment_years(df: pd.DataFrame) -> pd.DataFrame:
    df["Dt_Customer"] = pd.to_datetime(
        df["Dt_Customer"], infer_datetime_format=True
    )
    return df.assign(enrollment_years=2022 - df["Dt_Customer"].dt.year)


@task
def get_family_size(df: pd.DataFrame, size_map: dict) -> pd.DataFrame:
    return df.assign(
        family_size=df["Marital_Status"].map(size_map) + df["total_children"]
    )


@task
def drop_features(df: pd.DataFrame, keep_columns: list):
    df = df[keep_columns]
    return df


@task
def drop_outliers(df: pd.DataFrame, column_threshold: dict):
    for col, threshold in column_threshold.items():
        df = df[df[col] < threshold]
    return df.reset_index(drop=True)


@task
def get_scaler(df: pd.DataFrame):
    scaler = StandardScaler()
    scaler.fit(df)

    return scaler


@task
def scale_features(df: pd.DataFrame, scaler: StandardScaler):
    return pd.DataFrame(scaler.transform(df), columns=df.columns)


@flow(name="Process data")
def process_data():
    config = load_config()
    add_credentials()
    download_data(config.git, config.raw_data.path)
    df = read_data(config.raw_data.path)
    df = (
        df.pipe(drop_na)
        .pipe(get_age)
        .pipe(get_total_children)
        .pipe(get_total_purchases)
        .pipe(get_enrollment_years)
        .pipe(get_family_size, size_map=config.process.family_size)
        .pipe(drop_features, keep_columns=config.process.keep_columns)
        .pipe(
            drop_outliers,
            column_threshold=config.process.remove_outliers_threshold,
        )
    )
    scaler = get_scaler(df)
    df = scale_features(df, scaler)
    df.to_csv(config.intermediate.path, index=False)


if __name__ == "__main__":
    process_data()
