#!/usr/bin/env bash

SHELL_PATH=$(dirname -- "${BASH_SOURCE[0]}")

# upgrade pip
pip3 install --upgrade pip

# install cmake for kiwipiepy (https://github.com/bab2min/kiwipiepy)
pip3 install cmake

# install packages in requirements.txt
pip3 install -r "${SHELL_PATH}/requirements.txt"
