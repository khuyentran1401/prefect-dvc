import pickle
import warnings
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from omegaconf import DictConfig
from prefect import flow, task
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer

from helper import create_parent_directory, load_config

warnings.simplefilter(action="ignore", category=DeprecationWarning)


@task
def read_process_data(config: DictConfig):
    return pd.read_csv(config.intermediate.path)


@task
def get_pca_model(data: pd.DataFrame) -> PCA:

    pca = PCA(n_components=3)
    pca.fit(data)
    return pca


@task
def reduce_dimension(df: pd.DataFrame, pca: PCA) -> pd.DataFrame:
    return pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])


@task
def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


@task
def get_best_k_cluster(
    pca_df: pd.DataFrame, config: DictConfig
) -> pd.DataFrame:

    matplotlib.use("svg")
    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(111)

    elbow = KElbowVisualizer(KMeans(), metric="distortion")
    elbow.fit(pca_df)

    create_parent_directory(config.image.kmeans)
    elbow.fig.savefig(config.image.kmeans)

    k_best = elbow.elbow_value_
    return k_best


@task
def get_clusters_model(
    pca_df: pd.DataFrame, k: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    model = KMeans(n_clusters=k)

    # Fit model
    return model.fit(pca_df)


@task
def predict(model, pca_df: pd.DataFrame):
    return model.predict(pca_df)


@task
def insert_clusters_to_df(
    df: pd.DataFrame, clusters: np.ndarray
) -> pd.DataFrame:
    return df.assign(clusters=clusters)


@task
def plot_clusters(
    pca_df: pd.DataFrame,
    preds: np.ndarray,
    projections: dict,
    config: DictConfig,
) -> None:
    pca_df["clusters"] = preds
    matplotlib.use("svg")
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, projection="3d")
    ax.scatter(
        projections["x"],
        projections["y"],
        projections["z"],
        s=40,
        c=pca_df["clusters"],
        marker="o",
        cmap="Accent",
    )
    ax.set_title("The Plot Of The Clusters")

    plt.savefig(config.image.clusters)


@task
def save_data_and_model(data: pd.DataFrame, model: KMeans, config: DictConfig):
    create_parent_directory(config.final.path)
    data.to_csv(config.final.path, index=False)

    create_parent_directory(config.model.path)
    pickle.dump(model, open(config.model.path, "wb"))


@flow(name="Segment customers")
def segment() -> None:

    config = load_config()
    data = read_process_data(config)
    pca = get_pca_model(data)
    pca_df = reduce_dimension(data, pca)
    projections = get_3d_projection(pca_df)
    k_best = get_best_k_cluster(pca_df, config)
    model = get_clusters_model(pca_df, k_best)
    predictions = predict(model, pca_df)
    data = insert_clusters_to_df(data, predictions)
    plot_clusters(
        pca_df,
        predictions,
        projections,
        config,
    )
    save_data_and_model(data, model, config)


if __name__ == "__main__":
    segment()
