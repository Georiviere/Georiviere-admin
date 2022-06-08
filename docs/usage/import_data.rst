Import data
===========

To import data, you have to run these commands from the server where GeoRiviere-admin is hosted.

Import data
---------------------

Put your data file named CoursEau_FXX.shp in ``var/`` folder, and run command

Custom your import file named import_bdtopage.py et put this file in ``georiviere/``

.. code-block :: bash

	#!/usr/bin/env python
	import os
	import django
	import logging
	from django.contrib.gis.gdal import DataSource

	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'georiviere.settings')
	django.setup()
	from geotrek.authent.models import Structure
	from django.contrib.gis.geos.collections import MultiLineString
	from georiviere.river.models import Stream

	# get first structure, adapt with correct structure
	structure = Structure.objects.first()

	ds = DataSource('var/CoursEau_FXX.shp')

	for feat in ds[0][4:]:
		try:
			# get geos object
			geom = feat.geom.geos
			# force 2D
			geom.dim = 2
			name = feat.get('name') or 'No name'
			flow = feat.get('flow')
			if flow == 1:
				flow = 1
			elif flow == 2:
				flow = 2
			else:
				flow = 0
			stream = Stream.objects.create(structure=structure,
										geom=feat.geom.geos,
										name=name,
										flow=flow)

		except Exception as exc:
			logging.warn(exc, feat.geom.geos.ewkt)

And run command : `docker compose run --rm web ./import_bdtopage.py`


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
- Hydrobilogy stations with ``import_hydrobiologie_stations``

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

Example:

.. code-block :: bash

    docker compose run --rm web ./manage.py loadcities /opt/georiviere-admin/var/commune.shp --name-attribute nom --code-attribute insee_com


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

Example:

.. code-block :: bash

    docker compose run --rm web ./manage.py loaddistricts /opt/georiviere-admin/var/epci.shp --name-attribute nom --code-attribute code_siren


Load Restricted Area
''''''''''''''''''''

Load Restricted Area from a file within the spatial extent ``loadrestrictedareas <file_path>`` and specify the name of the Area type

Optional arguments:::

      -h, --help            show this help message and exit
      --name-attribute NAME, -n NAME
                            Name of the name's attribute inside the file
      --encoding ENCODING, -e ENCODING
                            File encoding, default utf-8
      --srid SRID, -s SRID  File's SRID
      --intersect, -i       Check features intersect spatial extent and not only within

Example:

.. code-block :: bash

    docker compose run --rm web ./manage.py loadrestrictedareas /opt/georiviere-admin/var/pnrhj.shp PNR --name-attribute nom
	

Import watershed
''''''''''''''''
To import, use QGIS and edit watershed_watershed layer and specify "name" and  "watershed_type_id" in attributes

Import sensibility areas from https://biodiv-sports.fr
'''''''''''''''''''''''''''''''''''''''''''''''''''''
Configure parser.py in /georiviere/var/conf like 

.. code-block :: bash
    
    from geotrek.sensitivity.parsers import BiodivParser

    class PNRHJBiodivParser(BiodivParser):
        url = 'https://biodiv-sports.fr/api/v2/sensitivearea/?format=json&bubble&period=ignore&practice=5'
        label = "Biodiv'Sports PNRHJ"

Mors informations  : https://geotrek.ecrins-parcnational.fr/ressources/gt/01-zones-sensibilite/doc-import.pdf

.. code-block :: bash

    docker-compose run --rm web ./manage.py import_parser -v 2 BiodivParser
