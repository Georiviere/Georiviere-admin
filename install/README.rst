INSTALL
=======

Requirements
------------
* You need docker, docker-compose and nginx
* Optional : if you want to use external database, prepare a postresql database with postgis enable and dedicated user.

* You can use external database by commenting postgres references in docker-compose.yml
  * set POSTGRES_HOST, POSTGRES_USER and POSTGRES_DATABASE variables in .env

Install
-------

* Go to https://github.com/Georiviere/Georiviere-admin/releases and download last release install.zip asset
* Unzip it where you want and enter it
  * unzip install.zip
  * mv install georiviere
  * cd georiviere
* Prepare environment variables
  * cp .env.dist .env
  * -> Set all required values
* Set default var folder
  * docker-compose run --rm web exit
* Set your var/conf/custom.py if required (as geotrek overlay, some settings should be set BEFORE database initialization)
* Init database and project config
  * docker-compose run --rm web update.sh
* Create your super user
  * docker-compose run --rm web ./manage.py createsuperuser
* Launch
  * docker-compose up

Update
------

* Read `release notes <https://github.com/Georiviere/Georiviere-admin/releases>` about bugfix, news and breaking changes.
* Backup your data (database and var folder)
* Pull latest image
  * docker-compose pull
* Run post update script
  * docker-compose run --rm web update.sh
* Relaunch you docker-compose stack
  * docker-compose down
  * docker-compose up
