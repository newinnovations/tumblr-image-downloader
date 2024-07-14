#!/bin/bash

SCRIPT_DIR=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")

cd "${SCRIPT_DIR}"

. activate

python3 ./tumblr.py
