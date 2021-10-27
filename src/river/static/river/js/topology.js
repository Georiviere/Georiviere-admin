L.Mixin.ActivableControl = {
    activable: function (activable) {
        /**
         * Allow to prevent user to activate the control.
         * (it is like setEnable(state), but ``enable`` word is used
         *  for handler already)
         */
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


L.Control.ExclusiveActivation = L.Class.extend({
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


L.Control.PointTopology = L.Control.extend({
    includes: L.Mixin.ActivableControl,

    statics: {
        TITLE: 'Cut',
    },

    options: {
        position: 'topleft',
    },

    initialize: function (map, guidesLayer, field, options) {
        L.Control.prototype.initialize.call(this, options);
        this.handler = new L.Handler.PointTopology(map, guidesLayer.layer, options);
        this.handler.on('added', this.toggle, this);
    },

    onAdd: function (map) {
        this._container = L.DomUtil.create('div', 'leaflet-draw leaflet-control leaflet-bar leaflet-control-zoom');
        var link = L.DomUtil.create('a', 'leaflet-control-zoom-out pointtopology-control', this._container);
        link.href = '#';
        link.title = L.Control.PointTopology.TITLE;

        L.DomEvent.addListener(link, 'click', L.DomEvent.stopPropagation)
                  .addListener(link, 'click', L.DomEvent.preventDefault)
                  .addListener(link, 'click', this.toggle, this);
        return this._container;
    }
});


L.Handler.PointTopology = L.Draw.Marker.extend({
    initialize: function (map, guidesLayer, options) {
        L.Draw.Marker.prototype.initialize.call(this, map, options);
        this._topoMarker = null;
        this._partTopo = null;
        this._guidesLayer = guidesLayer;
        map.on('draw:created', this._onDrawn, this);
    },

    reset: function() {
        if (this._topoMarker) {
            this._map.removeLayer(this._topoMarker);
        }
        this.fire('computed_topology', {topology: null});
    },

    restoreTopology: function (topo) {
        this._topoMarker = L.marker([topo.lat, topo.lng]);
        this._initMarker(this._topoMarker);
        if (topo.snap) {
            this._topoMarker.fire('move');  // snap to closest
        }
    },

    _onDrawn: function (e) {
        if (e.layerType === 'marker') {
            if (this._topoMarker !== null) {
                this._map.removeLayer(this._topoMarker);
            }

            this.fire('topo:created');
            this._topoMarker = L.marker(e.layer.getLatLng());
            this._initMarker(this._topoMarker);
        }
    },

    _initMarker: function (marker) {
        marker.addTo(this._map);
        L.DomUtil.addClass(marker._icon, 'marker-point');
        marker.editing = new L.Handler.MarkerSnap(this._map, marker);
        marker.editing.addGuideLayer(this._guidesLayer);
        marker.editing.enable();
        marker.on('snap', function (e) {
            var content = $('#form_topology');
            $('#lat').val(e.latlng.lat);
            $('#lng').val(e.latlng.lng);
            if (this._partTopo === null){
                var partTopo = new L.Polyline(L.GeometryUtil.extract(this._map, this._guidesLayer, L.GeometryUtil.locateOnLine(this._map, this._guidesLayer, e.latlng), 0),
                {color: 'red', weight: 5, opacity: 0.5});
                this._partTopo = partTopo;
                partTopo.addTo(this._map);
                this._map.on('layeradd', function (e) {
                    partTopo.bringToFront();
                });
            }
            this._partTopo.setLatLngs(
                L.GeometryUtil.extract(this._map,
                    this._guidesLayer,
                    L.GeometryUtil.locateOnLine(this._map, this._guidesLayer, e.latlng), 0));
            marker.bindPopup(content.html()).openPopup();
        }, this);
        marker.on('unsnap', function (e) {
                  marker.closePopup();
              }, this);
    },
});

