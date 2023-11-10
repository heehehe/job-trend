#!/usr/bin/python

import os
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

SITE_LIST = {"jumpit"}
DEFAULT_ARGS = {
    'owner': 'DE4E',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

DIR_PATH=os.path.abspath(__file__)
SCRIPT_PATH=f"{DIR_PATH}/../script"
DATA_PATH=f"{DIR_PATH}/../data"


with DAG(
    dag_id='job_trend_daily',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily'
) as dag:
    crawling_tasks = [
        BashOperator(
            task_id=f'crawling_{site}',
            bash_command=f'python3 {SCRIPT_PATH}/crawling.py -s "{site}" -d {DATA_PATH}'
        ) for site in SITE_LIST
    ]

    upload_task = BashOperator(
        task_id = 'upload_to_bigquery',
        bash_command = f'python3 {SCRIPT_PATH}/upload_to_bigquery.py'
    )

    crawling_tasks >> upload_task
