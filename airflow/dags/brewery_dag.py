from datetime import datetime, timedelta
import json
import requests
import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
from airflow import DAG
from airflow.operators.python import PythonOperator


# Define the file paths for the Bronze, Silver, and Gold layers
BRONZE_FILE_PATH = "/opt/airflow/layers/bronze"
SILVER_FILE_PATH = "/opt/airflow/layers/silver"
GOLD_FILE_PATH = "/opt/airflow/layers/gold"
CONTEXT = "brewery"


def extract_data():
    """
    Extracts data from the API and saves it to the Bronze layer.
    Sends a GET request to the brewery API and saves the retrieved
    data in JSON format to the Bronze layer.

    """
    print("Starting GET request")
    url = "https://api.openbrewerydb.org/breweries"
    response = requests.get(url)
    data = json.dumps(response.json())
    print(data)
    data_to_bronze(data)


def data_to_bronze(data) -> str:
    """
    Saves the extracted data to a CSV file in the Bronze layer.

    Args:
        data (str): The data in JSON format to be saved to the Bronze layer.

    """
    data_frame = pd.read_json(data)
    data_frame.to_csv(
        f"{BRONZE_FILE_PATH}/{CONTEXT}/bronze_{CONTEXT}.csv",
        index=False,
        mode="w",
        header=True,
    )


def data_to_silver():
    """
    Converts data from the Bronze layer to the Silver layer.
    Reads the data saved in the Bronze layer, transforms it as needed,
    and saves it to the Silver layer, partitioned by the brewery's state.
    """
    df = pd.read_csv(f"{BRONZE_FILE_PATH}/{CONTEXT}/bronze_{CONTEXT}.csv")
    print(df.to_markdown())

    write_deltalake(
        f"{SILVER_FILE_PATH}/{CONTEXT}/",
        df,
        partition_by=["state"],
        name=f"silver_{CONTEXT}",
        mode="overwrite",
    )


def data_to_gold():
    """
    Aggregates data from the Silver layer to the Gold layer.
    Groups the data by brewery type and state, counts the occurrences,
    and saves the result to the Gold layer.
    """
    df = DeltaTable(f"{SILVER_FILE_PATH}/{CONTEXT}/").to_pandas()
    df = (
        df.groupby(["brewery_type", "state"])
        .size()
        .reset_index(name="count")
        .sort_values(by="state")
    )
    print(df.to_markdown())

    write_deltalake(
        f"{GOLD_FILE_PATH}/{CONTEXT}/",
        data=df,
        name=f"gold_{CONTEXT}",
        mode="overwrite",
    )


# Define default arguments for the DAG
default_args = {
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG for the workflow
dag = DAG(
    dag_id="DAG_brewery_ingestion",
    description="ETL of Brewery data",
    default_args=default_args,
    start_date=datetime(2024, 8, 16),
    schedule="* 3 * * *",  # Custom scheduling
    catchup=False,
    tags=["brewery"],  # Tags for organization
)

# Define the tasks in the DAG
t1 = PythonOperator(task_id="bronze", python_callable=extract_data, dag=dag)

t2 = PythonOperator(task_id="silver", python_callable=data_to_silver, dag=dag)

t3 = PythonOperator(task_id="gold", python_callable=data_to_gold, dag=dag)

# Set task dependencies
t1 >> t2 >> t3
