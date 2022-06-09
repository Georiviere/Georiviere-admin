=========
CHANGELOG
=========

1.0.2+dev    (XXXX-XX-XX)
-------------------------

**Bug fixes**

* Add flow info and filter

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
