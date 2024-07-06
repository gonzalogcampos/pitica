#!/bin/bash
#
# Copyright Gonzalo G. Campos, 2024
#

SCRIPT_PATH="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"


pushd ${SCRIPT_PATH}/../src
    python3 -m build -o ${SCRIPT_PATH}/dist/
    rm -rf pitica.egg-info
    pip install -e .
popd