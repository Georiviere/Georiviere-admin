import factory

from georiviere.tests.factories import BaseLineStringFactory
from river.models import Stream, Topology
from geotrek.authent.factories import StructureFactory


class StreamFactory(BaseLineStringFactory):
    name = factory.Sequence(lambda n: 'stream-%d' % n)
    structure = factory.SubFactory(StructureFactory)

    class Meta:
        model = Stream


class TopologyFactory(factory.django.DjangoModelFactory):
    stream = factory.SubFactory(StreamFactory)
    start_position = 0.1
    end_position = 0.9
    qualified = False

    class Meta:
        model = Topology
