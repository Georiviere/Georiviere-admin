L.FieldStore.LineSnapStore = L.FieldStore.extend({

    _deserialize: function (value) {
        console.debug("Deserialize " + value);
        value = JSON.parse(value);
        value = value['geom'];
        return L.FieldStore.prototype._deserialize.call(this, value);
    },

    _serialize: function (layer) {
        var str = L.FieldStore.prototype._serialize.call(this, layer);

        var edited = layer.getLayers();
        if (edited.length === 0)
            return '';
        layer = edited[0];

        // Store snaplist
        if (layer.hasOwnProperty('_latlng')) {
            var n = 1;
        }
        else {
            var n = layer.getLatLngs().length;
        }
        var snaplist = new Array(n);
        if (layer.editing._poly === undefined) {
            if (layer.editing._markers !== undefined) {
                var marker = layer.editing._markers[0];
                if (marker.snap && marker.snap.properties && marker.snap.properties.pk)
                    snaplist[0] = marker.snap.properties.pk;
            }
        }
        if (layer.editing._snapper && layer.editing._snapper._markers) {
            var markers = layer.editing._snapper._markers.sort((a, b) => a._index - b._index)
            for (var i=0; i<n; i++) {
                var marker = markers[i];
                if (marker && marker.snap && marker.snap.properties && marker.snap.properties.pk)
                        snaplist[i] = marker.snap.properties.pk;
            }
        }

        var serialized = {geom: str,
                          snap: snaplist};
        console.debug("Serialized to " + JSON.stringify(serialized));
        return JSON.stringify(serialized);
    }
});


MapEntity.GeometryField.GeometryFieldStreamMixin = {
    /*
     * Load the stream layer in addition to another layer should be reusable.
     * (At least for the fix to propagate events)
     */
    buildStreamsLayer: function (objectsLayer) {
        var url_stream = window.SETTINGS.urls.stream_layer
        var streamsLayer = MapEntity.streamsLayer({style: {clickable: true}, no_draft: objectsLayer.modelname != 'stream'});
        streamsLayer.load(url_stream, true);

        this._map.addLayer(streamsLayer);

        // Propagate mouseover events, from the Stream layer (on top)
        // to the objects layer (below).
        // This fixes bug #680
        (function (){
            // Reference to the object layer hovered before the stream is hovered
            var overlapped = null;
            objectsLayer.on('mouseover', function (e) {
                overlapped = e.layer;
            });
            // On stream hover, propagate events to overlapped layer
            streamsLayer.on('mouseover mouseout', function (e) {
                if (overlapped !== null) {
                    e.layer = overlapped;
                    e.target = overlapped;
                    overlapped.fire(e.type, e);
                }
                if (e.type == 'mouseout') {
                    overlapped = null;
                }
            });
        })();
        return streamsLayer;
    },
};


MapEntity.GeometryField.GeometryFieldSnap = MapEntity.GeometryField.extend({
    options: {
        field_store_class: L.FieldStore.LineSnapStore
    },

    includes: MapEntity.GeometryField.GeometryFieldStreamMixin,

    initialize: function (options) {
        MapEntity.GeometryField.prototype.initialize.call(this, options);

        L.Handler.MarkerSnap.mergeOptions({
            snapDistance: window.SETTINGS.map.snap_distance
        });

        this._geometry = null;
        this._guidesLayers = [];
        this._streamsLayer = null;
        this._objectsLayer = null;
    },

    buildObjectsLayer: function () {
        this._objectsLayer = MapEntity.GeometryField.prototype.buildObjectsLayer(arguments);
        this._guidesLayers.push(this._objectsLayer);

        if (this.getModelName() != 'stream') {
            // If current model is not stream, we should add the stream layer
            // as a guide layer.
            this._streamsLayer = this.buildStreamsLayer(this._objectsLayer);
            this._guidesLayers.push(this._streamsLayer);
        }
        else {
            // It should like streams everywhere in the application
            var style = window.SETTINGS.map.styles.stream;
            this._objectsLayer.options.style = style;
            this._objectsLayer.options.styles.default = style;
        }

        if (this._geometry) {
            // null if not loaded (e.g. creation form)
            this._initSnap(this._geometry);
        }

        return this._objectsLayer;
    },

    guidesLayers: function () {
        return this._guidesLayers;
    },

    _initSnap: function (layer) {
        var handlerClass = null;
        if (layer instanceof L.Marker) {
            handlerClass = L.Handler.MarkerSnap;
            // Markers don't need draw edition because we don't need to modify multiple points we can move freely the Marker
            $('.leaflet-draw-edit-edit').hide()
            $('.leaflet-draw-edit-remove').hide()
        }
        else if (layer instanceof L.Polyline) {
            handlerClass = L.Handler.PolylineSnap;
            // We show draw edition in the case we used to draw a point and we change it for anything else
            $('.leaflet-draw-edit-edit').show()
            $('.leaflet-draw-edit-remove').show()
        }
        else {
            console.warn('Unsupported layer type for snap.');
            return;
        }
        layer.editing = new handlerClass(this._map, layer);
        for (var i=0, n=this._guidesLayers.length; i<n; i++) {
            layer.editing.addGuideLayer(this._guidesLayers[i]);
        }

        // Since snapping happens only once the geometry is created.
        // We are out of Leaflet.Draw.
        layer.on('move edit', function (e) {
            this.store.save(this.drawnItems);
        }, this);

        // On edition, show start and end markers as snapped
        this._map.on('draw:editstart', function (e) {
            if (layer.editing._snapper) {
                // The markers in snapper are kept between 2 modifications. Markers are added when we edit a layer.
                // We left an empty array, it will get all the old markers after.
                layer.editing._snapper._markers = [];
            }
            setTimeout(function () {
                if (!layer.editing) {
                    console.warn('Layer has no snap editing');
                    return;  // should never happen ;)
                }
                if (layer.editing._enabled === false) {
                    console.warn('Layer was not enable editing');
                    return;
                }
                var markers = layer.editing._markers;
                var first = markers[0],
                    last = markers[markers.length - 1];
                first.fire('move');
                last.fire('move');
            }, 0);
        });

    },

    onCreated: function (e) {
        MapEntity.GeometryField.prototype.onCreated.call(this, e);
        this._initSnap(e.layer);
    },

    load: function () {
        this._geometry = MapEntity.GeometryField.prototype.load.call(this);
        return this._geometry;
    }

});
