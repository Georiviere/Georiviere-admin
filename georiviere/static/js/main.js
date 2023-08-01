$(window).on('entity:map:list', function (e, data) {
    var map = data.map;

    map.addControl(new L.Control.Attribution());
});

