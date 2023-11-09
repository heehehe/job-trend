#!/usr/bin/python

import os
import sys
import json
import yaml
from pathlib import Path
from glob import glob
from google.cloud import bigquery

FILE_PATH = Path(__file__).resolve().parent
ENVS_PATH = os.path.join(FILE_PATH, "../envs")
DATA_PATH = os.path.join(FILE_PATH, "../data")


def main():
    with open(os.path.join(ENVS_PATH, 'bigquery.config.yml')) as f:
        bigquery_config = yaml.load(f, Loader=yaml.Loader)

    data_list = []
    for file in glob(os.path.join(DATA_PATH, '*.content.info.jsonl')):
        with open(file) as f:
            for data in f:
                data_json = json.loads(data)
                for key, value in data_json.items():
                    if value == '':
                        data_json[key] = None
                data_list.append(data_json)

    client = bigquery.Client.from_service_account_json(
        os.path.join(ENVS_PATH, bigquery_config['service_account_json'])
    )

    dataset_reference = bigquery.DatasetReference(
        client.project, bigquery_config['dataset_id']
    )
    table_reference = bigquery.TableReference(
        dataset_reference, bigquery_config['table_id']
    )

    response = client.insert_rows_json(
        table_reference, data_list
    )

    if response:
        sys.stderr.write("[ERROR]")
        # sys.stderr.write(response)
        for i in response :
            sys.stderr.write(str(i))



if __name__ == "__main__":
    main()
