#!/usr/bin/env bash

set -e

cd /opt/georiviere-admin

# Activate venv
. /opt/venv/bin/activate

mkdir -p var/static \
         var/conf/extra_static \
         var/media/upload \
         var/data \
         var/cache \
         var/log \
         var/conf/extra_templates \
         var/conf/extra_locale \
         var/tmp

# if not custom.py present, create it
if [ ! -f var/conf/custom.py ]; then
    cp georiviere/settings/custom.py.dist var/conf/custom.py
fi

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $PGPORT; do
    sleep 0.1
done
echo "PostgreSQL started"

# exec
exec "$@"
