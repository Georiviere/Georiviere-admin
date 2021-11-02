INSTALL
=======

Requirements
------------
* You need docker, docker-compose and nginx
* Optional : if you want to use external database, prepare a postresql database with postgis enable and dedicated user.



* You can use external database by commenting postgres references in docker-compose.yml
  * set POSTGRES_HOST, POSTGRES_USER and POSTGRES_DATABASE variables in .env
