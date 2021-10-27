#!/usr/bin/env bash

set -e

cd /code/src

# Activate venv
. /code/venv/bin/activate

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $PGPORT; do
    sleep 0.1
done
echo "PostgreSQL started"

# exec
exec "$@"
