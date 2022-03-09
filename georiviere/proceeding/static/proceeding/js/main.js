//
// Knowledge layer
//

$(window).on('entity:map', function (e, data) {
    var modelname = 'proceeding';
    var layername = `${modelname}_layer`;
    var url = window.SETTINGS.urls[layername];
    var loaded_proceeding = false;
    var map = data.map;

    // Show station layer in application maps
       var layer = new L.ObjectsLayer(null, {
           modelname: modelname,
           style: L.Util.extend(window.SETTINGS.map.styles[modelname] || {}, { clickable:false }),
       });

    if (data.modelname != modelname){
        map.layerscontrol.addOverlay(layer, tr('Proceeding'), tr('Proceeding'));
    };

    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        if (! loaded_proceeding) {
            if (options.modelname == modelname && options.modelname != data.modelname) {
                e.layer.load(url);
                loaded_proceeding = true;
            }
        }
    });
});
