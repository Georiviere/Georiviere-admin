from django.contrib.gis.db.models.functions import GeoFunc
from django.contrib.gis.db.models import GeometryField
from django.db.models import FloatField

from georiviere.fields import ElevationInfosField


class ElevationInfos(GeoFunc):
    function = 'ft_elevation_infos'
    geom_param_pos = (0, )
    output_field = ElevationInfosField()


class Length3D(GeoFunc):
    function = "ST_3DLENGTH"
    geom_param_pos = (0, )
    output_field = FloatField()


class LineSubString(GeoFunc):
    function = 'ST_Line_Substring'
    geom_param_pos = (0, )
    output_field = GeometryField()
