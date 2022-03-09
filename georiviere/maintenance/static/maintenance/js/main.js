//
// Knowledge layer
//

$(window).on('entity:map', function (e, data) {
    var modelname = 'intervention';
    var layername = `${modelname}_layer`;
    var url = window.SETTINGS.urls[layername];
    var loaded_layer = false;
    var map = data.map;

    // Show station layer in application maps
       var layer = new L.ObjectsLayer(null, {
           modelname: modelname,
           style: L.Util.extend(window.SETTINGS.map.styles[modelname] || {}, { clickable:false }),
       });

    if (data.modelname != modelname){
        map.layerscontrol.addOverlay(layer, tr('Interventions'), tr('Maintenance'));
    };

    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        if (! loaded_layer) {
            if (options.modelname == modelname && options.modelname != data.modelname) {
                e.layer.load(url);
                loaded_layer = true;
            }
        }
    });
});
