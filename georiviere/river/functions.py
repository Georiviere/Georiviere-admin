from django.contrib.gis.db.models.functions import GeomOutputGeoFunc


class ClosestPoint(GeomOutputGeoFunc):
    """ SQL Function class to get value from raster band (ST_VALUE) """
    geom_param_pos = (0, 1)
