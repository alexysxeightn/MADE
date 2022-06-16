import os
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

HOST_DATA_DIR = os.environ["HOST_DATA_DIR"]
DATA_RAW_PATH = "/data/raw/{{ ds }}"
MODEL_PATH = Variable.get("predicting_model_path")
PREDICTIONS_PATH = "/data/predictions/{{ ds }}"

with DAG(
    "predict",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(5),
) as dag:
    data_sensor = FileSensor(
        fs_conn_id="connection_1",
        task_id="data-sensor",
        filepath="raw/{{ ds }}/data.csv"
    )

    predict = DockerOperator(
        image="airflow-predict",
        command=f"-d {DATA_RAW_PATH} -m {MODEL_PATH} -p {PREDICTIONS_PATH}",
        network_mode="bridge",
        task_id="predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    data_sensor >> predict