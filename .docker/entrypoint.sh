#!/usr/bin/env bash

set -e

# Activate venv
. /opt/venv/bin/activate

mkdir -p /opt/georiviere-admin/var/static \
         /opt/georiviere-admin/var/conf/extra_static \
         /opt/georiviere-admin/var/media/upload \
         /opt/georiviere-admin/var/data \
         /opt/georiviere-admin/var/cache \
         /opt/georiviere-admin/var/log \
         /opt/georiviere-admin/var/conf/extra_templates \
         /opt/georiviere-admin/var/conf/extra_locale \
         /opt/georiviere-admin/var/tmp

# if not custom.py present, create it
if [ ! -f /opt/georiviere-admin/var/conf/custom.py ]; then
    cp /opt/georiviere-admin/georiviere/settings/custom.dist.py /opt/georiviere-admin/var/conf/custom.py
fi

# Defaults SECRET_KEY to a random value
SECRET_KEY_FILE=/opt/georiviere-admin/var/conf/secret_key
if [ -z $SECRET_KEY ]; then
    if [ ! -f $SECRET_KEY_FILE ]; then
        echo "Generate a secret key"
        dd bs=48 count=1 if=/dev/urandom 2>/dev/null | base64 > $SECRET_KEY_FILE
        chmod go-r $SECRET_KEY_FILE
    fi
    export SECRET_KEY=`cat $SECRET_KEY_FILE`
fi

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "PostgreSQL started"

# exec
exec "$@"
