=============
Configuration
=============

To customize lists for each module, go to django administration page.

.. image :: /images/georiviere-02-admin.png

* Description
    * Bank states
    * Facies diversities
    * Flow types
    * Granulometric diversities
    * Habitat types
    * Habitats diversities
    * Land types
    * Plan layout types
    * Sediment dynamics
    * Status types
    * Usage types
    * Working space types
* Finances and administration
    * Admin file domains
    * Admin file types
    * Administrative operations
    * Job categories
    * Organisms
* Knowledge
    * Age class diversities
    * Follow-up types
    * Knowledge types
    * Vegetations:
        * Specific diversities
        * Vegetation states
        * Vegetation stratas
        * Vegetation thickness types
        * Vegetation types
    * Work:
        * Work bank effects
        * Work fish continuity effects
        * Work materials
        * Work sediment effects
        * Work states
        * Work stream influences
        * Work types
* Main: File types
* Maintenance
    * Intervention's disorders
    * Intervention's stakes
    * Intervention's statuses
    * Intervention's types
    * Interventions
* Observations
    * Parameter categories
    * Parameters
    * Station profiles
    * Units
* Proceeding: Event types
* Studies Study types
* Watershed
    * Watershed types
    * Watersheds
* Zoning
    * Cities
    * Districts
    * Restricted area types
    * Restricted areas


Email settings
--------------

Georiviere-admin will send emails:

* to administrators when internal errors occur
* to managers when a contribution is created
* to contributors when a contribution is created

Email configuration takes place in ``var/conf/custom.py``, where you control
recipients emails (``ADMINS``, ``MANAGERS``) and email server configuration.

You can test your configuration with the following command. A fake email will
be sent to the managers:

::

    docker-compose run --rm web ./manage.py sendtestemail --managers

If you don't want to send an email to contributors when they create a contribution on portal website,
change this setting in ``var/conf/custom.py``:

::

    SEND_REPORT_ACK = False
