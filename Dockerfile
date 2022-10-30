FROM prefecthq/prefect:2.3.1-python3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt