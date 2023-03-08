MapEntity.streamsLayer = function buildStreamLayer(options) {
    var options = options || {};
    options.style = L.Util.extend(options.style || {}, window.SETTINGS.map.styles.stream);

    var streamsLayer = new L.ObjectsLayer(null, options);

    return streamsLayer;
};


//
// Stream layer
//
$(window).on('entity:map', function (e, data) {

    var modelname = 'stream';
    var layername = `${modelname}_layer`;
    var url = window.SETTINGS.urls[layername];
    var loaded_river = false;
    var map = data.map;

    // Show stream layer in application maps
    var layer = new L.ObjectsLayer(null, {
        modelname: modelname,
        style: L.Util.extend(window.SETTINGS.map.styles[modelname] || {}, { clickable:false }),
    });

    if (data.modelname != modelname){
	    map.layerscontrol.addOverlay(layer, tr('Streams'), tr('Streams'));
    };

    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        if (! loaded_river) {
            if (options.modelname == modelname && options.modelname != data.modelname) {
                e.layer.load(url);
                loaded_river = true;
            }
        }
    });

	var is_detail_view = /detail/.test(data.viewname);
    if (is_detail_view && (data.modelname == 'status' || data.modelname == 'morphology')) {
        map.on("layeradd", function(layer) {
            if (map.filecontrol === undefined){
                var pointToLayer = function (feature, latlng) {
                    return L.circleMarker(latlng, {style: window.SETTINGS.map.styles.filelayer})
                            .setRadius(window.SETTINGS.map.styles.filelayer.radius);
                },
                onEachFeature = function (feature, layer) {
                    if (feature.properties.name) {
                        layer.bindLabel(feature.properties.name);
                    }
                },
                filecontrol = L.Control.fileLayerLoad({
                    fitBounds: true,
                    position: 'topleft',
                    layerOptions: {style: window.SETTINGS.map.styles.filelayer,
                                   pointToLayer: pointToLayer,
                                   onEachFeature: onEachFeature,}

                });
                map.filecontrol = filecontrol;
                map.addControl(filecontrol);
            };
            if (map.cutControl === undefined){
                var cutControl = new L.Control.PointTopology(map, layer, {});

                var exclusive = new L.Control.ExclusiveActivation();
                map.cutControl = map.addControl(cutControl);
                exclusive.add(cutControl);

                cutControl.handler.on('enabled', function(){cutControl.handler.reset();}, this);
            }
        });

	}
	else {
        var distanceControl = new L.Control.PointDistance(map, layer, {});
        var exclusive = new L.Control.ExclusiveDistanceActivation();
        map.distanceControl = map.addControl(distanceControl);
        exclusive.add(distanceControl);
        distanceControl.handler.on('enabled', function(){
            if (! loaded_river) {
                map.addLayer(layer);
                loaded_river = true;
            }
            distanceControl.handler.reset();
           }, this);

	}
});
