from prefect import flow

from process_data import process_data
from segment import segment


@flow(name="Process and segment customers")
def main():
    process_data()
    segment()


if __name__ == "__main__":
    main()
