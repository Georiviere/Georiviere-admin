Local Environment
-----------------

* Configuration

To get local environment working, we recommend to use a custom domain, as 'georiviere.local'.
Define it in your /etc/hosts.

Copy the env dist file

.. code-block :: bash

    cp .env.dist .env

Set required values, for postgres database access


* Run:

.. code-block :: bash

    docker-compose up


* Launch tests :

.. code-block :: bash

    docker-compose run ./manage.py test


* With coverage :

.. code-block :: bash

    docker-compose run coverage run ./manage.py test
    docker-compose run coverage report -m


Documentation
-------------

We use sphinx doc and sphinx-rtd-theme.

Requirements are included.

To compile and test documentation on local environment, run :

.. code-block :: bash

    docker-compose run --workdir /opt/georiviere-admin/docs --rm web make html
