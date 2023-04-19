//
// Station layer
//
$(window).on('entity:map', function (e, data) {
    var modelname = 'poiknowledge';
    var layername = `${modelname}_layer`;
    var url = window.SETTINGS.urls[layername];
    var loaded_poiknowledge = false;
    var map = data.map;

    // Show station layer in application maps
    var layer = new L.ObjectsLayer(null, {
        modelname: modelname,
        style: L.Util.extend(window.SETTINGS.map.styles[modelname] || {}, { clickable:false }),
    });

    if (data.modelname != modelname){
        map.layerscontrol.addOverlay(layer, tr('POI knowledges'), tr('POI knowledges'));
    };

    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        if (! loaded_poiknowledge) {
            if (options.modelname == modelname && options.modelname != data.modelname) {
                e.layer.load(url);
                loaded_poiknowledge = true;
            }
        }
    });
});
