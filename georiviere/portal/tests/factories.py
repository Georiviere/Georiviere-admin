import factory

from .. import models


class MapBaseLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MapBaseLayer

    label = factory.Sequence(lambda n: f'Label {n}')
    order = factory.Sequence(lambda n: n)
    url = factory.Sequence(lambda n: f'http://foo{n}.fr')
    attribution = factory.Sequence(lambda n: f'Attribution {n}')
    bounds = factory.Sequence(lambda n: f'[{n}, {n+2}, {n+1}, {n+3}]')


class PortalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Portal

    name = factory.Sequence(lambda n: "Portal %s" % n)
    website = factory.Sequence(lambda n: "https://georiviere-{}.fr".format(n))

    @factory.post_generation
    def map_base_layers(obj, create, extracted=None, **kwargs):
        if create:
            if extracted:
                obj.map_base_layers.set(extracted)
            else:
                obj.map_base_layers.add(MapBaseLayerFactory.create())
