#!/usr/bin/env bash

set -e

cd /opt/georiviere-admin

# Activate venv
. /opt/venv/bin/activate

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $PGPORT; do
    sleep 0.1
done
echo "PostgreSQL started"

# exec
exec "$@"
