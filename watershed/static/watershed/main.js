$(window).on('entity:map', function (e, data) {

    var map = data.map;

    var watershedLayers = [];
    watershedLayers = watershedLayers.concat(window.SETTINGS.map['watershed_types']);

    watershedLayers.map(function(el) {
        el.isActive = false;
        return el;
    })

    for (var i=0; i<watershedLayers.length; i++) {
        var watershedLayer = watershedLayers[i];
        var style = L.Util.extend({clickable: false},
                                  window.SETTINGS.map.styles[watershedLayer.id] || {});
        style['color'] = watershedLayer.color;
        style['fillColor'] = watershedLayer.color;
        var layer = new L.ObjectsLayer(null, {
                indexing: false,
                modelname: watershedLayer.name,
                style: style,
        });
        var nameHTML = '<span style="color: '+ style['color'] + ';">&#x2B24;</span>&nbsp;' + watershedLayer.name;
        map.layerscontrol.addOverlay(layer, nameHTML, tr('Zoning'));
    };

    map.on('layeradd', function(e){
        var options = e.layer.options || {'modelname': 'None'};
        for (var i=0; i<watershedLayers.length; i++) {
            if (! watershedLayers[i].isActive){
                if (options.modelname == watershedLayers[i].name){
                    e.layer.load(watershedLayers[i].url);
                    watershedLayers[i].isActive = true;
                }
            }
        }
    });
});