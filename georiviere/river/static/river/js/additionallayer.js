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
        if (mapViewContext.additional_objects.includes('followups')) {
            var geojsonFollowUpMarkerOptions = {
                radius: 13,
                fillColor: "#fc7c14",
                color: "#fc7c14",
                weight: 3,
                opacity: 1,
                fillOpacity: 0.4
            };
            $.getJSON(window.SETTINGS.urls.stream_followups_layer, function (data) {
                var followups = new L.GeoJSON(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, geojsonFollowUpMarkerOptions);
                    }
                });
                map.addLayer(followups);

                followups.showEnumeration();
                $('.map-panel').addClass('other_object_enum_loaded');
            });
        }
        if (mapViewContext.additional_objects.includes('interventions')) {
            var geojsonInterventionMarkerOptions = {
                radius: 13,
                fillColor: "#dc3444",
                color: "#dc3444",
                weight: 3,
                opacity: 1,
                fillOpacity: 0.4
            };
            $.getJSON(window.SETTINGS.urls.stream_interventions_layer, function (data) {
                var interventions = new L.GeoJSON(data, {
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, geojsonInterventionMarkerOptions);
                    }
                });
                console.log(data);
                map.addLayer(interventions);

                interventions.showEnumeration();
                $('.map-panel').addClass('other_object_enum_loaded');
            });
        }
    }
    $('.map-panel').addClass('other_object_enum_loaded');

});