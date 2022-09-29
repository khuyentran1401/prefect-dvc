import matplotlib.pyplot as plt
from prefect import flow, task


@task
def plot():
    fig = plt.figure()
    fig.plot([1, 2, 3], [1, 2, 3])


@flow
def main():
    plot.submit()


if __name__ == "__main__":
    main()
