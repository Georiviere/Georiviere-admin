Modules
=======

Several modules are available in Georiviere, to display and edit professional content:

* Streams
* Descriptions (usage, land, morphology, status)
* Knowledges (vegetation, work or other knowledges)
* Follow-ups for a given knowledge
* Stations (hydrometric, temperature, physico-chemical quality or other types)
* Studies
* Finance and administrative files
* Proceedings
* Interventions (on knowledges)

In a content detail page, nearby other contents are displayed.

Streams
-------

Streams is a line with a source location.

Descriptions
------------

Four description models are available:

- usage
- land
- morphology
- status

Land and morphology have both a geom relative to a stream, and are created along to a stream on its creation.
They can be cut to edit more precisely their attributes.

Usage and status are both standalone geometry and can be whatever point, line or polygon.

Knowledges
----------

Knowledges can be a point, line or polygon about a stream, of vegetation, work or other type.

Vegetation and work type knowledges have specific fields.

Follow-ups
----------

Follow-ups can be added to a knowledge, to take regular readings related to this knowledge.

Stations
--------

Stations are points of measures, but they can be line or polygon too.
Tracked parameters can be added to a station, with their name, measure and transmission frequency, etc.

Station of hydrometric, temperature, physico-chemical quality can be imported from Hub'Eau API.

Studies
-------

A study is just a content with authors and year.

Finance and administrative files
--------------------------------

Estimated or actual costs, fundings, or organisations involved in a project can be filled in an administrative file.

Every content in georiviere can be linked to an administrative file with operation,
and for each you can edit its estimated, material, sub-contracting or man-days costs.

Proceedings
-----------

A proceeding can list all juridic events related to it.

Interventions
-------------

Intervention is a maintenance intervention related to a follow-up.
