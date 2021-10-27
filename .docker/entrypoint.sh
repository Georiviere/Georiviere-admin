#!/usr/bin/env bash

set -e

cd /code/src

# Activate venv
. /code/venv/bin/activate

# exec
exec "$@"
