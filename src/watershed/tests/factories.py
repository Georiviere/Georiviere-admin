from django.conf import settings
from django.contrib.gis.geos import Polygon, MultiPolygon
from factory import django, fuzzy, Sequence, SubFactory
from mapentity.helpers import bbox_split_srid_2154

from .. import models

geom_watershed_iter = bbox_split_srid_2154(settings.SPATIAL_EXTENT, by_x=4, by_y=4, cycle=True)


class WatershedTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.WatershedType

    name = Sequence(lambda n: "Watershed type name %s" % n)
    color = fuzzy.FuzzyText('#', length=6, chars='abcdef0123456789')


class WatershedFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Watershed

    name = Sequence(lambda n: "Watershed name %s" % n)
    eid = fuzzy.FuzzyInteger(0, 9999)
    geom = Sequence(lambda _: MultiPolygon(Polygon.from_bbox(next(geom_watershed_iter)), srid=settings.SRID))
    watershed_type = SubFactory(WatershedTypeFactory)
