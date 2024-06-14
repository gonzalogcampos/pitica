#!/bin/bash
#
# Copyright Gonzalo G. Campos, 2024
#

SCRIPT_PATH="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

python3 -m pitica -d ${SCRIPT_PATH}/generated -c
