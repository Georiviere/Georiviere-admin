MapEntity.streamsLayer = function buildStreamLayer(options) {
    var options = options || {};
    options.style = L.Util.extend(options.style || {}, window.SETTINGS.map.styles.stream);

    var streamsLayer = new L.ObjectsLayer(null, options);

    return streamsLayer;
};


//
// Core
//
$(window).on('entity:map', function (e, data) {
    var map = data.map;

    // Show stream layer in application maps
	var layer = new L.ObjectsLayer(null, {
		modelname: 'stream',
		style: L.Util.extend(window.SETTINGS.map.styles['stream'] || {}, { clickable:false }),
		pointToLayer: function (feature, latlng) {
			return L.marker(latlng, {icon: infrastructureIcon});
		}
	});
	var url = window.SETTINGS.urls['stream_layer'];
	layer.load(url);
	map.layerscontrol.addOverlay(layer, tr('Streams'), tr('Streams'));
	var is_detail_view = /detail/.test(data.viewname);
    if (is_detail_view && (data.modelname == 'status' || data.modelname == 'morphology')) {
        map.on("layeradd", function(layer) {
            if (map.cutControl === undefined){
                var cutControl = new L.Control.PointTopology(map, layer, {});

                var exclusive = new L.Control.ExclusiveActivation();
                map.cutControl = map.addControl(cutControl);
                exclusive.add(cutControl);

                cutControl.handler.on('enabled', function(){cutControl.handler.reset();}, this);
            }
        });

	}
});
