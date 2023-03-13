L.Mixin.ActivableDistanceControl = {
    activable: function (activable) {
        this._activable = activable;
        if (this._container) {
            if (activable)
                L.DomUtil.removeClass(this._container, 'control-disabled');
            else
                L.DomUtil.addClass(this._container, 'control-disabled');
        }
        this.handler.on('enabled', function (e) {
            L.DomUtil.addClass(this._container, 'enabled');
        }, this);
        this.handler.on('disabled', function (e) {
            L.DomUtil.removeClass(this._container, 'enabled');
        }, this);
    },

    setState: function (state) {
        if (state) {
            this.handler.enable.call(this.handler);
            this.handler.fire('enabled');
        }
        else {
            this.handler.disable.call(this.handler);
            this.handler.fire('disabled');
        }
    },

    toggle: function() {
        this._activable = !!this._activable;  // from undefined to false :)

        if (!this._activable)
            return;  // do nothing if not activable

        this.setState(!this.handler.enabled());
    },
};


L.Control.ExclusiveDistanceActivation = L.Class.extend({
    initialize: function () {
        this._controls = [];
    },

    add: function (control) {
        this._controls.push(control);
        var self = this;
        control.activable(true);
        control.handler.on('enabled', function (e) {
            // When this control is enabled, activate this one,
            // disable the others and prevent them to be activable.
            $.each(self._controls, function (i, c) {
                if (c != control) {
                    c.activable(false);
                }
            });
        }, this);

        control.handler.on('disabled', function (e) {
            // When this control is disabled, re-enable the others !
            // Careful, this will not take care of previous state :)
            $.each(self._controls, function (i, c) {
                c.activable(true);
            });
        }, this);
    },
});


L.Control.PointDistance = L.Control.extend({
    includes: L.Mixin.ActivableDistanceControl,

    statics: {
        TITLE: 'Distance to source',
    },

    options: {
        position: 'topleft',
    },

    initialize: function (map, guidesLayer, field, options) {
        L.Control.prototype.initialize.call(this, options);
        this.handler = new L.Handler.PointDistance(map, guidesLayer.layer, options);
        this.handler.on('added', this.toggle, this);
    },

    onAdd: function (map) {
        this._container = L.DomUtil.create('div', 'leaflet-draw leaflet-control leaflet-bar leaflet-control-zoom');
        var link = L.DomUtil.create('a', 'leaflet-control-zoom-out distance-control', this._container);
        link.href = '#';
        link.title = L.Control.PointDistance.TITLE;

        L.DomEvent.addListener(link, 'click', L.DomEvent.stopPropagation)
                  .addListener(link, 'click', L.DomEvent.preventDefault)
                  .addListener(link, 'click', this.toggle, this);
        return this._container;
    }
});


L.Handler.PointDistance = L.Draw.Marker.extend({
    initialize: function (map, guidesLayer, options) {
        L.Draw.Marker.prototype.initialize.call(this, map, options);
        this._guidesLayer = guidesLayer;
        this._helpText = tr("Click map to place marker, get the distance to the nearest stream's source.");
        this._distanceMarker = null;
        map.on('draw:created', this._onDrawn, this);
    },

	addHooks: function () {
		L.Draw.Marker.prototype.addHooks.call(this);
		if (this._map) {
			this._tooltip.updateContent({ text: this._helpText });
        }
    },

    reset: function() {
        if (this._distanceMarker) {
            this._map.removeLayer(this._distanceMarker);
        }
    },

    _onDrawn: function (e) {
        if (e.layerType === 'marker') {
            if (this._distanceMarker !== null) {
                this._map.removeLayer(this._distanceMarker);
            }

            this.fire('distance:created');
            this._distanceMarker = L.marker(e.layer.getLatLng());
            this._getDistance(this._distanceMarker);
        }
    },

    _getDistance: function (marker) {
        marker.addTo(this._map);
        $.ajax({
            url: window.SETTINGS.urls['distance_to_source'],
            type: 'GET',
            dataType: 'json',
            data: {
            "lat_distance": marker._latlng.lat,
             "lng_distance": marker._latlng.lng
             },
            success: function(data) {
                this._helpText = data;

                marker.bindPopup("<div><b>"+ tr('Distance to source') + " : " + data['distance'] + " m</b></div>").openPopup()
            }
        });
        this._map.on('popupclose', function(e) {

            if (e.popup._source._map.hasLayer(marker)) {
                e.popup._source._map.removeLayer(marker);
            }


        });
    },
});
