from django.contrib.gis.db.models.functions import GeoFunc, GeomOutputGeoFunc
from django.db.models import CharField, FloatField
from georiviere.fields import ElevationInfosField


class Area(GeoFunc):
    """ ST_Area postgis function """
    output_field = FloatField()


class Buffer(GeomOutputGeoFunc):
    """ ST_Buffer postgis function """
    pass


class GeometryType(GeoFunc):
    """ GeometryType postgis function """
    output_field = CharField()
    function = 'GeometryType'


class ElevationInfos(GeoFunc):
    function = 'ft_elevation_infos'
    geom_param_pos = (0, )
    output_field = ElevationInfosField()


class Length3D(GeoFunc):
    function = "ST_3DLENGTH"
    geom_param_pos = (0, )
    output_field = FloatField()


class LineSubString(GeomOutputGeoFunc):
    geom_param_pos = (0, )


class ClosestPoint(GeomOutputGeoFunc):
    """ SQL Function class to get closest point of an other geometry (ST_ClosestPoint) """
    geom_param_pos = (0, 1)
