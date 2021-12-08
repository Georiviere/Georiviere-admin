Settings
========

Settings can be overriden in `/opt/georiviere-admin/var/conf/custom.py` file.


Basic settings
--------------

These settings should be defined on installation.
See `Geotrek-admin documentation <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#basic-settings>`
for details.


Spatial reference identifier
''''''''''''''''''''''''''''

::

    SRID = 2154

Spatial reference identifier of your database. Default 2154 is RGF93 / Lambert-93 - France


Default Structure
'''''''''''''''''

::

    DEFAULT_STRUCTURE_NAME = "GEOTEAM"

Name for your default structure.


Translations
''''''''''''

::

   MODELTRANSLATION_LANGUAGES = ('en', 'fr', 'it', 'es')

Languages of your project. It will be used to generate fields for translations. (ex: description_fr, description_en)


Spatial Extent
''''''''''''''

::

    SPATIAL_EXTENT = (105000, 6150000, 1100000, 7150000)

Boundingbox of your project : x minimum , y minimum , x max, y max


Georiviere settings
-------------------

Base intersection margin

::

    BASE_INTERSECTION_MARGIN = 2000


Based on Geotrek or Mapentity settings
--------------------------------------

Some settings come from Geotrek-admin:

* `Email settings <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#email-settings>`_
* `Change or add WMTS tiles layers <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#change-or-add-wmts-tiles-layers-ign-osm-mapbox>`_
* `Map layers colors and style <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#map-layers-colors-and-style>`_

See `Geotrek-admin <https://geotrek.readthedocs.io/en/master/advanced-configuration.html>`_ for further information.
