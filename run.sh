#!/usr/bin/env bash

SHELL_PATH=$(dirname -- "${BASH_SOURCE[0]}")
DATA_PATH="${SHELL_PATH}/data"
mkdir -p $DATA_PATH

site_type_list=("saramin")


for site_type in ${site_type_list[@]}; do
    python3 script/crawling.py \
       --site_type "$site_type" \
       --data_path "$DATA_PATH" \
       > "${DATA_PATH}/tokens.${site_type}.tsv"
done
