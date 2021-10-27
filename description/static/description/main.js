//
// Core
//
$(window).on('entity:map', function (e, data) {

    var map = data.map;

    var managementLayers = [{url: window.SETTINGS.urls.land_layer, name: tr('Lands'), id: 'land'},
                            {url: window.SETTINGS.urls.status_layer, name: tr('Statuses'), id: 'status'},
                            {url: window.SETTINGS.urls.usage_layer, name: tr('Usages'), id: 'usage'},
                            {url: window.SETTINGS.urls.morphology_layer, name: tr('Morphologies'), id: 'morphology'}]
    managementLayers.map(function(el) {
        el.isActive = false;
        return el;
    });

    var colorspools = L.Util.extend({}, window.SETTINGS.map.colorspool);
    for (var i=0; i<managementLayers.length; i++) {
        var managementLayer = managementLayers[i];

        var style = L.Util.extend({clickable: false},
                                  window.SETTINGS.map.styles[managementLayer.id] || {});
        var layer = new L.ObjectsLayer(null, {
            modelname: managementLayer.name,
            style: style,
        });
        var nameHTML = '<span style="color: '+ style['color'] + ';">|</span>&nbsp;' + managementLayer.name;
        map.layerscontrol.addOverlay(layer, nameHTML, tr('Descriptions'));
    };
    map.on('layeradd', function(e){
        var options = e.layer.options || {'modelname': 'None'};
        for (var i=0; i<managementLayers.length; i++) {
            if (! managementLayers[i].isActive){
                if (options.modelname == managementLayers[i].name){
                    e.layer.load(managementLayers[i].url);
                    managementLayers[i].isActive = true;
                }
            }
        }
    });
});