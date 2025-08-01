Install local Environment
=========================

Installation
------------

* Configuration

To get local environment working, we recommend to use a custom domain, as 'georiviere.local'.
Define it in your /etc/hosts.

Copy the env dist file

.. code-block :: bash

    cp .env.dist .env

Set required values, for postgres database access


* Init database:

.. code-block :: bash

    docker compose run --rm web ./manage.py migrate


* Create user:

.. code-block :: bash

    docker compose run --rm web ./manage.py createsuperuser


* Run:

.. code-block :: bash

    docker compose up


Tests
-----

* Launch tests :

.. code-block :: bash

    docker compose run --rm web ./manage.py test


* With coverage :

.. code-block :: bash

    docker compose run --rm web coverage run ./manage.py test
    docker compose run --rm web coverage report -m


Dependencies
------------

* Manage all project dependencies with pip-tools
* Use included pip-tools to generate requirements (python version should match georiviere version)


Global dependencies:

Set global dependency in requirements.in

.. code-block :: bash

    docker compose run --rm web pip-compile

**pip-tools** does not upgrade any package by default. Package is upgrade only if new dependency require another version that already fixed in requirements.txt file.

To upgrade a package, run:

.. code-block :: bash

    docker compose run --rm web pip-compile --upgrade-package django==3.1.*

Development packages are separated in dev-requirements.in. dev-requirements.txt depends on requirements.txt.

.. code-block :: bash

    docker compose run --rm web pip-compile dev-requirements.in

.. warning::
    Geotrek is used as main library of this project. Sub-dependencies are not yet managed in geotrek setup.py.
    When you update geotrek, you should update requirements according geotrek dependencies versions.
