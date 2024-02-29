Requirements
============

* You need docker installed on your system.
    See `Docker <https://docs.docker.com/engine/install/>`_ install documentations.

* **Optional** : if you want to use external database, prepare a postgresql 10+ postgis2.5+ database with postgis, postgis_raster and unaccent enabled, and a dedicated user.

    You can use external database by commenting postgres container and volume references in docker-compose.yml, and set variables :
        * POSTGRES_HOST
        * PGPORT
        * POSTGRES_USER
        * POSTGRES_PASSWORD
        * POSTGRES_DB

Add local IPs in `pg_hba.conf` to allow connection from docker containers to your database.

* You can use external nginx proxy. Edit provided nginx conf file and comment nginx references in docker-compose.yml. Fix web:8000 to 127.0.0.1:8000 in nginx.conf.


Install
=======

* Download `zip package <https://github.com/Georiviere/Georiviere-admin/releases/latest/download/install.zip>`_

  .. code-block :: bash

      wget https://github.com/Georiviere/Georiviere-admin/releases/latest/download/install.zip


* Unzip it where you want

  .. code-block :: bash

      unzip install.zip
      cd georiviere


* Prepare environment variables

  .. code-block :: bash

      mv .env.dist .env

  **-> Set all required values**

* Pull images

  .. code-block :: bash

      docker compose pull


* Init default var folder

  .. code-block :: bash

      docker compose run --rm web bash -c "exit"

* Set at least these variables in ``var/conf/custom.py``:
    * ``SRID``
    * ``DEFAULT_STRUCTURE_NAME``
    * ``SPATIAL_EXTENT``

    As geotrek overlay, these settings should be set BEFORE database initialization.
    See :doc:`./settings` for details

* Init database and project config

  .. code-block :: bash

      docker compose run --rm web update.sh

* Create your super user

  .. code-block :: bash

      docker compose run --rm web ./manage.py createsuperuser

* Load initial data

  .. code-block :: bash

      docker compose run --rm web ./manage.py loaddata georiviere/contribution/fixtures/basic.json georiviere/description/fixtures/basic.json georiviere/finances_administration/fixtures/basic.json georiviere/knowledge/fixtures/basic.json georiviere/main/fixtures/basic.json georiviere/maintenance/fixtures/basic.json georiviere/observations/fixtures/basic.json georiviere/proceeding/fixtures/basic.json georiviere/river/fixtures/basic.json georiviere/studies/fixtures/basic.json georiviere/valorization/fixtures/basic.json

* Launch stack

  .. code-block :: bash

      docker compose up -d


Update
============

* Read `release notes <https://github.com/Georiviere/Georiviere-admin/releases>`_ about bugfix, news and breaking changes.

* Backup your data (database and var folder)

* Pull latest image

  .. code-block :: bash

      docker compose pull


* Run post update script

  .. code-block :: bash

      docker compose run --rm web update.sh


* Relaunch you docker-compose stack

  .. code-block :: bash

      docker compose down
      docker compose up -d
