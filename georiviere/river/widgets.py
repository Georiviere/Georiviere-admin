import json

from mapentity.widgets import MapWidget
from leaflet.forms.widgets import LeafletWidget


class SnappedLineStringWidget(MapWidget):
    geometry_field_class = 'MapEntity.GeometryField.GeometryFieldSnap'

    def serialize(self, value):
        geojson = super().serialize(value)
        snaplist = []
        if value:
            snaplist = [None for c in range(len(value.coords))]
        value = {'geom': geojson, 'snap': snaplist}
        return json.dumps(value)

    def deserialize(self, value):
        if isinstance(value, str) and value:
            value = json.loads(value)
            value = value['geom']
        return super().deserialize(value)


class SourceLocationWidget(MapWidget):
    """Widget for source location"""

    geometry_field_class = 'SourceLocationField'
    target_map = 'geom'
    geom_type = 'POINT'
