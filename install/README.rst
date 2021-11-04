Requirements
============
* You need docker installed. Docker-compose is recommended in the configuration below.
* Optional : if you want to use external database, prepare a postresql database with postgis enable and dedicated user.

* You can use external database by commenting postgres references in docker-compose.yml
  * set POSTGRES_HOST, POSTGRES_USER and POSTGRES_DATABASE variables in .env

* You can use external nginx proxy. Use and edit provided nginx conf file.


Install
=======

* Download `zip package <https://github.com/Georiviere/Georiviere-admin/releases/latest/download/install.zip>`_
* Unzip it where you want and enter it

.. code-block :: bash

    unzip install.zip
    cd georiviere

* Prepare environment variables

.. code-block :: bash
    cp .env.dist .env

* -> Set all required values

* Set default var folder

.. code-block :: bash
    mkdir var
    docker-compose run --rm web bash -c "exit"

* Set your var/conf/custom.py if required (as geotrek overlay, some settings should be set BEFORE database initialization)

* Init database and project config

  .. code-block :: bash
      docker-compose run --rm web update.sh

* Create your super user

  .. code-block :: bash
      docker-compose run --rm web ./manage.py createsuperuser


* Launch stack

  .. code-block :: bash
      docker-compose up


Update
============

* Read `release notes <https://github.com/Georiviere/Georiviere-admin/releases>`_ about bugfix, news and breaking changes.

* Backup your data (database and var folder)

* Pull latest image

  .. code-block :: bash
      docker-compose pull

* Run post update script

  .. code-block :: bash
      docker-compose run --rm web update.sh

* Relaunch you docker-compose stack

  .. code-block :: bash
      docker-compose down
      docker-compose up
