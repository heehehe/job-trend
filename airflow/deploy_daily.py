#!/usr/bin/python

import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator


DEFAULT_ARGS = {
    'owner': 'admin',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 3, 10)
}

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = f"{DIR_PATH}/../script"
DATA_PATH = f"{DIR_PATH}/../data"
DBT_PROJECT_PATH = f"{DIR_PATH}/../dbt_project"

if SCRIPT_PATH not in sys.path:
    sys.path.append(SCRIPT_PATH)

from crawling import CrawlingJumpit, CrawlingJobPlanet, CrawlingWanted

CRAWLING_CLASS = {
    "jumpit": CrawlingJumpit(data_path=DATA_PATH),
    "jobplanet": CrawlingJobPlanet(data_path=DATA_PATH),
    "wanted": CrawlingWanted(data_path=DATA_PATH)
}


with DAG(
    dag_id='job_trend_daily',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily'
) as dag:
    get_url_list = {}
    get_recruit_content_info = {}
    postprocess = {}

    for crawler_name, crawler in CRAWLING_CLASS.items():
        get_url_list[crawler_name] = PythonOperator(
            task_id=f"{crawler_name}.get_url_list",
            python_callable=crawler.get_url_list
        )
        get_recruit_content_info[crawler_name] = PythonOperator(
            task_id=f"{crawler_name}.get_recruit_content_info",
            python_callable=crawler.get_recruit_content_info
        )
        postprocess[crawler_name] = PythonOperator(
            task_id=f"{crawler_name}.postprocess",
            python_callable=crawler.postprocess
        )

    upload_to_bigquery = BashOperator(
        task_id='upload_to_bigquery',
        bash_command=f'python3 {SCRIPT_PATH}/upload_to_bigquery.py'
    )

    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command=f'cd {DBT_PROJECT_PATH}; dbt run'
    )

    for crawler_name in CRAWLING_CLASS.keys():
        get_url_list[crawler_name] >> get_recruit_content_info[crawler_name] >> postprocess[crawler_name] >> upload_to_bigquery

    upload_to_bigquery >> run_dbt
