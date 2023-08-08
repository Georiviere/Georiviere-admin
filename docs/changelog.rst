=========
CHANGELOG
=========

1.2.0+dev    (XXXX-XX-XX)
-------------------------

**Documentation**

* Add documentation api swagger / doc

**Enhancement**

* Add contributions linked on details of knowledge / interventions / followups
* Filter api portal elements without accents and uppercase
* Add detail sentivities portal

1.2.0        (2023-08-04)
-------------------------

**Documentation**

* Add documentation portals
* Add documentation distance to source

**Enhancement**

* Add informations when hub'eau does not send a json
* Add migration generation distance to source
* Add contributions validated and publication date
* Add contributions type / category filters
* Add contributions manager
* Add contribution status
* Send mail to managers when contribution is created
* Send mail to contributor when contribution is created
* Add linked objects on contributions
* Add portal SEO informations
* Add min zoom, max zoom extent portal
* Add public portals on watershed types allowing to publish them


1.1.0        (2023-06-13)
-------------------------

**Enhancement**

* Add public portals on stream allowing to publish them
* Add PDFs administration of rivers
* Add flatpages module
* Add valorization POIs
* Add sensitivity module

**Bug fixes**

* Fix all point's marker was showing point to distance
* Fix form intervention, targets was not save


1.0.4        (2023-04-05)
-------------------------

**Enhancement**

* Add field classification water policy on rivers (#117)
* Add possibility to show geometries overprinted on topologies (#105)
* Add possibility to create attachment with external link
* Add command import hydrobiologie stations hubeau
* Upgrade api hubeau PC quality
* Add control type on Land module
* Add phases on Administrative Files
* Allow to create operations directly from creation of studies / follow ups / interventions / stations

**Bug fixes**

* Fix update attachments save buttons


1.0.3 (2022-12-15)
-------------------------

**Enhancement**

* Change secondary flow and habitat to multiselect field in description module
* Add fields to work : upstream and downstream bed impact, water impact
* Change vegetation strata field into a multiselect field

**Bug fixes**

* Display flow and source in stream detail
* Add flow filter in stream list
* Fix standalone intervention creation bug (#93)

**Documentation**

* Update doc installation
* Fix install doc with PostgreSQL not in Docker


1.0.2        (2022-05-22)
-------------------------

**Bug fixes**

* Fix ```./manage.py loaddem ...``` command by including postgis libraries


1.0.1    (2022-03-30)
-------------------------

**Enhancement**

* Add data source and flow to stream


1.0.0    (2022-03-10)
-------------------------

**Enhancement**

* Add chosen multiselect on usage types
* Remove unused fields from Station form
* Get more data from Hubeau (start and end measure dates, measure type)
* Change base buffer width
* Change module picto colors
* Improve map color settings
* Display layers for all modules

**Bug fixes**

* Display missing unit
* Fix pip-tools / pip incompatibility

0.9.9    (2022-01-25)
-------------------------

**Enhancement**

* External link to station opened in new window
* Add unit on distance fields
* Remove secondary information from station detail
* Add chosen on some multiselect fields

**Bug fixes**

* Remove unwanted padding on lists
* Fix filter in service for stations
* Remove useless restricted area filter, replaced by zoning filter

**Dependencies**

* Update to django-mapentity 7.0.6 and Geotrek 2.75.0


0.9.8    (2022-01-20)
-------------------------

**Features**

* Display distance from object to stream source

**Enhancement**

* Improve morpho display

**Bug fixes**

* Fix translations


0.9.7    (2021-12-23)
-------------------------

**Enhancement**

* Change module order
* Add help text for multiselect

**Bug fixes**

* Fix logo header for PDF
* Fix man-days and costs display
* Fix translations

**Dependencies**

* Update to django-mapentity 7.0.5 and Geotrek 2.74.1


0.9.6    (2021-12-09)
-------------------------

* Use mapentity standalone release
* Improve documentation
* Add source location on a stream
* Make cut topology simpler
* Add help message on how edit man-days cost
* Fix filters on intervention and follow-ups


0.9.5        (2021-11-08)
-------------------------

* Improve documentation
* Improve README, maintainers and brand mark policy


0.9.4        (2021-11-05)
-------------------------

* First code publication
