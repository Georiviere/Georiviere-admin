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
