#!/usr/bin/env bash

set -e

cd /opt/georiviere-admin

./manage.py migrate --noinput
./manage.py clearsessions
./manage.py compilemessages
./manage.py collectstatic --clear --noinput --verbosity=0
./manage.py update_geotrek_permissions
rm -rf var/tmp/*
