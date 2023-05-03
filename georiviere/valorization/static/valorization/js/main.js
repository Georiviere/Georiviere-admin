//
// Station layer
//
$(window).on('entity:map', function (e, data) {
    var modelname = 'poi';
    var layername = `${modelname}_layer`;
    var url = window.SETTINGS.urls[layername];
    var loaded_poi = false;
    var map = data.map;

    // Show station layer in application maps
    var layer = new L.ObjectsLayer(null, {
        modelname: modelname,
        style: L.Util.extend(window.SETTINGS.map.styles[modelname] || {}, { clickable:false }),
    });

    if (data.modelname != modelname){
        map.layerscontrol.addOverlay(layer, tr('POIs'), tr('POIs'));
    };

    map.on('layeradd', function (e) {
        var options = e.layer.options || { 'modelname': 'None' };
        if (! loaded_poi) {
            if (options.modelname == modelname && options.modelname != data.modelname) {
                e.layer.load(url);
                loaded_poi = true;
            }
        }
    });
});

function toggle_hidden_types() {
    var categories_types = JSON.parse($('#poi-categories-types').text());
    var category = $('#id_category').val();
    var types_chosen = categories_types[category];
    var options = $('#id_type option');
    options.each(function() {
        var id_type = $(this).val();
        if (id_type && $.inArray(parseInt(id_type), types_chosen) == -1)
        {
            $(this).prop('hidden', true);
            $(this).removeProp('selected')
        }
        else {
            $(this).removeProp('hidden');
        }
    });
}

$(window).on('entity:view:add entity:view:update', function (e, data) {
    if (data.modelname == 'poi') {
        toggle_hidden_types();
        // Refresh poi types by category
        $('#id_category').change(function () {
            toggle_hidden_types();
        });
    }
    return;
});
