.. _basic-settings-section:

Basic settings
==============

Settings can be overriden in ``var/conf/custom.py`` file.

Basic settings should be defined on installation.
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
