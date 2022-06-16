import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

HOST_DATA_DIR = os.environ["HOST_DATA_DIR"]
DATA_SAVE_PATH = "/data/raw/{{ ds }}"

with DAG(
    "download",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(10),
) as dag:
    download = DockerOperator(
        image="airflow-download",
        command=f"-s {DATA_SAVE_PATH}",
        network_mode="bridge",
        task_id="download",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    download
