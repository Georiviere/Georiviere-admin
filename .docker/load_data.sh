#!/usr/bin/env bash

set -e

cd /opt/georiviere-admin

./manage.py loaddata georiviere/**/fixtures/basic.json
