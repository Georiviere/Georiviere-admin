SourceLocationField = L.GeometryField.extend({
    // This field is in charge of showing the source icon when editing

    initialize: function () {
        L.GeometryField.prototype.initialize.apply(this, arguments);
    },

    addTo: function (map) {
        L.GeometryField.prototype.addTo.apply(this, arguments);
        var $toolbar = $(this._drawControl._container);
        $toolbar.find('.leaflet-draw-draw-marker').attr('title', tr('Set the source location'));
        $toolbar.find('.leaflet-draw-edit-edit').attr('title', tr('Move the source location'));
        $toolbar.find('.leaflet-draw-edit-remove').attr('title', tr('Delete the source location'));
    },

    _controlDrawOptions: function () {
        var options = L.GeometryField.prototype._controlDrawOptions.call(this);
        options.draw.marker = {};
        options.draw.marker.icon = L.divIcon({className: 'source-location'});
        return options;
    },

    _setView: function () {
        // Do not affect map view on load (keep trek extent)
        // Override and do nothing.
    },

    onCreated: function (e) {
        // When user added a marker
        L.GeometryField.prototype.onCreated.apply(this, arguments);
        e.layer.setIcon(L.divIcon({className: 'source-location'}));
    },

    load: function () {
        // When instance multipoint is loaded
        var geometry = L.GeometryField.prototype.load.apply(this, arguments);
        if (geometry) {
            geometry.setIcon(L.divIcon({className: 'source-location'}));
        }
        return geometry;
    }
});