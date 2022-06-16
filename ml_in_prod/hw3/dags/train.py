import os
from datetime import timedelta

from airflow import DAG
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
DATA_PREPROCESS_PATH = "/data/processed/{{ ds }}"
DATA_SPLIT_PATH = "/data/split/{{ ds }}"
MODEL_PATH = "/data/models/{{ ds }}"

with DAG(
    "train",
    default_args=default_args,
    schedule_interval="@weekly",
    start_date=days_ago(5),
) as dag:
    data_sensor = FileSensor(
        fs_conn_id="connection_1",
        task_id="data-sensor",
        filepath="raw/{{ ds }}/data.csv"
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command=f"-l {DATA_RAW_PATH} -s {DATA_PREPROCESS_PATH}",
        network_mode="bridge",
        task_id="preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    split = DockerOperator(
        image="airflow-split",
        command=f"-l {DATA_PREPROCESS_PATH} -s {DATA_SPLIT_PATH}",
        network_mode="bridge",
        task_id="split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    train = DockerOperator(
        image="airflow-train",
        command=f"-d {DATA_SPLIT_PATH} -m {MODEL_PATH}",
        network_mode="bridge",
        task_id="train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    validation = DockerOperator(
        image="airflow-validation",
        command=f"-d {DATA_SPLIT_PATH} -m {MODEL_PATH}",
        network_mode="bridge",
        task_id="validation",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=HOST_DATA_DIR, target="/data", type='bind')]
    )

    data_sensor >> preprocess >> split >> train >> validation
