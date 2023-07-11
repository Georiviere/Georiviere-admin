import factory
from django.conf import settings
from django.contrib.gis.geos import Polygon

from .. import models

from geotrek.zoning.tests.factories import bbox_split_srid_2154


geom_spatial_extent_iter = bbox_split_srid_2154(settings.SPATIAL_EXTENT, by_x=4, by_y=4, cycle=True)


class PortalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Portal

    name = factory.Sequence(lambda n: "Portal %s" % n)
    website = factory.Sequence(lambda n: "https://georiviere-{}.fr".format(n))
    spatial_extent = factory.Sequence(lambda _: Polygon.from_bbox(next(geom_spatial_extent_iter)))

    @factory.post_generation
    def map_base_layers(obj, create, extracted=None, **kwargs):
        if create:
            MapBaseLayerFactory.create(portal=obj)


class MapBaseLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MapBaseLayer

    label = factory.Sequence(lambda n: f'Label {n}')
    order = factory.Sequence(lambda n: n)
    url = factory.Sequence(lambda n: f'http://foo{n}.fr')
    attribution = factory.Sequence(lambda n: f'Attribution {n}')
    portal = factory.SubFactory(PortalFactory)


class GroupMapLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MapGroupLayer

    label = factory.Sequence(lambda n: f'Label {n}')
    portal = factory.SubFactory(PortalFactory)
