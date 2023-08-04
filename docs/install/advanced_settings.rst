Advanced settings
=================

More settings can be overriden in ``var/conf/custom.py`` file.

After any change in custom.py, run:

.. code-block :: bash

	docker compose restart

Georiviere settings
-------------------

Base intersection margin

::

    BASE_INTERSECTION_MARGIN = 2000


Based on Geotrek or Mapentity settings
--------------------------------------

Some settings come from Geotrek-admin or Mapentity, on which Georiviere is based:

* `Email settings <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#email-settings>`_
* `Change or add WMTS tiles layers <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#change-or-add-wmts-tiles-layers-ign-osm-mapbox>`_
* `Map layers colors and style <https://geotrek.readthedocs.io/en/master/advanced-configuration.html#map-layers-colors-and-style>`_

See `Geotrek-admin documentation <https://geotrek.readthedocs.io/en/master/advanced-configuration.html>`_ for further information.


Override translations
---------------------

You can override default translation files available in each module

Don't edit these default files, use them to find which words you want to override.

Create the custom translations destination folder:

Create a ``django.po`` file in ``var/conf/extra_locale`` directory.
You can do one folder and one ``django.po`` file for each language
(example ``var/conf/extra_locale/fr/LC_MESSAGES/django.po`` for French translation overriding)

Override the translations that you want in these files.

Example of content for the French translation overriding:

::

    # MY FRENCH CUSTOM TRANSLATION
    # Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
    # This file is distributed under the same license as the PACKAGE package.
    # FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
    #
    msgid ""
    msgstr ""
    "Report-Msgid-Bugs-To: \n"
    "POT-Creation-Date: 2018-11-15 15:32+0200\n"
    "PO-Revision-Date: 2018-11-15 15:33+0100\n"
    "Last-Translator: \n"
    "Language-Team: LANGUAGE <LL@li.org>\n"
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "Project-Id-Verésion: PACKAGE VERSION\n"
    "Plural-Forms: nplurals=2; plural=(n > 1);\n"
    "Project-Id-Version: \n"
    "X-Generator: Poedit 1.5.4\n"

    msgid "City"
    msgstr "Région"

    msgid "District"
    msgstr "Pays"

Apply changes (French translation in this example) :

::

    sudo docker-compose run --rm web update.sh
