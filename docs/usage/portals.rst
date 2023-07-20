Valorization
============

To generate a good structure of your portal Georiviere, firstly you need to configurate in admin
portals, map base layers, layers and groups.

Portal
------

Fields :

* Name
* Web site
* Title
* Description
* Main color
* Min zoom on the map of your portal
* Max zoom on the map of your portal
* Spatial extent of your portal

Map Base Layers
---------------

Map base layers are linked with one unique portal

* Label
* Url
* Min zoom of this map base layer
* Max zoom of this map base layer
* Attribution
* Portal
* Order


Layers
------

Layers are generated for each type of element you could add on your portal web site :

* Contributions
* Sensitivity
* Districts
* Cities
* POIs (each category has it layer)
* Streams
* Watersheds

Firstly, you need to create your portal before accessing layers.
Then, you will be able to add them in a group of layer, change its labels...

If you create a new category of poi, a new layer is generated.

The fields of layers are :

* Label
* Group
* Active by default
* Style
* Order
* Hidden

Style can be changed following the documentation of leaflet,
for example:
`{"fillColor": "#d4b485"}`

(https://leafletjs.com/reference.html#path-stroke)

When a layer is hidden, the layer is not used in the portal.

The label is used in the portal and will be shown it.

Groups
------

You can create as many group as you need and can add layers in the group.

When a layer is not assigned to a group, the layer is groupped in a default group.

The fields of groups are :

* Label
* Order

---------------


It's better to create everything in this order :

* Create your portal
* Create your base layers
* Create the groups

* Modify the generated layers


