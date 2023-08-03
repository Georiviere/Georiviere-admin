/* To be removed when upgrading to mapentity 8.5.5 */

$(window).on('entity:map:list', function (e, data) {
    var map = data.map;

    map.addControl(new L.Control.Attribution());
});

