Import data
===========

To import data, you have to run these commands from the server where Georiviere-admin is hosted.

Import altimetry file
---------------------

Put your altimetry file in ``var/`` folder, and run command

.. code-block :: bash

    docker-compose run --rm web ./manage.py loaddem <dem_path>

where ``<dem_path>`` is ``/opt/georiviere-admin/var/my_dem_file.tiff``

Import stations from Hub'Eau
----------------------------

Stations can be imported from french Hub'Eau APIs :

- Temperature stations with ``import_temperature_stations``
- Hydrometry with ``import_hydrometric_stations``
- Physico-chemical quality with ``import_pcquality_stations``

Optional arguments::

    --department DEPARTMENT [DEPARTMENT ...]
                          Department code
    -p, --with-parameters
                          Get also parameter tracked by the station
    --size SIZE           Results per page

Example:

.. code-block :: bash

    docker-compose run --rm web ./manage.py import_pcquality_stations --department 39,25

Import data references from Sandre
----------------------------------

Some data references can be imported from Sandre, for now only units are imported.

Usage:

.. code-block :: bash

    docker-compose run --rm web ./manage.py import_reference_data

Import zoning data from file
----------------------------

Put your files into ``var/`` folder as for altimetry profile import.

Load cities
'''''''''''

Load Cities from a file within the spatial extent : ``loadcities <file_path>``

Optional arguments:::

      --code-attribute CODE, -c CODE
                            Name of the code's attribute inside the file
      --name-attribute NAME, -n NAME
                            Name of the name's attribute inside the file
      --encoding ENCODING, -e ENCODING
                            File encoding, default utf-8
      --srid SRID, -s SRID  File's SRID
      --intersect, -i       Check features intersect spatial extent and not only within

Load districts
''''''''''''''

Load Districts from a file within the spatial extent ``loaddistricts <file_path>``

Optional arguments:::

      -h, --help            show this help message and exit
      --name-attribute NAME, -n NAME
                            Name of the name's attribute inside the file
      --encoding ENCODING, -e ENCODING
                            File encoding, default utf-8
      --srid SRID, -s SRID  File's SRID
      --intersect, -i       Check features intersect spatial extent and not only within

Load Restricted Area from a file within the spatial extent ``loadrestrictedareas <file_path>``

Optional arguments:::

      -h, --help            show this help message and exit
      --name-attribute NAME, -n NAME
                            Name of the name's attribute inside the file
      --encoding ENCODING, -e ENCODING
                            File encoding, default utf-8
      --srid SRID, -s SRID  File's SRID
      --intersect, -i       Check features intersect spatial extent and not only within
