$(window).on('detailmap:ready', function (e, data) {
    var map = data.map;
    var mapViewContext = getURLParameter('context');

    if (mapViewContext && mapViewContext.additional_objects) {
        if (mapViewContext.additional_objects.includes('usages')) {
            var geojsonUsageMarkerOptions = {
                radius: 13,
                fillColor: "#64340c",
                color: "#64340c",
                weight: 3,
                opacity: 1,
                fillOpacity: 0.4
            };
            $.getJSON(window.SETTINGS.urls.stream_usages_layer, function (data) {
                var usages = new L.GeoJSON(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, geojsonUsageMarkerOptions);
                    }
                });
                map.addLayer(usages);

                usages.showEnumeration();
                $('.map-panel').addClass('other_object_enum_loaded');
            });
        }
        if (mapViewContext.additional_objects.includes('studies')) {
            var geojsonStudyMarkerOptions = {
                radius: 13,
                fillColor: "#d43484",
                color: "#d43484",
                weight: 3,
                opacity: 1,
                fillOpacity: 0.4
            };
            $.getJSON(window.SETTINGS.urls.stream_studies_layer, function (data) {
                var usages = new L.GeoJSON(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, geojsonStudyMarkerOptions);
                    }
                });
                map.addLayer(usages);

                usages.showEnumeration();
                $('.map-panel').addClass('other_object_enum_loaded');
            });
        }
        if (mapViewContext.additional_objects.includes('knowledges')) {
            var geojsonKnowledgeMarkerOptions = {
                radius: 13,
                fillColor: "#208454",
                color: "#208454",
                weight: 3,
                opacity: 1,
                fillOpacity: 0.4
            };
            console.log(geojsonKnowledgeMarkerOptions);
            $.getJSON(window.SETTINGS.urls.stream_knowledges_layer, function (data) {
                var knowledges = new L.GeoJSON(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, geojsonKnowledgeMarkerOptions);
                    }
                });
                map.addLayer(knowledges);

                knowledges.showEnumeration();
                $('.map-panel').addClass('other_object_enum_loaded');
            });
        }
    }
});