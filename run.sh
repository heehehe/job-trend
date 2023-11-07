#!/usr/bin/env bash

SHELL_PATH=$(dirname -- "${BASH_SOURCE[0]}")
SCRIPT_PATH="${SHELL_PATH}/script"
DATA_PATH="${SHELL_PATH}/data"

mkdir -p "$DATA_PATH"

SITE_LIST=("jumpit")


for site_type in "${SITE_LIST[@]}"; do
    python3 ${SCRIPT_PATH}/crawling.py \
       --site_type "$site_type" \
       --data_path "$DATA_PATH"

    cut -f3 "${DATA_PATH}/url.${site_type}.tsv" \
        python3 ${SCRIPT_PATH}/tokenizing.py \
        > "${DATA_PATH}/tokens.${site_type}.tsv"

done

python3 ${SCRIPT_PATH}/upload_to_bigquery.py
