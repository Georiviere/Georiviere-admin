#!/usr/bin/env bash

set -e

cd /opt/georiviere-admin

./manage.py loaddata georiviere/**/fixtures/basic.json

# copy media files for fixtures
for dir in `find georiviere/ -type d -name upload`; do pushd `dirname $$dir` > /dev/null && cp -R $dir/* /opt/georiviere-admin/var/media/upload/ && popd > /dev/null; done
