//
// Core
//
$(window).on('entity:map', function (e, data) {
    var map = data.map;

    // Show infrastructure layer in application maps
	var layer = new L.ObjectsLayer(null, {
		modelname: 'knowledge',
		style: L.Util.extend(window.SETTINGS.map.styles['knowledge'] || {}, { clickable:false }),
		pointToLayer: function (feature, latlng) {
			var knowledgeIcon = L.icon({
				iconUrl: feature.properties.type.pictogram,
				iconSize: [18, 18],
				iconAnchor: [9, 9],
			});
			return L.marker(latlng, {icon: knowledgeIcon});
		}
	});
	var url = window.SETTINGS.urls['knowledge_layer'];
	layer.load(url);
	map.layerscontrol.addOverlay(layer, tr('Knowledges'), tr('Knowledges'));
});
