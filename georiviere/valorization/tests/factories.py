import factory

from mapentity.tests.factories import PointFactory

from geotrek.authent.tests.factories import StructureFactory

from georiviere.valorization.models import POI, POIType, POICategory


class POICategoryFactory(factory.django.DjangoModelFactory):
    label = factory.Sequence(lambda n: f'POI category {n}')

    class Meta:
        model = POICategory


class POITypeFactory(factory.django.DjangoModelFactory):
    label = factory.Sequence(lambda n: f'POI type {n}')
    category = factory.SubFactory(POICategoryFactory)

    class Meta:
        model = POIType


class POIFactory(PointFactory):
    name = factory.Sequence(lambda n: f'name {n}')
    description = factory.Sequence(lambda n: f'description {n}')
    type = factory.SubFactory(POITypeFactory)
    structure = factory.SubFactory(StructureFactory)

    class Meta:
        model = POI
